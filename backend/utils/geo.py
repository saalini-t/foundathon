"""Geospatial utility functions."""

import json
import os


def load_boundary(boundary_file: str = "western_ghats.geojson") -> dict:
    """Load a boundary GeoJSON by filename."""
    boundary_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "data", "boundary", boundary_file
    )
    boundary_path = os.path.abspath(boundary_path)
    with open(boundary_path, "r") as f:
        return json.load(f)


# Backward-compatible alias
def load_western_ghats_boundary() -> dict:
    return load_boundary("western_ghats.geojson")


def point_in_bbox(lat: float, lon: float, bbox: tuple) -> bool:
    """Check if a point falls within a bounding box (W, S, E, N)."""
    west, south, east, north = bbox
    return south <= lat <= north and west <= lon <= east
