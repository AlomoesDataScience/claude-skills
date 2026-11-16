"""Read a saved robots.txt locally: what it says to bots, and whether our own User-Agents trip it. No requests.

Usage: python3 -I sitecheck.py ROBOTS_FILE [URL ...]
  ROBOTS_FILE  a robots.txt saved as text (site-rules/robots/<host>-<date>.txt; fetch it once with textpull.py check
               or curl, then read it here as often as needed)
  URL          paths we plan to request; each gets an allow/deny verdict for every one of our User-Agents
Prints: the comments addressed to bots, Crawl-delay values, Sitemap lines, the bots blocked outright, and
COLLISIONS: listed bot names that occur inside one of our UA names. Python's robotparser (and other matchers)
treat a listed name as a substring of our product token, so "docpull" counts as the blocked bot "DOC" and
"wikifetch" as "Fetch" (both found 2026-11-16 on en.wikipedia.org).
Our UAs: every "AI-Development-workspace-<name>" in the workspace-root .claude/skills/*/scripts (game-folder
skills are not scanned).
Fails when: a server matches agents differently from Python (exact match, regex): then a collision here may be
harmless there, and a pass here proves nothing for that server; rules in a policy page (rate, contact) are not
in robots.txt at all: read the site's bot policy too.
"""
import glob, os, re, sys, urllib.robotparser

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))


def our_uas():
    names = set()
    for f in glob.glob(os.path.join(ROOT, ".claude", "skills", "*", "scripts", "*.py")):
        try:
            names.update(re.findall(r"AI-Development-workspace-[\w-]+", open(f, encoding="utf-8", errors="replace").read()))
        except OSError:
            pass
    return sorted(names)


def main(a):
    if not a:
        sys.exit(__doc__)
    text = open(a[0], encoding="utf-8", errors="replace").read().lstrip("﻿")
    lines = text.splitlines()
    print(f"{a[0]}: {len(lines)} lines")
    keep = [l for l in lines if l.startswith("#") and re.search(r"please|fast|slow|rate|delay|block|welcome|bot|spider|crawl|exception|429|obey", l, re.I)]
    print("comments to bots:\n  " + "\n  ".join(keep[:30]) if keep else "comments to bots: none")
    agent = None
    for l in lines:
        m = re.match(r"(?i)\s*user-agent\s*:\s*(.+)", l)
        agent = m.group(1).strip() if m else agent
        if re.match(r"(?i)\s*(crawl-delay|request-rate)\s*:", l):
            print(f"  {l.strip()}   (for User-agent: {agent})")
        elif re.match(r"(?i)\s*sitemap\s*:", l):
            print("  " + l.strip())
    cur, blocked = [], []
    for l in lines + [""]:
        m = re.match(r"(?i)\s*user-agent\s*:\s*(.+)", l)
        if m:
            cur.append(m.group(1).strip())
        elif re.match(r"(?i)\s*disallow\s*:\s*/\s*$", l) and cur:
            blocked += [c for c in cur if c != "*"]
        elif not l.strip() or re.match(r"(?i)\s*(allow|disallow|crawl-delay)", l):
            if not l.strip():
                cur = []
    print(f"blocked outright ({len(blocked)}): {', '.join(blocked)}")
    listed = [x.lower().rstrip("*") for x in re.findall(r"(?im)^\s*user-agent\s*:\s*(.+)$", text) if x.strip() != "*"]
    uas = our_uas()
    print(f"our User-Agents ({len(uas)}): {', '.join(u[25:] for u in uas)}")
    bad = [(u, x) for u in uas for x in listed if x and x in u.lower()]
    print("COLLISIONS: " + ("; ".join(f"{u} matches '{x}'" for u, x in bad) if bad else "none"))
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(lines)
    for url in a[1:]:
        verdict = {u[25:]: rp.can_fetch(u + "/1.0", url) for u in uas}
        ok = [k for k, v in verdict.items() if v]
        print(f"{'ALLOW' if len(ok) == len(verdict) else 'DENY ' if not ok else 'MIXED'} {url}"
              + ("" if len(ok) in (0, len(verdict)) else f"  (denied: {', '.join(k for k, v in verdict.items() if not v)})"))


if __name__ == "__main__":
    main(sys.argv[1:])
