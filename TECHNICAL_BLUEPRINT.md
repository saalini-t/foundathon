# AI-Powered Ecosystem & Biodiversity Monitoring Platform

## Technical Blueprint — Western Ghats, India

---

## 1. Problem Context

### Why Biodiversity Monitoring Fails Today

Biodiversity loss is accelerating globally at an unprecedented rate. The Intergovernmental Science-Policy Platform on Biodiversity and Ecosystem Services (IPBES) estimates that approximately 1 million species face extinction. Yet governments and conservation organizations consistently react too late to environmental threats. The root causes are systemic:

**Fragmented Environmental Datasets**
Environmental data exists across dozens of disconnected silos. Satellite imagery sits in space agencies (NASA, ESA, ISRO). Biodiversity records live in GBIF and museum databases. Climate data is held by meteorological departments. Forest survey data resides with state forest departments. No unified system connects these datasets to produce a coherent picture of ecosystem health. A researcher studying deforestation impact on endemic species must manually download, align, and cross-reference data from 5–10 different sources — a process that takes weeks or months.

**Lack of Integrated Ecosystem Intelligence Systems**
Current environmental monitoring tools are domain-specific. Remote sensing tools analyze satellite images. Biodiversity databases catalog species. Climate models forecast weather. None of these systems are designed to answer integrated questions like: *"How is the combination of rising temperatures, declining rainfall, and forest fragmentation affecting endemic amphibian populations in the Anamalai Hills?"* There is no ecosystem intelligence layer that synthesizes signals from multiple environmental domains into actionable threat assessments.

**Slow Manual Environmental Monitoring**
Ground-based ecological surveys are the gold standard but are extremely labor-intensive. A single biodiversity survey of a forest patch may require a team of 5–10 field researchers working for weeks. India's Forest Survey of India (FSI) publishes its State of Forest Report only every two years. By the time data is collected, analyzed, and published, environmental damage may already be irreversible.

**Lack of Predictive Analytics**
Nearly all current environmental monitoring is retrospective — it tells us what has already happened. Deforestation is detected after trees are gone. Species decline is documented after populations have collapsed. There is almost no operational capability to predict where the next deforestation hotspot will emerge, which species are at imminent risk, or where the next forest fire will ignite.

**Lack of Real-Time Environmental Alerts**
When illegal logging occurs in a remote forest patch, or when an anomalous temperature spike threatens a fragile microhabitat, there is no automated system that detects the event and alerts authorities in real time. The lag between environmental events and human awareness can be weeks to months.

### Why AI-Driven Environmental Intelligence Is the Solution

An AI-powered platform can solve these problems by:

1. **Automated data integration** — Continuously ingesting and aligning data from satellites, climate stations, biodiversity databases, and IoT sensors into a unified geospatial data model.
2. **Pattern recognition at scale** — Machine learning models can process satellite imagery across thousands of square kilometers daily, detecting deforestation, land use change, and vegetation stress that would take human analysts months to review.
3. **Predictive analytics** — Time-series models and spatial analysis can forecast where deforestation, fire risk, and biodiversity loss are likely to occur next, enabling proactive intervention.
4. **Real-time alerting** — Event-driven architectures can trigger automated alerts when anomalous environmental changes are detected, reducing response times from months to hours.
5. **Integrated ecosystem scoring** — Multi-factor AI models can synthesize biodiversity, climate, forest cover, and pollution data into a single ecosystem health score for any geographic area.

---

## 2. Western Ghats Ecosystem Context

### Geographic Extent

The Western Ghats (also known as Sahyadri) is a 1,600 km mountain chain running parallel to India's western coast, from the Tapti River in Gujarat to the southern tip of Kerala. The range covers approximately **160,000 km²** across six states: Gujarat, Maharashtra, Goa, Karnataka, Kerala, and Tamil Nadu.

- **Latitude range**: approximately 8°N to 21°N
- **Longitude range**: approximately 73°E to 78°E
- **Elevation**: ranges from 300m to 2,695m (Anamudi, the highest peak in South India)
- **Bounding box** (approximate): `[72.5°E, 8.0°N, 78.5°E, 21.5°N]`

### Biodiversity Importance

The Western Ghats is one of the world's **8 "hottest" biodiversity hotspots** (per Conservation International) and a **UNESCO World Heritage Site** (39 serial sites inscribed in 2012).

Key biodiversity statistics:
- **~7,402 species of flowering plants** — 2,253 of which (~30%) are **endemic**
- **~570 bird species** — 16 endemic
- **~330 butterfly species** — 37 endemic
- **~269 freshwater fish species** — 118 endemic (~44%)
- **~225 amphibian species** — 159 endemic (~71%), one of the highest amphibian endemism rates globally
- **~175 reptile species** — 97 endemic (~55%)
- **~137 mammal species** — 12 endemic
- Unique taxa include Lion-Tailed Macaque, Nilgiri Tahr, Malabar Giant Squirrel, Purple Frog, and hundreds of endemic orchid and tree species.

### Major Threats

| Threat | Description | Severity |
|--------|-------------|----------|
| **Deforestation** | Conversion of forest to agriculture (tea, coffee, rubber, palm oil), mining, and urbanization. ~40% of original forest cover has been lost. | Critical |
| **Habitat Fragmentation** | Linear infrastructure (roads, railways, power lines) and monoculture plantations have broken contiguous forests into isolated patches, disrupting wildlife corridors. | High |
| **Climate Change** | Shifting monsoon patterns threaten moisture-dependent ecosystems. Shola-grassland mosaics at high elevations are particularly vulnerable. Temperature increases threaten cold-adapted endemic species. | High |
| **Forest Fires** | Increasing frequency of summer fires, both natural and human-caused, especially in dry deciduous forests and grasslands of Karnataka and Tamil Nadu. | High |
| **Invasive Species** | Lantana camara, Eucalyptus monocultures, and Senna spectabilis are aggressively colonizing native habitats. | Medium |
| **Human-Wildlife Conflict** | Expanding settlements create conflict zones, particularly with elephants, leopards, and wild boar. | Medium |
| **Mining and Quarrying** | Illegal and legal extraction in ecologically sensitive zones. | Medium |

### Why Monitoring This Region Is Important

The Western Ghats supplies water to approximately **400 million people** through rivers originating in its watersheds (Krishna, Godavari, Kaveri, Tungabhadra, Periyar). Ecosystem degradation here has cascading effects on:
- **Water security** for six states
- **Agricultural productivity** across the Deccan Plateau
- **Climate regulation** — the Ghats significantly influence the Indian monsoon
- **Irreplaceable biodiversity** — species found nowhere else on Earth

The Madhav Gadgil Committee (2011) and Kasturirangan Committee (2013) both recommended comprehensive monitoring and protective zoning, but implementation has been fragmented due to lack of integrated monitoring systems.

---

## 3. Real Data Sources for the Western Ghats

### 3.1 Satellite Data

#### Sentinel-2 (ESA Copernicus Programme)

| Attribute | Details |
|-----------|---------|
| **Source** | European Space Agency (ESA) via Copernicus Open Access Hub |
| **Data** | Multispectral imagery at 10m, 20m, and 60m resolution across 13 spectral bands |
| **Revisit** | Every 5 days (with 2 satellites) |
| **Useful for** | NDVI computation, land cover classification, vegetation health assessment, deforestation detection, water body mapping |
| **Access** | Copernicus Data Space Ecosystem API: `https://dataspace.copernicus.eu/` — Free, requires registration. Also available via Google Earth Engine. |

#### Landsat 8/9 (NASA/USGS)

| Attribute | Details |
|-----------|---------|
| **Source** | USGS EarthExplorer / Google Earth Engine |
| **Data** | Multispectral + thermal imagery at 30m resolution (15m panchromatic), 11 bands |
| **Revisit** | 16 days per satellite |
| **Useful for** | Long-term change detection (Landsat archive goes back to 1972), land surface temperature, historical deforestation analysis |
| **Access** | USGS EarthExplorer: `https://earthexplorer.usgs.gov/` — Free. Also via Google Earth Engine API. |

#### Google Earth Engine (GEE)

| Attribute | Details |
|-----------|---------|
| **Source** | Google |
| **Data** | Aggregated catalog of petabytes of satellite imagery (Sentinel, Landsat, MODIS, etc.) with built-in computation infrastructure |
| **Useful for** | Cloud-based analysis without downloading massive datasets. Ideal for NDVI time-series, land cover classification, and compositing. |
| **Access** | GEE JavaScript/Python API: `https://earthengine.google.com/` — Free for research and non-commercial use. |

#### NASA EarthData

| Attribute | Details |
|-----------|---------|
| **Source** | NASA Distributed Active Archive Centers (DAACs) |
| **Data** | MODIS vegetation indices (MOD13Q1), land cover (MCD12Q1), surface reflectance, atmospheric data |
| **Useful for** | 250m–1km resolution products ideal for regional-scale monitoring, NDVI, EVI, LAI indices |
| **Access** | NASA EarthData: `https://earthdata.nasa.gov/` — Free, requires EarthData login. AppEEARS API for poi"Now carefully evaluate any risks in increasing the scope beyond western ghats to other selectable biodiverse environment. Plan first and take action nt/area extractions. |

**Environmental Signals Extractable from Satellite Data:**

| Signal | Method | Resolution | Application |
|--------|--------|------------|-------------|
| **NDVI** (Normalized Difference Vegetation Index) | (NIR - Red) / (NIR + Red) from Sentinel-2 Bands 8 & 4 | 10m | Vegetation health, greening/browning trends |
| **EVI** (Enhanced Vegetation Index) | Improvement over NDVI for dense canopy areas | 250m (MODIS) | Forest canopy condition in dense tropical forests |
| **Land Surface Temperature** | Thermal bands from Landsat 8/9 (Band 10) | 100m | Heat stress detection, urban heat island effects |
| **Forest Cover** | Supervised classification of multispectral bands | 10–30m | Baseline forest mapping, change detection |
| **Land Use / Land Cover Change** | Multi-temporal comparison | 10–30m | Detecting conversion of forest to plantation/agriculture |
| **Burn Scar Mapping** | NIR + SWIR bands (NBR index) | 10–20m | Post-fire damage assessment |

---

### 3.2 Climate and Weather Data

#### India Meteorological Department (IMD)

