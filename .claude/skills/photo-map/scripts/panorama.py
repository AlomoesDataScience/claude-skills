#!/usr/bin/env python3
"""Photograph a whole game map by panning the camera, and stitch the photos into one picture.
The user (2026-11-02): "zoom all the way out, take a photo of the north, the middle and the south ...
construct the map JUST from those pictures. This is ALWAYS how you check what's going on."

  panorama.py [--axis v|h] [--fwd s] [--back w] [--step 400] [--home 4000]
              [--band X0 Y0 X1 Y1] [--max 12] [--out DIR] [--shots A.png B.png ...]

Runs on the bgplay screen (game-ui bgplay.py). Camera keys must pan while held (FoG II: W/S/A/D).
  1. hold --back for --home ms to reach one end of the map, photo
  2. hold --fwd for --step ms, photo; repeat until the picture stops changing (other end) or --max
  3. every photo is cut to --band, a strip of the screen with no UI overlays on it (overlays stay
     put while the map moves and would fool the matching); default 0 250 1490 725 = FoG II
  4. neighbours are lined up by matching their EDGES (fences, trees, figures, borders - flat grass
     carries no information), normalised cross-correlation over every shift, small sideways drift
     allowed; the step must move the map less than the band height (check the printed offsets:
     each must be > 0 and well below the band height)
  5. writes panorama.png (whole map) and prints each photo's offset; the photos are kept
--shots skips the camera and stitches existing photos (in order, same band).
--finish "STEP;STEP" bgplay steps run at the end to put the camera back where a human can read it
(idle-view hard rule; FoG II: --finish "move 1430 807;click 1430 807;wait 1500").
Only the camera moves - nothing is clicked or selected.
"""
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageFilter

BG = os.path.expanduser("~/Desktop/AI Development/.claude/skills/game-ui/scripts/bgplay.py")


def arg(a, k, d, n=1, cast=str):
    if k not in a:
        return d
    i = a.index(k)
    v = [cast(x) for x in a[i + 1:i + 1 + n]]
    return v[0] if n == 1 else v


def seq(*steps):
    out = subprocess.run([sys.executable, "-I", BG, "seq", *steps], capture_output=True, text=True).stdout
    return [l for l in out.splitlines() if l.endswith(".png")]


def edges(im):
    e = np.asarray(im.convert("L").filter(ImageFilter.FIND_EDGES), dtype=np.float32)
    e[e < 12] = 0                      # drop grass texture noise
    return e


def pool(e, k):
    H, W = e.shape[0] // k * k, e.shape[1] // k * k
    return e[:H, :W].reshape(H // k, k, W // k, k).max(axis=(1, 3))


def match(ea, eb, axis, maxdrift=12, minover=80):
    """Shift d of b relative to a along axis (a pixel at p in a is at p-d in b), plus drift.
    Coarse search on 4x max-pooled edges, then refine +-5 px at full size."""
    if axis == "h":
        ea, eb = ea.T, eb.T
    _, d0, x0 = ncc(pool(ea, 4), pool(eb, 4), range(1, ea.shape[0] // 4 - minover // 4),
                    range(-(maxdrift // 4), maxdrift // 4 + 1))
    return ncc(ea, eb, range(max(1, d0 * 4 - 5), d0 * 4 + 6), range(x0 * 4 - 5, x0 * 4 + 6))


def ncc(ea, eb, drange, xrange):
    H, W = ea.shape
    best = (-2.0, 0, 0)
    for d in drange:
        if d >= H:
            continue
        A = ea[d:, :]
        B = eb[:H - d, :]
        for dx in xrange:
            if dx >= 0:
                a, b = A[:, dx:], B[:, :W - dx]
            else:
                a, b = A[:, :W + dx], B[:, -dx:]
            a = a - a.mean()
            b = b - b.mean()
            den = np.sqrt((a * a).sum() * (b * b).sum())
            if den == 0:
                continue
            s = float((a * b).sum() / den)
            if s > best[0]:
                best = (s, d, dx)
    return best


def main(a):
    axis = arg(a, "--axis", "v")
    fwd = arg(a, "--fwd", "s" if axis == "v" else "d")
    back = arg(a, "--back", "w" if axis == "v" else "a")
    step, home, mx = arg(a, "--step", 400, cast=int), arg(a, "--home", 4000, cast=int), arg(a, "--max", 12, cast=int)
    band = arg(a, "--band", [0, 250, 1490, 725], 4, int)
    if "--shots" in a:
        shots = a[a.index("--shots") + 1:]
        shots = [s for s in shots if s.endswith(".png")]
    else:
        shots = seq("move 1550 950", f"hold {back} {home}", "wait 1500", "shot --full")
        last = None
        for _ in range(mx):
            p = seq(f"hold {fwd} {step}", "wait 1300", "shot --full")[-1]
            cur = np.asarray(Image.open(p).convert("L").crop(band), dtype=np.int16)
            prev = np.asarray(Image.open(shots[-1]).convert("L").crop(band), dtype=np.int16)
            if np.abs(cur - prev).mean() < 1.5:       # camera hit the far end
                break
            shots.append(p)
    outdir = arg(a, "--out", os.path.dirname(shots[0]))
    crops = [Image.open(s).convert("RGB").crop(band) for s in shots]
    E = [edges(c) for c in crops]
    pos = [(0, 0)]
    for i in range(1, len(crops)):
        s, d, dx = match(E[i - 1], E[i], axis)
        py, px = pos[-1]
        pos.append((py + d, px + dx) if axis == "v" else (py + dx, px + d))
        print(f"photo {i}: shift {d} px, drift {dx}, match {s:.2f}  ({os.path.basename(shots[i])})")
    w, h = crops[0].size
    ys, xs = [p[0] for p in pos], [p[1] for p in pos]
    canvas = Image.new("RGB", (w + max(xs) - min(xs), h + max(ys) - min(ys)), (0, 0, 0))
    for c, (py, px) in zip(crops, pos):
        canvas.paste(c, (px - min(xs), py - min(ys)))
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "panorama.png")
    canvas.save(out)
    print(f"{len(shots)} photos, panorama {canvas.size[0]}x{canvas.size[1]}: {out}")
    print("photos:", " ".join(shots))
    if "--finish" in a:   # restore the human view (idle-view hard rule), e.g. --finish "click 1430 807"
        steps = a[a.index("--finish") + 1].split(";")
        seq(*[x.strip() for x in steps if x.strip()], "move 1578 448")
        print("camera restored for a human:", steps)
    elif "--shots" not in a:
        print("WARNING: camera left at the map edge - restore the human view now (idle-view; FoG II: order.py present)")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):   # never drive a game just to see the usage
        sys.exit(__doc__ + "\n(run with --go and no other options for all the defaults)")
    main([x for x in sys.argv[1:] if x != "--go"])
