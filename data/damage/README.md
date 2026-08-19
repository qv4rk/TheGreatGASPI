# Gaza City damage-over-time — proof of concept

## What's here

`extract_unosat_gaza_city.py` reads UNOSAT/OCHA's Gaza City Comprehensive
Damage Assessment (22–23 September 2025 release — already sitting in
`data/_static_unosat_filesystem_4205_..._GDB.zip`, a real ESRI File
Geodatabase, not fetched over the network) and reshapes it into:

- `by_neighborhood/<neighborhood-slug>.geojson` — one file per Gaza City
  neighborhood (16 total, ~25MB combined, largest single file ~5.4MB), each
  a point-per-damage-site FeatureCollection with a compact per-site
  history: `h: [[date, damage_class_code, confidence_id, status_code], ...]`,
  oldest pass first. UNOSAT's own schema already tracks up to 14 dated
  satellite passes per site (Oct 2023 → Sept 2025) as repeated columns;
  this reshapes that into an explicit array instead of collapsing it to
  one latest value, so a time slider has something to actually animate.
  Code → label legend is embedded once per file (`legend` key), not
  repeated per feature.
- `gaza_city_neighborhood_damage_timeline.json` — for every neighborhood
  and every assessment date, a count of sites by damage class. This is
  the flagship "destruction accumulating over time" chart data, and
  doesn't require building-footprint geometry to already be useful.

## Real numbers, as a sanity check

Az Zaitoun (9,296 sites, the largest neighborhood in this file) goes from
33 destroyed / 123 possible-damage sites on 2023-10-15 to 4,072 destroyed
on 2025-09-22, across 11 dated satellite passes. Every number in that
trajectory is directly readable from `gaza_city_neighborhood_damage_timeline.json`.

## Building footprints (Az Zaitoun pilot)

`raw_osm_buildings/az-zaitoun.geojson` — real OSM building footprints for
Az Zaitoun, fetched via OSMnx outside this sandbox (network-blocked here;
see `colab_fetch_buildings_by_neighborhood.py`) and uploaded in.
14,305 buildings.

`join_buildings_to_damage.py` matches each UNOSAT damage point to a
building: first by point-within-polygon, then nearest building within
20m for points that don't land inside one. Damage points with no building
within 20m stay as their own point features — most likely the structure
was destroyed before OSM's mappers (heavily updated by the 2024 HOT
campaign) could capture a footprint for it, not that the assessment is
wrong. A building can carry more than one matched damage site; every one
is kept, never averaged into a single value.

For Az Zaitoun: 6,583/9,296 damage points matched (70.8%) — 5,336 directly
inside a building, 1,247 to the nearest building within 20m. 5,580 of the
14,305 buildings (39%) carry at least one UNOSAT damage record; the rest
have none, meaning "not individually assessed," not "confirmed intact."
792 buildings matched more than one damage site.

Output: `joined/az-zaitoun_buildings.geojson` (7.5MB) and
`joined/az-zaitoun_unmatched_points.geojson` (1.7MB).

**Live view:** the `v` repo's `gaza-damage/az-zaitoun.html` renders this
with a real building map and a turn-to-scrub time dial across all 15
dated assessment passes.

## What this is not yet

- **Only one neighborhood joined so far.** The other 15 Az Zaitoun-sized
  neighborhoods need their own OSM buildings fetch (same Colab script,
  different neighborhood) and a `join_buildings_to_damage.py` run each.
- **Damage-class and status code meanings are provisional.** 1–4 map to
  UNOSAT's well-documented standard scheme (Destroyed / Severe / Moderate
  / Possible), inferred from public UNOSAT methodology and this file's own
  value distribution — not confirmed against this release's own
  coded-value domain table (GDAL's CLI tools failed to install in this
  sandbox on an unrelated missing package, not a data problem). A small
  number of sites carry codes outside 1–4 (6, 11) and are left
  "Unclassified" rather than guessed at.
- **`EventCode` has two near-identical values** (`CE20231007PSE` and
  `CE202301007PSE`) that read as a data-entry typo of the same underlying
  event rather than two real events. Kept as-is per feature; not silently
  "corrected."
- **`SiteID` is not a unique feature key** — multiple distinct points
  share the same SiteID (it's a damage-site cluster ID). Every point is
  kept as its own feature.
- **No frontend yet.** This is data extraction only — the actual
  time-slider / chart UI that renders `by_neighborhood/` and
  `gaza_city_neighborhood_damage_timeline.json` hasn't been built.

## Regenerating

```
python3 data/damage/extract_unosat_gaza_city.py
```

Reads from the already-unzipped GDB path hardcoded at the top of the
script (this sandbox unzipped it to `/tmp`, which won't survive a fresh
session — re-unzip `data/_static_unosat_filesystem_4205_..._GDB.zip`
first and update `GDB` in the script, or generalize that path before
running this elsewhere).