| Attribute | Details |
|-----------|---------|
| **Source** | Government of India — IMD |
| **Data** | Gridded rainfall (0.25° × 0.25°, daily), temperature (1° × 1°), cyclone tracks, monsoon data |
| **Useful for** | Monsoon analysis, drought detection, rainfall anomalies in Western Ghats watersheds |
| **Access** | IMD Pune data portal: `https://www.imdpune.gov.in/` — Some datasets freely downloadable, others require data request. Gridded rainfall available via India-WRIS. |

#### Meteostat (Open Weather Data)

| Attribute | Details |
|-----------|---------|
| **Source** | Meteostat (aggregated from NOAA, DWD, and national weather services) |
| **Data** | Historical and near-real-time weather data: temperature, precipitation, humidity, wind speed, pressure, from weather stations |
| **Useful for** | Station-level weather data for specific locations in the Western Ghats, gap-filling climate records |
| **Access** | Meteostat Python library: `pip install meteostat` — Free, no API key needed. JSON API also available. |

#### Open-Meteo

| Attribute | Details |
|-----------|---------|
| **Source** | Open-Meteo (open-source weather API) |
| **Data** | Forecast + historical weather: temperature, precipitation, humidity, wind, soil moisture, evapotranspiration |
| **Useful for** | High-resolution weather data without rate limits, 7-day forecast for fire risk modeling |
| **Access** | REST API: `https://open-meteo.com/` — Free for non-commercial use, no API key required. |

#### NOAA Climate Data

| Attribute | Details |
|-----------|---------|
| **Source** | National Oceanic and Atmospheric Administration (USA) |
| **Data** | Global Historical Climatology Network (GHCN): long-term station records. ERA5 reanalysis data (via ECMWF). |
| **Useful for** | Decadal climate trends, anomaly detection, long-term baseline comparisons |
| **Access** | NOAA NCEI: `https://www.ncei.noaa.gov/` — Free. ERA5 via Copernicus Climate Data Store (CDS API). |

#### WorldClim

| Attribute | Details |
|-----------|---------|
| **Source** | WorldClim.org |
| **Data** | Bioclimatic variables (19 variables), monthly climate data at ~1km resolution, future climate projections (CMIP6) |
| **Useful for** | Species distribution modeling, climate envelope analysis, baseline climate characterization |
| **Access** | Direct download: `https://www.worldclim.org/` — Free. GeoTIFF format. |

**Available Climate Parameters:**

| Parameter | Sources | Use Case |
|-----------|---------|----------|
| Temperature (min/max/mean) | IMD, Meteostat, Open-Meteo, NOAA | Heat stress, fire risk, species habitat modeling |
| Rainfall (daily/monthly) | IMD, Open-Meteo, NOAA, WorldClim | Drought detection, monsoon monitoring, watershed health |
| Humidity | Meteostat, Open-Meteo | Fire danger index computation, evapotranspiration |
| Wind speed/direction | Meteostat, Open-Meteo | Fire spread modeling, pollutant dispersion |
| Climate anomalies | NOAA, ERA5 | Detecting deviation from historical baselines |

---

### 3.3 Biodiversity Data

#### GBIF (Global Biodiversity Information Facility)

| Attribute | Details |
|-----------|---------|
| **Source** | GBIF.org — international biodiversity data network |
| **Data** | ~2.4 billion occurrence records globally. For Western Ghats: millions of georeferenced species occurrence records including mammals, birds, amphibians, reptiles, plants, insects. |
| **Useful for** | Species distribution mapping, hotspot identification, temporal trends in species observations, invasive species tracking |
| **Access** | REST API: `https://www.gbif.org/developer/summary` — Free, requires registration. Python: `pygbif` library. Query by bounding box for Western Ghats: `decimalLatitude=8,21.5&decimalLongitude=72.5,78.5` |

#### India Biodiversity Portal (IBP)

| Attribute | Details |
|-----------|---------|
| **Source** | Strand Life Sciences / Government of India |
| **Data** | India-specific species observations, citizen science records, checklists, taxonomic information |
| **Useful for** | India-specific endemic species data, crowdsourced sightings supplementing GBIF |
| **Access** | `https://indiabiodiversity.org/` — Browse and export. Some API functionality available. |

#### IUCN Red List

| Attribute | Details |
|-----------|---------|
| **Source** | International Union for Conservation of Nature |
| **Data** | Conservation status (CR, EN, VU, NT, LC), range maps, population trends, threats for assessed species |
| **Useful for** | Prioritizing monitoring based on threat level, mapping critically endangered species habitats in Western Ghats |
| **Access** | IUCN Red List API: `https://apiv3.iucnredlist.org/` — Free API key required. Python: `pip install iucn_modlib` or direct REST calls. |

#### Western Ghats Biodiversity Information System (WGBIS)

| Attribute | Details |
|-----------|---------|
| **Source** | Indian Institute of Science / CES |
| **Data** | Spatial biodiversity data specific to Western Ghats, landscape-level datasets, connectivity maps |
| **Useful for** | Region-specific ecological data, landscape connectivity analysis |
| **Access** | `http://wgbis.ces.iisc.ernet.in/` — Downloadable datasets. |

**How Species Occurrence Data Analyzes Ecosystem Health:**
- **Species richness mapping**: Count distinct species per grid cell to identify biodiversity hotspots and coldspots.
- **Temporal trends**: Declining observation frequency of indicator species signals ecosystem degradation.
- **Range shift detection**: Species appearing outside historical ranges may indicate climate-driven migration.
- **Community composition analysis**: Shifts in species assemblages (e.g., generalists replacing specialists) indicate habitat degradation.
- **Invasive species mapping**: Tracking spread of invasive species like Lantana camara.

---

### 3.4 Forest and Deforestation Data

#### Global Forest Watch (GFW)

| Attribute | Details |
|-----------|---------|
| **Source** | World Resources Institute |
| **Data** | Annual tree cover loss (Hansen et al., 30m resolution, 2000–present), near-real-time deforestation alerts (GLAD alerts), tree cover density, primary forest extent |
| **Useful for** | Annual deforestation tracking, identifying deforestation frontlines, validating model predictions |
| **Access** | GFW API: `https://www.globalforestwatch.org/` — Free. Data downloads available. GFW API v2 for programmatic access. Also accessible via Google Earth Engine (Hansen Global Forest Change dataset). |

#### MODIS Vegetation Products

| Attribute | Details |
|-----------|---------|
| **Source** | NASA LP DAAC |
| **Data** | MOD13Q1 (16-day NDVI/EVI at 250m), MOD44B (vegetation continuous fields), MCD12Q1 (annual land cover at 500m) |
| **Useful for** | Regional-scale vegetation trend analysis, land cover classification baseline |
| **Access** | NASA EarthData AppEEARS: `https://appeears.earthdatacloud.nasa.gov/` — Free. Also via GEE. |

#### Forest Survey of India (FSI)

| Attribute | Details |
|-----------|---------|
| **Source** | Ministry of Environment, Forest and Climate Change, India |
| **Data** | India State of Forest Report (biennial), district-level forest cover statistics, forest type maps |
| **Useful for** | Official baseline forest cover data for Indian administrative units, validation against satellite-derived estimates |
| **Access** | `https://fsi.nic.in/` — Reports downloadable as PDF. Some geospatial data available. |

**How These Datasets Detect Deforestation:**
- **GLAD alerts** (Global Land Analysis & Discovery) provide near-real-time alerts (~weekly) for likely tree cover loss events at 30m resolution. These can trigger automated responses.
- **Hansen tree cover loss** provides validated annual maps of where tree cover was lost, enabling year-over-year comparison.
- **NDVI time-series from MODIS/Sentinel** — a sudden drop in NDVI in a forested area signals canopy removal. Persistent NDVI decline over multiple timesteps confirms land use change rather than seasonal variation.

---

### 3.5 Fire and Disaster Data

#### NASA FIRMS (Fire Information for Resource Management System)

| Attribute | Details |
|-----------|---------|
| **Source** | NASA LANCE (Land, Atmosphere Near Real-Time Capability for EOS) |
| **Data** | Active fire detections from MODIS (1km) and VIIRS (375m), updated every ~3 hours. Attributes: latitude, longitude, brightness temperature, fire radiative power, confidence, acquisition time. |
| **Useful for** | Near-real-time fire detection and alerting, fire frequency analysis, fire season characterization |
| **Access** | FIRMS API: `https://firms.modaps.eosdis.nasa.gov/api/` — Free, requires API key (MAP_KEY). CSV/JSON/GeoJSON download. REST endpoint: `https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/VIIRS_SNPP_NRT/{bounding_box}/{days}` |

#### MODIS Burned Area Product (MCD64A1)

| Attribute | Details |
|-----------|---------|
| **Source** | NASA LP DAAC |
| **Data** | Monthly burn scar mapping at 500m resolution, with burn date and confidence |
| **Useful for** | Historical fire extent analysis, post-fire recovery tracking |
| **Access** | NASA EarthData / GEE — Free. |

**Integrating Near-Real-Time Fire Alerts:**
- The FIRMS API delivers new fire detections within 3 hours of satellite overpass.
- A scheduled job (e.g., every 3 hours) queries the FIRMS API for the Western Ghats bounding box.
- Detections are filtered by confidence level (≥ 70% recommended) and cross-referenced with forest cover maps.
- Fires within forested or ecologically sensitive areas trigger high-priority alerts.
- Historical FIRMS data (2000–present) provides training data for fire risk prediction models.

---

### 3.6 Environmental Sensor Data (IoT / Ground Stations)

#### OpenAQ (Air Quality)

| Attribute | Details |
|-----------|---------|
| **Source** | OpenAQ Foundation — global open air quality platform |
| **Data** | Real-time and historical air quality measurements: PM2.5, PM10, NO₂, SO₂, O₃, CO from government and research-grade monitors |
| **Useful for** | Air quality monitoring near Western Ghats cities (Pune, Mangalore, Kochi), smoke detection from fires, industrial pollution tracking |
| **Access** | OpenAQ API v2: `https://api.openaq.org/v2/` — Free, no key required. Python: `pip install openaq`. Filter by country=IN and coordinates. |

#### AQICN (World Air Quality Index)

