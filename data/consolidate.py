#!/usr/bin/env python3
"""
Consolidates the paired perspective research files in data/raw/ into the
flat per-territory JS DATA structure the GASPI page renders.

Each territory has (usually) two raw files — one per named perspective/
language. Rather than picking one, this keeps both: metrics that both
files report get cross-checked (kept as a range if they disagree, same
as West Bank/Gaza were handled by hand earlier); items that speak to a
specific incident or claim (physical barriers, environmental incidents)
carry an `accounts` array with each file's own perspective attributed
by name, not compressed into "official" vs "objection."

This is a first pass, not a hand-polished one — some incident-level
matching between the two files is approximate rather than a full
cross-reference engine. Flagged inline where that simplification happens.
"""
import json
import glob
import re
from pathlib import Path

RAW = Path(__file__).parent / "raw"
OUT = Path(__file__).parent / "consolidated.json"

def load_all():
    files = sorted(glob.glob(str(RAW / "P*.json")))
    docs = []
    for f in files:
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception as e:
            print(f"  SKIP (parse error) {f}: {e}")
            continue
        if not d or "territory_name" not in d:
            print(f"  SKIP (empty) {f}")
            continue
        d["_file"] = f
        docs.append(d)
    return docs

# P-number -> (canonical territory key, canonical display name). Grouped
# by hand from the protocols document's 16-location list, since each raw
# file names its own territory in its own perspective's language and
# fuzzy name-matching across scripts (Arabic/Chinese/Tibetan/Russian/...)
# isn't reliable enough to trust for merging.
P_TO_TERRITORY = {
    1: ("west-bank", "West Bank"), 2: ("west-bank", "West Bank"),
    3: ("gaza-strip", "Gaza Strip"), 4: ("gaza-strip", "Gaza Strip"),
    5: ("western-sahara", "Western Sahara"), 6: ("western-sahara", "Western Sahara"),
    7: ("transnistria", "Transnistria"), 8: ("transnistria", "Transnistria"),
    9: ("puerto-rico", "Puerto Rico"), 10: ("puerto-rico", "Puerto Rico"),
    11: ("northern-cyprus", "Northern Cyprus"), 12: ("northern-cyprus", "Northern Cyprus"),
    13: ("tibet", "Tibet"), 14: ("tibet", "Tibet"),
    15: ("guam", "Guam"), 16: ("guam", "Guam"),
    17: ("crimea", "Crimea"), 18: ("crimea", "Crimea"),
    19: ("jammu-kashmir", "Jammu & Kashmir"), 20: ("jammu-kashmir", "Jammu & Kashmir"),
    21: ("west-papua", "West Papua"), 22: ("west-papua", "West Papua"),
    23: ("xinjiang", "Xinjiang"), 24: ("xinjiang", "Xinjiang"),
    25: ("new-caledonia", "New Caledonia"), 26: ("new-caledonia", "New Caledonia"),
    27: ("american-samoa", "American Samoa"), 28: ("american-samoa", "American Samoa"),
    29: ("rojava-aanes", "Rojava / AANES"), 30: ("rojava-aanes", "Rojava / AANES"),
    31: ("nagorno-karabakh", "Nagorno-Karabakh"), 32: ("nagorno-karabakh", "Nagorno-Karabakh"),
}

def group_by_territory(docs):
    groups = {}
    canonical_names = {}
    for d in docs:
        m = re.search(r"/P(\d+)_", d["_file"])
        if not m:
            print(f"  WARN: couldn't parse P-number from {d['_file']}, skipping")
            continue
        pnum = int(m.group(1))
        key, canon_name = P_TO_TERRITORY.get(pnum, (slug(d["territory_name"]), d["territory_name"]))
        groups.setdefault(key, []).append(d)
        canonical_names[key] = canon_name
    return groups, canonical_names

def to_float(v):
    try:
        if isinstance(v, str) and "not available" in v.lower():
            return None
        return float(v)
    except (TypeError, ValueError):
        return None

def num_or_range(vals):
    """DEPRECATED — kept only so nothing else importing this module breaks.
    Silently merges values with no record of which perspective reported
    which one. Use attributed_metric() instead; see its docstring for why."""
    nums = [to_float(v) for v in vals if to_float(v) is not None]
    nums = sorted(set(nums))
    if not nums:
        return "data not available"
    if len(nums) == 1:
        return nums[0]
    return [nums[0], nums[-1]]

