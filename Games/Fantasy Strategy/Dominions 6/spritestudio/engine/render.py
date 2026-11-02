"""Render one frame of a Sprite Studio model to a Dominions 6 sprite.

  python3 -I engine/render.py MODEL.json FRAME OUT.tga [--ss N]

Two looks (model["render"]["style"]):
  studio  reflective metal in a studio environment, soft shadows, ambient occlusion
          (the killbot look). Materials: chrome (color tints the reflection),
          paint (color, refl, spec, gloss), glow (flat emissive colour), flat (exactly its
          colour, no light or ink: what sprites converted from pixels use).
  cel     four painted tones with hard shadows and ink where parts overlap (the
          mad-science nation look). paint/chrome tones derive from color; glow gets
          a white-hot core.

  wire    pixel-art wireframe: a 1-pixel outline around every part, in the part's
          colour or wire_color. wire_by = "group" | "bone" | "part" picks which pieces get
          outlined; hidden = "dim" | "show" | "hide" for lines behind other pieces;
          fill = [r,g,b] paints the silhouette behind the lines (null = none); fill =
          "material" paints whatever is in front in its own colour (a sprite converted from
          pixels comes out as the original pixels), with only hidden lines drawn over it.

outline = false leaves the figure without the 1-pixel ink ring (and without inner ink).

Sprite rules: black (0,0,0) is transparent, magenta (255,0,255) is shadow, the figure
never uses either, two free rows under the feet, the unit faces left.
"""
import json
import math
import os
import sys
import time
from multiprocessing import get_all_start_methods, get_context

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw  # noqa: E402

from sdf import TAU, add, sub, mul, dot, norm, lerp, sqrt, sin, cos  # noqa: E402
from model import build_scene  # noqa: E402

DEFAULTS = {
    "studio": dict(res=[64, 64], px_per_m=34.0 / 1.88, scale=1.0, cx=None, y0=None, yaw=-30.0, pitch=9.0,
                   light=[-0.55, 0.75, 0.55], shadow=[20, 60, 46, 63], outline=[20, 18, 24], gamma=0.85,
                   ray_start=3.0, steps=220, coverage=0.42, free_rows=2),
    "cel": dict(res=[64, 64], px_per_m=34.6 / 1.73, scale=1.0, cx=None, y0=None, yaw=-30.0, pitch=8.0,
                light=[-0.65, 0.65, 0.4], shadow=[23, 60, 41, 63], outline=[30, 26, 32], gamma=1.0,
                ray_start=4.0, steps=300, coverage=0.42, free_rows=2),
}
DEFAULTS["wire"] = dict(DEFAULTS["cel"], wire_color="material", wire_by="group", hidden="dim", hidden_dim=0.42,
                        fill=None, ss=4)


def settings(model):
    r = model.get("render", {})
    s = dict(DEFAULTS[r.get("style", "studio")])
    s.update({k: v for k, v in r.items() if v is not None})
    s["style"] = r.get("style", "studio")
    w, h = s["res"]
    if s["cx"] is None:
        s["cx"] = w / 2
    if s["y0"] is None:
        s["y0"] = h - 2.4
    return s


# ---------------------------------------------------------------- per-process state
S = None          # settings
SCENE = None
MATS = []         # index -> material dict (index 0 unused)
A = DIR = VIEW = LIGHT = None
STRIPS = None


