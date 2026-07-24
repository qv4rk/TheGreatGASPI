-- The Great GASPI: Initial PostGIS Schema
-- PostgreSQL + PostGIS database initialization
-- Run this after: psql -U gsapi -d gsapi -f migrations/001_init_schema.sql

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- ============================================================================
-- TERRITORY & METADATA TABLES
-- ============================================================================

CREATE TABLE IF NOT EXISTS territories (
    id SERIAL PRIMARY KEY,
    territory_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    iso_code VARCHAR(3),
    controlling_entity VARCHAR(255),
    population BIGINT,
    total_area_sqkm FLOAT,
    accessible_area_sqkm FLOAT,
    area_ratio_accessible FLOAT,
    geom GEOMETRY(MultiPolygon, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_territories_territory_id ON territories(territory_id);
CREATE INDEX idx_territories_geom ON territories USING GIST(geom);

-- ============================================================================
-- PILLAR 1: TOPOGRAPHIC & PHYSICAL GEOGRAPHY
-- ============================================================================

CREATE TABLE IF NOT EXISTS topographic_data (
    id SERIAL PRIMARY KEY,
    territory_id INTEGER NOT NULL REFERENCES territories(id) ON DELETE CASCADE,

    -- Asymmetry Metrics
    asymmetry_factor_AF FLOAT,          -- AF = (Ar / At) * 100
    transverse_symmetry_T FLOAT,        -- T = Da / Dd
    basin_elongation_Eb FLOAT,          -- Basin shape indicator
    valley_floor_ratio_Vf FLOAT,        -- V-shaped valley indicator
    tectonic_activity_level VARCHAR(50),-- low|moderate|high

    -- High-Ground Advantage
    elevation_advantage_m FLOAT,        -- Relative elevation gain
    viewshed_coverage_pct FLOAT,        -- % of territory visible from high points
    chokepoints_controlled INT,         -- Number of strategic bottlenecks
    high_ground_advantage_rating FLOAT, -- 0-1 scale

    -- Demographics & Accessibility
    total_population BIGINT,
    non_citizen_population BIGINT,
    population_density_per_sqkm FLOAT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_topographic_territory ON topographic_data(territory_id);

CREATE TABLE IF NOT EXISTS population_density_pockets (
    id SERIAL PRIMARY KEY,
    territory_id INTEGER NOT NULL REFERENCES territories(id) ON DELETE CASCADE,
    name VARCHAR(255),
    density_per_sqkm FLOAT NOT NULL,
    population INT,
    geom GEOMETRY(Point, 4326) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_density_territory ON population_density_pockets(territory_id);
CREATE INDEX idx_density_geom ON population_density_pockets USING GIST(geom);

CREATE TABLE IF NOT EXISTS physical_barriers (
    id SERIAL PRIMARY KEY,
    territory_id INTEGER NOT NULL REFERENCES territories(id) ON DELETE CASCADE,
    type VARCHAR(50),               -- natural|manmade
    description TEXT,
    length_km FLOAT,
    impact_score FLOAT,             -- 0-1 scale
    geom GEOMETRY(LineString, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_barriers_territory ON physical_barriers(territory_id);

-- ============================================================================
-- PILLAR 2: HYDROPOLITICS & RESOURCE CONTROL
-- ============================================================================

CREATE TABLE IF NOT EXISTS hydrology_data (
    id SERIAL PRIMARY KEY,
    territory_id INTEGER NOT NULL REFERENCES territories(id) ON DELETE CASCADE,

    -- Water Basin Positioning
    upstream_sovereign_control BOOLEAN,
    downstream_dependent_status BOOLEAN,
    shared_river_basins INT,
    shared_aquifers INT,

    -- Water Infrastructure Control
    dam_count INT,
    dam_control_ratio FLOAT,        -- % of dams under external control
    groundwater_pumping_quota_km3 FLOAT,
    water_shutoff_levers INT,
    desalination_capacity_km3_daily FLOAT,

    -- Agricultural Vulnerability
    arable_land_pct FLOAT,
    local_crop_production_metric FLOAT,
    food_import_dependency_pct FLOAT,

    -- Resource Security Score Component
    water_security_score FLOAT,
    agricultural_autonomy_score FLOAT,
    resource_security_composite FLOAT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_hydrology_territory ON hydrology_data(territory_id);

CREATE TABLE IF NOT EXISTS river_basins (
    id SERIAL PRIMARY KEY,
    territory_id INTEGER NOT NULL REFERENCES territories(id) ON DELETE CASCADE,
    river_name VARCHAR(255),
    upstream_position BOOLEAN,         -- TRUE = upstream control
    downstream_dependence BOOLEAN,
    flow_direction VARCHAR(50),
    average_discharge_m3_s FLOAT,
    geom GEOMETRY(LineString, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_rivers_territory ON river_basins(territory_id);

-- ============================================================================
-- PILLAR 3: INFRASTRUCTURE & ECONOMIC LEVERS
-- ============================================================================

CREATE TABLE IF NOT EXISTS infrastructure_data (
    id SERIAL PRIMARY KEY,
    territory_id INTEGER NOT NULL REFERENCES territories(id) ON DELETE CASCADE,

    -- Airspace & Spectrum Control
    airspace_control_ratio FLOAT,       -- % under external control
    cellular_bands_controlled INT,      -- Number of spectrum bands
    frequency_spectrum_mhz TEXT,        -- e.g., "800-900 MHz, 2.1-2.2 GHz"

    -- Maritime Sovereignty
    eez_claimed_sqkm FLOAT,
    eez_accessible_sqkm FLOAT,
    major_ports_count INT,
    port_access_ratio FLOAT,

    -- Border & Mobility
    border_checkpoint_density_per_km FLOAT,
    permit_regime_restrictiveness INT,  -- 1-10 scale
    transit_permit_required BOOLEAN,

    -- Currency & Fiscal
    official_currency VARCHAR(10),
    local_currency_circulation BOOLEAN,
    currency_control_ratio FLOAT,       -- % of transactions in imposed currency

    -- Utility Grids
    power_grid_self_sufficiency_pct FLOAT,
    fuel_import_dependency_pct FLOAT,

    -- Composite Score
    infrastructural_control_score FLOAT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_infrastructure_territory ON infrastructure_data(territory_id);

CREATE TABLE IF NOT EXISTS border_checkpoints (
    id SERIAL PRIMARY KEY,
    territory_id INTEGER NOT NULL REFERENCES territories(id) ON DELETE CASCADE,
    name VARCHAR(255),
    checkpoint_type VARCHAR(50),        -- land|air|sea
    control_status VARCHAR(50),         -- external|shared|local
    permit_requirement BOOLEAN,
    geom GEOMETRY(Point, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_checkpoints_territory ON border_checkpoints(territory_id);

-- ============================================================================
-- PILLAR 4: LEGAL-CULTURAL FRICTION & GOVERNANCE DIVERGENCE
-- ============================================================================

CREATE TABLE IF NOT EXISTS legal_friction_data (
    id SERIAL PRIMARY KEY,
    territory_id INTEGER NOT NULL REFERENCES territories(id) ON DELETE CASCADE,

    -- Enforced Legal System
    enforced_system_name VARCHAR(255),
    enforced_system_source VARCHAR(50),  -- military|occupation|foreign
    enforced_jurisdiction TEXT,

    -- Preferred Local System
    preferred_system_name VARCHAR(255),
    preferred_system_source VARCHAR(50), -- customary|religious|secular|hybrid
    preferred_jurisdiction TEXT,

    -- Statutory Conflict Mapping
    family_law_divergence INT,          -- 1-10 scale
    criminal_law_divergence INT,
    commercial_law_divergence INT,
    personal_status_divergence INT,

    -- Friction Density & Metrics
    legal_friction_density FLOAT,       -- Normalized 0-100
    jurisdictional_autonomy_score FLOAT,-- 0-100 scale

    -- Population Affected
    population_under_external_law BIGINT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_legal_friction_territory ON legal_friction_data(territory_id);

CREATE TABLE IF NOT EXISTS legal_statutes (
    id SERIAL PRIMARY KEY,
    territory_id INTEGER NOT NULL REFERENCES territories(id) ON DELETE CASCADE,
    statute_type VARCHAR(50),           -- family|criminal|commercial|military
    enforcing_entity VARCHAR(255),
    local_preference VARCHAR(255),
    conflict_severity INT,              -- 1-10 scale
    url_reference TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_statutes_territory ON legal_statutes(territory_id);

-- ============================================================================
-- COMPOSITE SCORING & SOVEREIGNTY INDEX
-- ============================================================================

CREATE TABLE IF NOT EXISTS sovereignty_scores (
    id SERIAL PRIMARY KEY,
    territory_id INTEGER NOT NULL REFERENCES territories(id) ON DELETE CASCADE,

    -- Sub-Index Scores (0-100)
    jurisdictional_autonomy_score FLOAT,
    resource_security_score FLOAT,
    infrastructural_control_score FLOAT,

    -- Composite GASPI Index (0-100)
    composite_sovereignty_index FLOAT,

    -- Breakdown Components
    topographic_component FLOAT,
    hydrology_component FLOAT,
    infrastructure_component FLOAT,
    legal_component FLOAT,

    -- Metadata
    calculation_date TIMESTAMP,
    data_confidence_level VARCHAR(50),  -- high|medium|low
    notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_scores_territory ON sovereignty_scores(territory_id);

-- ============================================================================
-- DATA LINEAGE & ATTRIBUTION
-- ============================================================================

CREATE TABLE IF NOT EXISTS data_sources (
    id SERIAL PRIMARY KEY,
    source_name VARCHAR(255) NOT NULL UNIQUE,
    url TEXT,
    api_endpoint TEXT,
    license_type VARCHAR(50),           -- CC BY 4.0, MIT, etc.
    attribution_text TEXT,
    last_updated TIMESTAMP,
    update_frequency VARCHAR(50),       -- daily|weekly|monthly|yearly
    data_format VARCHAR(50),            -- geojson|raster|csv|api
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS data_lineage (
    id SERIAL PRIMARY KEY,
    territory_id INTEGER NOT NULL REFERENCES territories(id) ON DELETE CASCADE,
    source_id INTEGER NOT NULL REFERENCES data_sources(id) ON DELETE RESTRICT,
    data_type VARCHAR(50),              -- topographic|hydrology|demographic|infrastructure|legal
    ingestion_date TIMESTAMP,
    data_version VARCHAR(50),
    record_count INT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_lineage_territory ON data_lineage(territory_id);

-- ============================================================================
-- SPATIAL FEATURES (For Frontend Rendering)
-- ============================================================================

CREATE TABLE IF NOT EXISTS spatial_features (
    id SERIAL PRIMARY KEY,
    territory_id INTEGER NOT NULL REFERENCES territories(id) ON DELETE CASCADE,
    feature_type VARCHAR(50),           -- accessible_area|restricted_area|high_ground|barrier
    access_status VARCHAR(50),          -- accessible|restricted|disputed
    elevation_m FLOAT,
    geom GEOMETRY(Polygon, 4326),
    properties JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_features_territory ON spatial_features(territory_id);
CREATE INDEX idx_features_geom ON spatial_features USING GIST(geom);

-- ============================================================================
-- VIEW: Composite Territory Profile (for API serialization)
-- ============================================================================

CREATE OR REPLACE VIEW territory_profiles AS
SELECT
    t.id,
    t.territory_id,
    t.name,
    t.controlling_entity,
    t.population,
    t.total_area_sqkm,
    t.accessible_area_sqkm,
    t.area_ratio_accessible,
    ST_AsGeoJSON(t.geom) as geom_geojson,
    td.asymmetry_factor_AF,
    td.transverse_symmetry_T,
    td.valley_floor_ratio_Vf,
    td.high_ground_advantage_rating,
    hd.resource_security_composite,
    id.infrastructural_control_score,
    lf.jurisdictional_autonomy_score,
    ss.composite_sovereignty_index
FROM territories t
LEFT JOIN topographic_data td ON t.id = td.territory_id
LEFT JOIN hydrology_data hd ON t.id = hd.territory_id
LEFT JOIN infrastructure_data id ON t.id = id.territory_id
LEFT JOIN legal_friction_data lf ON t.id = lf.territory_id
LEFT JOIN sovereignty_scores ss ON t.id = ss.territory_id;

-- ============================================================================
-- Grant permissions (adjust as needed for your deployment)
-- ============================================================================

GRANT USAGE ON SCHEMA public TO gsapi;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO gsapi;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO gsapi;