def attributed_metric(docs, getter):
    """Pull one numeric field from every doc in the territory group via
    getter(doc) -> raw value, WITHOUT losing which perspective reported
    which number. If every perspective that has a value agrees exactly,
    returns {"value": n} — one number, still traceable to how many
    perspectives confirm it. If they disagree, or only some report it,
    returns {"reports": [{"perspective": ..., "value": ...}, ...]} so the
    UI can show each account instead of a silently-picked number or an
    unattributed range."""
    reports = []
    for d in docs:
        raw = getter(d)
        v = to_float(raw)
        if v is not None:
            reports.append({"perspective": d.get("perspective", "data not available"), "value": v})
    if not reports:
        return {"value": "data not available"}
    distinct = {r["value"] for r in reports}
    if len(distinct) == 1:
        return {"value": reports[0]["value"], "confirmed_by": len(reports)}
    return {"reports": reports}

def slug(name):
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")

def _norm_name(s):
    return re.sub(r"\s+", " ", (s or "").strip().lower())

# A tiny, fixed geographic offset applied only when two perspectives share
# a coordinate but named it differently — just enough that both markers
# are independently visible and clickable at normal zoom, not so much
# that they read as two different places. ~0.0008 deg is roughly 80-90m.
_OFFSET = 0.0008

_OUT_OF_TERRITORY = re.compile(
    r"not (directly )?within|outside (the )?territory|regional (strategic )?context"
    r"|not part of|located outside|not in (the )?west bank",
    re.I,
)

def _is_flagged_out_of_territory(item):
    for field in ("functional_strategic_description", "stated_justification",
                   "opposing_characterization", "temporal_variations"):
        val = item.get(field)
        if isinstance(val, str) and _OUT_OF_TERRITORY.search(val):
            return True
    return False

def collect_points(docs, path_parts, fields):
    """Pull a list-of-dicts field (e.g. named_high_ground_features) from
    every doc in this territory's group.

    Two perspectives naming the same physical location differently is the
    finding, not noise — each gets its own marker, own full description,
    attributed to its own perspective. Only when both files use the exact
    same name at the same location is it shown once (nothing distinct to
    preserve). Coincident-but-differently-named points get a small fixed
    offset applied in opposite directions so both stay independently
    visible and clickable instead of rendering exactly on top of each other.
    """
    raw = []
    for d in docs:
        node = d
        for p in path_parts:
            node = node.get(p, {}) if isinstance(node, dict) else {}
        if not isinstance(node, list):
            continue
        for item in node:
            name = item.get("name") or item.get("zone_name") or ""
            lat, lng = to_float(item.get("lat")), to_float(item.get("lng"))
            if lat is None or lng is None:
                continue
            # A handful of items are the source document's own regional
            # context (e.g. Mount Hermon, cited under West Bank strategy
            # while explicitly noting it isn't in the West Bank) — plotting
            # those as a marker inside the territory misrepresents them, so
            # skip anything the document itself flags as not actually here.
            if _is_flagged_out_of_territory(item):
                continue
            row = {f: item.get(f, "data not available") for f in fields}
            row["name"] = name
            row["lat"], row["lng"] = lat, lng
            row["perspective"] = d.get("perspective", "data not available")
            raw.append(row)

    # Group by rounded coordinate (~1km) to find coincident points.
    by_coord = {}
    for row in raw:
        key = (round(row["lat"], 2), round(row["lng"], 2))
        by_coord.setdefault(key, []).append(row)

    out = []
    for key, rows in by_coord.items():
        distinct_names = {_norm_name(r["name"]) for r in rows}
        if len(rows) == 1 or len(distinct_names) == 1:
            # Either only one perspective reported this point, or every
            # perspective that did agrees on the name exactly — one marker.
            out.append(rows[0])
            continue

        # Different names at (near-)identical coordinates: one marker per
        # perspective, nudged apart so neither is hidden under the other.
        n = len(rows)
        for i, r in enumerate(rows):
            angle = (2 * 3.14159265 * i) / n
            r = dict(r)
            r["lat"] = r["lat"] + _OFFSET * (0.6 * round(_cos(angle), 3))
            r["lng"] = r["lng"] + _OFFSET * (0.6 * round(_sin(angle), 3))
            out.append(r)
    return out

def _cos(a):
    import math
    return math.cos(a)

def _sin(a):
    import math
    return math.sin(a)

