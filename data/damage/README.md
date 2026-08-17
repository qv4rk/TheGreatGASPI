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

## What this is not yet

- **Points, not building polygons.** Each feature is a UNOSAT-assessed
  damage site (a point), not a real structure footprint. Joining these
  onto actual building outlines (e.g. HOTOSM's Palestine buildings layer)
  is the natural next step — this sandbox's network policy blocks
  `data.humdata.org`, Overpass, and Geofabrik outright (confirmed via the
  proxy's own rejection log), so that file needs to be supplied locally
  before the join can happen.
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
