from abc import ABC, abstractmethod
from typing import Any


class DataConnector(ABC):
    """Base class for all data source connectors."""

    @abstractmethod
    def fetch(self, bbox: tuple, start_date: str, end_date: str) -> list[dict[str, Any]]:
        """
        Fetch data for a given bounding box and date range.

        Args:
            bbox: (west, south, east, north) in decimal degrees
            start_date: ISO date string (YYYY-MM-DD)
            end_date: ISO date string (YYYY-MM-DD)

        Returns:
            List of records as dictionaries
        """
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        """Return the name of this data source."""
        pass
