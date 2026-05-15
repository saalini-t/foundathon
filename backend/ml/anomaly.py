"""
Anomaly Detection for Ecosystem Monitoring
============================================
Isolation Forest on NDVI + weather features to detect unusual
environmental conditions indicating disturbance (deforestation,
drought, unusual warming, etc.).

Features per cell:
  - ndvi_mean (current)
  - ndvi_deviation (current - baseline)
  - temp_mean (recent 7d average)
  - temp_deviation (7d avg - 30d avg)
  - precip_sum_30d
  - precip_deviation_pct
  - fire_count_30d
"""

import logging
import os
from datetime import datetime, timedelta
from typing import Any

import joblib
import numpy as np

from backend.regions import get_region, Region

logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "saved_models")

FEATURE_COLUMNS = [
    "ndvi_mean",
    "ndvi_deviation",
    "temp_mean",
    "temp_deviation",
    "precip_sum_30d",
    "precip_deviation_pct",
    "fire_count_30d",
]


def _model_path(region_id: str) -> str:
    return os.path.join(MODEL_DIR, f"anomaly_iforest_{region_id}.joblib")


def _generate_baseline_data(n_samples: int = 3000, region: Region | None = None) -> np.ndarray:
    """
    Generate synthetic 'normal' ecosystem data using the region's climate profile.
    """
    if region is None:
        region = get_region()
    cp = region.climate
    rng = np.random.default_rng(42)
    samples = []

    for _ in range(n_samples):
        ndvi = rng.normal(cp.ndvi_mean, cp.ndvi_std)
        ndvi = np.clip(ndvi, 0.1, 0.95)

        ndvi_dev = rng.normal(0.0, 0.03)
        ndvi_dev = np.clip(ndvi_dev, -0.15, 0.15)

        temp = rng.normal(cp.temp_mean, 3.0)
        temp = np.clip(temp, cp.temp_mean - 15, cp.temp_mean + 15)

        temp_dev = rng.normal(0.0, 1.0)
        temp_dev = np.clip(temp_dev, -4, 4)

        precip = rng.exponential((cp.precip_dry_scale + cp.precip_wet_scale) / 2)
        precip = np.clip(precip, 0, 800)

        precip_dev = rng.normal(0, 15)
        precip_dev = np.clip(precip_dev, -80, 80)

        fire_count = rng.poisson(0.3)
        fire_count = min(fire_count, 5)

        samples.append([ndvi, ndvi_dev, temp, temp_dev, precip, precip_dev, fire_count])

    return np.array(samples, dtype=np.float64)


def train_anomaly_model(
    n_samples: int = 3000, contamination: float = 0.05, region_id: str | None = None
) -> dict[str, Any]:
    """
    Train Isolation Forest on synthetic baseline data for a region.
    """
    from sklearn.ensemble import IsolationForest
    from sklearn.preprocessing import StandardScaler

    region = get_region(region_id)
    logger.info(f"Training anomaly model for {region.id} (IsolationForest)...")
    X = _generate_baseline_data(n_samples, region=region)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = IsolationForest(
        n_estimators=200,
        contamination=contamination,
        max_samples="auto",
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_scaled)

    scores = model.decision_function(X_scaled)
    predictions = model.predict(X_scaled)
    n_anomalies = int((predictions == -1).sum())

    os.makedirs(MODEL_DIR, exist_ok=True)
    path = _model_path(region.id)
    joblib.dump({"model": model, "scaler": scaler}, path)

    metrics = {
        "n_training_samples": n_samples,
        "contamination": contamination,
        "n_anomalies_in_training": n_anomalies,
        "anomaly_rate": round(n_anomalies / n_samples, 4),
        "score_mean": round(float(scores.mean()), 4),
        "score_std": round(float(scores.std()), 4),
    }
    logger.info(f"Anomaly model trained: {metrics}")
    return metrics


def load_anomaly_model(region_id: str | None = None):
    """Load or auto-train the anomaly model for a region."""
    region = get_region(region_id)
    path = _model_path(region.id)
    if os.path.exists(path):
        return joblib.load(path)
    logger.info(f"No saved anomaly model for {region.id}. Training fresh model...")
    train_anomaly_model(region_id=region.id)
    return joblib.load(path)


def detect_anomalies(features: list[dict[str, float]], region_id: str | None = None) -> list[dict[str, Any]]:
    """
    Detect anomalies in a list of feature dictionaries.

    Returns list of dicts with is_anomaly, anomaly_score, severity.
    """
    if not features:
        return []

    artifacts = load_anomaly_model(region_id=region_id)
    model = artifacts["model"]
    scaler = artifacts["scaler"]

    X = np.array([[f.get(col, 0.0) for col in FEATURE_COLUMNS] for f in features])
    X_scaled = scaler.transform(X)

    scores = model.decision_function(X_scaled)
    predictions = model.predict(X_scaled)

    results = []
    for i, feat in enumerate(features):
        is_anomaly = predictions[i] == -1
        raw_score = float(scores[i])

        # Convert to 0-1 anomaly severity (lower decision_function = more anomalous)
        severity = max(0, min(1, 0.5 - raw_score))

        if severity >= 0.7:
            severity_label = "critical"
        elif severity >= 0.5:
            severity_label = "high"
        elif severity >= 0.3:
            severity_label = "moderate"
        else:
            severity_label = "low"

        result = {
            "is_anomaly": bool(is_anomaly),
            "anomaly_score": round(raw_score, 4),
            "severity": round(severity, 3),
            "severity_label": severity_label,
        }

        # Add dominant factor explanation for anomalies
        if is_anomaly:
            result["factors"] = _explain_anomaly(feat)

        results.append(result)

    return results


