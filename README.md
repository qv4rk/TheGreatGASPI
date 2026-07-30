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
assembles those into `data/territories.json`, which gets spliced into
the page's embedded data object. Nothing gets shrunk or picked-between
in that step — every perspective's data stays in the output, attributed
to its source; see `data/supplementary_points.json` for coordinates
found afterward to fill map gaps, kept clearly separate from the
original 32-file research.

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

## Repository layout

```
data/
  raw/                       research documents, one per perspective per territory
  build_territories.py       assembles territories.json from data/raw/
  territories.json           output — consumed by frontend/index.html
  supplementary_points.json  coordinates found afterward to fill map gaps — kept
                              separate from data/raw/, never presented as if they
                              were part of the original perspective research
  *.zip, *.pdf                UNOSAT satellite damage assessment source files (not yet integrated)
frontend/
  index.html                  the site itself
research/
  GASPI_Complete_Prompts_Protocol.md   the research protocol used to generate data/raw/
```

## Status

3 of 16 territories are missing a perspective file (Crimea, New
Caledonia, Rojava/AANES) and are marked accordingly rather than
filled in with placeholder data. Several fields across all territories
read "data not available" where the underlying research didn't have an
answer — that's reported as-is, not backfilled.

## License

MIT — see [LICENSE](LICENSE).
