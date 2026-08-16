#!/usr/bin/env python3
"""
Migrates one territory's data/raw/ perspective documents into a GASPI 2.0
record set conforming to data/schema/gaspi_2_0.schema.json, per
research/GASPI_2.0_DATA_MODEL_SPEC.md.

First pass, piloted on West Bank only -- not a general-purpose migrator run
across all 16 territories yet. Deliberately conservative wherever a choice
would require inventing an attribution the source data doesn't actually
support: see ATTRIBUTION RULES below before extending this to another
territory or trusting its output as final.

ATTRIBUTION RULES (read before changing anything here)
--------------------------------------------------------
- A Claim's `perspective` field records which GASPI research pass reported
  the claim, never who the claim's text describes as speaking. Both
  `stated_justification` and `opposing_characterization` on a 1.x record
  are written by whichever perspective document that record came from --
  attributing `opposing_characterization` to "the other side's" perspective
  record would assert that perspective's own research produced text it
  never actually produced. This matches build_territories.py's existing
  behavior (opposing_characterization -> a generic "Documented opposing
  account" label, never a named party) -- see GASPI_2.0_DATA_MODEL_SPEC.md
  section 1.3 for the worked-out reasoning.
- Cross-perspective subject matching (e.g. recognizing that P1's
  "Separation Barrier" and P2's "جدار الضم والتوسع" are the same physical
  barrier) is done here only where a strong mechanical signal exists
  (exact length_km match). Anything that can't be matched this way stays
  perspective-scoped rather than being guessed into a shared subject.
- Dispute records are NOT auto-generated from claim text in this pass --
  detecting genuine disagreement (as opposed to two claims that simply
  don't mention each other) is a judgment call, not a mechanical one. One
  Dispute is hand-curated below as a demonstration; extending this to
  every subject is future work, not something this script claims to do.
- Source records for `"citation": "A; B; C"` strings are produced as
  review-flagged stubs (source_type "unattributed_secondary", reliability
  notes marked NEEDS REVIEW) -- resolving a citation string into a real,
  dated, linked source is a research task, not something this script can
  respectably automate.

Run: python3 data/migrate_to_2_0.py west-bank
Output: data/v2/<territory-key>.json (gitignored until reviewed -- see
bottom of this file) plus a REVIEW_REPORT printed to stdout listing every
item that still needs a human pass.
"""
import json
import re
import sys
import zlib
from pathlib import Path

def stable_id(name):
    """Deterministic short id from a name, for cases with no usable Latin
    slug. Python's built-in hash() is randomized per-process (PYTHONHASHSEED)
    -- using it here would make every re-run of this script produce
    different ids for the same input, which is exactly the kind of silent
    non-reproducibility this project's own build scripts (build_territories.py,
    splice_frontend.py) are otherwise careful to avoid."""
    return zlib.crc32(name.encode("utf-8")) % 10000

RAW = Path(__file__).parent / "raw"
SCHEMA = Path(__file__).parent / "schema" / "gaspi_2_0.schema.json"
OUT_DIR = Path(__file__).parent / "v2"

LANGUAGE_CODES = {
    "hebrew": "he", "arabic": "ar", "english": "en", "spanish": "es",
    "french": "fr", "russian": "ru", "romanian": "ro", "turkish": "tr",
    "greek": "el", "mandarin chinese (简体中文)": "zh-CN", "mandarin chinese": "zh-CN",
    "tibetan (བོད་ཡིག)": "bo", "tibetan": "bo",
}

# Hand-mapped for the two known West Bank perspectives -- see module
# docstring on why this isn't a generic NLP classifier. Extend explicitly
# per-territory rather than guessing when this migration is run elsewhere.
KNOWN_ACTORS = {
    "State of Israel / Civil Administration": ("actor:israel-state", "Israel", "state"),
    "دولة إسرائيل / الإدارة المدنية": ("actor:israel-state", "Israel", "state"),
    "Palestinian Authority": ("actor:palestinian-authority", "Palestinian Authority", "sub_state_authority"),
    "السلطة الفلسطينية": ("actor:palestinian-authority", "Palestinian Authority", "sub_state_authority"),
}

def _sanitize(s):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return re.sub(r"-{2,}", "-", s)

