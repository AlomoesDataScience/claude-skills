#!/usr/bin/env python3
"""Terrain map of the visible battlefield as text: hover every square, read the tooltip.

  terrscan.py [--x0 X] [--x1 X] [--y0 Y] [--y1 Y]

Assumes the camera was just centred by Next Unmoved / Tab (a unit at 800,465 = a square centre;
squares 59 px at max zoom-out, top view). Hovers square centres 800+59i, 465+59j inside the box
(default x 270..1480, y 290..880 - clear of the UI) and prints one letter per square:
  .  open ground      r rough ground     m marsh      W woods      d other difficult
  b  built-up area    t tracks/fields    #  obstacle (fence, hedge) on the square
  U  a unit stands there (terrain under it not shown)          ?  unreadable
  lower-case h after nothing - hills are flagged by a + in the second map
Prints the letter map, then the same map with + where the tooltip said (Hill), and the column x
and row y pixel centres so squares can be ordered by coordinates. Hover only - nothing is clicked.
"""
import os
import re
import subprocess
import sys

BG = os.path.expanduser("~/Desktop/AI Development/.claude/skills/game-ui/scripts/bgplay.py")
CX, CY, SQ = 800, 465, 59


def opt(a, k, d):
    return int(a[a.index(k) + 1]) if k in a else d


def tip(x, y):
    out = subprocess.run([sys.executable, "-I", BG, "seq", f"move {x} {y}", "wait 700",
                          f"read {x - 10} {y - 10} {min(1590, x + 560)} {y + 130}"],
                         capture_output=True, text=True).stdout
    return " ".join(ln for ln in out.splitlines() if ln.strip() and not ln.startswith("[")
                    and not ln.endswith(".png"))


def letter(t):
    if re.search(r"\(\d+\)", t):
        return "U"
    for k, c in (("Obstacle", "#"), ("Marsh", "m"), ("Wood", "W"), ("Rough", "r"), ("Built", "b"),
                 ("Difficult", "d"), ("Track", "t"), ("Field", "t"), ("Open", ".")):
        if k.lower() in t.lower():
            return c
    return "?"


def main(a):
    x0, x1, y0, y1 = opt(a, "--x0", 270), opt(a, "--x1", 1480), opt(a, "--y0", 290), opt(a, "--y1", 880)
    xs = [CX + i * SQ for i in range(-20, 21) if x0 <= CX + i * SQ <= x1]
    ys = [CY + j * SQ for j in range(-10, 11) if y0 <= CY + j * SQ <= y1]
    rows, hills = [], []
    for y in ys:
        r, h = "", ""
        for x in xs:
            t = tip(x, y)
            r += letter(t)
            h += "+" if "hill" in t.lower() else " "
        rows.append(r)
        hills.append(h)
        print(f"{y:4d} {r}", flush=True)
    print("hills:")
    for y, h in zip(ys, hills):
        print(f"{y:4d} {h}")
    print("columns x:", " ".join(str(x) for x in xs))
    subprocess.run([sys.executable, "-I", BG, "seq", "move 300 880"], capture_output=True)


if __name__ == "__main__":
    main(sys.argv[1:])
