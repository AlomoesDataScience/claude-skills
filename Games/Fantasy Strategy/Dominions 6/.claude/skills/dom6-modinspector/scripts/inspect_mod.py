"""Load Dominions 6 mods into the Mod Inspector and write out the modded game, the way the site's
"load mods" button does.

  python3 -I inspect_mod.py MOD.dm [MOD2.dm ...] [--out DIR] [--update]

Mods load in the order given. Writes into DIR (default: <tmp>/dom6-modinspect/<first mod name>):
  report.txt     loaded mods, the inspector parser's errors and warnings (file:line), and a list of
                 every new and changed unit, spell, item, weapon, armour, site, merc, event, nation
  mod_pages.txt  the full inspector page of every object the mods add or change; changed objects
                 also list their fields that differ from vanilla, and every page ends with the mod
                 lines that touched it
  pages/, records/, mods.json, VERSION
                 the whole modded game in the dom6-inspector layout, so dom6-inspector's
                 inspector.py can query it: inspector.py --data DIR unit "name"
Uses the dom6-inspector skill's build.py (git + headless firefox). --update pulls the latest site.
"""
import importlib.util
import json
import os
import re
import shutil
import sys
import tempfile
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
INSPECTOR = os.path.normpath(os.path.join(HERE, "..", "..", "dom6-inspector"))
spec = importlib.util.spec_from_file_location("dom6_inspector_build", os.path.join(INSPECTOR, "scripts", "build.py"))
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)

KINDS = build.KINDS
# fields the site derives or adds while preparing data: not interesting in a vanilla comparison
NOISE = {"modded", "searchable", "linkname", "sorttype", "sortschool", "rcostsort", "sacredsort", "titles",
         "_ressizeExplicitlySet", "used_by", "eracodes", "listed_mpath", "fatiguecostsort", "gemcostsort",
         "effect_record_id", "renderOverlay", "sprite", "nations", "summonedby", "recruitedby"}


def read_mod(path):
    raw = open(path, "rb").read()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1")                    # older mods (e.g. Dominions Enhanced)


def name_of(d):
    return d.get("fullname") or d.get("name") or d.get("nationname") or ""


def short(v):
    t = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)
    return t if len(t) <= 80 else t[:77] + "..."


def diff(old, new):
    out = []
    for k in sorted(set(old) | set(new)):
        if k in NOISE:
            continue
        a, b = old.get(k), new.get(k)
        if json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True):
            out.append(f"  {k}: {short(a) if a is not None else '-'} -> {short(b) if b is not None else '-'}")
    return out