def slug(s, fallback):
    """ASCII-only slug. Falls back to a stable index-based id when a name
    has no usable Latin content (e.g. an Arabic-only barrier name) --
    NEVER silently drops the original name; callers must keep it in the
    record's own text/notes so a human can still identify the subject.
    The fallback is sanitized too, defensively -- a caller-supplied
    fallback (e.g. built from a float length_km) could otherwise smuggle
    an invalid character straight into an id."""
    ascii_only = _sanitize(s)
    return ascii_only if len(ascii_only) >= 3 else _sanitize(fallback)

def is_missing(v):
    return v is None or (isinstance(v, str) and "not available" in v.lower())

def classify_actor(name):
    if name in KNOWN_ACTORS:
        return KNOWN_ACTORS[name]
    aid = "actor:" + slug(name, f"unclassified-{stable_id(name)}")
    lowered = name.lower()
    if any(k in lowered for k in ("court", "tribunal", "محكمة")):
        atype = "judicial_body"
    elif any(k in lowered for k in ("un ", "united nations", "الأمم المتحدة", "icj", "un.")):
        atype = "intergovernmental_body"
    elif any(k in lowered for k in ("state of", "government", "دولة")):
        atype = "state"
    elif any(k in lowered for k in ("authority", "administration", "سلطة", "إدارة")):
        atype = "sub_state_authority"
    else:
        atype = "unattributed"  # genuinely unclassified -- see review report
    return aid, name, atype

def split_citation(citation):
    """'A; B[citation:3]; C' -> ['A', 'B', 'C'] -- strips the inline
    [citation:N] markers used throughout data/raw/, which are positional
    footnote refs into that single document, not standalone source ids."""
    if is_missing(citation):
        return []
    cleaned = re.sub(r"\[citation:\d+\]", "", citation)
    return [p.strip() for p in cleaned.split(";") if p.strip()]

