"""Grid snap for the Dominions 6 battle replay: fit the perspective (isometric-looking) battlefield grid
(`g` on) in a screenshot so any screen point maps to a field square (column, row), then place every squad
(team squares, `c` on) on that grid as a text board. The user, 2026-11-03: "getting grid snap working for
isometric is a good idea".

Model (flat ground, camera without roll - the replay camera never rolls):
  - column lines all run to one vanishing point V; where they cross any fixed screen row they are evenly spaced
    (one depth = one scale), so col = (x at the reference row, along the line through V - phase) / spacing;
  - row lines are near-horizontal; 1 / (y - V.y) is linear in the row index (depth is linear in rows),
    so row = (1 / (y - V.y) - phase) / spacing.
Hills bend the lines a little: expect +-0.3 square, worse on slopes.

  python3 -I gridsnap.py check SHOT.png [OUT.png]   fit and draw the fitted grid over the shot (yellow) to check it
  python3 -I gridsnap.py board SHOT.png             fit + squads -> text board (columns left-right, rows far-near)

Library: fit(im) -> dict or None; cell(f, x, y) -> (col, row); board(im) -> (text, squads).
Run with no arguments = this text.
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def line_mask(im, top=110, bottom=45, log_panel=(0, 0, 900, 290)):
    """Grid lines: thin grey-white ridges. Top-hat of the min channel (pixel minus its 5x5 opening) > 18 finds
    them whatever the light (lines ~(120,134,100) over grass ~(70,90,40)); bigger bright things (squares, units,
    pale patches) are wider than the kernel and drop out."""
    import cv2
    a = np.asarray(im.convert("RGB"), dtype=np.uint8)
    th = cv2.morphologyEx(a.min(axis=2), cv2.MORPH_TOPHAT, np.ones((5, 5), np.uint8))
    m = (th > 18).astype(np.uint8)
    H = m.shape[0]
    m[:top] = 0; m[H - bottom:] = 0
    m[:log_panel[3], :log_panel[2]] = 0
    return m


def split_mask(m):
    """(rows, cols): row lines = horizontal runs >= 9 px; columns = the rest."""
    import cv2
    hm = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((1, 9), np.uint8))
    return hm, cv2.subtract(m, cv2.dilate(hm, np.ones((3, 3), np.uint8)))


def segments(m):
    import cv2
    s = cv2.HoughLinesP(m * 255, 1, np.pi / 720, threshold=60, minLineLength=70, maxLineGap=5)
    return [] if s is None else [tuple(map(float, x[0])) for x in s]


def _cluster(vals, tol):
    vals = sorted(vals)
    out = []
    for v in vals:
        if out and v - out[-1][-1] <= tol:
            out[-1].append(v)
        else:
            out.append([v])
    return [sum(c) / len(c) for c in out if len(c) >= 1]


def _spacing(xs, lo, hi):
    """Best (spacing, phase) for values on an evenly spaced comb: score each spacing by how close the values sit
    to the comb (circular mean of the residual phase)."""
    xs = np.asarray(xs, float)
    best = None
    for s in np.arange(lo, hi, (hi - lo) / 400):
        ang = 2 * np.pi * xs / s
        c, sn = np.cos(ang).mean(), np.sin(ang).mean()
        r = math.hypot(c, sn)
        if best is None or r > best[0] + 1e-6:
            best = (r, s, (math.atan2(sn, c) % (2 * np.pi)) * s / (2 * np.pi))
    return best                                     # (agreement 0..1, spacing, phase)


def _period(vals, lo, hi, nbins=4000):
    """Spacing of an evenly spaced comb in vals: the strongest autocorrelation peak of their histogram between
    lo and hi, refined with _spacing. Returns (spacing, phase, agreement)."""
    vals = np.asarray(vals, float)
    span = vals.max() - vals.min()
    bw = span / nbins
    h, _ = np.histogram(vals, bins=nbins)
    h = h - h.mean()
    ac = np.correlate(h, h, "full")[len(h) - 1:]
    ac = ac / ac[0]
    i0, i1 = max(2, int(lo / bw)), min(len(ac) - 1, int(hi / bw) + 1)
    if i1 <= i0 + 2:
        return None
    k = i0 + int(np.argmax(ac[i0:i1]))
    s0 = k * bw
    r, sp, ph = _spacing(vals, s0 * 0.9, s0 * 1.1)
    return sp, ph, r


def _peaks(profile, min_gap, frac=0.25):
    p = np.convolve(profile.astype(float), np.ones(3) / 3, "same")
    thr = p.max() * frac
    out = []
    for i in range(1, len(p) - 1):
        if p[i] >= thr and p[i] >= p[i - 1] and p[i] > p[i + 1]:
            if out and i - out[-1] < min_gap:
                if p[i] > p[out[-1]]:
                    out[-1] = i
                continue
            out.append(i)
    return out


def fit(im):
    """Fit the grid. Returns {"V": (vx, vy), "yref", "col": (spacing, phase, agreement), "rows": [[y, index]..],
    "row": (a, b) for 1/(y - vy) = a - b * index (extrapolation)} or None when too few lines are seen."""
    import cv2
    W, H = im.size
    hm, vm = split_mask(line_mask(im))
    cols = [s for s in segments(vm) if 20 < (math.degrees(math.atan2(s[3] - s[1], s[2] - s[0])) + 180) % 180 < 160]
    if len(cols) < 4:
        return None
    A, b = [], []                                   # vanishing point: least squares through the column lines
    for x0, y0, x1, y1 in cols:
        nx, ny = y1 - y0, x0 - x1
        L = math.hypot(nx, ny)
        A.append([nx / L, ny / L]); b.append((nx * x0 + ny * y0) / L)
    vx, vy = map(float, np.linalg.lstsq(np.asarray(A), np.asarray(b), rcond=None)[0])
    if vy > H * 0.3:
        return None
    # columns: crossings along the screen row with the most column pixels (lower half), evenly spaced there
    rowsum = vm[H // 2: H - 50].sum(axis=1)
    yref = H // 2 + int(np.argmax(np.convolve(rowsum, np.ones(9), "same")))
    xs = _peaks(vm[yref - 3: yref + 4].sum(axis=0), 6)
    if len(xs) < 4:
        return None
    gaps = np.diff(xs)
    s0 = float(np.median(gaps[(gaps > 6) & (gaps < 3 * np.median(gaps))]))
    r, cs, cp = _spacing(xs, s0 * 0.85, s0 * 1.15)
    # column mesh: crossings on scan lines every 24 px, indexed by following the lines out from yref in small
    # steps (prediction through V over 24 px is accurate even when V is a little off or the ground bends)
    def crossings(y):
        if y - 3 < 0 or y + 4 > H:
            return []
        return _peaks(vm[y - 3: y + 4].sum(axis=0), 5, 0.3)
    mesh = {yref: [(x, int(round((x - cp) / cs))) for x in xs]}
    for direction in (-1, 1):
        prev_y, prev = yref, mesh[yref]
        y = yref + 24 * direction
        while 120 < y < H - 50 and y - vy > 25:
            xs_y = crossings(y)
            if len(xs_y) >= 3 and prev:
                loc = np.median(np.diff(xs_y)) if len(xs_y) > 1 else cs
                pred = [(vx + (x - vx) * (y - vy) / (prev_y - vy), i) for x, i in prev]
                got = []
                for x in xs_y:
                    px, i = min(pred, key=lambda p: abs(p[0] - x))
                    if abs(px - x) < 0.4 * loc:
                        got.append((x, i))
                if len(got) >= 3:
                    mesh[y] = got
                    prev_y, prev = y, got
            y += 24 * direction
    # rows: peaks along a vertical strip at the screen centre (rows wave a little; interpolate between them)
    xc = int(min(max(vx, 200), W - 200))
    ys = [y for y in _peaks(hm[:, xc - 60: xc + 60].sum(axis=1), 3) if y - vy > 20]
    if len(ys) < 3:
        return None
    u = 1.0 / (np.asarray(ys, float) - vy)
    du = np.abs(np.diff(u))
    step = float(np.median(du))
    k = np.round((u[0] - u) / step).astype(int)     # 0 at the farthest row seen, growing toward the camera
    bb, aa = np.polyfit(k, u, 1)                     # u = aa + bb k  (bb < 0)
    k = np.round((u - aa) / bb).astype(int)          # re-index from the fit; one row line per index
    keep = {}
    for y, i, uu in zip(ys, k, u):
        err = abs(uu - (aa + bb * i))
        if i not in keep or err < keep[i][1]:
            keep[i] = (y, err)
    ys = [keep[i][0] for i in sorted(keep)]; k = np.asarray(sorted(keep))
    k = k - k.min()
    return {"V": (vx, vy), "yref": float(yref), "col": (cs, cp, r), "rows": [[int(y), int(i)] for y, i in zip(ys, k)],
            "row": (float(aa), float(-bb)), "n_seg": len(cols), "size": (W, H),
            "mesh": [[y, [list(map(float, p)) for p in sorted(mesh[y])]] for y in sorted(mesh)]}


def cell(f, x, y):
    """Screen point -> (col, row) as floats; integer parts = the square. Columns grow to the right, rows grow
    toward the camera, 0 = the farthest row line seen in this shot (compare squads within one shot)."""
    vx, vy = f["V"]
    if y - vy < 1:
        return None
    col = _mesh_col(f, x, y)
    if col is None:
        xr = vx + (x - vx) * (f["yref"] - vy) / (y - vy)
        cs, cp = f["col"][:2]
        col = (xr - cp) / cs
    ry = [r[0] for r in f["rows"]]; ri = [r[1] for r in f["rows"]]
    if ry[0] <= y <= ry[-1]:
        row = float(np.interp(y, ry, ri))
    else:
        aa, bb = f["row"]
        row = (aa - 1.0 / (y - vy)) / bb
    return (col, row)


def _scan_col(pts, x):
    xs = [p[0] for p in pts]; ix = [p[1] for p in pts]
    if x < xs[0] or x > xs[-1]:                     # extrapolate with the end spacing
        j = (0, 1) if x < xs[0] else (-2, -1)
        sp = (xs[j[1]] - xs[j[0]]) / max(1, ix[j[1]] - ix[j[0]])
        ref = 0 if x < xs[0] else -1
        return ix[ref] + (x - xs[ref]) / sp
    return float(np.interp(x, xs, ix))


def _mesh_col(f, x, y):
    """Column from the tracked mesh: interpolate along the scan lines above and below y, then between them."""
    mesh = f.get("mesh") or []
    mesh = [m for m in mesh if len(m[1]) >= 3]
    if not mesh:
        return None
    ys = [m[0] for m in mesh]
    if y <= ys[0]:
        return _scan_col(mesh[0][1], x)
    if y >= ys[-1]:
        return _scan_col(mesh[-1][1], x)
    j = int(np.searchsorted(ys, y))
    (y0, p0), (y1, p1) = mesh[j - 1], mesh[j]
    t = (y - y0) / (y1 - y0)
    # the same ground column moves sideways between scan lines: follow it through V for the lower line
    vx, vy = f["V"]
    x1 = vx + (x - vx) * (y1 - vy) / (y - vy); x0 = vx + (x - vx) * (y0 - vy) / (y - vy)
    return (1 - t) * _scan_col(p0, x0) + t * _scan_col(p1, x1)


def origin(f, margin=40):
    """Field coordinates: (col0, row0, edges) - the column index of the field's LEFT edge and the row index of its
    FAR edge when they are in view (the grid ends there, not at the screen edge), so boards from different
    rounds and camera positions line up. edges = which were found; when missing, 0 is used (relative)."""
    col0 = row0 = 0
    edges = []
    W = f["size"][0]
    lefts = [pts[0] for y, pts in f.get("mesh", []) if len(pts) >= 20 and pts[0][0] > margin]
    if lefts:
        col0 = int(round(min(p[1] for p in lefts))); edges.append("left")
    if f["rows"] and f["rows"][0][0] > 110 + margin:
        row0 = int(f["rows"][0][1]); edges.append("far")
    return col0, row0, edges


def draw(im, f, out):
    """The fitted grid in yellow over the shot - lines should sit on the game's white grid lines."""
    from PIL import ImageDraw
    im = im.convert("RGB").copy()
    d = ImageDraw.Draw(im)
    W, H = im.size
    vx, vy = f["V"]
    cs, cp = f["col"][:2]
    yref = f["yref"]
    top = max(vy + 5, 110)
    for k in range(-80, 80):                        # columns: through V and (cp + k cs, yref)
        xr = cp + k * cs
        xb = vx + (xr - vx) * (H - vy) / (yref - vy)
        xt = vx + (xr - vx) * (top - vy) / (yref - vy)
        if -W < xb < 2 * W:
            d.line([(xt, top), (xb, H)], fill=(255, 220, 0), width=1)
    for y, pts in f.get("mesh", []):                # tracked column crossings (cyan), labelled every 5th column
        for x, i in pts:
            d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(0, 255, 255))
            if int(i) % 5 == 0:
                d.text((x + 3, y - 12), str(int(i)), fill=(0, 255, 255))
    for y, i in f["rows"]:                          # detected row lines (yellow) and the model's (orange, dotted)
        d.line([(0, y), (W, y)], fill=(255, 220, 0), width=1)
    aa, bb = f["row"]
    for k in range(-60, 200):
        v = aa - k * bb
        if v > 0 and top < vy + 1 / v < H:
            yy = vy + 1 / v
            for x in range(0, W, 12):
                d.line([(x, yy), (x + 4, yy)], fill=(255, 120, 0))
    im.save(out)
    return out