def cam_matrix(yaw, pitch):
    a, b = math.radians(yaw), math.radians(pitch)
    ry = ((cos(a), 0, sin(a)), (0, 1, 0), (-sin(a), 0, cos(a)))
    rx = ((1, 0, 0), (0, cos(b), -sin(b)), (0, sin(b), cos(b)))
    return tuple(tuple(sum(rx[i][k] * ry[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def to_model(v):
    return tuple(v[0] * A[0][j] + v[1] * A[1][j] + v[2] * A[2][j] for j in range(3))


def to_cam(v):
    return tuple(dot(A[i], v) for i in range(3))


def material_table(model):
    names = list(model["materials"])
    ids = {n: i + 1 for i, n in enumerate(names)}
    return ids, [None] + [model["materials"][n] for n in names]


def setup(model, frame_key):
    global S, SCENE, MATS, A, DIR, VIEW, LIGHT, STRIPS, PINS, K, SINGLES
    S = settings(model)
    ids, MATS = material_table(model)
    wire = S["style"] == "wire"
    if wire:                                       # surfaces are labelled by part number
        MATS = [None] + [model["materials"].get(p["mat"], {"kind": "paint", "color": [1, 0, 1]})
                         for p in model["parts"]]
    A = cam_matrix(S["yaw"], S["pitch"])
    DIR = to_model((0, 0, -1))
    VIEW = mul(DIR, -1)
    LIGHT = norm(to_model(norm(tuple(S["light"]))))
    az = math.atan2(VIEW[0], VIEW[2])
    STRIPS = (az + math.radians(80), az - math.radians(95))
    K = S["px_per_m"] * S["scale"]
    w, h = S["res"]

    def on_canvas(c, r):                           # parts wholly off the canvas are left out
        p, rr = to_cam(c), r * K + 2
        u, v = S["cx"] + p[0] * K, S["y0"] - p[1] * K
        return u + rr >= 0 and u - rr <= w and v + rr >= 0 and v - rr <= h
    if wire:
        SCENE, PINS, SINGLES = build_scene(model, frame_key, ids, per_part=True, keep=on_canvas)
    else:
        SCENE, PINS = build_scene(model, frame_key, ids, keep=on_canvas)
        SINGLES = []


# ---------------------------------------------------------------- marching
def sdf(x, y, z, groups):
    best, bm = 1e9, 0
    for g in groups:
        c = g.c
        bd = sqrt((x - c[0]) ** 2 + (y - c[1]) ** 2 + (z - c[2]) ** 2) - g.R
        if bd >= best:
            continue
        if bd > 0.02:
            best, bm = bd, 0
            continue
        d, m = g.eval(x, y, z)
        if d < best:
            best, bm = d, m
    return best, bm


def dist(p):
    return sdf(p[0], p[1], p[2], SCENE)[0]


def normal(p, e):
    n = (0.0, 0.0, 0.0)
    for v in ((1, -1, -1), (-1, -1, 1), (-1, 1, -1), (1, 1, 1)):
        n = add(n, mul(v, dist(add(p, mul(v, e)))))
    return norm(n)


def soft_shadow(p, l):
    res, t = 1.0, 0.012
    for _ in range(48):
        d = dist(add(p, mul(l, t)))
        if d < 0.0005:
            return 0.0
        res = min(res, 9.0 * d / t)
        t += max(min(d, 0.08), 0.004)
        if t > 1.4:
            break
    return max(res, 0.0)


def hard_shadow(p, l):
    t = 0.015
    for _ in range(64):
        d = dist(add(p, mul(l, t)))
        if d < 0.0006:
            return 0.0
        t += max(min(d, 0.1), 0.004)
        if t > 2.0:
            break
    return 1.0


def occlusion(p, n):
    occ, w = 0.0, 1.0
    for i in range(1, 6):
        h = 0.014 * i
        occ += (h - dist(add(p, mul(n, h)))) * w
        w *= 0.65
    return min(max(1.0 - 4.0 * occ, 0.0), 1.0)


def env(d):
    """Studio environment: sky dome, floor with a dark horizon band, key softbox and two
    vertical strip lights that give chrome its edge highlights."""
    t = d[1]
    if t >= 0:
        c = lerp((0.55, 0.57, 0.63), (0.95, 0.96, 1.0), t ** 0.6)
    elif t > -0.08:
        c = (0.12, 0.115, 0.115)
    else:
        c = lerp((0.36, 0.33, 0.31), (0.22, 0.21, 0.2), min(1.0, (-t - 0.08) * 2))
    c = add(c, mul((1.0, 0.98, 0.95), 1.5 * max(dot(d, LIGHT), 0.0) ** 24))
    if abs(t) < 0.85:
        az = math.atan2(d[0], d[2])
        for k, sa in enumerate(STRIPS):
            da = (az - sa + math.pi) % TAU - math.pi
            c = add(c, mul((1.0, 1.0, 1.0), (1.1 if k == 0 else 0.7) * math.exp(-(da / 0.16) ** 2)))
    return c


def shade_studio(p, m):
    M = MATS[m]
    kind = M["kind"]
    if kind in ("glow", "flat"):
        return tuple(M["color"])
    n = normal(p, 0.0005)
    ndv = max(dot(n, VIEW), 0.0)
    r = sub(mul(n, 2 * dot(n, VIEW)), VIEW)
    sh = soft_shadow(add(p, mul(n, 0.003)), LIGHT)
    ao = occlusion(p, n)
    ndl = max(dot(n, LIGHT), 0.0)
    spec = max(dot(r, LIGHT), 0.0)
    e = env(r)
    if kind == "chrome":
        fres = 0.8 + 0.2 * (1 - ndv) ** 5
        c = mul(e, fres * ao * (0.7 + 0.3 * sh))
        c = add(c, mul((0.9, 0.9, 0.95), 0.18 * ndl * sh))
        c = add(c, mul((1.0, 1.0, 1.0), 1.1 * sh * spec ** 70))
        tint = M["color"]
        return (c[0] * tint[0], c[1] * tint[1], c[2] * tint[2])
    c = add(mul(e, M.get("refl", 0.4) * ao), mul(tuple(M["color"]), (0.35 + 1.3 * ndl * sh) * ao))
    return add(c, mul((1.0, 1.0, 1.0), M.get("spec", 0.45) * sh * spec ** M.get("gloss", 30)))


def tones(M):
    """lit, shade, deep (0-255) for a cel material: explicit "tones" or derived from color."""
    if M.get("tones"):
        return [tuple(t) for t in M["tones"]]
    c = [v * 255 for v in M["color"]]
    return [tuple(c), tuple(v * 0.76 for v in c), tuple(v * 0.54 for v in c)]


def glow_cel(M):
    c = tuple(v * 255 for v in M["color"])
    return c, lerp(c, (255.0, 255.0, 255.0), 0.85)


def shade_cel(p, m):
    M = MATS[m]
    if M["kind"] == "flat":
        return tuple(M["color"])
    n = normal(p, 0.0006)
    if M["kind"] == "glow":
        edge, core = glow_cel(M)
        return mul(lerp(edge, core, min(1.0, max(dot(n, VIEW), 0.0) ** 2 * 1.4)), 1 / 255)
    lit, mid, deep = tones(M)
    v = max(dot(n, LIGHT), 0.0)
    if v > 0.1:
        v *= hard_shadow(add(p, mul(n, 0.004)), LIGHT)
    if v > 0.75:
        c = lerp(lit, (255, 255, 255), 0.16)
    elif v > 0.38:
        c = lit
    elif v > 0.1:
        c = mid
    else:
        c = deep
    return mul(c, 1 / 255)


def no_shade(p, m):
    return (0.0, 0.0, 0.0)


def trace(x_cam, y_cam):
    """(rgb 0-1, material, depth) for one ray; material 0 is a miss."""
    z0 = S["ray_start"]
    o = to_model((x_cam, y_cam, z0))
    cands = [g for g in SCENE if (lambda c: (c[0] - x_cam) ** 2 + (c[1] - y_cam) ** 2 <= g.R * g.R)(to_cam(g.c))]
    if not cands:
        return (0, 0, 0), 0, 1e9
    t = max(min(z0 - to_cam(g.c)[2] - g.R for g in cands), 0.0)
    tend = max(z0 - to_cam(g.c)[2] + g.R for g in cands)
    shade = {"cel": shade_cel, "wire": no_shade}.get(S["style"], shade_studio)
    for _ in range(S["steps"]):
        p = add(o, mul(DIR, t))
        d, m = sdf(p[0], p[1], p[2], cands)
        if d < 0.0004 and m:
            return shade(p, m), m, t
        t += max(d * 0.7, 0.0002)
        if t > tend:
            break
    return (0, 0, 0), 0, 1e9


def render_rows(args):
    rows, ss, w = args
    out = []
    for j in rows:
        line = []
        for i in range(w):
            u, v = (i + 0.5) / ss, (j + 0.5) / ss
            line.append(trace((u - S["cx"]) / K, (S["y0"] - v) / K))
        out.append((j, line))
    return out


def init(model, frame_key):
    setup(model, frame_key)


def workers(model, frame_key):
    """Worker pool with this frame set up in every worker. Linux forks; Windows has no fork, so
    workers start fresh and get the model passed over (SPRITESTUDIO_SPAWN=1 tests that here)."""
    fork = "fork" in get_all_start_methods() and not os.environ.get("SPRITESTUDIO_SPAWN")
    return get_context("fork" if fork else "spawn").Pool(os.cpu_count(), initializer=init, initargs=(model, frame_key))


def render_hi(model, frame_key, ss):
    w, h = S["res"]
    nx, ny = w * ss, h * ss
    jobs = [(list(range(j, min(j + 4, ny))), ss, nx) for j in range(0, ny, 4)]
    with workers(model, frame_key) as pool:
        rows = {}
        for chunk in pool.imap_unordered(render_rows, jobs):
            for j, line in chunk:
                rows[j] = line
    return [rows[j] for j in range(ny)]


def clamp8(c):
    return tuple(max(0, min(255, int(v * 255 + 0.5))) for v in c)


def is_glow(m):
    return m and MATS[m]["kind"] == "glow"


def no_ink(m):
    return MATS[m]["kind"] in ("glow", "flat")


# ---------------------------------------------------------------- sprite
def xray_part(args):
    """One part on its own: {sub-pixel index: depth} wherever its surface is hit."""
    k, ss = args
    label, g = SINGLES[k]
    w, h = S["res"]
    nx, ny = w * ss, h * ss
    z0 = S["ray_start"]
    c = to_cam(g.c)
    u0, u1 = (S["cx"] + (c[0] - g.R) * K) * ss, (S["cx"] + (c[0] + g.R) * K) * ss
    v0, v1 = (S["y0"] - (c[1] + g.R) * K) * ss, (S["y0"] - (c[1] - g.R) * K) * ss
    hits = {}
    for j in range(max(int(v0), 0), min(int(v1) + 1, ny)):
        for i in range(max(int(u0), 0), min(int(u1) + 1, nx)):
            xc, yc = ((i + 0.5) / ss - S["cx"]) / K, (S["y0"] - (j + 0.5) / ss) / K
            if (c[0] - xc) ** 2 + (c[1] - yc) ** 2 > g.R * g.R:
                continue
            o = to_model((xc, yc, z0))
            t, tend = max(z0 - c[2] - g.R, 0.0), z0 - c[2] + g.R
            for _ in range(S["steps"]):
                p = add(o, mul(DIR, t))
                d = g.eval(p[0], p[1], p[2])[0]
                if d < 0.0004:
                    hits[j * nx + i] = t
                    break
                t += max(d * 0.7, 0.0002)
                if t > tend:
                    break
    return label, hits


def segments(model):
    """Part label -> segment number; wire_by groups parts into the pieces that get outlined."""
    by = S.get("wire_by", "group")
    keys, seg = {}, [0]
    for p in model["parts"]:
        k = {"part": id(p), "bone": p["bone"]}.get(by, (p["bone"], p.get("group") or p["bone"]))
        seg.append(keys.setdefault(k, len(keys) + 1))
    return seg


def sprite_wire(model, frame_key, ss):
    """Pixel-art wireframe: a 1-pixel outline around every piece. Where two pieces touch, the
    nearer one owns the edge; outlines of pieces hidden behind others are dimmed (or shown/hidden)."""
    hi = render_hi(model, frame_key, ss)
    w, h = S["res"]
    nx = w * ss
    seg = segments(model)
    need = S["coverage"] * ss * ss
    front, fdep, fpart = [[0] * w for _ in range(h)], [[1e9] * w for _ in range(h)], [[0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            cnt, parts = {}, {}
            for j in range(ss):
                for i in range(ss):
                    _, m, dep = hi[y * ss + j][x * ss + i]
                    if m:
                        sg = seg[m]
                        cnt[sg] = cnt.get(sg, 0) + 1
                        parts[m] = parts.get(m, 0) + 1
                        if dep < fdep[y][x]:
                            fdep[y][x] = dep
            if sum(cnt.values()) >= need:
                front[y][x] = max(cnt, key=cnt.get)
                fpart[y][x] = max((m for m in parts if seg[m] == front[y][x]), key=parts.get)
            else:
                fdep[y][x] = 1e9
    nb4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
    lines = {}                                     # pixel -> (part label for colour, hidden?)
    for y in range(h):
        for x in range(w):
            sg = front[y][x]
            if not sg:
                continue
            for dx, dy in nb4:
                xx, yy = x + dx, y + dy
                other = front[yy][xx] if 0 <= xx < w and 0 <= yy < h else 0
                if other != sg and (other == 0 or fdep[y][x] <= fdep[yy][xx]):
                    lines[(x, y)] = (fpart[y][x], False)
                    break
    if S["hidden"] != "hide":                      # outlines of what is behind
        with workers(model, frame_key) as pool:
            hits = list(pool.imap_unordered(xray_part, [(k, ss) for k in range(len(SINGLES))]))
        cover, depth, best = {}, {}, {}
        for label, hp in hits:
            sg = seg[label]
            sub = cover.setdefault(sg, {})
            for idx, dep in hp.items():
                j, i = divmod(idx, nx)
                px = (i // ss, j // ss)
                sub.setdefault(px, set()).add(idx)
                if dep < depth.get((sg, px), 1e9):
                    depth[(sg, px)] = dep
            if len(hp) > best.get(sg, (0, 0))[0]:
                best[sg] = (len(hp), label)
        for sg, sub in cover.items():
            mask = {px for px, ids in sub.items() if len(ids) >= need}
            for (x, y) in mask:
                if (x, y) in lines or front[y][x] == sg:
                    continue
                if any((x + dx, y + dy) not in mask for dx, dy in nb4) and fdep[y][x] < depth[(sg, (x, y))]:
                    lines[(x, y)] = (best[sg][1], True)
    out = Image.new("RGB", (w, h), (0, 0, 0))
    o = out.load()
    if S.get("shadow"):
        sh = Image.new("L", (w, h), 0)
        ImageDraw.Draw(sh).ellipse(list(S["shadow"]), fill=255)
        shp = sh.load()
        for y in range(h):
            for x in range(w):
                if shp[x, y]:
                    o[x, y] = (255, 0, 255)
    solid = S.get("fill") == "material"
    if solid:                                      # the front surface in its own colours
        for y in range(h):
            for x in range(w):
                if front[y][x]:
                    mat = MATS[fpart[y][x]]
                    c = tuple(int(round(v * 255)) for v in mat["color"])
                    o[x, y] = c if mat["kind"] == "flat" else tuple(max(v, 10) for v in c)
                    if o[x, y] in ((0, 0, 0), (255, 0, 255)):
                        o[x, y] = (10, 10, 10) if o[x, y] == (0, 0, 0) else (254, 0, 255)
    elif S.get("fill"):
        fill = tuple(max(int(v), 10) for v in S["fill"])
        for y in range(h):
            for x in range(w):
                if front[y][x]:
                    o[x, y] = fill
    fixed = S["wire_color"] if isinstance(S["wire_color"], list) else None
    for (x, y), (label, hidden) in lines.items():
        if solid and not hidden:                   # front lines would only repaint the fill
            continue
        col = fixed or [v * 255 for v in MATS[label]["color"]]
        if not fixed and MATS[label]["kind"] != "glow":       # lift dark paints so lines read on black
            col = [max(v, 80) for v in col]
        k = S["hidden_dim"] if hidden and S["hidden"] == "dim" else 1.0
        c = tuple(max(int(v * k), 10) for v in col)
        o[x, y] = (254, c[1], c[2]) if c == (255, 0, 255) else c
    for y in range(h - S["free_rows"], h):
        for x in range(w):
            if o[x, y] not in ((0, 0, 0), (255, 0, 255)):
                o[x, y] = (255, 0, 255)
    return out


def sprite(model, frame_key, ss=None):
    setup(model, frame_key)
    ss = ss or S.get("ss", 5)
    if S["style"] == "wire":
        return sprite_wire(model, frame_key, ss)
    hi = render_hi(model, frame_key, ss)
    w, h = S["res"]
    nx, ny = w * ss, h * ss
    cel = S["style"] == "cel"
    ink = None
    if cel and S.get("outline"):      # ink only where a nearer part overlaps a clearly farther one
        offs = [(dx, dy) for dx in range(-3, 4) for dy in range(-3, 4) if 0 < dx * dx + dy * dy <= 9]
        ink = [[False] * nx for _ in range(ny)]
        for j in range(ny):
            for i in range(nx):
                c, m, dep = hi[j][i]
                if not m or no_ink(m):
                    continue
                for di, dj in offs:
                    ii, jj = i + di, j + dj
                    if 0 <= ii < nx and 0 <= jj < ny:
                        c2, m2, d2 = hi[jj][ii]
                        if m2 and not no_ink(m2) and d2 > dep + 0.07:
                            ink[j][i] = True
                            break
    INK = tuple(S["outline"]) if S.get("outline") else None
    out = Image.new("RGB", (w, h), (0, 0, 0))
    o = out.load()
    solid = [[0] * w for _ in range(h)]       # 0 empty, 1 body, else the glowing material
    col = [[None] * w for _ in range(h)]
    exact = [[False] * w for _ in range(h)]   # only flat (pixel) materials here: keep the colour as is
    gamma = S["gamma"]
    for y in range(h):
        for x in range(w):
            acc, cnt, glow, flat = [0.0, 0.0, 0.0], 0, {}, 0
            for j in range(ss):
                for i in range(ss):
                    c, m, _ = hi[y * ss + j][x * ss + i]
                    if m:
                        if ink and ink[y * ss + j][x * ss + i]:
                            c = mul(INK, 1 / 255)
                        cnt += 1
                        if is_glow(m):
                            glow[m] = glow.get(m, 0) + 1
                        flat += MATS[m]["kind"] == "flat"
                        acc[0] += c[0]; acc[1] += c[1]; acc[2] += c[2]
            if cnt / (ss * ss) >= S["coverage"]:
                gm = max(glow, key=glow.get) if glow else 0
                solid[y][x] = gm if cel and glow and glow[gm] * 2 > cnt else 1
                col[y][x] = clamp8(tuple((v / cnt) ** gamma if gamma != 1.0 else v / cnt for v in acc))
                exact[y][x] = flat == cnt and gamma == 1.0 and col[y][x] != (0, 0, 0)
    if S.get("shadow"):
        sh = Image.new("L", (w, h), 0)
        ImageDraw.Draw(sh).ellipse(list(S["shadow"]), fill=255)
        shp = sh.load()
        for y in range(h):
            for x in range(w):
                if shp[x, y]:
                    o[x, y] = (255, 0, 255)
    for y in range(h):
        for x in range(w):
            if solid[y][x]:
                r, g, b = col[y][x]
                if (r, g, b) == (255, 0, 255):
                    r = 254
                o[x, y] = (r, g, b) if exact[y][x] else (max(r, 10), max(g, 10), max(b, 12))   # never pure black
                continue
            near = [solid[y + dy][x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                    if 0 <= x + dx < w and 0 <= y + dy < h and solid[y + dy][x + dx]]
            if near and INK:
                if 1 in near or not cel:
                    o[x, y] = INK
                else:                                     # dark rim in the glow's own colour
                    e = glow_cel(MATS[near[0]])[0]
                    o[x, y] = (max(int(e[0]) // 2, 10), max(int(e[1]) // 2, 10), max(int(e[2]) // 2, 12))
    if cel and model.get("frames", {}).get(frame_key, {}).get("halo"):
        for y in range(h):
            for x in range(w):
                if o[x, y] not in ((0, 0, 0), (255, 0, 255)):
                    continue
                hit = None
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        xx, yy = x + dx, y + dy
                        if dx * dx + dy * dy <= 4 and 0 <= xx < w and 0 <= yy < h and solid[yy][xx] > 1:
                            hit = solid[yy][xx]
                            break
                    if hit:
                        break
                if hit:
                    e = glow_cel(MATS[hit])[0]
                    o[x, y] = (max(int(e[0] * 0.62), 10), max(int(e[1] * 0.62), 10), max(int(e[2] * 0.62), 12))
    for p, color in PINS:                                 # small glowing points survive the downscale
        c = to_cam(p)
        u, v = S["cx"] + c[0] * K, S["y0"] - c[1] * K
        if 0 <= int(v) < h and 0 <= int(u) < w and solid[int(v)][int(u)]:
            o[int(u), int(v)] = tuple(color)
    for y in range(h - S["free_rows"], h):                # free rows below the feet
        for x in range(w):
            if o[x, y] not in ((0, 0, 0), (255, 0, 255)):
                o[x, y] = (255, 0, 255)
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    path, frame_key, out = args
    with open(path) as f:
        model = json.load(f)
    t0 = time.time()
    img = sprite(model, frame_key, int(opts["ss"]) if "ss" in opts else None)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    img.save(out)
    if "png" in opts:
        img.save(opts["png"])
    print(json.dumps({"seconds": round(time.time() - t0, 2), "size": img.size}))


if __name__ == "__main__":
    main()
