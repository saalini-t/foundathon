"""
Feature 3 — Temporal Ecosystem Time Machine
=============================================
Returns historical monthly NDVI / EHI snapshots for the time slider.
"""

import logging

from fastapi import APIRouter, Query

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/timemachine", tags=["timemachine"])


@router.get("/ndvi")
def ndvi_time_machine(
    region: str = Query(None, description="Region id"),
    month: int = Query(None, ge=1, le=12, description="Specific month (1-12) or omit for all 12"),
):
    """
    Return NDVI grid snapshots for each month over the past 12 months.
    If `month` is specified, return only that month's snapshot.
    Used by the frontend time slider to animate ecosystem changes.
    """
    from backend.connectors.ndvi import NDVIConnector

    connector = NDVIConnector(region_id=region)
    all_data = connector.fetch()

    # Group by (year, month)
    monthly: dict[str, list[dict]] = {}
    for cell in all_data:
        key = cell["date"][:7]  # "2025-03"
        monthly.setdefault(key, []).append({
            "cell_id": cell["cell_id"],
            "center_lat": cell["center_lat"],
            "center_lon": cell["center_lon"],
            "ndvi_mean": cell["ndvi_mean"],
            "ndvi_min": cell["ndvi_min"],
            "ndvi_max": cell["ndvi_max"],
        })

    # Sort by date key
    sorted_months = sorted(monthly.keys())

    # Filter to specific month if requested
    if month is not None:
        sorted_months = [k for k in sorted_months if int(k.split("-")[1]) == month]

    snapshots = []
    for m_key in sorted_months:
        cells = monthly[m_key]
        avg = sum(c["ndvi_mean"] for c in cells) / len(cells) if cells else 0
        snapshots.append({
            "month_key": m_key,
            "cell_count": len(cells),
            "average_ndvi": round(avg, 4),
            "cells": cells,
        })

    return {
        "region": region,
        "snapshot_count": len(snapshots),
        "snapshots": snapshots,
    }


@router.get("/ehi")
def ehi_time_machine(
    region: str = Query(None, description="Region id"),
):
    """
    Return monthly EHI approximations for the past 12 months by
    computing EHI using each month's NDVI snapshot with current
    weather and species baselines.

    This gives users a sense of how ecosystem health has trended.
    """
    from backend.connectors.ndvi import NDVIConnector
    from backend.ml.ehi import compute_vegetation_health, compute_forest_integrity, WEIGHTS
    import numpy as np

    connector = NDVIConnector(region_id=region)
    all_data = connector.fetch()

    # Group by month
    monthly: dict[str, list[dict]] = {}
    for cell in all_data:
        key = cell["date"][:7]
        monthly.setdefault(key, []).append(cell)

    # Compute 12-month baseline NDVI
    all_ndvi = [c["ndvi_mean"] for c in all_data]
    baseline_ndvi = float(np.mean(all_ndvi)) if all_ndvi else 0.5

    sorted_months = sorted(monthly.keys())
    timeline = []
    for m_key in sorted_months:
        cells = monthly[m_key]
        ndvi_vals = [c["ndvi_mean"] for c in cells]
        avg_ndvi = float(np.mean(ndvi_vals)) if ndvi_vals else 0.5

        # Simplified EHI using vegetation and forest sub-indices
        vh = compute_vegetation_health(avg_ndvi)
        fi = compute_forest_integrity(avg_ndvi, baseline_ndvi)

        # Approximate total EHI with stable sub-indices for other components
        approx_ehi = round(
            WEIGHTS["vegetation_health"] * vh
            + WEIGHTS["forest_integrity"] * fi
            + WEIGHTS["biodiversity_richness"] * 65  # stable baseline
            + WEIGHTS["climate_stability"] * 60
            + WEIGHTS["air_quality"] * 55
            + WEIGHTS["fire_disturbance"] * 70,
            1,
        )
        approx_ehi = max(0, min(100, approx_ehi))

        if approx_ehi >= 80:
            status = "excellent"
        elif approx_ehi >= 60:
            status = "good"
        elif approx_ehi >= 40:
            status = "fair"
        elif approx_ehi >= 20:
            status = "poor"
        else:
            status = "critical"

        timeline.append({
            "month_key": m_key,
            "average_ndvi": round(avg_ndvi, 4),
            "ehi_score": approx_ehi,
            "status": status,
            "cell_count": len(cells),
        })

    return {
        "region": region,
        "months": len(timeline),
        "timeline": timeline,
    }
