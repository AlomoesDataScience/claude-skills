#!/usr/bin/env python3
"""Find a map's border lines in photos: runs of rows and columns that are mostly border-coloured.
  borders.py IMG [IMG...] [--sat 14] [--br 70 200] [--min 0.6] [--x X0 X1] [--y Y0 Y1]
Border colour = low saturation (max-min of RGB < --sat) and brightness in --br (FoG II: grey stone;
tinted areas need a lower --br min, e.g. 40). --x/--y limit the search area (skip UI). Prints each run
(start, end): the INNER edge of a top/left border is end+1, of a bottom/right border is start."""
import sys

import numpy as np
from PIL import Image


def opt(a, k, d, n=1, cast=int):
    if k not in a:
        return d
    i = a.index(k)
    v = [cast(x) for x in a[i + 1:i + 1 + n]]
    return v[0] if n == 1 else v


def runs(idx):
    out, s, p = [], None, None
    for i in idx:
        if s is None:
            s = p = i
        elif i == p + 1:
            p = i
        else:
            out.append((s, p)); s = p = i
    if s is not None:
        out.append((s, p))
    return out


def main(a):
    sat, br, mn = opt(a, "--sat", 14), opt(a, "--br", [70, 200], 2), opt(a, "--min", 0.6, cast=float)
    xs, ys = opt(a, "--x", None, 2), opt(a, "--y", None, 2)
    skip = {"--sat": 1, "--br": 2, "--min": 1, "--x": 2, "--y": 2}
    files, i = [], 0
    while i < len(a):
        if a[i] in skip:
            i += skip[a[i]] + 1; continue
        files.append(a[i]); i += 1
    for f in files:
        im = np.asarray(Image.open(f).convert("RGB")).astype(int)
        y0, y1 = ys or (0, im.shape[0]); x0, x1 = xs or (0, im.shape[1])
        im = im[y0:y1, x0:x1]
        g = ((im.max(2) - im.min(2)) < sat) & (im.mean(2) >= br[0]) & (im.mean(2) <= br[1])
        rr = [(s + y0, e + y0) for s, e in runs([i for i, v in enumerate(g.mean(1)) if v > mn])]
        cc = [(s + x0, e + x0) for s, e in runs([i for i, v in enumerate(g.mean(0)) if v > mn])]
        print(f"{f}  {im.shape[1]}x{im.shape[0]}\n  border rows {rr}\n  border cols {cc}")


if __name__ == "__main__":
    main(sys.argv[1:])
