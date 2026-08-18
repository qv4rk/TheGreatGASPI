#!/usr/bin/env python3
"""
Joins real OSM building footprints (fetched via
colab_fetch_buildings_by_neighborhood.py) to UNOSAT damage points
(data/damage/by_neighborhood/*.geojson) for one neighborhood.

MATCHING RULE
-------------
1. A damage point that falls INSIDE a building polygon matches that
   building directly.
2. A damage point with no containing building is matched to the NEAREST
   building within 20m (UNOSAT's point placement isn't always exactly
   inside the structure it's assessing).
3. A damage point with no building within 20m stays UNMATCHED -- kept as
   its own point feature, not dropped. The most likely explanation is
   that the structure was destroyed before OSM's mappers captured it
   (Gaza's building footprints were most recently and heavily updated by
   the 2024 HOT mapping campaign, which mapped the post-damage/current
   state in many areas -- a fully-flattened site may simply have no
   footprint left to map), not that the assessment is wrong.
4. A building can match MORE THAN ONE damage point. Every matched point
   is kept in that building's `damage_sites` array -- never averaged or
   reduced to one, same rule as everywhere else in this project.

OUTPUT
------
data/damage/joined/<neighborhood-slug>_buildings.geojson -- every
building polygon in the source file, each carrying a `damage_sites`
array (empty for buildings with no UNOSAT match -- most of them; UNOSAT
assesses specific damage sites, not every structure in the city).

data/damage/joined/<neighborhood-slug>_unmatched_points.geojson --
damage points with no building within 20m.
"""
import json
import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import shape

def clean(v):
    """pandas represents a missing tag as float NaN, not None -- and
    json.dumps happily emits the bare token NaN for that, which is valid
    Python-flavored JSON but not valid JSON per spec, so browsers'
    JSON.parse()/fetch().json() reject it outright. Every value pulled
    from a GeoDataFrame row needs this before going into json.dumps."""
    return None if pd.isna(v) else v

OUT_DIR = Path(__file__).parent / "joined"
NEAREST_MAX_M = 20

def slug(name):
    return re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()

def join(buildings_path, damage_path, neighborhood_slug):
    buildings = gpd.read_file(buildings_path)
    buildings = buildings[buildings.geometry.is_valid & ~buildings.geometry.is_empty].reset_index(drop=True)
    buildings["bldg_idx"] = buildings.index

    damage_raw = json.loads(Path(damage_path).read_text(encoding="utf-8"))
    legend = damage_raw["legend"]
    metadata = damage_raw["metadata"]
    damage_gdf = gpd.GeoDataFrame(
        [{"site_id": f["properties"]["site_id"], "event_code": f["properties"]["event_code"],
          "latest_date": f["properties"]["latest_date"], "latest_class": f["properties"]["latest_class"],
          "pass_count": f["properties"]["pass_count"], "h": f["properties"]["h"],
          "geometry": shape(f["geometry"])} for f in damage_raw["features"]],
        crs="EPSG:4326",
    )

    buildings_m = buildings.to_crs(epsg=32636)
    damage_m = damage_gdf.to_crs(epsg=32636)

    within = gpd.sjoin(damage_m, buildings_m[["bldg_idx", "geometry"]], how="left", predicate="within")
    matched_within = within[~within["bldg_idx"].isna()]

    unmatched_first_pass = within[within["bldg_idx"].isna()].drop(columns=["bldg_idx", "index_right"])
    nearest = gpd.sjoin_nearest(unmatched_first_pass, buildings_m[["bldg_idx", "geometry"]],
                                 how="left", max_distance=NEAREST_MAX_M, distance_col="dist_m")
    matched_nearest = nearest[~nearest["bldg_idx"].isna()]
    still_unmatched = nearest[nearest["bldg_idx"].isna()]

    by_building = {}
    for _, row in matched_within.iterrows():
        by_building.setdefault(int(row["bldg_idx"]), []).append(row)
    for _, row in matched_nearest.iterrows():
        by_building.setdefault(int(row["bldg_idx"]), []).append(row)

    building_features = []
    buildings_wgs = buildings.to_crs(epsg=4326)
    for idx, brow in buildings_wgs.iterrows():
        sites = by_building.get(idx, [])
        building_features.append({
            "type": "Feature",
            "properties": {
                "bldg_id": int(idx),
                "osm_id": clean(brow.get("id")),
                "building_tag": clean(brow.get("building")),
                "name": clean(brow.get("name")),
                "damage_sites": [
                    {"site_id": clean(s["site_id"]), "event_code": clean(s["event_code"]),
                     "latest_date": clean(s["latest_date"]), "latest_class": clean(s["latest_class"]),
                     "pass_count": clean(s["pass_count"]), "h": s["h"]}
                    for s in sites
                ],
            },
            "geometry": json.loads(gpd.GeoSeries([brow.geometry]).to_json())["features"][0]["geometry"],
        })

    unmatched_features = []
    unmatched_wgs = still_unmatched.to_crs(epsg=4326) if len(still_unmatched) else still_unmatched
    for _, row in unmatched_wgs.iterrows():
        unmatched_features.append({
            "type": "Feature",
            "properties": {"site_id": clean(row["site_id"]), "event_code": clean(row["event_code"]),
                            "latest_date": clean(row["latest_date"]), "latest_class": clean(row["latest_class"]),
                            "pass_count": clean(row["pass_count"]), "h": row["h"]},
            "geometry": {"type": "Point", "coordinates": [round(row.geometry.x, 6), round(row.geometry.y, 6)]},
        })

    OUT_DIR.mkdir(exist_ok=True)
    buildings_out = {
        "type": "FeatureCollection",
        "metadata": {**metadata, "match_stats": {
            "damage_points_total": len(damage_gdf),
            "matched_within_building": len(matched_within),
            "matched_nearest_20m": len(matched_nearest),
            "unmatched": len(still_unmatched),
            "buildings_total": len(buildings),
            "buildings_with_damage_data": len(by_building),
        }},
        "legend": legend,
        "features": building_features,
    }
    (OUT_DIR / f"{neighborhood_slug}_buildings.geojson").write_text(
        json.dumps(buildings_out, separators=(",", ":")), encoding="utf-8")

    unmatched_out = {"type": "FeatureCollection", "metadata": metadata, "legend": legend, "features": unmatched_features}
    (OUT_DIR / f"{neighborhood_slug}_unmatched_points.geojson").write_text(
        json.dumps(unmatched_out, separators=(",", ":")), encoding="utf-8")

    print(f"{neighborhood_slug}: {len(buildings)} buildings, {len(by_building)} with damage data, "
          f"{len(matched_within)+len(matched_nearest)}/{len(damage_gdf)} points matched "
          f"({100*(len(matched_within)+len(matched_nearest))/len(damage_gdf):.1f}%), "
          f"{len(still_unmatched)} unmatched points kept separately")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: join_buildings_to_damage.py <buildings.geojson> <neighborhood-slug>")
        print("  (damage file is looked up at data/damage/by_neighborhood/<slug>.geojson)")
        sys.exit(1)
    buildings_path = sys.argv[1]
    neighborhood_slug = sys.argv[2]
    damage_path = Path(__file__).parent / "by_neighborhood" / f"{neighborhood_slug}.geojson"
    join(buildings_path, damage_path, neighborhood_slug)
