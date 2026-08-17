# GASPI 2.0 — Data Model Specification

**Status: spec. Nothing in `data/` conforms to this yet.** This defines the
target shape before any JSON Schema or migration script gets written, per
the build order in `GASPI_2.0_Design_Blueprint.md` (spec → schema →
migration → renderer) — writing the schema first would let field names
lock in before the actual relationships are understood, which is how 1.x
ended up with `population_a`/`population_b` (see §4 below for exactly what
that cost).

GASPI has never been a static blob by design choice — it has always been
research documents feeding a renderer, meant to grow. 1.x's limitation was
never "should this grow a real data layer," it was that the growth path
was blocked on one thing: **claims, measurements, and sources have no
stable identity.** A `note` string can say who claimed what, but nothing
can point *at* that claim from an article, a dispute record, or a second
perspective's rebuttal. 2.0 gives every one of those a stable ID. That's
the whole change; everything else in this document follows from it.

## 0. Grounding example

Every entity below is defined against one real case already sitting in
`data/raw/P1_West_Bank_12of12.json` and `data/raw/P2_الضفة_الغربية_12of12.json`
— the Separation Barrier — because a spec written from invented examples
tends to omit the field some real record actually needs. Where a design
choice was driven by a specific gap found in the real files, that's noted
inline.

## 1. Entities

### 1.1 Actor

Who is speaking, controlling, documenting, claiming, or being described.
Not the same as a Perspective (§1.2) — one Actor's positions can be
represented across multiple perspectives, and one perspective document
cites many Actors it doesn't speak for.

```json
{
  "id": "actor:icj",
  "name": "International Court of Justice",
  "actor_type": "judicial_body",
  "jurisdiction": "international",
  "notes": ""
}
```

`actor_type` enum: `state`, `sub_state_authority`, `judicial_body`,
`intergovernmental_body`, `ngo`, `press`, `academic`, `armed_actor`,
`population_group`, `company`, `unattributed`.

For NGOs/institutions specifically, the blueprint's §15 accountability
fields (`legal_name`, `entity_type`, `incorporation_jurisdiction`,
`funding_disclosures`, etc.) attach here as optional properties on an
Actor record — deliberately **not required**, because most Actors cited
in `data/raw/` today (e.g. "EcoMENA", "Peace Now") don't have that
research done yet, and 2.0 must not silently downgrade an Actor to
"untrustworthy" just because its accountability record is still empty.
Absence of this data is `unresearched`, not `flagged`.

### 1.2 Perspective

The documentary viewpoint under which a GASPI research pass was run.
This already exists in 1.x as the top-level `perspective` field in each
`data/raw/*.json` file — 2.0 gives it an ID so Claims can reference it
directly instead of Claims and Perspectives both living as loose text
inside the same document.

```json
{
  "id": "perspective:west-bank:israel-civil-administration",
  "territory": "west-bank",
  "represented_actor": "actor:israel-state",
  "label": "State of Israel / Civil Administration",
  "research_language": "he",
  "source_language_reason": "Primary documentary language of the represented institution",
  "years_of_scope": "1967-2026",
  "original_text_preserved": false,
  "literal_translation": false,
  "contextual_translation": true
}
```

The `original_text_preserved` / `literal_translation` /
`contextual_translation` flags are honest right now: `data/raw/`'s two
West Bank files are each already fully in one language (Hebrew-sourced
content presented in English prose, Arabic-sourced content presented in
Arabic) — neither preserves original-language quotations alongside a
literal English rendering. That's not a 2.0 migration-script job; it's a
research-protocol change (§9 below), and the flags exist so the interface
can say "translation methodology not yet applied to this perspective"
instead of implying a rigor that isn't there.

### 1.3 Claim

A proposition attributed to a Perspective. This is the entity 1.x is
missing entirely — `stated_justification` and `opposing_characterization`
are inline strings on a barrier/incident/zone record, not addressable
objects.

```json
{
  "id": "claim:west-bank:separation-barrier:justification:israel-civil-administration",
  "territory": "west-bank",
  "perspective": "perspective:west-bank:israel-civil-administration",
  "subject": "physical_barrier:west-bank:separation-barrier",
  "claim_type": "justification",
  "text": "The barrier is necessary to protect Israeli civilians from Palestinian terrorism; suicide bombings declined by over 90% in the 11 months after the first continuous segment was completed.",
  "supporting_measurements": ["measurement:west-bank:suicide-bombings-pre-post-barrier"],
  "sources": ["source:west-bank:israeli-supreme-court-2004-barrier-ruling"],
  "status": "documented"
}
```

