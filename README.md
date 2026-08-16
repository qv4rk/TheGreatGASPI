# The Great GASPI

*Global Asymmetric Sovereignty & Power Index*

A geospatial platform mapping structural power asymmetry — territorial
control, water access, checkpoints, physical barriers, environmental
damage, and legal jurisdiction — across 16 contested or occupied
territories.

## What this actually is

`frontend/index.html` is a single self-contained, static HTML page. No
build step, no backend, no database. It loads a MapLibre GL globe and
renders per-territory data that's baked directly into the page.

That data comes from `data/raw/`: paired research documents, one per
named institutional perspective per territory (government bodies,
international organizations, advocacy groups — always attributed by
name, never reduced to "side A / side B"). `data/build_territories.py`
assembles those into `data/territories.json`, which
`data/splice_frontend.py` writes into the page's embedded `const DATA =
{...}` object (a repo-maintenance step; the deployed page itself is
still a single static file with no build step at request time). Nothing
gets shrunk or picked-between in that step — every perspective's data
stays in the output, attributed to its source; see
`data/supplementary_points.json` for coordinates found afterward to fill
map gaps, kept clearly separate from the original 32-file research.

Territory extent on the map defaults to a circle sized from the
territory's own reported area — approximate, and labeled as such in the
legend. `data/boundaries/<territory-key>.geojson` can override that with
a real administrative boundary polygon for a territory: a plain GeoJSON
Feature carrying `geometry_status` (`documented|reconstructed|approximate`),
`confidence` (`high|medium|low`), `source`, `source_url`, and `license`
in its properties. `build_territories.py` attaches it to that
territory's `boundary` field automatically if the file exists; nothing
else changes. These polygons are present-day administrative extents
only, sourced independently of the perspective research — never a
historical reconstruction, and never inferred from a GPS point. West
Bank and Gaza Strip currently have one, sourced from Natural Earth's
public-domain admin-0 map subunits; the other 14 territories still fall
back to the circle until a real polygon is curated for them the same
way.

The design intent: each perspective's account is told in full, in its
own terms — not merged, not averaged, not compressed into "official
justification" vs. "objection." Where two perspectives report different
numbers, or name the same location differently, both are shown,
attributed to their source. Composite sovereignty scoring is
deliberately not computed by AI research passes — only by a fixed
deterministic formula applied identically to every territory, and it is
not yet implemented in the live page.

The live, deployed copy of this page is maintained in the author's
portfolio site repository, not here — this repo is the source and the
data pipeline.

## GASPI 2.0 — the evidence model

1.x's per-territory record is a flat JSON blob: a claim and its rebuttal
live as two string fields (`stated_justification` /
`opposing_characterization`) on whatever record they're about, and
`sources` is one unattributed list of names for the whole territory.
That was never meant to be the end state — GASPI has always been research
documents feeding a renderer, built to grow. 2.0 is that growth: claims,
measurements, sources, and judicial findings become their own
addressable, ID-linked records, so a claim can point at exactly the
sources that back it, a number can carry the population it actually
describes, and a documented judicial finding is kept distinct from an
actor's own characterization of events.

- `research/GASPI_2.0_DATA_MODEL_SPEC.md` — the entity model (Actor,
  Perspective, Claim, Measurement, Source, Finding, Dispute, Unknown),
  worked out against real West Bank data, including the exact bug
  (`population_a`/`population_b` silently meaning different things in
  different perspective files) that motivated the Measurement entity.
- `data/schema/gaspi_2_0.schema.json` — the JSON Schema implementing that
  spec.
- `data/migrate_to_2_0.py` — a first-pass migration script, piloted on
  West Bank only. It converts `data/raw/` into `data/v2/<territory>.json`
  and prints a review report for everything it couldn't do mechanically
  (citation strings that need resolving to real sources, actor types it
  had to guess, perspective labels that bundle multiple institutions into
  one Actor). It is not a general migrator run across all 16 territories
  yet, and its output should not be treated as more authoritative than
  `data/raw/` until the flagged items get a human pass.
- The frontend's presentation layer (mode toggle: All / Single
  perspective / Compare; perspective comparison rail; source-chain
  drawer) reads `data/v2/<territory>.json` when it exists for the active
  territory, and falls back to the 1.x-derived summary otherwise —
  visibly, via a "GASPI 2.0 pilot" badge, not silently.

## Repository layout

```
data/
  raw/                       research documents, one per perspective per territory
  boundaries/                real administrative boundary polygons, one GeoJSON Feature
                              per territory-key.geojson — present-day extent only, sourced
                              independently of data/raw/; absent for territories that don't
                              have one yet (those fall back to the map's circle mask)
  v2/                        GASPI 2.0 evidence-model output (see above), one file per
                              migrated territory — currently west-bank.json only
  schema/gaspi_2_0.schema.json  JSON Schema for data/v2/
  build_territories.py       assembles territories.json from data/raw/ (+ data/boundaries/)
  migrate_to_2_0.py          first-pass 1.x -> 2.0 migrator, piloted on West Bank
  splice_frontend.py         writes territories.json + data/v2/ into frontend/index.html
  territories.json           output — consumed by frontend/index.html
  supplementary_points.json  coordinates found afterward to fill map gaps — kept
                              separate from data/raw/, never presented as if they
                              were part of the original perspective research
  *.zip, *.pdf                UNOSAT satellite damage assessment source files (not yet integrated)
frontend/
  index.html                  the site itself
research/
  GASPI_Complete_Prompts_Protocol.md   the 1.x research protocol used to generate data/raw/
  GASPI_2.0_DATA_MODEL_SPEC.md         the 2.0 evidence-model spec
  HISTORICAL_GEOGRAPHY_RECONSTRUCTION_PROMPTS.md   research prompts for historical (pre-2025)
                                                    boundary reconstruction — not yet run
```

After editing `data/raw/` or `data/boundaries/`, regenerate and re-embed with:

```
python3 data/build_territories.py
python3 data/migrate_to_2_0.py west-bank   # re-run only if data/raw/ West Bank files changed
python3 data/splice_frontend.py
```

## Status

3 of 16 territories are missing a perspective file (Crimea, New
Caledonia, Rojava/AANES) and are marked accordingly rather than
filled in with placeholder data. Several fields across all territories
read "data not available" where the underlying research didn't have an
answer — that's reported as-is, not backfilled.

2 of 16 territories (West Bank, Gaza Strip) have a real sourced boundary
polygon in `data/boundaries/`; the other 14 still render as the
approximate circle mask until one is curated for them.

1 of 16 territories (West Bank) has been migrated to the GASPI 2.0
evidence model, as a first pass with 29 items flagged for human review —
see `data/migrate_to_2_0.py`'s review report. The other 15 render from
1.x data only.

## License

MIT — see [LICENSE](LICENSE).
