"""
Feature 1 — Contextual Alerts & Actionable Playbooks
======================================================
When a fire/anomaly alert is clicked, return environmental context
(proximity to villages, roads, protected areas, vegetation density)
and recommended response actions.
"""

import logging
import math
from typing import Any

from fastapi import APIRouter, Query
from backend.regions import get_region

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/context", tags=["context"])

# ── Simulated geospatial reference data per region ────────────
# In production these would come from OpenStreetMap / PostGIS queries.
# For the MVP we maintain representative data per region.

REGION_INFRASTRUCTURE: dict[str, dict[str, list[dict]]] = {
    "western_ghats": {
        "villages": [
            {"name": "Meppadi", "lat": 11.55, "lon": 76.13},
            {"name": "Bavali", "lat": 11.73, "lon": 75.99},
            {"name": "Lakkidi", "lat": 11.52, "lon": 76.04},
            {"name": "Sulthan Bathery", "lat": 11.66, "lon": 76.26},
            {"name": "Gundlupet", "lat": 11.81, "lon": 76.69},
            {"name": "Agumbe", "lat": 13.50, "lon": 75.10},
            {"name": "Thirthahalli", "lat": 13.69, "lon": 75.24},
            {"name": "Madikeri", "lat": 12.42, "lon": 75.74},
            {"name": "Kalpetta", "lat": 11.61, "lon": 76.08},
            {"name": "Munnar Town", "lat": 10.09, "lon": 77.06},
        ],
        "roads": [
            {"name": "NH-766 (Kozhikode-Mysore)", "lat": 11.60, "lon": 76.10},
            {"name": "NH-275 (Mysore-Ooty)", "lat": 11.80, "lon": 76.60},
            {"name": "SH-17 (Agumbe Ghat)", "lat": 13.51, "lon": 75.09},
            {"name": "NH-48 (Mangalore-Bangalore)", "lat": 12.80, "lon": 75.50},
            {"name": "NH-85 (Munnar Road)", "lat": 10.10, "lon": 77.00},
        ],
        "protected_areas": [
            {"name": "Wayanad Wildlife Sanctuary", "lat": 11.72, "lon": 76.08},
            {"name": "Bandipur National Park", "lat": 11.66, "lon": 76.63},
            {"name": "Kudremukh National Park", "lat": 13.18, "lon": 75.25},
            {"name": "Silent Valley National Park", "lat": 11.07, "lon": 76.43},
            {"name": "Periyar Tiger Reserve", "lat": 9.47, "lon": 77.17},
            {"name": "Mudumalai Tiger Reserve", "lat": 11.56, "lon": 76.55},
            {"name": "Nagarhole National Park", "lat": 12.05, "lon": 76.10},
        ],
    },
    "amazon_rainforest": {
        "villages": [
            {"name": "São Gabriel", "lat": -0.13, "lon": -67.09},
            {"name": "Tefé", "lat": -3.35, "lon": -64.71},
            {"name": "Itacoatiara", "lat": -3.14, "lon": -58.44},
            {"name": "Parintins", "lat": -2.63, "lon": -56.74},
            {"name": "Altamira", "lat": -3.20, "lon": -52.21},
            {"name": "Itaituba", "lat": -4.28, "lon": -55.99},
            {"name": "Marabá", "lat": -5.37, "lon": -49.12},
        ],
        "roads": [
            {"name": "BR-163 (Cuiabá-Santarém)", "lat": -4.50, "lon": -55.50},
            {"name": "Trans-Amazonian Highway (BR-230)", "lat": -3.80, "lon": -52.00},
            {"name": "BR-174 (Manaus-Boa Vista)", "lat": -1.50, "lon": -60.50},
        ],
        "protected_areas": [
            {"name": "Jaú National Park", "lat": -2.00, "lon": -62.50},
            {"name": "Tapajós National Forest", "lat": -3.30, "lon": -55.00},
            {"name": "Xingu Indigenous Park", "lat": -5.50, "lon": -53.50},
            {"name": "Anavilhanas National Park", "lat": -2.38, "lon": -60.95},
        ],
    },
    "borneo": {
        "villages": [
            {"name": "Long Lellang", "lat": 3.40, "lon": 115.20},
            {"name": "Bario", "lat": 3.74, "lon": 115.48},
            {"name": "Sukau", "lat": 5.50, "lon": 118.30},
            {"name": "Deramakot", "lat": 5.25, "lon": 117.35},
            {"name": "Tanjung Puting", "lat": -2.75, "lon": 111.75},
        ],
        "roads": [
            {"name": "Pan Borneo Highway", "lat": 2.00, "lon": 111.00},
            {"name": "Sandakan-Kota Kinabalu Highway", "lat": 5.90, "lon": 117.00},
            {"name": "Trans-Kalimantan Highway", "lat": -1.00, "lon": 114.00},
        ],
        "protected_areas": [
            {"name": "Danum Valley", "lat": 4.96, "lon": 117.80},
            {"name": "Kinabalu National Park", "lat": 6.08, "lon": 116.55},
            {"name": "Tanjung Puting National Park", "lat": -2.75, "lon": 111.90},
            {"name": "Heart of Borneo Corridor", "lat": 1.50, "lon": 115.00},
        ],
    },
    "eastern_himalaya": {
        "villages": [
            {"name": "Yuksom", "lat": 27.37, "lon": 88.22},
            {"name": "Lachung", "lat": 27.69, "lon": 88.75},
            {"name": "Mangan", "lat": 27.51, "lon": 88.53},
            {"name": "Ziro", "lat": 27.54, "lon": 93.83},
            {"name": "Tawang Town", "lat": 27.59, "lon": 91.87},
        ],
        "roads": [
            {"name": "NH-10 (Siliguri-Gangtok)", "lat": 27.00, "lon": 88.50},
            {"name": "NH-13 (Tezpur-Tawang)", "lat": 27.30, "lon": 92.00},
            {"name": "NH-31 (Terai Highway)", "lat": 26.50, "lon": 90.00},
        ],
        "protected_areas": [
            {"name": "Kaziranga National Park", "lat": 26.58, "lon": 93.17},
            {"name": "Kanchenjunga National Park", "lat": 27.60, "lon": 88.30},
            {"name": "Namdapha National Park", "lat": 27.50, "lon": 96.40},
            {"name": "Manas National Park", "lat": 26.70, "lon": 91.00},
        ],
    },
}


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two points in km."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _nearest(lat: float, lon: float, items: list[dict]) -> dict:
    """Find the nearest item and its distance."""
    best = None
    best_dist = float("inf")
    for item in items:
        d = _haversine_km(lat, lon, item["lat"], item["lon"])
        if d < best_dist:
            best_dist = d
            best = item
    return {"name": best["name"] if best else "Unknown", "distance_km": round(best_dist, 1)}


