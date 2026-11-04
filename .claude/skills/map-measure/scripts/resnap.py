#!/usr/bin/env python3
"""Re-snap the map grid on a screenshot by matching it against an older picture whose grid is known
(the user 2026-11-02: "create a tool to automatically resnap the grid based on an older picture ... so you
know where the grid is at. It should also support zooming in and zooming out"). Runs on Claude's side
only - photos in, numbers out; the game is never touched.

  resnap.py build OUT.png --sq 59.25 --cols 32 --rows 24 [--margin 400] --strip PANO.png MAPX0 MAPY0 [...]
      paste photo strips into one reference picture. MAPX0 MAPY0 = where the strip's top-left pixel
      sits in MAP pixels ((0,0) = inner corner of square 0,0; a strip whose inner west edge is at x 325
      and north edge at y 215 -> -325 -215). --margin keeps that much border/void around the map so
      views showing the map's edge still match. Writes OUT.json (sq, margin) beside it.
  resnap.py find REF.png SHOT.png [--zoom LO HI] [--ui X0 Y0 X1 Y1 ...] [--area X0 Y0 X1 Y1]
      prints  sq S  x0 X  y0 Y  match M : on SHOT, square (c,r) spans X + c*S .. +S, Y + r*S .. +S.
      --zoom searches screen square sizes from LO*sq to HI*sq (1 = the reference's zoom).
      --area = the map part of the screen; --ui = boxes masked out (fixed UI). Defaults: FoG II bgplay.
Method (OpenCV matchTemplate when installed, else numpy FFT; --numpy forces it): smoothed brightness (woods dark, tracks light; grass texture and figures blur out), masked
normalised cross-correlation by FFT at 1/4 size for every zoom, a fine zoom pass, then a full-size local
refine. Right answers score 0.75-0.9; under 0.5 do not trust it (look at the picture)."""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageFilter
try:
    import cv2                              # OpenCV: fast masked template matching (optional)
except ImportError:
    cv2 = None

AREA = (0, 30, 1600, 900)
UI = [(0, 30, 330, 250), (1370, 30, 1600, 120), (1500, 400, 1600, 560), (1330, 715, 1600, 900),
      (310, 740, 1290, 900)]   # unit cards: ours bottom-left, hovered enemy bottom-middle


def lum(im, blur=3):
    return np.asarray(im.convert("L").filter(ImageFilter.GaussianBlur(blur)), dtype=np.float64)


def fcorr(a, b, sh):
    """correlation of b over a (valid part), both already in the same size frame."""
    return np.fft.irfft2(np.fft.rfft2(a, sh) * np.conj(np.fft.rfft2(b, sh)), sh)


def mncc_map(ref, tpl, mask):
    """masked normalised cross-correlation of tpl (with 0/1 mask) at every valid offset in ref."""
    H, W = ref.shape; h, w = tpl.shape
    sh = (1 << int(np.ceil(np.log2(H + h))), 1 << int(np.ceil(np.log2(W + w))))
    n = mask.sum()
    t0 = mask * (tpl - (tpl * mask).sum() / n)
    num = fcorr(ref, t0, sh)[:H - h + 1, :W - w + 1]
    s1 = fcorr(ref, mask, sh)[:H - h + 1, :W - w + 1]
    s2 = fcorr(ref * ref, mask, sh)[:H - h + 1, :W - w + 1]
    var = np.maximum(s2 - s1 * s1 / n, 1e-6)
    return num / np.sqrt(var * (t0 * t0).sum())


def mncc(r, t, m):
    n = m.sum(); t0 = m * (t - (t * m).sum() / n); r0 = m * (r - (r * m).sum() / n)
    d = np.sqrt((t0 * t0).sum() * (r0 * r0).sum())
    return float((t0 * r0).sum() / d) if d else -1.0


def opt(a, k, n, d):
    if k not in a:
        return d
    i = a.index(k); v = a[i + 1:i + 1 + n]
    return [float(x) for x in v] if n > 1 else float(v[0])


