"""
SQLAlchemy ORM schemas for The Great GASPI
Maps PostGIS database tables to Python models
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, BigInteger, DateTime, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from datetime import datetime

Base = declarative_base()


# ============================================================================
# CORE TERRITORY ENTITY
# ============================================================================

class Territory(Base):
    """Core territory entity with boundary geometry"""
    __tablename__ = "territories"

    id = Column(Integer, primary_key=True)
    territory_id = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    iso_code = Column(String(3))
    controlling_entity = Column(String(255))
    population = Column(BigInteger)
    total_area_sqkm = Column(Float)
    accessible_area_sqkm = Column(Float)
    area_ratio_accessible = Column(Float)
    geom = Column(Geometry("MultiPolygon", srid=4326), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    topographic_data = relationship("TopographicData", back_populates="territory", uselist=False)
    hydrology_data = relationship("HydrologyData", back_populates="territory", uselist=False)
    infrastructure_data = relationship("InfrastructureData", back_populates="territory", uselist=False)
    legal_friction_data = relationship("LegalFrictionData", back_populates="territory", uselist=False)
    sovereignty_scores = relationship("SovereigntyScore", back_populates="territory", uselist=False)
    population_density_pockets = relationship("PopulationDensityPocket", back_populates="territory")
    physical_barriers = relationship("PhysicalBarrier", back_populates="territory")
    river_basins = relationship("RiverBasin", back_populates="territory")
    border_checkpoints = relationship("BorderCheckpoint", back_populates="territory")
    legal_statutes = relationship("LegalStatute", back_populates="territory")
    spatial_features = relationship("SpatialFeature", back_populates="territory")
    data_lineage = relationship("DataLineage", back_populates="territory")


# ============================================================================
# PILLAR 1: TOPOGRAPHIC & PHYSICAL GEOGRAPHY
# ============================================================================

class TopographicData(Base):
    """Pillar 1: Topographic asymmetry metrics"""
    __tablename__ = "topographic_data"

    id = Column(Integer, primary_key=True)
    territory_id = Column(Integer, ForeignKey("territories.id", ondelete="CASCADE"), index=True, nullable=False)

    # Asymmetry metrics
    asymmetry_factor_AF = Column(Float)
    transverse_symmetry_T = Column(Float)
    basin_elongation_Eb = Column(Float)
    valley_floor_ratio_Vf = Column(Float)
    tectonic_activity_level = Column(String(50))  # low|moderate|high

    # High-ground advantage
    elevation_advantage_m = Column(Float)
    viewshed_coverage_pct = Column(Float)
    chokepoints_controlled = Column(Integer)
    high_ground_advantage_rating = Column(Float)

    # Demographics
    total_population = Column(BigInteger)
    non_citizen_population = Column(BigInteger)
    population_density_per_sqkm = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    territory = relationship("Territory", back_populates="topographic_data")


class PopulationDensityPocket(Base):
    """Population concentration areas"""
    __tablename__ = "population_density_pockets"

    id = Column(Integer, primary_key=True)
    territory_id = Column(Integer, ForeignKey("territories.id", ondelete="CASCADE"), index=True, nullable=False)
    name = Column(String(255))
    density_per_sqkm = Column(Float, nullable=False)
    population = Column(Integer)
    geom = Column(Geometry("Point", srid=4326), index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    territory = relationship("Territory", back_populates="population_density_pockets")


class PhysicalBarrier(Base):
    """Natural and artificial barriers"""
    __tablename__ = "physical_barriers"

    id = Column(Integer, primary_key=True)
    territory_id = Column(Integer, ForeignKey("territories.id", ondelete="CASCADE"), index=True, nullable=False)
    type = Column(String(50))  # natural|manmade
    description = Column(Text)
    length_km = Column(Float)
    impact_score = Column(Float)  # 0-1
    geom = Column(Geometry("LineString", srid=4326))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    territory = relationship("Territory", back_populates="physical_barriers")


# ============================================================================
# PILLAR 2: HYDROPOLITICS & RESOURCE CONTROL
# ============================================================================

class HydrologyData(Base):
    """Pillar 2: Water and resource control metrics"""
    __tablename__ = "hydrology_data"

    id = Column(Integer, primary_key=True)
    territory_id = Column(Integer, ForeignKey("territories.id", ondelete="CASCADE"), index=True, nullable=False)

    # Water basin positioning
    upstream_sovereign_control = Column(Boolean)
    downstream_dependent_status = Column(Boolean)
    shared_river_basins = Column(Integer)
    shared_aquifers = Column(Integer)

    # Water infrastructure
    dam_count = Column(Integer)
    dam_control_ratio = Column(Float)
    groundwater_pumping_quota_km3 = Column(Float)
    water_shutoff_levers = Column(Integer)
    desalination_capacity_km3_daily = Column(Float)

    # Agricultural vulnerability
    arable_land_pct = Column(Float)
    local_crop_production_metric = Column(Float)
    food_import_dependency_pct = Column(Float)

    # Composite scores
    water_security_score = Column(Float)
    agricultural_autonomy_score = Column(Float)
    resource_security_composite = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    territory = relationship("Territory", back_populates="hydrology_data")


class RiverBasin(Base):
    """Shared river basin data"""
    __tablename__ = "river_basins"

    id = Column(Integer, primary_key=True)
    territory_id = Column(Integer, ForeignKey("territories.id", ondelete="CASCADE"), index=True, nullable=False)
    river_name = Column(String(255))
    upstream_position = Column(Boolean)
    downstream_dependence = Column(Boolean)
    flow_direction = Column(String(50))
    average_discharge_m3_s = Column(Float)
    geom = Column(Geometry("LineString", srid=4326))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    territory = relationship("Territory", back_populates="river_basins")


# ============================================================================
# PILLAR 3: INFRASTRUCTURE & ECONOMIC LEVERS
# ============================================================================

class InfrastructureData(Base):
    """Pillar 3: Infrastructure and economic control"""
    __tablename__ = "infrastructure_data"

    id = Column(Integer, primary_key=True)
    territory_id = Column(Integer, ForeignKey("territories.id", ondelete="CASCADE"), index=True, nullable=False)

    # Airspace & spectrum
    airspace_control_ratio = Column(Float)
    cellular_bands_controlled = Column(Integer)
    frequency_spectrum_mhz = Column(String(255))

    # Maritime
    eez_claimed_sqkm = Column(Float)
    eez_accessible_sqkm = Column(Float)
    major_ports_count = Column(Integer)
    port_access_ratio = Column(Float)

    # Borders & mobility
    border_checkpoint_density_per_km = Column(Float)
    permit_regime_restrictiveness = Column(Integer)  # 1-10
    transit_permit_required = Column(Boolean)

    # Currency & fiscal
    official_currency = Column(String(10))
    local_currency_circulation = Column(Boolean)
    currency_control_ratio = Column(Float)

    # Energy
    power_grid_self_sufficiency_pct = Column(Float)
    fuel_import_dependency_pct = Column(Float)

    # Composite score
    infrastructural_control_score = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    territory = relationship("Territory", back_populates="infrastructure_data")


class BorderCheckpoint(Base):
    """Border crossing infrastructure"""
    __tablename__ = "border_checkpoints"

    id = Column(Integer, primary_key=True)
    territory_id = Column(Integer, ForeignKey("territories.id", ondelete="CASCADE"), index=True, nullable=False)
    name = Column(String(255))
    checkpoint_type = Column(String(50))  # land|air|sea
    control_status = Column(String(50))  # external|shared|local
    permit_requirement = Column(Boolean)
    geom = Column(Geometry("Point", srid=4326))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    territory = relationship("Territory", back_populates="border_checkpoints")


# ============================================================================
# PILLAR 4: LEGAL-CULTURAL FRICTION & GOVERNANCE DIVERGENCE
# ============================================================================

class LegalFrictionData(Base):
    """Pillar 4: Legal-cultural friction metrics"""
    __tablename__ = "legal_friction_data"

    id = Column(Integer, primary_key=True)
    territory_id = Column(Integer, ForeignKey("territories.id", ondelete="CASCADE"), index=True, nullable=False)

    # Enforced legal system
    enforced_system_name = Column(String(255))
    enforced_system_source = Column(String(50))  # military|occupation|foreign
    enforced_jurisdiction = Column(Text)

    # Preferred local system
    preferred_system_name = Column(String(255))
    preferred_system_source = Column(String(50))  # customary|religious|secular|hybrid
    preferred_jurisdiction = Column(Text)

    # Statutory divergence (1-10 scale)
    family_law_divergence = Column(Integer)
    criminal_law_divergence = Column(Integer)
    commercial_law_divergence = Column(Integer)
    personal_status_divergence = Column(Integer)

    # Friction metrics
    legal_friction_density = Column(Float)  # 0-100
    jurisdictional_autonomy_score = Column(Float)  # 0-100
    population_under_external_law = Column(BigInteger)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    territory = relationship("Territory", back_populates="legal_friction_data")


class LegalStatute(Base):
    """Individual statutory conflicts"""
    __tablename__ = "legal_statutes"

    id = Column(Integer, primary_key=True)
    territory_id = Column(Integer, ForeignKey("territories.id", ondelete="CASCADE"), index=True, nullable=False)
    statute_type = Column(String(50))  # family|criminal|commercial|military
    enforcing_entity = Column(String(255))
    local_preference = Column(String(255))
    conflict_severity = Column(Integer)  # 1-10
    url_reference = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    territory = relationship("Territory", back_populates="legal_statutes")


# ============================================================================
# COMPOSITE SCORING
# ============================================================================

class SovereigntyScore(Base):
    """Composite GASPI Sovereignty Index"""
    __tablename__ = "sovereignty_scores"

    id = Column(Integer, primary_key=True)
    territory_id = Column(Integer, ForeignKey("territories.id", ondelete="CASCADE"), index=True, nullable=False)

    # Sub-index scores (0-100)
    jurisdictional_autonomy_score = Column(Float)
    resource_security_score = Column(Float)
    infrastructural_control_score = Column(Float)

    # Composite index (0-100)
    composite_sovereignty_index = Column(Float)

    # Component breakdown
    topographic_component = Column(Float)
    hydrology_component = Column(Float)
    infrastructure_component = Column(Float)
    legal_component = Column(Float)

    # Metadata
    calculation_date = Column(DateTime)
    data_confidence_level = Column(String(50))  # high|medium|low
    notes = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    territory = relationship("Territory", back_populates="sovereignty_scores")


# ============================================================================
# DATA LINEAGE & ATTRIBUTION
# ============================================================================

class DataSource(Base):
    """Data source registry with attribution"""
    __tablename__ = "data_sources"

    id = Column(Integer, primary_key=True)
    source_name = Column(String(255), unique=True, nullable=False)
    url = Column(Text)
    api_endpoint = Column(Text)
    license_type = Column(String(50))  # CC BY 4.0, MIT, etc.
    attribution_text = Column(Text)
    last_updated = Column(DateTime)
    update_frequency = Column(String(50))  # daily|weekly|monthly|yearly
    data_format = Column(String(50))  # geojson|raster|csv|api
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    data_lineage = relationship("DataLineage", back_populates="source")


class DataLineage(Base):
    """Track which sources contributed to each territory"""
    __tablename__ = "data_lineage"

    id = Column(Integer, primary_key=True)
    territory_id = Column(Integer, ForeignKey("territories.id", ondelete="CASCADE"), index=True, nullable=False)
    source_id = Column(Integer, ForeignKey("data_sources.id", ondelete="RESTRICT"), nullable=False)
    data_type = Column(String(50))  # topographic|hydrology|demographic|infrastructure|legal
    ingestion_date = Column(DateTime)
    data_version = Column(String(50))
    record_count = Column(Integer)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    territory = relationship("Territory", back_populates="data_lineage")
    source = relationship("DataSource", back_populates="data_lineage")


# ============================================================================
# SPATIAL FEATURES (For Frontend Rendering)
# ============================================================================

class SpatialFeature(Base):
    """GeoJSON features for map visualization"""
    __tablename__ = "spatial_features"

    id = Column(Integer, primary_key=True)
    territory_id = Column(Integer, ForeignKey("territories.id", ondelete="CASCADE"), index=True, nullable=False)
    feature_type = Column(String(50))  # accessible_area|restricted_area|high_ground|barrier
    access_status = Column(String(50))  # accessible|restricted|disputed
    elevation_m = Column(Float)
    geom = Column(Geometry("Polygon", srid=4326), index=True)
    properties = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    territory = relationship("Territory", back_populates="spatial_features")
