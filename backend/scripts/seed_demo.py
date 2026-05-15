"""
Demo data seeder — adds compelling, realistic fire alerts and anomalies
for demonstration purposes across all supported regions.

Usage:
    cd foundathon
    python -m backend.scripts.seed_demo
"""

import logging
import os
import sys
import random
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.db.database import init_db, SessionLocal
from backend.db.models import FireAlert, SpeciesOccurrence
from backend.regions import list_regions

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def seed_fire_alerts(db):
    """Generate realistic fire detection records for every registered region."""
    rng = random.Random(42)
    now = datetime.now()
    total_inserted = 0

    for region in list_regions():
        logger.info(f"Seeding fires for {region.name}...")
        for cluster in region.fire_clusters:
            lat_c, lon_c = cluster.center
            radius = cluster.radius
            count = cluster.count

            for i in range(count):
                lat = lat_c + rng.uniform(-radius, radius)
                lon = lon_c + rng.uniform(-radius, radius)

                days_ago = rng.randint(0, 4)
                fire_date = now - timedelta(days=days_ago)
                hour = rng.choice([1, 2, 13, 14])
                minute = rng.randint(0, 59)
                acq_time = f"{hour:02d}{minute:02d}"

                confidence = rng.choices(
                    ["high", "nominal", "low"],
                    weights=[0.5, 0.35, 0.15],
                    k=1,
                )[0]

                if confidence == "high":
                    frp = round(rng.uniform(15.0, 180.0), 1)
                elif confidence == "nominal":
                    frp = round(rng.uniform(5.0, 60.0), 1)
                else:
                    frp = round(rng.uniform(1.0, 15.0), 1)

                brightness = round(rng.uniform(310.0, 380.0), 1)
                bright_t31 = round(brightness - rng.uniform(10, 30), 1)
                satellite = rng.choice(["N", "N", "1"])
                daynight = "N" if hour < 6 else "D"

                alert = FireAlert(
                    latitude=round(lat, 4),
                    longitude=round(lon, 4),
                    brightness=brightness,
                    scan=round(rng.uniform(0.3, 1.2), 1),
                    track=round(rng.uniform(0.3, 1.0), 1),
                    acq_date=fire_date.strftime("%Y-%m-%d"),
                    acq_time=acq_time,
                    satellite=satellite,
                    instrument="VIIRS",
                    confidence=confidence,
                    bright_t31=bright_t31,
                    frp=frp,
                    daynight=daynight,
                )
                db.add(alert)
                total_inserted += 1

            logger.info(f"  🔥 {cluster.name}: {count} fire detections")

    db.commit()
    return total_inserted


