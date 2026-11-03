#!/usr/bin/env python3
"""Cut every map square out of the photos into a labelled grid, so terrain and units can be read
square by square (and checked against a drawn board).
  squares.py CONFIG.json
CONFIG: {"cols": 32, "rows": 24, "square": 59.25, "cell": 48, "parts": [2, 2], "out": "DIR",
         "strips": [{"file": "west.png", "x0": 229, "y0": 17, "cols": [0, 11]}, ...]}
x0/y0 = where map square (0,0)'s top-left corner would be in that photo (may be negative or off the
photo); "cols" = [first, last+1] map columns taken from that photo. A strip may also give "rows".
Writes DIR/squares.png (whole grid) and DIR/squares_<i><j>.png parts with column/row numbers."""
import json
import os
import sys

from PIL import Image, ImageDraw


def main(cfg_path):
    cfg = json.load(open(cfg_path))
    C, R, sq, cell = cfg["cols"], cfg["rows"], cfg["square"], cfg.get("cell", 48)
    out_dir = cfg.get("out", os.path.dirname(os.path.abspath(cfg_path)))
    os.makedirs(out_dir, exist_ok=True)
    img = Image.new("RGB", (C * cell, R * cell), "black")
    for s in cfg["strips"]:
        ph = Image.open(s["file"]).convert("RGB")
        c0, c1 = s.get("cols", [0, C]); r0, r1 = s.get("rows", [0, R])
        for c in range(c0, c1):
            for r in range(r0, r1):
                box = tuple(int(v) for v in (s["x0"] + c * sq, s["y0"] + r * sq, s["x0"] + (c + 1) * sq, s["y0"] + (r + 1) * sq))
                img.paste(ph.crop(box).resize((cell, cell)), (c * cell, r * cell))
    d = ImageDraw.Draw(img)
    for c in range(C + 1):
        d.line([c * cell, 0, c * cell, R * cell], fill="white")
    for r in range(R + 1):
        d.line([0, r * cell, C * cell, r * cell], fill="white")
    img.save(os.path.join(out_dir, "squares.png"))
    pc, pr = cfg.get("parts", [2, 2])
    for i in range(pc):
        for j in range(pr):
            ca, cb = C * i // pc, C * (i + 1) // pc
            ra, rb = R * j // pr, R * (j + 1) // pr
            part = img.crop((ca * cell, ra * cell, cb * cell, rb * cell))
            P = Image.new("RGB", (part.width + 30, part.height + 20), "white")
            P.paste(part, (30, 20)); dd = ImageDraw.Draw(P)
            for c in range(ca, cb):
                dd.text((30 + (c - ca) * cell + cell // 2 - 6, 4), str(c), fill="black")
            for r in range(ra, rb):
                dd.text((4, 20 + (r - ra) * cell + cell // 2 - 6), str(r), fill="black")
            P.save(os.path.join(out_dir, f"squares_{i}{j}.png"))
    print(out_dir)


if __name__ == "__main__":
    main(sys.argv[1])
