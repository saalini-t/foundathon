"""
Feature 4 — AI Narrative Summary
==================================
Generate a natural-language ecosystem summary for a selected grid cell
using data from EHI, NDVI, fire risk, anomaly status, and biodiversity.
"""

import logging
from typing import Any

from fastapi import APIRouter, HTTPException, Query

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/narrative", tags=["narrative"])


def _trend_word(values: list[float]) -> str:
    """Describe the trend across a series of values."""
    if len(values) < 2:
        return "stable"
    first_half = sum(values[: len(values) // 2]) / max(len(values) // 2, 1)
    second_half = sum(values[len(values) // 2 :]) / max(len(values) - len(values) // 2, 1)
    diff = second_half - first_half
    if diff > 0.05:
        return "improving"
    if diff < -0.05:
        return "declining"
    return "stable"


def _risk_sentence(risk_prob: float) -> str:
    if risk_prob >= 0.75:
        return "Fire risk is currently **extreme** — immediate monitoring recommended."
    if risk_prob >= 0.5:
        return "Fire risk is **high**, driven by low moisture and elevated temperatures."
    if risk_prob >= 0.25:
        return "Fire risk is **moderate**; seasonal dryness may elevate risk in coming weeks."
    return "Fire risk is currently **low**."


def _ehi_sentence(score: float, status: str) -> str:
    return f"Overall ecosystem health scores **{score:.0f}/100** ({status})."


def _biodiversity_sentence(species_count: int) -> str:
    if species_count >= 20:
        return f"Biodiversity presence is **high** with {species_count} species recorded in this area."
    if species_count >= 10:
        return f"Moderate biodiversity levels observed — {species_count} species on record."
    if species_count > 0:
        return f"Biodiversity records are **sparse** ({species_count} species), warranting further field surveys."
    return "No species occurrence records are available for this cell."


def _anomaly_sentence(is_anomaly: bool, factors: list[str] | None) -> str:
    if not is_anomaly:
        return "No environmental anomalies detected."
    factor_text = ", ".join(factors[:2]) if factors else "multi-variable deviation"
    return f"⚠️ An environmental anomaly has been flagged due to {factor_text}."


def _ndvi_sentence(ndvi: float, trend: str) -> str:
    if ndvi >= 0.7:
        veg = "dense and healthy"
    elif ndvi >= 0.5:
        veg = "moderately healthy"
    elif ndvi >= 0.3:
        veg = "showing signs of stress"
    else:
        veg = "significantly degraded"
    return f"Vegetation is {veg} (NDVI {ndvi:.2f}), with a {trend} trend over the past 12 months."


@router.get("/{cell_id}")
def generate_narrative(
    cell_id: str,
    region: str = Query(None, description="Region id"),
):
    """
    Generate a short natural-language ecosystem summary for a grid cell.
    Combines EHI, NDVI trend, fire risk, anomaly status, and species data.
    """
    from backend.connectors.ndvi import NDVIConnector
    from backend.ml.ehi import compute_ehi_grid
    from backend.ml.fire_risk import predict_fire_risk_grid
    from backend.ml.anomaly import detect_anomalies_grid
    from backend.db.database import SessionLocal
    from backend.db.models import SpeciesOccurrence
    from sqlalchemy import func

    # ── Gather data for this cell ─────────────────────────────

    # NDVI timeseries
    ndvi_connector = NDVIConnector(region_id=region)
    all_ndvi = ndvi_connector.fetch()
    cell_ndvi = sorted(
        [r for r in all_ndvi if r["cell_id"] == cell_id],
        key=lambda r: r["date"],
    )
    if not cell_ndvi:
        raise HTTPException(404, f"Cell '{cell_id}' not found in region.")

    latest_ndvi = cell_ndvi[-1]["ndvi_mean"]
    ndvi_trend = _trend_word([c["ndvi_mean"] for c in cell_ndvi])

    # EHI
    ehi_cells = compute_ehi_grid(region_id=region)
    ehi_match = next((c for c in ehi_cells if c["cell_id"] == cell_id), None)
    ehi_score = ehi_match["ehi_score"] if ehi_match else 50.0
    ehi_status = ehi_match["status"] if ehi_match else "fair"

    # Fire risk
    fr_cells = predict_fire_risk_grid(region_id=region)
    fr_match = next((c for c in fr_cells if c["cell_id"] == cell_id), None)
    fire_prob = fr_match["risk_probability"] if fr_match else 0.1

    # Anomalies
    anom_cells = detect_anomalies_grid(region_id=region)
    anom_match = next((c for c in anom_cells if c["cell_id"] == cell_id), None)
    is_anomaly = anom_match["is_anomaly"] if anom_match else False
    anom_factors = anom_match.get("factors") if anom_match else []

    # Species count near this cell
    center_lat = cell_ndvi[-1]["center_lat"]
    center_lon = cell_ndvi[-1]["center_lon"]
    db = SessionLocal()
    try:
        species_count = (
            db.query(func.count(func.distinct(SpeciesOccurrence.species)))
            .filter(
                SpeciesOccurrence.latitude.between(center_lat - 0.1, center_lat + 0.1),
                SpeciesOccurrence.longitude.between(center_lon - 0.1, center_lon + 0.1),
            )
            .scalar()
        ) or 0
    finally:
        db.close()

    # ── Compose narrative ─────────────────────────────────────
    sentences = [
        _ehi_sentence(ehi_score, ehi_status),
        _ndvi_sentence(latest_ndvi, ndvi_trend),
        _biodiversity_sentence(species_count),
        _risk_sentence(fire_prob),
        _anomaly_sentence(is_anomaly, anom_factors),
    ]

    narrative = " ".join(sentences)

    return {
        "cell_id": cell_id,
        "narrative": narrative,
        "data": {
            "ehi_score": ehi_score,
            "ehi_status": ehi_status,
            "ndvi_current": round(latest_ndvi, 3),
            "ndvi_trend": ndvi_trend,
            "fire_risk_probability": round(fire_prob, 3),
            "is_anomaly": is_anomaly,
            "species_count": species_count,
        },
    }