class Migrator:
    def __init__(self, territory_key):
        self.territory_key = territory_key
        self.actors = {}
        self.perspectives = []
        self.claims = []
        self.measurements = []
        self.sources = {}
        self.findings = []
        self.disputes = []
        self.review_notes = []
        self._id_counts = {}

    def note(self, msg):
        self.review_notes.append(msg)

    def unique_id(self, prefix, base):
        candidate = f"{prefix}:{base}"
        n = self._id_counts.get(candidate, 0)
        self._id_counts[candidate] = n + 1
        return candidate if n == 0 else f"{candidate}-{n+1}"

    def add_actor(self, name):
        if is_missing(name):
            return None
        aid, label, atype = classify_actor(name)
        if aid not in self.actors:
            if atype == "unattributed":
                self.note(f"Actor '{name}' -> actor_type guessed as 'unattributed'; needs human classification.")
            self.actors[aid] = {"id": aid, "name": label, "actor_type": atype, "jurisdiction": "data not available", "notes": ""}
        return aid

    def add_source_stub(self, name):
        if is_missing(name):
            return None
        sid = "source:" + self.territory_key + ":" + slug(name, f"src-{stable_id(name)}")
        if sid not in self.sources:
            self.sources[sid] = {
                "id": sid, "title": name, "publisher": name,
                "source_type": "unattributed_secondary",
                "date_published": "not_researched", "date_accessed": "not_researched",
                "url": "not_researched", "language": "data not available",
                "reliability_notes": "NEEDS REVIEW: citation string, not yet resolved to a dated, linked, classified source.",
            }
            self.note(f"Source stub '{name}' ({sid}) needs review: resolve to a real dated/linked source.")
        return sid

    def add_sources_from_citation(self, citation):
        return [sid for sid in (self.add_source_stub(n) for n in split_citation(citation)) if sid]

    def perspective_id(self, doc):
        fallback = "perspective-" + re.sub(r"[^a-z0-9]+", "-", doc.get("language", "unk").lower()).strip("-")
        return "perspective:" + self.territory_key + ":" + slug(doc["perspective"], fallback)

    def migrate_perspective(self, doc):
        pid = self.perspective_id(doc)
        if any(sep in doc["perspective"] for sep in (" / ", "/")):
            self.note(f"Perspective label '{doc['perspective']}' looks like multiple institutions bundled into one Actor "
                      f"(represented_actor points at a single compound name) -- consider splitting into separate Actor "
                      f"records with their own represented_actor links if the underlying research treats them distinctly.")
        actor_id = self.add_actor(doc["perspective"])
        lang = LANGUAGE_CODES.get(doc.get("language", "").strip().lower(), doc.get("language", "data not available"))
        self.perspectives.append({
            "id": pid, "territory": self.territory_key, "represented_actor": actor_id or "actor:unattributed",
            "label": doc["perspective"], "research_language": lang,
            "source_language_reason": "Primary documentary language of the represented institution",
            "years_of_scope": doc.get("years_of_scope", "data not available"),
            "original_text_preserved": False, "literal_translation": False, "contextual_translation": True,
        })
        return pid

    def migrate_barriers(self, doc, pid):
        topo = doc.get("topographic_and_control_data", {})
        for b in topo.get("physical_barriers", []) or []:
            length = b.get("length_km")
            match_key = length if isinstance(length, (int, float)) else None
            base_name = b["name"] if re.search(r"[a-zA-Z]{3,}", b["name"]) else f"barrier-{match_key or 'unnamed'}"
            slug_name = slug(base_name, f"barrier-{match_key or 'unnamed'}")
            subject = f"physical_barrier:{self.territory_key}:{slug_name}"
            if not re.search(r"[a-zA-Z]{3,}", b["name"]):
                self.note(f"Barrier subject '{subject}' derived from non-Latin name '{b['name']}' via length_km match ({match_key} km) -- verify this is the same barrier as any Latin-named counterpart.")
            if b.get("stated_justification") and not is_missing(b["stated_justification"]):
                self.claims.append({
                    "id": self.unique_id("claim", f"{self.territory_key}:{slug_name}:justification"),
                    "territory": self.territory_key, "perspective": pid, "subject": subject,
                    "claim_type": "justification", "text": b["stated_justification"],
                    "sources": self.add_sources_from_citation(b.get("citation")) or [self.add_source_stub("Unattributed") or "source:unattributed"],
                    "status": "documented",
                })
            if b.get("opposing_characterization") and not is_missing(b["opposing_characterization"]):
                self.claims.append({
                    "id": self.unique_id("claim", f"{self.territory_key}:{slug_name}:characterization"),
                    "territory": self.territory_key, "perspective": pid, "subject": subject,
                    "claim_type": "characterization", "text": b["opposing_characterization"],
                    "sources": self.add_sources_from_citation(b.get("citation")) or [self.add_source_stub("Unattributed") or "source:unattributed"],
                    "status": "documented",
                })

    def migrate_incidents(self, doc, pid):
        for inc in doc.get("environmental_degradation_incidents", []) or []:
            slug_name = slug(inc.get("incident_type", ""), f"incident-{len(self.claims)}")
            subject = f"incident:{self.territory_key}:{slug_name}"
            for field, ctype in (("stated_justification", "justification"), ("opposing_characterization", "characterization")):
                text = inc.get(field)
                if text and not is_missing(text):
                    self.claims.append({
                        "id": self.unique_id("claim", f"{self.territory_key}:{slug_name}:{ctype}"),
                        "territory": self.territory_key, "perspective": pid, "subject": subject,
                        "claim_type": ctype, "text": text,
                        "sources": self.add_sources_from_citation("; ".join(inc.get("citations", []))) or [self.add_source_stub("Unattributed") or "source:unattributed"],
                        "status": "documented",
                    })

    def migrate_statutory_conflicts(self, doc, pid):
        jf = doc.get("jurisprudence_and_statutory_friction", {}) or {}
        for conf in jf.get("documented_statutory_conflicts", []) or []:
            slug_name = slug(conf.get("legal_domain", ""), f"statutory-conflict-{len(self.claims)}")
            subject = f"legal:{self.territory_key}:{slug_name}"
            if conf.get("conflict_description") and not is_missing(conf["conflict_description"]):
                self.claims.append({
                    "id": self.unique_id("claim", f"{self.territory_key}:{slug_name}"),
                    "territory": self.territory_key, "perspective": pid, "subject": subject,
                    "claim_type": "factual_assertion", "text": conf["conflict_description"],
                    "sources": self.add_sources_from_citation(conf.get("citation")) or [self.add_source_stub("Unattributed") or "source:unattributed"],
                    "status": "documented",
                })

    def migrate_findings(self, doc):
        jf = doc.get("jurisprudence_and_statutory_friction", {}) or {}
        for case in jf.get("landmark_jurisprudence_and_treaties", []) or []:
            issuing_name = case.get("judicial_body_or_treaty", "data not available")
            actor_id = self.add_actor(issuing_name) or "actor:unattributed"
            slug_name = slug(case.get("case_or_resolution_name", ""), f"finding-{len(self.findings)}")
            text = case.get("holding_or_standard") or case.get("official_legal_rationale") or "data not available"
            self.findings.append({
                "id": self.unique_id("finding", f"{self.territory_key}:{slug_name}"),
                "territory": self.territory_key, "issuing_body": actor_id,
                "subject": f"legal:{self.territory_key}:{slug_name}",
                "finding_type": "judicial", "text": text,
                "date": str(case["year"]) if case.get("year") and not is_missing(case.get("year")) else "not_available",
                "sources": self.add_sources_from_citation(case.get("citation")) or [self.add_source_stub(issuing_name) or "source:unattributed"],
                "binding_status": "data not available",
                "accepted_by": [], "rejected_by": [],
            })

    def migrate_water_measurements(self, docs):
        """Hand-mapped, territory-specific: see GASPI_2.0_DATA_MODEL_SPEC.md
        section 1.4 for why population_a/population_b can't be resolved
        generically (the label flips which population it means between
        perspective files) and why this one metric gets special-cased
        instead of generic automated handling."""
        reports = []
        for doc, pid in docs:
            wc = doc.get("hydrology_data", {}).get("per_capita_water_consumption_l_d", {}) or {}
            pa, pb = wc.get("population_a"), wc.get("population_b")
            if is_missing(pa) or is_missing(pb):
                continue
            reports.append((pid, doc, float(pa), float(pb)))
        if not reports:
            return
        # Both known West Bank perspective files independently report the
        # same two figures (242 and 73 L/person/day) with population_a and
        # population_b swapped between files -- see spec section 1.4. This
        # mapping is West Bank-specific domain knowledge, not inferred.
        settler_value, palestinian_value = 242.0, 73.0
        who = None
        srcs = set()
        reported_by = []
        for pid, doc, pa, pb in reports:
            reported_by.append(pid)
            wc = doc["hydrology_data"]["per_capita_water_consumption_l_d"]
            who = wc.get("who_reference_standard", who)
            for sid in self.add_sources_from_citation(wc.get("citation")):
                srcs.add(sid)
            found = {pa, pb}
            if found != {settler_value, palestinian_value}:
                self.note(f"Water-consumption values from {pid} ({pa}, {pb}) don't match the expected (242, 73) pair -- hand-mapping in migrate_water_measurements() needs updating before trusting this measurement.")
        srcs = sorted(srcs) or [self.add_source_stub("Unattributed") or "source:unattributed"]
        corroboration = f"confirmed_by_{len(reports)}_perspectives" if len(reports) > 1 else "single_source"
        self.measurements.append({
            "id": f"measurement:{self.territory_key}:per-capita-water-consumption:settlers",
            "territory": self.territory_key, "metric": "per_capita_water_consumption",
            "unit": "liters_per_person_per_day", "value": settler_value,
            "population": {"group": "Israeli settlers in West Bank", "actor": self.add_actor("Israeli settlers in West Bank")},
            "period": "not_available", "reported_by": reported_by, "sources": srcs,
            "corroboration": corroboration, "who_reference_standard": who or 100.0,
        })
        self.measurements.append({
            "id": f"measurement:{self.territory_key}:per-capita-water-consumption:palestinians",
            "territory": self.territory_key, "metric": "per_capita_water_consumption",
            "unit": "liters_per_person_per_day", "value": palestinian_value,
            "population": {"group": "Palestinians in the West Bank", "actor": self.add_actor("Palestinians in the West Bank")},
            "period": "not_available", "reported_by": reported_by, "sources": srcs,
            "corroboration": corroboration, "who_reference_standard": who or 100.0,
        })

    def add_hand_curated_dispute(self):
        """One demonstration Dispute record. NOT auto-generated -- see
        module docstring. Only added if the two claims it references
        actually exist in this run's output, so this stays honest if the
        upstream data ever changes shape."""
        just_id = None
        char_id = None
        for c in self.claims:
            if c["subject"].startswith("physical_barrier:") and "separation-barrier" in c["subject"]:
                if c["claim_type"] == "justification" and just_id is None:
                    just_id = c["id"]
                if c["claim_type"] == "characterization" and char_id is None:
                    char_id = c["id"]
        icj_finding = next((f["id"] for f in self.findings if "wall" in f["subject"] or "جدار" in f.get("_orig_name", "")), None)
        if not icj_finding:
            icj_finding = next((f["id"] for f in self.findings if f["finding_type"] == "judicial"), None)
        if just_id and icj_finding:
            self.disputes.append({
                "id": f"dispute:{self.territory_key}:separation-barrier-legality",
                "territory": self.territory_key, "subject": "physical_barrier:" + self.territory_key + ":separation-barrier-geder-hahafrada-security-fence",
                "relationship": "contradicts",
                "parties": [
                    {"claim": just_id, "position": "documented"},
                    {"claim": icj_finding, "position": "documented"},
                ],
                "status": "unresolved",
                "notes": "Israel's own justification for the barrier and the ICJ's 2004 finding that the barrier and its regime are contrary to international law are both documented in the source research. GASPI records both without adjudicating which is authoritative for the reader.",
            })
        else:
            self.note("Hand-curated separation-barrier Dispute record was NOT added -- expected justification claim or ICJ finding not found in this run's output (check subject slugs above).")

    def build(self, migrated_from):
        return {
            "schema_version": "2.0.0",
            "territory_key": self.territory_key,
            "migrated_from": migrated_from,
            "actors": sorted(self.actors.values(), key=lambda a: a["id"]),
            "perspectives": self.perspectives,
            "claims": self.claims,
            "measurements": self.measurements,
            "sources": sorted(self.sources.values(), key=lambda s: s["id"]),
            "findings": self.findings,
            "disputes": self.disputes,
        }

