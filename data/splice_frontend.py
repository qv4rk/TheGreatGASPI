#!/usr/bin/env python3
"""
Splices data/territories.json into frontend/index.html's embedded `const
DATA = {...};` block, and every data/v2/<territory-key>.json (GASPI 2.0
evidence-model output -- see research/GASPI_2.0_DATA_MODEL_SPEC.md and
data/migrate_to_2_0.py) into the sibling `const GASPI_V2 = {...};` block,
keyed by territory. The deployed page is still a single self-contained
static file with no build step -- this script is a repo-maintenance step
for this repo only, run by hand after build_territories.py and/or
migrate_to_2_0.py, the same way build_territories.py itself assembles
data/raw/ into territories.json.

Finds each object literal by brace-matching from its `const NAME = {`
marker (not by searching for a literal "};", which could false-match text
that happens to appear inside a note/citation string) and replaces only
that object, leaving the surrounding file -- including comment blocks --
untouched.
"""
import json
from pathlib import Path

TERRITORIES = Path(__file__).parent / "territories.json"
V2_DIR = Path(__file__).parent / "v2"
FRONTEND = Path(__file__).parent.parent / "frontend" / "index.html"

def find_object_span(html, marker, start_from=0):
    """Return (obj_start, obj_end) spanning the `{...}` object literal that
    follows `marker`, found by counting braces (ignoring braces inside JSON
    string literals) rather than pattern-matching the closing text."""
    obj_start = html.index(marker, start_from) + len(marker)
    while html[obj_start] != "{":
        obj_start += 1
    depth = 0
    i = obj_start
    in_string = False
    escape = False
    while i < len(html):
        c = html[i]
        if in_string:
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == '"':
                in_string = False
        else:
            if c == '"':
                in_string = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return obj_start, i + 1
        i += 1
    raise SystemExit(f"Unbalanced braces while scanning {marker!r} object")

def splice(html, marker, obj, start_from=0):
    obj_start, obj_end = find_object_span(html, marker, start_from)
    new_json = json.dumps(obj, indent=2, ensure_ascii=False)
    return html[:obj_start] + new_json + html[obj_end:], obj_start + len(new_json)

def load_v2():
    v2 = {}
    if not V2_DIR.exists():
        return v2
    for f in sorted(V2_DIR.glob("*.json")):
        v2[f.stem] = json.loads(f.read_text(encoding="utf-8"))
    return v2

def main():
    data = json.loads(TERRITORIES.read_text(encoding="utf-8"))
    v2 = load_v2()
    html = FRONTEND.read_text(encoding="utf-8")

    html, end_pos = splice(html, "const DATA = ", data)
    html, _ = splice(html, "const GASPI_V2 = ", v2, start_from=end_pos)

    FRONTEND.write_text(html, encoding="utf-8")
    print(f"Spliced {len(data)} territories into {FRONTEND}")
    print(f"Spliced GASPI 2.0 data for {len(v2)} territory(ies) ({', '.join(sorted(v2)) or 'none'}) into {FRONTEND}")

if __name__ == "__main__":
    main()
