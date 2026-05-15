from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    # API Keys
    firms_api_key: str = ""

    # Database
    database_url: str = "sqlite:///./data/ecosystem_monitor.db"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True

    # CORS
    frontend_url: str = "http://localhost:5173"

    # Default region (can be overridden per request)
    default_region: str = "western_ghats"

    # Legacy Western Ghats bounding box (kept for backward compat)
    wg_bbox_west: float = 72.5
    wg_bbox_south: float = 8.0
    wg_bbox_east: float = 78.5
    wg_bbox_north: float = 21.5

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    @property
    def wg_bbox(self) -> tuple:
        return (self.wg_bbox_west, self.wg_bbox_south, self.wg_bbox_east, self.wg_bbox_north)

    @property
    def wg_bbox_str(self) -> str:
        """FIRMS format: W,S,E,N"""
        return f"{self.wg_bbox_west},{self.wg_bbox_south},{self.wg_bbox_east},{self.wg_bbox_north}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
