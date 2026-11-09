#!/usr/bin/env python3
"""Cleanup pipeline: catalogue a folder's clutter for the user's review; nothing is ever deleted.

  cleanup.py scan DIR [--out NAME]   catalogue -> Archive/cleanup/<date>-<name>.md: installers, archives,
                                     duplicates (same content), copy-named files, caches, temp files, empty
                                     files/dirs, very large files, loose files in DIR's top level - each line
                                     a checkbox with size, date and a suggested action. Prints the summary.
  cleanup.py apply CATALOGUE         move every line the user ticked [x] to Archive/cleanup/held-<date>/<same path>
                                     and write a manifest there (reversible)
  cleanup.py undo HELD_DIR           move everything in a held folder back where it came from
Pure standard library. Skips .git, Archive/ and .claude/ (skills have their own tools)."""
import collections, datetime, hashlib, json, os, re, shutil, sys

ROOT = os.path.expanduser(os.environ.get("CLEANUP_ROOT", "~/Desktop/AI Development"))   # env: tests
OUT = os.path.join(ROOT, "Archive", "cleanup")
SKIP = {".git", "Archive", ".claude", ".venv", "venv"}
CAT = {  # category: (test, suggestion)
    "installer": (lambda n: re.search(r"\.(exe|msi|dmg)$|^gog_.*\.sh$|^setup_", n, re.I),
                  "install (install-windows-games) or file under the game; then hold"),
    "archive": (lambda n: re.search(r"\.(zip|7z|rar|tar|tgz|tar\.gz|tar\.xz)$", n, re.I),
                "extract/file via library-intake if not done; then hold the archive"),
    "copy-named": (lambda n: re.search(r"\(\d\)\.|\bcopy\b|~$|\.orig$", n, re.I), "probably a stray copy - compare, hold"),
    "temp": (lambda n: re.search(r"\.(tmp|part|crdownload|swp|bak)$", n, re.I), "temporary file - hold"),
    "cache": (lambda n: n.endswith(".pyc"), "regenerates - hold"),
}
CACHE_DIRS = {"__pycache__", ".pytest_cache", "node_modules", ".mypy_cache"}


def human(b):
    for u in ("B", "KB", "MB", "GB"):
        if b < 1024:
            return f"{b:.0f} {u}"
        b /= 1024
    return f"{b:.1f} TB"


