# 🌿 Western Ghats Ecosystem Monitor

**AI-Powered Ecosystem & Biodiversity Monitoring Platform for the Western Ghats, India**

A real-time environmental intelligence dashboard that combines satellite imagery analysis, machine learning models, and multi-source biodiversity data to monitor ecosystem health across one of the world's most biodiverse regions — the Western Ghats UNESCO World Heritage Site.

![Dashboard](https://img.shields.io/badge/Dashboard-React-61DAFB?style=flat&logo=react)
![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi)
![ML](https://img.shields.io/badge/ML-XGBoost%20%7C%20Scikit--learn-FF6600?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## 🎯 What It Does

| Feature | Description |
|---------|-------------|
| **Ecosystem Health Index (EHI)** | Composite 0–100 score per grid cell combining vegetation, forest integrity, biodiversity, climate, air quality, and fire disturbance |
| **Wildfire Risk Prediction** | XGBoost ML model predicting fire probability using NDVI, weather, and terrain features |
| **Anomaly Detection** | Isolation Forest identifying unusual ecosystem changes (drought, deforestation, heat anomalies) |
| **Biodiversity Mapping** | Species richness heatmap from 800+ species across 2,100+ GBIF occurrence records |
| **NDVI Vegetation Monitoring** | Satellite-derived vegetation indices with 12-month trend analysis |
| **Real-Time Fire Alerts** | Active fire detections from NASA FIRMS VIIRS satellite data |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     FRONTEND DASHBOARD                              │
│  React 18 + TypeScript │ Leaflet Maps │ Recharts │ TailwindCSS     │
│  6 interactive map layers │ EHI gauges │ NDVI charts │ Alert feed  │
└─────────────────────────────┬───────────────────────────────────────┘
                              │ Vite proxy → /api
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     BACKEND API (FastAPI)                            │
│  /api/map/* │ /api/alerts/* │ /api/predict/* │ /api/data/*          │
│  /api/ndvi/* │ /api/sync/*                                          │
├─────────────────────────────────────────────────────────────────────┤
│  AI MODEL LAYER                       │  DATA CONNECTORS            │
│  ┌────────────────┐ ┌──────────────┐  │  ┌─────────────────┐       │
│  │ XGBoost Fire   │ │ Isolation    │  │  │ NASA FIRMS      │       │
│  │ Risk Predictor │ │ Forest       │  │  │ Open-Meteo      │       │
│  │ (AUC: 0.87)   │ │ Anomaly Det. │  │  │ GBIF Biodiv.    │       │
│  ├────────────────┤ ├──────────────┤  │  │ Sentinel-2 NDVI │       │
│  │ EHI Composite  │ │ NDVI Trend   │  │  └─────────────────┘       │
│  │ Scorer (0-100) │ │ Analysis     │  │                             │
│  └────────────────┘ └──────────────┘  │                             │
├─────────────────────────────────────────────────────────────────────┤
│  DATABASE: SQLite + WAL mode                                        │
│  Tables: fire_alerts │ weather_observations │ species_occurrences   │
│          grid_cells                                                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 18+** (with npm)
- Git

### 1. Clone & Install

```bash
git clone <repo-url>
cd foundathon

# Backend dependencies
pip install -r backend/requirements.txt

# Frontend dependencies
cd frontend
npm install
cd ..
```

### 2. Environment Setup

```bash
# Copy the example env file
cp .env.example .env

# (Optional) Add your NASA FIRMS API key for live fire data
# Get one free at: https://firms.modaps.eosdis.nasa.gov/api/
# Edit .env and set: FIRMS_API_KEY=your_key_here
```

### 3. Seed the Database

```bash
# Seed with real data from APIs
python -m backend.scripts.seed_data

# Add demo fire alerts + calibrate anomaly model
python -m backend.scripts.seed_demo
```

### 4. Start the Platform

```bash
# Terminal 1: Backend (port 8000)
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend (port 5173)
cd frontend
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## 📊 Dashboard Layers

### 🌿 Ecosystem Health Index (EHI)
Choropleth map with composite health score per 0.1° grid cell (~11km). Six sub-indices weighted by ecological importance:

| Sub-Index | Weight | Source |
|-----------|--------|--------|
| Vegetation Health | 25% | Sentinel-2 NDVI |
| Forest Integrity | 20% | NDVI baseline comparison |
| Biodiversity Richness | 20% | GBIF species density |
| Climate Stability | 15% | Temperature/rainfall anomalies |
| Air Quality | 10% | Simulated PM2.5 data |
| Fire Disturbance | 10% | FIRMS fire frequency |

### 🔥 Active Fire Detections
Real-time fire markers from NASA FIRMS VIIRS satellite. Circle size indicates Fire Radiative Power (FRP), color indicates confidence level.

### 🎯 AI Fire Risk Prediction
XGBoost binary classifier trained on 8,000 samples with 11 features. Grid cells colored by predicted fire probability.

### 🦎 Species Biodiversity Heatmap
Density visualization of 800+ species from GBIF occurrence records using Leaflet.heat.

### 🌳 NDVI Vegetation Index
Normalized Difference Vegetation Index values per grid cell. Click any cell to see a 12-month NDVI trend chart. Low-NDVI areas highlighted as potential deforestation zones.

### ⚠️ Ecosystem Anomalies
Isolation Forest model detects multi-variate anomalies across NDVI, temperature, precipitation, and fire patterns. Anomalous cells shown with severity-based coloring and explanatory factors.

---

## 🧠 AI/ML Models

### Fire Risk Prediction
- **Algorithm**: XGBoost Gradient Boosted Trees
- **Features**: NDVI, temperature, precipitation, humidity, wind speed, days since rain, fire history, month, latitude
- **Performance**: AUC 0.87, F1 0.74
- **Top feature**: `days_since_rain` (importance: 0.54)

### Anomaly Detection
- **Algorithm**: Isolation Forest (scikit-learn)
- **Features**: NDVI mean/deviation, temperature mean/deviation, precipitation, fire count
- **Contamination**: 8% (calibrated for demo sensitivity)

### Ecosystem Health Index
- **Method**: Weighted composite scoring (deterministic)
- **Range**: 0 (critically degraded) – 100 (pristine)
- **Categories**: Critical < 20 < Poor < 40 < Fair < 60 < Good < 80 < Excellent

---

## 📁 Project Structure

```
foundathon/
├── backend/
│   ├── main.py                  # FastAPI application entry point
│   ├── config.py                # Settings & environment variables
│   ├── requirements.txt         # Python dependencies
│   ├── api/routes/
│   │   ├── map.py               # Map data endpoints (boundary, layers)
│   │   ├── alerts.py            # Fire alert endpoints
│   │   ├── data.py              # Weather & species data endpoints
│   │   └── predict.py           # ML prediction endpoints
│   ├── connectors/
│   │   ├── base.py              # Abstract connector base class
│   │   ├── firms.py             # NASA FIRMS fire data
│   │   ├── open_meteo.py        # Open-Meteo weather API
│   │   ├── gbif.py              # GBIF biodiversity records
│   │   └── ndvi.py              # Simulated Sentinel-2 NDVI
│   ├── db/
│   │   ├── database.py          # SQLAlchemy engine & session
│   │   └── models.py            # ORM models (4 tables)
│   ├── ml/
│   │   ├── fire_risk.py         # XGBoost fire risk model
│   │   ├── ehi.py               # Ecosystem Health Index scorer
│   │   ├── anomaly.py           # Isolation Forest anomaly detector
│   │   └── saved_models/        # Serialized model files
│   ├── scripts/
│   │   ├── seed_data.py         # Initial data seeding
│   │   └── seed_demo.py         # Demo data + model calibration
│   └── utils/
│       └── geo.py               # Geospatial utilities
├── frontend/
│   ├── src/
│   │   ├── App.tsx              # Main app with layer controls
│   │   ├── services/api.ts      # API client & TypeScript interfaces
│   │   └── components/
│   │       ├── Header.tsx        # Platform header with stats
│   │       ├── Sidebar.tsx       # EHI metrics, weather, species
│   │       ├── AlertFeed.tsx     # Live fire + anomaly alerts
│   │       ├── NDVITrendChart.tsx # 12-month NDVI chart
│   │       └── Map/
│   │           ├── MapView.tsx        # Main Leaflet map
│   │           ├── EHIChoropleth.tsx   # EHI grid layer
│   │           ├── FireMarkers.tsx     # Fire detection markers
│   │           ├── FireRiskLayer.tsx   # AI risk grid layer
│   │           ├── SpeciesHeatmap.tsx  # Biodiversity heatmap
│   │           └── DeforestationLayer.tsx  # NDVI/deforestation
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── data/
│   ├── boundary/western_ghats.geojson
│   └── ecosystem_monitor.db     # SQLite database
└── .env                         # Environment variables
```

---

## 🔌 API Reference

The backend provides auto-generated API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/map/boundary` | Western Ghats boundary GeoJSON |
| GET | `/api/map/fire-layer` | Fire detections as GeoJSON |
| GET | `/api/map/species-layer` | Species occurrences GeoJSON |
| GET | `/api/map/species-heatmap` | Species density grid |
| GET | `/api/alerts/fires` | Recent fire alerts |
| GET | `/api/data/weather/stations` | Weather station list |
| GET | `/api/data/weather/current` | Live weather from Open-Meteo |
| GET | `/api/data/species/summary` | Top species by occurrence |
| GET | `/api/data/stats` | Platform statistics |
| GET | `/api/predict/ehi` | Ecosystem Health Index grid |
| GET | `/api/predict/fire-risk` | Fire risk predictions grid |
| GET | `/api/predict/anomalies` | Anomaly detection results |
| GET | `/api/ndvi/latest` | Latest NDVI values |
| GET | `/api/ndvi/timeseries/{cell_id}` | 12-month NDVI trend |

---

## 🛠️ Technology Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | React 18, TypeScript, Vite, Leaflet, Recharts, TailwindCSS, TanStack Query |
| **Backend** | Python 3.11, FastAPI, Uvicorn, SQLAlchemy, Pydantic |
| **ML/AI** | XGBoost, scikit-learn (Isolation Forest), NumPy, Pandas, Joblib |
| **Data Sources** | NASA FIRMS, Open-Meteo, GBIF, Sentinel-2 (simulated) |
| **Database** | SQLite with WAL mode |
| **Geospatial** | GeoPandas, Shapely, GeoJSON |

---

## 🌍 Data Sources

| Source | Data Type | Frequency |
|--------|-----------|-----------|
| **NASA FIRMS** | Active fire detections (VIIRS 375m) | Near real-time (~3hr) |
| **Open-Meteo** | Weather: temp, precip, humidity, wind | Daily/hourly |
| **GBIF** | Species occurrence records | Weekly sync |
| **Sentinel-2** (simulated) | NDVI vegetation indices | Monthly composites |

---

## 📄 License

MIT License — built for the Foundathon hackathon.
