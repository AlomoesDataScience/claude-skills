#!/usr/bin/env python3
"""Read, compare and check Space Empires IV data files (Data/*.txt).

  se4data.py list FILE [FIELD=TEXT ...]      record names (optionally filtered, substring match)
  se4data.py show FILE NAME                  one record, every field
  se4data.py fields FILE                     field names and how many records use each
  se4data.py diff MOD_ROOT [--base GAME] [--detail]   per file: new, removed, changed records
  se4data.py check MOD_ROOT [--overlay]      ERROR: missing files, unknown techs/abilities, empty or
                                             miscounted requirements; WARN: duplicate names, a tech level
                                             above its maximum; NOTE: deliberately locked (max level 0)
  se4data.py gather NOTES_DIR BUILD_ROOT [--detail]  game-format records in design notes (any .txt
                                             outside _Builds) that the build lacks, by data file
  se4data.py merge NOTES_DIR BUILD_ROOT OUT_ROOT     new build: vanilla Data/ + Pictures/, the old
                                             build pasted over, then the notes' records it lacks appended
                                             (MERGE_LOG.txt says what and from where)
  se4data.py tree MOD_ROOT [--base GAME] [GROUP]      tech areas by group: cost, levels, needs, unlocks

MOD_ROOT is a folder with Data/ in it (a mod folder, or the game's se4 folder). FILE is a path to
one data file. GAME defaults to the Steam install (--base GAME to change). --overlay: the mod
is copied over the game's Data/ (WMD style), so files it lacks are the vanilla ones, not an error. Files are read as latin-1 and never written.
"""
import os, re, sys, signal
from collections import Counter, OrderedDict

signal.signal(signal.SIGPIPE, signal.SIG_DFL)
GAME = os.path.expanduser("~/.local/share/Steam/steamapps/common/Space Empires IV Deluxe/se4")
KV = re.compile(r"^(\S[^:=]*?)\s*:=\s?(.*)$")


def parse(path, loose=False):
    """Records between *BEGIN* and *END* (anywhere in the file if loose); a new record starts at each Name field."""
    recs, cur, on = [], None, loose
    for raw in open(path, encoding="latin-1"):
        line = raw.rstrip("\r\n")
        if line.startswith("*BEGIN*"):
            on = True; continue
        if line.startswith("*END*"):
            break
        if not on:
            continue
        m = KV.match(line)
        if not m:
            continue
        k, v = m.group(1).strip(), m.group(2).strip()
        if cur is None or (k == "Name" and "Name" in cur):
            cur = OrderedDict(); recs.append(cur)
        if k in cur:                       # repeated key inside a record: keep both
            n = 2
            while f"{k} #{n}" in cur:
                n += 1
            k = f"{k} #{n}"
        cur[k] = v
    return recs


def data_dir(root):
    d = os.path.join(root, "Data")
    return d if os.path.isdir(d) else root


def load(root):
    d = data_dir(root)
    return {f: parse(os.path.join(d, f)) for f in sorted(os.listdir(d)) if f.lower().endswith(".txt")}


def ability_names(path):
    """Abilities.txt lists names flush left, each followed by indented Value1/Value2 lines."""
    names, prev = set(), None
    for raw in open(path, encoding="latin-1"):
        line = raw.rstrip("\r\n")
        if line.startswith("  Value1") and prev:
            names.add(prev)
        prev = line.strip() if line and not line.startswith(" ") and not line.startswith("=") else None
    return names


def numbered(rec, count_key, item_fmt):
    try:
        n = int(rec.get(count_key, "0") or 0)
    except ValueError:
        n = -1
    return n, [rec.get(item_fmt.format(i), "") for i in range(1, max(n, 0) + 1)]


def name_of(rec):
    return rec.get("Name", "(no name)")


def pick(base_root, mod_root, fname):
    """Mod's own file if it has one, else the base game's (what the game falls back to for bitmaps only)."""
    for r in (mod_root, base_root):
        p = os.path.join(data_dir(r), fname)
        if os.path.isfile(p):
            return p, r is mod_root
    return None, False


def cmd_list(path, *filters):
    for rec in parse(path):
        ok = True
        for f in filters:
            k, _, t = f.partition("=")
            ok &= t.lower() in rec.get(k, "").lower()
        if ok:
            print(name_of(rec))


def cmd_show(path, name):
    hits = [r for r in parse(path) if name_of(r).lower() == name.lower()] or \
           [r for r in parse(path) if name.lower() in name_of(r).lower()]
    if not hits:
        sys.exit(f"no record named {name!r}")
    for r in hits[:5]:
        w = max(map(len, r))
        print("\n".join(f"{k:<{w}} := {v}" for k, v in r.items()), end="\n\n")
    if len(hits) > 5:
        print(f"... {len(hits) - 5} more matches")


