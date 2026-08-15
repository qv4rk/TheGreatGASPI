# Historical Geography Reconstruction — Research Prompt Pack

**Status: not run. Nothing in this repository's data was generated from
this pack yet.** This is a prompt pack for a *human* to run against a
research-capable model with real source access (archives, historical map
collections, academic literature) — one run per snapshot year, ten runs
total. It is deliberately not something GASPI's own harvesting pass
produces automatically: unlike `data/raw/` (which harvests each
institution's *own stated present-day position*, a thing a model can do
directly), reconstructing 1800s administrative geography requires
primary-source archival work no model should assert from memory.

**Do not treat this file's own prose as historical fact.** It is
instructions for how to go find out, not an answer.

## Why this exists

The Atlas can currently show real, present-day territory boundaries (see
`data/boundaries/`) for a growing subset of the 16 territories. It
cannot yet show what those boundaries were in 1832, or 1858, or 1925 —
that geography has to be reconstructed from period sources, snapshot by
snapshot, and every polygon needs a traceable evidence trail. Fabricating
that from a model's general knowledge would silently launder guesses
into the same schema that everywhere else in this project insists on
`"data not available"` over invented precision. This pack exists so
that doesn't happen.

## How to use this

1. Pick one target year from the table below.
2. Take the master prompt template, fill in `[INSERT YEAR]` and the
   year's regime-specific emphasis from the table.
3. Run it against a research model with live source access (not a
   model answering from parametric memory alone).
4. The output is **candidate** evidence, not a finished GASPI record.
   Review it, verify citations resolve to real sources, and only then
   turn confirmed results into a new file under `data/boundaries/`
   (using the same `geometry_status` / `confidence` / `source` /
   `source_url` / `license` shape already documented in the main
   README) or a new dated event under a future historical-events store.
5. Repeat for the next year. Each year is its own reconstruction regime
   — see the table — not a date substituted into an otherwise identical
   query. Running the same master prompt with only the year changed
   will under-specify what evidence actually exists for that period.

## Master prompt template

