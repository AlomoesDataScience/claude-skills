"""Query the local copy of the Dominions 6 Mod Inspector (built by build.py into ../data).

  python3 -I inspector.py KIND NAME|ID [--all]   the full page(s): unit, spell, item, weapon, armor,
                                                 site, merc, event, nation (name: exact, else substring)
  python3 -I inspector.py grep REGEX [--kind K]  objects whose page matches, with the matching lines
  python3 -I inspector.py filter KIND COND...    table of matching objects, e.g.
                                                 filter unit holy=1 goldcost<40 "nationname~Ulm"
                                                 COND: key=v  key!=v  key<n  key>n  key<=n  key>=n
                                                 key~text (substring, case-insensitive)  key (present, not 0)
  python3 -I inspector.py keys KIND              every computed field of that kind and how often it is set
  python3 -I inspector.py sprite NAME|ID         paths of a unit's sprite images
  python3 -I inspector.py version                source commit and counts

  --data DIR (before the command) queries another copy, e.g. a modded game written by the
  dom6-modinspector skill: inspector.py --data /tmp/dom6-modinspect/ananke unit penitent
"""
import json
import os
import re
import sys

VANILLA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
DATA = VANILLA
KINDS = {"unit": "units", "spell": "spells", "item": "items", "weapon": "weapons", "wpn": "weapons",
         "armor": "armor", "armour": "armor", "site": "sites", "merc": "mercs", "mercenary": "mercs",
         "event": "events", "nation": "nations"}
for k in set(KINDS.values()):
    KINDS[k] = k


def kind_of(word):
    k = KINDS.get(word.lower())
    if not k:
        sys.exit(f"unknown kind {word!r}: use one of " + ", ".join(sorted(set(KINDS.values()))))
    return k


def pages(kind):
    text = open(os.path.join(DATA, "pages", kind + ".txt"), encoding="utf-8").read()
    for block in text.split("\n\n"):
        block = block.strip("\n")
        if block.startswith("=== "):
            m = re.match(r"=== \S+ (-?[\d.]+): (.*)", block)        # nation variants have ids like 239.01
            yield m.group(1), m.group(2), block


def records(kind):
    with open(os.path.join(DATA, "records", kind + ".jsonl"), encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)


def find(kind, q):
    allp = list(pages(kind))
    if re.fullmatch(r"-?[\d.]+", q):
        return [p for p in allp if float(p[0]) == float(q)]
    ql = q.lower()
    exact = [p for p in allp if p[1].lower() == ql or p[1].lower().split(" - ")[-1].strip("“” ") == ql]
    return exact or [p for p in allp if ql in p[1].lower()]


def show(kind, q, all_=False):
    hits = find(kind, q)
    if not hits:
        sys.exit(f"no {kind} matches {q!r}")
    if len(hits) > 1 and not all_:
        print(f"{len(hits)} {kind} match {q!r} (give an id, or --all to print them all):")
        for i, name, _ in hits[:60]:
            print(f"  {i:>5}  {name}")
        return
    print("\n\n".join(p[2] for p in hits))


def grep(rx, kinds):
    r = re.compile(rx, re.I)
    for kind in kinds:
        for i, name, block in pages(kind):
            lines = [l for l in block.split("\n")[1:] if r.search(l)]
            if lines:
                print(f"{kind[:-1] if kind.endswith('s') else kind} {i}: {name}")
                for l in lines[:6]:
                    print("    " + (l if len(l) < 220 else l[:217] + "..."))


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def flat_text(v):
    if isinstance(v, dict):
        return " ".join(flat_text(x) for x in v.values())
    if isinstance(v, list):
        return " ".join(flat_text(x) for x in v)
    return str(v)


