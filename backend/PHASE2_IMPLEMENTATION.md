# Phase 2: Backend API Development - Implementation Guide

This document outlines the Phase 2 implementation for The Great GASPI backend.

## Status

**Phase 2 Deliverables:**
- ✅ PostGIS database schema (SQL migrations)
- ✅ Pydantic models for all four pillars
- ✅ FastAPI endpoint scaffolding
- ✅ Metric calculation functions (AF, T, Vf, Encirclement, etc.)
- ✅ ETL data loader framework
- 🔄 **IN PROGRESS:** Database integration with actual queries
- ⏳ **PENDING:** Data population from open sources

## Architecture Overview

```
Frontend (GaspiMapViewer.jsx)
    ↓ HTTP requests
FastAPI Backend (/api/v1/territories/:id)
    ↓ SQL queries
PostGIS Database (PostgreSQL + PostGIS)
    ↓ ETL pipeline
Open Data Sources (HydroSHEDS, WorldPop, FAOSTAT, etc.)
```

## File Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Settings & configuration
│   ├── database.py          # Database connection & session management
│   ├── models.py            # Pydantic response models (all pillars)
│   ├── calculations.py      # Metric calculation functions
│   ├── routes.py            # API endpoint handlers
│   └── [NEW] schemas.py     # SQLAlchemy ORM schemas (TODO)
│
├── etl/
│   ├── __init__.py
│   ├── run_pipeline.py      # Main ETL orchestrator
│   ├── loader.py            # Data loader for all sources
│   ├── sources/             # Individual source loaders (TODO)
│   │   ├── hydrosheds.py
│   │   ├── worldpop.py
│   │   ├── faostat.py
│   │   └── courtlistener.py
│   └── validators.py        # Data validation schemas (TODO)
│
├── migrations/
│   ├── 001_init_schema.sql  # PostGIS schema initialization
│   └── 002_seed_demo.sql    # (Optional) Demo data
│
├── tests/
│   ├── test_calculations.py # Unit tests for metrics
│   ├── test_routes.py       # Integration tests for endpoints
│   └── test_etl.py          # ETL pipeline tests
│
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container image
└── PHASE2_IMPLEMENTATION.md # This file
```

## Next Steps to Complete Phase 2

### 1. SQLAlchemy ORM Schemas (2-3 hours)

Create `app/schemas.py` with SQLAlchemy declarative models:

```python
from sqlalchemy import Column, Integer, Float, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()

class Territory(Base):
    __tablename__ = "territories"
    id = Column(Integer, primary_key=True)
    territory_id = Column(String(255), unique=True)
    name = Column(String(255))
    # ... map all columns from SQL schema

class TopographicData(Base):
    __tablename__ = "topographic_data"
    # ... all topographic columns

# ... ORM models for all tables
```

### 2. Database Query Functions (4-5 hours)

Implement actual SQL queries in `routes.py`:

```python
async def get_territory_profile(territory_id: str):
    db = SessionLocal()
    territory = db.query(Territory).filter(Territory.territory_id == territory_id).first()
    topo = db.query(TopographicData).filter(TopographicData.territory_id == territory.id).first()
    # ... query all related tables
    # ... serialize to TerritoryProfile Pydantic model
```

### 3. Individual Source ETL Loaders (8-10 hours)

Implement in `etl/sources/`:

**hydrosheds.py:**
```python
def load_hydrosheds_basins(territory_gdf, database_url):
    # Fetch from HydroSHEDS API
    # Intersect with territory boundary
    # Calculate upstream/downstream metrics
    # Insert into river_basins table
```

**worldpop.py:**
```python
def load_worldpop_density(territory_bounds, database_url):
    # Fetch 100m gridded population data
    # Identify density pockets (local maxima)
    # Insert into population_density_pockets table
```

**faostat.py:**
```python
def load_faostat_agriculture(territory_name, database_url):
    # Query FAOSTAT API for territory
    # Extract arable %, crop yields, imports/exports
    # Calculate food import dependency
```

**courtlistener.py:**
```python
def load_legal_statutes(territory_id, controlling_entity, database_url):
    # Query CourtListener API
    # Fetch relevant legal cases/statutes
    # Identify statutory conflicts
```

### 4. Demo Data Seeding (1-2 hours)

Create `migrations/002_seed_demo.sql` with sample data for testing:

```sql
INSERT INTO territories (territory_id, name, controlling_entity, total_area_sqkm, geom)
VALUES ('west-bank', 'West Bank', 'Israel', 5960, ST_GeomFromGeoJSON(...));