```
GREAT GASPI — HISTORICAL GEOGRAPHY RECONSTRUCTION ENGINE

TARGET REGION:
Historical Palestine / southern Levant, including the territory corresponding
to present-day Israel, West Bank, Gaza Strip, and adjacent Ottoman districts
where necessary to accurately reconstruct historical administration.

TARGET SNAPSHOT YEAR:
[INSERT YEAR]

REGIME FOR THIS YEAR:
[INSERT regime + source emphasis + special caveat from the table below]

OBJECTIVE:
Reconstruct the geographic and administrative landscape existing at or as
close as possible to [YEAR]. The output is intended for a temporal GIS /
historical atlas. Do NOT assume that modern political boundaries existed in
the target year. The purpose is not to retroactively impose modern borders
on historical geography.

============================================================
1. POLITICAL / ADMINISTRATIVE GEOGRAPHY
============================================================
Identify the sovereign or imperial authority governing the region.
Identify every documented administrative unit relevant to the target year:
province / eyalet / vilayet, sanjak, kaza, nahiye, district, subdistrict,
municipal jurisdiction, village jurisdiction, tribal/customary territory
where documented.
For each unit determine: historical name, Arabic name, Ottoman Turkish name
where applicable, transliteration, administrative parent, capital/seat,
approximate geographic extent, beginning date, ending date, source, and
whether the boundary is documented, reconstructed, or uncertain.

============================================================
2. POLYGON RECONSTRUCTION
============================================================
For every administrative or territorial unit for which a geographic extent
can reasonably be reconstructed, produce a GIS polygon.
Preferred geometry hierarchy: (1) digitized historical boundary, (2)
boundary reconstructed from a contemporary map, (3) boundary reconstructed
from archival administrative descriptions, (4) boundary reconstructed from
neighboring jurisdictions, (5) approximate historical extent.
NEVER fabricate precision. If the exact boundary cannot be established:
mark geometry_status = "approximate", provide uncertainty notes, identify
the evidence used, provide confidence = low/medium/high, and do not create
a false precise boundary.

============================================================
3. HISTORICAL MAP SOURCES
============================================================
Search specifically for maps produced during the target period, immediately
before it, and immediately after it. Prioritize: Library of Congress,
National Library of Israel, David Rumsey Historical Map Collection, Ottoman
archives, British Library, Palestine Exploration Fund, Survey of Palestine,
historical cadastral maps, Ottoman administrative maps, contemporary travel
maps, military survey maps.
Record: map title, cartographer, publication date, date depicted, scale,
archive, URL, license, relevant sheet/page, whether boundaries are explicit
or inferred.

============================================================
4. VILLAGES AND SETTLEMENTS
============================================================
Identify every historically documented village, town and city that can be
reliably associated with the target geography. For each: historical name,
alternate names, Arabic name, Hebrew name where historically appropriate,
Ottoman name/transliteration, latitude, longitude, administrative unit,
population if available, settlement status, source, source date.
Do NOT treat a modern coordinate as proof that the same administrative
territory existed historically.

============================================================
5. VILLAGE TERRITORY
============================================================
Where historical evidence permits, reconstruct the agricultural or
jurisdictional territory associated with each village. Distinguish:
built-up settlement, cultivated land, village lands, grazing/common land,
waqf land, state/miri land, private/mulk land, tribal/customary territory.
If no defensible polygon can be constructed, return the village as a point
rather than inventing a polygon.

============================================================
6. LEGAL LAND STATUS
============================================================
Identify the land-tenure regime operating at the target date. Record: miri,
mulk, waqf, metruke, mewat, other relevant categories. Identify relevant
legal instruments and administrative reforms. For 1858 specifically,
investigate the Ottoman Land Code and distinguish: legal purpose,
implementation, registration behavior, local resistance or avoidance,
consequences documented by primary sources, later scholarly interpretations.
Do not present a claimed causal relationship as established fact unless
supported by evidence.

============================================================
7. TEMPORAL CHANGES
============================================================
Identify changes from the preceding snapshot. For every boundary change
record: OLD UNIT, NEW UNIT, CHANGE DATE, TYPE OF CHANGE, LEGAL/ADMINISTRATIVE
BASIS, SOURCE.

============================================================
8. GIS OUTPUT
============================================================
Return GeoJSON-compatible records. Each Feature must contain:

{
  "type": "Feature",
  "properties": {
    "id": "",
    "name": "", "name_ar": "", "name_he": "", "name_ottoman": "",
    "snapshot_year": 0, "valid_from": "", "valid_to": "",
    "authority": "", "administrative_level": "", "parent_unit": "",
    "geometry_status": "documented|reconstructed|approximate",
    "confidence": "high|medium|low",
    "source_ids": [], "notes": ""
  },
  "geometry": { "type": "Polygon", "coordinates": [] }
}

If a polygon cannot be responsibly reconstructed, return
"geometry_status": "point_only" and provide the point separately.

============================================================
9. EVIDENCE RULE
============================================================
Every polygon must have an evidence trail. Never infer a historical
boundary solely from a modern political boundary. Never convert a GPS
point into a territorial polygon merely because the point lies inside a
modern region. Never silently substitute present-day geography for
historical geography. If sources disagree: return both interpretations.

============================================================
10. UNCERTAINTY
============================================================
HIGH: direct contemporary cartographic or administrative evidence.
MEDIUM: multiple historical sources permit a reasonable reconstruction.
LOW: reconstruction depends substantially on inference.
UNKNOWN: insufficient evidence to reconstruct.

============================================================
FINAL OUTPUT
Return: A. Historical administrative hierarchy. B. Historical settlements.
C. Polygon candidates. D. Point-only settlements. E. Boundary-change
events. F. Land-tenure system. G. Historical map sources. H. Conflicting
evidence. I. Unresolved questions. J. GeoJSON FeatureCollection.

Do not fill missing data with modern equivalents. Use "data not available"
where appropriate.
```