def build(a):
    out = a[1]; sq = opt(a, "--sq", 1, 59.25); M = int(opt(a, "--margin", 1, 400))
    cols, rows = int(opt(a, "--cols", 1, 32)), int(opt(a, "--rows", 1, 24))
    W, H = int(round(cols * sq)) + 2 * M, int(round(rows * sq)) + 2 * M
    canvas = Image.new("RGB", (W, H), (0, 0, 0))
    i = 0
    while "--strip" in a[i:]:
        i = a.index("--strip", i)
        canvas.paste(Image.open(a[i + 1]).convert("RGB"), (int(float(a[i + 2])) + M, int(float(a[i + 3])) + M))
        i += 4
    canvas.save(out)
    json.dump({"sq": sq, "margin": M, "cols": cols, "rows": rows}, open(os.path.splitext(out)[0] + ".json", "w"))
    print("reference", out, canvas.size, "square", sq, "margin", M)


def find(a):
    ref_p, shot_p = a[1], a[2]
    meta_p = os.path.splitext(ref_p)[0] + ".json"
    meta = json.load(open(meta_p)) if os.path.exists(meta_p) else {"sq": 59.25, "margin": 0}
    sq, M = meta["sq"], meta["margin"]
    zlo, zhi = opt(a, "--zoom", 2, [1.0, 1.0])
    ax0, ay0, ax1, ay1 = [int(v) for v in opt(a, "--area", 4, list(AREA))]
    ui = UI if "--ui" not in a else [tuple(int(v) for v in a[i + 1:i + 5]) for i, k in enumerate(a) if k == "--ui"]
    shot = Image.open(shot_p).convert("RGB").crop((ax0, ay0, ax1, ay1))
    mask_full = np.ones((ay1 - ay0, ax1 - ax0))
    for (x0, y0, x1, y1) in ui:
        mask_full[max(0, y0 - ay0):max(0, y1 - ay0), max(0, x0 - ax0):max(0, x1 - ax0)] = 0
    mask_im = Image.fromarray((mask_full * 255).astype(np.uint8))
    ref_im = Image.open(ref_p).convert("RGB")
    K = 4
    ref4 = lum(ref_im.resize((ref_im.width // K, ref_im.height // K), Image.BILINEAR), 1)

    def search(z):                          # z = screen px per reference px
        tw, th = int(shot.width / z / K), int(shot.height / z / K)
        if tw >= ref4.shape[1] or th >= ref4.shape[0] or tw < 30 or th < 20:
            return (-2, z, 0, 0)
        t = lum(shot.resize((tw, th), Image.BILINEAR), 1)
        m = (np.asarray(mask_im.resize((tw, th), Image.NEAREST)) > 127).astype(np.float64)
        if cv2 is not None and "--numpy" not in a:
            c = cv2.matchTemplate(ref4.astype(np.float32), t.astype(np.float32), cv2.TM_CCOEFF_NORMED,
                                  mask=m.astype(np.float32))
            c = np.nan_to_num(c, nan=-1.0, posinf=-1.0, neginf=-1.0)
        else:
            c = mncc_map(ref4, t, m)
        py, px = np.unravel_index(np.argmax(c), c.shape)
        return (float(c[py, px]), z, px * K, py * K)

    scales = [1.0] if zlo == zhi == 1.0 else list(np.exp(np.linspace(np.log(zlo), np.log(zhi), 41)))
    best = max((search(z) for z in scales), key=lambda t: t[0])
    if len(scales) > 1:
        best = max([best] + [search(best[1] * f) for f in np.arange(0.97, 1.0301, 0.005)], key=lambda t: t[0])
    _, z, rx, ry = best
    # full-size refine (at half size for speed) around the coarse answer
    k = 2
    refh = lum(ref_im.resize((ref_im.width // k, ref_im.height // k), Image.BILINEAR), 1.5)
    tw, th = int(shot.width / z / k), int(shot.height / z / k)
    t = lum(shot.resize((tw, th), Image.BILINEAR), 1.5)
    m = (np.asarray(mask_im.resize((tw, th), Image.NEAREST)) > 127).astype(np.float64)
    loc = (-2, rx // k, ry // k)
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            x, y = rx // k + dx, ry // k + dy
            if 0 <= y <= refh.shape[0] - th and 0 <= x <= refh.shape[1] - tw:
                s = mncc(refh[y:y + th, x:x + tw], t, m)
                if s > loc[0]:
                    loc = (s, x, y)
    mt, rx, ry = loc[0], loc[1] * k, loc[2] * k
    S = sq * z
    x0 = ax0 - (rx - M) * z; y0 = ay0 - (ry - M) * z     # screen position of the map's (0,0) corner
    print(f"sq {S:.2f} x0 {x0:.1f} y0 {y0:.1f} match {mt:.2f}")
    return S, x0, y0, mt


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    {"build": build, "find": find}[a[0]](a)