def _vegetation_density_label(ndvi: float) -> str:
    if ndvi >= 0.7:
        return "Very High"
    if ndvi >= 0.55:
        return "High"
    if ndvi >= 0.4:
        return "Moderate"
    if ndvi >= 0.25:
        return "Low"
    return "Very Low"


def _generate_playbook(fire_risk_level: str, vegetation: str, dist_village_km: float, is_protected: bool) -> list[str]:
    """Generate context-aware recommended response actions."""
    actions: list[str] = []

    # Fire response actions
    if fire_risk_level in ("high", "extreme"):
        actions.append("Deploy rapid-response ranger team for immediate ground inspection")
        actions.append("Alert nearest fire station and coordinate aerial surveillance")
    else:
        actions.append("Schedule ranger patrol within 24 hours")

    # Proximity actions
    if dist_village_km < 5:
        actions.append(f"Issue community alert to settlement ({dist_village_km} km away)")
        actions.append("Activate village-level disaster preparedness protocols")

    # Vegetation actions
    if vegetation in ("Very High", "High"):
        actions.append("Monitor soil moisture and fuel load levels")
        actions.append("Establish fire break perimeter if risk escalates")
    else:
        actions.append("Verify satellite detection with ground observation")

    # Protected area actions
    if is_protected:
        actions.append("Notify Wildlife Warden and initiate Protected Area emergency protocol")
        actions.append("Ensure no wildlife corridors are compromised")

    actions.append("Log incident in field verification system for follow-up")
    return actions


@router.get("/alert/{lat}/{lon}")
def get_alert_context(
    lat: float,
    lon: float,
    region: str = Query(None, description="Region id"),
):
    """
    Return environmental context and actionable playbook for a given alert location.
    """
    r = get_region(region)

    # Fetch infrastructure for this region
    infra = REGION_INFRASTRUCTURE.get(r.id, REGION_INFRASTRUCTURE["western_ghats"])

    nearest_village = _nearest(lat, lon, infra["villages"])
    nearest_road = _nearest(lat, lon, infra["roads"])
    nearest_pa = _nearest(lat, lon, infra["protected_areas"])

    # Get NDVI for vegetation density
    from backend.connectors.ndvi import NDVIConnector
    ndvi_connector = NDVIConnector(region_id=r.id)
    latest_ndvi = ndvi_connector.get_latest_ndvi()

    # Find closest cell
    best_ndvi = 0.5  # default
    for cell in latest_ndvi:
        d = abs(cell["center_lat"] - lat) + abs(cell["center_lon"] - lon)
        if d < 0.15:
            best_ndvi = cell["ndvi_mean"]
            break

    veg_label = _vegetation_density_label(best_ndvi)
    is_protected = nearest_pa["distance_km"] < 10
    fire_risk = "high" if best_ndvi < 0.4 else "moderate" if best_ndvi < 0.6 else "low"

    playbook = _generate_playbook(fire_risk, veg_label, nearest_village["distance_km"], is_protected)

    return {
        "location": {"latitude": lat, "longitude": lon},
        "context": {
            "nearest_village": nearest_village,
            "nearest_road": nearest_road,
            "nearest_protected_area": nearest_pa,
            "vegetation_density": veg_label,
            "ndvi_value": round(best_ndvi, 3),
            "inside_protected_area": is_protected,
            "estimated_fire_risk": fire_risk,
        },
        "playbook": {
            "title": f"{'High' if fire_risk in ('high','extreme') else 'Moderate'} Risk Zone Detected",
            "recommended_actions": playbook,
        },
    }
