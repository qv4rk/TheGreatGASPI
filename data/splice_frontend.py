#!/usr/bin/env python3
"""
Splices data/territories.json into frontend/index.html's embedded `const
DATA = {...};` block. The deployed page is still a single self-contained
static file with no build step -- this script is a repo-maintenance step
for this repo only, run by hand after build_territories.py, the same way
build_territories.py itself assembles data/raw/ into territories.json.

Finds the object literal by brace-matching from `const DATA = {` (not by
searching for a literal "};", which could false-match text that happens to
appear inside a note/citation string) and replaces only that object,
leaving the surrounding file -- including the comment block right after
it -- untouched.
"""
import json
from pathlib import Path

TERRITORIES = Path(__file__).parent / "territories.json"
FRONTEND = Path(__file__).parent.parent / "frontend" / "index.html"

def find_object_span(html, marker):
    """Return (obj_start, obj_end) spanning the `{...}` object literal that
    follows `marker`, found by counting braces (ignoring braces inside JSON
    string literals) rather than pattern-matching the closing text."""
    obj_start = html.index(marker) + len(marker)
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
    raise SystemExit("Unbalanced braces while scanning const DATA object")

def main():
    data = json.loads(TERRITORIES.read_text(encoding="utf-8"))
    html = FRONTEND.read_text(encoding="utf-8")

    obj_start, obj_end = find_object_span(html, "const DATA = ")
    new_json = json.dumps(data, indent=2, ensure_ascii=False)
    html = html[:obj_start] + new_json + html[obj_end:]
    FRONTEND.write_text(html, encoding="utf-8")
    print(f"Spliced {len(data)} territories ({len(new_json)} bytes) into {FRONTEND}")

if __name__ == "__main__":
    main()
