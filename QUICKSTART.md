# The Great GASPI - Quick Start Guide

Get the complete platform running locally in 10 minutes.

## Prerequisites

- Docker & Docker Compose installed
- Python 3.10+ installed
- Node.js 18+ installed
- Git

## Step 1: Start PostgreSQL + PostGIS (2 minutes)

```bash
# From repo root
docker-compose up -d

# Verify PostgreSQL is running
docker-compose logs postgres | grep "ready to accept connections"

# Optional: Access pgAdmin at http://localhost:5050
# Login: admin@gsapi.local / admin
```

## Step 2: Initialize Database Schema (1 minute)

```bash
# Option A: From inside container
docker exec gsapi-postgres psql -U gsapi -d gsapi -f /docker-entrypoint-initdb.d/01-init.sql

# Option B: From host (if psql installed)
psql -U gsapi -h localhost -d gsapi -f backend/migrations/001_init_schema.sql
```

Verify:
```bash
docker exec gsapi-postgres psql -U gsapi -d gsapi -c "SELECT table_name FROM information_schema.tables WHERE table_schema='public';" | head -20
```

You should see 19 tables listed (territories, topographic_data, hydrology_data, etc.)

## Step 3: Seed Demo Data (2 minutes)

```bash
# Load SQL seed data
docker exec gsapi-postgres psql -U gsapi -d gsapi -f /docker-entrypoint-initdb.d/02-seed-demo-data.sql

# Run Python populator (spatial features, checkpoints, etc.)
cd backend
pip install -r requirements.txt
python -m etl.seed_demo_data
cd ..
```

Verify demo territories were created:
```bash
docker exec gsapi-postgres psql -U gsapi -d gsapi -c "SELECT name, controlling_entity, total_area_sqkm FROM territories;"
```

Output should show 4 territories:
- West Bank (Israel)
- Western Sahara (Morocco)
- Northern Cyprus (Turkey)
- Transnistria (Russia)

## Step 4: Start Backend API (2 minutes)

```bash
cd backend

# Install dependencies (if not already done)
pip install -r requirements.txt

# Run FastAPI server
uvicorn app.main:app --reload --port 8000

# You should see:
# Uvicorn running on http://0.0.0.0:8000
```

Test the API:
```bash
# In another terminal
curl http://localhost:8000/health
# Response: {"status":"healthy","service":"gasapi-backend",...}

# Get West Bank profile
curl http://localhost:8000/api/v1/territories/west-bank | jq .

# List all territories
curl http://localhost:8000/api/v1/territories | jq .
```

**API docs available at:** http://localhost:8000/docs

## Step 5: Start Frontend (2 minutes)

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev

# You should see:
# Local:   http://127.0.0.1:5173/
```

Open http://localhost:5173 in your browser.

You should see:
- **3D Interactive Map** with West Bank, Western Sahara, Northern Cyprus, Transnistria
- **Population density heatmap** showing major cities
- **High-ground markers** (gold/yellow) showing tactical advantage zones
- **Accessible/restricted areas** (green/red) showing territorial control
- **Radar chart** showing multi-axis sovereignty scores

## Common Issues & Solutions

### Database connection refused
```bash
# Check if postgres is running
docker-compose ps

# View postgres logs
docker-compose logs postgres

# Restart containers
docker-compose restart
```

### "psql: command not found"
Install PostgreSQL client tools:
```bash
# macOS
brew install postgresql

# Ubuntu/Debian
sudo apt-get install postgresql-client

# Windows: Download from https://www.postgresql.org/download/windows/
```

### Frontend can't connect to backend
- Verify backend is running on port 8000: `curl http://localhost:8000/health`
- Check browser console for CORS errors
- Ensure CORS origins are correct in `backend/app/main.py`

### Demo data not appearing
```bash
# Verify data in database
docker exec gsapi-postgres psql -U gsapi -d gsapi -c "SELECT COUNT(*) FROM territories;"
# Should return 4

# Check scores were calculated
docker exec gsapi-postgres psql -U gsapi -d gsapi -c "SELECT territory_id, composite_sovereignty_index FROM sovereignty_scores;"
```

## API Endpoints

### Territory Data
- `GET /api/v1/territories` — List all territories
- `GET /api/v1/territories/{id}` — Complete profile (all 4 pillars)
- `GET /api/v1/territories/{id}/scores` — Sovereignty scores for radar chart
- `GET /api/v1/territories/{id}/spatial-features` — GeoJSON for map
- `GET /api/v1/territories/{id}/compare?compare_to={id2}` — Side-by-side comparison

### Data Attribution
- `GET /api/v1/sources` — All data sources with licenses
- `GET /api/v1/territories/{id}/sources` — Data lineage for territory

### Health
- `GET /health` — Service health check
- `GET /` — Service info

## Example: Get West Bank Profile

```bash
curl http://localhost:8000/api/v1/territories/west-bank | jq .

# Response includes:
# {
#   "territory": { "name": "West Bank", "population": 2800000, ... },
#   "topographic_asymmetry": { "asymmetry_factor_AF": 52.3, ... },
#   "hydrology": { "resource_security_composite": 30.8, ... },
#   "infrastructure": { "infrastructural_control_score": 15.3, ... },
#   "legal_friction": { "jurisdictional_autonomy_score": 18.7, ... },
#   "scores": { "composite_sovereignty_index": 24.2, ... },
#   "spatial_features": { "type": "FeatureCollection", "features": [...] },
#   "high_ground_peaks": [...],
#   "density_pockets": [...]
# }
```

## Next Steps

1. **Explore the dashboard** — interact with the 3D map, view different territories
2. **Check API documentation** — http://localhost:8000/docs
3. **View demo data** — http://localhost:5050 (pgAdmin)
4. **Review code** — `backend/app/routes_db.py` for query examples
5. **Add your own territories** — Edit `backend/migrations/002_seed_demo_data.sql`

## Stopping Services

```bash
# Stop backend (press Ctrl+C in terminal)

# Stop frontend (press Ctrl+C in terminal)

# Stop database
docker-compose down
```

## Architecture Reminder

```
Frontend (React + Deck.gl + D3.js)
    ↓ HTTP /api/v1/...
Backend (FastAPI)
    ↓ SQL queries
Database (PostgreSQL + PostGIS)
```

All demo data is synthetic but realistic for testing purposes.

---

**Issues?** Check the logs:
- Backend: `uvicorn` terminal output
- Frontend: Browser console (F12)
- Database: `docker-compose logs postgres`
