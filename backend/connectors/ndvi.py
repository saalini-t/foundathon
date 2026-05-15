"""
NDVI (Normalized Difference Vegetation Index) data connector.

For hackathon MVP: generates realistic NDVI data based on regional
ecology, location and seasonal patterns. In production, this would use
Google Earth Engine (GEE) Python API with Sentinel-2/MODIS imagery.

The simulated data captures real ecological patterns per region:
- Baseline NDVI driven by region climate profile
- Seasonal modulation (wet/dry season)
- Latitude-dependent gradient where applicable
"""

import logging
import math
from datetime import datetime, timedelta
from typing import Any

import numpy as np

from backend.connectors.base import DataConnector
from backend.config import get_settings
from backend.regions import get_region, Region

logger = logging.getLogger(__name__)

# Grid resolution: ~0.1° cells (~11km)
GRID_RESOLUTION = 0.1


def _ndvi_baseline(lat: float, lon: float, region: Region) -> float:
    """
    Compute baseline mean NDVI for a location using the region's climate profile.
    """
    cp = region.climate
    # If region has a deciduous threshold, create a latitude gradient
    if cp.ndvi_deciduous_threshold_lat is not None:
        south, north = cp.lat_range
        if lat < cp.ndvi_deciduous_threshold_lat:
            base = cp.ndvi_wet  # evergreen / wetter zone
        else:
            base = cp.ndvi_dry  # deciduous / drier zone
    else:
        # Uniform canopy (e.g. Amazon, Borneo) — small lat gradient
        base = cp.ndvi_mean

    # Slight west-slope / coast effect: cells in western 1/3 of bbox get boost
    bbox_w, _, bbox_e, _ = region.bbox
    west_third = bbox_w + (bbox_e - bbox_w) / 3
    if lon < west_third:
        base += 0.03

    return min(base, 0.95)