| Attribute | Details |
|-----------|---------|
| **Source** | AQICN.org |
| **Data** | Real-time AQI from monitoring stations globally |
| **Useful for** | Supplementary air quality data, particularly for cities along the Western Ghats corridor |
| **Access** | API: `https://aqicn.org/api/` — Free with API token. |

#### Meteostat Weather Stations

| Attribute | Details |
|-----------|---------|
| **Source** | Meteostat (aggregated from national services) |
| **Data** | Station-level observations: temperature, dew point, humidity, precipitation, wind, pressure, visibility |
| **Useful for** | Ground-truth validation of satellite and reanalysis climate data, microclimate characterization |
| **Access** | Meteostat Python library or JSON API — Free. Stations near Western Ghats can be queried by lat/lon. |

**Environmental Measurements from Ground Sensors:**

| Measurement | Sources | Ecological Relevance |
|-------------|---------|---------------------|
| Air Quality (PM2.5, PM10) | OpenAQ, AQICN | Fire smoke detection, industrial impact on forests |
| Temperature | Meteostat, IMD, Open-Meteo | Microhabitat suitability, heat stress |
| Humidity | Meteostat, Open-Meteo | Fire danger assessment, amphibian habitat suitability |
| Atmospheric Pressure | Meteostat | Weather pattern detection, storm prediction |
| Rainfall (gauge) | IMD, Meteostat | Ground truth for satellite precipitation estimates |

---

## 4. Data Integration Strategy

### Challenge: Heterogeneous Data Fusion

The datasets listed above differ in:
- **Spatial resolution**: from 10m (Sentinel-2) to 0.25° (~25km) grids (IMD rainfall)
- **Temporal resolution**: from near-real-time (FIRMS, OpenAQ) to annual (Hansen forest loss)
- **Data format**: GeoTIFF rasters, CSV/JSON point data, shapefiles, API responses
- **Coordinate reference systems**: WGS84, UTM zones, custom projections
- **Data quality**: from highly validated (Landsat) to noisy (citizen science observations)

### Integration Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     DATA INGESTION LAYER                        │
├──────────┬──────────┬──────────┬──────────┬─────────────────────┤
│ Satellite│ Climate  │Biodiversi│  Fire    │ Environmental       │
│ Imagery  │ Weather  │  ty Data │ Alerts   │  Sensors            │
│ (GEE,    │ (IMD,    │ (GBIF,   │ (FIRMS)  │ (OpenAQ,            │
│  USGS)   │ Open-    │  IUCN)   │          │  Meteostat)         │
│          │  Meteo)  │          │          │                     │
└────┬─────┴────┬─────┴────┬─────┴────┬─────┴──────────┬──────────┘
     │          │          │          │                │
     ▼          ▼          ▼          ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│              DATA PROCESSING & ALIGNMENT LAYER                  │
│                                                                 │
│  ┌────────────┐ ┌──────────────┐ ┌──────────────────────────┐  │
│  │ Reproject  │ │ Resample to  │ │ Normalize to             │  │
│  │ to EPSG:   │ │ common grid  │ │ common time              │  │
│  │ 4326       │ │ (1km × 1km)  │ │ intervals                │  │
│  └────────────┘ └──────────────┘ └──────────────────────────┘  │
│                                                                 │
│  ┌────────────┐ ┌──────────────┐ ┌──────────────────────────┐  │
│  │ Cloud mask │ │ Outlier      │ │ Feature                  │  │
│  │ & QA       │ │ removal &    │ │ extraction               │  │
│  │ filtering  │ │ gap filling  │ │ & indexing               │  │
│  └────────────┘ └──────────────┘ └──────────────────────────┘  │
│                                                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                 UNIFIED GEOSPATIAL DATA STORE                   │
│                                                                 │
│  PostgreSQL + PostGIS   │   GeoParquet files   │  Cloud Storage │
│  (vector data, points,  │   (raster summaries  │  (raw satellite│
│   polygons, queries)    │    per grid cell)    │   imagery)     │
│                                                                 │
│  Unified grid: 1km × 1km hexagonal or square cells             │
│  covering Western Ghats bounding box                            │
│  (~160,000 cells at 1km resolution)                             │
└─────────────────────────────────────────────────────────────────┘
```

### Step-by-Step Integration Process

#### 4.1 Data Ingestion Pipelines

| Data Source | Ingestion Method | Frequency | Format |
|-------------|-----------------|-----------|--------|
| Sentinel-2 | GEE Python API → cloud-optimized GeoTIFF | Weekly | Raster |
| Landsat | GEE Python API or USGS M2M API | Bi-weekly | Raster |
| MODIS NDVI | GEE or AppEEARS API | 16-day | Raster |
| IMD Climate | Bulk download + Python parsing | Daily | Gridded NetCDF/CSV |
| Open-Meteo | REST API | Daily/hourly | JSON |
| GBIF | pygbif Python library or REST API | Weekly | JSON/CSV |
| IUCN Red List | REST API | Monthly | JSON |
| FIRMS Fire | REST API (scheduled every 3 hours) | Near-real-time | CSV/JSON |
| Global Forest Watch | GFW API / GEE (Hansen dataset) | Annual + GLAD alerts weekly | Raster/JSON |
| OpenAQ | REST API | Hourly | JSON |
| Meteostat | Python library | Daily | DataFrame |

```python
# Example: FIRMS fire data ingestion
import requests
import geopandas as gpd

FIRMS_API_KEY = "your_map_key"
WESTERN_GHATS_BBOX = "72.5,8.0,78.5,21.5"  # W,S,E,N

def fetch_fire_alerts(days=1):
    url = (
        f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
        f"{FIRMS_API_KEY}/VIIRS_SNPP_NRT/{WESTERN_GHATS_BBOX}/{days}"
    )
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    # Parse CSV response into GeoDataFrame
    from io import StringIO
    import pandas as pd
    df = pd.read_csv(StringIO(response.text))
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df.longitude, df.latitude),
        crs="EPSG:4326"
    )
    return gdf
```

#### 4.2 API Connectors

Build a modular connector architecture:

```python
# connector_base.py
from abc import ABC, abstractmethod
import geopandas as gpd

class DataConnector(ABC):
    """Base class for all data source connectors."""

    @abstractmethod
    def fetch(self, bbox: tuple, start_date: str, end_date: str) -> gpd.GeoDataFrame:
        """Fetch data for given bounding box and date range."""
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        pass

# Implement connectors:
# - SentinelConnector (via GEE)
# - FIRMSConnector (NASA REST API)
# - GBIFConnector (pygbif)
# - OpenMeteoConnector (REST API)
# - OpenAQConnector (REST API)
# - GlobalForestWatchConnector (GFW API)
```

#### 4.3 Satellite Image Preprocessing

```
Raw Sentinel-2 Scene
        │
        ▼
┌─────────────────────┐
│ Cloud Masking        │ ← Use SCL band (Scene Classification Layer)
│ (remove cloudy       │   or s2cloudless algorithm
│  pixels)             │
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ Atmospheric          │ ← Use Level-2A (bottom-of-atmosphere reflectance)
│ Correction           │   Already done for Sentinel-2 L2A products
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ Index Computation    │ ← NDVI, EVI, NBR, NDWI, BSI
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ Temporal Compositing │ ← Monthly median composite to fill cloud gaps
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ Zonal Statistics     │ ← Aggregate raster values to grid cells
│ (per 1km grid cell)  │   (mean, std, min, max NDVI per cell)
└─────────────────────┘
```

```python
# GEE-based NDVI computation for Western Ghats
import ee
ee.Initialize()

western_ghats = ee.Geometry.Rectangle([72.5, 8.0, 78.5, 21.5])

def compute_monthly_ndvi(year, month):
    start = ee.Date.fromYMD(year, month, 1)
    end = start.advance(1, 'month')

    s2 = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
          .filterBounds(western_ghats)
          .filterDate(start, end)
          .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30)))

    def add_ndvi(image):
        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
        return image.addBands(ndvi)

    ndvi_composite = s2.map(add_ndvi).select('NDVI').median()
    return ndvi_composite.clip(western_ghats)
```

#### 4.4 Geospatial Alignment

All datasets are aligned to a **common reference grid** covering the Western Ghats:

- **CRS**: EPSG:4326 (WGS84) for storage; project to UTM Zone 43N (EPSG:32643) for area calculations
- **Grid**: 1km × 1km square grid (~160,000 cells) or H3 hexagonal grid (resolution 7, ~5.16 km² per hexagon)
- **Process**:
  - Raster data → zonal statistics per grid cell (mean, min, max, std)
  - Point data (species occurrences, fire detections, weather stations) → spatial join to grid cells
  - Polygon data (protected areas, administrative boundaries) → overlay intersection with grid

```python
import geopandas as gpd
import numpy as np
from shapely.geometry import box

def create_grid(bbox, cell_size_deg=0.01):
    """Create a 1km (~0.01°) grid over the Western Ghats."""
    xmin, ymin, xmax, ymax = bbox
    xs = np.arange(xmin, xmax, cell_size_deg)
    ys = np.arange(ymin, ymax, cell_size_deg)
    cells = []
    for x in xs:
        for y in ys:
            cells.append(box(x, y, x + cell_size_deg, y + cell_size_deg))
    grid = gpd.GeoDataFrame(geometry=cells, crs="EPSG:4326")
    grid['cell_id'] = range(len(grid))
    return grid

