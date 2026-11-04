#!/usr/bin/env python3
"""What a mod does to Dominions 6 magic, read from a dom6-modinspector output folder (any mod).

  python3 -I modmagic.py summary DATA                        counts: new / better / worse / mixed / AI-only,
                                                             by school and by path
  python3 -I modmagic.py better DATA [--paths E2N2G1H2] [--school Alt] [--top 40]
                                                             spells the mod made better, best first, with why
  python3 -I modmagic.py worse DATA [same options]           spells the mod made worse
  python3 -I modmagic.py new DATA [same options]             spells the mod added
  python3 -I modmagic.py spell DATA NAME                     one spell's changes, scored line by line

DATA = a folder written by dom6-modinspector (inspect_mod.py <mod.dm> --out DATA), e.g.
dom6-scbm/data/inspector. --paths keeps spells a mage with those paths can cast (no gems/boosters counted).
Scoring (per changed field, weight x direction): path level 3, research level 2, gem cost 2, area 2,
effects 2, damage 2 (area read from aoe_s), fatigue 1, precision 1, range 1, cast time 1, MR-negates removed 2, ignores
shields 2. AI-weight-only changes (aispellmod, ainocast...) are reported apart: they change what the AI
casts on its own, not the spell - script what the AI now avoids.
"""
import os
import re
import sys

AI_KEYS = {"aispellmod", "aiassmod", "ainocast", "aibadlvl", "aisinglerec"}
LOWER = {"pathlevel1": 3, "pathlevel2": 3, "researchlevel": 2, "gemcost": 2, "fatiguecost": 1, "casttime": 1}
HIGHER = {"aoe_s": 2, "nreff": 2, "damage": 2, "precision": 1, "rng_bat": 1}
FLAGS = {"mrnegates": -2, "mrnegateseasily": -2, "hardmrneg": +2, "ignoreshield": +2}   # flag added = this x 1
ORDER = ["Conjuration", "Alteration", "Evocation", "Construction", "Enchantment", "Thaumaturgy", "Blood", "Divine"]


def load(data):
    txt = open(os.path.join(data, "mod_pages.txt"), encoding="utf-8").read()
    recs = []
    for block in re.split(r"\n(?==== )", txt):
        m = re.match(r"=== spell (\S+): (.*)", block)
        if not m:
            continue
        tag = "new" if "\n[new]" in block else "changed" if "\n[changed]" in block else None
        if not tag:
            continue
        lines = block.split("\n")
        diff = {}
        if "changed from vanilla:" in block:
            for ln in block.split("changed from vanilla:")[1].split("\n")[1:]:
                if not ln.startswith("  "):
                    break
                k, _, v = ln.strip().partition(": ")
                old, _, new = v.partition(" -> ")
                diff[k] = (old.strip(), new.strip())
        school, lvl = (lines[1].strip().rsplit(" ", 1) + ["?"])[:2] if len(lines) > 1 else ("?", "?")
        g = lambda k: (re.search(r"\[" + k + r"\]: (.*)", block) or [None, ""])[1].strip()
        recs.append({"id": m.group(1), "name": m.group(2).strip(), "tag": tag, "school": school, "level": lvl,
                     "kind": lines[3].strip() if len(lines) > 3 else "", "path": lines[4].strip() if len(lines) > 4 else "",
                     "range": g("rng_bat"), "aoe": g("aoe_s"), "fat": g("fatiguecost"), "diff": diff,
                     "desc": ((re.search(r"\ndescription: (.*)", block) or [None, ""])[1].strip()
                              or " ".join(re.findall(r'#details "([^"]*)', block)))})
    return recs


