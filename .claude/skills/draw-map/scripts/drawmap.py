#!/usr/bin/env python3
"""Draw a game map as Claude reads it: a text board -> a picture with grid, terrain colours, units
with facing, and movement arrows. A thinking aid, not a copy of the game's map.

  drawmap.py BOARD.txt [OUT.png] [--cell 28] [--origin COL ROW]   (axis labels start at COL, ROW: real map
                                                    coordinates for a cropped board)

BOARD.txt sections (lines starting with # are comments):
  grid:            one line per row, one character per column (row 0 = top/north)
  units:           ID SIDE COL ROW FACING [label...]   SIDE = a colour name or #hex; FACING = N NE E SE S SW W NW or -
  moves:           ID COL ROW -> COL ROW [c=COLOUR] [label...]   (from -> to; drawn as an arrow)
  marks:           COL ROW text...                     (a note on a square)
  colour:          CHAR #hex name                      (add or change a terrain colour)
Default terrain characters: . open  W woods  H hill  R rough  F fields  T track/road  B buildings
M marsh  S stream/water  E enclosure  O obstacle (hedge/wall)  X impassable  ? unknown  # border."""
import math
import sys

from PIL import Image, ImageDraw, ImageFont

TERRAIN = {".": ("#9cc46a", "open"), "W": ("#2f6b2f", "woods"), "H": ("#c9b26b", "hill"),
           "R": ("#a08a6a", "rough"), "F": ("#c7cf6e", "fields"), "T": ("#d9c9a3", "track"),
           "B": ("#8a5a44", "buildings"), "M": ("#5f8f86", "marsh"), "S": ("#4f7fbf", "water"),
           "E": ("#b5c98a", "enclosure"), "O": ("#6b4f2f", "obstacle"), "X": ("#333333", "impassable"),
           "?": ("#bbbbbb", "unknown"), "#": ("#777777", "border")}
DIRS = {"N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1), "S": (0, 1), "SW": (-1, 1),
        "W": (-1, 0), "NW": (-1, -1)}


def parse(path):
    sec, grid, units, moves, marks = None, [], [], [], []
    for raw in open(path):
        line = raw.rstrip("\n")
        if line.strip().startswith("#") and sec != "grid":
            continue
        if line.strip().endswith(":") and line.strip()[:-1] in ("grid", "units", "moves", "marks", "colour"):
            sec = line.strip()[:-1]; continue
        if not line.strip():
            continue
        p = line.split()
        if sec == "grid":
            grid.append(line.strip())
        elif sec == "units":
            units.append((p[0], p[1], int(p[2]), int(p[3]), p[4], " ".join(p[5:])))
        elif sec == "moves":
            rest = p[6:]
            col = "#d01010"
            if rest and rest[0].startswith("c="):
                col, rest = rest[0][2:], rest[1:]
            moves.append((p[0], int(p[1]), int(p[2]), int(p[4]), int(p[5]), " ".join(rest), col))
        elif sec == "marks":
            marks.append((int(p[0]), int(p[1]), " ".join(p[2:])))
        elif sec == "colour":
            TERRAIN[p[0]] = (p[1], " ".join(p[2:]) or p[0])
    return grid, units, moves, marks


def main(a):
    if not a:
        sys.exit(__doc__)
    cell = int(a[a.index("--cell") + 1]) if "--cell" in a else 28
    oc, orr = (int(a[a.index("--origin") + 1]), int(a[a.index("--origin") + 2])) if "--origin" in a else (0, 0)
    skip = set()
    for k, n in (("--cell", 1), ("--origin", 2)):
        if k in a:
            i = a.index(k); skip.update(range(i, i + n + 1))
    args = [x for i, x in enumerate(a) if i not in skip]
    src = args[0]
    out = args[1] if len(args) > 1 else src.rsplit(".", 1)[0] + ".png"
    grid, units, moves, marks = parse(src)
    rows, cols = len(grid), max(len(r) for r in grid)
    m = 22
    used = sorted({c for r in grid for c in r})
    W = max(m + cols * cell + 4, 320)
    per = max(1, (W - m) // 140)
    legend_h = 18 * ((len(used) + per - 1) // per) + 10
    img = Image.new("RGB", (W, m + rows * cell + legend_h), "white")
    d = ImageDraw.Draw(img)
    try:
        f = ImageFont.truetype("DejaVuSans.ttf", max(9, cell // 3))
        fs = ImageFont.truetype("DejaVuSans.ttf", 10)
    except OSError:
        f = fs = ImageFont.load_default()
    xy = lambda c, r: (m + c * cell, m + r * cell)
    for r, row in enumerate(grid):
        for c in range(cols):
            ch = row[c] if c < len(row) else "?"
            x, y = xy(c, r)
            d.rectangle([x, y, x + cell, y + cell], fill=TERRAIN.get(ch, ("#ff00ff", ch))[0], outline="#55555555")
    for c in range(cols):
        d.text((m + c * cell + cell // 2 - 4, 4), str(c + oc), fill="black", font=fs)
    for r in range(rows):
        d.text((2, m + r * cell + cell // 2 - 6), str(r + orr), fill="black", font=fs)
    for c, r, t in marks:
        x, y = xy(c, r); d.text((x + 2, y + 2), t, fill="black", font=fs)
    for uid, side, c, r, face, label in units:
        x, y = xy(c, r); k = cell * 0.15
        d.rectangle([x + k, y + k, x + cell - k, y + cell - k], fill=side, outline="black", width=2)
        d.text((x + k + 2, y + k), uid, fill="white" if side not in ("yellow", "white") else "black", font=f)
        if face in DIRS:
            dx, dy = DIRS[face]; cx, cy = x + cell / 2, y + cell / 2
            d.line([cx, cy, cx + dx * cell * 0.55, cy + dy * cell * 0.55], fill="black", width=3)
    for uid, _, c0, r0, c1, r1, label, mcol in [(mv[0], None, *mv[1:]) for mv in moves]:
        (x0, y0), (x1, y1) = xy(c0, r0), xy(c1, r1)
        d.rectangle([x0 + 3, y0 + 3, x0 + cell - 3, y0 + cell - 3], outline="#555555", width=1)  # where it started
        x0 += cell / 2; y0 += cell / 2; x1 += cell / 2; y1 += cell / 2
        L = math.hypot(x1 - x0, y1 - y0) or 1
        ang = math.atan2(y1 - y0, x1 - x0)
        x1 -= math.cos(ang) * cell * 0.38; y1 -= math.sin(ang) * cell * 0.38   # stop short of the unit box
        d.line([x0, y0, x1, y1], fill=mcol, width=3)
        for s_ in (0.45, -0.45):
            d.line([x1, y1, x1 - 12 * math.cos(ang + s_), y1 - 12 * math.sin(ang + s_)], fill=mcol, width=3)
        if label:
            d.text(((x0 + x1) / 2 + 3, (y0 + y1) / 2 - 12), label, fill=mcol, font=fs)
    ly = m + rows * cell + 6
    for i, ch in enumerate(used):
        x = m + (i % per) * 140; y = ly + (i // per) * 18
        d.rectangle([x, y, x + 14, y + 14], fill=TERRAIN.get(ch, ("#ff00ff", ch))[0], outline="black")
        d.text((x + 18, y), f"{ch} {TERRAIN.get(ch, ('', '?'))[1]}", fill="black", font=fs)
    img.save(out)
    print(out, f"{cols}x{rows}")


if __name__ == "__main__":
    main(sys.argv[1:])
