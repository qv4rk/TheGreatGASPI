# Data Sources & Attribution

The Great GSAPI is built entirely on open-access datasets. This document provides complete attribution, URLs, licenses, and data dictionaries for all integrated sources.

## Hydrology & Water Sovereignty

### HydroSHEDS
- **URL:** https://www.hydrosheds.org/
- **License:** CC BY 4.0
- **Format:** GeoTIFF, GeoJSON
- **Data Type:** River basins, flow direction, upstream/downstream analysis
- **Attribution:** WWF Global Freshwater Team
- **Update Frequency:** Periodic (5-10 year intervals)
- **Citation:** Lehner, B., Verdin, K., Jarvis, A. (2008). New global hydrography derived from spaceborne elevation data. Eos. Trans. AGU 89(47):93-94.

### OpenLandMap Hydrography
- **URL:** https://openlandmap.org/
- **License:** CC BY 4.0
- **Format:** GeoTIFF, GeoJSON
- **Data Type:** Wetlands, water bodies, groundwater potential
- **Attribution:** OpenLandMap contributors
- **Update Frequency:** Annual

## Demographics & Population

### WorldPop
- **URL:** https://www.worldpop.org/
- **License:** CC BY 4.0
- **Format:** GeoTIFF (raster grid), JSON statistics
- **Data Type:** Population distribution, density gridded to 100m resolution
- **Attribution:** University of Southampton
- **Update Frequency:** Annual
- **Citation:** Stevens, F.R., Gaughan, A.E., Linard, C., & Tatem, A.J. (2015). Disaggregating census data for population mapping using random forests with remotely-sensed and ancillary data. PLOS ONE 10(2): e0107042.

### UN Data API
- **URL:** https://data.un.org/
- **License:** CC BY 4.0
- **Format:** JSON, CSV
- **Data Type:** Official demographic statistics, population by age/gender
- **Attribution:** United Nations Statistics Division
- **Update Frequency:** Annual/Semi-annual

## Topography & Elevation

### Open-Elevation API
- **URL:** https://open-elevation.com/
- **License:** MIT
- **Format:** REST JSON, DEM Raster
- **Data Type:** Digital Elevation Model (DEM), terrain analysis
- **Attribution:** Open-Elevation contributors
- **Update Frequency:** Static (USGS SRTM 30m data)

### Mapbox Raster DEM
- **URL:** https://docs.mapbox.com/mapbox-gl-js/
- **License:** Open Data (CC BY 2.0)
- **Format:** RGB raster tiles
- **Data Type:** Elevation for 3D visualization
- **Attribution:** Mapbox, GEBCO, GEBCO, NOAA ETOPO1
- **Update Frequency:** Periodic

## Agriculture & Land Use

### FAOSTAT (UN FAO)
- **URL:** https://www.fao.org/faostat/
- **License:** CC BY-NC-SA 3.0
- **Format:** JSON, CSV
- **Data Type:** Arable land percentage, crop production, agricultural imports
- **Attribution:** Food and Agriculture Organization of the United Nations
- **Update Frequency:** Annual
- **Variables:**
  - Land use (arable, permanent crops, forest)
  - Crop production volume & value
  - Trade statistics (imports/exports)
  - Agri-commodity dependency

## Legal Systems & Statutes

### CourtListener API
- **URL:** https://www.courtlistener.com/api/
- **License:** Apache 2.0 / Public Domain (US legal documents)
- **Format:** REST JSON
- **Data Type:** Legal statutes, court opinions, case law
- **Attribution:** Free Law Project
- **Update Frequency:** Real-time
- **Coverage:** Primarily US federal courts; international law datasets partial

### WorldWideLaw
- **URL:** https://www.worldwidelaw.org/
- **License:** BSD / Research
- **Format:** REST JSON
- **Data Type:** International legal frameworks, treaty data
- **Attribution:** WorldWide Law contributors
- **Update Frequency:** Periodic

## Legal-Cultural Friction & Religion

### Pew Research Center
- **URL:** https://www.pewresearch.org/
- **License:** Open Access Research
- **Format:** CSV, microdata datasets
- **Data Type:** Religious demographics, attitudes toward law/governance
- **Attribution:** Pew Research Center
- **Update Frequency:** Periodic (multi-year surveys)
- **Variables:**
  - Religious affiliation distribution
  - Attitudes toward government authority
  - Legal system preferences by population

### World Values Survey
- **URL:** https://www.worldvaluessurvey.org/
- **License:** Open Access (Creative Commons)
- **Format:** Microdata (CSV, SPSS, Stata)
- **Data Type:** Cultural values, legal preferences, governance attitudes
- **Attribution:** World Values Survey Association
- **Update Frequency:** Every 5 years (waves)
- **Coverage:** 90+ countries; representative national samples

## Spatial Base Layers

### OpenStreetMap
- **URL:** https://www.openstreetmap.org/
- **License:** ODbL (Open Data Commons Open Database License)
- **Format:** Vector Tiles (.mvt), GeoJSON
- **Data Type:** Base map features (roads, buildings, POIs), territorial boundaries
- **Attribution:** OpenStreetMap contributors
- **Update Frequency:** Real-time (crowdsourced)
- **Note:** Requires attribution in UI: "© OpenStreetMap contributors"

### MapLibre GL JS
- **URL:** https://maplibre.org/
- **License:** BSD 3-Clause
- **Format:** Vector Tiles, rendered WebGL
- **Data Type:** Map rendering library
- **Attribution:** MapLibre contributors

## Data Integration & Processing

### ETL Pipeline
The data integration pipeline (`etl/`) performs:
1. **Ingestion** — Downloads from APIs/sources via `requests`, `geopandas`
2. **Validation** — Schema conformance, coordinate system checks, temporal validation
3. **Transformation** — Reprojection to EPSG:4326 (WGS84), spatial indexing
4. **Storage** — PostGIS database with metadata tables
5. **Attribution** — Source tracking (URL, license, date downloaded, version)

### Metadata Tables
All ingested data includes metadata:
- `data_sources` — Source registry (URL, license, attribution)
- `data_lineage` — Processing history, timestamps, data versions
- `update_log` — Track when each source was last updated

## License Compliance

| Source | License | Commercial Use | Modification | Attribution Required |
|--------|---------|-----------------|--------------|----------------------|
| HydroSHEDS | CC BY 4.0 | ✅ | ✅ | ✅ |
| WorldPop | CC BY 4.0 | ✅ | ✅ | ✅ |
| Open-Elevation | MIT | ✅ | ✅ | ✅ |
| FAOSTAT | CC BY-NC-SA 3.0 | ❌ (NC) | ✅ | ✅ |
| CourtListener | Apache 2.0 | ✅ | ✅ | ✅ |
| OpenStreetMap | ODbL | ✅ | ✅ | ✅ |
| Pew Research | Open Access | ✅ | ✅ | ✅ |
| World Values Survey | CC (varies) | ✅ | Varies | ✅ |

**Note:** The Great GSAPI is released under MIT license. Specific data sources retain their original licenses. See [LICENSE](LICENSE) for complete terms.

## How to Add New Data Sources

1. **Source Selection** — Ensure open-access with compatible license
2. **API Documentation** — Document endpoint, rate limits, format
3. **Update ETL Script** — Add ingestion logic to `etl/sources/`
4. **Validate Schema** — Ensure data conforms to existing structure
5. **Update This File** — Add source to DATA_SOURCES.md with complete attribution
6. **Test & Commit** — Verify integration and submit PR

---

**Last Updated:** July 2026

For questions about data sources, licensing, or attribution, please open an [issue](https://github.com/qv4rk/TheGreatGSAPI/issues).
