#!/usr/bin/env python3
"""Hover a list of screen points one at a time and show what each one says (tooltip, highlight).
The user's rule (2026-11-02): on a new screen, check what every element does - UI elements stand out
from the background (frames, bevels, icons, text on plates); hover each before clicking any.

  hoversheet.py [--bg] [--wait MS] [--park X Y] X,Y [X,Y ...]

For each point: park the pointer (default top-left corner area 5,5... see --park), shoot, move onto
the point, wait (--wait, default 1500 ms: tooltips take a moment), shoot again. The difference
between the two shots is what the hover changed - the tooltip wherever the game draws it (next to
the pointer, in a bottom bar, in a side panel) plus the element's own highlight. Two parked shots
are taken so that whatever moves by itself (a 3D scene) is ignored. Prints per point
the changed box and its text (OCR through the tool's `read`), "nothing" when the hover changed
nothing (background, or a disabled element), and saves one contact sheet - a labelled crop per
point - to <shots dir>/hoversheet.png. Read the sheet; the OCR is only a first pass.

--bg  = the bgplay virtual screen (bgplay.py); without it gameui.py with its guard (UI_WMCLASS).
Hovering only: nothing is clicked.
"""
import os
import subprocess
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))


def opt(a, name, n=1):
    if name in a:
        i = a.index(name)
        v = a[i + 1:i + 1 + n]
        del a[i:i + 1 + n]
        return v
    return None


def seq(tool, *steps):
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, tool), "seq", *steps],
                       capture_output=True, text=True)
    return [ln for ln in r.stdout.splitlines() if ln.endswith(".png")], r.stdout


def changed(a, b):
    return ImageChops.difference(a.convert("L"), b.convert("L")).point(lambda v: 255 if v > 24 else 0)


def changed_box(still1, still2, hover):
    """What the hover changed, minus what changes by itself (3D scenes: flags, water, camera drift):
    pixels that differ between the two parked shots are masked out (grown a little), and speckle
    is removed (MinFilter) so only a solid block - a tooltip, a highlight - is left."""
    moving = changed(still1, still2).filter(ImageFilter.MaxFilter(9))
    d = ImageChops.subtract(changed(still2, hover), moving)
    return d.filter(ImageFilter.MinFilter(5)).getbbox()


def main(a):
    if not a or "-h" in a or "--help" in a:
        sys.exit(__doc__)
    bg = "--bg" in a
    if bg:
        a.remove("--bg")
    wait = int((opt(a, "--wait") or ["1500"])[0])
    park = opt(a, "--park", 2) or ["5", "5"]
    tool = "bgplay.py" if bg else "gameui.py"
    nums = [int(v) for p in a for v in p.split(",") if v.strip()]       # "X,Y X,Y" or "X Y X Y"
    if len(nums) % 2:
        sys.exit("points come in pairs: X,Y X,Y ... (or X Y X Y ...)")
    pts = list(zip(nums[::2], nums[1::2]))
    crops, outdir = [], None
    for x, y in pts:
        shots, _ = seq(tool, f"move {park[0]} {park[1]}", "wait 600", "shot --full", "wait 400",
                       "shot --full", f"move {x} {y}", f"wait {wait}", "shot --full")
        if len(shots) < 3:
            print(f"{x},{y}: no shot")
            continue
        outdir = os.path.dirname(shots[-1])
        s1, s2, after = (Image.open(f).convert("RGB") for f in shots[:3])
        box = changed_box(s1, s2, after)
        if not box:
            print(f"{x},{y}: nothing (hover changed nothing)")
            crop = after.crop((max(0, x - 80), max(0, y - 30), x + 80, y + 30))
        else:
            box = (max(0, box[0] - 6), max(0, box[1] - 6), min(after.width, box[2] + 6), min(after.height, box[3] + 6))
            _, txt = seq(tool, f"read {box[0]} {box[1]} {box[2]} {box[3]}")
            words = " ".join(ln.strip() for ln in txt.splitlines()
                             if ln.strip() and not ln.startswith("[") and not ln.endswith(".png"))
            print(f"{x},{y}: box {box}  text: {words[:160] or '(no text read)'}")
            crop = after.crop(box)
            if crop.width > 900 or crop.height > 400:          # the hover redrew a big area: keep near the point
                crop = after.crop((max(0, x - 300), max(0, y - 120), x + 400, y + 200))
        crops.append((f"{x},{y}", crop))
    if not crops:
        return
    w = max(c.width for _, c in crops) + 10
    h = sum(c.height + 22 for _, c in crops)
    sheet = Image.new("RGB", (max(w, 200), h), "white")
    dr, yy = ImageDraw.Draw(sheet), 0
    for label, c in crops:
        dr.text((4, yy + 4), label, fill="black")
        sheet.paste(c, (5, yy + 20))
        yy += c.height + 22
    out = os.path.join(outdir, "hoversheet.png")
    sheet.save(out)
    print(out)


if __name__ == "__main__":
    main(sys.argv[1:])
