"""
Fire Risk Prediction Model
===========================
XGBoost binary classifier: predicts fire probability per grid cell
using weather features + NDVI + fire history.

Features per cell:
  - ndvi_current: current NDVI value (vegetation dryness)
  - ndvi_anomaly: deviation from 12-month mean
  - temp_max_7d: max temperature last 7 days
  - temp_mean_7d: mean temperature last 7 days
  - precip_sum_30d: cumulative precipitation last 30 days
  - humidity_min_7d: minimum humidity last 7 days
  - wind_max_7d: max wind speed last 7 days
  - days_since_rain: consecutive dry days
  - fire_history_count: historical fire count in this cell (30d)
  - month: current month (seasonality)
  - latitude: cell latitude (proxy for ecological zone)
"""

import logging
import os
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

from backend.regions import get_region, Region

logger = logging.getLogger(__name__)

MODEL_DIR = Path(__file__).parent / "saved_models"
MODEL_DIR.mkdir(exist_ok=True)

FEATURE_COLUMNS = [
    "ndvi_current",
    "ndvi_anomaly",
    "temp_max_7d",
    "temp_mean_7d",
    "precip_sum_30d",
    "humidity_min_7d",
    "wind_max_7d",
    "days_since_rain",
    "fire_history_count",
    "month",
    "latitude",
]


def _model_path(region_id: str) -> Path:
    return MODEL_DIR / f"fire_risk_xgb_{region_id}.joblib"


def _generate_training_data(
    n_samples: int = 5000, seed: int = 42, region: Region | None = None
) -> pd.DataFrame:
    """
    Generate synthetic but ecologically realistic training data
    for fire risk prediction using the region's climate profile.
    """
    if region is None:
        region = get_region()
    cp = region.climate
    rng = np.random.default_rng(seed)

    latitudes = rng.uniform(cp.lat_range[0], cp.lat_range[1], n_samples)
    months = rng.integers(1, 13, n_samples)

    is_dry_season = np.isin(months, cp.dry_months)

    # NDVI: lower in dry season; latitude gradient if deciduous threshold exists
    if cp.ndvi_deciduous_threshold_lat is not None:
        ndvi_base = np.where(latitudes > cp.ndvi_deciduous_threshold_lat, cp.ndvi_dry, cp.ndvi_wet)
    else:
        ndvi_base = np.full(n_samples, cp.ndvi_mean)
    seasonal_mod = np.where(is_dry_season, -0.15, 0.05)
    ndvi_current = ndvi_base + seasonal_mod + rng.normal(0, cp.ndvi_std, n_samples)
    ndvi_current = np.clip(ndvi_current, 0.1, 0.9)
    ndvi_anomaly = rng.normal(0, 0.1, n_samples)

    # Temperature
    temp_base = cp.temp_mean + (cp.lat_range[1] - latitudes) * cp.temp_lat_gradient
    temp_seasonal = np.where(is_dry_season, cp.temp_dry_offset, cp.temp_wet_offset)
    temp_max_7d = temp_base + temp_seasonal + rng.normal(0, 3, n_samples)
    temp_mean_7d = temp_max_7d - rng.uniform(2, 6, n_samples)

    # Precipitation
    precip_sum_30d = np.where(
        is_dry_season,
        rng.exponential(cp.precip_dry_scale, n_samples),
        rng.exponential(cp.precip_wet_scale, n_samples),
    )

    # Humidity
    humidity_min_7d = np.where(
        is_dry_season,
        rng.normal(cp.humidity_dry_mean, 12, n_samples),
        rng.normal(cp.humidity_wet_mean, 10, n_samples),
    )
    humidity_min_7d = np.clip(humidity_min_7d, 10, 98)

    # Wind
    wind_max_7d = rng.normal(15, 7, n_samples)
    wind_max_7d = np.clip(wind_max_7d, 0, 50)

    # Days since rain
    days_since_rain = np.where(
        is_dry_season,
        rng.integers(5, 45, n_samples),
        rng.integers(0, 5, n_samples),
    ).astype(float)

    # Fire history
    fire_history = rng.poisson(0.5, n_samples)

    # --- Fire probability (logistic model for label generation) ---
    logit = (
        -3.0
        + 2.5 * (1.0 - ndvi_current)  # Dry vegetation
        + 0.08 * temp_max_7d           # Heat
        - 0.01 * precip_sum_30d        # Rain suppresses fire
        - 0.03 * humidity_min_7d       # Dry air
        + 0.02 * wind_max_7d           # Wind fans fires
        + 0.03 * days_since_rain       # Prolonged dry spell
        + 0.4 * fire_history           # Historical tendency
        - 0.8 * ndvi_anomaly           # Negative anomaly = stress
    )
    prob = 1.0 / (1.0 + np.exp(-logit))
    fire = (rng.random(n_samples) < prob).astype(int)

    df = pd.DataFrame({
        "ndvi_current": ndvi_current,
        "ndvi_anomaly": ndvi_anomaly,
        "temp_max_7d": temp_max_7d,
        "temp_mean_7d": temp_mean_7d,
        "precip_sum_30d": precip_sum_30d,
        "humidity_min_7d": humidity_min_7d,
        "wind_max_7d": wind_max_7d,
        "days_since_rain": days_since_rain,
        "fire_history_count": fire_history,
        "month": months,
        "latitude": latitudes,
        "fire": fire,
    })

    logger.info(
        f"Generated {n_samples} training samples. "
        f"Fire rate: {fire.mean():.2%}"
    )
    return df


