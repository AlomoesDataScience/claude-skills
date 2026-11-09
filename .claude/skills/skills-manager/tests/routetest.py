#!/usr/bin/env python3
"""Routing regression test: does the check-skills matcher put an expected skill in the top N?
  routetest.py [--n 5] [-v]     prints the score (hits / cases); -v lists the misses."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "check-skills", "scripts"))
import checkskills  # noqa: E402
n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 5
cases = json.load(open(os.path.join(HERE, "routing.json")))
hits, miss = 0, []
for prompt, want in cases:
    got = [r[1] for r in checkskills.rank(prompt, checkskills.ROOT, n)]
    if set(want) & set(got):
        hits += 1
    else:
        miss.append((prompt, want, got))
print(f"routing: {hits}/{len(cases)} in top {n}")
if "-v" in sys.argv:
    for p, w, g in miss:
        print(f"  MISS {p!r}\n       want {w}\n       got  {g}")
sys.exit(0 if hits == len(cases) else 1)
