"""Pydantic models for The Great GASPI FastAPI"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class TectonicActivityLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


class AccessStatus(str, Enum):
    ACCESSIBLE = "accessible"
    RESTRICTED = "restricted"
    DISPUTED = "disputed"


class DataConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# ============================================================================
# PILLAR 1: TOPOGRAPHIC & PHYSICAL GEOGRAPHY
# ============================================================================

class TopographicAsymmetryMetrics(BaseModel):
    """Pillar 1: Topographic asymmetry and high-ground advantage metrics"""

    asymmetry_factor_AF: float = Field(..., description="Basin asymmetry: AF = (Ar/At)*100")
    transverse_symmetry_T: float = Field(..., description="Lateral symmetry: T = Da/Dd")
    basin_elongation_Eb: float = Field(..., description="Basin shape indicator")
    valley_floor_ratio_Vf: float = Field(..., description="V-shaped valley indicator")
    tectonic_activity_level: TectonicActivityLevel

    elevation_advantage_m: float = Field(..., description="Meters of relative elevation")
    viewshed_coverage_pct: float = Field(..., description="% of territory visible from high points")
    chokepoints_controlled: int = Field(..., description="Number of strategic bottlenecks")
    high_ground_advantage_rating: float = Field(..., ge=0, le=1, description="Normalized 0-1 scale")


class PopulationDensityPocket(BaseModel):
    """Population concentration area"""

    name: str
    lat: float
    lng: float
    density: float = Field(..., description="Population per km²")
    population: Optional[int] = None


class PhysicalBarrier(BaseModel):
    """Natural or artificial barrier"""

    type: str = Field(..., description="natural|manmade")
    description: str
    length_km: float
    impact_score: float = Field(..., ge=0, le=1, description="Normalized impact 0-1")


# ============================================================================
# PILLAR 2: HYDROPOLITICS & RESOURCE CONTROL
# ============================================================================

class HydrologyData(BaseModel):
    """Pillar 2: Water and resource control metrics"""

    upstream_sovereign_control: bool
    downstream_dependent_status: bool
    shared_river_basins: int
    shared_aquifers: int

    dam_count: int
    dam_control_ratio: float = Field(..., description="% of dams under external control")
    groundwater_pumping_quota_km3: float
    water_shutoff_levers: int
    desalination_capacity_km3_daily: float

    arable_land_pct: float
    local_crop_production_metric: float
    food_import_dependency_pct: float

    water_security_score: float = Field(..., ge=0, le=100)
    agricultural_autonomy_score: float = Field(..., ge=0, le=100)
    resource_security_composite: float = Field(..., ge=0, le=100)


class RiverBasin(BaseModel):
    """Shared river basin data"""

    river_name: str
    upstream_position: bool
    downstream_dependence: bool
    flow_direction: str
    average_discharge_m3_s: float


# ============================================================================
# PILLAR 3: INFRASTRUCTURE & ECONOMIC LEVERS
# ============================================================================

class InfrastructureData(BaseModel):
    """Pillar 3: Infrastructure and economic control metrics"""

    airspace_control_ratio: float = Field(..., description="% under external control")
    cellular_bands_controlled: int
    frequency_spectrum_mhz: str

    eez_claimed_sqkm: float
    eez_accessible_sqkm: float
    major_ports_count: int
    port_access_ratio: float

    border_checkpoint_density_per_km: float
    permit_regime_restrictiveness: int = Field(..., ge=1, le=10)
    transit_permit_required: bool

    official_currency: str
    local_currency_circulation: bool
    currency_control_ratio: float

    power_grid_self_sufficiency_pct: float
    fuel_import_dependency_pct: float

    infrastructural_control_score: float = Field(..., ge=0, le=100)


class BorderCheckpoint(BaseModel):
    """Border crossing infrastructure"""

    name: str
    checkpoint_type: str = Field(..., description="land|air|sea")
    control_status: str = Field(..., description="external|shared|local")
    permit_requirement: bool
    lat: float
    lng: float


# ============================================================================
# PILLAR 4: LEGAL-CULTURAL FRICTION
# ============================================================================

class LegalFrictionData(BaseModel):
    """Pillar 4: Legal-cultural divergence metrics"""

    enforced_system_name: str
    enforced_system_source: str = Field(..., description="military|occupation|foreign")
    enforced_jurisdiction: str

    preferred_system_name: str
    preferred_system_source: str = Field(..., description="customary|religious|secular|hybrid")
    preferred_jurisdiction: str

    family_law_divergence: int = Field(..., ge=1, le=10)
    criminal_law_divergence: int = Field(..., ge=1, le=10)
    commercial_law_divergence: int = Field(..., ge=1, le=10)
    personal_status_divergence: int = Field(..., ge=1, le=10)

    legal_friction_density: float = Field(..., ge=0, le=100)
    jurisdictional_autonomy_score: float = Field(..., ge=0, le=100)
    population_under_external_law: int


# ============================================================================
# COMPOSITE SCORING
# ============================================================================

class SovereigntyScores(BaseModel):
    """Composite GASPI Sovereignty Index scores"""

    jurisdictional_autonomy_score: float = Field(..., ge=0, le=100)
    resource_security_score: float = Field(..., ge=0, le=100)
    infrastructural_control_score: float = Field(..., ge=0, le=100)

    composite_sovereignty_index: float = Field(..., ge=0, le=100, description="Final GASPI Index")

    topographic_component: float = Field(..., ge=0, le=100)
    hydrology_component: float = Field(..., ge=0, le=100)
    infrastructure_component: float = Field(..., ge=0, le=100)
    legal_component: float = Field(..., ge=0, le=100)

    calculation_date: datetime
    data_confidence_level: DataConfidenceLevel


# ============================================================================
# SPATIAL FEATURES (For Map Rendering)
# ============================================================================

class SpatialFeature(BaseModel):
    """GeoJSON feature for frontend visualization"""

    feature_type: str = Field(..., description="accessible_area|restricted_area|high_ground|barrier")
    access_status: AccessStatus
    elevation_m: Optional[float] = None
    geometry: dict = Field(..., description="GeoJSON geometry object")
    properties: dict


# ============================================================================
# TERRITORY PROFILE (Composite Response)
# ============================================================================

class TerritoryProfile(BaseModel):
    """Complete territory profile for frontend dashboard"""

    territory: dict = Field(..., description="Territory metadata")
    topographic_asymmetry: TopographicAsymmetryMetrics
    hydrology: HydrologyData
    infrastructure: InfrastructureData
    legal_friction: LegalFrictionData
    scores: SovereigntyScores

    high_ground_peaks: List[dict] = Field(default_factory=list, description="High-ground markers")
    density_pockets: List[PopulationDensityPocket] = Field(default_factory=list)
    spatial_features: dict = Field(..., description="GeoJSON FeatureCollection for map")


# ============================================================================
# DATA ATTRIBUTION
# ============================================================================

class DataSource(BaseModel):
    """Data source attribution and metadata"""

    name: str
    url: str
    license_type: str
    attribution_text: str
    last_updated: datetime
    update_frequency: str
    data_format: str


# ============================================================================
# API RESPONSES
# ============================================================================

class HealthResponse(BaseModel):
    """Health check response"""

    status: str = "healthy"
    service: str = "gasapi-backend"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """Error response"""

    detail: str
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