# Create grid
wg_grid = create_grid((72.5, 8.0, 78.5, 21.5))
```

#### 4.5 Data Cleaning and Normalization

| Issue | Solution |
|-------|----------|
| Missing satellite data (clouds) | Temporal compositing (monthly median), gap-filling interpolation |
| Inconsistent coordinate systems | Reproject all data to EPSG:4326 using GeoPandas/rasterio |
| Different temporal granularities | Resample all to common period (e.g., monthly for analysis, daily for alerts) |
| Noisy biodiversity records | Filter GBIF by coordinate uncertainty (<1km), remove flagged records |
| Scale differences | Min-max normalization or z-score standardization per variable before model input |
| Outliers in sensor data | IQR-based outlier removal, replace with interpolated values |

---

## 5. AI and Machine Learning Models

### 5.1 Deforestation Detection (Computer Vision)

**Objective:** Detect areas where forest cover has been recently removed or degraded using satellite imagery.

| Attribute | Details |
|-----------|---------|
| **Model Architecture** | U-Net (semantic segmentation) or ResNet-50 with Feature Pyramid Network (FPN) |
| **Input Features** | Sentinel-2 multi-band images (B2, B3, B4, B8, B11, B12) — 6-channel input. Bi-temporal pairs (before/after) for change detection. |
| **Training Data** | Hansen Global Forest Change (tree cover loss year) as labels. Sentinel-2 corresponding imagery as input. For Western Ghats: ~20 years of validated labels available. |
| **Output** | Binary segmentation mask: deforested (1) vs. intact (0) per pixel at 10m resolution. Probability map for change confidence. |
| **Approach** | **Option A (Transfer Learning):** Fine-tune a pretrained model from the DeepGlobe or SpaceNet dataset on Western Ghats-specific imagery. **Option B (Change Detection):** Feed bi-temporal image pairs into a Siamese U-Net to detect changes. |
| **Hackathon Simplification** | Use a Random Forest classifier on per-pixel NDVI change instead of deep learning. Threshold-based: NDVI drop > 0.3 over 3 months flags potential deforestation. |

```python
# Simplified deforestation detection
import numpy as np

def detect_deforestation(ndvi_before, ndvi_after, threshold=-0.3):
    """
    Detect deforestation from NDVI change.
    Args:
        ndvi_before: NDVI array for earlier period
        ndvi_after: NDVI array for later period
        threshold: NDVI change threshold (negative = vegetation loss)
    Returns:
        Binary mask of deforested pixels
    """
    ndvi_change = ndvi_after - ndvi_before
    deforested = (ndvi_change < threshold) & (ndvi_before > 0.4)  # Was forested
    return deforested.astype(np.uint8)
```

### 5.2 Wildfire Risk Prediction (Time-Series Model)

**Objective:** Predict the probability of wildfire occurrence in each grid cell for the coming 1–7 days.

| Attribute | Details |
|-----------|---------|
| **Model Architecture** | Gradient Boosted Trees (XGBoost/LightGBM) for tabular features, or LSTM for temporal sequences |
| **Input Features** | Per grid cell: NDVI (vegetation dryness), temperature (max, mean), humidity, rainfall (last 7/14/30 days), wind speed, days since last rain, historical fire frequency, elevation, slope, distance to roads, land cover type |
| **Training Data** | FIRMS historical fire detections (2001–present) as positive labels. Sample non-fire grid cells at same timestamps as negatives. |
| **Output** | Fire risk probability (0–1) per grid cell. Classification into risk levels: Low / Moderate / High / Extreme. |
| **Evaluation Metrics** | AUC-ROC, Precision-Recall (important due to class imbalance — fires are rare events) |

```python
# Fire risk feature engineering
def compute_fire_risk_features(grid_cell_id, date):
    return {
        'ndvi_current': ...,           # Current vegetation greenness
        'ndvi_anomaly': ...,           # Deviation from long-term mean
        'temp_max_7d': ...,            # Max temperature last 7 days
        'rainfall_30d': ...,           # Cumulative rainfall last 30 days
        'days_since_rain': ...,        # Days since last rainfall > 1mm
        'humidity_min_7d': ...,        # Minimum humidity last 7 days
        'wind_max_3d': ...,            # Maximum wind speed last 3 days
        'elevation': ...,              # Meters above sea level
        'slope': ...,                  # Terrain slope in degrees
        'land_cover': ...,             # Forest type (deciduous/evergreen/grassland)
        'dist_to_road': ...,           # Distance to nearest road (km)
        'fire_history_count': ...,     # Historical fire count in this cell
        'month': date.month,           # Seasonality
    }
```

### 5.3 Ecosystem Health Scoring (Multi-Factor Ecological Index)

**Objective:** Compute a composite Ecosystem Health Index (EHI) for each grid cell ranging from 0 (critically degraded) to 100 (pristine).

| Attribute | Details |
|-----------|---------|
| **Model Architecture** | Weighted composite index with optional ML-based weight optimization |
| **Input Components** | 6 sub-indices (each normalized 0–100): |

**Sub-Index Components:**

| Sub-Index | Weight | Source Data | Computation |
|-----------|--------|-------------|-------------|
| Vegetation Health (VH) | 0.25 | Sentinel-2 NDVI | Current NDVI percentile vs. historical range |
| Forest Integrity (FI) | 0.20 | Hansen forest cover, GFW tree loss | % intact forest cover × (1 - recent loss rate) |
| Biodiversity Richness (BR) | 0.20 | GBIF species occurrences, IUCN status | Weighted species count (endangered species weighted higher) |
| Climate Stability (CS) | 0.15 | IMD/Open-Meteo climate data | Inverse of temperature and rainfall anomalies |
| Air Quality (AQ) | 0.10 | OpenAQ | Inverse of PM2.5 concentration |
| Fire Disturbance (FD) | 0.10 | FIRMS | Inverse of recent fire frequency and burnt area |

```python
def compute_ecosystem_health_index(cell_data):
    """Compute EHI for a grid cell."""
    vh = normalize(cell_data['ndvi'], min_val=0, max_val=0.9) * 100
    fi = (cell_data['forest_cover_pct'] *
          (1 - cell_data['recent_loss_rate'])) * 100
    br = compute_biodiversity_score(
        cell_data['species_count'],
        cell_data['endangered_count']
    )
    cs = 100 - normalize(
        abs(cell_data['temp_anomaly']) + abs(cell_data['rainfall_anomaly']),
        min_val=0, max_val=5
    ) * 100
    aq = 100 - normalize(cell_data['pm25'], min_val=0, max_val=200) * 100
    fd = 100 - normalize(cell_data['fire_count_1yr'], min_val=0, max_val=10) * 100

    ehi = (0.25 * vh + 0.20 * fi + 0.20 * br +
           0.15 * cs + 0.10 * aq + 0.10 * fd)

    return round(max(0, min(100, ehi)), 1)
```

**Output:** Per-cell EHI (0–100) visualized as a choropleth map. Temporal trends show improving or degrading areas.

### 5.4 Anomaly Detection (Ecosystem Change Detection)

**Objective:** Detect unusual or unexpected changes in ecosystem variables that may indicate emerging threats.

| Attribute | Details |
|-----------|---------|
| **Model Architecture** | Isolation Forest or Autoencoder for multivariate anomaly detection |
| **Input Features** | Per grid cell time series: NDVI, temperature, rainfall, species observation rate, fire frequency — deviations from seasonal norms |
| **Training Data** | Historical normal conditions (e.g., 2015–2024 baseline) to learn expected ranges |
| **Output** | Anomaly score per cell per time step. Cells exceeding threshold trigger investigation alerts. |

**Types of Anomalies Detected:**

| Anomaly Type | Signal | Potential Cause |
|--------------|--------|-----------------|
| Sudden NDVI drop in non-fire area | Vegetation index plummets | Illegal logging, disease, landslide |
| Temperature spike + low humidity | Climate extremes | Drought onset, increased fire risk |
| Species observation rate drop | Declining sightings | Habitat degradation, migration |
| Unusual fire in evergreen forest | Fire in wet zone | Anthropogenic fire, extreme drought |
| NDVI increase in grassland | Greening where grass expected | Invasive species encroachment |

```python
from sklearn.ensemble import IsolationForest

def train_anomaly_detector(historical_features_df):
    """Train anomaly detector on historical normal conditions."""
    model = IsolationForest(
        n_estimators=200,
        contamination=0.05,  # Expect ~5% anomalies
        random_state=42
    )
    model.fit(historical_features_df)
    return model

def detect_anomalies(model, current_features_df):
    """Score current conditions. -1 = anomaly, 1 = normal."""
    predictions = model.predict(current_features_df)
    scores = model.decision_function(current_features_df)
    return predictions, scores
