# GASPI — New Requirements & Open Threads

Working reference for everything decided, found, or proposed in the research-methodology-overhaul conversation. Split into **done**, **decided but not built**, **found but not fixed**, and **discussed but not committed to**, so nothing gets mistaken for finished work.

---

## 1. Research methodology overhaul

**Status: 4 of 4 source documents delivered. Not yet integrated into the live data model.**

The prior research process mixed both sides' content into single documents, which produced the mislabeling bug described in §2. The new process uses four strictly isolated, single-perspective "Zero Contamination" prompts — one per side per territory — each explicitly forbidding inclusion of the other side's narrative or justification.

| Prompt | Language | Scope | Report file | Status |
|---|---|---|---|---|
| `01westbank.txt` | Hebrew | West Bank, Israeli official/institutional perspective | `research/westbank-israel.md` | ✅ delivered by user, saved |
| `02westbank.txt` | Arabic | West Bank, Palestinian institutional perspective | `research/westbank-palestine.md` | ✅ delivered by user, saved |
| `03gaza.txt` | Hebrew | Gaza, Israeli official/institutional perspective | `research/gaza-israel.md` | ✅ delivered by user, saved |
| `04gaza.txt` | Arabic | Gaza, Palestinian institutional perspective | `research/gaza-palestine.md` | ✅ delivered by user, saved |

All four were read and verified in full — titles, language, and body content all correctly match their intended filename/prompt pairing (checked directly, not assumed; no swaps).

**Not yet done:** mapping these four documents into GASPI 2.0's actual schema (Actor/Perspective/Claim/Measurement/Source/Finding/Dispute) and merging into `data/territories.json` / `data/v2/*.json`. User explicitly deferred this ("no not yet" / "not yet") pending the fix in §2 and §3 below — don't integrate until the purity-check mechanism exists, or the new data risks the same mislabeling bug on day one.

---

## 2. The perspective-mislabeling bug (found, root-caused, NOT fixed)

**Status: confirmed at the source. Scope across the full corpus is unverified.**

### What it is
Every raw research document (`data/raw/P*.json`) carries a document-level `"perspective"` field (e.g. `"State of Israel / Civil Administration"`). That field means *"which side's institutional/documentary lens this research was conducted through"* — a methodology descriptor. But individual entries inside the document (rulings, laws, incidents) inherit that same tag regardless of whether the entry is that side's own claim or something adverse to them that turned up during research under that lens.

### Where it's confirmed present
- `data/raw/P1_West_Bank_12of12.json` — the raw source, doc-level `perspective: "State of Israel / Civil Administration"`.
- `data/territories.json` (compiled) — same mislabeling present in the West Bank `legal` array. Example: the 2004 ICJ Advisory Opinion (a ruling *against* Israel) is tagged `"perspective": "State of Israel / Civil Administration"` as if it were Israel's own assertion.
- `thegreatgaspi/index.html` (deployed frontend) — inherits it from the compiled file, was live on the public site until this was found.

### What's NOT yet checked
- The other sections of `P1` (topographic, hydrology, environmental incidents, security/justification) — only `jurisprudence_and_statutory_friction` has been inspected.
- The other 30 raw documents (every other GASPI territory). User now has the full `data/raw/` corpus (delivered as a zip) to check independently.

**Action needed:** systematic audit of all 32 raw documents' internal entries against their own doc-level perspective tag, using the structural check in §3 rather than manual review.

---

## 3. Proposed fixes — what's accepted, what's rejected, what's pending

A third-party proposal ("Sovereign Dual-Track Intelligence Portal," from Gemini) was reviewed in two passes. Net decision: **keep the existing engine and schema, retrofit three specific ideas into it.** Do not replace the architecture.

### Rejected outright
- **Wholesale schema/layout replacement** (the "Sovereign Dual-Track" TypeScript schema + CSS grid layout). Would be a technical regression: forces a rigid 1:1 party-A/party-B pairing that doesn't match real evidence (sometimes only one side has documented something, sometimes a finding comes from neither side), and its `domainCategory` enum has no room for content GASPI already ships — legal framework, checkpoints, physical barriers, environmental degradation, the Gaza 3D damage layer.
- **Fabricated SHA-256 provenance hashes.** The proposal's example hashes (`sha256:7f8a92e104c98a3b2e`) are ~18 hex characters — not valid SHA-256 (64 chars) — displayed next to a `[VERIFIED]` badge. This is *worse* than the "UNVERIFIED" labeling bug already fixed on the live site: that was honest about uncertainty, this would be actively fabricating certainty.
- **Regex/keyword "rebuttal isolation" linter** (flagging text containing "however," "ICJ," "opponents argue," etc.). Tested directly against the three real mislabeled West Bank entries — **it would not have flagged any of them.** None of the actual bug's text contains any of the listed markers; it's flat, factual-sounding critical prose with no linguistic tell. Also produces false positives: Israel's own Supreme Court ruling legitimately contains the word "however" while being correctly attributed. Sentiment/keyword matching is the wrong tool for this class of bug.

### Accepted, not yet built
- **Structural purity check** (replaces the regex linter): compare `claim.perspective` against `claim.source.issuing_body` / publisher. If a claim is filed under one actor's perspective but its own cited source is issued by a different, unrelated body (e.g. the ICJ), flag it. Deterministic, metadata-based, no prose analysis — and it's the shape of check that actually would have caught the real bug. **Not implemented. Needs to be built against the real `data/schema/gaspi_2_0.schema.json` fields, not a reinvented schema.**
- **Honest provenance states**, replacing fake hashes: `verificationStatus: 'verified_checksum' | 'archived_url' | 'unverified'`. Only claim `verified_checksum` when a real 64-char hash exists (requires an actual archival pipeline — fetch, hash, store — not built yet). `archived_url` (an `archiveUrl` + `dateRetrievedISO` pair) is realistic to populate now for new sources. **Not implemented.**
- **Literal vs. contextual translation split** for claims sourced from non-English originals — keep both the literal and the interpreted/contextual translation, not just one collapsed English version. **Not implemented**, and note: the 22 already-migrated West Bank claims in `data/v2/west-bank.json` have no native-language text captured at all, so this only applies going forward unless someone goes back to the raw Hebrew/Arabic docs to backfill it — that's real research work, not a schema change.

