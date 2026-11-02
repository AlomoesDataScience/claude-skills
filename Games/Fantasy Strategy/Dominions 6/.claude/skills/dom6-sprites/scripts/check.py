"""Validate Dominions 6 sprites and print their figure bounds.

  python3 -I check.py file.tga [...]

Checks: width and height are each 8/16/32/64/128 (wide 128x64 canvases are
used for beasts and vehicles), 24-bit RGB (or RGBA), and the bottom two
rows hold only shadow or transparency. Prints the bounding box of non-transparent, non-shadow
pixels (x range, top row, bottom row) for comparing heights with reference units.
The bounds include raised weapons and effects, so compare idle frames for body height.
"""
import sys

from PIL import Image

ok = True
for f in sys.argv[1:]:
    im = Image.open(f)
    w, h = im.size
    px = im.convert("RGB").load()
    notes = []
    if w not in (8, 16, 32, 64, 128) or h not in (8, 16, 32, 64, 128):
        notes.append(f"bad size {im.size}")
    if im.mode not in ("RGB", "RGBA"):
        notes.append(f"mode {im.mode}")
    pts = [(x, y) for y in range(h) for x in range(w) if px[x, y] not in ((0, 0, 0), (255, 0, 255))]
    if any(y >= h - 2 for x, y in pts):
        notes.append("figure pixels in the bottom 2 rows")
    box = (min(p[0] for p in pts), max(p[0] for p in pts), min(p[1] for p in pts), max(p[1] for p in pts)) if pts else None
    ok &= not notes
    print(f, im.size, im.mode, "x %d-%d  y %d-%d (%d px tall)" % (box[0], box[1], box[2], box[3], box[3] - box[2] + 1)
          if box else "empty", "; ".join(notes) or "OK")
sys.exit(0 if ok else 1)
