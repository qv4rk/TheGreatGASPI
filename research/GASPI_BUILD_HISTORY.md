# GASPI — Build History: From "Circles, Not Polygons" to Today

Companion to `GASPI_NEW_REQUIREMENTS.md` (which covers the current research-methodology-overhaul phase). This document covers the earlier arc: the original diagnosis of why territories rendered as circles instead of real borders, the vertical slice proposed to fix it, and what actually got built afterward — traced against the record, not reconstructed from memory of intentions.

---

## 1. The original diagnosis

Before any of the work below, the actual gap was checked directly against the code rather than assumed:

- `control_zones` in the GASPI schema had `zone_name`, `area_pct`, `governing_authority` — **no geometry field at all.**
- The only polygon anywhere in the frontend was `circlePolygon()` — a synthetic circle punched around each territory's center point to make a spotlight mask. Every territory on the map, including West Bank and Gaza, was a circle, not a border.
- Conclusion at the time: "GPS coordinates are dots, borders are circles" wasn't a perception problem — it was the only geometry type that existed anywhere in the pipeline. A precise, fixable diagnosis, not a vague one.

Also confirmed at the same time, and worth preserving because it was a real finding, not just praise: `GASPI_Complete_Prompts_Protocol.md` and `build_territories.py` already did most of what a separately-reviewed "different AI" proposal was reinventing from scratch — dual named perspectives (never "side A/side B"), mandatory `stated_justification` + `opposing_characterization` on every barrier/restriction, "data not available" instead of invented numbers, and `attributed_metric()` / `collect_points()` deliberately refusing to merge disagreeing reports into one number — when two perspectives report different figures for the same thing, both survive into `territories.json` as separate attributed entries rather than being averaged or picked. That mechanism predates and is more disciplined than most external proposals that have since tried to solve the same problem (see `GASPI_NEW_REQUIREMENTS.md` §3 for the most recent example of that pattern repeating).

Also on record from the same review: `app/dial.js` + `app/data.js` were already a working orrery driven off real Julian-date math, and `data/events.json` already had dated, geo-anchored narrative events — n01 (Safed 1834) was cited then as an example, sourced, with the unnamed sheikh preserved as unresolved rather than guessed at. (n01 has since been read in full in this conversation and independently confirmed to hold up — see the empathy/craft review earlier in this thread.)

---

## 2. The vertical slice that was proposed

Four items, deliberately scoped to what was buildable soon versus what needed a slower, separate research track:

1. **Schema:** add a real geometry field (Point/LineString/Polygon) + `geometry_status` + `confidence` to `control_zones` and a new boundary object. Small, additive change.
2. **Render actual polygons for today's well-sourced boundaries first** — West Bank Areas A/B/C, Gaza governorates, OCHA/UN-sourced, not reconstructed — to kill the circle problem with zero historical-research risk.
3. **Wire the dial to swap layers**, starting with 3-4 well-documented snapshots (1948 armistice, 1967, 1993 Oslo, present) rather than all ten proposed Ottoman-era years.
4. **Treat 1800-1900 as an events layer, not a polygon layer** — Safed 1834, the 1837 earthquake, the 1858 Land Code slot into `events.json`'s existing point+narrative pattern. Polygon reconstruction for that era stays a slower, separate research track.

Explicit warning attached at the time: a ten-snapshot Ottoman-to-present polygon reconstruction is a research project measured in weeks, and running that research pack would mostly return `point_only` / low-confidence results for 1800-1850 specifically — correct, but not something to schedule alongside "ASAP." Israel/Palestine boundary geometry specifically was flagged as needing more sourcing rigor than most other GASPI territories, since an AI-approximated polygon that drifts from its cited source is exactly the kind of thing that reads as bias to a skeptical reader.

---

## 3. What actually got built, item by item

