"""Signed-distance primitives and vector maths for the sprite engine.

Primitives are copied unchanged from the killbot generator so models converted
into Sprite Studio render the same. Each primitive returns
(fn(x, y, z) -> distance, bound centre, bound radius).
"""
import math

sqrt, sin, cos = math.sqrt, math.sin, math.cos
TAU = 2 * math.pi


# ---------------------------------------------------------------- vectors
def add(a, b): return (a[0] + b[0], a[1] + b[1], a[2] + b[2])
def sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def mul(a, s): return (a[0] * s, a[1] * s, a[2] * s)
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def length(a): return sqrt(dot(a, a))
def norm(a): return mul(a, 1.0 / length(a))
def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def lerp(a, b, t): return add(a, mul(sub(b, a), t))
def mirror(p): return (-p[0], p[1], p[2])


def basis(fwd, up=(0, 1, 0)):
    ez = norm(fwd)
    ex = norm(cross(up, ez))
    return (ex, cross(ez, ex), ez)


def yaw_basis(deg):
    a = math.radians(deg)
    return basis((sin(a), 0, cos(a)))


# ---------------------------------------------------------------- primitives

# each returns (fn(x, y, z) -> distance, bound centre, bound radius)
def sphere(c, r):
    cx, cy, cz = c
    return (lambda x, y, z: sqrt((x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2) - r), c, r


def capsule(a, b, r):
    ax, ay, az = a
    bx, by, bz = sub(b, a)
    inv = 1.0 / (bx * bx + by * by + bz * bz)

    def f(x, y, z):
        px, py, pz = x - ax, y - ay, z - az
        h = (px * bx + py * by + pz * bz) * inv
        h = 0.0 if h < 0 else (1.0 if h > 1 else h)
        px -= bx * h; py -= by * h; pz -= bz * h
        return sqrt(px * px + py * py + pz * pz) - r
    return f, lerp(a, b, 0.5), length(sub(b, a)) / 2 + r


def roundcone(a, b, r1, r2):
    ax, ay, az = a
    bx, by, bz = sub(b, a)
    l2 = bx * bx + by * by + bz * bz
    rr = r1 - r2
    a2 = l2 - rr * rr
    il2 = 1.0 / l2
    srr = 1.0 if rr >= 0 else -1.0

    def f(x, y, z):
        px, py, pz = x - ax, y - ay, z - az
        yy = px * bx + py * by + pz * bz
        zz = yy - l2
        qx, qy, qz = px * l2 - bx * yy, py * l2 - by * yy, pz * l2 - bz * yy
        x2 = qx * qx + qy * qy + qz * qz
        y2 = yy * yy * l2
        z2 = zz * zz * l2
        k = srr * rr * rr * x2
        if (1 if zz > 0 else -1) * a2 * z2 > k:
            return sqrt(x2 + z2) * il2 - r2
        if (1 if yy > 0 else -1) * a2 * y2 < k:
            return sqrt(x2 + y2) * il2 - r1
        return (sqrt(x2 * a2 * il2) + yy * rr) * il2 - r1
    return f, lerp(a, b, 0.5), length(sub(b, a)) / 2 + max(r1, r2)


def ellipsoid(c, r):
    cx, cy, cz = c
    rx, ry, rz = r

    def f(x, y, z):
        px, py, pz = x - cx, y - cy, z - cz
        k0 = sqrt((px / rx) ** 2 + (py / ry) ** 2 + (pz / rz) ** 2)
        k1 = sqrt((px / (rx * rx)) ** 2 + (py / (ry * ry)) ** 2 + (pz / (rz * rz)) ** 2)
        if k1 < 1e-9:
            return -min(r)
        return k0 * (k0 - 1.0) / k1
    return f, c, max(r)


def box(c, half, bas=((1, 0, 0), (0, 1, 0), (0, 0, 1)), rnd=0.0):
    cx, cy, cz = c
    (e0, e1, e2) = bas
    hx, hy, hz = half

    def f(x, y, z):
        px, py, pz = x - cx, y - cy, z - cz
        qx = abs(px * e0[0] + py * e0[1] + pz * e0[2]) - hx
        qy = abs(px * e1[0] + py * e1[1] + pz * e1[2]) - hy
        qz = abs(px * e2[0] + py * e2[1] + pz * e2[2]) - hz
        ox, oy, oz = max(qx, 0.0), max(qy, 0.0), max(qz, 0.0)
        return sqrt(ox * ox + oy * oy + oz * oz) + min(max(qx, qy, qz), 0.0) - rnd
    return f, c, length(half) + rnd


def grooves(prim, origin, axis, period, amp, lo=-1e9, hi=1e9):
    """Cut periodic rings (ribs, fins, teeth) across `axis` between lo and hi."""
    f, c, r = prim
    ox, oy, oz = origin
    ux, uy, uz = norm(axis)
    w = TAU / period

    def g(x, y, z):
        t = (x - ox) * ux + (y - oy) * uy + (z - oz) * uz
        d = f(x, y, z)
        if lo < t < hi:
            d += amp * (0.5 + 0.5 * sin(w * t))
        return d
    return g, c, r + amp




def torus(c, n, R, r):
    """Ring of radius R and tube radius r around axis n."""
    cx, cy, cz = c
    nx, ny, nz = norm(n)

    def f(x, y, z):
        qx, qy, qz = x - cx, y - cy, z - cz
        h = qx * nx + qy * ny + qz * nz
        rx, ry, rz = qx - nx * h, qy - ny * h, qz - nz * h
        return sqrt((sqrt(rx * rx + ry * ry + rz * rz) - R) ** 2 + h * h) - r
    return f, c, R + r


def disc(c, axis, r, thick, rnd=0.003):
    """Flat rounded cylinder: radius r, thickness thick along axis."""
    ax, ay, az = norm(axis)
    cx, cy, cz = c
    rr, hh = r - rnd, max(thick / 2 - rnd, 0.0005)

    def f(x, y, z):
        px, py, pz = x - cx, y - cy, z - cz
        h = px * ax + py * ay + pz * az
        qx, qy, qz = px - ax * h, py - ay * h, pz - az * h
        dx, dy = sqrt(qx * qx + qy * qy + qz * qz) - rr, abs(h) - hh
        return min(max(dx, dy), 0.0) + sqrt(max(dx, 0.0) ** 2 + max(dy, 0.0) ** 2) - rnd
    return f, c, r + thick


def ik(root, target, l1, l2, pole):
    """Two-bone IK: returns (middle joint, reached end)."""
    d = sub(target, root)
    dist = min(length(d), l1 + l2 - 1e-4)
    dn = norm(d)
    a = (l1 * l1 + dist * dist - l2 * l2) / (2 * dist)
    h = sqrt(max(l1 * l1 - a * a, 0.0))
    pp = norm(sub(pole, mul(dn, dot(pole, dn))))
    return add(add(root, mul(dn, a)), mul(pp, h)), add(root, mul(dn, dist))


# ---------------------------------------------------------------- Sprite Studio shapes
def _local(c, bas):
    """Coordinates in a part's own axes (rows of bas)."""
    cx, cy, cz = c
    (e0, e1, e2) = bas

    def to(x, y, z):
        px, py, pz = x - cx, y - cy, z - cz
        return (px * e0[0] + py * e0[1] + pz * e0[2], px * e1[0] + py * e1[1] + pz * e1[2],
                px * e2[0] + py * e2[1] + pz * e2[2])
    return to


def _slab2(dx, dy):
    """Distance from 2D (radial, height) offsets past a flat-capped profile."""
    return min(max(dx, dy), 0.0) + sqrt(max(dx, 0.0) ** 2 + max(dy, 0.0) ** 2)


def _axial(a, b):
    """Centre, unit axis and half length of the segment a-b."""
    c = mul(add(a, b), 0.5)
    d = sub(b, a)
    L = length(d)
    return c, (mul(d, 1.0 / L) if L > 1e-9 else (0.0, 1.0, 0.0)), L / 2


def cylinder(a, b, r, rnd=0.004):
    """Flat-ended cylinder from a to b, edges rounded by rnd."""
    c, (ax, ay, az), hh = _axial(a, b)
    cx, cy, cz = c
    rnd = min(rnd, r * 0.9, hh * 0.9)
    rr, h2 = r - rnd, hh - rnd

    def f(x, y, z):
        px, py, pz = x - cx, y - cy, z - cz
        h = px * ax + py * ay + pz * az
        qx, qy, qz = px - ax * h, py - ay * h, pz - az * h
        return _slab2(sqrt(qx * qx + qy * qy + qz * qz) - rr, abs(h) - h2) - rnd
    return f, c, sqrt(r * r + hh * hh)


def cone(a, b, r1, r2):
    """Cone or truncated cone: radius r1 at a, r2 at b (0 = pointed)."""
    ax, ay, az = a
    bax, bay, baz = sub(b, a)
    baba = bax * bax + bay * bay + baz * baz
    rba = r2 - r1
    k = rba * rba + baba

    def f(x, y, z):
        px, py, pz = x - ax, y - ay, z - az
        papa = px * px + py * py + pz * pz
        paba = (px * bax + py * bay + pz * baz) / baba
        xx = sqrt(max(papa - paba * paba * baba, 0.0))
        cax = max(0.0, xx - (r1 if paba < 0.5 else r2))
        cay = abs(paba - 0.5) - 0.5
        t = min(max((rba * (xx - r1) + paba * baba) / k, 0.0), 1.0)
        cbx, cby = xx - r1 - t * rba, paba - t
        s = -1.0 if (cbx < 0.0 and cay < 0.0) else 1.0
        return s * sqrt(min(cax * cax + cay * cay * baba, cbx * cbx + cby * cby * baba))
    c = mul(add(a, b), 0.5)
    return f, c, sqrt(max(r1, r2) ** 2 + baba / 4)


def tube(a, b, r, wall):
    """Hollow pipe from a to b: outer radius r, wall thickness wall."""
    c, (ax, ay, az), hh = _axial(a, b)
    cx, cy, cz = c
    wall = min(wall, r)
    mid, hw = r - wall / 2, wall / 2

    def f(x, y, z):
        px, py, pz = x - cx, y - cy, z - cz
        h = px * ax + py * ay + pz * az
        qx, qy, qz = px - ax * h, py - ay * h, pz - az * h
        return _slab2(abs(sqrt(qx * qx + qy * qy + qz * qz) - mid) - hw, abs(h) - hh)
    return f, c, sqrt(r * r + hh * hh)


def dome(c, axis, r):
    """Half sphere: flat side at c, bulging along axis."""
    cx, cy, cz = c
    ax, ay, az = norm(axis)

    def f(x, y, z):
        px, py, pz = x - cx, y - cy, z - cz
        return max(sqrt(px * px + py * py + pz * pz) - r, -(px * ax + py * ay + pz * az))
    return f, c, r


def wedge(c, half, bas):
    """Ramp: a box with its top front edge cut away (full height at the back, -z)."""
    to = _local(c, bas)
    hx, hy, hz = half
    n = sqrt(hz * hz + hy * hy)
    ny, nz = hz / n, hy / n

    def f(x, y, z):
        lx, ly, lz = to(x, y, z)
        qx, qy, qz = abs(lx) - hx, abs(ly) - hy, abs(lz) - hz
        b = sqrt(max(qx, 0.0) ** 2 + max(qy, 0.0) ** 2 + max(qz, 0.0) ** 2) + min(max(qx, qy, qz), 0.0)
        return max(b, ly * ny + lz * nz)
    return f, c, length(half)


def pyramid(c, half, bas):
    """Square pyramid: base 2hx by 2hz at -hy, point at +hy."""
    to = _local(c, bas)
    hx, hy, hz = half
    nx, nz = sqrt(4 * hy * hy + hx * hx), sqrt(4 * hy * hy + hz * hz)

    def f(x, y, z):
        lx, ly, lz = to(x, y, z)
        return max((2 * hy * abs(lx) + hx * ly - hx * hy) / nx,
                   (2 * hy * abs(lz) + hz * ly - hz * hy) / nz, -ly - hy)
    return f, c, length(half)


def hexprism(c, r, thick, bas):
    """Six-sided prism (a nut or bolt head): corner radius r, thickness along its own y."""
    to = _local(c, bas)
    ap, hh = r * sqrt(3) / 2, thick / 2

    def f(x, y, z):
        lx, ly, lz = to(x, y, z)
        d2 = max(abs(lx), abs(0.5 * lx + 0.8660254 * lz), abs(0.5 * lx - 0.8660254 * lz)) - ap
        return _slab2(d2, abs(ly) - hh)
    return f, c, sqrt(r * r + hh * hh)


def make_prim(p):
    """A part record from a model file -> primitive."""
    t = p["type"]
    if t == "sphere":
        prim = sphere(tuple(p["c"]), p["r"])
    elif t == "capsule":
        prim = capsule(tuple(p["a"]), tuple(p["b"]), p["r"])
    elif t == "roundcone":
        prim = roundcone(tuple(p["a"]), tuple(p["b"]), p["r1"], p["r2"])
    elif t == "ellipsoid":
        prim = ellipsoid(tuple(p["c"]), tuple(p["r"]))
        if p.get("basis"):                      # turned ellipsoid: evaluate in its own axes
            f, c, rad = prim
            (e0, e1, e2), (cx, cy, cz) = p["basis"], c

            def fe(x, y, z, f=f, e0=e0, e1=e1, e2=e2):
                px, py, pz = x - cx, y - cy, z - cz
                return f(cx + px * e0[0] + py * e0[1] + pz * e0[2], cy + px * e1[0] + py * e1[1] + pz * e1[2],
                         cz + px * e2[0] + py * e2[1] + pz * e2[2])
            prim = fe, c, rad
    elif t == "box":
        bas = tuple(tuple(v) for v in p["basis"]) if p.get("basis") else ((1, 0, 0), (0, 1, 0), (0, 0, 1))
        prim = box(tuple(p["c"]), tuple(p["half"]), bas, p.get("rnd", 0.0))
    elif t == "torus":
        prim = torus(tuple(p["c"]), tuple(p["n"]), p["R"], p["r"])
    elif t == "disc":
        prim = disc(tuple(p["c"]), tuple(p["axis"]), p["r"], p["thick"], p.get("rnd", 0.003))
    elif t == "cylinder":
        prim = cylinder(tuple(p["a"]), tuple(p["b"]), p["r"], p.get("rnd", 0.004))
    elif t == "cone":
        prim = cone(tuple(p["a"]), tuple(p["b"]), p["r1"], p["r2"])
    elif t == "tube":
        prim = tube(tuple(p["a"]), tuple(p["b"]), p["r"], p["wall"])
    elif t == "dome":
        prim = dome(tuple(p["c"]), tuple(p["axis"]), p["r"])
    elif t in ("wedge", "pyramid", "hexprism"):
        bas = tuple(tuple(v) for v in p["basis"]) if p.get("basis") else ((1, 0, 0), (0, 1, 0), (0, 0, 1))
        if t == "hexprism":
            prim = hexprism(tuple(p["c"]), p["r"], p["thick"], bas)
        else:
            prim = (wedge if t == "wedge" else pyramid)(tuple(p["c"]), tuple(p["half"]), bas)
    else:
        raise ValueError(f"unknown part type {t!r}")
    gr = p.get("grooves")
    if gr:
        prim = grooves(prim, tuple(gr["origin"]), tuple(gr["axis"]), gr["period"], gr["amp"],
                       gr.get("lo", -1e9), gr.get("hi", 1e9))
    return prim
