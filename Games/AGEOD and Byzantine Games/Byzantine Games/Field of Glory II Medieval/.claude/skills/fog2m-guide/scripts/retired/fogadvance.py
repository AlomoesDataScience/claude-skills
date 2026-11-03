#!/usr/bin/env python3
"""Advance the whole army east by N squares in one turn, in a safe order, with text output only.

  fogadvance.py [--squares 2] [--dx 1|-1] [--skip NAME,NAME]

Uses the right-panel Next Unmoved button (it selects the next unit that hasn't moved and centres
the camera on it at about 800,465). Order, so nobody blocks anybody (the user: move the screen first):
  pass 1  light troops and cavalry (Javelinmen, Archers, Knights, Sergeants, Cavalry)
  pass 2  the first foot unit met gets Move Whole Command (moves its whole command in parallel)
  pass 3  anything still unmoved, one by one
Target = N squares along x (59 px per square at max zoom-out); if that square is occupied or the
order isn't allowed, it tries one square less. Units named in --skip are left alone. A unit is
"done" for this run once tried. Prints one line per unit. Uses the order menu (▲ Move Unit / blue
▲▲▲ Move Whole Command) when the game opens it.
"""
import os
import re
import subprocess
import sys

from PIL import Image

BG = os.path.expanduser("~/Desktop/AI Development/.claude/skills/game-ui/scripts/bgplay.py")
CX, CY, SQ = 800, 465, 59
LIGHT = ("Javelin", "Archers", "Knights", "Sergeants", "Cavalry")


def seq(*steps):
    return subprocess.run([sys.executable, "-I", BG, "seq", *steps], capture_output=True, text=True).stdout


def text(out):
    return " ".join(ln.strip() for ln in out.splitlines()
                    if ln.strip() and not ln.startswith("[") and not ln.endswith(".png"))


def shot_rgb(out):
    p = [ln for ln in out.splitlines() if ln.endswith(".png")]
    return Image.open(p[-1]).convert("RGB") if p else None


def blue(img, x, y):
    px = list(img.crop((x - 20, y - 20, x + 20, y + 20)).getdata())
    r, g, b = (sum(p[i] for p in px) / len(px) for i in range(3))
    return b > 90 and b > r + 35 and b > g + 12


TYPES = ("Knights & Sergeants", "Sergeants", "Irish Foot", "Irish Kerns", "Javelinmen", "Archers",
         "Spearmen", "Longbowmen", "Ostmen", "Cavalry")
DIGIT = str.maketrans("cCoOiIlt", "00001111")


def next_unmoved():
    """(key, label) of the unit Next Unmoved selected: key = its number (unique), label = type + number."""
    for _ in range(2):
        out = text(seq("key space", "wait 400", "click 1567 268", "wait 1800", "move 300 880", "wait 400",
                       "read 440 755 790 790"))
        m = re.search(r"\(([0-9cCoOiIlt]{1,2})\)", out)
        if m:
            num = m.group(1).translate(DIGIT)
            kind = next((t for t in TYPES if t.split()[-1] in out), "?")
            return num, f"{kind} ({num})"
        print(f"  (unreadable card: {out[:60]!r})", flush=True)
    return "", ""


def order(squares, dx, whole):
    for n in range(squares, 0, -1):
        tx = CX + dx * n * SQ
        tip = text(seq(f"move {tx} {CY}", "wait 1000", f"read {tx - 10} {CY - 10} {tx + 520} {CY + 100}"))
        if re.search(r"\(\d+\)", tip):
            continue                                       # a unit stands there
        img = shot_rgb(seq(f"click {tx} {CY} --right", "wait 1400", "shot --full"))
        if img is not None and blue(img, tx, CY + 60):
            seq(f"click {tx} {CY + 60 if whole else CY}", "wait 2200")
            return f"{n} sq ({'whole command' if whole else 'menu'})"
        moved = text(seq("move 300 880", "wait 300", "read 440 755 790 860"))
        m = re.search(r"AP:?\s*(\d+)/(\d+)", moved)
        if m and m.group(1) != m.group(2):
            return f"{n} sq (AP {m.group(1)}/{m.group(2)})"
        if not m:
            return f"{n} sq (ordered)"
    return "could not move"


def main(a):
    squares = int(a[a.index("--squares") + 1]) if "--squares" in a else 2
    dx = int(a[a.index("--dx") + 1]) if "--dx" in a else 1
    skip = [s.strip() for s in a[a.index("--skip") + 1].split(",")] if "--skip" in a else []
    tried, whole_done = set(), False
    for pas in (1, 2, 3):
        first = None
        for _ in range(40):
            key, name = next_unmoved()
            if not key:
                break
            if key == first:
                break                                      # went all the way round
            first = first or key
            if key in tried or any(s and s in name for s in skip):
                continue
            light = any(k in name for k in LIGHT)
            if pas == 1 and not light:
                continue
            if pas == 2 and (light or whole_done):
                continue
            res = order(squares, dx, whole=(pas == 2))
            tried.add(key)
            if pas == 2:
                whole_done = True
            print(f"pass {pas}: {name}: {res}", flush=True)
            first = None
        if pas == 2 and not whole_done:
            print("pass 2: no foot unit found")
    seq("key space", "wait 300")


if __name__ == "__main__":
    main(sys.argv[1:])