# P-number -> raw filenames, mirroring build_territories.py's own mapping
# for the two territories this pilot covers.
TERRITORY_FILES = {
    "west-bank": ["P1_West_Bank_12of12.json", "P2_الضفة_الغربية_12of12.json"],
}

def migrate(territory_key):
    filenames = TERRITORY_FILES.get(territory_key)
    if not filenames:
        raise SystemExit(f"No raw-file mapping for '{territory_key}' -- this pilot only covers: {list(TERRITORY_FILES)}")
    docs = [json.loads((RAW / f).read_text(encoding="utf-8")) for f in filenames]

    m = Migrator(territory_key)
    doc_pids = []
    for doc in docs:
        pid = m.migrate_perspective(doc)
        doc_pids.append((doc, pid))
        m.migrate_barriers(doc, pid)
        m.migrate_incidents(doc, pid)
        m.migrate_statutory_conflicts(doc, pid)
        m.migrate_findings(doc)
    m.migrate_water_measurements(doc_pids)
    m.add_hand_curated_dispute()

    result = m.build(filenames)

    OUT_DIR.mkdir(exist_ok=True)
    out_path = OUT_DIR / f"{territory_key}.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Wrote {out_path}")
    print(f"  actors={len(result['actors'])} perspectives={len(result['perspectives'])} "
          f"claims={len(result['claims'])} measurements={len(result['measurements'])} "
          f"sources={len(result['sources'])} findings={len(result['findings'])} disputes={len(result['disputes'])}")

    if m.review_notes:
        print(f"\nREVIEW REPORT — {len(m.review_notes)} item(s) need a human pass before this is trusted as final:")
        for note in m.review_notes:
            print(f"  - {note}")
    else:
        print("\nREVIEW REPORT — nothing flagged (unexpected for a first pass; double-check the review-note logic itself).")

    try:
        import jsonschema
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema).validate(result)
        print(f"\nValidated OK against {SCHEMA}")
    except ImportError:
        print("\n(jsonschema not installed -- skipped schema validation. `pip install jsonschema` to check.)")

if __name__ == "__main__":
    territory = sys.argv[1] if len(sys.argv) > 1 else "west-bank"
    migrate(territory)