# ── Region-specific species for demo data ──────────────────────────────────
REGION_SPECIES = {
    "western_ghats": {
        "country": "India",
        "species": [
            {"species": "Nasikabatrachus sahyadrensis", "genus": "Nasikabatrachus", "family": "Nasikabatrachidae", "order": "Anura", "class_name": "Amphibia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "EN"},
            {"species": "Raorchestes chalazodes", "genus": "Raorchestes", "family": "Rhacophoridae", "order": "Anura", "class_name": "Amphibia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "CR"},
            {"species": "Macaca silenus", "genus": "Macaca", "family": "Cercopithecidae", "order": "Primates", "class_name": "Mammalia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "EN"},
            {"species": "Panthera tigris", "genus": "Panthera", "family": "Felidae", "order": "Carnivora", "class_name": "Mammalia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "EN"},
            {"species": "Elephas maximus", "genus": "Elephas", "family": "Elephantidae", "order": "Proboscidea", "class_name": "Mammalia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "EN"},
            {"species": "Buceros bicornis", "genus": "Buceros", "family": "Bucerotidae", "order": "Bucerotiformes", "class_name": "Aves", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "VU"},
            {"species": "Nilgiritragus hylocrius", "genus": "Nilgiritragus", "family": "Bovidae", "order": "Artiodactyla", "class_name": "Mammalia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "EN"},
            {"species": "Dipterocarpus indicus", "genus": "Dipterocarpus", "family": "Dipterocarpaceae", "order": "Malvales", "class_name": "Magnoliopsida", "phylum": "Tracheophyta", "kingdom": "Plantae", "iucn": "CR"},
            {"species": "Impatiens jerdoniae", "genus": "Impatiens", "family": "Balsaminaceae", "order": "Ericales", "class_name": "Magnoliopsida", "phylum": "Tracheophyta", "kingdom": "Plantae", "iucn": "EN"},
            {"species": "Python molurus", "genus": "Python", "family": "Pythonidae", "order": "Squamata", "class_name": "Reptilia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "NT"},
        ],
    },
    "amazon_rainforest": {
        "country": "Brazil",
        "species": [
            {"species": "Panthera onca", "genus": "Panthera", "family": "Felidae", "order": "Carnivora", "class_name": "Mammalia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "NT"},
            {"species": "Harpia harpyja", "genus": "Harpia", "family": "Accipitridae", "order": "Accipitriformes", "class_name": "Aves", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "VU"},
            {"species": "Pteronura brasiliensis", "genus": "Pteronura", "family": "Mustelidae", "order": "Carnivora", "class_name": "Mammalia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "EN"},
            {"species": "Trichechus inunguis", "genus": "Trichechus", "family": "Trichechidae", "order": "Sirenia", "class_name": "Mammalia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "VU"},
            {"species": "Ara chloropterus", "genus": "Ara", "family": "Psittacidae", "order": "Psittaciformes", "class_name": "Aves", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "LC"},
            {"species": "Dendrobates tinctorius", "genus": "Dendrobates", "family": "Dendrobatidae", "order": "Anura", "class_name": "Amphibia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "LC"},
            {"species": "Inia geoffrensis", "genus": "Inia", "family": "Iniidae", "order": "Cetacea", "class_name": "Mammalia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "EN"},
            {"species": "Bradypus variegatus", "genus": "Bradypus", "family": "Bradypodidae", "order": "Pilosa", "class_name": "Mammalia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "LC"},
            {"species": "Victoria amazonica", "genus": "Victoria", "family": "Nymphaeaceae", "order": "Nymphaeales", "class_name": "Magnoliopsida", "phylum": "Tracheophyta", "kingdom": "Plantae", "iucn": "LC"},
            {"species": "Bertholletia excelsa", "genus": "Bertholletia", "family": "Lecythidaceae", "order": "Ericales", "class_name": "Magnoliopsida", "phylum": "Tracheophyta", "kingdom": "Plantae", "iucn": "VU"},
        ],
    },
    "borneo": {
        "country": "Malaysia",
        "species": [
            {"species": "Pongo pygmaeus", "genus": "Pongo", "family": "Hominidae", "order": "Primates", "class_name": "Mammalia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "CR"},
            {"species": "Elephas maximus borneensis", "genus": "Elephas", "family": "Elephantidae", "order": "Proboscidea", "class_name": "Mammalia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "EN"},
            {"species": "Neofelis diardi", "genus": "Neofelis", "family": "Felidae", "order": "Carnivora", "class_name": "Mammalia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "VU"},
            {"species": "Nasalis larvatus", "genus": "Nasalis", "family": "Cercopithecidae", "order": "Primates", "class_name": "Mammalia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "EN"},
            {"species": "Rhinoceros sondaicus", "genus": "Rhinoceros", "family": "Rhinocerotidae", "order": "Perissodactyla", "class_name": "Mammalia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "CR"},
            {"species": "Buceros rhinoceros", "genus": "Buceros", "family": "Bucerotidae", "order": "Bucerotiformes", "class_name": "Aves", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "VU"},
            {"species": "Rafflesia arnoldii", "genus": "Rafflesia", "family": "Rafflesiaceae", "order": "Malpighiales", "class_name": "Magnoliopsida", "phylum": "Tracheophyta", "kingdom": "Plantae", "iucn": "EN"},
            {"species": "Nepenthes rajah", "genus": "Nepenthes", "family": "Nepenthaceae", "order": "Caryophyllales", "class_name": "Magnoliopsida", "phylum": "Tracheophyta", "kingdom": "Plantae", "iucn": "EN"},
            {"species": "Varanus salvator", "genus": "Varanus", "family": "Varanidae", "order": "Squamata", "class_name": "Reptilia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "LC"},
            {"species": "Helarctos malayanus", "genus": "Helarctos", "family": "Ursidae", "order": "Carnivora", "class_name": "Mammalia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "VU"},
        ],
    },
    "eastern_himalaya": {
        "country": "India",
        "species": [
            {"species": "Ailurus fulgens", "genus": "Ailurus", "family": "Ailuridae", "order": "Carnivora", "class_name": "Mammalia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "EN"},
            {"species": "Panthera uncia", "genus": "Panthera", "family": "Felidae", "order": "Carnivora", "class_name": "Mammalia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "VU"},
            {"species": "Budorcas taxicolor", "genus": "Budorcas", "family": "Bovidae", "order": "Artiodactyla", "class_name": "Mammalia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "VU"},
            {"species": "Tragopan blythii", "genus": "Tragopan", "family": "Phasianidae", "order": "Galliformes", "class_name": "Aves", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "VU"},
            {"species": "Neofelis nebulosa", "genus": "Neofelis", "family": "Felidae", "order": "Carnivora", "class_name": "Mammalia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "VU"},
            {"species": "Bucerotidae bicornis", "genus": "Buceros", "family": "Bucerotidae", "order": "Bucerotiformes", "class_name": "Aves", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "VU"},
            {"species": "Rhododendron arboreum", "genus": "Rhododendron", "family": "Ericaceae", "order": "Ericales", "class_name": "Magnoliopsida", "phylum": "Tracheophyta", "kingdom": "Plantae", "iucn": "LC"},
            {"species": "Magnolia campbellii", "genus": "Magnolia", "family": "Magnoliaceae", "order": "Magnoliales", "class_name": "Magnoliopsida", "phylum": "Tracheophyta", "kingdom": "Plantae", "iucn": "EN"},
            {"species": "Ophiophagus hannah", "genus": "Ophiophagus", "family": "Elapidae", "order": "Squamata", "class_name": "Reptilia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "VU"},
            {"species": "Moschus chrysogaster", "genus": "Moschus", "family": "Moschidae", "order": "Artiodactyla", "class_name": "Mammalia", "phylum": "Chordata", "kingdom": "Animalia", "iucn": "EN"},
        ],
    },
}


def seed_species(db):
    """Generate realistic species occurrence records for every region."""
    rng = random.Random(99)
    now = datetime.now()
    total_inserted = 0

    for region in list_regions():
        rid = region.id
        spec_cfg = REGION_SPECIES.get(rid)
        if not spec_cfg:
            continue

        west, south, east, north = region.bbox
        country = spec_cfg["country"]
        species_list = spec_cfg["species"]
        logger.info(f"Seeding species for {region.name}...")

        for sp in species_list:
            # 15-40 occurrences per species scattered within bbox
            n_occ = rng.randint(15, 40)
            for _ in range(n_occ):
                lat = round(rng.uniform(south + 0.2, north - 0.2), 5)
                lon = round(rng.uniform(west + 0.2, east - 0.2), 5)
                days_ago = rng.randint(0, 365)
                event_date = (now - timedelta(days=days_ago)).strftime("%Y-%m-%d")

                occ = SpeciesOccurrence(
                    gbif_id=rng.randint(1_000_000_000, 4_000_000_000),
                    species=sp["species"],
                    genus=sp["genus"],
                    family=sp["family"],
                    order=sp["order"],
                    class_name=sp["class_name"],
                    phylum=sp["phylum"],
                    kingdom=sp["kingdom"],
                    latitude=lat,
                    longitude=lon,
                    event_date=event_date,
                    basis_of_record="HUMAN_OBSERVATION",
                    country=country,
                    iucn_status=sp.get("iucn"),
                    coordinate_uncertainty=round(rng.uniform(5.0, 500.0), 1),
                )
                db.add(occ)
                total_inserted += 1

            logger.info(f"  🧬 {sp['species']}: {n_occ} occurrences")

    db.commit()
    return total_inserted


def retrain_models_all_regions():
    """Retrain anomaly + fire models per region for demo sensitivity."""
    from backend.ml.anomaly import train_anomaly_model
    from backend.ml.fire_risk import train_fire_model as _train_fire

    for region in list_regions():
        rid = region.id
        logger.info(f"Training models for {region.name}...")
        _train_fire(n_samples=8000, region_id=rid)
        train_anomaly_model(n_samples=3000, contamination=0.08, region_id=rid)
        logger.info(f"  ✅ Models ready for {region.name}")


def main():
    logger.info("=" * 60)
    logger.info("Demo Data Seeder — Multi-Region Ecosystem Monitor")
    logger.info("=" * 60)

    os.makedirs("data", exist_ok=True)
    init_db()

    db = SessionLocal()
    try:
        n_fires = seed_fire_alerts(db)
        logger.info(f"Total fire alerts seeded: {n_fires}")

        n_species = seed_species(db)
        logger.info(f"Total species occurrences seeded: {n_species}")

        retrain_models_all_regions()

        regions = list_regions()
        logger.info("=" * 60)
        logger.info("Demo seeding complete!")
        logger.info(f"  🔥 {n_fires} fire alerts across {len(regions)} regions")
        logger.info(f"  🧬 {n_species} species occurrences across {len(regions)} regions")
        logger.info("  ✅ ML models trained per region")
        logger.info("=" * 60)
    finally:
        db.close()


if __name__ == "__main__":
    main()