def train_fire_model(n_samples: int = 8000, region_id: str | None = None) -> dict[str, Any]:
    """
    Train XGBoost fire risk model on synthetic data for a region.
    Returns training metrics.
    """
    from xgboost import XGBClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import (
        roc_auc_score,
        precision_score,
        recall_score,
        f1_score,
    )

    region = get_region(region_id)
    df = _generate_training_data(n_samples=n_samples, region=region)
    X = df[FEATURE_COLUMNS]
    y = df["fire"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = XGBClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=(y_train == 0).sum() / max((y_train == 1).sum(), 1),
        random_state=42,
        eval_metric="logloss",
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "auc_roc": round(roc_auc_score(y_test, y_proba), 4),
        "precision": round(precision_score(y_test, y_pred, zero_division=0), 4),
        "recall": round(recall_score(y_test, y_pred, zero_division=0), 4),
        "f1": round(f1_score(y_test, y_pred, zero_division=0), 4),
        "train_size": len(X_train),
        "test_size": len(X_test),
        "fire_rate_train": round(y_train.mean(), 4),
        "fire_rate_test": round(y_test.mean(), 4),
    }

    # Feature importances
    importances = dict(
        zip(FEATURE_COLUMNS, [round(float(v), 4) for v in model.feature_importances_])
    )
    metrics["feature_importances"] = importances

    # Save model per region
    path = _model_path(region.id)
    joblib.dump(model, path)
    logger.info(f"Fire risk model saved to {path}. AUC: {metrics['auc_roc']}")

    return metrics


def load_fire_model(region_id: str | None = None):
    """Load the trained fire risk model from disk for a region."""
    region = get_region(region_id)
    path = _model_path(region.id)
    if not path.exists():
        logger.info(f"No saved fire model for {region.id}. Training new model...")
        train_fire_model(region_id=region.id)
    return joblib.load(path)


def predict_fire_risk(features: list[dict[str, float]], region_id: str | None = None) -> list[dict[str, Any]]:
    """
    Predict fire risk for a list of grid cells.

    Args:
        features: list of dicts with keys matching FEATURE_COLUMNS

    Returns:
        list of dicts with cell features + risk_probability + risk_level
    """
    model = load_fire_model(region_id=region_id)

    df = pd.DataFrame(features)
    # Fill missing columns with defaults
    for col in FEATURE_COLUMNS:
        if col not in df.columns:
            df[col] = 0.0

    X = df[FEATURE_COLUMNS].fillna(0)
    probabilities = model.predict_proba(X)[:, 1]

    results = []
    for i, prob in enumerate(probabilities):
        prob_val = float(prob)
        if prob_val >= 0.7:
            level = "extreme"
        elif prob_val >= 0.5:
            level = "high"
        elif prob_val >= 0.3:
            level = "moderate"
        else:
            level = "low"

        result = {**features[i], "risk_probability": round(prob_val, 4), "risk_level": level}
        results.append(result)

    return results