```

---

## 6. System Architecture

### Complete Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          FRONTEND DASHBOARD                             │
│                                                                         │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐  │
│  │   Interactive     │  │   EHI Gauges &   │  │   Alert Feed &       │  │
│  │   Map (Mapbox/    │  │   Trend Charts   │  │   Notifications      │  │
│  │   Leaflet)        │  │   (Chart.js/     │  │                      │  │
│  │                   │  │   Recharts)      │  │   Fire alerts        │  │
│  │  ● Choropleth EHI │  │                  │  │   Deforestation      │  │
│  │  ● Fire markers   │  │  ● Per-region    │  │   Anomaly warnings   │  │
│  │  ● Species dots   │  │  ● Time series   │  │                      │  │
│  │  ● Deforestation  │  │  ● Sub-indices   │  │                      │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────────┘  │
│                                                                         │
│  React + TypeScript │ Mapbox GL JS / Leaflet │ TailwindCSS             │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │ HTTPS / WebSocket
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          BACKEND API LAYER                              │
│                                                                         │
│  Python FastAPI                                                         │
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │ /api/map     │  │ /api/alerts  │  │ /api/predict │  │ /api/data  │ │
│  │              │  │              │  │              │  │            │ │
│  │ GET grid     │  │ GET fire     │  │ POST fire    │  │ GET NDVI   │ │
│  │ cells with   │  │ alerts       │  │ risk         │  │ time       │ │
│  │ EHI scores   │  │ GET anomaly  │  │ POST defor-  │  │ series     │ │
│  │ GET species  │  │ alerts       │  │ estation     │  │ GET species│ │
│  │ for region   │  │              │  │ detection    │  │ list       │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └─────┬──────┘ │
│         │                 │                  │                │        │
│  ┌──────┴─────────────────┴──────────────────┴────────────────┴──────┐ │
│  │                    SERVICE LAYER                                   │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌────────────┐  │ │
│  │  │ Map Service │ │ Alert       │ │ Prediction  │ │ Data       │  │ │
│  │  │             │ │ Service     │ │ Service     │ │ Service    │  │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └────────────┘  │ │
│  └───────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
│  AI MODEL LAYER  │ │  DATABASE    │ │ EVENT PROCESSING │
│                  │ │              │ │                  │
│ ┌──────────────┐ │ │ PostgreSQL + │ │ Scheduled Jobs   │
│ │ Deforestation│ │ │ PostGIS      │ │ (APScheduler /   │
│ │ Detector     │ │ │              │ │  Celery)         │
│ ├──────────────┤ │ │ ┌──────────┐ │ │                  │
│ │ Fire Risk    │ │ │ │ Grid     │ │ │ ● FIRMS poll     │
│ │ Predictor    │ │ │ │ cells    │ │ │   (every 3 hrs)  │
│ ├──────────────┤ │ │ │ Species  │ │ │ ● NDVI update    │
│ │ EHI Scorer   │ │ │ │ Alerts   │ │ │   (weekly)       │
│ ├──────────────┤ │ │ │ Time     │ │ │ ● Weather sync   │
│ │ Anomaly      │ │ │ │ series   │ │ │   (daily)        │
│ │ Detector     │ │ │ └──────────┘ │ │ ● Anomaly scan   │
│ └──────────────┘ │ │              │ │   (daily)        │
│                  │ │ Cloud Storage│ │                  │
│ Models served    │ │ (S3/GCS for  │ └──────────────────┘
│ via FastAPI or   │ │  imagery)    │
│ MLflow           │ │              │
└──────────────────┘ └──────────────┘

                               ▲
                               │
┌──────────────────────────────┴──────────────────────────────────────────┐
│                       DATA INGESTION LAYER                              │
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐  ┌──────────────┐  │
│  │ Satellite    │  │ Climate      │  │ Biodiver- │  │ Fire &       │  │
│  │ (GEE API)    │  │ (Open-Meteo, │  │ sity      │  │ Sensor       │  │
│  │              │  │  IMD)        │  │ (GBIF,    │  │ (FIRMS,      │  │
│  │ Sentinel-2   │  │              │  │  IUCN)    │  │  OpenAQ)     │  │
│  │ Landsat      │  │ Meteostat    │  │           │  │              │  │
│  │ MODIS        │  │ NOAA         │  │ IBP       │  │ AQICN        │  │
│  └──────────────┘  └──────────────┘  └───────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

### Component Details

#### 6.1 Data Ingestion Layer

| Component | Technology | Function |
|-----------|-----------|----------|
| Satellite Connector | Google Earth Engine Python API | Fetch Sentinel-2, Landsat, MODIS imagery; compute NDVI; export results |
| Climate Connector | `requests` + `meteostat` Python lib + Open-Meteo REST API | Fetch temperature, rainfall, humidity, wind for Western Ghats stations/grid points |
| Biodiversity Connector | `pygbif` + IUCN REST API | Fetch species occurrence records, conservation status |
| Fire Connector | NASA FIRMS REST API | Fetch near-real-time active fire detections |
| Air Quality Connector | OpenAQ REST API | Fetch PM2.5, PM10 from stations near Western Ghats |
| Scheduler | APScheduler (Python) or Celery + Redis | Orchestrate periodic data fetches |

#### 6.2 Data Processing Layer

| Component | Technology | Function |
|-----------|-----------|----------|
| Geospatial Processing | GeoPandas, Rasterio, Shapely | Vector/raster operations, spatial joins, zonal statistics |
| Satellite Preprocessing | Google Earth Engine (server-side) or Rasterio (local) | Cloud masking, index computation, compositing |
| Data Normalization | Pandas, NumPy, Scikit-learn | Scaling, outlier removal, temporal alignment |
| Feature Extraction | Custom Python pipelines | Compute derived features for ML models |

#### 6.3 AI Model Layer

| Model | Framework | Serving |
|-------|-----------|---------|
| Deforestation Detection | Scikit-learn (RF) or PyTorch (U-Net) | FastAPI endpoint |
| Fire Risk Prediction | XGBoost / LightGBM | FastAPI endpoint |
| Ecosystem Health Index | NumPy weighted computation | FastAPI endpoint |
| Anomaly Detection | Scikit-learn Isolation Forest | FastAPI endpoint |

#### 6.4 Backend Infrastructure

| Component | Technology | Details |
|-----------|-----------|---------|
| API Framework | Python FastAPI | Async REST API, auto-generated OpenAPI docs |
| Authentication | API key-based (hackathon) or JWT | Protect endpoints |
| Task Queue | Celery + Redis (or APScheduler for simplicity) | Background data processing and model inference |
| Caching | Redis | Cache frequently requested map data |

#### 6.5 Frontend Dashboard

| Component | Technology | Details |
|-----------|-----------|---------|
| Framework | React + TypeScript | SPA with component architecture |
| Map Engine | Mapbox GL JS or Leaflet + React-Leaflet | Interactive map with choropleth layers, markers, popups |
| Charts | Recharts or Chart.js | EHI trends, NDVI time series, fire frequency |
| Styling | TailwindCSS | Rapid responsive UI development |
| State Management | React Query (TanStack Query) | Server state caching and synchronization |

**Dashboard Layout:**

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: AI Ecosystem Monitor — Western Ghats                   │
│  [Dashboard] [Alerts] [Analysis] [Reports]                      │
├─────────────────────────────────────────────┬───────────────────┤
│                                             │  SIDEBAR           │
│         INTERACTIVE MAP                     │                   │
│                                             │  EHI Score: 67/100│
│    ┌────────────────────────────┐           │  ▉▉▉▉▉▉▉░░░      │
│    │                            │           │                   │
│    │    Western Ghats           │           │  Vegetation: 72   │
│    │    Choropleth Map          │           │  Forest: 61       │
│    │                            │           │  Biodiversity: 68 │
│    │    [EHI] [Fire] [NDVI]     │           │  Climate: 74      │
│    │    [Species] [Deforest]    │           │  Air Quality: 55  │
│    │                            │           │  Fire Risk: LOW   │
│    └────────────────────────────┘           │                   │
│                                             │  ─── ALERTS ───   │
│  LAYER CONTROLS:                            │  🔴 Fire detected │
│  ☑ Ecosystem Health  ☑ Fire Alerts          │     Wayanad       │
│  ☑ Species Hotspots  ☑ Deforestation        │  🟡 NDVI anomaly  │
│  ☐ Climate Anomalies ☐ Air Quality          │     Kodagu        │
├─────────────────────────────────────────────┴───────────────────┤
│  TREND PANEL:  [NDVI Trend] [Temperature] [Rainfall] [EHI]     │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  📈  Line chart: Monthly NDVI for selected region       │    │
│  │      2024 ━━━━   2025 ━━━━   2026 ━━━━                 │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

#### 6.6 Cloud Infrastructure

| Component | Option A (AWS) | Option B (GCP) | Hackathon (Free) |
|-----------|---------------|----------------|-------------------|
| Compute | EC2 / Lambda | Cloud Run / GCE | Local machine / Railway.app |
| Database | RDS PostgreSQL | Cloud SQL | Local PostgreSQL or SQLite + SpatiaLite |
| Object Storage | S3 | Cloud Storage | Local filesystem |
| Model Serving | SageMaker | Vertex AI | FastAPI on same server |
| Satellite Processing | — | Google Earth Engine | Google Earth Engine (free) |
| Container | ECS / EKS | Cloud Run | Docker Compose |

---

## 7. Example User Workflow

### Persona 1: Environmental Researcher

Dr. Priya Nair, a conservation ecologist at the Ashoka Trust for Research in Ecology and the Environment (ATREE) in Bangalore, studies amphibian populations in the Anamalai Hills.

1. She opens the platform and navigates to the **Anamalai Hills** region on the interactive map.
2. The map shows the **Ecosystem Health Index** choropleth — she notices a cluster of grid cells in orange (EHI 40–55) where surrounding cells are green (EHI 70+).
3. She clicks on the degraded cluster. The **sidebar** shows:
   - Vegetation Health sub-index dropped from 78 to 42 over the last 6 months
   - NDVI trend chart shows a sharp decline starting 4 months ago
   - No fire alerts were recorded in this area
   - Forest Integrity sub-index unchanged (no Hansen tree loss detected)
4. She switches to the **Species layer** — GBIF records show that Purple Frog (*Nasikabatrachus sahyadrensis*) was historically observed in this area but has had zero observations in 18 months.
5. She checks the **Climate panel** — rainfall anomaly shows this area received 40% below average rainfall in the last monsoon season.
6. **Insight**: The combination of drought stress (visible in NDVI decline) without deforestation suggests climate-driven vegetation degradation, potentially threatening endemic amphibian habitat.
7. She **exports a report** with maps, charts, and data to support a research publication and conservation funding proposal.

### Persona 2: Government Policymaker

Mr. Rajesh Kumar, a Deputy Conservator of Forests in Karnataka's Western Ghats division.

1. At 6:00 AM, his phone receives a **push notification**: *"High-confidence fire detected in Kudremukh National Park — 2 active hotspots detected at 02:30 AM IST."*
2. He opens the platform dashboard. The map shows two **red fire markers** inside the national park boundary with VIIRS satellite detection confidence of 87% and 92%.
3. The system cross-references with **weather data** — temperature 38°C, humidity 22%, wind 15 km/h from WSW — and displays a **Fire Spread Risk: HIGH** alert.
4. The **AI fire risk model** highlights adjacent grid cells with elevated risk scores, showing the predicted spread direction based on wind, slope, and vegetation type.
5. He dispatches a ground team to the coordinates and coordinates with the forest department's fire response unit.
6. **Impact**: Response time reduced from 2–3 days (when ground patrol would have discovered the fire) to **4 hours**.

### Persona 3: Conservation Organization

The Western Ghats Conservation Alliance uses the platform to track deforestation trends.

1. Monthly, the platform generates an **automated deforestation report** for the Western Ghats.
2. The current month shows **3 new deforestation hotspots** flagged in the Wayanad-Mysore corridor — a critical elephant migration route.
3. The **NDVI change detection** module shows 12 hectares of dense forest converted to what appears to be coffee plantation (NDVI drop + different spectral signature).
4. The team overlays the **Ecologically Sensitive Area (ESA)** boundary — 2 of the 3 hotspots fall within the Kasturirangan-designated ESA zone.
5. They generate a **policy brief** from the platform with satellite imagery, NDVI change maps, and EHI trend data, and submit it to the National Green Tribunal.

### Threat Detection Scenario: Early Warning

**Scenario**: Predicting a biodiversity crisis before it manifests.

- **Month 1**: The anomaly detection model flags a grid cell cluster in the Nilgiri Biosphere Reserve where temperature has been 2.5°C above the 30-year average for 45 consecutive days.
- **Month 2**: NDVI values in the flagged area drop by 15%, but no deforestation is detected. Fire risk model shows elevated scores. The system generates an **"Ecosystem Stress Warning"**.
- **Month 3**: GBIF observation data shows a decline in butterfly species diversity in adjacent cells. The system escalates to a **"Biodiversity Risk Alert"** with a combined analysis:
  - Temperature anomaly → vegetation stress → pollinator decline → potential cascade.
- **Month 4**: Without intervention, this area would have experienced undetected habitat degradation. With the platform's early warning, researchers deploy field teams and the state forest department implements temporary fire monitoring patrols.

---

## 8. Hackathon MVP Plan (24–48 Hours)

### Phase 1: Foundation (Hours 0–8)

**Goal**: Data pipeline + basic backend

| Task | Details | Time |
|------|---------|------|
| Project setup | FastAPI backend scaffold, React frontend scaffold, PostgreSQL with PostGIS (or SQLite) | 1.5 hrs |
| Western Ghats boundary | Load official boundary GeoJSON (available from WDPA/GADM) | 0.5 hrs |
| FIRMS fire data integration | Build connector, fetch last 7 days of fire data for Western Ghats bbox, store in DB | 2 hrs |
| Open-Meteo weather integration | Fetch current + historical weather for 10 representative stations across WG | 2 hrs |
| GBIF biodiversity data | Fetch species occurrences for Western Ghats bbox (top 500 species), store in DB | 2 hrs |

### Phase 2: AI Models (Hours 8–20)

**Goal**: Working prediction models

| Task | Details | Time |
|------|---------|------|
| NDVI data from GEE | Use GEE Python API to compute monthly NDVI composites for last 12 months, export as GeoJSON stats per grid cell | 3 hrs |
| Fire risk model | Train XGBoost on FIRMS historical data + weather features. Simple binary classifier: fire/no-fire per cell. | 3 hrs |
| Ecosystem Health Index | Implement weighted scoring function combining NDVI, weather anomalies, species richness, fire frequency | 2 hrs |
| Anomaly detection | Fit Isolation Forest on historical NDVI + weather baseline, score current conditions | 2 hrs |
| API endpoints | Build REST endpoints for all model predictions and data queries | 2 hrs |

### Phase 3: Dashboard (Hours 20–36)

**Goal**: Interactive visualization

| Task | Details | Time |
|------|---------|------|
| Map component | React + Leaflet/Mapbox showing Western Ghats boundary with layer controls | 3 hrs |
| EHI choropleth layer | Color-coded grid cells by Ecosystem Health Index | 2 hrs |
| Fire alert markers | Real-time fire detections from FIRMS displayed as markers with popups | 2 hrs |
| Species heatmap | GBIF species richness as heatmap layer | 2 hrs |
| Sidebar with metrics | EHI score breakdown, trend sparklines, active alerts list | 2 hrs |
| NDVI trend chart | Interactive line chart for selected region's NDVI over time | 1.5 hrs |
| Alert feed | Real-time list of fire alerts and anomaly warnings | 1.5 hrs |
| Deforestation layer | Visualize NDVI change detection results on map | 2 hrs |

### Phase 4: Polish (Hours 36–48)

| Task | Details | Time |
|------|---------|------|
| End-to-end testing | Test complete workflow from data ingestion to dashboard | 2 hrs |
| Demo data seeding | Ensure compelling data is loaded for demo | 1 hr |
| UI polish | Colors, legends, loading states, error handling | 2 hrs |
| Demo preparation | Build narrative and talking points, screenshots, recordings | 2 hrs |
| README and documentation | Project description, setup instructions, architecture diagram | 1 hr |
| Deployment | Deploy backend to Railway/Render, frontend to Vercel | 2 hrs |
| Buffer | Unexpected bugs and issues | 2 hrs |

### MVP Priority Dataset Selection

| Priority | Dataset | Reason |
|----------|---------|--------|
| **P0** | NASA FIRMS (fire) | Dramatic, real-time, easy API | 
| **P0** | Open-Meteo (weather) | Free, no auth, fast API |
| **P0** | Google Earth Engine (NDVI) | Core satellite intelligence |
| **P1** | GBIF (species) | Rich occurrence data for biodiversity layer |
| **P1** | Hansen/GFW (forest loss) | Available in GEE, essential for deforestation |
| **P2** | OpenAQ (air quality) | Nice-to-have for EHI |
| **P2** | IUCN Red List | Enriches species data with conservation status |

### MVP AI Model Selection

| Model | Complexity | Hackathon Approach |
|-------|-----------|-------------------|
| **Fire Risk** | Medium | XGBoost binary classifier with 5-7 weather + NDVI features |
| **EHI Score** | Low | Weighted formula (no ML needed, deterministic) |
| **Deforestation** | Low-Medium | NDVI threshold-based change detection |
| **Anomaly** | Low | Isolation Forest on 4-5 features from historical baseline |

---

## 9. Recommended Technology Stack

### Frontend

| Technology | Purpose | Why |
|-----------|---------|-----|
| **React 18+** | UI framework | Component-based, massive ecosystem, fast development |
| **TypeScript** | Type safety | Catches bugs early, better developer experience |
| **Mapbox GL JS** or **React-Leaflet** | Geospatial maps | Mapbox: beautiful vector tiles, free tier 50K loads/month. Leaflet: fully open-source, simpler. |
| **Recharts** or **Chart.js** | Data visualization | Time series, bar charts, gauges for EHI |
| **TailwindCSS** | Styling | Utility-first, rapid prototyping |
| **TanStack Query** | Server state | Caching, automatic refetch, loading states |
| **Deck.gl** (optional) | Large-scale geo rendering | WebGL-powered rendering for thousands of grid cells |

### Backend

| Technology | Purpose | Why |
|-----------|---------|-----|
| **Python 3.11+** | Primary language | Dominant in data science, geospatial, and ML ecosystems |
| **FastAPI** | Web framework | Async, auto-docs (Swagger), Pydantic validation, fast |
| **Uvicorn** | ASGI server | High-performance async server for FastAPI |
| **APScheduler** | Task scheduling | Lightweight scheduled jobs (data sync, model refresh) |
| **Celery + Redis** (optional) | Distributed task queue | For heavier background processing if needed |
| **Pydantic** | Data validation | Schema enforcement for API requests/responses |

### Machine Learning

| Technology | Purpose | Why |
|-----------|---------|-----|
| **Scikit-learn** | Classical ML | Random Forest, Isolation Forest, preprocessing pipelines |
| **XGBoost** or **LightGBM** | Gradient boosted trees | State-of-the-art for tabular data (fire risk prediction) |
| **PyTorch** (optional) | Deep learning | U-Net for satellite image segmentation if time permits |
| **NumPy / Pandas** | Data manipulation | Foundation of all data processing |
| **Joblib** | Model serialization | Save/load trained models |

### Geospatial Processing

| Technology | Purpose | Why |
|-----------|---------|-----|
| **Google Earth Engine** (Python API) | Cloud-based satellite analysis | Avoids downloading massive imagery, scalable computation |
| **GeoPandas** | Vector geospatial data | Spatial joins, overlays, geometry operations |
| **Rasterio** | Raster data I/O | Read/write GeoTIFF, zonal statistics |
| **Shapely** | Geometry operations | Point-in-polygon, buffering, intersection |
| **Fiona** | Vector file I/O | Read shapefiles, GeoJSON |
| **GDAL** (via rasterio) | Low-level geospatial | Reprojection, format conversion |
| **Folium** (optional) | Quick Python maps | Rapid prototyping before frontend is ready |

### Database

| Technology | Purpose | Why |
|-----------|---------|-----|
| **PostgreSQL + PostGIS** | Primary database | Spatial queries (ST_Within, ST_Intersects), spatial indexing, mature ecosystem |
| **SQLite + SpatiaLite** | Hackathon alternative | Zero-config, file-based, sufficient for MVP |
| **Redis** | Caching + message broker | Cache map tiles, API responses; broker for Celery |
| **MongoDB** (optional) | Document store | Flexible schema for heterogeneous biodiversity records |

### Cloud & Deployment

| Technology | Purpose | Why |
|-----------|---------|-----|
| **Vercel** | Frontend hosting | Free tier, instant deploys, great for React |
| **Railway** or **Render** | Backend hosting | Free/cheap tier, easy Python deployment, managed PostgreSQL |
| **Google Earth Engine** | Satellite processing cloud | Free for research, eliminates need for heavy compute |
| **AWS S3** / **GCS** | Object storage | Store satellite imagery, model artifacts |
| **Docker** + **Docker Compose** | Containerization | Reproducible dev environment, easy deployment |
| **GitHub Actions** | CI/CD | Automated testing and deployment |

### Key Python Dependencies (requirements.txt)

```
# Web framework
fastapi==0.115.*
uvicorn==0.34.*
pydantic==2.*

