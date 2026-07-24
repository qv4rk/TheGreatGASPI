# The Great GSAPI
*Global Sovereignty & Asymmetric Power Index*

Open-source geopolitical analytics platform mapping non-traditional power dynamics, resource control, and legal-cultural friction across disputed territories.

## 🌍 Features

- **Interactive 3D Geospatial Dashboard** — Deck.gl-powered 3D terrain, water sovereignty layers, territorial control visualization
- **4-Pillar Sovereignty Scoring** — Composite algorithm measuring jurisdictional autonomy, resource security, and infrastructural control
- **10+ Mirrored Open Datasets** — Self-hosted PostGIS backend (HydroSHEDS, WorldPop, FAO, OpenStreetMap, CourtListener, more)
- **API-Independent Architecture** — All data cached locally; platform works even if upstream sources go down
- **Comparative Territory Analysis** — Side-by-side friction analysis across territories, upstream/downstream dynamics, legal divergence

## 📊 Four Analytical Pillars

### Pillar A: Physical Geography & Territorial Asymmetry
Topography, elevation, geographic isolation, demographic breakdown, topographic high-ground advantage

### Pillar B: Hydropolitics & Resource Control
Upstream vs. downstream river basin positions, groundwater aquifer control, dam rights, arable land %, agricultural import dependency

### Pillar C: Infrastructural & Economic Levers of Power
Border checkpoint management, EEZ rights, airspace sovereignty, frequency spectrum, power grid connectivity, monetary control

### Pillar D: Legal-Cultural Friction & Governance Divergence
Gap between enforced legal systems (occupation law, military orders) and preferred local systems (customary law, religious baseline)

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.10+
- Node.js 18+

### Clone & Run Locally

```bash
git clone https://github.com/qv4rk/TheGreatGSAPI.git
cd TheGreatGSAPI

# Start PostgreSQL + PostGIS backend
docker-compose up -d

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Run ETL pipeline to load data
python etl/run_pipeline.py

# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

```bash
# In another terminal, install frontend
cd frontend
npm install
npm run dev
```

Frontend will be available at `http://localhost:3000`

## 🏗️ Architecture

### Backend Stack
- **FastAPI** — REST API serving spatial queries
- **PostGIS** — PostgreSQL extension for geospatial data
- **GeoPandas** — Python geospatial analysis
- **Shapely** — Geometric operations
- **SQLAlchemy** — ORM for database abstraction

### Frontend Stack
- **React** — UI framework
- **Deck.gl** — High-performance WebGL rendering for 3D geospatial
- **MapLibre GL JS** — Lightweight base mapping
- **D3.js** — Custom visualizations
- **Nivo** — Radar charts & comparative analytics

### Data Pipeline (ETL)
- **Python scripts** ingest data from 10+ open sources
- **Periodic updates** (configurable: daily/weekly/monthly)
- **Data validation** & schema conformance
- **Spatial indexing** for fast queries
- **Version tracking** with source attribution

## 📚 Data Sources & Attribution

All datasets are open-access and properly attributed. See [DATA_SOURCES.md](DATA_SOURCES.md) for complete attribution, URLs, licenses, and data dictionaries.

**Key Sources:**
- HydroSHEDS (CC BY 4.0) — River basins, flow direction
- WorldPop (CC BY 4.0) — Population distribution
- OpenStreetMap (ODbL) — Base layers, POIs
- FAOSTAT (CC BY-NC-SA 3.0) — Agricultural data
- CourtListener API (Apache 2.0) — Legal statutes & cases
- Open-Elevation API (MIT) — Topography & DEM
- Pew Research / World Values Survey — Cultural friction metrics

## 📋 Project Roadmap

| Phase | Milestone | Status | Target |
|-------|-----------|--------|--------|
| 1 | Data Harvesting & GIS Pipeline Setup | ✅ Completed | — |
| 2 | Backend API Development | 🟡 In Progress | Aug 2026 |
| 3 | Frontend Deck.gl/MapLibre UI Integration | ⏳ Planned | Sep 2026 |
| 4 | Sovereignty Scorecard & Radar Charts | ⏳ Planned | Oct 2026 |
| 5 | Open-Source Release & GitHub Docs | ⏳ Planned | Nov 2026 |

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Reporting bugs
- Proposing features
- Submitting pull requests
- Adding new data sources

## 📖 Documentation

- [DATA_SOURCES.md](DATA_SOURCES.md) — Complete attribution & data dictionary
- [CONTRIBUTING.md](CONTRIBUTING.md) — Contribution guidelines
- [ARCHITECTURE.md](ARCHITECTURE.md) — Detailed system design (coming)
- [API_DOCS.md](API_DOCS.md) — FastAPI endpoint reference (coming)

## 🔗 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment guides (Vercel, AWS, self-hosted).

## 📜 License

MIT License — See [LICENSE](LICENSE)

This project is built on open data. We maintain full attribution and encourage others to fork, modify, and build upon this work.

## 🙏 Acknowledgments

This project would not be possible without the open-source geospatial community:
- Natural Earth / OpenStreetMap contributors
- HydroSHEDS team at WWF
- WorldPop researchers at University of Southampton
- D3.js, Deck.gl, and PostGIS communities

---

**Questions?** Open an [issue](https://github.com/qv4rk/TheGreatGSAPI/issues) or check the [discussions](https://github.com/qv4rk/TheGreatGSAPI/discussions).

*Last Updated: July 2026*