def _ndvi_seasonal(month: int, lat: float, region: Region) -> float:
    """
    Seasonal NDVI modulation based on the region's wet/dry calendar.
    """
    cp = region.climate
    # Determine peak month (centre of wet season)
    wet_months = [m for m in range(1, 13) if m not in cp.dry_months]
    if wet_months:
        peak_month = wet_months[len(wet_months) // 2]
    else:
        peak_month = 8

    phase = 2 * math.pi * (month - peak_month) / 12.0
    # Amplitude higher in deciduous / seasonal regions
    if cp.ndvi_deciduous_threshold_lat is not None and lat > cp.ndvi_deciduous_threshold_lat:
        amplitude = 0.12
    else:
        amplitude = 0.06
    return amplitude * math.cos(phase)


class NDVIConnector(DataConnector):
    """
    NDVI data connector — simulates monthly NDVI composites for
    regional grid cells using ecological models.

    In production, replace with GEE API calls:
        ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
        .filterBounds(geometry).map(compute_ndvi).median()
    """

    def __init__(self, region_id: str | None = None):
        self.settings = get_settings()
        self._region = get_region(region_id)
        self._rng = np.random.default_rng(42)

    def get_source_name(self) -> str:
        return "NDVI (Simulated from Sentinel-2 patterns)"

    def fetch(
        self,
        bbox: tuple | None = None,
        start_date: str = "",
        end_date: str = "",
    ) -> list[dict[str, Any]]:
        """
        Generate monthly NDVI composites for grid cells.

        Returns one record per grid cell per month within the date range.
        """
        if bbox is None:
            bbox = self._region.bbox
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        start = datetime.strptime(start_date[:10], "%Y-%m-%d")
        end = datetime.strptime(end_date[:10], "%Y-%m-%d")

        records = []
        # Generate month list
        current = start.replace(day=1)
        while current <= end:
            month_records = self._generate_month(bbox, current.year, current.month)
            records.extend(month_records)
            # Advance to next month
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1)
            else:
                current = current.replace(month=current.month + 1)

        logger.info(f"NDVI: generated {len(records)} grid-cell-month records.")
        return records

    def _generate_month(
        self, bbox: tuple, year: int, month: int
    ) -> list[dict[str, Any]]:
        """Generate NDVI values for all grid cells for one month."""
        west, south, east, north = bbox
        records = []

        lat = south
        while lat < north:
            lon = west
            while lon < east:
                center_lat = round(lat + GRID_RESOLUTION / 2, 4)
                center_lon = round(lon + GRID_RESOLUTION / 2, 4)

                # Only include cells within region zone bands
                if self._in_region_zone(center_lat, center_lon):
                    base = _ndvi_baseline(center_lat, center_lon, self._region)
                    seasonal = _ndvi_seasonal(month, center_lat, self._region)
                    noise = self._rng.normal(0, 0.03)
                    ndvi_mean = float(np.clip(base + seasonal + noise, 0.05, 0.95))

                    # Std dev: lower in dense forest, higher in mixed areas
                    ndvi_std = float(
                        np.clip(0.04 + self._rng.normal(0, 0.01), 0.01, 0.15)
                    )
                    ndvi_min = float(np.clip(ndvi_mean - 2 * ndvi_std, 0.0, ndvi_mean))
                    ndvi_max = float(np.clip(ndvi_mean + 2 * ndvi_std, ndvi_mean, 1.0))

                    cell_id = f"{center_lat:.2f}_{center_lon:.2f}"

                    records.append({
                        "cell_id": cell_id,
                        "center_lat": center_lat,
                        "center_lon": center_lon,
                        "year": year,
                        "month": month,
                        "date": f"{year}-{month:02d}-01",
                        "ndvi_mean": round(ndvi_mean, 4),
                        "ndvi_std": round(ndvi_std, 4),
                        "ndvi_min": round(ndvi_min, 4),
                        "ndvi_max": round(ndvi_max, 4),
                        "pixel_count": int(self._rng.integers(80, 120)),
                        "cloud_free_pct": round(
                            float(np.clip(self._rng.normal(0.78, 0.12), 0.3, 1.0)), 2
                        ),
                    })
                lon += GRID_RESOLUTION
            lat += GRID_RESOLUTION

        return records

    def _in_region_zone(self, lat: float, lon: float) -> bool:
        """
        Check if a cell falls within one of the region's NDVI zone bands.
        Each zone defines a lat/lon band that represents actual habitat.
        """
        for z in self._region.ndvi_zones:
            if z.lat_min <= lat < z.lat_max and z.lon_min <= lon <= z.lon_max:
                return True
        return False

    def get_grid_cells(self) -> list[dict[str, Any]]:
        """Return the list of grid cells covering the active region."""
        bbox = self._region.bbox
        west, south, east, north = bbox
        cells = []
        lat = south
        while lat < north:
            lon = west
            while lon < east:
                center_lat = round(lat + GRID_RESOLUTION / 2, 4)
                center_lon = round(lon + GRID_RESOLUTION / 2, 4)
                if self._in_region_zone(center_lat, center_lon):
                    cells.append({
                        "cell_id": f"{center_lat:.2f}_{center_lon:.2f}",
                        "center_lat": center_lat,
                        "center_lon": center_lon,
                        "lat_min": round(lat, 4),
                        "lat_max": round(lat + GRID_RESOLUTION, 4),
                        "lon_min": round(lon, 4),
                        "lon_max": round(lon + GRID_RESOLUTION, 4),
                    })
                lon += GRID_RESOLUTION
            lat += GRID_RESOLUTION
        return cells

    def get_latest_ndvi(self) -> list[dict[str, Any]]:
        """Get the most recent month's NDVI for all grid cells."""
        now = datetime.now()
        # Use previous month as "latest available" (satellite processing delay)
        if now.month == 1:
            year, month = now.year - 1, 12
        else:
            year, month = now.year, now.month - 1

        start = f"{year}-{month:02d}-01"
        end = f"{year}-{month:02d}-28"
        return self.fetch(start_date=start, end_date=end)
