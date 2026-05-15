"""
Open-Meteo weather data connector.

Fetches historical and current weather data for representative stations
across a biodiversity region. Free API, no authentication required.
API docs: https://open-meteo.com/en/docs
"""

import logging
from datetime import datetime, timedelta
from typing import Any

import httpx

from backend.connectors.base import DataConnector
from backend.regions import get_region, Region

logger = logging.getLogger(__name__)

OPEN_METEO_HISTORICAL_URL = "https://archive-api.open-meteo.com/v1/archive"
OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def _get_stations(region: Region) -> list[dict[str, Any]]:
    """Convert Region.stations to the dict format used by fetch methods."""
    return [
        {"name": s.name, "lat": s.lat, "lon": s.lon, "state": s.state}
        for s in region.stations
    ]


class OpenMeteoConnector(DataConnector):
    """Connector for Open-Meteo weather data."""

    def __init__(self, region_id: str | None = None):
        self._region = get_region(region_id)
        self._stations = _get_stations(self._region)

    def get_source_name(self) -> str:
        return "Open-Meteo"

    def fetch(
        self,
        bbox: tuple | None = None,
        start_date: str = "",
        end_date: str = "",
    ) -> list[dict[str, Any]]:
        """
        Fetch historical weather data for Western Ghats stations.

        Args:
            bbox: Not used (we use predefined stations).
            start_date: ISO date (YYYY-MM-DD). Defaults to 30 days ago.
            end_date: ISO date (YYYY-MM-DD). Defaults to yesterday.

        Returns:
            List of daily weather observation records.
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        all_records = []
        for station in self._stations:
            records = self._fetch_station(station, start_date, end_date)
            all_records.extend(records)

        logger.info(
            f"Open-Meteo: fetched {len(all_records)} weather records "
            f"from {len(self._stations)} stations."
        )
        return all_records

    def _fetch_station(
        self,
        station: dict,
        start_date: str,
        end_date: str,
    ) -> list[dict[str, Any]]:
        """Fetch weather data for a single station."""
        params = {
            "latitude": station["lat"],
            "longitude": station["lon"],
            "start_date": start_date,
            "end_date": end_date,
            "daily": ",".join([
                "temperature_2m_max",
                "temperature_2m_min",
                "temperature_2m_mean",
                "precipitation_sum",
                "rain_sum",
                "windspeed_10m_max",
                "relative_humidity_2m_mean",
                "et0_fao_evapotranspiration",
            ]),
            "timezone": self._region.timezone,
        }

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.get(OPEN_METEO_HISTORICAL_URL, params=params)
                response.raise_for_status()

            data = response.json()
            daily = data.get("daily", {})
            dates = daily.get("time", [])

            records = []
            for i, date in enumerate(dates):
                records.append({
                    "latitude": station["lat"],
                    "longitude": station["lon"],
                    "station_name": station["name"],
                    "date": date,
                    "temperature_max": daily.get("temperature_2m_max", [None])[i],
                    "temperature_min": daily.get("temperature_2m_min", [None])[i],
                    "temperature_mean": daily.get("temperature_2m_mean", [None])[i],
                    "precipitation_sum": daily.get("precipitation_sum", [None])[i],
                    "rain_sum": daily.get("rain_sum", [None])[i],
                    "windspeed_max": daily.get("windspeed_10m_max", [None])[i],
                    "humidity_mean": daily.get("relative_humidity_2m_mean", [None])[i],
                    "et0_fao": daily.get("et0_fao_evapotranspiration", [None])[i],
                })

            return records

        except httpx.HTTPStatusError as e:
            logger.error(
                f"Open-Meteo error for {station['name']}: "
                f"{e.response.status_code}"
            )
            return []
        except Exception as e:
            logger.error(f"Open-Meteo fetch failed for {station['name']}: {e}")
            return []

    def fetch_current(self) -> list[dict[str, Any]]:
        """Fetch current weather conditions for all stations (single batch request)."""
        # Open-Meteo supports comma-separated coordinates for batch queries
        lats = ",".join(str(s["lat"]) for s in self._stations)
        lons = ",".join(str(s["lon"]) for s in self._stations)

        params = {
            "latitude": lats,
            "longitude": lons,
            "current": ",".join([
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "wind_speed_10m",
                "wind_direction_10m",
            ]),
            "timezone": self._region.timezone,
        }

        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(OPEN_METEO_FORECAST_URL, params=params)
                response.raise_for_status()

            results = response.json()
            # Batch response is a list of station results
            if not isinstance(results, list):
                results = [results]

            all_records = []
            for i, station in enumerate(self._stations):
                if i >= len(results):
                    break
                current = results[i].get("current", {})
                all_records.append({
                    "station_name": station["name"],
                    "latitude": station["lat"],
                    "longitude": station["lon"],
                    "state": station["state"],
                    "temperature": current.get("temperature_2m"),
                    "humidity": current.get("relative_humidity_2m"),
                    "precipitation": current.get("precipitation"),
                    "wind_speed": current.get("wind_speed_10m"),
                    "wind_direction": current.get("wind_direction_10m"),
                    "time": current.get("time"),
                })

            logger.info(f"Open-Meteo: fetched current conditions for {len(all_records)} stations.")
            return all_records
        except Exception as e:
            logger.error(f"Open-Meteo current weather batch request failed: {e}")
            return []