### Must be preserved if any new schema work happens
- All 5 real `claim_type` values already in production and already rendered by the frontend (`justification`, `characterization`, `factual_assertion`, `allegation`, `denial`) — the Gemini proposal's schema draft only listed 3. Don't ship a schema that silently drops types already in use.

---

## 4. Standing rule: no internal QA/confidence signaling on the public site

**Status: done, but stated here as a durable rule for all future work, not a one-time fix.**

Already removed from the live site: `NEEDS REVIEW` / `UNVERIFIED` tags, the `GASPI 2.0 pilot` badge, `migrated claims` / `(GASPI 2.0)` / "not yet migrated" language, and a `partial OSM building coverage` caveat that had briefly been added to the Gaza damage picker. All of that is legitimate to track in commit messages and code comments — it is not legitimate to surface to visitors. Any future data-quality caveat (including from the audit in §2, or from the provenance work in §3) needs to follow this same rule: internal state stays internal.

---

## 5. Editorial direction — discussed, not committed to build

**Status: exploratory. Nothing in this section is a build order.**

- Direction floated: present GASPI content the way top-tier narrative journalism/documentary work does — lead with a specific human-scale story, let systemic data sit underneath as the "show your work" layer for someone already hooked, rather than leading with data tables. Named tradeoff: this trades rigor (auditable, source-backed) for resonance (curatorial — whose story gets picked is itself an editorial judgment call with no source-hash to defend it).
- `nodes/n01.md` ("The Ledger and the Mob: Galilee Under the Pashas, 1831-1840" — Safed 1834) and `nodes/n05.md` ("After the Pashas: Tanzimat, the Land Code, and the New Lords of Palestine" — 1858 Land Code / Sursock–Jezreel Valley chain) were reviewed against this standard and both hold up well — real named individuals on multiple sides, honest sourcing gaps stated explicitly rather than invented over, no side flattened into pure villain or pure victim. n01 works through individual/atrocity-level empathy; n05 works through institutional-mechanism understanding (a well-intentioned land reform, filtered through conscription-era trauma, producing mass dispossession as an unintended structural consequence). These are not GASPI-schema content — they're Atlas narrative nodes — but they're the existing proof that the target tone is achievable.
- User's thesis, checked and partially validated: the generational "sense of betrayal" cycle traces back to Safed 1834, with roughly a "decade or 3" cadence between reprisals. Real, checkable support found: Hebron was hit in both 1834 and 1929, and 1929's violence is documented as carrying active folk memory of 1834 ("Yagma el Gabireh"); Safed was likewise hit in both 1834 and 1929. Refined framing offered and not yet contested: this is better described as a **compounding-trauma model** (each episode has its own real proximate cause, but lands on a population primed by the last one) than a strict **reciprocal tit-for-tat** model (implying direct revenge-for-revenge causation, which the record doesn't cleanly support).
- "Ephemeris" tangent: floated as a possible thematic/visual framing device — juxtaposing the ~29-year reprisal cadence against real astronomical ephemeris data (consistent with the site's existing astronomical tooling: natal-chart app, the Antikythera-style dial concept, necronomy-atlas) as a *coincidence worth showing*, explicitly not as literal causation. The ~29-year number has a mundane, well-evidenced explanation already available (one human generation — the time for a traumatized child to grow into someone with the social power to act on accumulated grievance), which was named directly rather than left ambiguous.

**Not started, no commitment made either way:**
- A dedicated piece tracing the full reprisal chain from 1834 forward with n01/n05-level sourcing rigor.
- An "ephemeris-and-reprisal-cycle" piece pairing the generational cadence against real ephemeris data.

---

## 6. Delivery/process requirements surfaced this session

Not code requirements, but working constraints worth keeping in mind for future file deliveries:

- When asked for "a copy of the source material" or "the way it is on GitHub," deliver files mirroring the actual repo folder structure (`git archive` output), not a merged/stripped single-file version — a self-contained single file was tried once for a different reason (offline portability) and was explicitly the wrong deliverable for verification purposes.
- Any local run of `thegreatgaspi/index.html` needs a local HTTP server (`python3 -m http.server`), not `file://` — relative `fetch()` calls for the Gaza damage GeoJSON silently fail otherwise. This has been the likely cause of at least one "nothing loads locally" report.
- `SendUserFile` has a 30MB cap; the full repo zips (~70MB+) exceed it, but scoped `git archive` output (code only, or code + Gaza damage data) comes in well under it and should be the default rather than the full repo.

---

## 7. Outstanding items, unranked

- Full audit of the perspective-mislabeling bug across all 32 raw documents' full content (§2).
- Build the structural purity-check validator against the real schema (§3).
- Build honest provenance tracking (`archived_url` state at minimum) for new sources (§3).
- Decide how/when to integrate the 4 new isolated research documents into the live GASPI 2.0 data model (§1) — blocked on the above two items by the user's own stated preference.
- At Turukman neighborhood (Gaza damage layer) still needs a re-fetch with the corrected bounding box previously provided — unrelated to the research-methodology work but still open.
- GASPI dossier UI structural issue (topbar/G2-command-bar overlap, mobile "desktop mode" rendering) — diagnosed, fix scope proposed, user deferred ("not yet") — still open whenever revisited.
