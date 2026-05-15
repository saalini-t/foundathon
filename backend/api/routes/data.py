"""Data API routes — weather, biodiversity queries."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.db.database import get_db
from backend.db.models import WeatherObservation, SpeciesOccurrence, FireAlert
from backend.regions import get_region

router = APIRouter(prefix="/api/data", tags=["data"])


@router.get("/weather/stations")
def get_weather_stations(
    region: str = Query(None, description="Region id"),
    db: Session = Depends(get_db),
):
    """Get list of weather stations with latest data."""
    r = get_region(region)
    west, south, east, north = r.bbox

    stations = (
        db.query(
            WeatherObservation.station_name,
            WeatherObservation.latitude,
            WeatherObservation.longitude,
            func.max(WeatherObservation.date).label("latest_date"),
            func.count(WeatherObservation.id).label("record_count"),
        )
        .filter(WeatherObservation.latitude.between(south, north))
        .filter(WeatherObservation.longitude.between(west, east))
        .group_by(WeatherObservation.station_name)
        .all()
    )

    return {
        "stations": [
            {
                "name": s.station_name,
                "latitude": s.latitude,
                "longitude": s.longitude,
                "latest_date": s.latest_date,
                "record_count": s.record_count,
            }
            for s in stations
        ]
    }


@router.get("/weather/history")
def get_weather_history(
    station: str = Query(..., description="Station name"),
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    """Get weather history for a specific station."""
    from datetime import datetime, timedelta

    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    records = (
        db.query(WeatherObservation)
        .filter(WeatherObservation.station_name == station)
        .filter(WeatherObservation.date >= cutoff)
        .order_by(WeatherObservation.date)
        .all()
    )

    return {
        "station": station,
        "records": [
            {
                "date": r.date,
                "temperature_max": r.temperature_max,
                "temperature_min": r.temperature_min,
                "temperature_mean": r.temperature_mean,
                "precipitation_sum": r.precipitation_sum,
                "humidity_mean": r.humidity_mean,
                "windspeed_max": r.windspeed_max,
            }
            for r in records
        ],
        "count": len(records),
    }


@router.get("/weather/current")
def get_current_weather(region: str = Query(None, description="Region id")):
    """Fetch live current weather from Open-Meteo (not from DB)."""
    from backend.connectors.open_meteo import OpenMeteoConnector

    connector = OpenMeteoConnector(region_id=region)
    data = connector.fetch_current()
    return {"stations": data, "count": len(data)}


@router.get("/species/summary")
def get_species_summary(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=500),
    region: str = Query(None, description="Region id"),
):
    """Get top species by occurrence count."""
    r = get_region(region)
    west, south, east, north = r.bbox

    results = (
        db.query(
            SpeciesOccurrence.species,
            SpeciesOccurrence.family,
            SpeciesOccurrence.kingdom,
            func.count(SpeciesOccurrence.id).label("count"),
        )
        .filter(SpeciesOccurrence.species.isnot(None))
        .filter(SpeciesOccurrence.latitude.between(south, north))
        .filter(SpeciesOccurrence.longitude.between(west, east))
        .group_by(SpeciesOccurrence.species)
        .order_by(func.count(SpeciesOccurrence.id).desc())
        .limit(limit)
        .all()
    )

    return {
        "species": [
            {
                "species": r.species,
                "family": r.family,
                "kingdom": r.kingdom,
                "occurrence_count": r.count,
            }
            for r in results
        ],
        "total_species": len(results),
    }


@router.get("/species/families")
def get_family_summary(
    db: Session = Depends(get_db),
    region: str = Query(None, description="Region id"),
):
    """Get species count grouped by family."""
    r = get_region(region)
    west, south, east, north = r.bbox

    results = (
        db.query(
            SpeciesOccurrence.family,
            SpeciesOccurrence.kingdom,
            func.count(func.distinct(SpeciesOccurrence.species)).label("species_count"),
            func.count(SpeciesOccurrence.id).label("occurrence_count"),
        )
        .filter(SpeciesOccurrence.family.isnot(None))
        .filter(SpeciesOccurrence.latitude.between(south, north))
        .filter(SpeciesOccurrence.longitude.between(west, east))
        .group_by(SpeciesOccurrence.family)
        .order_by(func.count(SpeciesOccurrence.id).desc())
        .all()
    )

    return {
        "families": [
            {
                "family": r.family,
                "kingdom": r.kingdom,
                "species_count": r.species_count,
                "occurrence_count": r.occurrence_count,
            }
            for r in results
        ]
    }


@router.get("/stats")
def get_overall_stats(
    db: Session = Depends(get_db),
    region: str = Query(None, description="Region id"),
):
    """Get overall platform statistics."""
    r = get_region(region)
    west, south, east, north = r.bbox

    fire_count = (
        db.query(FireAlert)
        .filter(FireAlert.latitude.between(south, north))
        .filter(FireAlert.longitude.between(west, east))
        .count()
    )
    weather_count = (
        db.query(WeatherObservation)
        .filter(WeatherObservation.latitude.between(south, north))
        .filter(WeatherObservation.longitude.between(west, east))
        .count()
    )
    species_occ_count = (
        db.query(SpeciesOccurrence)
        .filter(SpeciesOccurrence.latitude.between(south, north))
        .filter(SpeciesOccurrence.longitude.between(west, east))
        .count()
    )
    unique_species = (
        db.query(func.count(func.distinct(SpeciesOccurrence.species)))
        .filter(SpeciesOccurrence.latitude.between(south, north))
        .filter(SpeciesOccurrence.longitude.between(west, east))
        .scalar()
    )
    weather_stations = (
        db.query(func.count(func.distinct(WeatherObservation.station_name)))
        .filter(WeatherObservation.latitude.between(south, north))
        .filter(WeatherObservation.longitude.between(west, east))
        .scalar()
    )

    return {
        "fire_detections": fire_count,
        "weather_observations": weather_count,
        "weather_stations": weather_stations,
        "species_occurrences": species_occ_count,
        "unique_species": unique_species or 0,
    }
