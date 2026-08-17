#!/usr/bin/env python3
"""
Proof-of-concept extraction: UNOSAT's Gaza City Comprehensive Damage
Assessment (22-23 Sept 2025 release) into web-ready, time-series-preserving
GeoJSON, split one file per neighborhood, plus a lightweight rollup for a
damage-over-time view.

WHAT THIS IS
------------
Source: data/_static_unosat_filesystem_4205_OCHA-OPT-030_UNOSAT_A3_Gaza_
Governorate_CDA_22-23September2025_GDB.zip -- a real ESRI File Geodatabase
downloaded from UNOSAT/OCHA (via HDX), already sitting in this repo. Not
fetched from the network by this script; this sandbox's egress policy
blocks data.humdata.org, Overpass, and Geofabrik outright (confirmed via
the proxy's own rejection log, not a guess), so this is built entirely
from what's already local.

Each of the 41,222 features in the source layer is a POINT (a damage
site), not a building footprint polygon. UNOSAT's own schema already
carries up to 14 dated satellite passes per site as repeated field groups
(SensorDate/_2/_3.../_14, Main_Damage_Site_Class, ConfidenceID,
Damage_Status) -- that IS the time series; this script reshapes it into an
explicit, compact `h` (history) array per site instead of the wide
repeated-column layout, and does NOT collapse it to a single latest value.

OUTPUT SHAPE
------------
data/damage/by_neighborhood/<slug>.geojson -- one FeatureCollection per
neighborhood (16 total), each Point feature carrying a compact history
array: [[date, damage_class_code, confidence_id, status_code], ...]. Class
codes are resolved via the top-level `legend` object embedded once per
file, not repeated per feature -- avoids the ~40x bloat that made a first,
naive per-feature-verbose-label version of this file 111MB for the whole
city. Territory/Governorate/Municipality are constant across every site in
this release (checked directly, not assumed) and are recorded once in each
file's top-level `metadata`, not per feature.

data/damage/gaza_city_neighborhood_damage_timeline.json -- for every
neighborhood and every assessment date, a count of sites by damage class.
This is the flagship "damage accumulating over time" chart data -- doesn't
need building polygons to be useful on its own.

WHAT THIS IS NOT YET
---------------------
- Not building polygons. Real building-footprint geometry (e.g. HOTOSM's
  Palestine buildings layer) would let each site's damage classification
  render as an actual structure outline instead of a point -- that join
  is the natural next step once that file is available locally (network
  fetch is blocked here; see README.md in this directory).
- The damage-class and damage-status code meanings are UNOSAT's
  well-documented standard four-class scheme (Destroyed / Severe /
  Moderate / Possible) inferred from public UNOSAT methodology notes and
  this file's own value distribution -- NOT confirmed against this
  specific release's own coded-value domain table, which this sandbox
  couldn't read (GDAL CLI tools failed to install here on an unrelated
  missing dependency, not a data problem). Codes outside 1-4 (a small
  number of 6s and 11s appear in this file) are left as "unclassified"
  rather than guessed at. Treat the legend as provisional until checked
  against UNOSAT's published legend for this exact release.
- One SiteID is not a unique per-point key -- multiple distinct point
  features in this file share the same SiteID (a "damage site" cluster
  ID, not a feature ID), confirmed by inspection. This script keeps every
  point as its own feature rather than deduplicating by SiteID.
- EventCode has two distinct values across this file ('CE20231007PSE' and
  'CE202301007PSE') that look like a data-entry typo of the same
  underlying event rather than two real events -- kept as-is per feature
  rather than silently "corrected", since this script doesn't have a way
  to confirm that reading against UNOSAT's own records.
"""
import json
import re
from pathlib import Path
from collections import defaultdict

import fiona

GDB = ("/tmp/unosat_inspect/_static_unosat_filesystem_4205_OCHA-OPT-030_UNOSAT_A3_Gaza_"
       "Governorate_CDA_22-23September2025_GDB/UNOSAT_GazaCity_CDA_22 September2025.gdb")
LAYER = "Damage_Sites_GazaCity_20250922"
OUT_DIR = Path(__file__).parent
BY_NEIGHBORHOOD_DIR = OUT_DIR / "by_neighborhood"

# UNOSAT's standard four-class damage taxonomy, as documented across their
# public conflict damage assessments. PROVISIONAL for this release -- see
# module docstring. Codes not in this map are labeled "Unclassified".
DAMAGE_CLASS_LABELS = {1: "Destroyed", 2: "Severe Damage", 3: "Moderate Damage", 4: "Possible Damage"}
STATUS_LABELS = {0: "No change since previous pass (inferred)", 1: "Change since previous pass (inferred)"}
MAX_PASSES = 14

