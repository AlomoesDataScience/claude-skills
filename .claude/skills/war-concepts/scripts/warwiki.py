#!/usr/bin/env python3
"""Look up war terms in the local copy of Wikipedia's "Index of war-related articles".

Data: Theory/Sources/Military Theory/wiki/war-index.json (1,146 articles: title, short description, first two
sentences, tier) and Theory/Sources/Military Theory/wiki/war/<title>.txt (full text of the tier-A articles).
Tiers (Claude's triage, 2026-11-02): A = concepts for playing/designing games (full text local),
B = specific weapons, platforms, troop types, branches, wars (fetch on demand), C = not useful
for games (ranks, law cases, atrocities, culture, wrong-target links).

  warwiki.py look TERM...      matching articles (title first, then description/intro), with tier,
                               description, intro and the local full-text file if any
  warwiki.py grep WORD [-n N]  search the full texts; prints title and the matching lines
  warwiki.py tier A|B|C        list one tier
  warwiki.py fetch TITLE       download one article's full text into war/ (e.g. a B article)
  warwiki.py stats
"""
import json, os, re, subprocess, sys, time, urllib.parse

ROOT = os.path.expanduser("~/Desktop/AI Development/Theory/Sources/Military Theory/wiki")
IDX, FULL = os.path.join(ROOT, "war-index.json"), os.path.join(ROOT, "war")


def rows():
    return json.load(open(IDX))


def path(t):
    p = os.path.join(FULL, t.replace("/", "_") + ".txt")
    return p if os.path.exists(p) else None


def look(terms):
    q = " ".join(terms).lower()
    rs = rows()
    hits = [r for r in rs if q in r["title"].lower()] + \
           [r for r in rs if q not in r["title"].lower() and (q in r["desc"].lower() or q in r["intro"].lower())]
    for r in hits[:15]:
        print(f"[{r['tier']}] {r['title']} - {r['desc']}\n    {r['intro'][:400]}")
        if path(r["title"]):
            print("    full text:", path(r["title"]))
    if not hits:
        print("no match; try fewer words, or: warwiki.py fetch 'Title'")


def grep(word, n=3):
    pat = re.compile(re.escape(word), re.I)
    for f in sorted(os.listdir(FULL)):
        lines = [l.strip() for l in open(os.path.join(FULL, f)) if pat.search(l)]
        if lines:
            print(f"== {f[:-4]} ({len(lines)})")
            for l in lines[:n]:
                print("   ", l[:300])


_ROBOTS = {}
def robots_ok(url, ua):
    """robots.txt verdict for url (site-rules skill). 200: obey it; 404: none, allowed; anything else: refuse."""
    import urllib.parse, urllib.robotparser
    root = "{0.scheme}://{0.netloc}".format(urllib.parse.urlsplit(url))
    if root not in _ROBOTS:
        r = subprocess.run(["curl", "-sSL", "--compressed", "-A", ua, "--max-time", "30", "-w", "\n%{http_code}",
                            root + "/robots.txt"], capture_output=True, text=True)
        body, _, code = r.stdout.rpartition("\n")
        rp = urllib.robotparser.RobotFileParser()
        if code == "200":
            rp.parse(body.splitlines())
        elif code == "404":
            rp.allow_all = True
        else:
            rp.disallow_all = True
        _ROBOTS[root] = rp
    return _ROBOTS[root].can_fetch(ua, url)


def fetch(title):
    url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "query", "prop": "extracts", "explaintext": "1", "titles": title, "redirects": "1", "format": "json"})
    if not robots_ok(url, "AI-Development-workspace-wikitext/1.0"):
        sys.exit("STOP: robots.txt disallows en.wikipedia.org/w/api.php for bots (site-rules skill). Ask the user.")
    r = subprocess.run(["curl", "-sSL", "--compressed", "-A", "AI-Development-workspace-wikitext/1.0 (personal offline reading; low rate)",
                        "--max-time", "60", url], capture_output=True, text=True)
    pages = json.loads(r.stdout).get("query", {}).get("pages", {})
    p = next(iter(pages.values()), {})
    if not p.get("extract"):
        sys.exit("no such article")
    os.makedirs(FULL, exist_ok=True)
    fn = os.path.join(FULL, p["title"].replace("/", "_") + ".txt")
    open(fn, "w").write(f"# {p['title']}\nSource: https://en.wikipedia.org/wiki/{urllib.parse.quote(p['title'].replace(' ', '_'))} "
                        f"(CC BY-SA 4.0; local reading copy)\n\n{p['extract']}\n")
    print(fn)


def main(a):
    if not a:
        sys.exit(__doc__)
    c = a[0]
    if c == "look":
        look(a[1:])
    elif c == "grep":
        grep(a[1], int(a[a.index("-n") + 1]) if "-n" in a else 3)
    elif c == "tier":
        for r in rows():
            if r["tier"] == a[1].upper():
                print(f"{r['title']} - {r['desc']}")
    elif c == "fetch":
        fetch(" ".join(a[1:]))
    elif c == "stats":
        from collections import Counter
        print(Counter(r["tier"] for r in rows()), "| full texts:", len(os.listdir(FULL)))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
