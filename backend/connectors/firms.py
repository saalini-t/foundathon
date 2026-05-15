"""
NASA FIRMS (Fire Information for Resource Management System) connector.

Fetches active fire detections from VIIRS/MODIS satellites for the Western Ghats.
API docs: https://firms.modaps.eosdis.nasa.gov/api/
"""

import logging
from io import StringIO
from typing import Any

import httpx
import pandas as pd

from backend.config import get_settings
from backend.connectors.base import DataConnector

logger = logging.getLogger(__name__)

FIRMS_BASE_URL = "https://firms.modaps.eosdis.nasa.gov/api/area/csv"


class FIRMSConnector(DataConnector):
    """Connector for NASA FIRMS active fire data."""

    def __init__(self):
        self.settings = get_settings()
        self.api_key = self.settings.firms_api_key

    def get_source_name(self) -> str:
        return "NASA FIRMS"

    def fetch(
        self,
        bbox: tuple | None = None,
        start_date: str = "",
        end_date: str = "",
        days: int = 7,
        source: str = "VIIRS_SNPP_NRT",
    ) -> list[dict[str, Any]]:
        """
        Fetch active fire detections.

        Args:
            bbox: (west, south, east, north). Defaults to Western Ghats.
            start_date: Not used directly (FIRMS uses 'days' parameter).
            end_date: Not used directly.
            days: Number of days to look back (1-10).
            source: VIIRS_SNPP_NRT, VIIRS_NOAA20_NRT, or MODIS_NRT.

        Returns:
            List of fire detection records.
        """
        if not self.api_key or self.api_key == "your_firms_map_key_here":
            logger.warning("FIRMS API key not configured. Returning empty results.")
            return []

        if bbox is None:
            bbox = self.settings.wg_bbox

        bbox_str = f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}"
        days = max(1, min(10, days))

        url = f"{FIRMS_BASE_URL}/{self.api_key}/{source}/{bbox_str}/{days}"

        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.get(url)
                response.raise_for_status()

            if not response.text.strip():
                logger.info("FIRMS returned empty response — no fires detected.")
                return []

            df = pd.read_csv(StringIO(response.text))

            if df.empty:
                logger.info("No fire detections in the specified area/period.")
                return []

            logger.info(f"FIRMS: fetched {len(df)} fire detections for last {days} days.")
            return df.to_dict(orient="records")

        except httpx.HTTPStatusError as e:
            logger.error(f"FIRMS API error: {e.response.status_code} — {e.response.text[:200]}")
            return []
        except Exception as e:
            logger.error(f"FIRMS fetch failed: {e}")
            return []

    def fetch_and_filter(
        self,
        min_confidence: str = "nominal",
        days: int = 7,
    ) -> list[dict[str, Any]]:
        """
        Fetch fires and filter by confidence level.

        VIIRS confidence levels: 'low', 'nominal', 'high'
        """
        records = self.fetch(days=days)

        confidence_order = {"low": 0, "nominal": 1, "high": 2}
        min_level = confidence_order.get(min_confidence, 1)

        filtered = [
            r for r in records
            if confidence_order.get(str(r.get("confidence", "")).lower(), 0) >= min_level
        ]

        logger.info(
            f"FIRMS: {len(filtered)}/{len(records)} records after confidence filter (>= {min_confidence})."
        )
        return filtered
