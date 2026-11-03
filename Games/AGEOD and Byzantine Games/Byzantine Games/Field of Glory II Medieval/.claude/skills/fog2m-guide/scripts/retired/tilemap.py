#!/usr/bin/env python3
"""FoG II Medieval: draw the visible battlefield as a grid map - terrain per square and who is where -
from ONE screenshot plus a few hovers. The user (2026-11-02): "check the map, figure out what tiles
mean what, and draw a map to do things geometrically with tactics".

  tilemap.py [--every 3] [--out DIR]

Before running: top view, max zoom-out, nothing selected, and the camera centred on a unit (Tab /
Next Unmoved / a Unit List entry put it at 800,465 = a square centre; squares are 59 px).
  1. one screenshot; every square inside the map view gets colour/texture features
  2. LEARN: hover every Nth square (--every, both ways) and read the tooltip -> labelled samples
     (open, rough, marsh, woods, fields, built-up, difficult, obstacle/fence, hill flag)
  3. CLASSIFY the rest by nearest labelled sample in feature space
  4. UNITS: squares with figure-like pixels (bright white / saturated non-green) are hovered;
     tooltip gives the name, the card banner gives the side (blue ours, green Irish)
Output: a text map with column/row numbers relative to the centre square (+col east/right,
+row south/down), a unit list, and tilemap.png (the screenshot with the grid and labels drawn) in
--out (default the bgplay shots dir). Coordinates hold until the camera moves.
"""
import os
import re
import subprocess
import sys

from PIL import Image, ImageDraw, ImageStat

BG = os.path.expanduser("~/Desktop/AI Development/.claude/skills/game-ui/scripts/bgplay.py")
CX, CY, SQ = 800, 465, 59
VIEW = (0, 30, 1500, 900)                 # map view, clear of the right icon column
UI_BOXES = [(0, 30, 340, 250), (1370, 30, 1600, 120), (1330, 720, 1600, 900), (1490, 170, 1600, 740)]
TER = (("Obstacle", "#"), ("Marsh", "m"), ("Wood", "W"), ("Rough", "r"), ("Built", "b"),
       ("Difficult", "d"), ("Track", "t"), ("Field", "f"), ("Open", "."))


def seq(*steps):
    return subprocess.run([sys.executable, "-I", BG, "seq", *steps], capture_output=True, text=True).stdout


def text(out):
    return " ".join(ln for ln in out.splitlines() if ln.strip() and not ln.startswith("[")
                    and not ln.endswith(".png"))


def shots(out):
    return [ln for ln in out.splitlines() if ln.endswith(".png")]


def in_ui(x, y):
    return any(a - 30 <= x <= c + 30 and b - 30 <= y <= d + 30 for a, b, c, d in UI_BOXES)


def feats(img, x, y):
    c = img.crop((x - 24, y - 24, x + 24, y + 24))
    st = ImageStat.Stat(c)
    r, g, b = st.mean
    lum = ImageStat.Stat(c.convert("L"))
    px = list(c.getdata())
    brown = sum(1 for p in px if p[0] > p[1] and p[0] - p[2] > 25 and p[0] < 150) / len(px)
    figure = sum(1 for p in px if min(p) > 185 or
                 (max(p) - min(p) > 80 and not (p[1] >= p[0] - 10 and p[1] >= p[2]))) / len(px)
    return (r, g, b, lum.stddev[0], brown * 100), figure


def tooltip(x, y):
    out = seq(f"move {x} {y}", "wait 900", f"read 0 {y + 12} 1590 {min(990, y + 150)}",
              f"read 0 {max(0, y - 170)} 1590 {y - 8}", "shot --full")
    return text(out), (shots(out)[-1] if shots(out) else None)


def side(shot):
    if not shot:
        return "?"
    px = list(Image.open(shot).convert("RGB").crop((822, 752, 848, 800)).getdata())
    r, g, b = (sum(p[i] for p in px) / len(px) for i in range(3))
    return "A" if b > r + 25 and b > g else ("E" if g > r + 15 and g > b else "?")


def label(t):
    return next((c for k, c in TER if k.lower() in t.lower()), None)