def predict_fire_risk_grid(region_id: str | None = None) -> list[dict[str, Any]]:
    """
    Predict fire risk for all grid cells in the active region using
    current NDVI + latest weather data from DB.
    """
    from backend.connectors.ndvi import NDVIConnector
    from backend.db.database import SessionLocal
    from backend.db.models import WeatherObservation, FireAlert
    from sqlalchemy import func
    from datetime import datetime, timedelta

    ndvi_connector = NDVIConnector(region_id=region_id)
    ndvi_data = ndvi_connector.get_latest_ndvi()

    # Build NDVI lookup
    ndvi_map: dict[str, dict] = {}
    for r in ndvi_data:
        ndvi_map[r["cell_id"]] = r

    # Fetch 12-month NDVI for anomaly
    all_ndvi = ndvi_connector.fetch()
    cell_means: dict[str, list] = {}
    for r in all_ndvi:
        cid = r["cell_id"]
        cell_means.setdefault(cid, []).append(r["ndvi_mean"])
    ndvi_baselines = {cid: np.mean(vals) for cid, vals in cell_means.items()}

    # Fetch weather aggregates from DB
    db = SessionLocal()
    try:
        cutoff_7d = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        cutoff_30d = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        # Get station-level weather aggregates
        weather_7d = (
            db.query(
                WeatherObservation.station_name,
                func.max(WeatherObservation.temperature_max).label("temp_max"),
                func.avg(WeatherObservation.temperature_mean).label("temp_mean"),
                func.min(WeatherObservation.humidity_mean).label("humidity_min"),
                func.max(WeatherObservation.windspeed_max).label("wind_max"),
            )
            .filter(WeatherObservation.date >= cutoff_7d)
            .group_by(WeatherObservation.station_name)
            .all()
        )

        precip_30d = (
            db.query(
                WeatherObservation.station_name,
                func.sum(WeatherObservation.precipitation_sum).label("precip_total"),
            )
            .filter(WeatherObservation.date >= cutoff_30d)
            .group_by(WeatherObservation.station_name)
            .all()
        )

        # Compute average weather across all stations (simple approach for grid)
        if weather_7d:
            avg_temp_max = float(np.mean([w.temp_max or 30 for w in weather_7d]))
            avg_temp_mean = float(np.mean([w.temp_mean or 25 for w in weather_7d]))
            avg_humidity_min = float(np.mean([w.humidity_min or 50 for w in weather_7d]))
            avg_wind_max = float(np.mean([w.wind_max or 10 for w in weather_7d]))
        else:
            avg_temp_max, avg_temp_mean = 32.0, 27.0
            avg_humidity_min, avg_wind_max = 45.0, 12.0

        if precip_30d:
            avg_precip_30d = float(np.mean([p.precip_total or 0 for p in precip_30d]))
        else:
            avg_precip_30d = 20.0

        # Days since rain: check for last day with precipitation > 1mm
        last_rain = (
            db.query(func.max(WeatherObservation.date))
            .filter(WeatherObservation.precipitation_sum > 1.0)
            .scalar()
        )
        if last_rain:
            days_since = (datetime.now() - datetime.strptime(last_rain, "%Y-%m-%d")).days
        else:
            days_since = 30

        # Fire history per approximate cell
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
        fire_map = {f"{f.lat:.1f}_{f.lon:.1f}": f.cnt for f in fire_30d}
    finally:
        db.close()

    # Build feature vectors for each grid cell
    now = datetime.now()
    cell_features = []
    for cid, nd in ndvi_map.items():
        baseline = ndvi_baselines.get(cid, nd["ndvi_mean"])
        cell_features.append({
            "cell_id": cid,
            "center_lat": nd["center_lat"],
            "center_lon": nd["center_lon"],
            "ndvi_current": nd["ndvi_mean"],
            "ndvi_anomaly": nd["ndvi_mean"] - baseline,
            "temp_max_7d": avg_temp_max,
            "temp_mean_7d": avg_temp_mean,
            "precip_sum_30d": avg_precip_30d,
            "humidity_min_7d": avg_humidity_min,
            "wind_max_7d": avg_wind_max,
            "days_since_rain": float(days_since),
            "fire_history_count": fire_map.get(cid, 0),
            "month": now.month,
            "latitude": nd["center_lat"],
        })

    if not cell_features:
        return []

    return predict_fire_risk(cell_features, region_id=region_id)
