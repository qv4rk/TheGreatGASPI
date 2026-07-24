"""
Database query implementations for The Great GASPI routes
Actual SQL queries using SQLAlchemy ORM models
"""

import logging
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
import json
from geoalchemy2.functions import ST_AsGeoJSON

from .schemas import (
    Territory, TopographicData, HydrologyData, InfrastructureData,
    LegalFrictionData, SovereigntyScore, PopulationDensityPocket,
    BorderCheckpoint, SpatialFeature, DataSource, DataLineage
)
from .models import (
    TerritoryProfile, TopographicAsymmetryMetrics, HydrologyData as HydroModel,
    InfrastructureData as InfraModel, LegalFrictionData as LegalModel,
    SovereigntyScores, PopulationDensityPocket as DensityModel,
    SpatialFeature as FeatureModel
)

logger = logging.getLogger(__name__)


# ============================================================================
# TERRITORY PROFILE QUERIES
# ============================================================================

def get_territory_by_id(db: Session, territory_id: str) -> Territory:
    """Query territory metadata by territory_id"""
    territory = db.query(Territory).filter(
        Territory.territory_id == territory_id
    ).first()

    if not territory:
        return None

    logger.info(f"Retrieved territory: {territory_id}")
    return territory


def get_territory_profile(db: Session, territory_id: str) -> dict:
    """
    Assemble complete territory profile from database
    Queries all pillars and returns composite response
    """
    # 1. Get territory metadata
    territory = get_territory_by_id(db, territory_id)
    if not territory:
        raise ValueError(f"Territory {territory_id} not found")

    # 2. Get all pillar data
    topographic = db.query(TopographicData).filter(
        TopographicData.territory_id == territory.id
    ).first()

    hydrology = db.query(HydrologyData).filter(
        HydrologyData.territory_id == territory.id
    ).first()

    infrastructure = db.query(InfrastructureData).filter(
        InfrastructureData.territory_id == territory.id
    ).first()

    legal_friction = db.query(LegalFrictionData).filter(
        LegalFrictionData.territory_id == territory.id
    ).first()

    scores = db.query(SovereigntyScore).filter(
        SovereigntyScore.territory_id == territory.id
    ).first()

    # 3. Get high-ground peaks (highest density population + elevation)
    high_ground_peaks = db.query(PopulationDensityPocket).filter(
        PopulationDensityPocket.territory_id == territory.id
    ).order_by(
        PopulationDensityPocket.density_per_sqkm.desc()
    ).limit(10).all()

    # 4. Get population density pockets
    density_pockets = db.query(PopulationDensityPocket).filter(
        PopulationDensityPocket.territory_id == territory.id
    ).all()

    # 5. Get spatial features as GeoJSON
    spatial_features_query = db.query(SpatialFeature).filter(
        SpatialFeature.territory_id == territory.id
    ).all()

    # 6. Build response objects
    profile = {
        "territory": {
            "id": territory.id,
            "territory_id": territory.territory_id,
            "name": territory.name,
            "iso_code": territory.iso_code,
            "controlling_entity": territory.controlling_entity,
            "population": territory.population,
            "total_area_sqkm": territory.total_area_sqkm,
            "accessible_area_sqkm": territory.accessible_area_sqkm,
            "area_ratio_accessible": territory.area_ratio_accessible
        },
        "topographic_asymmetry": {
            "asymmetry_factor_AF": topographic.asymmetry_factor_AF if topographic else None,
            "transverse_symmetry_T": topographic.transverse_symmetry_T if topographic else None,
            "basin_elongation_Eb": topographic.basin_elongation_Eb if topographic else None,
            "valley_floor_ratio_Vf": topographic.valley_floor_ratio_Vf if topographic else None,
            "tectonic_activity_level": topographic.tectonic_activity_level if topographic else "unknown",
            "elevation_advantage_m": topographic.elevation_advantage_m if topographic else None,
            "viewshed_coverage_pct": topographic.viewshed_coverage_pct if topographic else None,
            "chokepoints_controlled": topographic.chokepoints_controlled if topographic else None,
            "high_ground_advantage_rating": topographic.high_ground_advantage_rating if topographic else None
        },
        "hydrology": {
            "upstream_sovereign_control": hydrology.upstream_sovereign_control if hydrology else None,
            "downstream_dependent_status": hydrology.downstream_dependent_status if hydrology else None,
            "shared_river_basins": hydrology.shared_river_basins if hydrology else None,
            "dam_count": hydrology.dam_count if hydrology else None,
            "dam_control_ratio": hydrology.dam_control_ratio if hydrology else None,
            "arable_land_pct": hydrology.arable_land_pct if hydrology else None,
            "food_import_dependency_pct": hydrology.food_import_dependency_pct if hydrology else None,
            "water_security_score": hydrology.water_security_score if hydrology else None,
            "agricultural_autonomy_score": hydrology.agricultural_autonomy_score if hydrology else None,
            "resource_security_composite": hydrology.resource_security_composite if hydrology else None
        },
        "infrastructure": {
            "airspace_control_ratio": infrastructure.airspace_control_ratio if infrastructure else None,
            "cellular_bands_controlled": infrastructure.cellular_bands_controlled if infrastructure else None,
            "eez_claimed_sqkm": infrastructure.eez_claimed_sqkm if infrastructure else None,
            "major_ports_count": infrastructure.major_ports_count if infrastructure else None,
            "border_checkpoint_density_per_km": infrastructure.border_checkpoint_density_per_km if infrastructure else None,
            "permit_regime_restrictiveness": infrastructure.permit_regime_restrictiveness if infrastructure else None,
            "official_currency": infrastructure.official_currency if infrastructure else None,
            "power_grid_self_sufficiency_pct": infrastructure.power_grid_self_sufficiency_pct if infrastructure else None,
            "infrastructural_control_score": infrastructure.infrastructural_control_score if infrastructure else None
        },
        "legal_friction": {
            "enforced_system_name": legal_friction.enforced_system_name if legal_friction else None,
            "preferred_system_name": legal_friction.preferred_system_name if legal_friction else None,
            "family_law_divergence": legal_friction.family_law_divergence if legal_friction else None,
            "criminal_law_divergence": legal_friction.criminal_law_divergence if legal_friction else None,
            "legal_friction_density": legal_friction.legal_friction_density if legal_friction else None,
            "jurisdictional_autonomy_score": legal_friction.jurisdictional_autonomy_score if legal_friction else None,
            "population_under_external_law": legal_friction.population_under_external_law if legal_friction else None
        },
        "scores": {
            "jurisdictional_autonomy_score": scores.jurisdictional_autonomy_score if scores else None,
            "resource_security_score": scores.resource_security_score if scores else None,
            "infrastructural_control_score": scores.infrastructural_control_score if scores else None,
            "composite_sovereignty_index": scores.composite_sovereignty_index if scores else None,
            "topographic_component": scores.topographic_component if scores else None,
            "hydrology_component": scores.hydrology_component if scores else None,
            "infrastructure_component": scores.infrastructure_component if scores else None,
            "legal_component": scores.legal_component if scores else None,
            "calculation_date": scores.calculation_date.isoformat() if scores else None,
            "data_confidence_level": scores.data_confidence_level if scores else None
        },
        "high_ground_peaks": [
            {
                "name": p.name,
                "lat": p.geom.y if p.geom else None,
                "lng": p.geom.x if p.geom else None,
                "density": p.density_per_sqkm,
                "population": p.population
            }
            for p in high_ground_peaks
        ],
        "density_pockets": [
            {
                "name": p.name,
                "lat": p.geom.y if p.geom else None,
                "lng": p.geom.x if p.geom else None,
                "density": p.density_per_sqkm,
                "population": p.population
            }
            for p in density_pockets
        ],
        "spatial_features": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": json.loads(db.query(ST_AsGeoJSON(sf.geom)).scalar() or "{}") if sf.geom else {},
                    "properties": {
                        "feature_type": sf.feature_type,
                        "access_status": sf.access_status,
                        "elevation_m": sf.elevation_m,
                        **(sf.properties or {})
                    }
                }
                for sf in spatial_features_query
            ]
        }
    }

    logger.info(f"Built complete profile for {territory_id}")
    return profile


