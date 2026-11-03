#!/usr/bin/env python3
"""FoG II Medieval: one screenshot with the square grid drawn on it, labelled col,row from the centre
square, so Claude reads terrain and units off the picture and plans by geometry. No hovering.
(the user: identify forest, farms, open, hills from the photo - like the Dominions maps; no tooltips.)

  gridshot.py [--every 2] [--at X Y]
      --at   a known square centre becomes (0,0)
      (anchor by eye: a unit column's centre for x, a unit or the stone map edge - a square
       boundary - for y; panning with W/S keeps x, A/D keeps y)

Camera must be centred on a unit (Tab / Next Unmoved / Unit List put it at 800,465; squares 59 px,
top view, max zoom-out; then Space to deselect). +col = east (right), +row = south (down).
Screen point of square (c,r) = (X + 59c, Y + 59r), X,Y = 800,465 or --at. Prints the image path.
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw

BG = os.path.expanduser("~/Desktop/AI Development/.claude/skills/game-ui/scripts/bgplay.py")
CX, CY, SQ = 800, 465, 59
if "--at" in sys.argv:          # a square centre seen in the picture (a unit column, half a square in
    i = sys.argv.index("--at")  # from the stone map edge) when the camera isn't centred on a unit
    CX, CY = int(sys.argv[i + 1]), int(sys.argv[i + 2])

def seq(*steps):
    return subprocess.run([sys.executable, "-I", BG, "seq", *steps], capture_output=True, text=True).stdout


every = int(sys.argv[sys.argv.index("--every") + 1]) if "--every" in sys.argv else 2
out = seq("move 1550 880", "wait 500", "shot --full")
img = Image.open([l for l in out.splitlines() if l.endswith(".png")][-1]).convert("RGB")
dr = ImageDraw.Draw(img)
for c in range(-14, 15):
    x = CX + c * SQ - SQ // 2
    dr.line((x, 30, x, 900), fill=(255, 255, 255) if c != 0 else (255, 255, 0))
for r in range(-8, 9):
    y = CY + r * SQ - SQ // 2
    dr.line((0, y, 1500, y), fill=(255, 255, 255))
for c in range(-14, 15):
    for r in range(-8, 9):
        if c % every == 0 and r % every == 0:
            x, y = CX + c * SQ - 27, CY + r * SQ - 28
            dr.rectangle((x, y, x + 30, y + 10), fill=(0, 0, 0))
            dr.text((x + 1, y - 1), f"{c},{r}", fill=(255, 255, 0))
p = os.path.join(os.path.dirname([l for l in out.splitlines() if l.endswith(".png")][-1]), "gridshot.png")
img.crop((0, 30, 1500, 900)).save(p)
print(p)