def board(im, f=None, min_px=6):
    """Squares held, on the fitted grid: every team-square pixel (`c` on) is mapped to its cell; a cell with
    >= min_px pixels of one colour is held by that side. Letters: D dark green, L light green, P pale (in Troban:
    D = Tir na n'Og, L = Pangaea, P = independents - name them from the Battle Summary and round 0), X = two
    colours in one cell (contact). Returns (text, cells {(col, row): letter})."""
    sys.path.insert(0, HERE)
    from battle_review import square_masks
    f = f or fit(im)
    if not f:
        return "no grid fit (is `g` on?)", {}
    vx, vy = f["V"]
    col0, row0, edges = origin(f)
    ytop = min(f["rows"][0][0], f["mesh"][0][0] if f.get("mesh") else 1e9) - 15   # the field's far edge in view
    counts = {}
    for kind, m in square_masks(im).items():
        ys, xs = np.nonzero(m)
        for x, y in zip(xs[::2], ys[::2]):
            if y < ytop or y - vy < 25:
                continue
            c = cell(f, float(x), float(y))
            if c:
                k = (int(math.floor(c[0])) - col0, int(math.floor(c[1])) - row0)
                counts.setdefault(k, {}).setdefault(kind, 0)
                counts[k][kind] += 2
    letter = {"dark": "D", "light": "L", "pale": "P"}
    cells = {}
    for k, kinds in counts.items():
        held = [letter[kd] for kd, n in kinds.items() if n >= min_px]
        if held:
            cells[k] = held[0] if len(held) == 1 else "X"
    if not cells:
        return "no squads on the grid", {}
    c0 = min(k[0] for k in cells) - 1; c1 = max(k[0] for k in cells) + 2
    r0 = min(k[1] for k in cells) - 1; r1 = max(k[1] for k in cells) + 2
    if c1 - c0 > 120 or r1 - r0 > 80:
        return f"grid fit unreliable (span {c1 - c0} x {r1 - r0})", cells
    n = {L: sum(1 for v in cells.values() if v == L) for L in "DLPX"}
    lines = [f"cols {c0}..{c1 - 1} left->right (labels every 5), rows {r0}..{r1 - 1} far->near; squares held: "
             + ", ".join(f"{L} {v}" for L, v in n.items() if v)
             + f"; origin: {' + '.join(edges) + ' field edge' if edges else 'RELATIVE (no field edge in view)'}"
             + f"; column fit {f['col'][2]:.2f}, {len(f.get('mesh', []))} scan lines, {len(f['rows'])} row lines"]
    lab = [" "] * (c1 - c0 + 3)
    for c in range(c0, c1):
        if c % 5 == 0:
            for j, ch in enumerate(str(c)):
                lab[c - c0 + j] = ch
    lines.append("     " + "".join(lab).rstrip())
    hdr = "".join("|" if c % 5 == 0 else " " for c in range(c0, c1))
    lines.append("     " + hdr)
    for r in range(r0, r1):
        lines.append(f"{r:4d} " + "".join(cells.get((c, r), ".") for c in range(c0, c1)))
    return "\n".join(lines), cells