def _with_perspective(note, perspective):
    note = note if (note and note != "data not available") else ""
    if not perspective or perspective == "data not available":
        return note or "data not available"
    tag = f"— per {perspective}"
    return f"{note} {tag}".strip() if note else tag

def _lead_note(*parts, perspective=None):
    """Join labeled text parts (skipping missing/empty ones) into one plain-
    text note, control/attribution info first — written for someone reading
    the marker list as text (screen reader or TTS), not looking at a colored
    dot on a map. A dot's color alone was never meant to carry meaning; this
    is the actual content that has to."""
    clean = []
    for label, val in parts:
        if val and val != "data not available":
            clean.append(f"{label}: {val}" if label else val)
    text = ". ".join(clean)
    return _with_perspective(text, perspective) if perspective else (text or "data not available")

def build_incidents(docs):
    incidents = []
    for d in docs:
        persp = d.get("perspective", "data not available")
        for inc in d.get("environmental_degradation_incidents", []) or []:
            accounts = []
            if inc.get("stated_justification"):
                accounts.append({
                    "party": persp,
                    "account": inc.get("stated_justification"),
                    "citations": inc.get("citations", []),
                })
            if inc.get("opposing_characterization"):
                accounts.append({
                    "party": "Documented opposing account (see source citations)",
                    "account": inc.get("opposing_characterization"),
                    "citations": inc.get("citations", []),
                })
            incidents.append({
                "type": inc.get("incident_type", "data not available"),
                "area": inc.get("affected_area_sqkm", "data not available"),
                "chemical_agents": inc.get("chemical_or_hazard_agents", []),
                "first_documented_year": inc.get("first_documented_year", "data not available"),
                "ongoing": inc.get("ongoing", "data not available"),
                "documenting_orgs": inc.get("documenting_orgs", []),
                "accounts": accounts,
            })
    return incidents

def build_legal(docs):
    """Each entry is attributed to the perspective whose file reported it.
    Two perspectives citing the same case/statute get two entries — same
    name, different perspective — since which side raises a given citation
    (and how it frames the holding) is itself part of the record. Only
    exact (name, perspective) duplicates within the source data collapse."""
    legal = []
    seen = set()
    for d in docs:
        persp = d.get("perspective", "data not available")
        jf = d.get("jurisprudence_and_statutory_friction", {}) or {}
        for case in jf.get("landmark_jurisprudence_and_treaties", []) or []:
            name = f"{case.get('case_or_resolution_name','')} ({case.get('year','')}) — {case.get('judicial_body_or_treaty','')}".strip()
            desc = case.get("holding_or_standard") or case.get("official_legal_rationale") or "data not available"
            key = (name, persp)
            if key in seen:
                continue
            seen.add(key)
            legal.append({"name": name, "desc": desc, "perspective": persp})
        for conf in jf.get("documented_statutory_conflicts", []) or []:
            name = conf.get("legal_domain", "Statutory conflict")
            desc = conf.get("conflict_description", "data not available")
            key = (name, persp)
            if key in seen:
                continue
            seen.add(key)
            legal.append({"name": name, "desc": desc, "perspective": persp})
    return legal