def test(d, cond):
    m = re.fullmatch(r"([A-Za-z0-9_]+)\s*(!=|<=|>=|=|<|>|~)\s*(.*)", cond)
    if not m:
        v = d.get(cond)
        return v not in (None, "", "0", 0, [], {})
    k, op, want = m.groups()
    v = d.get(k)
    if op == "~":
        return v is not None and want.lower() in flat_text(v).lower()
    if v is None and num(want) == 0:                    # unset fields mean 0
        v = 0
    if op in ("=", "!="):
        same = str(v if v is not None else "").lower() == want.lower() or (num(v) is not None and num(v) == num(want))
        return same if op == "=" else not same
    a, b = num(v), num(want)
    if a is None or b is None:
        return False
    return {"<": a < b, ">": a > b, "<=": a <= b, ">=": a >= b}[op]


def filt(kind, conds):
    keys = [re.split(r"!=|<=|>=|=|<|>|~", c)[0] for c in conds]
    extra = {"units": ["goldcost", "rcost", "typechar", "nationname"], "spells": ["research", "mpath", "type"],
             "items": ["constlevel", "mainpath", "mainlevel", "type"]}.get(kind, [])
    cols = list(dict.fromkeys(extra + keys))
    rows = [d for d in records(kind) if all(test(d, c) for c in conds)]
    print(f"{len(rows)} {kind}")
    print("   id  name" + "".join(f" | {c}" for c in cols))
    for d in rows:
        name = d.get("fullname") or d.get("name") or ""
        vals = []
        for c in cols:
            v = d.get(c, "")
            vals.append(flat_text(v)[:40] if isinstance(v, (dict, list)) else str(v))
        print(f"{d.get('id'):>5}  {name}" + "".join(f" | {v}" for v in vals))


def keys(kind):
    count = {}
    for d in records(kind):
        for k, v in d.items():
            if v not in (None, "", "0", 0, [], {}):
                count[k] = count.get(k, 0) + 1
    for k, n in sorted(count.items(), key=lambda x: -x[1]):
        print(f"{n:>6}  {k}")


def sprite(q):
    hits = find("units", q)
    if len({h[1] for h in hits}) == 1:                 # the site lists some units twice (ids like 6404.01)
        hits = hits[:1]
    if len(hits) != 1:
        return show("units", q)
    mods = {}
    if os.path.exists(os.path.join(DATA, "mods.json")):                 # mod sprites: mods/<path> in the mod's folder
        mods = json.load(open(os.path.join(DATA, "mods.json")))
    if mods:                                           # the site draws no image for mod units: use #spr1/#spr2
        rec = next((d for d in records("units") if str(d.get("id")) == hits[0][0]), {})
        sp = rec.get("sprite") if isinstance(rec.get("sprite"), dict) else rec
        sprs = [sp[k] for k in ("spr1", "spr2") if isinstance(sp.get(k), str)]
        if sprs:
            for spr in sprs:
                tgas = [os.path.join(d, spr.lstrip("./")) for d in mods["folders"]]
                found = [t for t in tgas if os.path.exists(t)]
                print(found[0] if found else f"{spr} (not found in the mod folders)")
            return
    for l in hits[0][2].split("\n"):
        if l.startswith("image: "):
            rel = l[7:]
            p = os.path.abspath(os.path.join(VANILLA, rel))
            for alt in (p, p.replace("_1.png", "_2.png")):
                print(alt, "" if os.path.exists(alt) else "(missing: build without --no-images)")


def main():
    global DATA
    a = sys.argv[1:]
    if a[:1] == ["--data"]:
        DATA, a = a[1], a[2:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd = a[0].lower()
    if cmd == "version":
        print(open(os.path.join(DATA, "VERSION")).read().strip())
    elif cmd == "grep":
        kinds = [kind_of(a[a.index("--kind") + 1])] if "--kind" in a else ["units", "spells", "items", "weapons", "armor", "sites", "mercs", "events", "nations"]
        grep(a[1], kinds)
    elif cmd == "filter":
        filt(kind_of(a[1]), a[2:])
    elif cmd == "keys":
        keys(kind_of(a[1]))
    elif cmd == "sprite":
        sprite(" ".join(x for x in a[1:]))
    else:
        all_ = "--all" in a
        rest = [x for x in a[1:] if x != "--all"]
        show(kind_of(cmd), " ".join(rest), all_)


if __name__ == "__main__":
    main()
