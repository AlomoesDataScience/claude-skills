#!/usr/bin/env python3
"""FoG II Medieval board snapshot as text: terrain of every visible square and who stands where.
The user (2026-11-02): "this game is a geometry game ... build tools", "identify who is where".

  board.py [--x0 X] [--x1 X] [--y0 Y] [--y1 Y] [--json FILE]

The camera must be centred on a unit first (Next Unmoved, Tab, or clicking a Unit List entry
puts that unit at 800,465 = a square centre; squares are 59 px at max zoom-out, top view, nothing
selected). Hovers each square centre in the box (default the whole map view clear of the UI) and,
in one bgplay call per square, reads the tooltip both below-right and above-left of the pointer
(it flips near edges) and takes a shot: a hovered unit's card appears in the right card slot, and
its banner colour gives the side (blue = ours, green = Irish).
Prints
  - the terrain map: . open  r rough  m marsh  W woods  d difficult  b built-up  t tracks/fields
    # obstacle  ~ off map/unreadable;   units drawn as A (ours) / E (enemy) / U (side unknown)
  - a units list: side, name, grid (col,row) relative to the centre square (+col = east/right,
    +row = south/down), and its screen x,y
Coordinates are valid until the camera moves - re-centre and re-run (or keep the JSON).
"""
import json
import os
import re
import subprocess
import sys

from PIL import Image

BG = os.path.expanduser("~/Desktop/AI Development/.claude/skills/game-ui/scripts/bgplay.py")
CX, CY, SQ = 800, 465, 59
TER = (("Obstacle", "#"), ("Marsh", "m"), ("Wood", "W"), ("Rough", "r"), ("Built", "b"),
       ("Difficult", "d"), ("Track", "t"), ("Field", "t"), ("Open", "."))


def opt(a, k, d):
    return int(a[a.index(k) + 1]) if k in a else d


def probe(x, y):
    out = subprocess.run([sys.executable, "-I", BG, "seq", f"move {x} {y}", "wait 900",
                          f"read 0 {y + 12} 1590 {min(990, y + 150)}",       # tooltips are wide and
                          f"read 0 {max(0, y - 170)} 1590 {y - 8}", "shot --full"],   # placed left or above
                         capture_output=True, text=True).stdout
    shots = [ln for ln in out.splitlines() if ln.endswith(".png")]
    txt = " ".join(ln for ln in out.splitlines() if ln.strip() and not ln.startswith("[")
                   and not ln.endswith(".png"))
    return txt, (shots[-1] if shots else None)


def side(shot):
    """Banner on the right card slot (hovered unit): sample the flag cloth."""
    if not shot:
        return "?"
    im = Image.open(shot).convert("RGB").crop((822, 752, 848, 800))
    px = list(im.getdata())
    r, g, b = (sum(p[i] for p in px) / len(px) for i in range(3))
    if b > r + 25 and b > g:
        return "A"
    if g > r + 15 and g > b:
        return "E"
    return "U"


def main(a):
    x0, x1, y0, y1 = opt(a, "--x0", 240), opt(a, "--x1", 1480), opt(a, "--y0", 290), opt(a, "--y1", 880)
    xs = [CX + i * SQ for i in range(-20, 21) if x0 <= CX + i * SQ <= x1]
    ys = [CY + j * SQ for j in range(-10, 11) if y0 <= CY + j * SQ <= y1]
    units, cells = [], {}
    print("      " + "".join(f"{(x - CX) // SQ:+d}"[-1] for x in xs) + "   (col last digit)")
    for y in ys:
        row = ""
        for x in xs:
            t, shot = probe(x, y)
            ter = next((c for k, c in TER if k.lower() in t.lower()), "~")
            m = re.search(r"([A-Z][A-Za-z&'() ]*?)\s*\((\d{1,2})\)", t)
            ch = ter
            if m:
                s = side(shot)
                ch = s
                units.append({"side": {"A": "ours", "E": "enemy"}.get(s, "?"), "name": f"{m.group(1).strip()} ({m.group(2)})",
                              "col": (x - CX) // SQ, "row": (y - CY) // SQ, "x": x, "y": y, "terrain": ter,
                              "hill": "hill" in t.lower()})
            cells[f"{(x - CX) // SQ},{(y - CY) // SQ}"] = {"t": ter, "hill": "hill" in t.lower()}
            row += ch
        print(f"{(y - CY) // SQ:+3d} {y:4d} {row}", flush=True)
    print("units (col,row from centre; +col east, +row south):")
    for u in sorted(units, key=lambda u: (u["side"], u["row"], u["col"])):
        print(f"  {u['side']:5s} {u['name']:32s} ({u['col']:+d},{u['row']:+d})  at {u['x']},{u['y']}"
              f"  on {u['terrain']}{' hill' if u['hill'] else ''}")
    if "--json" in a:
        json.dump({"units": units, "cells": cells}, open(a[a.index("--json") + 1], "w"), indent=1)
    subprocess.run([sys.executable, "-I", BG, "seq", "move 300 880"], capture_output=True)


if __name__ == "__main__":
    main(sys.argv[1:])
