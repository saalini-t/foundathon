"""Map data API routes — boundary, grid cells, layers."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.db.database import get_db
from backend.db.models import FireAlert, SpeciesOccurrence, GridCell
from backend.utils.geo import load_boundary
from backend.regions import get_region, list_regions

router = APIRouter(prefix="/api/map", tags=["map"])


@router.get("/boundary")
def get_boundary(region: str = Query(None, description="Region id")):
    """Return the boundary GeoJSON for the selected region."""
    r = get_region(region)
    return load_boundary(r.boundary_file)


@router.get("/fire-layer")
def get_fire_layer(
    days: int = Query(7, ge=1, le=30, description="Number of past days"),
    min_confidence: str = Query("nominal", description="Minimum confidence: low, nominal, high"),
    region: str = Query(None, description="Region id"),
    db: Session = Depends(get_db),
):
    """Return fire detections as GeoJSON for map display."""
    from datetime import datetime, timedelta

    r = get_region(region)
    west, south, east, north = r.bbox
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    query = (
        db.query(FireAlert)
        .filter(FireAlert.acq_date >= cutoff)
        .filter(FireAlert.latitude.between(south, north))
        .filter(FireAlert.longitude.between(west, east))
    )

    confidence_order = {"low": 0, "nominal": 1, "high": 2}
    min_level = confidence_order.get(min_confidence, 1)

    alerts = query.all()

    features = []
    for a in alerts:
        alert_level = confidence_order.get(str(a.confidence).lower(), 0)
        if alert_level < min_level:
            continue
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [a.longitude, a.latitude],
            },
            "properties": {
                "id": a.id,
                "brightness": a.brightness,
                "acq_date": a.acq_date,
                "acq_time": a.acq_time,
                "satellite": a.satellite,
                "confidence": a.confidence,
                "frp": a.frp,
                "daynight": a.daynight,
            },
        })

    return {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {"count": len(features), "days": days},
    }


@router.get("/species-layer")
def get_species_layer(
    limit: int = Query(500, ge=1, le=5000),
    family: str = Query(None, description="Filter by family name"),
    region: str = Query(None, description="Region id"),
    db: Session = Depends(get_db),
):
    """Return species occurrences as GeoJSON for map display."""
    r = get_region(region)
    west, south, east, north = r.bbox
    query = (
        db.query(SpeciesOccurrence)
        .filter(SpeciesOccurrence.latitude.between(south, north))
        .filter(SpeciesOccurrence.longitude.between(west, east))
    )

    if family:
        query = query.filter(SpeciesOccurrence.family == family)

    query = query.limit(limit)
    occurrences = query.all()

    features = []
    for o in occurrences:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [o.longitude, o.latitude],
            },
            "properties": {
                "species": o.species,
                "genus": o.genus,
                "family": o.family,
                "kingdom": o.kingdom,
                "event_date": o.event_date,
                "basis_of_record": o.basis_of_record,
                "state_province": o.state_province,
            },
        })

    return {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {"count": len(features)},
    }


@router.get("/species-heatmap")
def get_species_heatmap(
    region: str = Query(None, description="Region id"),
    db: Session = Depends(get_db),
):
    """
    Return species density data for heatmap visualization.
    Groups occurrences into ~0.1° cells and counts species per cell.
    """
    r = get_region(region)
    west, south, east, north = r.bbox
    results = (
        db.query(
            func.round(SpeciesOccurrence.latitude, 1).label("lat"),
            func.round(SpeciesOccurrence.longitude, 1).label("lon"),
            func.count(func.distinct(SpeciesOccurrence.species)).label("species_count"),
            func.count(SpeciesOccurrence.id).label("occurrence_count"),
        )
        .filter(SpeciesOccurrence.latitude.between(south, north))
        .filter(SpeciesOccurrence.longitude.between(west, east))
        .group_by("lat", "lon")
        .all()
    )

    points = [
        {
            "lat": float(r.lat),
            "lon": float(r.lon),
            "species_count": r.species_count,
            "occurrence_count": r.occurrence_count,
        }
        for r in results
    ]

    return {"points": points, "count": len(points)}