## Year-specific regimes

Each year is a different evidentiary regime, not the same query with a
different date. Fill the `REGIME FOR THIS YEAR` block above from this
table before running.

| Year | Regime | Source emphasis | Boundary confidence | Special caveat |
|---|---|---|---|---|
| 1800 | Late Ottoman, pre-Tanzimat | Ottoman eyalet/sanjak/kaza registers, qadi court records, early travel maps, Hughes 1843 as a close postdate | low/medium | Reconstruct Ottoman administrative geography only. No "Palestine" unit. No Mandate borders. |
| 1825 | Late Ottoman / pre-Egyptian invasion | Ottoman administrative records, early 19th-century European maps | low/medium | Many internal boundaries approximate. Southern/desert areas often "no documented boundary." |
| 1850 | Early Tanzimat, pre-1858 Land Code | Ottoman salnames, administrative maps, 1857 Rumsey map as near-contemporary | low/medium | Do not retroactively apply 1858 land categories. Village-level evidence usually point-based only. |
| 1875 | Post-1858 Land Code, post-1864 Vilayet Law | Ottoman cadastral/registration records, PEF 1880 survey, Ottoman provincial yearbooks | medium | Land tenure better documented; village territories still often reconstructed, not surveyed. |
| 1900 | Late Ottoman | 1899 Ottoman administrative-division map, PEF sheets, German/British surveys | medium/high for districts, low/medium for subdistricts | Formal boundaries improving; not all village lands surveyed. |
| 1925 | British Mandate | Mandate district maps, Survey of Palestine, 1922 census | high for districts, medium for village territories | Use Mandate administrative geography, not Ottoman continuation. |
| 1950 | Post-1948 | Armistice lines, Jordanian West Bank administration, Egyptian Gaza administration, Israeli administrative records | medium/high for armistice lines, low/medium for local boundaries | New political geography — do not derive from Ottoman or Mandate layers. |
| 1975 | Post-1967 occupation | Israeli military administration, Jordanian pre-1967 district references, refugee camp records, UN maps | medium/high for occupation boundaries, low/medium for local Palestinian administrative units | No clean sovereign "Palestine" polygon. Use occupation/administration boundaries explicitly. |
| 2000 | Oslo-era | Areas A/B/C, Palestinian Authority governorates, Israeli administrative divisions, barrier/access maps | medium/high | Separate sovereign, administrative, and control layers — do not collapse them into one line. |
| 2025 | Contemporary | PA governorates, Israeli districts, access/blockade zones, UN OCHA boundary data | high for reference boundaries, contested boundaries flagged | Current reference geography, not historical reconstruction — can mostly reuse `data/boundaries/` sourcing instead of this pack. |

## Geometry categories the output should distinguish

Don't force every snapshot into a single "border" line. Each year can
carry several independent geometries at once — collapsing them loses the
distinction between who *claims* a place, who *administers* it, and who
*controls it on the ground*, which is exactly the kind of flattening this
project exists to avoid elsewhere in the schema:

- `sovereignty`
- `administrative_boundaries`
- `local_jurisdictions`
- `village_territories`
- `land_tenure`
- `military_control`
- `internationally_recognized_boundary`
- `disputed_or_claimed_boundary`
- `uncertain_extent`

## Point events that don't fit a snapshot year

Some documented history (e.g. the 1834 Safed unrest and the Ein al-Zeitun
sheltering episode, or a specific earthquake) falls between snapshot
years and isn't a boundary question at all — it's a dated event anchored
to a place. Keep those as events layered *between* the surrounding
snapshots (e.g. 1825 and 1850 establish the geography; a 1834 event
animates something that happened inside it) rather than stretching a
snapshot year to cover them. Where a detail remains genuinely unresolved
after real research — an unnamed protector, a lost record — the record
should say so explicitly (`identification_status: "unresolved"`) rather
than have a model infer a plausible name. That is a feature of the
Atlas, not a gap to be silently closed.