def num(v, lvl):
    """inspector value -> number at the spell's own path level (1000+N = N+lvl, 2000+N = N+2lvl...)"""
    v = v.strip()
    if v in ("", "-"):
        return 0.0
    m = re.match(r"(-?\d+)\+? *(?:\[(\d+)/lvl\])?", v)          # '30+ [5/lvl]', '6+ [2/lvl]'
    if m and m.group(2):
        return float(m.group(1)) + float(m.group(2)) * lvl
    m = re.match(r"(-?\d+)\s*([FAWESDNGB])?$", v)              # '5', '-2012', '5E' (gem cost)
    if not m:
        return None
    n = int(m.group(1))
    if 1000 <= n < 5000:
        n = n % 1000 + (n // 1000) * lvl
    elif n < 0 or n >= 900 and m.group(2):                     # negative codes / 999 = special, skip
        return None
    return float(n)


def score(r):
    """(score, [reasons]) - positive = the mod made the spell better"""
    lvl = int(re.search(r"\d", r["path"]).group()) if re.search(r"\d", r["path"]) else 1
    s, why = 0, []
    for k, (old, new) in r["diff"].items():
        if k in LOWER or k in HIGHER:
            a, b = num(old, lvl), num(new, lvl)
            if a is None or b is None or a == b:
                continue
            w = LOWER.get(k) or HIGHER.get(k)
            better = (b < a) if k in LOWER else (b > a)
            if k == "gemcost" and a == 0:                       # a gem cost appearing is worse
                better = False
            s += w if better else -w
            why.append(("+" if better else "-") + f"{k} {old}->{new}")
        elif k in FLAGS:
            added = new not in ("-", "0", "")
            d = FLAGS[k] * (1 if added else -1)
            s += d
            why.append(("+" if d > 0 else "-") + f"{k} {'added' if added else 'removed'}")
    return s, why


def kind_of(r):
    if r["tag"] == "new":
        return "new"
    keys = set(r["diff"])
    if keys and keys <= AI_KEYS:
        return "AI only"
    s, why = score(r)
    if not why:
        return "other"                                          # e.g. description, summons, effect changed
    pos, neg = any(w[0] == "+" for w in why), any(w[0] == "-" for w in why)
    return "better" if pos and not neg else "worse" if neg and not pos else "mixed"


def can_cast(path, paths):
    have = dict((p, int(n)) for p, n in re.findall(r"([FAWESDNGBH])(\d+)", paths))
    need = re.findall(r"([FAWESDNGBH])(\d+)", path)
    return bool(need) and all(have.get(p, 0) >= int(n) for p, n in need)


def pick(recs, a):
    paths = a[a.index("--paths") + 1] if "--paths" in a else ""
    sch = a[a.index("--school") + 1] if "--school" in a else ""
    return [r for r in recs if (not paths or can_cast(r["path"], paths)) and r["school"].startswith(sch)]


def row(r, extra=""):
    return (f"| {r['name']} | {r['school'][:5]} {r['level']} | {r['path']} | {r['kind']} | {r['range']} | {r['aoe']} | "
            f"{r['fat']} | {extra.replace('|', '/')[:220]} |")


HEAD = ["| Spell | School | Path | Kind | Rng | Area | Fat | Why |", "|---|---|---|---|---|---|---|---|"]


def main(a):
    if len(a) < 2 or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    cmd, data = a[0], a[1]
    recs = load(data)
    top = int(a[a.index("--top") + 1]) if "--top" in a else 40
    if cmd == "summary":
        from collections import Counter
        kinds = Counter(kind_of(r) for r in recs)
        print(f"{len(recs)} spells touched: " + ", ".join(f"{k} {n}" for k, n in kinds.most_common()))
        for title, key in (("by school", lambda r: r["school"].split()[0] if r["school"] else "?"),
                           ("by path", lambda r: (re.findall(r"([FAWESDNGBH])\d", r["path"]) or ["?"])[0])):
            c = {}
            for r in recs:
                c.setdefault(key(r), Counter())[kind_of(r)] += 1
            print(f"\n{title}: (new / better / worse / mixed / AI only)")
            for k, v in sorted(c.items(), key=lambda kv: -sum(kv[1].values())):
                print(f"  {k:14} {v['new']:4} {v['better']:4} {v['worse']:4} {v['mixed']:4} {v['AI only']:4}")
    elif cmd in ("better", "worse"):
        rows = [(score(r), r) for r in pick(recs, a) if r["tag"] == "changed"]
        rows = [x for x in rows if (x[0][0] > 0 if cmd == "better" else x[0][0] < 0)]
        rows.sort(key=lambda x: -x[0][0] if cmd == "better" else x[0][0])
        print("\n".join(HEAD + [row(r, f"{s:+d}: " + "; ".join(why)) for (s, why), r in rows[:top]]))
        print(f"\n{len(rows)} spells {cmd}" + (f" (top {top} shown)" if len(rows) > top else ""))
    elif cmd == "new":
        rows = [r for r in pick(recs, a) if r["tag"] == "new"]
        print("\n".join(HEAD + [row(r, r["desc"][:200]) for r in rows[:top]]))
        print(f"\n{len(rows)} new spells")
    elif cmd == "spell":
        name = " ".join(x for x in a[2:] if not x.startswith("--")).lower()
        for r in recs:
            if r["name"].lower() == name or name in r["name"].lower():
                s, why = score(r)
                print(f"{r['name']} ({r['tag']}, {r['school']} {r['level']}, {r['path']}): score {s:+d}, {kind_of(r)}")
                for k, (o, n) in r["diff"].items():
                    print(f"  {k}: {o} -> {n}")
                print("  scored:", "; ".join(why) or "nothing scoreable")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