def list_territories(db: Session, limit: int = 50, offset: int = 0) -> tuple:
    """List territories with pagination"""
    query = db.query(Territory)
    total = query.count()

    territories = query.offset(offset).limit(limit).all()

    result = [
        {
            "id": t.id,
            "territory_id": t.territory_id,
            "name": t.name,
            "controlling_entity": t.controlling_entity,
            "population": t.population,
            "total_area_sqkm": t.total_area_sqkm
        }
        for t in territories
    ]

    logger.info(f"Listed {len(result)} territories (total: {total})")
    return result, total


# ============================================================================
# SOVEREIGNTY SCORE QUERIES
# ============================================================================

def get_sovereignty_scores(db: Session, territory_id: str) -> dict:
    """Get sovereignty scores for radar chart"""
    territory = get_territory_by_id(db, territory_id)
    if not territory:
        raise ValueError(f"Territory {territory_id} not found")

    scores = db.query(SovereigntyScore).filter(
        SovereigntyScore.territory_id == territory.id
    ).first()

    if not scores:
        return None

    return {
        "jurisdiction": scores.jurisdictional_autonomy_score,
        "water_access": scores.resource_security_score,
        "food_self_sufficiency": scores.resource_security_score,
        "mobility_borders": scores.infrastructural_control_score,
        "airspace_spectrum": scores.infrastructural_control_score,
        "currency": scores.infrastructural_control_score
    }