# Geospatial
geopandas==1.*
rasterio==1.*
shapely==2.*
fiona==1.*
earthengine-api==1.*
folium==0.18.*

# Machine Learning
scikit-learn==1.*
xgboost==2.*
numpy==2.*
pandas==2.*
joblib==1.*

# Data sources
pygbif==0.*
meteostat==1.*
requests==2.*

# Database
sqlalchemy==2.*
geoalchemy2==0.*
psycopg2-binary==2.*

# Task scheduling
apscheduler==3.*

# Utilities
python-dotenv==1.*
httpx==0.*
```

---

## 10. Innovation Opportunities

The following features would elevate the project from a competent prototype to a hackathon-winning platform:

### 10.1 Ecosystem Health Score (EHI) — Live Composite Index

**What:** A single, easy-to-understand score (0–100) for any location in the Western Ghats, updated in near-real-time.

**Why it's impressive:** No existing platform provides a composite, multi-factor, real-time ecosystem health score for the Western Ghats. Judges can immediately understand "this area scores 43/100 — that's bad" without needing ecological expertise.

**Implementation:** Combine NDVI, forest cover, biodiversity richness, climate anomalies, air quality, and fire disturbance into one weighted score per grid cell (detailed in Section 5.3).

---

### 10.2 AI Biodiversity Risk Index (BRI)

**What:** A predictive index that forecasts which species in a given area are at elevated risk of local extinction based on current environmental trends.

**How:**
1. For each grid cell, identify species historically observed there (GBIF data).
2. Cross-reference each species' environmental tolerance range (from IUCN habitat data and WorldClim bioclimatic variables).
3. Compare current and projected environmental conditions against species tolerance envelopes.
4. Species whose habitat conditions are departing from their tolerance range receive elevated risk scores.
5. Aggregate into a cell-level BRI.

**Why it's impressive:** Provides proactive conservation intelligence — identifying species at risk *before* population collapse, not after.

---

### 10.3 Satellite-Based Deforestation Detection with Change Alerts

**What:** Automated bi-weekly scanning of the entire Western Ghats using Sentinel-2 imagery, detecting new deforestation events and pushing alerts within 5 days of occurrence.

**How:**
1. GEE script computes NDVI for current bi-weekly composite.
2. Compare against same-season baseline NDVI (previous year's composite).
3. Flag pixels where NDVI dropped below threshold (>0.3 decrease) in areas classified as forest.
4. Cluster flagged pixels into events, filter by minimum size (>0.5 ha).
5. Cross-reference with known activities (mining permits, road construction) to classify as legal/suspicious.
6. Push alert to dashboard and subscribed users.

**Why it's impressive:** Mimics Global Forest Watch's GLAD alert system at regional scale with custom sensitivity for Western Ghats forest types.

---

### 10.4 AI-Generated Environmental Reports

**What:** One-click generation of comprehensive environmental status reports for any selected region, combining data visualizations, AI analysis, and narrative text.

**How:**
1. User selects a region (district, protected area, or custom polygon).
2. Backend aggregates all available data layers for that region.
3. An LLM (GPT-4 / Claude API) generates a structured narrative report including:
   - Executive summary
   - Vegetation health analysis with NDVI trend interpretation
   - Biodiversity status with species inventory
   - Climate trend analysis
   - Threat assessment (fire, deforestation, climate anomalies)
   - Recommendations
4. Report is rendered as a downloadable PDF with embedded maps and charts.

**Why it's impressive:** Automates what would take an environmental consultant days. Demonstrates AI going beyond prediction to communication. Extremely useful for government reports and grant applications.

```python
# Example LLM prompt for report generation
def generate_report_prompt(region_data):
    return f"""
    Generate a Western Ghats ecosystem health report for {region_data['name']}.

    Data summary:
    - Ecosystem Health Index: {region_data['ehi']}
    - NDVI trend (12 months): {region_data['ndvi_trend']}
    - Forest cover change: {region_data['forest_change_pct']}%
    - Active fires (last 30 days): {region_data['fire_count']}
    - Species recorded: {region_data['species_count']}
    - Endangered species: {region_data['endangered_species']}
    - Temperature anomaly: {region_data['temp_anomaly']}°C
    - Rainfall anomaly: {region_data['rainfall_anomaly']}%

    Structure: Executive Summary, Vegetation Analysis, Biodiversity Status,
    Climate Assessment, Threats, Recommendations.
    Tone: Technical but accessible. Include specific data points.
    """
