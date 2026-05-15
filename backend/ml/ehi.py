"""
Ecosystem Health Index (EHI) Scoring
=====================================
Weighted composite index (0-100) per grid cell combining:

  Sub-Index                Weight    Source
  ─────────────────────────────────────────────
  Vegetation Health (VH)    0.25    NDVI
  Forest Integrity (FI)     0.20    NDVI baseline as proxy
  Biodiversity Richness     0.20    Species count from GBIF
  Climate Stability (CS)    0.15    Weather anomalies
  Air Quality (AQ)          0.10    Placeholder (no OpenAQ yet)
  Fire Disturbance (FD)     0.10    FIRMS fire frequency

Score 80-100: Excellent — pristine ecosystem
Score 60-79:  Good — minor pressures
Score 40-59:  Fair — moderate degradation
Score 20-39:  Poor — significant degradation
Score 0-19:   Critical — severe degradation
"""

import logging
from datetime import datetime, timedelta
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)

# Sub-index weights
WEIGHTS = {
    "vegetation_health": 0.25,
    "forest_integrity": 0.20,
    "biodiversity_richness": 0.20,
    "climate_stability": 0.15,
    "air_quality": 0.10,
    "fire_disturbance": 0.10,
}


def _normalize(value: float, min_val: float, max_val: float) -> float:
    """Normalize a value to 0-1 range."""
    if max_val <= min_val:
        return 0.5
    return max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))


def compute_vegetation_health(ndvi: float, ndvi_historical_range: tuple = (0.2, 0.85)) -> float:
    """
    Score 0-100: where does current NDVI fall within historical range?
    Higher NDVI = healthier vegetation.
    """
    score = _normalize(ndvi, ndvi_historical_range[0], ndvi_historical_range[1]) * 100
    return round(score, 1)


def compute_forest_integrity(ndvi: float, ndvi_baseline: float) -> float:
    """
    Score 0-100: how close is current NDVI to the baseline?
    Loss = baseline - current; if positive, there's degradation.
    """
    if ndvi_baseline <= 0:
        return 50.0  # No baseline available
    ratio = ndvi / ndvi_baseline
    # Perfect = 1.0 → score 100. ratio 0.5 → score ~50
    score = min(ratio, 1.2) / 1.2 * 100
    return round(max(0, min(100, score)), 1)


def compute_biodiversity_richness(
    species_count: int,
    max_expected: int = 50,
    endangered_count: int = 0,
) -> float:
    """
    Score 0-100: species richness in the cell, with bonus for endangered species.
    """
    base_score = _normalize(species_count, 0, max_expected) * 80
    # Endangered species presence is actually a positive indicator (habitat quality)
    endangered_bonus = min(endangered_count * 5, 20)
    return round(min(100, base_score + endangered_bonus), 1)


def compute_climate_stability(
    temp_anomaly: float,
    precip_anomaly_pct: float,
) -> float:
    """
    Score 0-100: inverse of temperature + rainfall anomalies.
    Anomaly near 0 = stable = high score.
    temp_anomaly: degrees C deviation from long-term mean
    precip_anomaly_pct: % deviation from long-term mean precipitation
    """
    temp_penalty = _normalize(abs(temp_anomaly), 0, 5) * 50
    precip_penalty = _normalize(abs(precip_anomaly_pct), 0, 100) * 50
    score = 100 - temp_penalty - precip_penalty
    return round(max(0, min(100, score)), 1)


def compute_air_quality(pm25: float = 25.0) -> float:
    """
    Score 0-100: inverse of PM2.5 concentration.
    PM2.5 0 = perfect (100), PM2.5 200+ = terrible (0).
    Default: moderate air quality (no real-time OpenAQ data yet).
    """
    score = (1 - _normalize(pm25, 0, 200)) * 100
    return round(max(0, min(100, score)), 1)


def compute_fire_disturbance(fire_count_30d: int, fire_count_1yr: int = 0) -> float:
    """
    Score 0-100: inverse of recent fire frequency.
    0 fires = 100, 10+ fires in 30 days = 0.
    """
    short_term = _normalize(fire_count_30d, 0, 10) * 70
    long_term = _normalize(fire_count_1yr, 0, 50) * 30
    score = 100 - short_term - long_term
    return round(max(0, min(100, score)), 1)


def compute_ehi(
    ndvi: float,
    ndvi_baseline: float,
    species_count: int = 0,
    temp_anomaly: float = 0.0,
    precip_anomaly_pct: float = 0.0,
    fire_count_30d: int = 0,
    fire_count_1yr: int = 0,
    pm25: float = 25.0,
    endangered_count: int = 0,
) -> dict[str, Any]:
    """
    Compute the full Ecosystem Health Index for a grid cell.

    Returns:
        Dict with EHI score and all sub-index scores.
    """
    vh = compute_vegetation_health(ndvi)
    fi = compute_forest_integrity(ndvi, ndvi_baseline)
    br = compute_biodiversity_richness(species_count, endangered_count=endangered_count)
    cs = compute_climate_stability(temp_anomaly, precip_anomaly_pct)
    aq = compute_air_quality(pm25)
    fd = compute_fire_disturbance(fire_count_30d, fire_count_1yr)

    ehi = (
        WEIGHTS["vegetation_health"] * vh
        + WEIGHTS["forest_integrity"] * fi
        + WEIGHTS["biodiversity_richness"] * br
        + WEIGHTS["climate_stability"] * cs
        + WEIGHTS["air_quality"] * aq
        + WEIGHTS["fire_disturbance"] * fd
    )

    ehi = round(max(0, min(100, ehi)), 1)

    if ehi >= 80:
        status = "excellent"
    elif ehi >= 60:
        status = "good"
    elif ehi >= 40:
        status = "fair"
    elif ehi >= 20:
        status = "poor"
    else:
        status = "critical"

    return {
        "ehi_score": ehi,
        "status": status,
        "sub_indices": {
            "vegetation_health": vh,
            "forest_integrity": fi,
            "biodiversity_richness": br,
            "climate_stability": cs,
            "air_quality": aq,
            "fire_disturbance": fd,
        },
        "weights": WEIGHTS,
    }