```json
{
  "id": "claim:west-bank:separation-barrier:characterization:opposing",
  "territory": "west-bank",
  "perspective": "perspective:west-bank:israel-civil-administration",
  "subject": "physical_barrier:west-bank:separation-barrier",
  "claim_type": "characterization",
  "text": "Opponents argue the barrier's route deviates substantially from the Green Line and is an illegal attempt to annex Palestinian land under the guise of security.",
  "sources": ["source:west-bank:icj-2004-advisory-opinion"],
  "status": "documented"
}
```

Note this Claim's `perspective` is the *Israeli* perspective document, not the
Palestinian one — deliberately. `stated_justification` and
`opposing_characterization` are both fields on the same 1.x record, written
by whichever institution's research pass produced that record; the
`opposing_characterization` text is that document's own paraphrase of what
opponents say, not an independently sourced quote from the Palestinian
perspective's own file. Attributing it to `perspective:west-bank:israel-civil-administration`
records who reported it, which is what's actually known. Attributing it to
the Palestinian perspective as if that perspective's own research produced
it would be a fabricated attribution — exactly the failure mode §17
("Courtroom-accounts principle") exists to prevent. `build_territories.py`
already gets this right today: `opposing_characterization` is attributed to
a generic `"Documented opposing account (see source citations)"` label, not
to a named party. A future research pass that goes and finds the Palestinian
perspective's *own* primary-sourced statement on the same subject can then
add a second, independently attributed Claim — that's a research task, not
something a migration script should assert on its own.

`claim_type` enum: `justification` (an actor's stated reason for its own
action), `characterization` (an actor's description of someone else's
action or a situation), `factual_assertion`, `allegation`, `denial`.
This is what replaces `stated_justification` / `opposing_characterization`
as fixed slots on every record type — instead, any number of Claims of
any type can attach to a `subject`, from any number of perspectives, so a
third or fourth perspective on the same subject doesn't require a schema
change to add a third string field.

`status` uses the vocabulary from Design Blueprint §13
(`documented|verified|corroborated|partially_verified|contested|disputed|unverified|not_yet_researched|source_only_claim`)
— never collapsed to true/false.

### 1.4 Measurement

A numerical observation, kept structurally separate from Claim because a
number needs a denominator and a population before it means anything —
and 1.x's own data shows exactly what happens when it doesn't.

**The motivating bug:** `data/raw/P1_West_Bank_12of12.json` records
`per_capita_water_consumption_l_d: {"population_a": "242", "population_b": "73"}`.
`data/raw/P2_الضفة_الغربية_12of12.json` — the Palestinian-perspective file
for the *same territory, same metric* — records
`{"population_a": 73, "population_b": 242}`. Both files report the same
two real numbers (242 and 73 liters/person/day). Which one is
`population_a` flips depending on which file you're reading, because
`population_a`/`population_b` are anonymous slots with no attached
identity — `build_territories.py` currently has no way to know these two
reports describe the same underlying reality with the labels swapped,
so it stores them as if they were four independent numbers across two
perspectives. A Measurement record makes the population identity a
required field instead of a positional convention:

```json
{
  "id": "measurement:west-bank:per-capita-water-consumption:settlers",
  "territory": "west-bank",
  "metric": "per_capita_water_consumption",
  "unit": "liters_per_person_per_day",
  "value": 242,
  "population": {
    "group": "Israeli settlers in West Bank",
    "actor": "actor:israeli-settlers-west-bank"
  },
  "period": "data not available",
  "reported_by": [
    "perspective:west-bank:israel-civil-administration",
    "perspective:west-bank:palestinian-civil-authorities"
  ],
  "sources": ["source:west-bank:ecomena", "source:west-bank:palestinian-hydrology-group"],
  "corroboration": "confirmed_by_2_perspectives",
  "who_reference_standard": 100.0
}
```

