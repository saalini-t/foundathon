"""
Phase 2 — Prediction / ML API endpoints
=========================================
GET  /api/predict/fire-risk      Fire risk predictions per grid cell
GET  /api/predict/ehi            Ecosystem Health Index per grid cell
GET  /api/predict/anomalies      Anomaly detection results
POST /api/predict/fire-risk/train  Retrain the fire model
POST /api/predict/anomaly/train    Retrain the anomaly model
GET  /api/ndvi/latest            Latest NDVI values per cell
GET  /api/ndvi/grid              Grid cell definitions
"""

import logging

from fastapi import APIRouter, HTTPException, Query

logger = logging.getLogger(__name__)

router = APIRouter(tags=["predict"])


# ── Fire Risk ─────────────────────────────────────────────────

@router.get("/api/predict/fire-risk")
def fire_risk_grid(region: str = Query(None, description="Region id")):
    """Return fire risk predictions for all grid cells."""
    try:
        from backend.ml.fire_risk import predict_fire_risk_grid
        results = predict_fire_risk_grid(region_id=region)
        return {
            "count": len(results),
            "predictions": results,
        }
    except Exception as e:
        logger.exception("Fire risk prediction failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/predict/fire-risk/train")
def train_fire_model_endpoint(
    n_samples: int = 8000,
    region: str = Query(None, description="Region id"),
):
    """Retrain the XGBoost fire risk model."""
    try:
        from backend.ml.fire_risk import train_fire_model
        metrics = train_fire_model(n_samples=n_samples, region_id=region)
        return {"message": "Fire risk model retrained.", "metrics": metrics}
    except Exception as e:
        logger.exception("Fire model training failed")
        raise HTTPException(status_code=500, detail=str(e))


# ── Ecosystem Health Index ────────────────────────────────────

@router.get("/api/predict/ehi")
def ehi_grid(region: str = Query(None, description="Region id")):
    """Return Ecosystem Health Index for all grid cells."""
    try:
        from backend.ml.ehi import compute_ehi_grid
        results = compute_ehi_grid(region_id=region)

        # Summary statistics
        scores = [r["ehi_score"] for r in results]
        avg_score = round(sum(scores) / len(scores), 1) if scores else 0
        status_counts = {}
        for r in results:
            s = r["status"]
            status_counts[s] = status_counts.get(s, 0) + 1

        return {
            "count": len(results),
            "average_ehi": avg_score,
            "status_distribution": status_counts,
            "cells": results,
        }
    except Exception as e:
        logger.exception("EHI computation failed")
        raise HTTPException(status_code=500, detail=str(e))


# ── Anomaly Detection ────────────────────────────────────────

@router.get("/api/predict/anomalies")
def anomaly_grid(region: str = Query(None, description="Region id")):
    """Return anomaly detection results for all grid cells."""
    try:
        from backend.ml.anomaly import detect_anomalies_grid
        results = detect_anomalies_grid(region_id=region)

        anomalies = [r for r in results if r["is_anomaly"]]
        return {
            "count": len(results),
            "anomaly_count": len(anomalies),
            "anomaly_rate": round(len(anomalies) / max(len(results), 1), 3),
            "anomalies": anomalies,
            "all_cells": results,
        }
    except Exception as e:
        logger.exception("Anomaly detection failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/predict/anomaly/train")
def train_anomaly_model_endpoint(
    n_samples: int = 3000,
    contamination: float = 0.05,
    region: str = Query(None, description="Region id"),
):
    """Retrain the Isolation Forest anomaly model."""
    try:
        from backend.ml.anomaly import train_anomaly_model
        metrics = train_anomaly_model(
            n_samples=n_samples, contamination=contamination, region_id=region,
        )
        return {"message": "Anomaly model retrained.", "metrics": metrics}
    except Exception as e:
        logger.exception("Anomaly model training failed")
        raise HTTPException(status_code=500, detail=str(e))


# ── NDVI ──────────────────────────────────────────────────────

@router.get("/api/ndvi/latest")
def ndvi_latest(region: str = Query(None, description="Region id")):
    """Return the latest NDVI values for all grid cells."""
    try:
        from backend.connectors.ndvi import NDVIConnector
        connector = NDVIConnector(region_id=region)
        data = connector.get_latest_ndvi()
        return {"count": len(data), "cells": data}
    except Exception as e:
        logger.exception("NDVI fetch failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/ndvi/grid")
def ndvi_grid_cells(region: str = Query(None, description="Region id")):
    """Return the grid cell definitions for the selected region."""
    try:
        from backend.connectors.ndvi import NDVIConnector
        connector = NDVIConnector(region_id=region)
        cells = connector.get_grid_cells()
        return {"count": len(cells), "cells": cells}
    except Exception as e:
        logger.exception("Grid cells fetch failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/ndvi/timeseries/{cell_id}")
def ndvi_timeseries(
    cell_id: str,
    region: str = Query(None, description="Region id"),
):
    """Return 12-month NDVI timeseries for a specific grid cell."""
    try:
        from backend.connectors.ndvi import NDVIConnector
        connector = NDVIConnector(region_id=region)
        all_data = connector.fetch()
        cell_data = [r for r in all_data if r["cell_id"] == cell_id]
        if not cell_data:
            raise HTTPException(status_code=404, detail=f"Cell '{cell_id}' not found")
        cell_data.sort(key=lambda r: r["date"])
        return {"cell_id": cell_id, "count": len(cell_data), "timeseries": cell_data}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("NDVI timeseries failed")
        raise HTTPException(status_code=500, detail=str(e))
