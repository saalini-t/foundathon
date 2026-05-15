"""
GBIF (Global Biodiversity Information Facility) connector.

Fetches species occurrence records for a biodiversity region.
API docs: https://www.gbif.org/developer/summary
"""

import logging
from typing import Any

import httpx

from backend.config import get_settings
from backend.connectors.base import DataConnector
from backend.regions import get_region

logger = logging.getLogger(__name__)

GBIF_OCCURRENCE_URL = "https://api.gbif.org/v1/occurrence/search"
GBIF_SPECIES_URL = "https://api.gbif.org/v1/species"


class GBIFConnector(DataConnector):
    """Connector for GBIF biodiversity occurrence data."""

    def __init__(self, region_id: str | None = None):
        self.settings = get_settings()
        self._region = get_region(region_id)

    def get_source_name(self) -> str:
        return "GBIF"

    def fetch(
        self,
        bbox: tuple | None = None,
        start_date: str = "",
        end_date: str = "",
        limit: int = 300,
        offset: int = 0,
        taxon_key: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Fetch species occurrence records for the active region.

        Args:
            bbox: (west, south, east, north). Defaults to region bbox.
            start_date: ISO date for filtering by event date.
            end_date: ISO date for filtering by event date.
            limit: Max records per request (GBIF max: 300).
            offset: Pagination offset.
            taxon_key: Optional GBIF taxon key to filter by taxonomic group.

        Returns:
            List of occurrence records.
        """
        if bbox is None:
            bbox = self._region.bbox

        # GBIF uses "decimalLatitude" and "decimalLongitude" range filters
        params: dict[str, Any] = {
            "decimalLatitude": f"{bbox[1]},{bbox[3]}",
            "decimalLongitude": f"{bbox[0]},{bbox[2]}",
            "hasCoordinate": "true",
            "hasGeospatialIssue": "false",
            "limit": min(limit, 300),
            "offset": offset,
        }

        # Filter by country — GBIF expects single country code
        if len(self._region.country_codes) == 1:
            params["country"] = self._region.country_codes[0]

        if start_date:
            params["eventDate"] = f"{start_date},{end_date}" if end_date else start_date

        if taxon_key:
            params["taxonKey"] = taxon_key

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.get(GBIF_OCCURRENCE_URL, params=params)
                response.raise_for_status()

            data = response.json()
            results = data.get("results", [])
            total = data.get("count", 0)

            records = []
            for r in results:
                records.append({
                    "gbif_id": r.get("key"),
                    "species": r.get("species", r.get("scientificName", "Unknown")),
                    "genus": r.get("genus"),
                    "family": r.get("family"),
                    "order": r.get("order"),
                    "class_name": r.get("class"),
                    "phylum": r.get("phylum"),
                    "kingdom": r.get("kingdom"),
                    "latitude": r.get("decimalLatitude"),
                    "longitude": r.get("decimalLongitude"),
                    "event_date": r.get("eventDate"),
                    "basis_of_record": r.get("basisOfRecord"),
                    "country": r.get("country"),
                    "state_province": r.get("stateProvince"),
                    "coordinate_uncertainty": r.get("coordinateUncertaintyInMeters"),
                })

            logger.info(
                f"GBIF: fetched {len(records)} occurrences "
                f"(total available: {total})."
            )
            return records

        except httpx.HTTPStatusError as e:
            logger.error(f"GBIF API error: {e.response.status_code}")
            return []
        except Exception as e:
            logger.error(f"GBIF fetch failed: {e}")
            return []

    def fetch_multiple_pages(
        self,
        max_records: int = 2000,
        bbox: tuple | None = None,
    ) -> list[dict[str, Any]]:
        """
        Fetch multiple pages of occurrence data.

        Args:
            max_records: Maximum total records to fetch.
            bbox: Bounding box filter.

        Returns:
            Aggregated list of occurrence records.
        """
        all_records = []
        offset = 0
        page_size = 300

        while offset < max_records:
            records = self.fetch(
                bbox=bbox,
                limit=page_size,
                offset=offset,
            )
            if not records:
                break

            all_records.extend(records)
            offset += page_size

            if len(records) < page_size:
                break  # No more records

        logger.info(f"GBIF: fetched {len(all_records)} total occurrences across pages.")
        return all_records

    def get_species_summary(
        self,
        bbox: tuple | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get a summary of unique species found in the area.

        Returns list of species with occurrence count.
        """
        records = self.fetch_multiple_pages(max_records=3000, bbox=bbox)

        species_counts: dict[str, dict] = {}
        for r in records:
            sp = r.get("species")
            if not sp:
                continue
            if sp not in species_counts:
                species_counts[sp] = {
                    "species": sp,
                    "genus": r.get("genus"),
                    "family": r.get("family"),
                    "order": r.get("order"),
                    "class_name": r.get("class_name"),
                    "kingdom": r.get("kingdom"),
                    "count": 0,
                }
            species_counts[sp]["count"] += 1

        summary = sorted(species_counts.values(), key=lambda x: x["count"], reverse=True)
        logger.info(f"GBIF: found {len(summary)} unique species in area.")
        return summary
