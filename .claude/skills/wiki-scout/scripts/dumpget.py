"""Get whole articles out of the local English Wikipedia dump by title, with no web requests.

Usage: python3 -I dumpget.py DUMP OUTDIR TITLE [TITLE ...]
       python3 -I dumpget.py DUMP --find REGEX [--limit 40]
  DUMP    the dump folder made by dumppass.py (Theory/Sources/Wikipedia/enwiki-dump)
  OUTDIR  where each article is written as "<Title>.wiki" (wikitext; read it, write our own words)
  --find  list catalogue titles matching REGEX (case-insensitive), with part, bytes and short description
Redirects are followed once (the catalogue's redirect column). Titles not found are reported, not guessed.
Each call scans the whole catalogue (about 1 minute), so pass several titles in one call.
Fails when: the title differs in spelling or dashes from the dump's (use --find first); the dump is a
2026-11-01 snapshot, so later edits are missing.
"""
import gzip, json, lzma, os, re, sys


def catalogue(dump):
    d = os.path.join(dump, "catalogue")
    for name in sorted(os.listdir(d)):
        part = name.split("-")[1].split(".")[0]
        with gzip.open(os.path.join(d, name), "rt", encoding="utf-8") as f:
            for line in f:
                c = line.rstrip("\n").split("\t")
                if len(c) > 5 and c[1] == "0":
                    yield part, c


def find(dump, rx, limit):
    r = re.compile(rx, re.I)
    n = 0
    for part, c in catalogue(dump):
        if r.search(c[2]):
            print(f"{part}\t{c[3]}\t{c[2]}\t{'-> ' + c[4] if c[4] else c[5]}")
            n += 1
            if n >= limit:
                break


def get(dump, out, titles):
    want = set(titles)
    where, redirect = {}, {}
    for part, c in catalogue(dump):
        if c[2] in want:
            if c[4]:
                redirect[c[2]] = c[4]
                want.add(c[4])
            else:
                where[c[2]] = part
        if all(t in where or t in redirect for t in want):
            break
    os.makedirs(out, exist_ok=True)
    byPart = {}
    for t, p in where.items():
        byPart.setdefault(p, set()).add(t)
    got = set()
    for p, ts in sorted(byPart.items()):
        for sub in ("text", "rest"):
            fn = os.path.join(dump, sub, f"part-{p}.jsonl.xz")
            if not os.path.exists(fn) or ts <= got:
                continue
            with lzma.open(fn, "rt", encoding="utf-8") as f:
                for line in f:
                    row = json.loads(line)
                    if row["title"] in ts:
                        safe = row["title"].replace("/", "_")
                        with open(os.path.join(out, safe + ".wiki"), "w", encoding="utf-8") as o:
                            o.write(row["wikitext"])
                        got.add(row["title"])
                        if ts <= got:
                            break
    for t in titles:
        tt = redirect.get(t, t)
        print(f"{'ok' if tt in got else 'MISSING'}\t{t}" + (f" -> {tt}" if tt != t else ""))


def main(a):
    if len(a) < 2:
        print(__doc__)
        return
    if a[1] == "--find":
        lim = int(a[a.index("--limit") + 1]) if "--limit" in a else 40
        find(a[0], a[2], lim)
    elif len(a) >= 3:
        get(a[0], a[1], a[2:])
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
