"""
Ecosystem & Biodiversity Monitoring Platform
==============================================
FastAPI backend application — multi-region support.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.db.database import init_db
from backend.api.routes import map, alerts, data, predict
from backend.api.routes import context, verification, timemachine, narrative
from backend.regions import get_region, list_regions

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    logger.info("Initializing database...")
    init_db()
    logger.info("Database ready.")
    yield
    logger.info("Shutting down.")


app = FastAPI(
    title="Ecosystem & Biodiversity Monitor",
    description=(
        "AI-Powered Ecosystem & Biodiversity Monitoring Platform "
        "supporting multiple biodiversity hotspots worldwide."
    ),
    version="0.2.0",
    lifespan=lifespan,
)

# CORS — allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(map.router)
app.include_router(alerts.router)
app.include_router(data.router)
app.include_router(predict.router)
app.include_router(context.router)
app.include_router(verification.router)
app.include_router(timemachine.router)
app.include_router(narrative.router)


@app.get("/")
def root():
    return {
        "name": "Ecosystem & Biodiversity Monitor",
        "version": "0.2.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/api/regions", tags=["regions"])
def get_available_regions():
    """Return all available regions with their metadata."""
    regions = list_regions()
    return {
        "regions": [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "center": r.center,
                "zoom": r.zoom,
                "bbox": r.bbox,
                "country_codes": r.country_codes,
            }
            for r in regions
        ]
    }


# --- Data sync endpoints (trigger manually or via scheduler) ---

@app.post("/api/sync/fires", tags=["sync"])
def sync_fire_data(days: int = 7, region: str = Query(None, description="Region id")):
    """Fetch latest fire data from FIRMS and store in DB."""
    from backend.connectors.firms import FIRMSConnector
    from backend.db.database import SessionLocal
    from backend.db.models import FireAlert

    connector = FIRMSConnector()
    records = connector.fetch(days=days)

    if not records:
        return {"message": "No fire data fetched (check API key).", "count": 0}

    db = SessionLocal()
    try:
        inserted = 0
        for r in records:
            # Check for duplicate by lat/lon/date/time
            existing = (
                db.query(FireAlert)
                .filter(
                    FireAlert.latitude == r.get("latitude"),
                    FireAlert.longitude == r.get("longitude"),
                    FireAlert.acq_date == str(r.get("acq_date")),
                    FireAlert.acq_time == str(r.get("acq_time")),
                )
                .first()
            )
            if existing:
                continue

            alert = FireAlert(
                latitude=r.get("latitude"),
                longitude=r.get("longitude"),
                brightness=r.get("bright_ti4") or r.get("brightness"),
                scan=r.get("scan"),
                track=r.get("track"),
                acq_date=str(r.get("acq_date")),
                acq_time=str(r.get("acq_time")),
                satellite=r.get("satellite"),
                instrument=r.get("instrument"),
                confidence=str(r.get("confidence")),
                bright_t31=r.get("bright_ti5") or r.get("bright_t31"),
                frp=r.get("frp"),
                daynight=r.get("daynight"),
            )
            db.add(alert)
            inserted += 1

        db.commit()
        return {"message": f"Synced {inserted} new fire alerts.", "count": inserted}
    finally:
        db.close()


@app.post("/api/sync/weather", tags=["sync"])
def sync_weather_data(days: int = 30, region: str = Query(None, description="Region id")):
    """Fetch weather data from Open-Meteo and store in DB."""
    from datetime import datetime, timedelta
    from backend.connectors.open_meteo import OpenMeteoConnector
    from backend.db.database import SessionLocal
    from backend.db.models import WeatherObservation

    connector = OpenMeteoConnector(region_id=region)
    start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    end = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    records = connector.fetch(start_date=start, end_date=end)

    if not records:
        return {"message": "No weather data fetched.", "count": 0}

    db = SessionLocal()
    try:
        inserted = 0
        for r in records:
            existing = (
                db.query(WeatherObservation)
                .filter(
                    WeatherObservation.station_name == r.get("station_name"),
                    WeatherObservation.date == r.get("date"),
                )
                .first()
            )
            if existing:
                continue

            obs = WeatherObservation(
                latitude=r.get("latitude"),
                longitude=r.get("longitude"),
                station_name=r.get("station_name"),
                date=r.get("date"),
                temperature_max=r.get("temperature_max"),
                temperature_min=r.get("temperature_min"),
                temperature_mean=r.get("temperature_mean"),
                precipitation_sum=r.get("precipitation_sum"),
                rain_sum=r.get("rain_sum"),
                windspeed_max=r.get("windspeed_max"),
                humidity_mean=r.get("humidity_mean"),
                et0_fao=r.get("et0_fao"),
            )
            db.add(obs)
            inserted += 1

        db.commit()
        return {"message": f"Synced {inserted} weather observations.", "count": inserted}
    finally:
        db.close()


@app.post("/api/sync/species", tags=["sync"])
def sync_species_data(max_records: int = 2000, region: str = Query(None, description="Region id")):
    """Fetch species data from GBIF and store in DB."""
    from backend.connectors.gbif import GBIFConnector
    from backend.db.database import SessionLocal
    from backend.db.models import SpeciesOccurrence

    connector = GBIFConnector(region_id=region)
    records = connector.fetch_multiple_pages(max_records=max_records)

    if not records:
        return {"message": "No species data fetched.", "count": 0}

    db = SessionLocal()
    try:
        inserted = 0
        for r in records:
            gbif_id = r.get("gbif_id")
            if gbif_id:
                existing = (
                    db.query(SpeciesOccurrence)
                    .filter(SpeciesOccurrence.gbif_id == gbif_id)
                    .first()
                )
                if existing:
                    continue

            occ = SpeciesOccurrence(
                gbif_id=gbif_id,
                species=r.get("species"),
                genus=r.get("genus"),
                family=r.get("family"),
                order=r.get("order"),
                class_name=r.get("class_name"),
                phylum=r.get("phylum"),
                kingdom=r.get("kingdom"),
                latitude=r.get("latitude"),
                longitude=r.get("longitude"),
                event_date=r.get("event_date"),
                basis_of_record=r.get("basis_of_record"),
                country=r.get("country"),
                state_province=r.get("state_province"),
                coordinate_uncertainty=r.get("coordinate_uncertainty"),
            )
            db.add(occ)
            inserted += 1

        db.commit()
        return {"message": f"Synced {inserted} species occurrences.", "count": inserted}
    finally:
        db.close()


@app.post("/api/sync/all", tags=["sync"])
def sync_all_data():
    """Sync all data sources."""
    results = {}
    results["fires"] = sync_fire_data(days=7)
    results["weather"] = sync_weather_data(days=30)
    results["species"] = sync_species_data(max_records=2000)
    return results
