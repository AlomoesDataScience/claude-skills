"""Expected magic sites a searcher finds per province, from the Dom6 site data (inspector).

  python3 -I siteodds.py [--freq 60] [--md]       one age's table (sites and gems by path, terrain, level 1-3)

Generation (illwiki, Dom5 research by SirToma and Loggy): up to 8 rolls per province, the first at
global frequency + terrain modifier %, each next at 75% of the previous. A hit picks rarity 0/1/2 with
odds 3/4, 9/40, 1/40, then (assumed) a uniform site of that rarity allowed in the terrain. A searcher of
path P and level L finds the sites of path P with level 1..L; level-0 sites are found on conquest.
Gems are the found sites' total gem income (all paths). Uniques are treated like any site.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "dom6-inspector", "scripts"))
import inspector  # noqa: E402

TERRAIN = [("Plains", 1, 0), ("Farmland", 16, -20), ("Forest", 2, 10), ("Mountain", 4, 10), ("Cave", 512, 15),
           ("Wasteland", 8, 20), ("Swamp", 128, 20), ("Sea", 32, 0), ("Deep Sea", 256, 10)]
PATHS = ["Fire", "Air", "Water", "Earth", "Astral", "Death", "Nature", "Glamour", "Blood", "Holy"]
RARITY = {0: 0.75, 1: 9 / 40, 2: 1 / 40}
GEMS = "FAWESDNGB"


def sites():
    out = []
    for r in inspector.records("sites"):
        if r.get("rarity") not in RARITY or r.get("loc") is None:
            continue
        gems = sum(int(r.get(g) or 0) for g in GEMS)
        out.append((r["path"], int(r.get("level") or 0), r["rarity"], int(r["loc"]), gems))
    return out


def expected_rolls(chance):
    p, n = max(5, chance) / 100, 0.0
    for _ in range(8):
        n += min(p, 1.0)
        p *= 0.75
    return n


def table(freq):
    S = sites()
    res = {}
    for tname, bit, mod in TERRAIN:
        n = expected_rolls(freq + mod)
        pool = {r: [s for s in S if s[2] == r and s[3] & bit] for r in RARITY}
        w = {r: RARITY[r] for r in RARITY if pool[r]}
        tot = sum(w.values())
        res[tname] = {"avg": n}
        for path in PATHS:
            cells = []
            for lvl in (1, 2, 3):
                ns = ng = 0.0
                for r in w:
                    found = [s for s in pool[r] if s[0] == path and 1 <= s[1] <= lvl]
                    ns += n * w[r] / tot * len(found) / len(pool[r])
                    ng += n * w[r] / tot * sum(s[4] for s in found) / len(pool[r])
                cells.append((ns, ng))
            res[tname][path] = cells
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--freq", type=int, default=60)
    a = ap.parse_args()
    t = table(a.freq)
    names = [x[0] for x in TERRAIN]
    print("| Path | " + " | ".join(names) + " |")
    print("|---|" + "---|" * len(names))
    print("| Rolls (all sites) | " + " | ".join(f"{t[n]['avg']:.2f}" for n in names) + " |")
    for p in PATHS:
        print(f"| {p} | " + " | ".join("/".join(f"{c[0]:.2f}".lstrip("0") for c in t[n][p]) + " · " +
                                       "/".join(f"{c[1]:.2f}".lstrip("0") for c in t[n][p]) for n in names) + " |")
    print("| **Gems, every path searched** | " + " | ".join(
        "/".join(f"{sum(t[n][p][i][1] for p in PATHS):.2f}" for i in range(3)) for n in names) + " |")


if __name__ == "__main__":
    main()