def _explain_anomaly(feat: dict[str, float]) -> list[str]:
    """Provide human-readable explanations for why a cell is anomalous."""
    factors = []
    ndvi = feat.get("ndvi_mean", 0.65)
    ndvi_dev = feat.get("ndvi_deviation", 0.0)
    temp_dev = feat.get("temp_deviation", 0.0)
    precip_dev = feat.get("precip_deviation_pct", 0.0)
    fire_count = feat.get("fire_count_30d", 0)

    if ndvi < 0.35:
        factors.append("Very low NDVI — possible deforestation or barren land")
    if ndvi_dev < -0.1:
        factors.append(f"NDVI dropped {abs(ndvi_dev):.2f} below baseline — vegetation loss")
    if temp_dev > 3:
        factors.append(f"Temperature {temp_dev:.1f}°C above normal — heat anomaly")
    if temp_dev < -3:
        factors.append(f"Temperature {abs(temp_dev):.1f}°C below normal — cold anomaly")
    if precip_dev < -50:
        factors.append(f"Rainfall {abs(precip_dev):.0f}% below normal — drought risk")
    if precip_dev > 80:
        factors.append(f"Rainfall {precip_dev:.0f}% above normal — flood risk")
    if fire_count >= 3:
        factors.append(f"{fire_count} fires in 30 days — active fire disturbance")

    if not factors:
        factors.append("Multi-factor deviation from baseline conditions")

    return factors


def detect_anomalies_grid(region_id: str | None = None) -> list[dict[str, Any]]:
    """
    Run anomaly detection across all grid cells in the active region
    using live NDVI + weather + fire data.
    """
    from backend.connectors.ndvi import NDVIConnector
    from backend.db.database import SessionLocal
    from backend.db.models import WeatherObservation, FireAlert
    from sqlalchemy import func

    ndvi_connector = NDVIConnector(region_id=region_id)

    # Latest NDVI
    latest_ndvi = ndvi_connector.get_latest_ndvi()
    ndvi_map = {r["cell_id"]: r for r in latest_ndvi}

    # 12-month NDVI baselines
    all_ndvi = ndvi_connector.fetch()
    cell_baselines: dict[str, list[float]] = {}
    for r in all_ndvi:
        cell_baselines.setdefault(r["cell_id"], []).append(r["ndvi_mean"])
    ndvi_baselines = {cid: float(np.mean(vals)) for cid, vals in cell_baselines.items()}

    # DB data
    db = SessionLocal()
    try:
        cutoff_30d = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        cutoff_7d = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        # Fire counts
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

        # Weather aggregates
        weather_30d = (
            db.query(
                func.avg(WeatherObservation.temperature_mean).label("tmean"),
                func.avg(WeatherObservation.precipitation_sum).label("pmean"),
            )
            .filter(WeatherObservation.date >= cutoff_30d)
            .one()
        )
        weather_7d = (
            db.query(
                func.avg(WeatherObservation.temperature_mean).label("tmean"),
                func.avg(WeatherObservation.precipitation_sum).label("pmean"),
            )
            .filter(WeatherObservation.date >= cutoff_7d)
            .one()
        )

        temp_mean = float(weather_7d.tmean or 25)
        temp_30d_mean = float(weather_30d.tmean or 25)
        precip_30d = float(weather_30d.pmean or 5) * 30
        precip_30d_baseline = float(weather_30d.pmean or 5) * 30
    finally:
        db.close()

    temp_dev = temp_mean - temp_30d_mean
    precip_dev_pct = (
        ((precip_30d - precip_30d_baseline) / max(precip_30d_baseline, 0.1)) * 100
        if precip_30d_baseline > 0
        else 0
    )

    # Build feature vectors
    feature_list = []
    cell_meta = []
    for cid, nd in ndvi_map.items():
        baseline = ndvi_baselines.get(cid, nd["ndvi_mean"])
        feat = {
            "ndvi_mean": nd["ndvi_mean"],
            "ndvi_deviation": nd["ndvi_mean"] - baseline,
            "temp_mean": temp_mean,
            "temp_deviation": temp_dev,
            "precip_sum_30d": precip_30d,
            "precip_deviation_pct": precip_dev_pct,
            "fire_count_30d": fire_map.get(cid, 0),
        }
        feature_list.append(feat)
        cell_meta.append({
            "cell_id": cid,
            "center_lat": nd["center_lat"],
            "center_lon": nd["center_lon"],
        })

    # Run detection
    anomaly_results = detect_anomalies(feature_list, region_id=region_id)

    # Merge
    output = []
    for meta, features, result in zip(cell_meta, feature_list, anomaly_results):
        output.append({
            **meta,
            "features": features,
            **result,
        })

    n_anomalies = sum(1 for r in output if r["is_anomaly"])
    logger.info(f"Anomaly detection: {n_anomalies}/{len(output)} cells flagged.")
    return output