```json
{
  "id": "measurement:west-bank:per-capita-water-consumption:palestinians",
  "territory": "west-bank",
  "metric": "per_capita_water_consumption",
  "unit": "liters_per_person_per_day",
  "value": 73,
  "population": {
    "group": "Palestinians in the West Bank",
    "actor": "actor:palestinians-west-bank"
  },
  "period": "data not available",
  "reported_by": [
    "perspective:west-bank:israel-civil-administration",
    "perspective:west-bank:palestinian-civil-authorities"
  ],
  "sources": ["source:west-bank:ecomena", "source:west-bank:palestinian-hydrology-group"],
  "corroboration": "confirmed_by_2_perspectives",
  "who_reference_standard": 100.0
}
```

Once population identity is a field instead of a slot label, both
perspectives reporting the *same* 242 and the *same* 73 becomes visible
as agreement (`corroboration: confirmed_by_2_perspectives`) instead of
two unrelated, differently-ordered pairs of numbers — which is a
materially different, and more accurate, finding than what 1.x currently
displays.

Required fields: `value`, `unit`, `population` (with an explicit `group`
description — never left implicit), `sources`. `period` and `denominator`
default to `"data not available"` rather than being omitted, per the
existing 1.x rule that a verifiable-but-absent figure is stated, not
dropped.

### 1.5 Source

The actual document. 1.x's `sources` field is a flat array of org-name
strings (`"sources": ["EcoMENA", "Palestinian Hydrology Group", ...]`) —
that's a reference to who published something, not to the something
itself, and it's the same list for every claim/measurement in the whole
territory regardless of which one it actually backs. A Source record is
addressable and specific:

```json
{
  "id": "source:west-bank:icj-2004-advisory-opinion",
  "title": "Legal Consequences of the Construction of a Wall in the Occupied Palestinian Territory (Advisory Opinion)",
  "publisher": "International Court of Justice",
  "source_type": "judicial_finding",
  "date_published": "2004-07-09",
  "date_accessed": "data not available",
  "url": "data not available",
  "language": "en",
  "reliability_notes": ""
}
```

`source_type` enum: `judicial_finding`, `legal_instrument`,
`government_statement`, `ngo_report`, `press`, `academic`,
`dataset`, `interview`, `archival_document`, `unattributed_secondary`.
Every 1.x `"citation": "..."` string becomes a `sources: [...]` array of
IDs pointing here once migrated — see §migration below for how much of
that the script can do automatically versus what needs a human to
actually resolve a citation string into a real Source record.

### 1.6 Finding