def cmd_fields(path):
    c = Counter(re.sub(r" #\d+$", "", k) for r in parse(path) for k in r)
    for k, n in c.most_common():
        print(f"{n:6}  {k}")


def cmd_diff(mod, base, detail):
    m, b = load(mod), load(base)
    for f in sorted(set(m) | set(b)):
        if f not in m:
            print(f"{f}: not in mod (vanilla used if the mod is copied over Data/; a Path.txt mod folder needs it)"); continue
        if f not in b:
            print(f"{f}: new file, {len(m[f])} records"); continue
        mi = {name_of(r): r for r in m[f]}; bi = {name_of(r): r for r in b[f]}
        new = [n for n in mi if n not in bi]; gone = [n for n in bi if n not in mi]
        chg = [n for n in mi if n in bi and mi[n] != bi[n]]
        if not (new or gone or chg):
            print(f"{f}: same as base"); continue
        print(f"{f}: {len(m[f])} records (base {len(b[f])}): {len(new)} new, {len(gone)} removed, {len(chg)} changed")
        if detail:
            for n in new:
                print(f"  + {n}")
            for n in gone:
                print(f"  - {n}")
            for n in chg:
                d = [k for k in set(mi[n]) | set(bi[n]) if mi[n].get(k) != bi[n].get(k)]
                print(f"  ~ {n}: " + "; ".join(f"{k}: {bi[n].get(k, '-')} -> {mi[n].get(k, '-')}" for k in sorted(d)[:8])
                      + (f" (+{len(d) - 8} more)" if len(d) > 8 else ""))


def cmd_check(mod, base, overlay=False):
    count = Counter()
    def bad(msg, level="ERROR"):
        count[level] += 1; print(f"{level:5} {msg}")
    have = set(os.listdir(data_dir(mod)))
    for f in sorted(os.listdir(os.path.join(base, "Data"))):
        if f not in have and not overlay:
            bad(f"Data/{f} missing (Path.txt: a mod folder must hold every data file; only bitmaps fall back;"
                " use --overlay for a mod copied over the game's own Data/)")
    tp, _ = pick(base, mod, "TechArea.txt"); ap, _ = pick(base, mod, "Abilities.txt")
    techs = {name_of(r): r for r in parse(tp)} if tp else {}
    abil = ability_names(ap) if ap else set()
    for f in ("Components.txt", "Facility.txt", "VehicleSize.txt"):    # vanilla uses a few unlisted ones
        bp = os.path.join(base, "Data", f)
        for r in parse(bp) if os.path.isfile(bp) else []:
            abil.update(numbered(r, "Number of Abilities", "Ability {} Type")[1])
    for f in ("TechArea.txt", "Components.txt", "Facility.txt", "VehicleSize.txt"):
        p = os.path.join(data_dir(mod), f)
        if not os.path.isfile(p):
            continue
        recs = parse(p)
        dup = [n for n, c in Counter(map(name_of, recs)).items() if c > 1]
        for n in dup:
            bad(f"{f}: duplicate name {n!r} (lookups are by name: check in game which one wins)", "WARN")
        for r in recs:
            n, reqs = numbered(r, "Number of Tech Req", "Tech Area Req {}")
            if n < 0:
                bad(f"{f}: {name_of(r)!r}: Number of Tech Req is not a number")
            for i, t in enumerate(reqs, 1):
                if not t:
                    bad(f"{f}: {name_of(r)!r}: Tech Area Req {i} is empty (count says {n})")
                elif t not in techs:
                    bad(f"{f}: {name_of(r)!r}: tech {t!r} is not in TechArea.txt")
                else:
                    lvl = r.get(f"Tech Level Req {i}", "0")
                    mx = techs[t].get("Maximum Level", "0")
                    if lvl.isdigit() and mx.isdigit() and int(lvl) > int(mx):
                        if mx == "0":
                            bad(f"{f}: {name_of(r)!r}: locked behind {t} (max level 0), never researchable", "NOTE")
                        else:
                            bad(f"{f}: {name_of(r)!r}: needs {t} {lvl} but its Maximum Level is {mx}: never unlocks", "WARN")
            if "Number of Abilities" in r:
                n, ab = numbered(r, "Number of Abilities", "Ability {} Type")
                for i, a in enumerate(ab, 1):
                    if not a:
                        bad(f"{f}: {name_of(r)!r}: Ability {i} Type missing (count says {n})")
                    elif abil and a not in abil:
                        bad(f"{f}: {name_of(r)!r}: ability {a!r} is not in Abilities.txt")
    print(", ".join(f"{count[k]} {k.lower()}" for k in ("ERROR", "WARN", "NOTE") if count[k]) or "no problems found")