def pass_suffix(i):
    return "" if i == 1 else f"_{i}"

def slug(name):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()
    return s or "unspecified"

def extract_history(props):
    """Compact [date, class_code, confidence_id, status_code] tuples --
    labels are resolved once via the file-level legend, not per entry."""
    history = []
    for i in range(1, MAX_PASSES + 1):
        suf = pass_suffix(i)
        date = props.get(f"SensorDate{suf}")
        if date is None:
            continue
        cls = props.get(f"Main_Damage_Site_Class{suf}")
        conf = props.get(f"ConfidenceID{suf}")
        status = props.get(f"Damage_Status{suf}")
        history.append([date.isoformat() if hasattr(date, "isoformat") else str(date), cls, conf, status])
    history.sort(key=lambda h: h[0])
    return history

def main():
    by_neighborhood = defaultdict(list)
    neighborhood_timeline = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    skipped_no_geom = skipped_no_history = 0
    territory = governorate = municipality = None

    with fiona.open(GDB, layer=LAYER) as src:
        for feat in src:
            props = feat["properties"]
            geom = feat["geometry"]
            if geom is None:
                skipped_no_geom += 1
                continue
            history = extract_history(props)
            if not history:
                skipped_no_history += 1
                continue
            territory = territory or props.get("Territory")
            governorate = governorate or props.get("Governorate")
            municipality = municipality or props.get("Municipality")

            neighborhood = props.get("Neighborhood") or "Unspecified"
            latest = history[-1]
            for h in history:
                label = DAMAGE_CLASS_LABELS.get(h[1], "Unclassified" if h[1] is not None else None) or "Unclassified"
                neighborhood_timeline[neighborhood][h[0]][label] += 1

            lon, lat = geom["coordinates"][0], geom["coordinates"][1]
            by_neighborhood[neighborhood].append({
                "type": "Feature",
                "properties": {
                    "site_id": props.get("SiteID"),
                    "event_code": props.get("EventCode"),
                    "latest_date": latest[0],
                    "latest_class": latest[1],
                    "pass_count": len(history),
                    "h": history,
                },
                "geometry": {"type": "Point", "coordinates": [round(lon, 6), round(lat, 6)]},
            })

    BY_NEIGHBORHOOD_DIR.mkdir(exist_ok=True)
    total_bytes = 0
    for neighborhood, features in by_neighborhood.items():
        out = {
            "type": "FeatureCollection",
            "metadata": {
                "source": "UNOSAT/OCHA, Gaza City Comprehensive Damage Assessment, 22-23 September 2025 release",
                "geometry_status": "point_only",
                "confidence": "high",
                "notes": "Points are UNOSAT-assessed damage sites, not building footprints. h = [date, damage_class_code, confidence_id, status_code] per satellite pass, oldest first. See extract_unosat_gaza_city.py docstring for legend provenance.",
                "territory": territory, "governorate": governorate, "municipality": municipality,
                "neighborhood": neighborhood,
            },
            "legend": {
                "damage_class": {str(k): v for k, v in DAMAGE_CLASS_LABELS.items()},
                "status": {str(k): v for k, v in STATUS_LABELS.items()},
            },
            "features": features,
        }
        path = BY_NEIGHBORHOOD_DIR / f"{slug(neighborhood)}.geojson"
        text = json.dumps(out, separators=(",", ":"))
        path.write_text(text, encoding="utf-8")
        total_bytes += len(text.encode("utf-8"))

    timeline_out = {
        neighborhood: [{"date": date, "counts": dict(counts)} for date, counts in sorted(by_date.items())]
        for neighborhood, by_date in neighborhood_timeline.items()
    }
    timeline_path = OUT_DIR / "gaza_city_neighborhood_damage_timeline.json"
    timeline_path.write_text(json.dumps(timeline_out, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Wrote {len(by_neighborhood)} neighborhood file(s) to {BY_NEIGHBORHOOD_DIR}/ ({total_bytes:,} bytes total)")
    for neighborhood, features in sorted(by_neighborhood.items(), key=lambda kv: -len(kv[1])):
        size = (BY_NEIGHBORHOOD_DIR / f"{slug(neighborhood)}.geojson").stat().st_size
        print(f"  {neighborhood}: {len(features)} sites, {size:,} bytes")
    print(f"Wrote {timeline_path} ({len(timeline_out)} neighborhoods)")
    if skipped_no_geom:
        print(f"Skipped {skipped_no_geom} feature(s) with no geometry")
    if skipped_no_history:
        print(f"Skipped {skipped_no_history} feature(s) with no dated passes at all")

if __name__ == "__main__":
    main()