```

---

### 10.5 Policy Recommendation Engine

**What:** Based on detected threats and ecosystem conditions, the system generates specific, actionable policy recommendations aligned with Indian environmental law and Western Ghats conservation frameworks.

**How:**
1. Maintain a knowledge base of relevant policies: Wildlife Protection Act (1972), Forest Conservation Act (1980), Western Ghats ESA notifications, Gadgil Committee recommendations, National Biodiversity Act (2002).
2. When a threat is detected (e.g., deforestation in ESA zone), the system:
   - Identifies the applicable legal framework
   - Suggests specific interventions (e.g., "Invoke Section 2 of Forest Conservation Act — unauthorized non-forest use in Reserved Forest")
   - Recommends monitoring escalation (increase satellite revisit frequency, deploy ground teams)
   - Suggests habitat restoration measures
3. Recommendations are ranked by urgency and feasibility.

**Why it's impressive:** Bridges the gap between environmental data and governance action — a major pain point in Indian conservation. Demonstrates the platform's utility beyond monitoring to decision support.

---

### 10.6 Temporal Simulation / "What-If" Analysis

**What:** Allow users to simulate future scenarios: "What happens to ecosystem health in this region if deforestation continues at the current rate for 5 years?"

**How:**
1. Extrapolate current trends (deforestation rate, climate trajectory, species decline rate) forward in time.
2. Apply ecological models (species-area relationships, forest fragmentation thresholds) to estimate cascading impacts.
3. Visualize the simulated future EHI on the map, showing progression year by year.

**Why it's impressive:** Turns the platform from a monitoring tool into a strategic planning tool. Compelling for demo — showing a region turning from green to red over simulated time.

---

### 10.7 Community / Citizen Science Integration

**What:** Allow users to submit field observations (photos, species sightings, threat reports) via the platform, which are verified and integrated into the data pipeline.

**How:**
1. Mobile-friendly submission form with GPS auto-tagging
2. Photo classification using a pretrained species identification model (e.g., iNaturalist's vision model)
3. Flagged submissions for unusual sightings or threats
4. Gamification: contribution leaderboard, badges

**Why it's impressive:** Demonstrates a participatory approach to conservation, increasing data density in areas with sparse sensor coverage.

---

### 10.8 Multi-Lingual Alert System

Since the Western Ghats spans 6 states with different languages (Marathi, Kannada, Malayalam, Tamil, Konkani, Gujarati), alerts and reports generated in local languages using LLM translation would demonstrate real-world deployability and inclusivity.

---

### Summary: Innovation Impact Matrix

| Feature | Technical Difficulty | Demo Impact | Hackathon Feasibility |
|---------|---------------------|-------------|----------------------|
| Ecosystem Health Score | Low | Very High | ✅ Must-have |
| Biodiversity Risk Index | Medium | High | ✅ Achievable |
| Deforestation Detection | Medium | Very High | ✅ Achievable |
| AI-Generated Reports | Medium | Very High | ✅ Achievable (with LLM API) |
| Policy Recommendation Engine | High | Very High | ⚠️ Partial implementation |
| What-If Simulation | High | Very High | ⚠️ Simplified version |
| Citizen Science Integration | Medium | Medium | ⚠️ UI effort |
| Multi-Lingual Alerts | Low | Medium | ✅ Easy with LLM |

---

## 11. Advanced Features (Implemented)

The following four advanced features have been fully implemented in both the backend (FastAPI) and frontend (React), elevating the platform from a monitoring dashboard into an actionable ecosystem intelligence system.

### 11.1 Contextual Alerts & Actionable Playbooks

**Problem:** Raw fire or anomaly alerts lack situational context — responders don't know how close a threat is to a village, a road, or a protected area, making triage difficult.

**Solution:** When a user clicks any fire detection marker on the map, the system instantly computes a **Contextual Alert Report** containing:

- **Proximity analysis** — distance to nearest village, road, and protected area (computed via Haversine formula)
- **Vegetation density classification** — derived from the latest NDVI value at that location (Dense/High/Moderate/Sparse/Barren)
- **Protected area boundary check** — whether the alert falls inside a national park, wildlife sanctuary, or biosphere reserve
- **Estimated fire risk level** — cross-referenced from the XGBoost fire prediction model

Based on this context, an **Actionable Playbook** is auto-generated with specific, prioritized recommended actions:
- *Emergency Protocol* (fire inside dense protected forest near a village) → immediate evacuation coordination, fire crew dispatch, aerial reconnaissance
- *High-Risk Response* (fire in protected area, away from settlements) → ranger deployment, monitoring, fire break establishment
- *Moderate Risk* → scheduled patrol, monitoring, logging
- *Low Risk* → standard observation, periodic satellite review

| Component | Implementation |
|-----------|---------------|
| Backend endpoint | `GET /api/context/alert/{lat}/{lon}?region=` |
| Distance computation | Haversine formula (great-circle distance) |
| Infrastructure database | Curated for all 4 monitored regions — villages, roads, protected areas with lat/lon |
| Frontend component | `ContextPanel.tsx` — renders context cards with proximity info + playbook actions |

### 11.2 Ground Truth Verification Loop

**Problem:** Remote sensing detections (fires, anomalies) produce false positives. Without a mechanism to verify alerts from the ground, the system's reliability cannot be validated or improved.

**Solution:** A **Field Verification System** allows field rangers, researchers, and citizen scientists to submit ground-truth reports for any alert:

- **Submit verification reports** with free-text observations, status classification (verified / resolved / false_alarm), geo-coordinates, and optional photo upload
- **Track verification status** for any alert — check whether a fire detection has been confirmed, resolved, or marked as a false alarm
- **View recent reports** filtered by region — see all field reports from the selected biodiversity hotspot

This creates a **feedback loop** that can be used to:
1. Retrain fire prediction and anomaly detection models with verified labels
2. Compute per-region false positive rates
3. Demonstrate real-world deployment readiness to stakeholders

| Component | Implementation |
|-----------|---------------|
| Backend endpoints | `POST /api/verify/report` (FormData + photo upload), `GET /api/verify/reports`, `GET /api/verify/status/{alert_id}` |
| Database model | `FieldVerification` — stores alert_id, alert_type, lat/lon, message, photo_path, status, reporter_name, timestamp |
| File storage | Uploaded photos saved to `data/uploads/` with UUID filenames |
| Frontend component | `VerificationPanel.tsx` — form submission + report listing with status badges |

### 11.3 Temporal Ecosystem Time Machine

**Problem:** Snapshot-based dashboards show only current conditions. Ecologists and policymakers need to understand **how ecosystem health has changed over time** — is the trend improving, stable, or degrading?

**Solution:** A **12-month interactive timeline slider** that shows the evolution of Ecosystem Health Index (EHI) over the past year:

- **Monthly EHI reconstruction** — for each of the last 12 months, the system computes an approximate EHI using:
  - NDVI data grouped by month → vegetation health and forest integrity sub-indices
  - Stable baseline estimates for biodiversity richness (65), climate stability (60), air quality (55), and fire disturbance (70) — representing long-term regional averages
  - Weighted combination using the standard EHI formula
- **Interactive range slider** — users can scrub through months to see how the overall ecosystem health score changed
- **Trend visualization** — a Recharts AreaChart shows the EHI trend line with gradient fill, with a reference line indicating the currently selected month

This enables temporal analysis questions like:
- *"Did the monsoon season improve vegetation health?"*
- *"When did the EHI start declining — before or after the fire season?"*
- *"Is the ecosystem recovering from last year's drought?"*

| Component | Implementation |
|-----------|---------------|
| Backend endpoints | `GET /api/timemachine/ehi?region=` (12-month timeline), `GET /api/timemachine/ndvi?region=&month=` (monthly NDVI grid) |
| Data source | NDVIConnector fetched NDVI records grouped by `year-month` |
| EHI approximation | Monthly vegetation/forest sub-indices from NDVI + stable baselines for other sub-indices |
| Frontend component | `TimeMachineSlider.tsx` — range input + AreaChart with gradient, toggled via "⏳ Timeline" button in layer controls |

### 11.4 AI Narrative Summary

**Problem:** Grid cells display numerical metrics (EHI score, NDVI, fire risk %) that require domain expertise to interpret. Non-expert users (policymakers, journalists, NGO staff) need **plain-language explanations** of what the data means.

**Solution:** For any selected grid cell, the system generates a **natural language narrative** that synthesizes all available data into a readable summary:

- **EHI status sentence** — *"Overall ecosystem health scores **64/100** (good)."*
- **NDVI and vegetation sentence** — *"Vegetation is moderately healthy (NDVI 0.69), with a stable trend over the past 12 months."*
- **Biodiversity sentence** — *"This cell hosts 12 recorded species, indicating moderate biodiversity."*
- **Fire risk sentence** — *"Fire risk is currently **low** at 15% probability."* or *"Fire risk is **extreme** at 92%."*
- **Anomaly sentence** — *"An environmental anomaly has been flagged — investigate potential disruption."*

The narrative is composed using template-based natural language generation (NLG) functions that select appropriate wording based on metric thresholds. This approach is deterministic, fast, and requires no external LLM API.

Alongside the narrative, compact **data chips** display the raw metrics (EHI score, NDVI with trend arrow, species count, fire risk %, anomaly flag) for users who want both the story and the numbers.

| Component | Implementation |
|-----------|---------------|
| Backend endpoint | `GET /api/narrative/{cell_id}?region=` |
| Data aggregation | Gathers EHI, NDVI timeseries, fire risk, anomalies, species count for the cell |
| NLG engine | Template functions: `_ehi_sentence()`, `_ndvi_sentence()`, `_biodiversity_sentence()`, `_risk_sentence()`, `_anomaly_sentence()` |
| Frontend component | `NarrativePanel.tsx` — rendered in sidebar when a cell is selected, shows narrative text + data chips |

### Advanced Features: Impact Summary

| Feature | Problem Solved | Key Differentiator | Technical Complexity |
|---------|---------------|-------------------|---------------------|
| Contextual Alerts & Playbooks | Raw alerts lack spatial context | Auto-generated response protocols based on proximity + risk | Medium |
| Ground Truth Verification | No feedback loop for ML models | Bridges satellite AI with field reality | Medium |
| Temporal Time Machine | No historical trend visibility | 12-month EHI evolution with interactive scrubbing | Medium |
| AI Narrative Summary | Data overload for non-experts | Plain-language ecosystem intelligence per grid cell | Low–Medium |

---

## Appendix A: Western Ghats Bounding Box and Key Coordinates

```json
{
  "bounding_box": {
    "west": 72.5,
    "south": 8.0,
    "east": 78.5,
    "north": 21.5
  },
  "key_locations": {
    "nilgiri_hills": {"lat": 11.4, "lon": 76.7},
    "anamalai_hills": {"lat": 10.3, "lon": 77.0},
    "wayanad": {"lat": 11.7, "lon": 76.1},
    "kudremukh": {"lat": 13.2, "lon": 75.2},
    "agumbe": {"lat": 13.5, "lon": 75.1},
    "silent_valley": {"lat": 11.1, "lon": 76.4},
    "kodagu_coorg": {"lat": 12.4, "lon": 75.7},
    "mahabaleshwar": {"lat": 17.9, "lon": 73.7},
    "amboli": {"lat": 15.9, "lon": 74.0}
  },
  "protected_areas_count": 39,
  "national_parks": ["Silent Valley", "Kudremukh", "Bandipur", "Mudumalai", "Eravikulam", "Periyar"],
  "tiger_reserves": ["Bhadra", "Bandipur-Nagarhole", "Parambikulam", "Kalakad-Mundanthurai"]
}
```

## Appendix B: Quick API Reference

| API | Base URL | Auth | Rate Limit |
|-----|----------|------|------------|
| NASA FIRMS | `https://firms.modaps.eosdis.nasa.gov/api/` | MAP_KEY | Reasonable use |
| Open-Meteo | `https://api.open-meteo.com/v1/` | None | 10,000/day (free) |
| GBIF | `https://api.gbif.org/v1/` | None (optional API key) | Reasonable use |
| IUCN Red List | `https://apiv3.iucnredlist.org/api/v3/` | API token | ~100K/day |
| OpenAQ | `https://api.openaq.org/v2/` | None | 100/min |
| AQICN | `https://api.waqi.info/` | API token | ~1,000/day |
| Google Earth Engine | Python API (`ee`) | Google account / service account | Computation quotas |
| Meteostat | Python library / `https://meteostat.p.rapidapi.com/` | None (Python) / RapidAPI key | Reasonable use |
| GFW | `https://data-api.globalforestwatch.org/` | API key | Reasonable use |