# ============================================================================
# SPATIAL FEATURE QUERIES
# ============================================================================

def get_spatial_features(db: Session, territory_id: str, feature_type: Optional[str] = None) -> dict:
    """Get GeoJSON spatial features for map"""
    territory = get_territory_by_id(db, territory_id)
    if not territory:
        raise ValueError(f"Territory {territory_id} not found")

    query = db.query(SpatialFeature).filter(
        SpatialFeature.territory_id == territory.id
    )

    if feature_type:
        query = query.filter(SpatialFeature.feature_type == feature_type)

    features = query.all()

    geojson_features = []
    for sf in features:
        if sf.geom:
            try:
                geom_json = json.loads(db.query(ST_AsGeoJSON(sf.geom)).scalar() or "{}")
            except:
                geom_json = {}

            geojson_features.append({
                "type": "Feature",
                "geometry": geom_json,
                "properties": {
                    "feature_type": sf.feature_type,
                    "access_status": sf.access_status,
                    "elevation_m": sf.elevation_m,
                    **(sf.properties or {})
                }
            })

    return {
        "type": "FeatureCollection",
        "features": geojson_features
    }


def get_border_checkpoints(db: Session, territory_id: str) -> list:
    """Get border checkpoint locations"""
    territory = get_territory_by_id(db, territory_id)
    if not territory:
        raise ValueError(f"Territory {territory_id} not found")

    checkpoints = db.query(BorderCheckpoint).filter(
        BorderCheckpoint.territory_id == territory.id
    ).all()

    return [
        {
            "name": c.name,
            "checkpoint_type": c.checkpoint_type,
            "control_status": c.control_status,
            "permit_requirement": c.permit_requirement,
            "lat": c.geom.y if c.geom else None,
            "lng": c.geom.x if c.geom else None
        }
        for c in checkpoints
    ]


# ============================================================================
# COMPARISON QUERIES
# ============================================================================

def compare_territories(db: Session, territory_id_1: str, territory_id_2: str) -> dict:
    """Compare two territories side-by-side"""
    profile_1 = get_territory_profile(db, territory_id_1)
    profile_2 = get_territory_profile(db, territory_id_2)

    return {
        "territory_1": profile_1,
        "territory_2": profile_2,
        "comparison": {
            "sovereignty_index_diff": (profile_1["scores"]["composite_sovereignty_index"] or 0) -
                                      (profile_2["scores"]["composite_sovereignty_index"] or 0),
            "area_ratio_diff": (profile_1["territory"]["area_ratio_accessible"] or 0) -
                               (profile_2["territory"]["area_ratio_accessible"] or 0),
            "water_security_diff": (profile_1["hydrology"]["water_security_score"] or 0) -
                                   (profile_2["hydrology"]["water_security_score"] or 0)
        }
    }


# ============================================================================
# DATA SOURCE ATTRIBUTION
# ============================================================================

def get_data_sources(db: Session) -> list:
    """Get all data sources with attribution"""
    sources = db.query(DataSource).all()

    return [
        {
            "id": s.id,
            "name": s.source_name,
            "url": s.url,
            "license_type": s.license_type,
            "attribution_text": s.attribution_text,
            "last_updated": s.last_updated.isoformat() if s.last_updated else None,
            "update_frequency": s.update_frequency,
            "data_format": s.data_format
        }
        for s in sources
    ]


def get_territory_data_lineage(db: Session, territory_id: str) -> list:
    """Get data lineage for a territory"""
    territory = get_territory_by_id(db, territory_id)
    if not territory:
        raise ValueError(f"Territory {territory_id} not found")

    lineage = db.query(DataLineage).filter(
        DataLineage.territory_id == territory.id
    ).all()

    return [
        {
            "source_name": l.source.source_name,
            "data_type": l.data_type,
            "ingestion_date": l.ingestion_date.isoformat() if l.ingestion_date else None,
            "data_version": l.data_version,
            "record_count": l.record_count,
            "license_type": l.source.license_type,
            "attribution": l.source.attribution_text
        }
        for l in lineage
    ]