def cmd_tree(mod, base, group=None):
    tp, _ = pick(base, mod, "TechArea.txt")
    techs = parse(tp)
    unlock = {}
    for f in ("Components.txt", "Facility.txt", "VehicleSize.txt"):
        p, _ = pick(base, mod, f)
        for r in parse(p) if p else []:
            _, reqs = numbered(r, "Number of Tech Req", "Tech Area Req {}")
            for i, t in enumerate(reqs, 1):
                unlock.setdefault(t, []).append(f"{name_of(r)} ({f[:4]} L{r.get(f'Tech Level Req {i}', '?')})")
    by = OrderedDict()
    for r in techs:
        by.setdefault(r.get("Group", "?"), []).append(r)
    for g, rs in by.items():
        if group and group.lower() not in g.lower():
            continue
        print(f"## {g}")
        for r in rs:
            _, reqs = numbered(r, "Number of Tech Req", "Tech Area Req {}")
            need = ", ".join(f"{t} {r.get(f'Tech Level Req {i}', '')}" for i, t in enumerate(reqs, 1)) or "-"
            u = unlock.get(name_of(r), [])
            print(f"  {name_of(r)}  [max {r.get('Maximum Level')}, cost {r.get('Level Cost')}, start {r.get('Start Level')}]"
                  f"  needs: {need}  unlocks {len(u)}: " + ", ".join(u[:6]) + (" ..." if len(u) > 6 else ""))
    needed = {t for r in techs for t in numbered(r, "Number of Tech Req", "Tech Area Req {}")[1]}
    dead = [name_of(r) for r in techs if name_of(r) not in unlock and name_of(r) not in needed]
    if dead and not group:
        print(f"## Dead ends ({len(dead)}): unlock nothing and no tech needs them")
        print("  " + ", ".join(dead))


FILE_KINDS = ("Components.txt", "Facility.txt", "TechArea.txt", "VehicleSize.txt")


def collect(src, base):
    """{data file: {name: (record, source file)}} for game-format records in notes outside _Builds,
    plus the names written differently in two notes (newest file wins). AI files (*_AI_*) are skipped."""
    shapes = {}
    for f in FILE_KINDS:
        shapes[f] = {re.sub(r"\d+", "#", k) for r in parse(os.path.join(base, "Data", f)) for k in r}
    found, clash = {f: OrderedDict() for f in FILE_KINDS}, []
    for dp, dn, fn in os.walk(src):
        dn[:] = sorted(d for d in dn if d != "_Builds" and not d.startswith("."))
        for n in sorted(fn):
            if not n.lower().endswith(".txt") or "_ai_" in n.lower():
                continue
            path = os.path.join(dp, n)
            for r in parse(path, loose=True):
                if "Name" not in r or len(r) < 5:
                    continue
                keys = {re.sub(r"\d+", "#", k) for k in r}
                kind = max(FILE_KINDS, key=lambda f: len(keys & shapes[f]) / len(keys | shapes[f]))
                rel = os.path.relpath(path, src)
                old = found[kind].get(name_of(r))
                if old is None:
                    found[kind][name_of(r)] = (r, rel)
                elif dict(old[0]) != dict(r):          # the most recently edited note wins
                    if os.path.getmtime(path) > os.path.getmtime(os.path.join(src, old[1])):
                        found[kind][name_of(r)] = (r, rel); clash.append((kind, name_of(r), rel, old[1]))
                    else:
                        clash.append((kind, name_of(r), old[1], rel))
    return found, clash


def build_names(build, f, base):
    p = os.path.join(data_dir(build), f)
    return {name_of(r): r for r in parse(p)} if os.path.isfile(p) else {}


