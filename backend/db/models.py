from sqlalchemy import Column, Integer, Float, String, DateTime, Text, Index, Boolean
from sqlalchemy.sql import func
from backend.db.database import Base


class FireAlert(Base):
    """Active fire detections from NASA FIRMS."""
    __tablename__ = "fire_alerts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    brightness = Column(Float)
    scan = Column(Float)
    track = Column(Float)
    acq_date = Column(String, nullable=False)
    acq_time = Column(String)
    satellite = Column(String)
    instrument = Column(String)
    confidence = Column(String)
    bright_t31 = Column(Float)
    frp = Column(Float)  # Fire Radiative Power
    daynight = Column(String)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_fire_lat_lon", "latitude", "longitude"),
        Index("idx_fire_date", "acq_date"),
    )


class WeatherObservation(Base):
    """Weather data from Open-Meteo."""
    __tablename__ = "weather_observations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    station_name = Column(String)
    date = Column(String, nullable=False)
    temperature_max = Column(Float)
    temperature_min = Column(Float)
    temperature_mean = Column(Float)
    precipitation_sum = Column(Float)
    rain_sum = Column(Float)
    windspeed_max = Column(Float)
    humidity_mean = Column(Float)
    et0_fao = Column(Float)  # Reference evapotranspiration
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_weather_lat_lon", "latitude", "longitude"),
        Index("idx_weather_date", "date"),
        Index("idx_weather_station", "station_name"),
    )


class SpeciesOccurrence(Base):
    """Biodiversity occurrence records from GBIF."""
    __tablename__ = "species_occurrences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    gbif_id = Column(Integer)
    species = Column(String, nullable=False)
    genus = Column(String)
    family = Column(String)
    order = Column(String)
    class_name = Column(String)  # 'class' is reserved in Python
    phylum = Column(String)
    kingdom = Column(String)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    event_date = Column(String)
    basis_of_record = Column(String)
    country = Column(String)
    state_province = Column(String)
    iucn_status = Column(String)
    coordinate_uncertainty = Column(Float)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_species_lat_lon", "latitude", "longitude"),
        Index("idx_species_name", "species"),
        Index("idx_species_family", "family"),
        Index("idx_species_date", "event_date"),
    )


class GridCell(Base):
    """Reference grid cells covering the Western Ghats."""
    __tablename__ = "grid_cells"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cell_id = Column(String, unique=True, nullable=False)
    lat_min = Column(Float, nullable=False)
    lat_max = Column(Float, nullable=False)
    lon_min = Column(Float, nullable=False)
    lon_max = Column(Float, nullable=False)
    center_lat = Column(Float, nullable=False)
    center_lon = Column(Float, nullable=False)
    # Aggregated metrics (computed by sync tasks)
    fire_count_30d = Column(Integer, default=0)
    species_count = Column(Integer, default=0)
    ndvi_latest = Column(Float)
    ehi_score = Column(Float)

    __table_args__ = (
        Index("idx_grid_center", "center_lat", "center_lon"),
    )


class FieldVerification(Base):
    """Ground-truth verification reports from field agents."""
    __tablename__ = "field_verifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    alert_id = Column(Integer, nullable=True)       # FK to fire_alerts.id (nullable for standalone reports)
    alert_type = Column(String, default="fire")      # "fire" or "anomaly"
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    message = Column(Text, nullable=False)
    photo_path = Column(String, nullable=True)       # path to uploaded image
    status = Column(String, default="verified")       # verified | resolved | false_alarm
    reporter_name = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_verify_alert", "alert_id", "alert_type"),
        Index("idx_verify_coords", "latitude", "longitude"),
    )
