"""Database and Pydantic models for The Great GSAPI"""

from pydantic import BaseModel
from typing import Optional


class SovereigntyScoreResponse(BaseModel):
    """Sovereignty score for a territory"""

    territory_id: str
    territory_name: str
    jurisdictional_autonomy: float
    resource_security: float
    infrastructural_control: float
    composite_score: float


class TerritoryResponse(BaseModel):
    """Territory metadata"""

    id: str
    name: str
    area_km2: float
    population: Optional[int] = None
    controlling_entity: Optional[str] = None


class DataSourceResponse(BaseModel):
    """Attribution and metadata for a data source"""

    name: str
    url: str
    license: str
    last_updated: str
    attribution: str