def modded_lines(d):
    """The mod lines the site attached to the object ("1:12  #hp 15" ...), as plain text."""
    m = d.get("modded")
    if not m or m == 1 or m == "1":
        return []
    t = re.sub(r"<br\s*/?>", "\n", str(m)).replace("&nbsp;", " ")
    return [l.strip() for l in t.split("\n") if l.strip()]


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return
    out = a[a.index("--out") + 1] if "--out" in a else None
    mods = [x for i, x in enumerate(a) if x.endswith(".dm") and (i == 0 or a[i - 1] != "--out")]
    if not mods:
        sys.exit("give one or more .dm files")
    for m in mods:
        if not os.path.exists(m):
            sys.exit(f"no such file: {m}")
    base = os.path.splitext(os.path.basename(mods[0]))[0]
    out = os.path.abspath(out or os.path.join(tempfile.gettempdir(), "dom6-modinspect", base))

    repo = build.ensure_repo(build.WORK, update="--update" in a)
    moddir = os.path.join(repo, "mods")
    os.makedirs(moddir, exist_ok=True)
    for fn in os.listdir(moddir):                     # earlier copies of ours
        if fn.endswith(".dm"):
            os.remove(os.path.join(moddir, fn))
    names = []
    for i, m in enumerate(mods):
        fn = re.sub(r"[^\w.-]", "_", os.path.basename(m))
        if fn in names:
            fn = f"{i}_{fn}"
        open(os.path.join(moddir, fn), "w", encoding="utf-8").write(read_mod(m))
        names.append(fn)

    dumpdir = os.path.join(out, "dump")
    shutil.rmtree(dumpdir, ignore_errors=True)
    os.makedirs(dumpdir)
    print("rendering the modded game headless...")
    build.dump(repo, dumpdir, "loadEvents=1&" + "&".join("mod=" + quote(n) for n in names))
    note = "mods: " + ", ".join(os.path.abspath(m) for m in mods) + "\n"
    build.write_data(repo, dumpdir, images=False, data=out, note=note, raw=False)
    json.dump({"mods": [os.path.abspath(m) for m in mods],
               "folders": [os.path.dirname(os.path.abspath(m)) for m in mods]}, open(os.path.join(out, "mods.json"), "w"), indent=1)

    # compare with the vanilla copy
    msgs = json.load(open(os.path.join(dumpdir, "messages.json")))
    vanilla_dir = os.path.join(INSPECTOR, "data", "records")
    report, pages_out, counts = [], [], {}
    pages = {kind: {} for kind in KINDS}
    for kind in KINDS:
        for block in open(os.path.join(out, "pages", kind + ".txt"), encoding="utf-8").read().split("\n\n"):
            mm = re.match(r"=== \S+ (-?[\d.]+):", block.strip("\n"))
            if mm:
                pages[kind][mm.group(1)] = block.strip("\n")
    for kind in KINDS:
        vanilla = {}
        vp = os.path.join(vanilla_dir, kind + ".jsonl")
        if os.path.exists(vp):
            for line in open(vp, encoding="utf-8"):
                d = json.loads(line)
                vanilla[str(d.get("id"))] = d
        new, changed = [], []
        for line in open(os.path.join(out, "records", kind + ".jsonl"), encoding="utf-8"):
            d = json.loads(line)
            old = vanilla.get(str(d.get("id")))
            if kind in ("events", "mercs"):             # the site does not tag these as modded: compare
                if old is None:
                    new.append(d)
                elif diff(old, d):
                    changed.append(d)
                continue
            if not d.get("modded"):
                continue
            (changed if old is not None else new).append(d)
        counts[kind] = (len(new), len(changed))
        one = kind[:-1] if kind.endswith("s") else kind
        for tag, lst in (("new", new), ("changed", changed)):
            for d in lst:
                variant = "   (the site's second listing of this unit)" if re.search(r"\.\d+$", str(d.get("id"))) else ""
                report.append(f"{tag:8} {one} {d.get('id')}: {name_of(d)}{variant}")
                page = pages[kind].get(str(d.get("id")), f"=== {one} {d.get('id')}: {name_of(d)}")
                extra = []
                if tag == "changed":
                    ch = diff(vanilla[str(d.get("id"))], d)
                    extra = ["changed from vanilla:"] + (ch or ["  (no field differences the site records)"])
                lines = [] if "[modded]" in page else modded_lines(d)     # the page usually shows them already
                pages_out.append(f"{page}\n[{tag}]" + ("\n" + "\n".join(extra) if extra else "")
                                 + ("\nmod lines:\n" + "\n".join("  " + l for l in lines) if lines else ""))

    with open(os.path.join(out, "report.txt"), "w", encoding="utf-8") as f:
        f.write(f"mods loaded (in order): {', '.join(msgs.get('loadedmods') or names)}\n")
        f.write("files: " + ", ".join(os.path.abspath(m) for m in mods) + "\n\n")
        f.write("summary (new / changed):\n")
        for kind, (n, c) in counts.items():
            if n or c:
                f.write(f"  {kind:8} {n:5} new {c:5} changed\n")
        m = msgs.get("messages") or []
        f.write(f"\ninspector parser messages: {len(m)}\n")
        f.write("".join("  " + " ".join(x.split()) + "\n" for x in m))
        f.write("\nobjects:\n" + "".join("  " + r + "\n" for r in report))
    open(os.path.join(out, "mod_pages.txt"), "w", encoding="utf-8").write("\n\n".join(pages_out) + "\n")
    shutil.rmtree(dumpdir, ignore_errors=True)
    print(open(os.path.join(out, "report.txt"), encoding="utf-8").read().split("\nobjects:")[0])
    print(f"wrote {out}/report.txt, mod_pages.txt, pages/, records/")


if __name__ == "__main__":
    main()
