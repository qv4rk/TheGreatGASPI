"""
FastAPI route handlers for The Great GASPI
Endpoints for serving territory profiles, scores, and spatial features to frontend
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime

from .models import (
    TerritoryProfile,
    SovereigntyScores,
    DataSource,
    HealthResponse,
    ErrorResponse
)
from .database import SessionLocal
from . import routes_db

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/v1", tags=["territories"])


# ============================================================================
# TERRITORY ENDPOINTS
# ============================================================================

@router.get("/territories/{territory_id}")
async def get_territory_profile(territory_id: str, db: Session = Depends(lambda: SessionLocal())):
    """
    Get complete territory profile with all four pillars and scores
    Feeds the frontend GaspiMapViewer component

    Example: GET /api/v1/territories/west-bank
    """
    try:
        logger.info(f"Fetching profile for territory: {territory_id}")
        profile = routes_db.get_territory_profile(db, territory_id)
        return profile
    except ValueError as e:
        logger.error(f"Territory not found: {territory_id}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching territory {territory_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/territories")
async def list_territories(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(lambda: SessionLocal())
):
    """
    List all available territories with basic metadata
    Paginated response for frontend territory selector
    """
    try:
        logger.info(f"Listing territories: limit={limit}, offset={offset}")
        territories, total = routes_db.list_territories(db, limit, offset)
        return {
            "territories": territories,
            "total": total,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Error listing territories: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/territories/{territory_id}/scores")
async def get_sovereignty_scores(territory_id: str, db: Session = Depends(lambda: SessionLocal())):
    """
    Get sovereignty scores for a territory
    Returns the multi-axis radar chart data for frontend
    """
    try:
        logger.info(f"Fetching scores for: {territory_id}")
        scores = routes_db.get_sovereignty_scores(db, territory_id)
        if not scores:
            raise HTTPException(status_code=404, detail="Scores not found for this territory")
        return scores
    except ValueError as e:
        logger.error(f"Territory not found: {territory_id}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching scores: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/territories/{territory_id}/compare")
async def compare_territories(
    territory_id: str,
    compare_to: str = Query(..., description="Territory ID to compare against"),
    db: Session = Depends(lambda: SessionLocal())
):
    """
    Compare two territories side-by-side
    Returns comparative metrics for both territories
    """
    try:
        logger.info(f"Comparing {territory_id} vs {compare_to}")
        comparison = routes_db.compare_territories(db, territory_id, compare_to)
        return comparison
    except ValueError as e:
        logger.error(f"Territory not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error comparing territories: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


# ============================================================================
# SPATIAL FEATURES ENDPOINTS
# ============================================================================

@router.get("/territories/{territory_id}/spatial-features")
async def get_spatial_features(
    territory_id: str,
    feature_type: Optional[str] = Query(None, description="accessible_area|restricted_area|high_ground|barrier"),
    db: Session = Depends(lambda: SessionLocal())
):
    """
    Get GeoJSON spatial features for map rendering
    Returns FeatureCollection for Deck.gl/MapLibre visualization
    """
    try:
        logger.info(f"Fetching spatial features for {territory_id}")
        features = routes_db.get_spatial_features(db, territory_id, feature_type)
        return features
    except ValueError as e:
        logger.error(f"Territory not found: {territory_id}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching spatial features: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/territories/{territory_id}/high-ground-peaks")
async def get_high_ground_peaks(territory_id: str):
    """
    Get tactical high-ground peak locations for map markers
    Returns array of peak points with elevation advantage ratings
    """
    try:
        logger.info(f"Fetching high-ground peaks for {territory_id}")

        # TODO: Query topographic_data and compute peak locations
        raise HTTPException(
            status_code=501,
            detail="High-ground peaks endpoint not yet implemented"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching peaks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/territories/{territory_id}/density-pockets")
async def get_population_density_pockets(territory_id: str):
    """
    Get population concentration areas for heatmap layer
    Returns array of density pocket locations and intensities
    """
    try:
        logger.info(f"Fetching density pockets for {territory_id}")

        # TODO: Query population_density_pockets table
        raise HTTPException(
            status_code=501,
            detail="Density pockets endpoint not yet implemented"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching density pockets: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# PILLAR-SPECIFIC ENDPOINTS
# ============================================================================

@router.get("/territories/{territory_id}/pillar/topography")
async def get_topography_pillar(territory_id: str):
    """
    Get Pillar 1: Physical Geography & Topographic Asymmetry
    Returns AF, T, Eb, Vf metrics and high-ground advantage ratings
    """
    try:
        logger.info(f"Fetching topography pillar for {territory_id}")
        # TODO: Query topographic_data table
        raise HTTPException(status_code=501, detail="Not yet implemented")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/territories/{territory_id}/pillar/hydrology")
async def get_hydrology_pillar(territory_id: str):
    """
    Get Pillar 2: Hydropolitics & Resource Control
    Returns water security, agricultural autonomy, resource scores
    """
    try:
        logger.info(f"Fetching hydrology pillar for {territory_id}")
        # TODO: Query hydrology_data and river_basins tables
        raise HTTPException(status_code=501, detail="Not yet implemented")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/territories/{territory_id}/pillar/infrastructure")
async def get_infrastructure_pillar(territory_id: str):
    """
    Get Pillar 3: Infrastructure & Economic Levers
    Returns airspace, spectrum, maritime, border, currency control metrics
    """
    try:
        logger.info(f"Fetching infrastructure pillar for {territory_id}")
        # TODO: Query infrastructure_data and border_checkpoints tables
        raise HTTPException(status_code=501, detail="Not yet implemented")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/territories/{territory_id}/pillar/legal-friction")
async def get_legal_friction_pillar(territory_id: str):
    """
    Get Pillar 4: Legal-Cultural Friction & Governance Divergence
    Returns jurisdictional autonomy, legal friction density, statutory conflicts
    """
    try:
        logger.info(f"Fetching legal friction pillar for {territory_id}")
        # TODO: Query legal_friction_data and legal_statutes tables
        raise HTTPException(status_code=501, detail="Not yet implemented")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# DATA ATTRIBUTION & SOURCES
# ============================================================================

@router.get("/sources")
async def get_data_sources(db: Session = Depends(lambda: SessionLocal())):
    """
    Get attribution and metadata for all data sources
    Lists licenses, URLs, and update frequencies
    """
    try:
        logger.info("Fetching data sources")
        sources = routes_db.get_data_sources(db)
        return {"sources": sources, "total": len(sources)}
    except Exception as e:
        logger.error(f"Error fetching sources: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/territories/{territory_id}/sources")
async def get_territory_data_lineage(territory_id: str):
    """
    Get data lineage for a specific territory
    Shows which sources contributed data and update dates
    """
    try:
        logger.info(f"Fetching data lineage for {territory_id}")
        # TODO: Query data_lineage table
        raise HTTPException(
            status_code=501,
            detail="Data lineage endpoint not yet implemented"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# HEALTH & METADATA
# ============================================================================

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    Returns service status and timestamp
    """
    return HealthResponse(
        status="healthy",
        service="gasapi-backend",
        timestamp=datetime.utcnow()
    )


@router.get("/info")
async def get_service_info():
    """
    Get service metadata and API information
    """
    return {
        "service": "The Great GASPI",
        "version": "0.1.0-phase2",
        "description": "Global Asymmetric Sovereignty & Power Index API",
        "documentation": "/docs",
        "openapi": "/openapi.json",
        "base_url": "/api/v1",
        "pillars": [
            "Physical Geography & Topographic Asymmetry",
            "Hydropolitics & Resource Control",
            "Infrastructure & Economic Levers",
            "Legal-Cultural Friction & Governance Divergence"
        ],
        "territory_count": "0 (database not yet populated)"
    }
