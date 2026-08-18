#!/usr/bin/env python3
"""
PASTE THIS WHOLE FILE INTO ONE GOOGLE COLAB CELL AND RUN IT.

Fetches OSM building footprints for Gaza City, scoped to the 16
neighborhood bounding boxes that actually contain UNOSAT damage points
(computed from data/damage/by_neighborhood/*.geojson, +60m buffer each) --
about 60% of the area of a naive full-city bounding box, and every tile
lines up with a neighborhood file that already exists in the repo.

Downloads ONE FILE PER NEIGHBORHOOD as it finishes (not one giant file at
the end) -- so if Colab disconnects partway through, or a tile is clearly
too large, you already have whatever completed before that point.
"""
!pip install osmnx geopandas --quiet

import time
import geopandas as gpd
import osmnx as ox

ox.settings.use_cache = True
ox.settings.requests_timeout = 300
ox.settings.overpass_rate_limit = True

def slug(name):
    import re
    return re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()

# (name, (west, south, east, north)) -- real bounding boxes from the
# actual UNOSAT damage-point coordinates, not an arbitrary grid.
TILES = [
    ("Az Zaitoun", (34.419374, 31.470545, 34.467619, 31.506518)),
    ("At Turukman - Ijdeedeh", (34.458057, 31.479583, 34.480873, 31.502713)),
    ("Ash Shuja'iyeh - Ijdeedeh", (34.467495, 31.491013, 34.497557, 31.509295)),
    ("At Tuffah", (34.467455, 31.505046, 34.499896, 31.521631)),
    ("Ad Darraj", (34.452038, 31.506898, 34.476303, 31.527182)),
    ("An Naser", (34.448063, 31.521427, 34.468389, 31.540725)),
    ("Northern Remal", (34.437109, 31.513376, 34.461893, 31.530787)),
    ("Ash Sheikh Radwan", (34.460755, 31.526416, 34.478145, 31.539701)),
    ("Southern Remal", (34.42421, 31.506672, 34.451103, 31.529183)),
    ("Ash Sheikh 'Ijleen", (34.41408, 31.494489, 34.434131, 31.515424)),
    ("As Sabra", (34.436959, 31.50153, 34.459575, 31.514094)),
    ("Old City", (34.457642, 31.499526, 34.471333, 31.509467)),
    ("Al Awadah", (34.450404, 31.535446, 34.465206, 31.54673)),
    ("Tal El Hawa", (34.427885, 31.499444, 34.443427, 31.509634)),
    ("At Turukman", (34.449746, 31.462708, 34.484876, 31.491295)),
    ("Ijdeedeh", (34.480887, 31.485299, 34.514723, 31.513767)),
]

from google.colab import files

total_buildings = 0
total_bytes = 0
for i, (name, bbox) in enumerate(TILES, 1):
    print(f"[{i}/{len(TILES)}] {name}: fetching...", end=" ", flush=True)
    try:
        gdf = ox.features.features_from_bbox(bbox, {"building": True})
        gdf = gdf[gdf.geometry.type.isin(["Polygon", "MultiPolygon"])].copy()
        gdf = gdf[gdf.geometry.is_valid & ~gdf.geometry.is_empty]
        keep = ["geometry"] + [c for c in gdf.columns if c != "geometry" and gdf[c].dropna().apply(lambda x: not isinstance(x, (list, dict))).all()]
        gdf = gdf[keep]

        out_name = f"buildings_{slug(name)}.geojson"
        gdf.to_file(out_name, driver="GeoJSON")
        import os
        size = os.path.getsize(out_name)
        total_buildings += len(gdf)
        total_bytes += size
        print(f"{len(gdf)} buildings, {size/1e6:.1f} MB")
        files.download(out_name)
        time.sleep(2)
    except Exception as ex:
        print(f"FAILED: {ex}")

print(f"\nDone. {total_buildings:,} buildings total, {total_bytes/1e6:.1f} MB across {len(TILES)} files.")
print("Upload all the buildings_*.geojson files that downloaded (check your browser's Downloads folder).")