def compute_ehi_grid(region_id: str | None = None) -> list[dict[str, Any]]:
    """
    Compute EHI for every grid cell in the active region using live data.
    Pulls NDVI, species, weather, fire data from DB/connectors.
    """
    from backend.connectors.ndvi import NDVIConnector
    from backend.db.database import SessionLocal
    from backend.db.models import WeatherObservation, FireAlert, SpeciesOccurrence
    from sqlalchemy import func

    ndvi_connector = NDVIConnector(region_id=region_id)

    # --- Get latest NDVI ---
    latest_ndvi = ndvi_connector.get_latest_ndvi()
    ndvi_map = {r["cell_id"]: r for r in latest_ndvi}

    # --- Get 12-month NDVI baselines ---
    all_ndvi = ndvi_connector.fetch()
    cell_baselines: dict[str, list[float]] = {}
    for r in all_ndvi:
        cell_baselines.setdefault(r["cell_id"], []).append(r["ndvi_mean"])
    ndvi_baselines = {cid: float(np.mean(vals)) for cid, vals in cell_baselines.items()}

    # --- DB queries ---
    db = SessionLocal()
    try:
        cutoff_30d = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        cutoff_1yr = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

        # Fire counts per cell (approximate by rounding lat/lon to 0.1°)
        fire_30d = (
            db.query(
                func.round(FireAlert.latitude, 1).label("lat"),
                func.round(FireAlert.longitude, 1).label("lon"),
                func.count(FireAlert.id).label("cnt"),
            )
            .filter(FireAlert.acq_date >= cutoff_30d)
            .group_by("lat", "lon")
            .all()
        )
        fire_30d_map = {f"{f.lat:.1f}_{f.lon:.1f}": f.cnt for f in fire_30d}

        fire_1yr = (
            db.query(
                func.round(FireAlert.latitude, 1).label("lat"),
                func.round(FireAlert.longitude, 1).label("lon"),
                func.count(FireAlert.id).label("cnt"),
            )
            .filter(FireAlert.acq_date >= cutoff_1yr)
            .group_by("lat", "lon")
            .all()
        )
        fire_1yr_map = {f"{f.lat:.1f}_{f.lon:.1f}": f.cnt for f in fire_1yr}

        # Species count per cell (rounded lat/lon)
        species_cells = (
            db.query(
                func.round(SpeciesOccurrence.latitude, 1).label("lat"),
                func.round(SpeciesOccurrence.longitude, 1).label("lon"),
                func.count(func.distinct(SpeciesOccurrence.species)).label("sp_cnt"),
            )
            .group_by("lat", "lon")
            .all()
        )
        species_map = {f"{s.lat:.1f}_{s.lon:.1f}": s.sp_cnt for s in species_cells}

        # Weather anomalies (simple: deviation of last 7d mean from 30d mean)
        weather_30d = (
            db.query(
                func.avg(WeatherObservation.temperature_mean).label("tmean"),
                func.avg(WeatherObservation.precipitation_sum).label("pmean"),
            )
            .filter(WeatherObservation.date >= cutoff_30d)
            .one()
        )

        cutoff_7d = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        weather_7d = (
            db.query(
                func.avg(WeatherObservation.temperature_mean).label("tmean"),
                func.avg(WeatherObservation.precipitation_sum).label("pmean"),
            )
            .filter(WeatherObservation.date >= cutoff_7d)
            .one()
        )

        temp_anomaly = float((weather_7d.tmean or 25) - (weather_30d.tmean or 25))
        precip_mean_30d = float(weather_30d.pmean or 5)
        precip_mean_7d = float(weather_7d.pmean or 5)
        precip_anomaly_pct = (
            ((precip_mean_7d - precip_mean_30d) / max(precip_mean_30d, 0.1)) * 100
        )
    finally:
        db.close()

    # --- Compute EHI for each cell ---
    results = []
    for cid, nd in ndvi_map.items():
        baseline = ndvi_baselines.get(cid, nd["ndvi_mean"])
        sp_count = species_map.get(cid, 0)
        fire_30 = fire_30d_map.get(cid, 0)
        fire_yr = fire_1yr_map.get(cid, 0)

        ehi = compute_ehi(
            ndvi=nd["ndvi_mean"],
            ndvi_baseline=baseline,
            species_count=sp_count,
            temp_anomaly=temp_anomaly,
            precip_anomaly_pct=precip_anomaly_pct,
            fire_count_30d=fire_30,
            fire_count_1yr=fire_yr,
        )

        results.append({
            "cell_id": cid,
            "center_lat": nd["center_lat"],
            "center_lon": nd["center_lon"],
            **ehi,
        })

    logger.info(f"EHI: computed scores for {len(results)} grid cells.")
    return results
