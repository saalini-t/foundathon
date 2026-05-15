"""
Data seeding script — fetches initial data from all connectors and stores in DB.

Usage:
    cd foundathon
    python -m backend.scripts.seed_data
"""

import logging
import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.db.database import init_db, SessionLocal
from backend.db.models import FireAlert, WeatherObservation, SpeciesOccurrence, GridCell

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def seed_fire_data(db, days: int = 7):
    """Fetch and store fire data from NASA FIRMS."""
    from backend.connectors.firms import FIRMSConnector

    logger.info("=== Seeding fire data from NASA FIRMS ===")
    connector = FIRMSConnector()
    records = connector.fetch(days=days)

    if not records:
        logger.warning("No fire data returned. Check FIRMS_API_KEY in .env")
        return 0

    inserted = 0
    for r in records:
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
    logger.info(f"Fire data: inserted {inserted} records.")
    return inserted


def seed_weather_data(db, days: int = 30):
    """Fetch and store weather data from Open-Meteo."""
    from datetime import datetime, timedelta
    from backend.connectors.open_meteo import OpenMeteoConnector

    logger.info("=== Seeding weather data from Open-Meteo ===")
    connector = OpenMeteoConnector()
    start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    end = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    records = connector.fetch(start_date=start, end_date=end)

    if not records:
        logger.warning("No weather data returned.")
        return 0

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
    logger.info(f"Weather data: inserted {inserted} records.")
    return inserted


def seed_grid_cells(db):
    """Generate and store reference grid cells for all 4 monitored regions."""
    from backend.connectors.ndvi import NDVIConnector
    from backend.regions import REGIONS

    logger.info("=== Seeding grid cells for all regions ===")
    total_inserted = 0

    for region_id in REGIONS:
        connector = NDVIConnector(region_id=region_id)
        cells = connector.get_grid_cells()

        for c in cells:
            existing = db.query(GridCell).filter(GridCell.cell_id == c["cell_id"]).first()
            if existing:
                continue
            db.add(GridCell(
                cell_id=c["cell_id"],
                lat_min=c["lat_min"],
                lat_max=c["lat_max"],
                lon_min=c["lon_min"],
                lon_max=c["lon_max"],
                center_lat=c["center_lat"],
                center_lon=c["center_lon"],
            ))
            total_inserted += 1

        logger.info(f"  {region_id}: {len(cells)} cells generated")

    db.commit()
    logger.info(f"Grid cells: inserted {total_inserted} records across {len(REGIONS)} regions.")
    return total_inserted


def seed_species_data(db, max_records: int = 2000):
    """Fetch and store species data from GBIF."""
    from backend.connectors.gbif import GBIFConnector

    logger.info("=== Seeding species data from GBIF ===")
    connector = GBIFConnector()
    records = connector.fetch_multiple_pages(max_records=max_records)

    if not records:
        logger.warning("No species data returned.")
        return 0

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
    logger.info(f"Species data: inserted {inserted} records.")
    return inserted


def main():
    logger.info("=" * 60)
    logger.info("Western Ghats Ecosystem Monitor — Data Seeding")
    logger.info("=" * 60)

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    # Initialize database
    logger.info("Initializing database...")
    init_db()

    db = SessionLocal()
    try:
        totals = {}

        # 1. Weather data (no API key needed, always works)
        totals["weather"] = seed_weather_data(db, days=30)

        # 2. Fire data (needs FIRMS API key)
        totals["fires"] = seed_fire_data(db, days=7)

        # 3. Species data (no API key needed)
        totals["species"] = seed_species_data(db, max_records=2000)

        # 4. Grid cells (reference grid for all regions)
        totals["grid_cells"] = seed_grid_cells(db)

        logger.info("=" * 60)
        logger.info("Seeding complete!")
        logger.info(f"  Weather records:  {totals['weather']}")
        logger.info(f"  Fire alerts:      {totals['fires']}")
        logger.info(f"  Species records:  {totals['species']}")
        logger.info(f"  Grid cells:       {totals['grid_cells']}")
        logger.info("=" * 60)

    finally:
        db.close()


if __name__ == "__main__":
    main()