## Appendix C: Project Directory Structure (Recommended)

```
western-ghats-monitor/
├── README.md
├── docker-compose.yml
├── .env.example
│
├── backend/
│   ├── main.py                    # FastAPI application entry
│   ├── config.py                  # Environment variables, settings
│   ├── requirements.txt
│   │
│   ├── api/
│   │   ├── routes/
│   │   │   ├── map.py             # /api/map endpoints
│   │   │   ├── alerts.py          # /api/alerts endpoints
│   │   │   ├── predict.py         # /api/predict endpoints
│   │   │   ├── data.py            # /api/data endpoints
│   │   │   ├── context.py         # Contextual alerts & playbooks
│   │   │   ├── verification.py    # Ground truth verification loop
│   │   │   ├── timemachine.py     # Temporal ecosystem time machine
│   │   │   └── narrative.py       # AI narrative summary generation
│   │   └── dependencies.py
│   │
│   ├── connectors/
│   │   ├── base.py                # DataConnector ABC
│   │   ├── firms.py               # NASA FIRMS connector
│   │   ├── open_meteo.py          # Open-Meteo weather connector
│   │   ├── gbif.py                # GBIF biodiversity connector
│   │   ├── gee.py                 # Google Earth Engine connector
│   │   ├── openaq.py              # OpenAQ air quality connector
│   │   └── gfw.py                 # Global Forest Watch connector
│   │
│   ├── models/
│   │   ├── fire_risk.py           # Fire risk prediction model
│   │   ├── deforestation.py       # Deforestation detection
│   │   ├── ecosystem_health.py    # EHI computation
│   │   └── anomaly.py             # Anomaly detection
│   │
│   ├── services/
│   │   ├── map_service.py
│   │   ├── alert_service.py
│   │   ├── prediction_service.py
│   │   └── data_service.py
│   │
│   ├── db/
│   │   ├── database.py            # DB connection, session
│   │   ├── models.py              # SQLAlchemy ORM models
│   │   └── migrations/
│   │
│   ├── tasks/
│   │   ├── scheduler.py           # APScheduler configuration
│   │   ├── sync_firms.py          # Fire data sync task
│   │   ├── sync_weather.py        # Weather data sync task
│   │   └── compute_ehi.py         # EHI recomputation task
│   │
│   └── utils/
│       ├── geo.py                 # Geospatial utilities
│       └── grid.py                # Grid creation and management
│
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   │
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   │
│   │   ├── components/
│   │   │   ├── Map/
│   │   │   │   ├── MapView.tsx        # Main map component
│   │   │   │   ├── EHILayer.tsx       # Ecosystem health choropleth
│   │   │   │   ├── FireLayer.tsx      # Fire alert markers
│   │   │   │   ├── SpeciesLayer.tsx   # Species heatmap
│   │   │   │   └── DeforestLayer.tsx  # Deforestation overlay
│   │   │   │
│   │   │   ├── Sidebar/
│   │   │   │   ├── EHIPanel.tsx       # EHI score & breakdown
│   │   │   │   ├── AlertFeed.tsx      # Active alerts list
│   │   │   │   └── RegionInfo.tsx     # Selected region details
│   │   │   │
│   │   │   ├── ContextPanel.tsx       # Contextual alerts & playbooks
│   │   │   ├── VerificationPanel.tsx  # Ground truth verification
│   │   │   ├── TimeMachineSlider.tsx  # Temporal EHI timeline
│   │   │   ├── NarrativePanel.tsx     # AI narrative summary
│   │   │   │
│   │   │   └── Charts/
│   │   │       ├── NDVITrend.tsx      # NDVI time series chart
│   │   │       ├── ClimateChart.tsx   # Temperature/rainfall chart
│   │   │       └── EHIGauge.tsx       # EHI gauge visualization
│   │   │
│   │   ├── hooks/
│   │   │   ├── useMapData.ts
│   │   │   ├── useAlerts.ts
│   │   │   └── usePredictions.ts
│   │   │
│   │   ├── services/
│   │   │   └── api.ts                 # API client
│   │   │
│   │   └── types/
│   │       └── index.ts               # TypeScript interfaces
│   │
│   └── public/
│       └── western_ghats.geojson      # WG boundary for map
│
├── data/
│   ├── boundary/                      # Western Ghats boundary shapefiles
│   ├── grid/                          # Precomputed grid cells
│   └── models/                        # Trained model artifacts
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_ndvi_analysis.ipynb
│   ├── 03_fire_risk_model.ipynb
│   └── 04_ehi_computation.ipynb
│
└── scripts/
    ├── create_grid.py                 # Generate Western Ghats grid
    ├── seed_data.py                   # Initial data loading
    └── train_models.py                # Model training pipeline
```

---

*This technical blueprint provides the complete foundation to build an AI-Powered Ecosystem & Biodiversity Monitoring Platform for the Western Ghats. The architecture is designed to be modular — start with the MVP in Section 8, then progressively add capabilities from Sections 5, 6, and 10.*