| Proposed item | Status | What happened |
|---|---|---|
| 1. Geometry field in schema | ✅ Built | Schema extended with real geometry fields. |
| 2. Real present-day boundaries, West Bank + Gaza first | ✅ Built | Real boundary polygons sourced and wired into `build_territories.py`; frontend renders them, with the circle mask kept as an explicit **fallback** for territories that don't have sourced geometry — this was a pilot for West Bank + Gaza specifically, not all 16 GASPI territories. The other 14 territories still render as circles as of this writing. |
| 3. Dial wired to swap boundary layers across historical snapshots | ❌ **Not built** | No task, commit, or code exists for this. `dial.js` remains an astronomical orrery (planetary/zodiac display via Julian-date math) with no connection to `territories.json` or historical boundary snapshots. "Turn the dial, watch borders change across 1948/1967/1993/present" was proposed and never implemented. Still open. |
| 4. Treat 1800s as events, not polygons | ✅ Built (partially, as intended) | A ten-year-snapshot historical-reconstruction research **prompt pack** was drafted — the research track itself, not yet run to produce actual polygons, exactly as scoped ("a slower, separate research track feeding in later"). Separately, n01 (Safed 1834) shipped as a real events.json node with full sourcing, matching the "events layer" recommendation directly. |

---

## 4. What came after the vertical slice — the GASPI 2.0 evidence model

Once the circle-vs-polygon gap was closed for West Bank + Gaza, the project moved to a deeper structural problem than geometry: how to represent competing claims about the same fact without collapsing them into one number or one narrative. This produced a new, more general layer on top of (not replacing) the `attributed_metric()`/`collect_points()` mechanism praised in §1:

- A full **GASPI 2.0 Data Model Specification** — Actor / Perspective / Claim / Measurement / Source / Finding / Dispute as distinct entity types, a real vocabulary for the "don't merge disagreeing reports" instinct the original pipeline already had.
- A **JSON Schema** for the above.
- A **1.x → 2.0 migration script**, run and piloted on **West Bank only** — not the other 15 territories. This matters for scope: the live site's GASPI 2.0 UI (mode toggle, perspective rail, source drawer) only shows real migrated Claims for West Bank; every other territory falls back to 1.x-style rendering, by design, not as a bug.
- The **G2 UI layer** — the ALL/SINGLE PERSPECTIVE/COMPARE mode toggle, the perspective comparison rail, and the source-chain drawer — built and merged on top of the existing map.

This is also where the perspective-mislabeling bug documented in `GASPI_NEW_REQUIREMENTS.md` §2 was eventually found — inside the West Bank pilot migration, in the legal/jurisprudence section specifically.

---

## 5. What came after that — Gaza damage-over-time, and site-wide fixes

Documented in detail via commit history and PRs in the `V` repo; summarized here only to keep this document's timeline complete:

- A real UNOSAT-satellite-damage-assessment-to-OSM-building-footprint join pipeline, covering 15 of Gaza City's 16 UNOSAT-assessed neighborhoods (the 16th, At Turukman, held back after a real coordinate-offset bug was found in its source data rather than shipped as if it were good), rendered as a toggleable map layer with a real 3D building-height extrusion driven by each building's actual damage classification over time.
- A mobile UI fix for a perspective panel that covered the entire screen with no way to dismiss it.
- Hebrew and Arabic translations of the site's historical article content, and a site-wide rename from "Manifold Atlas" to "The Atlas."
- Removal of internal QA/confidence-flag language ("NEEDS REVIEW," "UNVERIFIED," "GASPI 2.0 pilot") that had been leaking from migration-script metadata onto the public-facing site.

## 6. Current phase

The research-methodology overhaul — isolated single-perspective source documents, the perspective-mislabeling bug's full scope, and the proposed (not yet built) structural purity check — is covered in full in `GASPI_NEW_REQUIREMENTS.md`. Not duplicated here.

---

## 7. Still open, from the original plan specifically

- **The dial has never been wired to swap boundary/territory layers.** This was proposed, scoped conservatively (3-4 historical snapshots, not ten), and never built. Still real, still cheap relative to the historical-geometry research itself — the plumbing is a `loadHistoricalLayer(year)` call keyed off the dial's existing date state, separate from and much cheaper than producing the historical geometry itself.
- **Real boundary polygons exist for West Bank + Gaza only.** The other 14 GASPI territories still render with the circle-mask fallback.
- **The GASPI 2.0 evidence model migration has only been run on West Bank.** Gaza and every other territory still render via the 1.x path.
- **The ten-year-snapshot historical polygon reconstruction pack was drafted, never run.** 1800-1850 boundary geometry for the Ottoman-era snapshots does not exist yet, correctly, because it was never supposed to be rushed.
