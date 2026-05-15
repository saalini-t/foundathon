"""
Feature 2 — Ground Truth Verification Loop
=============================================
Webhook endpoint for field agents to verify/resolve alerts
with photos, GPS coords, and status updates.
"""

import logging
import os
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.models import FieldVerification, FireAlert

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/verify", tags=["verification"])

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/report")
async def submit_verification(
    latitude: float = Form(...),
    longitude: float = Form(...),
    message: str = Form(...),
    status: str = Form("verified"),  # verified | resolved | false_alarm
    alert_id: int | None = Form(None),
    alert_type: str = Form("fire"),
    reporter_name: str | None = Form(None),
    photo: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    """
    Accept a field verification report (simulating WhatsApp / SMS webhook).
    Optionally includes a photo upload.
    """
    photo_path = None
    if photo and photo.filename:
        # Sanitize filename
        ext = os.path.splitext(photo.filename)[1][:5]  # limit extension length
        safe_name = f"{uuid.uuid4().hex}{ext}"
        photo_path = os.path.join(UPLOAD_DIR, safe_name)
        contents = await photo.read()
        with open(photo_path, "wb") as f:
            f.write(contents)
        photo_path = f"uploads/{safe_name}"

    report = FieldVerification(
        alert_id=alert_id,
        alert_type=alert_type,
        latitude=latitude,
        longitude=longitude,
        message=message,
        photo_path=photo_path,
        status=status,
        reporter_name=reporter_name,
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    return {
        "id": report.id,
        "message": "Verification report submitted.",
        "status": report.status,
        "alert_id": report.alert_id,
        "photo_path": report.photo_path,
    }


@router.get("/reports")
def list_verifications(
    region: str = Query(None, description="Region id"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """List recent verification reports, optionally filtered by region bbox."""
    from backend.regions import get_region

    query = db.query(FieldVerification).order_by(FieldVerification.created_at.desc())

    if region:
        r = get_region(region)
        west, south, east, north = r.bbox
        query = query.filter(
            FieldVerification.latitude.between(south, north),
            FieldVerification.longitude.between(west, east),
        )

    reports = query.limit(limit).all()

    return {
        "reports": [
            {
                "id": rpt.id,
                "alert_id": rpt.alert_id,
                "alert_type": rpt.alert_type,
                "latitude": rpt.latitude,
                "longitude": rpt.longitude,
                "message": rpt.message,
                "photo_path": rpt.photo_path,
                "status": rpt.status,
                "reporter_name": rpt.reporter_name,
                "created_at": rpt.created_at.isoformat() if rpt.created_at else None,
            }
            for rpt in reports
        ],
        "count": len(reports),
    }


@router.get("/status/{alert_id}")
def get_alert_verification_status(
    alert_id: int,
    alert_type: str = Query("fire"),
    db: Session = Depends(get_db),
):
    """Check if a specific alert has been verified by the field."""
    reports = (
        db.query(FieldVerification)
        .filter(
            FieldVerification.alert_id == alert_id,
            FieldVerification.alert_type == alert_type,
        )
        .order_by(FieldVerification.created_at.desc())
        .all()
    )

    if not reports:
        return {"alert_id": alert_id, "verified": False, "reports": []}

    latest = reports[0]
    return {
        "alert_id": alert_id,
        "verified": True,
        "latest_status": latest.status,
        "report_count": len(reports),
        "latest_report": {
            "id": latest.id,
            "message": latest.message,
            "status": latest.status,
            "reporter_name": latest.reporter_name,
            "photo_path": latest.photo_path,
            "created_at": latest.created_at.isoformat() if latest.created_at else None,
        },
    }
