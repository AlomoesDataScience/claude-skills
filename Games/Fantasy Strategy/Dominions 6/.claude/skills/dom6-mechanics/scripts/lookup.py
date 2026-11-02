"""Find a unit, spell, item or nation in the game manual's tables and print its whole entry.

  python3 -I lookup.py NAME [TABLES_TXT]

NAME is matched case-insensitively at the start of a table row ("mystic", "fireball", "fire sword",
"arcoscephale, golden era"). An entry is the matching row plus the indented lines under it (unit
stats, summoned monster stats, ritual descriptions). Each hit shows its manual page.
TABLES_TXT defaults to /tmp/dom6manual/tables.txt (made by game_manual_text.py).
"""
import re
import sys

name = sys.argv[1].lower()
path = sys.argv[2] if len(sys.argv) > 2 else "/tmp/dom6manual/tables.txt"
lines = open(path).read().split("\n")
page, hits = 0, 0
for i, l in enumerate(lines):
    m = re.match(r"=== page (\d+)", l)
    if m:
        page = int(m.group(1))
        continue
    body = re.sub(r"^(Evo|Alt|Conj|Constr|Ench|Thau|Blood|Div)\s+\d+\s+", "", l.strip())   # spell rows
    indent = len(l) - len(l.lstrip())
    if not 99 <= page < 434 or indent > 8 or not re.match(re.escape(name) + r"(?![a-z])", body.lower()):
        continue                                 # rows only: not rules, word index or indented prose
    hits += 1
    print(f"--- page {page}")
    print(l)
    for nxt in lines[i + 1:]:
        if nxt.startswith("=== page") or len(nxt) - len(nxt.lstrip()) <= indent:
            break
        print(nxt)
if not hits:
    print("no table row starts with", repr(sys.argv[1]), "- try grep -n -i on", path)