COLOURS = {"D": (70, 150, 255), "L": (255, 160, 40), "P": (210, 210, 200), "X": (240, 40, 40)}


def draw_board(cells, size=(420, 230), view=None, names=None):
    """A top-down minimap of a board (cells {(col, row): letter}) for the GIF panel. view = (c0, r0, c1, r1) to
    show (the same for every round of a battle, so the picture doesn't jump); names = {letter: side name}."""
    from PIL import Image, ImageDraw
    im = Image.new("RGB", size, (28, 34, 28))
    d = ImageDraw.Draw(im)
    names = names or {"D": "dark-green squares", "L": "light-green squares", "P": "pale squares", "X": "contact"}
    x = 6
    for L in "DLPX":                                # legend
        d.rectangle([x, 6, x + 8, 14], fill=COLOURS[L]); d.text((x + 11, 4), names.get(L, L), fill=(220, 220, 220))
        x += 14 + 6 * len(names.get(L, L)) + 8
    if not cells:
        return im
    if view is None:
        cs = [k[0] for k in cells]; rs = [k[1] for k in cells]
        view = (min(cs) - 3, min(rs) - 3, max(cs) + 4, max(rs) + 4)
    c0, r0, c1, r1 = view
    top = 22
    sc = min((size[0] - 10) / (c1 - c0), (size[1] - top - 14) / (r1 - r0))
    ox = 5 + ((size[0] - 10) - sc * (c1 - c0)) / 2
    d.rectangle([ox, top, ox + sc * (c1 - c0), top + sc * (r1 - r0)], outline=(90, 110, 90))
    for (c, r), L in cells.items():
        if c0 <= c < c1 and r0 <= r < r1:
            X = ox + (c - c0) * sc; Y = top + (r - r0) * sc
            d.rectangle([X, Y, X + max(1, sc - 1), Y + max(1, sc - 1)], fill=COLOURS.get(L, (255, 255, 255)))
    d.text((6, size[1] - 13), f"from above: cols {c0}-{c1 - 1}, far rows at the top", fill=(160, 170, 160))
    return im


def main(a):
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    from PIL import Image
    im = Image.open(a[1])
    f = fit(im)
    if not f:
        sys.exit("no grid fit: too few grid lines (is `g` on, is the field in view?)")
    print(f"vanishing point {f['V'][0]:.0f},{f['V'][1]:.0f}; column spacing {f['col'][0]:.1f} px at y {f['yref']:.0f} "
          f"(fit {f['col'][2]:.2f}); {len(f['rows'])} row lines; {len(f['mesh'])} scan lines; origin {origin(f)}")
    if a[0] == "check":
        print(draw(im, f, a[2] if len(a) > 2 else os.path.splitext(a[1])[0] + "_grid.png"))
    elif a[0] == "board":
        print(board(im, f)[0])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