def main(a):
    every = int(a[a.index("--every") + 1]) if "--every" in a else 3
    out = shots(seq("move 1550 880", "wait 500", "shot --full"))
    img = Image.open(out[-1]).convert("RGB")
    outdir = a[a.index("--out") + 1] if "--out" in a else os.path.dirname(out[-1])
    cols = [i for i in range(-20, 21) if VIEW[0] + 30 <= CX + i * SQ <= VIEW[2] - 30]
    rows = [j for j in range(-10, 11) if VIEW[1] + 30 <= CY + j * SQ <= VIEW[3] - 30]
    sq = {}
    for j in rows:
        for i in cols:
            x, y = CX + i * SQ, CY + j * SQ
            if in_ui(x, y):
                continue
            f, fig = feats(img, x, y)
            if f[0] + f[1] + f[2] < 90 or (abs(f[0] - f[1]) < 8 and abs(f[1] - f[2]) < 8 and f[0] > 90):
                sq[(i, j)] = {"t": "~", "f": f, "fig": 0}       # black outside / grey stone border
            else:
                sq[(i, j)] = {"t": None, "f": f, "fig": fig}
    # learn
    samples = []
    for (i, j), s in sq.items():
        if s["t"] is None and i % every == 0 and j % every == 0 and s["fig"] < 0.01:
            t, _ = tooltip(CX + i * SQ, CY + j * SQ)
            lab = label(t)
            if lab and not re.search(r"\(\d+\)", t):
                s["t"], s["hill"] = lab, "hill" in t.lower()
                samples.append((s["f"], lab))
    print(f"learned {len(samples)} samples: " + ", ".join(sorted({l for _, l in samples})), flush=True)
    # classify
    for s in sq.values():
        if s["t"] is None and samples:
            s["t"] = min(samples, key=lambda fl: sum((p - q) ** 2 for p, q in zip(s["f"], fl[0])))[1]
    # units
    units = []
    for (i, j), s in sq.items():
        if s["fig"] >= 0.01 and s["t"] != "~":
            t, shot = tooltip(CX + i * SQ, CY + j * SQ)
            m = re.search(r"([A-Z][A-Za-z&' ]*?)\s*\((\d{1,2})\)", t)
            if m:
                sd = side(shot)
                s["u"] = sd
                units.append((sd, f"{m.group(1).strip()} ({m.group(2)})", i, j, label(t) or s["t"]))
            elif label(t):
                s["t"] = label(t)
    # draw
    print("     " + "".join(f"{i:+d}"[-1] for i in cols) + "   <- col (last digit), centre col 0 at x=800")
    for j in rows:
        line = "".join(sq.get((i, j), {}).get("u") or sq.get((i, j), {}).get("t") or " " for i in cols)
        print(f"{j:+3d}  {line}")
    print("legend: . open  f fields  t track  r rough  d difficult  m marsh  W woods  b built-up  # fence/obstacle"
          "  ~ off-map   A ours  E enemy  ? side unknown")
    print("units (col,row): " if units else "no units found")
    for sd, n, i, j, t in sorted(units, key=lambda u: (u[0], u[2], u[3])):
        print(f"  {'ours ' if sd == 'A' else 'ENEMY' if sd == 'E' else '?    '} {n:30s} ({i:+d},{j:+d}) x={CX + i * SQ} y={CY + j * SQ} on {t}")
    dr = ImageDraw.Draw(img)
    for (i, j), s in sq.items():
        x, y = CX + i * SQ, CY + j * SQ
        dr.rectangle((x - 29, y - 29, x + 29, y + 29), outline=(0, 0, 0))
        mark = s.get("u") or s["t"] or ""
        colour = {"A": (0, 0, 255), "E": (255, 0, 0)}.get(mark, (0, 0, 0))
        dr.text((x - 26, y - 27), f"{i},{j}", fill=(0, 0, 0))
        dr.text((x - 4, y - 6), mark, fill=colour)
    p = os.path.join(outdir, "tilemap.png")
    img.save(p)
    print(p)
    seq("move 1550 880")


if __name__ == "__main__":
    main(sys.argv[1:])