def build_territory(name, docs):
    center = docs[0].get("wgs84_center", {})
    perspectives = [d.get("perspective", "data not available") for d in docs]

    # zones don't have lat/lng so collect_points' dedupe-by-coords doesn't apply; built directly:
    zones = []
    seen_z = set()
    for d in docs:
        for z in d.get("topographic_and_control_data", {}).get("control_zones", []) or []:
            zn = z.get("zone_name", "")
            if zn in seen_z:
                continue
            seen_z.add(zn)
            zones.append({
                "name": zn,
                "pct": to_float(z.get("area_pct")) or 0,
                "governing_authority": z.get("governing_authority", "data not available"),
            })

    peaks = collect_points(docs, ["topographic_and_control_data", "named_high_ground_features"],
                            ["name", "lat", "lng", "elevation_m", "control_zone", "functional_strategic_description"])
    barriers_raw = collect_points(docs, ["topographic_and_control_data", "physical_barriers"],
                                   ["name", "lat", "lng", "length_km", "type",
                                    "stated_justification", "opposing_characterization"])
    checkpoints = collect_points(docs, ["infrastructure_and_logistics_data", "checkpoints_and_gates"],
                                  ["name", "lat", "lng", "permit_type_required", "stated_justification"])
    water = collect_points(docs, ["hydrology_data", "water_infrastructure"],
                            ["name", "lat", "lng", "controlling_entity", "capacity_or_flow_rate"])

    # Water consumption is reported per-perspective (each file's own read on
    # per-capita liters/day) rather than a single shared number — keep every
    # perspective's report distinct instead of taking the first non-empty one.
    water_reports = []
    for d in docs:
        wc = d.get("hydrology_data", {}).get("per_capita_water_consumption_l_d", {}) or {}
        if wc:
            # Kept as raw values (not coerced to float) — several files report
            # this as descriptive text ("Military population: approximately
            # 450-550 L/c/d...") rather than a clean number, and that detail
            # is exactly the kind of thing this project exists to preserve.
            water_reports.append({
                "perspective": d.get("perspective", "data not available"),
                "population_a": wc.get("population_a", "data not available"),
                "population_b": wc.get("population_b", "data not available"),
                "who_reference_standard": wc.get("who_reference_standard", "data not available"),
            })

    incidents = build_incidents(docs)
    legal = build_legal(docs)

    sources = set()
    for d in docs:
        for inc in d.get("environmental_degradation_incidents", []) or []:
            for org in inc.get("documenting_orgs", []) or []:
                sources.add(org)

    return {
        "name": name,
        "sub": " · ".join(dict.fromkeys(perspectives)),
        "center": {"lat": to_float(center.get("lat")) or 0, "lng": to_float(center.get("lng")) or 0},
        "metrics": {
            "area_sqkm": attributed_metric(
                docs, lambda d: d.get("topographic_and_control_data", {}).get("total_area_sqkm")),
            "food_import_pct": attributed_metric(
                docs, lambda d: d.get("hydrology_data", {}).get("agriculture", {}).get("food_import_dependency_pct")),
            "water": {"reports": water_reports} if water_reports else {"value": "data not available"},
        },
        "zones": zones,
        # Every note leads with who controls / operates / justifies the thing,
        # in plain text — not left to marker color to imply. Someone reading
        # this list with a screen reader or TTS gets the same information as
        # someone looking at the map.
        "peaks": [{"name": p["name"], "lat": to_float(p["lat"]) or 0, "lng": to_float(p["lng"]) or 0,
                    "elev": p.get("elevation_m"),
                    "note": _lead_note(
                        ("Control zone", p.get("control_zone")),
                        ("Strategic significance", p.get("functional_strategic_description")),
                        perspective=p.get("perspective"))}
                   for p in peaks if to_float(p.get("lat"))],
        "checkpoints": [{"name": c["name"], "lat": to_float(c["lat"]) or 0, "lng": to_float(c["lng"]) or 0,
                          "note": _lead_note(
                              ("Permit required", c.get("permit_type_required")),
                              ("Stated justification", c.get("stated_justification")),
                              perspective=c.get("perspective"))}
                         for c in checkpoints if to_float(c.get("lat"))],
        "water": [{"name": w["name"], "lat": to_float(w["lat"]) or 0, "lng": to_float(w["lng"]) or 0,
                    "note": _lead_note(
                        ("Controlled by", w.get("controlling_entity")),
                        ("Capacity", w.get("capacity_or_flow_rate")),
                        perspective=w.get("perspective"))}
                   for w in water if to_float(w.get("lat"))],
        "barriers": [{"name": b["name"], "lat": to_float(b["lat"]) or 0, "lng": to_float(b["lng"]) or 0,
                       "note": _lead_note(
                           ("Length", f"{b.get('length_km','?')} km" if b.get("length_km") not in (None, "data not available") else None),
                           ("Type", b.get("type")),
                           ("Stated justification", b.get("stated_justification")),
                           ("Opposing characterization", b.get("opposing_characterization")),
                           perspective=b.get("perspective"))}
                      for b in barriers_raw if to_float(b.get("lat"))],
        "incidents": incidents,
        "legal": legal,
        "sources": sorted(sources),
    }

def main():
    docs = load_all()
    print(f"Loaded {len(docs)} populated research files")
    groups, canonical_names = group_by_territory(docs)
    print(f"Grouped into {len(groups)} territories:")
    for key, ds in groups.items():
        print(f"  - {canonical_names[key]} ({key}): {len(ds)} perspective file(s)")

    result = {}
    for key, ds in groups.items():
        result[key] = build_territory(canonical_names[key], ds)

    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {OUT}")

if __name__ == "__main__":
    main()
