"""Configuration settings for The Great GASPI Backend"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database
    database_url: str = "postgresql://gsapi:gsapi_dev_password@postgres:5432/gsapi"
    database_pool_size: int = 20
    database_max_overflow: int = 10

    # API
    api_title: str = "The Great GASPI"
    api_version: str = "0.1.0"
    api_description: str = "Global Asymmetric Sovereignty & Power Index"

    # CORS
    cors_origins: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Feature flags
    debug_mode: bool = False
    enable_demo_data: bool = True

    # Data sources
    hydrosheds_api_url: str = "https://www.hydrosheds.org/"
    worldpop_api_url: str = "https://www.worldpop.org/api/"
    faostat_api_url: str = "https://www.fao.org/faostat/"
    courtlistener_api_url: str = "https://www.courtlistener.com/api/"
    openstreetmap_api_url: str = "https://overpass-api.de/api/"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