INSERT INTO topographic_data (territory_id, asymmetry_factor_AF, ...)
VALUES (1, 52.3, ...);
```

### 5. Testing & Validation (3-4 hours)

Write tests in `tests/`:

```python
# test_calculations.py
def test_asymmetry_factor():
    gdf = create_test_geodataframe()
    af = calculate_asymmetry_factor(gdf)
    assert 0 <= af <= 100

# test_routes.py
def test_get_territory_profile():
    response = client.get("/api/v1/territories/west-bank")
    assert response.status_code == 200
    assert "topographic_asymmetry" in response.json()
```

## Quick Start - Local Development

### 1. Start PostgreSQL + PostGIS

```bash
docker-compose up -d postgres pgadmin
```

### 2. Initialize Database Schema

```bash
docker exec gsapi-postgres psql -U gsapi -d gsapi -f /docker-entrypoint-initdb.d/001_init_schema.sql
```

Or from host:
```bash
psql -U gsapi -h localhost -d gsapi -f backend/migrations/001_init_schema.sql
```

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Run FastAPI Server

```bash
uvicorn app.main:app --reload --port 8000
```

### 5. Test Endpoints

```bash
# Health check
curl http://localhost:8000/health

# API docs
open http://localhost:8000/docs

# Try endpoint (will return 501 until DB queries implemented)
curl http://localhost:8000/api/v1/territories/west-bank
```

### 6. Start Frontend (in another terminal)

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` to see the dashboard trying to connect to the backend.

## Key Implementation Decisions

### 1. Database Choice: PostgreSQL + PostGIS

**Why:**
- PostGIS: Industry-standard for geospatial queries
- Full-featured: Raster + vector support
- Open-source and performant
- Supports complex spatial operations needed for calculations

### 2. ORM: SQLAlchemy

**Why:**
- Type-safe ORM with GeoAlchemy2 extension
- Async support for FastAPI
- Alembic integration for migrations

### 3. Calculation Approach

Metrics are computed at **data ingestion time**, not query time:
- Store pre-calculated AF, T, Vf, Encirclement scores
- Reduces API latency
- Audit trail of when metrics were computed

### 4. ETL Strategy

**Pull model:** ETL runs on schedule, pulls from open APIs
- Maintains local mirror of data
- Independent of external API availability
- Versioning and data lineage tracking

## API Endpoint Reference

All endpoints return standardized responses with attribution:

**GET /api/v1/territories/{territory_id}**
```json
{
  "territory": { "name": "West Bank", ... },
  "topographic_asymmetry": { "asymmetry_factor_AF": 52.3, ... },
  "hydrology": { "resource_security_composite": 35.8, ... },
  "infrastructure": { "infrastructural_control_score": 28.4, ... },
  "legal_friction": { "jurisdictional_autonomy_score": 22.1, ... },
  "scores": { "composite_sovereignty_index": 34.2, ... },
  "high_ground_peaks": [...],
  "density_pockets": [...],
  "spatial_features": { "type": "FeatureCollection", "features": [...] }
}
```

## Common Issues & Solutions

### Issue: `psycopg2: server closed the connection unexpectedly`
**Solution:** Ensure PostgreSQL is running: `docker-compose logs postgres`

### Issue: `LOCATION not found in spatial_ref_sys`
**Solution:** Run `SELECT PostGIS_Full_Version()` to verify installation

### Issue: GeoJSON parsing errors
**Solution:** Validate GeoJSON with `geojson.py` or https://geojson.io/

## Performance Considerations

### Queries
- Index on `territory_id` (PK)
- Index on `geom` columns (GIST)
- Use `ST_DWithin()` for proximity queries

### Data
- Simplify geometries for web (use `ST_Simplify()`)
- Cache API responses (Redis, future phase)
- Compress raster data (GeoTIFF with compression)

## Security Notes

- Never expose database credentials in code (use `.env`)
- Sanitize all API inputs
- Rate limit ETL operations
- Validate all incoming GeoJSON

## Next Phase (Phase 3)

Once Phase 2 is complete, Phase 3 will integrate:
- Deck.gl rendering for 3D terrain
- Real-time data updates
- Performance optimization
- Frontend caching

---

**Questions?** Refer to:
- [PostGIS Documentation](https://postgis.net/docs/)
- [FastAPI Guide](https://fastapi.tiangolo.com/)
- [GeoAlchemy2](https://geoalchemy-2.readthedocs.io/)
- [GeoPandas](https://geopandas.org/)
