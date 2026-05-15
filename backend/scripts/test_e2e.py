"""End-to-end test of all API endpoints."""
import requests
import sys

base = "http://localhost:8000"
errors = []

def test(num, name, url, timeout=10, check=None):
    try:
        r = requests.get(base + url, timeout=timeout)
        if r.status_code != 200:
            errors.append(f"[{num}] {name}: HTTP {r.status_code}")
            print(f"  FAIL [{num}] {name}: HTTP {r.status_code}")
            return None
        d = r.json()
        info = check(d) if check else str(d)[:80]
        print(f"  OK   [{num}] {name}: {info}")
        return d
    except Exception as e:
        errors.append(f"[{num}] {name}: {e}")
        print(f"  FAIL [{num}] {name}: {e}")
        return None

print("=== COMPREHENSIVE END-TO-END TEST ===\n")

test(1, "Health", "/health", check=lambda d: d.get("status"))
test(2, "Stats", "/api/data/stats", check=lambda d: f"fires={d['fire_detections']}, species={d['unique_species']}, weather={d['weather_observations']}")
test(3, "Boundary", "/api/map/boundary", check=lambda d: f"{len(d.get('features',[]))} features")
test(4, "Fire Layer", "/api/map/fire-layer?days=7", check=lambda d: f"{d['metadata']['count']} fire features")
test(5, "Species Heatmap", "/api/map/species-heatmap", check=lambda d: f"{d['count']} grid points")
test(6, "Fire Alerts", "/api/alerts/fires?days=7", check=lambda d: f"{d['count']} alerts")
test(7, "Weather Stations", "/api/data/weather/stations", check=lambda d: f"{len(d['stations'])} stations")
test(8, "Current Weather", "/api/data/weather/current", 15, check=lambda d: f"{d['count']} stations")
test(9, "Species Summary", "/api/data/species/summary", check=lambda d: f"{d['total_species']} species")
ehi = test(10, "EHI Grid", "/api/predict/ehi", 30, check=lambda d: f"avg={d['average_ehi']}, cells={d['count']}")
test(11, "Fire Risk", "/api/predict/fire-risk", 30, check=lambda d: f"{d['count']} predictions")
test(12, "Anomalies", "/api/predict/anomalies", 30, check=lambda d: f"{d['anomaly_count']}/{d['count']} anomalous")
ndvi = test(13, "NDVI Latest", "/api/ndvi/latest", 15, check=lambda d: f"{d['count']} cells")

if ndvi and ndvi.get("cells"):
    cid = ndvi["cells"][0]["cell_id"]
    test(14, f"NDVI Timeseries ({cid})", f"/api/ndvi/timeseries/{cid}", 10, check=lambda d: f"{d['count']} months")

print(f"\n{'='*50}")
if errors:
    print(f"FAILED: {len(errors)} errors")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
else:
    print("ALL 14 TESTS PASSED")