A conclusion reached by an authoritative body, as distinct from a Claim
(which is any actor's own assertion). The ICJ 2004 Advisory Opinion is
the clean example already in the data: it's not "Israel's claim" or "the
Palestinian characterization" — it's a judicial determination.

```json
{
  "id": "finding:west-bank:icj-2004-wall-contrary-to-international-law",
  "territory": "west-bank",
  "issuing_body": "actor:icj",
  "subject": "physical_barrier:west-bank:separation-barrier",
  "finding_type": "judicial",
  "text": "The construction of the wall, and its associated regime, are contrary to international law.",
  "date": "2004-07-09",
  "sources": ["source:west-bank:icj-2004-advisory-opinion"],
  "binding_status": "advisory_opinion_non_binding",
  "accepted_by": [],
  "rejected_by": ["actor:israel-state"]
}
```

`accepted_by`/`rejected_by` record which Actors have taken a public
position on the finding itself — 1.x's data already states "Israel
rejected the ICJ opinion and continued construction," so this is not new
research, just a new place to put research that already exists.

### 1.7 Dispute

An explicit relationship between two Claims (or a Claim and a Finding)
showing disagreement. Design Blueprint §12's relationship vocabulary
applies here.

```json
{
  "id": "dispute:west-bank:separation-barrier-legality",
  "territory": "west-bank",
  "subject": "physical_barrier:west-bank:separation-barrier",
  "relationship": "contradicts",
  "parties": [
    {"claim": "claim:west-bank:separation-barrier:justification:israel-civil-administration", "position": "documented"},
    {"claim": "finding:west-bank:icj-2004-wall-contrary-to-international-law", "position": "documented"}
  ],
  "status": "unresolved",
  "notes": "Israel's Supreme Court (2004) accepted the government's security rationale for the barrier in essence while ordering a 30km reroute; the ICJ, the same year, found the barrier and its regime contrary to international law. Israel does not accept the ICJ's jurisdiction on this question. Both findings are documented; GASPI records both without adjudicating which one is authoritative for the reader."
}
```

The `status` field never resolves to "X was right" — it tracks whether
the dispute itself is `unresolved`, `resolved_by_subsequent_finding`, or
`superseded`.

### 1.8 Unknown

Not a new record type — a required, explicit value. Every field above
that would otherwise be omitted when data doesn't exist must instead
carry one of: `not_available` (no verifiable figure exists),
`not_researched` (nobody has looked yet), `inaccessible` (a source is
known to exist but can't be reached), `disputed_and_unresolved` (sources
actively conflict with no way to adjudicate), `source_claims_unavailable`
(an actor was asked and stated they don't have or won't provide the
information). This is 1.x's `"data not available"` convention, made more
specific — the difference between "nobody's checked" and "actively
suppressed" is itself a finding worth keeping, and 1.x currently
collapses both into the same string.

## 2. ID scheme

`<type>:<territory-key>:<slug>[:<qualifier>]`

- Territory-scoped by default (`claim:west-bank:...`) since GASPI's unit
  of research has always been one territory at a time.
- `actor:` and `source:` IDs are **not** territory-prefixed when the
  actor/source is not territory-specific (e.g. `actor:icj`,
  `actor:un-ocha`) — an actor doesn't get a new identity in every
  territory it appears in. Territory-specific actors (e.g.
  `actor:israeli-settlers-west-bank`) are prefixed because "the same"
  population group in a different territory is not the same Actor
  record.
- Slugs are derived from the existing `name` fields already in
  `data/raw/` wherever possible, so migrated IDs stay legible against the
  1.x source they came from.

## 3. Relationships (how the entities connect)

```
Actor ──represented_by──> Perspective ──asserts──> Claim ──about──> (barrier | zone | incident | checkpoint | ...)
                                                       │
                                                       ├──supported_by──> Measurement
                                                       ├──cited_in──────> Source
                                                       └──disputed_by───> Dispute ──references──> Claim | Finding

Finding ──issued_by──> Actor (judicial_body | intergovernmental_body)
Finding ──about──────> (same subject types as Claim)
```

A `subject` (barrier, zone, checkpoint, incident, legal record, water
infrastructure node) keeps its own identity and its own geometry/location
fields exactly as in 1.x — this spec does not change how *things* are
recorded, only how *statements about things* are recorded and connected.

## 4. What this fixes, concretely, in existing data

- The `population_a`/`population_b` ambiguity (§1.4) — the most concrete,
  already-discovered bug this model closes.
- `sources: [...]` as a flat, territory-wide string list becomes
  per-claim, per-measurement, per-finding attribution — a reader can
  finally tell *which* source backs *which* specific sentence, which is
  the entire premise of the source-chain drawer in the uploaded
  prototype (currently that drawer can only say "this source is
  represented somewhere in this territory's record," not what it backs).
- `stated_justification` / `opposing_characterization` as two fixed
  string slots become an open-ended list of Claims — a third or later
  perspective (this project already runs some territories with only one
  perspective file, e.g. Crimea, New Caledonia, Rojava/AANES — see
  README "Status") is not structurally second-class the way a third
  opinion would be forced into an `opposing_characterization` field built
  for exactly two.

## 5. What this spec deliberately does not do yet

- It does not require every existing 1.x record to be migrated before
  2.0 can ship anything. Migration is per-territory (§ migration script,
  separate document/tooling) — West Bank is the pilot.
- It does not resolve `"citation": "Wikipedia; Israeli Supreme Court
  rulings; International Court of Justice Advisory Opinion (2004)"`
  style multi-source citation strings into individual Source records
  automatically with full confidence — a migration script can split on
  `;` and propose candidates, but "Wikipedia" citing something is not the
  same evidentiary weight as the ICJ ruling itself, and collapsing that
  distinction automatically would be worse than leaving it as an
  unresolved string flagged for a human pass.
- It does not yet specify the translation-triple record (original /
  literal / contextual) in full — that's Design Blueprint §9–10, and
  depends on a research-protocol change to how `data/raw/` documents get
  produced in the first place, not on this data model.
