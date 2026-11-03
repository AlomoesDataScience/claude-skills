#!/usr/bin/env python3
"""Look a term up in a game's manuals: hits with page and chapter heading, pages to read as pictures.
  lookup.py TERM [TERM2 ...] [--game DIR] [-C N]      lookup.py --list [--game DIR]
Text versions are made next to the PDF by game-sources manual.py (once). Read-only otherwise."""
import os
import re
import subprocess
import sys

MANUAL = os.path.expanduser("~/Desktop/AI Development/.claude/skills/game-sources/scripts/manual.py")
HEAD = re.compile(r"^\s*(\d{1,2}(?:\.\d+)*\.?)\s+([A-Z][\w ,/&'()-]{2,60})\s*$")


def game_dir(a):
    if "--game" in a:
        return a[a.index("--game") + 1]
    d = os.getcwd()
    while d != "/":
        if os.path.isdir(os.path.join(d, "Manuals")):
            return d
        d = os.path.dirname(d)
    sys.exit("no game folder with a Manuals/ folder above here - pass --game DIR")


def pdfs(g):
    out = []
    for r, _, fs in os.walk(g):
        if "/install" in r or "/." in r:
            continue
        out += [os.path.join(r, f) for f in fs if f.lower().endswith(".pdf")]
    return sorted(out)


def text_of(pdf):
    t = pdf[:-4] + ".txt"
    if not os.path.exists(t):
        subprocess.run([sys.executable, "-I", MANUAL, "text", pdf, t], capture_output=True)
    return t if os.path.exists(t) else None


def pages(txt):
    cur, buf, out = 0, [], []
    for line in open(txt, errors="replace"):
        m = re.match(r"=== page (\d+)", line)
        if m:
            out.append((cur, buf)); cur, buf = int(m.group(1)), []
        else:
            buf.append(line.rstrip("\n"))
    out.append((cur, buf))
    return out


def main(a):
    g = game_dir(a)
    fs = pdfs(g)
    if "--list" in a:
        for f in fs:
            print(("text " if text_of(f) else "NO TEXT ") + os.path.relpath(f, g))
        return
    C = int(a[a.index("-C") + 1]) if "-C" in a else 1
    skip = {"--game", "-C"}
    terms = [x for i, x in enumerate(a) if x not in skip and (i == 0 or a[i - 1] not in skip)]
    if not terms:
        sys.exit(__doc__)
    rx = re.compile("|".join(re.escape(t) for t in terms), re.I)
    picture = [f for f in fs if re.search(r"ebook|colou?r", f, re.I)]
    hitpages = set()
    for f in fs:
        t = text_of(f)
        if not t:
            print(f"[{os.path.basename(f)}] no text layer - read its pages as images"); continue
        head = ""
        for n, lines in pages(t):
            for i, l in enumerate(lines):
                h = HEAD.match(l)
                if h:
                    head = (h.group(1) + " " + h.group(2)).strip()
                if rx.search(l):
                    ctx = " | ".join(x.strip() for x in lines[max(0, i - C):i + C + 1] if x.strip())
                    print(f"[{os.path.basename(f)[:28]}] p.{n}  §{head[:40]}  {ctx[:220]}")
                    if f in picture:
                        hitpages.add(n)
    if hitpages:
        print("\nread as pictures (" + os.path.basename(picture[0]) + "): pages " +
              ", ".join(str(p) for p in sorted(hitpages)))


if __name__ == "__main__":
    main(sys.argv[1:])
