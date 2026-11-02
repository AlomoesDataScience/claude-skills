#!/usr/bin/env python3
"""Cross-game systems catalogue from the game guides' "## Systems" sections.

  borrow.py index              build systems.md (next to this skill) from every guide
  borrow.py find REGEX         matching Systems lines across all guides
  borrow.py options CATEGORY   every game's entries for one taxonomy category
  borrow.py gaps               game guides with no ## Systems section yet
"""
import os, re, sys, glob, signal
signal.signal(signal.SIGPIPE, signal.SIG_DFL)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
while ROOT != "/" and not os.path.isfile(os.path.join(ROOT, "BACKLOG.md")):
    ROOT = os.path.dirname(ROOT)
CATS = ["Time", "Map", "Economy", "Production", "Research", "Population", "Characters", "Politics", "Diplomacy",
        "Operational war", "Tactical combat", "Logistics", "Intelligence", "AI", "Victory", "UI", "Modding"]
OUT = os.path.join(HERE, "..", "systems.md")


def guides():
    for p in sorted(glob.glob(os.path.join(ROOT, "**", ".claude", "skills", "*", "SKILL.md"), recursive=True)):
        if "/repos/" in p or "/.claude/skills/" not in p:
            continue
        name = os.path.basename(os.path.dirname(p))
        if name.endswith("-guide") or name.endswith("-design"):
            yield name, p


def systems(p):
    s = open(p, encoding="utf-8").read()
    m = re.search(r"(?ms)^## Systems\s*\n(.*?)(?=^## |\Z)", s)
    if not m:
        return None
    out, cur = [], None
    for line in m.group(1).splitlines():
        b = re.match(r"\s*- \*\*([^*]+)\*\*:?\s*(.*)", line)
        if b:
            cur = [b.group(1).strip().rstrip(":"), b.group(2).strip()]; out.append(cur)
        elif cur and line.strip() and line.startswith("  "):
            cur[1] += " " + line.strip()
    return out


def game_of(p):
    rel = os.path.relpath(p, ROOT).split(os.sep)
    i = rel.index(".claude")
    return "/".join(rel[1:i]) if rel[0] in ("Games", "Projects") else "/".join(rel[:i]) or "(root)"


def main(a):
    if not a:
        sys.exit(__doc__)
    rows = []
    gaps = []
    for name, p in guides():
        sy = systems(p)
        if sy is None:
            gaps.append((name, game_of(p))); continue
        for cat, text in sy:
            rows.append((cat, game_of(p), name, text))
    if a[0] == "gaps":
        for n, g in gaps:
            print(f"  {n:<22} {g}")
        print(f"{len(gaps)} guides without ## Systems")
    elif a[0] == "find":
        rx = re.compile(a[1], re.I)
        for cat, g, n, t in rows:
            if rx.search(t) or rx.search(cat):
                print(f"[{cat}] {g}: {t}")
    elif a[0] == "options":
        want = a[1].lower()
        for cat, g, n, t in sorted(rows, key=lambda r: r[1]):
            if cat.lower() == want:
                print(f"- {g} ({n}): {t}")
    elif a[0] == "index":
        odd = sorted({r[0] for r in rows} - set(CATS))
        with open(OUT, "w") as f:
            f.write("# Systems catalogue\n\nBuilt by borrow.py index from the guides' ## Systems sections; do not edit by hand.\n")
            for c in CATS + odd:
                sel = sorted((r for r in rows if r[0] == c), key=lambda r: r[1])
                if sel:
                    f.write(f"\n## {c}\n\n" + "".join(f"- **{g}**: {t}\n" for _, g, _, t in sel))
        print(f"{len(rows)} entries from {len({r[2] for r in rows})} guides -> systems.md"
              + (f"; categories outside the taxonomy: {odd}" if odd else "") + f"; {len(gaps)} guides still without ## Systems")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
