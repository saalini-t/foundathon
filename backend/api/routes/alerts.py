"""Alert API routes — fire alerts, anomaly warnings."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from backend.db.database import get_db
from backend.db.models import FireAlert
from backend.regions import get_region

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("/fires")
def get_fire_alerts(
    days: int = Query(7, ge=1, le=30),
    min_confidence: str = Query("nominal"),
    region: str = Query(None, description="Region id"),
    db: Session = Depends(get_db),
):
    """Get recent fire alerts sorted by date."""
    r = get_region(region)
    west, south, east, north = r.bbox
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    alerts = (
        db.query(FireAlert)
        .filter(FireAlert.acq_date >= cutoff)
        .filter(FireAlert.latitude.between(south, north))
        .filter(FireAlert.longitude.between(west, east))
        .order_by(FireAlert.acq_date.desc(), FireAlert.acq_time.desc())
        .all()
    )

    confidence_order = {"low": 0, "nominal": 1, "high": 2}
    min_level = confidence_order.get(min_confidence, 1)

    result = []
    for a in alerts:
        if confidence_order.get(str(a.confidence).lower(), 0) < min_level:
            continue
        result.append({
            "id": a.id,
            "latitude": a.latitude,
            "longitude": a.longitude,
            "brightness": a.brightness,
            "acq_date": a.acq_date,
            "acq_time": a.acq_time,
            "satellite": a.satellite,
            "confidence": a.confidence,
            "frp": a.frp,
            "daynight": a.daynight,
        })

    return {"alerts": result, "count": len(result)}


@router.get("/fires/stats")
def get_fire_stats(
    days: int = Query(30, ge=1, le=365),
    region: str = Query(None, description="Region id"),
    db: Session = Depends(get_db),
):
    """Get fire statistics for the period."""
    r = get_region(region)
    west, south, east, north = r.bbox
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    base = (
        db.query(FireAlert)
        .filter(FireAlert.acq_date >= cutoff)
        .filter(FireAlert.latitude.between(south, north))
        .filter(FireAlert.longitude.between(west, east))
    )

    total = base.count()
    high_confidence = base.filter(FireAlert.confidence == "high").count()

    from sqlalchemy import func
    daily = (
        db.query(
            FireAlert.acq_date,
            func.count(FireAlert.id).label("count"),
        )
        .filter(FireAlert.acq_date >= cutoff)
        .filter(FireAlert.latitude.between(south, north))
        .filter(FireAlert.longitude.between(west, east))
        .group_by(FireAlert.acq_date)
        .order_by(FireAlert.acq_date)
        .all()
    )

    return {
        "total_fires": total,
        "high_confidence": high_confidence,
        "days": days,
        "daily_breakdown": [
            {"date": d.acq_date, "count": d.count} for d in daily
        ],
    }