def cmd_gather(src, build, base, detail):
    """Game-format records in design notes (outside _Builds) that the build does not have yet."""
    found, clash = collect(src, base)
    for f in FILE_KINDS:
        have = build_names(build, f, base)
        recs = found[f]
        miss = [(n, w) for n, (r, w) in recs.items() if n not in have]
        diff = sum(1 for n, (r, w) in recs.items() if n in have and dict(have[n]) != dict(r))
        print(f"{f}: {len(recs)} named records in the notes, {len(recs) - len(miss)} already in the build"
              f" ({diff} written differently there), {len(miss)} not yet")
        by = OrderedDict()
        for n, w in miss:
            by.setdefault(w, []).append(n)
        for w, ns in by.items():
            print(f"  {w}: " + (", ".join(ns) if detail else f"{len(ns)} ({ns[0]}{', ...' if len(ns) > 1 else ''})"))
    if clash:
        print(f"{len(clash)} names written differently in two notes (the newer file is used, listed first):")
        for k, n, a, b in clash[: None if detail else 10]:
            print(f"  {k}: {n!r}: {a} | {b}")


def write_record(rec, width):
    out = []
    for k, v in rec.items():
        k = re.sub(r" #\d+$", "", k)
        out.append(f"{k:<{width}}:= {v}".rstrip() if v == "" else f"{k:<{width}}:= {v}")
    return "\r\n".join(out) + "\r\n\r\n"


def cmd_merge(src, build, out, base):
    """the user's build method: vanilla Data/ and Pictures/ first, the previous build pasted over them,
    then the notes' records the build lacks appended to each data file; MERGE_LOG.txt says what."""
    import shutil
    if os.path.exists(out) and os.listdir(out):
        sys.exit(f"{out} exists and is not empty: pick a new folder")
    for d in ("Data", "Pictures"):
        shutil.copytree(os.path.join(base, d), os.path.join(out, d), dirs_exist_ok=True)
    shutil.copytree(build, out, dirs_exist_ok=True)
    seen = {}
    for dp, dn, fn in os.walk(out):                 # the game runs on Windows rules: names ignore case
        for n in dn + fn:
            k = os.path.join(dp, n).lower()
            if k in seen:
                print(f"WARN  two names differ only in case: {seen[k]} / {os.path.join(dp, n)}")
            seen[k] = os.path.join(dp, n)
    found, clash = collect(src, base)
    log = [f"merge: build {build}", f"       notes {src}", ""]
    for f in FILE_KINDS:
        p = os.path.join(data_dir(out), f)
        if not os.path.isfile(p):
            shutil.copy(os.path.join(base, "Data", f), p)
            log.append(f"{f}: not in the build, started from vanilla")
        text = open(p, encoding="latin-1", newline="").read()
        have = build_names(out, f, base)
        m = re.search(r"^(Name\s*):=", text[text.index("*BEGIN*"):], re.M)
        width = len(m.group(1)) if m else 22
        add = [(n, r, w) for n, (r, w) in found[f].items() if n not in have]
        diff = [(n, w) for n, (r, w) in found[f].items() if n in have and dict(have[n]) != dict(r)]
        cut = text.rfind("\n", 0, text.rindex("*END*"))          # line before *END* (the ===== rule)
        cut = text.rfind("\n", 0, cut) + 1
        text = text[:cut] + "".join(write_record(r, width) for n, r, w in add) + text[cut:]
        open(p, "w", encoding="latin-1", newline="").write(text)
        log.append(f"{f}: added {len(add)} records, kept the build's version of {len(diff)} that the notes write differently")
        log += [f"  + {n}   ({w})" for n, r, w in add]
        log += [f"  = {n}   (notes: {w})" for n, w in diff]
    if clash:
        log.append(f"names written differently in two notes (the newer file was used): {len(clash)}")
        log += [f"  {k}: {n}: used {a}, not {b}" for k, n, a, b in clash]
    open(os.path.join(out, "MERGE_LOG.txt"), "w", encoding="latin-1", newline="\r\n").write("\n".join(log) + "\n")
    print("\n".join(l for l in log if not l.startswith("  ")))
    print(f"log: {os.path.join(out, 'MERGE_LOG.txt')}")


def main(a):
    if len(a) < 2 or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    base = GAME
    if "--base" in a:
        i = a.index("--base"); base = a[i + 1]; del a[i:i + 2]
    detail, overlay = "--detail" in a, "--overlay" in a
    a = [x for x in a if x not in ("--detail", "--overlay")]
    c = a[0]
    if c == "list":   cmd_list(*a[1:])
    elif c == "show": cmd_show(a[1], a[2])
    elif c == "fields": cmd_fields(a[1])
    elif c == "diff": cmd_diff(a[1], base, detail)
    elif c == "check": cmd_check(a[1], base, overlay)
    elif c == "gather": cmd_gather(a[1], a[2], base, detail)
    elif c == "merge": cmd_merge(a[1], a[2], a[3], base)
    elif c == "tree": cmd_tree(a[1], base, a[2] if len(a) > 2 else None)
    else: sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
