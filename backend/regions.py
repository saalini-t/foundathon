"""
Multi-Region Configuration Registry
=====================================
Defines biodiversity hotspots the platform can monitor.
Each region carries its own bbox, map view, weather stations,
climate profile (for ML training data), NDVI baselines, and
demo fire-cluster locations.

Add a new region by appending to REGIONS below.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ClimateProfile:
    """Regional climate parameters used to generate synthetic ML training data."""
    lat_range: tuple[float, float]          # (south, north)
    dry_months: list[int]                    # months considered "dry season"
    ndvi_mean: float                         # mean NDVI for region
    ndvi_std: float                          # NDVI standard deviation
    ndvi_deciduous_threshold_lat: float | None  # lat above which deciduous NDVI applies (or None)
    ndvi_wet: float                          # NDVI during wet season
    ndvi_dry: float                          # NDVI during dry season
    temp_mean: float                         # °C baseline temperature
    temp_lat_gradient: float                 # °C per degree latitude from south
    temp_dry_offset: float                   # °C added in dry season
    temp_wet_offset: float                   # °C added in wet season
    precip_dry_scale: float                  # exponential scale for dry-season rainfall (mm)
    precip_wet_scale: float                  # exponential scale for wet-season rainfall (mm)
    humidity_dry_mean: float
    humidity_wet_mean: float
    anomaly_contamination: float = 0.08


@dataclass(frozen=True)
class Station:
    name: str
    lat: float
    lon: float
    state: str  # administrative region label


@dataclass(frozen=True)
class FireCluster:
    name: str
    center: tuple[float, float]
    radius: float
    count: int


@dataclass(frozen=True)
class NdviZone:
    """Latitude band with longitude limits for cell-filtering."""
    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float


@dataclass(frozen=True)
class Region:
    id: str
    name: str
    description: str
    bbox: tuple[float, float, float, float]   # (west, south, east, north)
    center: tuple[float, float]               # (lat, lon) for map view
    zoom: int
    country_codes: list[str]                  # ISO-2 for GBIF queries
    timezone: str
    climate: ClimateProfile
    stations: list[Station]
    fire_clusters: list[FireCluster]
    ndvi_zones: list[NdviZone]                # cell-filter bands (replaces WG approx)
    boundary_file: str                        # filename under data/boundary/


# ---------------------------------------------------------------------------
# Region definitions
# ---------------------------------------------------------------------------

WESTERN_GHATS = Region(
    id="western_ghats",
    name="Western Ghats",
    description="UNESCO World Heritage mountain chain along India's west coast — one of the world's 8 hottest biodiversity hotspots.",
    bbox=(72.5, 8.0, 78.5, 21.5),
    center=(13.5, 75.8),
    zoom=6,
    country_codes=["IN"],
    timezone="Asia/Kolkata",
    climate=ClimateProfile(
        lat_range=(8.5, 20.5),
        dry_months=[1, 2, 3, 4, 5],
        ndvi_mean=0.68, ndvi_std=0.08,
        ndvi_deciduous_threshold_lat=14.0,
        ndvi_wet=0.70, ndvi_dry=0.55,
        temp_mean=25.0, temp_lat_gradient=0.3,
        temp_dry_offset=5.0, temp_wet_offset=-2.0,
        precip_dry_scale=10.0, precip_wet_scale=150.0,
        humidity_dry_mean=35.0, humidity_wet_mean=70.0,
    ),
    stations=[
        Station("Mahabaleshwar", 17.92, 73.66, "Maharashtra"),
        Station("Pune (Western Ghats edge)", 18.52, 73.86, "Maharashtra"),
        Station("Amboli", 15.96, 74.00, "Maharashtra"),
        Station("Castle Rock (Goa)", 15.40, 74.33, "Goa"),
        Station("Agumbe", 13.50, 75.10, "Karnataka"),
        Station("Kudremukh", 13.18, 75.25, "Karnataka"),
        Station("Kodagu (Coorg)", 12.42, 75.74, "Karnataka"),
        Station("Wayanad", 11.69, 76.08, "Kerala"),
        Station("Silent Valley", 11.07, 76.43, "Kerala"),
        Station("Munnar", 10.09, 77.06, "Kerala"),
    ],
    fire_clusters=[
        FireCluster("Wayanad Wildlife Sanctuary", (11.72, 76.08), 0.15, 6),
        FireCluster("Bandipur National Park", (11.66, 76.63), 0.12, 5),
        FireCluster("Kudremukh National Park", (13.18, 75.25), 0.10, 3),
        FireCluster("Mudumalai Tiger Reserve", (11.56, 76.55), 0.08, 4),
        FireCluster("Nilgiri Biosphere Reserve", (11.40, 76.70), 0.12, 3),
        FireCluster("Anshi National Park", (15.01, 74.33), 0.10, 2),
        FireCluster("Koyna Wildlife Sanctuary", (17.40, 73.75), 0.10, 3),
        FireCluster("Periyar Tiger Reserve", (9.47, 77.17), 0.08, 2),
        FireCluster("Sharavathi Valley", (14.05, 74.80), 0.06, 2),
        FireCluster("Dandeli Wildlife Sanctuary", (15.25, 74.60), 0.08, 2),
    ],
    ndvi_zones=[
        NdviZone(8.0, 10.5, 76.0, 77.5),    # Southern tip (Kerala)
        NdviZone(10.5, 13.0, 74.8, 76.5),   # Kerala / Karnataka
        NdviZone(13.0, 16.0, 74.0, 76.0),   # Karnataka / Goa
        NdviZone(16.0, 18.0, 73.5, 75.5),   # Goa / Maharashtra
        NdviZone(18.0, 20.5, 73.0, 74.5),   # Maharashtra
        NdviZone(20.5, 21.5, 73.0, 74.0),   # Northern tip
    ],
    boundary_file="western_ghats.geojson",
)


AMAZON_RAINFOREST = Region(
    id="amazon_rainforest",
    name="Amazon Rainforest",
    description="World's largest tropical rainforest — 10% of all species on Earth. Central Amazon basin covering Amazonas and Pará states.",
    bbox=(-70.0, -10.0, -50.0, 2.0),
    center=(-3.0, -60.0),
    zoom=5,
    country_codes=["BR"],
    timezone="America/Manaus",
    climate=ClimateProfile(
        lat_range=(-9.5, 1.5),
        dry_months=[6, 7, 8, 9, 10],
        ndvi_mean=0.82, ndvi_std=0.05,
        ndvi_deciduous_threshold_lat=None,
        ndvi_wet=0.85, ndvi_dry=0.75,
        temp_mean=27.0, temp_lat_gradient=0.1,
        temp_dry_offset=3.0, temp_wet_offset=-1.0,
        precip_dry_scale=30.0, precip_wet_scale=250.0,
        humidity_dry_mean=60.0, humidity_wet_mean=85.0,
    ),
    stations=[
        Station("Manaus", -3.12, -60.02, "Amazonas"),
        Station("Belém", -1.46, -48.50, "Pará"),
        Station("Santarém", -2.44, -54.71, "Pará"),
        Station("Tefé", -3.35, -64.71, "Amazonas"),
        Station("Porto Velho", -8.76, -63.90, "Rondônia"),
        Station("Macapá", 0.03, -51.07, "Amapá"),
        Station("Marabá", -5.37, -49.12, "Pará"),
        Station("Altamira", -3.20, -52.21, "Pará"),
        Station("Itaituba", -4.28, -55.99, "Pará"),
        Station("São Gabriel da Cachoeira", -0.13, -67.09, "Amazonas"),
    ],
    fire_clusters=[
        FireCluster("Deforestation Arc — Rondônia", (-9.50, -63.50), 0.25, 7),
        FireCluster("Trans-Amazonian Highway", (-3.80, -52.00), 0.20, 5),
        FireCluster("Xingu Indigenous Park edge", (-5.50, -53.50), 0.15, 4),
        FireCluster("BR-163 Corridor", (-4.50, -55.50), 0.20, 4),
        FireCluster("Jamanxim National Forest", (-5.80, -55.80), 0.12, 3),
        FireCluster("Tapajós National Forest", (-3.30, -55.00), 0.10, 3),
        FireCluster("Amazonas floodplain", (-3.00, -60.50), 0.15, 2),
        FireCluster("Marabá Deforestation Front", (-5.30, -49.50), 0.18, 4),
    ],
    ndvi_zones=[
        NdviZone(-10.0, -6.0, -70.0, -50.0),   # Southern Amazon
        NdviZone(-6.0, -2.0, -70.0, -50.0),     # Central Amazon
        NdviZone(-2.0, 2.0, -70.0, -50.0),      # Northern Amazon
    ],
    boundary_file="amazon_rainforest.geojson",
)


BORNEO = Region(
    id="borneo",
    name="Borneo Rainforest",
    description="Third-largest island on Earth — ancient rainforest hosting orangutans, pygmy elephants, and over 15,000 plant species. Major palm-oil deforestation hotspot.",
    bbox=(108.0, -4.5, 119.5, 7.5),
    center=(1.5, 114.0),
    zoom=6,
    country_codes=["MY", "ID", "BN"],
    timezone="Asia/Kuching",
    climate=ClimateProfile(
        lat_range=(-4.0, 7.0),
        dry_months=[2, 3, 4, 7, 8, 9],
        ndvi_mean=0.80, ndvi_std=0.06,
        ndvi_deciduous_threshold_lat=None,
        ndvi_wet=0.84, ndvi_dry=0.72,
        temp_mean=27.5, temp_lat_gradient=0.05,
        temp_dry_offset=2.0, temp_wet_offset=-0.5,
        precip_dry_scale=40.0, precip_wet_scale=200.0,
        humidity_dry_mean=65.0, humidity_wet_mean=88.0,
    ),
    stations=[
        Station("Kuching", 1.55, 110.35, "Sarawak"),
        Station("Kota Kinabalu", 5.98, 116.07, "Sabah"),
        Station("Sandakan", 5.84, 118.12, "Sabah"),
        Station("Sibu", 2.30, 111.83, "Sarawak"),
        Station("Miri", 4.40, 114.01, "Sarawak"),
        Station("Pontianak", -0.02, 109.34, "West Kalimantan"),
        Station("Balikpapan", -1.27, 116.83, "East Kalimantan"),
        Station("Palangkaraya", -2.21, 113.92, "Central Kalimantan"),
        Station("Banjarmasin", -3.32, 114.59, "South Kalimantan"),
        Station("Tawau", 4.24, 117.89, "Sabah"),
    ],
    fire_clusters=[
        FireCluster("Central Kalimantan peatlands", (-2.30, 114.00), 0.25, 6),
        FireCluster("West Kalimantan oil-palm frontier", (0.50, 109.50), 0.20, 5),
        FireCluster("Heart of Borneo corridor", (1.50, 115.00), 0.15, 3),
        FireCluster("Danum Valley edge", (4.96, 117.80), 0.10, 2),
        FireCluster("Kinabatangan floodplain", (5.50, 118.00), 0.12, 3),
        FireCluster("South Kalimantan plantation fires", (-3.00, 115.50), 0.20, 4),
        FireCluster("Sabah interior logging roads", (5.20, 116.50), 0.10, 3),
        FireCluster("Sarawak peat swamp", (2.00, 111.00), 0.15, 4),
    ],
    ndvi_zones=[
        NdviZone(-4.5, -1.0, 108.0, 119.5),   # South Kalimantan
        NdviZone(-1.0, 3.0, 108.0, 119.5),     # Central Borneo
        NdviZone(3.0, 7.5, 108.0, 119.5),      # North Borneo (Sabah/Sarawak)
    ],
    boundary_file="borneo.geojson",
)


EASTERN_HIMALAYA = Region(
    id="eastern_himalaya",
    name="Eastern Himalaya",
    description="Montane biodiversity hotspot spanning NE India, Nepal, and Bhutan — from subtropical jungle to alpine meadows, home to red pandas and snow leopards.",
    bbox=(85.0, 25.0, 97.5, 30.0),
    center=(27.5, 91.0),
    zoom=6,
    country_codes=["IN", "NP", "BT"],
    timezone="Asia/Kolkata",
    climate=ClimateProfile(
        lat_range=(25.5, 29.5),
        dry_months=[11, 12, 1, 2, 3],
        ndvi_mean=0.52, ndvi_std=0.12,
        ndvi_deciduous_threshold_lat=27.0,
        ndvi_wet=0.65, ndvi_dry=0.35,
        temp_mean=18.0, temp_lat_gradient=0.8,
        temp_dry_offset=-5.0, temp_wet_offset=4.0,
        precip_dry_scale=8.0, precip_wet_scale=180.0,
        humidity_dry_mean=30.0, humidity_wet_mean=75.0,
    ),
    stations=[
        Station("Darjeeling", 27.04, 88.26, "West Bengal"),
        Station("Gangtok", 27.33, 88.62, "Sikkim"),
        Station("Shillong", 25.57, 91.88, "Meghalaya"),
        Station("Itanagar", 27.10, 93.62, "Arunachal Pradesh"),
        Station("Tawang", 27.59, 91.87, "Arunachal Pradesh"),
        Station("Kathmandu", 27.72, 85.32, "Nepal"),
        Station("Pokhara", 28.21, 83.99, "Nepal"),
        Station("Thimphu", 27.47, 89.64, "Bhutan"),
        Station("Cherrapunji", 25.30, 91.70, "Meghalaya"),
        Station("Dibrugarh", 27.47, 94.91, "Assam"),
    ],
    fire_clusters=[
        FireCluster("Kaziranga NP periphery", (26.58, 93.17), 0.12, 4),
        FireCluster("North Bengal Tea Belt", (26.80, 88.40), 0.10, 3),
        FireCluster("Manas National Park", (26.70, 91.00), 0.12, 3),
        FireCluster("Namdapha NP (Arunachal)", (27.50, 96.40), 0.10, 2),
        FireCluster("Chitwan buffer zone", (27.50, 84.30), 0.15, 4),
        FireCluster("Bardia NP (Nepal)", (28.40, 81.50), 0.10, 3),
        FireCluster("Kanchenjunga foothills", (27.30, 88.10), 0.08, 2),
        FireCluster("Meghalaya jhum burning", (25.50, 91.50), 0.15, 3),
    ],
    ndvi_zones=[
        NdviZone(25.0, 26.5, 85.0, 97.5),    # Terai/foothills
        NdviZone(26.5, 28.0, 85.0, 97.5),     # Mid-hills
        NdviZone(28.0, 30.0, 85.0, 97.5),     # High mountains
    ],
    boundary_file="eastern_himalaya.geojson",
)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

REGIONS: dict[str, Region] = {
    r.id: r
    for r in [WESTERN_GHATS, AMAZON_RAINFOREST, BORNEO, EASTERN_HIMALAYA]
}

DEFAULT_REGION_ID = "western_ghats"


def get_region(region_id: str | None = None) -> Region:
    """Return a Region by id, falling back to the default."""
    if region_id is None:
        region_id = DEFAULT_REGION_ID
    region = REGIONS.get(region_id)
    if region is None:
        raise ValueError(f"Unknown region: {region_id!r}. Available: {list(REGIONS)}")
    return region


def list_regions() -> list:
    """Return all registered Region objects."""
    return list(REGIONS.values())
