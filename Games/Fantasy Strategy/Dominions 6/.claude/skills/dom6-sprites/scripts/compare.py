"""Side-by-side zoomed comparison sheet.

  python3 -I compare.py OUT.png ZOOM row1a.tga,row1b.tga,... row2a.tga,...

Each argument after ZOOM is one row of comma-separated images. Every image is
drawn at ZOOM times its own size, so relative scale is preserved. Rows are labelled with
the first file's name. Use it to put a new sprite next to its Dominions Enhanced
stance reference, or to check a whole roster for consistent scale.
"""
import os
import sys

from PIL import Image, ImageDraw

out, z, rows = sys.argv[1], int(sys.argv[2]), [r.split(",") for r in sys.argv[3:]]
ims = [[Image.open(f).convert("RGB") for f in r] for r in rows]
w = max(sum(i.size[0] * z + 8 for i in r) for r in ims)
hs = [max(i.size[1] for i in r) * z + 14 for r in ims]
W = Image.new("RGB", (w, sum(hs)), (60, 100, 50))
d = ImageDraw.Draw(W)
y = 0
for r, files, h in zip(ims, rows, hs):
    x = 0
    for im in r:
        big = im.resize((im.size[0] * z, im.size[1] * z), Image.NEAREST)
        W.paste(big, (x, y + h - big.size[1]))
        x += big.size[0] + 8
    d.text((2, y), os.path.basename(files[0]), fill=(255, 255, 0))
    y += h
W.save(out)