def sha(p):
    h = hashlib.sha1()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def scan(top, name):
    top = os.path.abspath(top)
    rows = collections.defaultdict(list)       # category -> [(rel, size, mtime, note)]
    sizes = collections.defaultdict(list)
    for d, ds, fs in os.walk(top):
        for x in list(ds):
            if x in CACHE_DIRS:
                p = os.path.join(d, x)
                sz = sum(os.path.getsize(os.path.join(a, f)) for a, _, ff in os.walk(p) for f in ff)
                rows["cache"].append((os.path.relpath(p, ROOT), sz, os.path.getmtime(p), "cache folder - regenerates; hold"))
        ds[:] = [x for x in ds if x not in SKIP and x not in CACHE_DIRS]
        if not fs and not ds and d != top:
            rows["empty"].append((os.path.relpath(d, ROOT) + "/", 0, os.path.getmtime(d), "empty folder - hold"))
        for f in fs:
            p = os.path.join(d, f)
            if os.path.islink(p):
                continue
            try:
                sz, mt = os.path.getsize(p), os.path.getmtime(p)
            except OSError:
                continue
            rel = os.path.relpath(p, ROOT)
            hit = False
            for c, (test, note) in CAT.items():
                if test(f):
                    rows[c].append((rel, sz, mt, note)); hit = True; break
            if sz == 0:
                rows["empty"].append((rel, 0, mt, "empty file - hold")); hit = True
            elif sz > 200 * 1048576 and not hit:
                rows["large"].append((rel, sz, mt, "large - keep unless known junk"))
            if d == top and not hit and f not in ("README.md", "BACKLOG.md"):
                rows["loose"].append((rel, sz, mt, "loose in the top folder - file it (library-intake)"))
            if sz > 0:
                sizes[sz].append(p)
    groups = [ps for ps in sizes.values() if len(ps) > 1]
    dup = collections.defaultdict(list)         # (copy folder, kept folder) -> [(copy, kept)]
    for ps in groups:
        by = collections.defaultdict(list)
        for p in ps:
            by[sha(p)].append(p)
        for same in by.values():
            if len(same) > 1:
                keep = min(same, key=lambda p: (os.path.getmtime(p), len(p)))
                for p in same:
                    if p != keep:
                        dup[(os.path.dirname(p), os.path.dirname(keep))].append((p, keep))
    side = {}
    for (cd, kd), pairs in sorted(dup.items(), key=lambda kv: -len(kv[1])):
        sz = sum(os.path.getsize(p) for p, _ in pairs)
        if len(pairs) >= 5:                         # a whole folder of copies: one line, file list in the sidecar
            gid = f"dupgroup-{len(side) + 1}"
            side[gid] = [os.path.relpath(p, ROOT) for p, _ in pairs]
            rows["duplicate"].append((gid, sz, max(os.path.getmtime(p) for p, _ in pairs),
                                      f"{len(pairs)} files in `{os.path.relpath(cd, ROOT)}/` same as `{os.path.relpath(kd, ROOT)}/`"
                                      " - game installs and mod builds often copy on purpose"))
        else:
            for p, k in pairs:
                rows["duplicate"].append((os.path.relpath(p, ROOT), os.path.getsize(p), os.path.getmtime(p),
                                          f"same content as {os.path.relpath(k, ROOT)} - hold"))
    os.makedirs(OUT, exist_ok=True)
    dst = os.path.join(OUT, f"{datetime.date.today()}-{name}.md")
    json.dump(side, open(dst[:-3] + ".groups.json", "w"), indent=0)
    order = ["duplicate", "copy-named", "installer", "archive", "temp", "cache", "empty", "large", "loose"]
    out = [f"# Cleanup catalogue - {os.path.relpath(top, os.path.dirname(ROOT))}", "",
           f"Status: draft ({datetime.date.today()})", "",
           "Tick `[x]` what may go to the holding folder, then `cleanup.py apply` on this file. Held items move to",
           "`Archive/cleanup/held-<date>/` (same paths, manifest, `cleanup.py undo`). Nothing is deleted by Claude.", "",
           "| Category | Items | Size |", "|---|---|---|"]
    for c in order:
        if rows[c]:
            out.append(f"| {c} | {len(rows[c])} | {human(sum(r[1] for r in rows[c]))} |")
    for c in order:
        if not rows[c]:
            continue
        out += ["", f"## {c}", ""]
        for rel, sz, mt, note in sorted(rows[c], key=lambda r: -r[1]):
            out.append(f"- [ ] `{rel}` ({human(sz)}, {datetime.date.fromtimestamp(mt)}) - {note}")
    open(dst, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("\n".join(out[7:9 + len([c for c in order if rows[c]])]))
    print(os.path.relpath(dst, ROOT))


def apply(cat):
    held = os.path.join(OUT, f"held-{datetime.datetime.now():%Y-%m-%d-%H%M}")
    moved = []
    side = json.load(open(cat[:-3] + ".groups.json")) if os.path.exists(cat[:-3] + ".groups.json") else {}
    items = []
    for l in open(cat, encoding="utf-8"):
        m = re.match(r"- \[[xX]\] `([^`]+)`", l)
        if m:
            items += side.get(m.group(1), [m.group(1)])
    for rel in items:
        m = re.match(r"(.*)", rel)
        src = os.path.join(ROOT, m.group(1).rstrip("/"))
        if not os.path.exists(src):
            print("gone:", m.group(1)); continue
        dst = os.path.join(held, m.group(1).rstrip("/"))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(src, dst)
        moved.append([src, dst])
    if moved:
        json.dump(moved, open(os.path.join(held, "MANIFEST.json"), "w"), indent=1)
    print(f"held {len(moved)} items in {os.path.relpath(held, ROOT) if moved else '-'}")


def undo(held):
    man = json.load(open(os.path.join(held, "MANIFEST.json")))
    for src, dst in man:
        if os.path.exists(dst) and not os.path.exists(src):
            os.makedirs(os.path.dirname(src), exist_ok=True)
            shutil.move(dst, src)
    print(f"restored {len(man)} items")


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    if a[0] == "scan":
        top = a[1] if len(a) > 1 else ROOT
        name = a[a.index("--out") + 1] if "--out" in a else (re.sub(r"[^a-z0-9]+", "-", os.path.basename(os.path.abspath(top)).lower()).strip("-") or "root")
        scan(top, name)
    elif a[0] == "apply":
        apply(a[1])
    elif a[0] == "undo":
        undo(a[1])


if __name__ == "__main__":
    main()
