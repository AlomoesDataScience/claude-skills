#!/usr/bin/env python3
"""Measure how a game's map camera moves: pixels of map shift per held key, so pans can be planned
(photos that overlap, a camera move that lands on the spot you want). Runs on the bgplay screen.

  camcal.py [--keys w s a d] [--ms 150] [--band X0 Y0 X1 Y1] [--wait 1200]
For each key: photo, hold the key --ms, photo, match the two by edges (photo-map panorama.py), print
the shift in px, px per 100 ms and the match score, then hold the opposite key the same time to come
back. Match below ~0.25 = not trusted (pan too big for the band, or featureless ground) - lower --ms.
Only the camera moves; nothing is clicked."""
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.expanduser("~/Desktop/AI Development/.claude/skills/photo-map/scripts"))
import panorama as P  # noqa: E402

OPP = {"w": "s", "s": "w", "a": "d", "d": "a", "Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}


def main(a):
    keys = P.arg(a, "--keys", None)
    if keys is not None:
        i = a.index("--keys") + 1
        keys = []
        while i < len(a) and not a[i].startswith("--"):
            keys.append(a[i]); i += 1
    keys = keys or ["w", "s", "a", "d"]
    ms = P.arg(a, "--ms", 150, cast=int)
    wait = P.arg(a, "--wait", 1200, cast=int)
    band = P.arg(a, "--band", [570, 190, 1595, 665], 4, int)
    for k in keys:
        before = P.seq("move 1590 960", f"wait {wait}", "shot --full")[-1]
        after = P.seq(f"hold {k} {ms}", f"wait {wait}", "shot --full")[-1]
        ea = P.edges(Image.open(before).convert("RGB").crop(band))
        eb = P.edges(Image.open(after).convert("RGB").crop(band))
        res = []
        for axis in ("v", "h"):
            for x, y, sign in ((ea, eb, 1), (eb, ea, -1)):
                s, d, dx = P.match(x, y, axis)
                res.append((s, axis, sign * d, sign * dx if axis == "v" else sign * dx))
        s, axis, d, dx = max(res)
        if axis == "v":
            dy_, dx_ = d, dx
        else:
            dy_, dx_ = dx, d
        print(f"{k:>6} {ms} ms: map moved dy {dy_:+d} px, dx {dx_:+d} px  "
              f"({abs(d) * 100 / ms:.0f} px/100ms along {'y' if axis == 'v' else 'x'}), match {s:.2f}")
        if k in OPP:
            P.seq(f"hold {OPP[k]} {ms}", "wait 600")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):   # never drive a game just to see the usage
        sys.exit(__doc__ + "\n(run with --go and no other options for all the defaults)")
    main([x for x in sys.argv[1:] if x != "--go"])
