"""Terminator-style endoskeleton killbot, rendered with a small SDF ray marcher,
then exported as Dominions 6 sprites (64x64 24-bit TGA, black = transparent,
magenta = shadow) plus a full-size picture.

Model space is metres: y up, x = robot's left, z = robot's front, feet at y=0.
The figure is 1.88 m tall with human proportions (head ~1/7.5 of height).

usage: python3 killbot3d.py OUTDIR
"""
import math
import os
import sys
from multiprocessing import Pool

from PIL import Image, ImageChops, ImageDraw, ImageFilter

sqrt, sin, cos = math.sqrt, math.sin, math.cos
TAU = 2 * math.pi

# materials
CHROME, DARK, EYE, GUNMETAL, GLOW, BOLT = 1, 2, 3, 4, 5, 6


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


# ---------------------------------------------------------------- groups
class Group:
    def __init__(self, name):
        self.name = name
        self.ops = []

    def add(self, prim, mat=CHROME):
        self.ops.append((0, prim, mat))

    def cut(self, prim, mat=DARK):
        self.ops.append((1, prim, mat))

    def finish(self):
        adds = [p for k, p, m in self.ops if k == 0]
        c = mul(sum_v([p[1] for p in adds]), 1.0 / len(adds))
        self.c = c
        self.R = max(length(sub(p[1], c)) + p[2] for p in adds) + 0.01
        self.fns = [(k, p[0], m) for k, p, m in self.ops]

    def eval(self, x, y, z):
        d, m = 1e9, 0
        for kind, fn, mat in self.fns:
            v = fn(x, y, z)
            if kind == 0:
                if v < d:
                    d, m = v, mat
            elif -v > d:
                d, m = -v, mat
        return d, m


def sum_v(vs):
    s = (0.0, 0.0, 0.0)
    for v in vs:
        s = add(s, v)
    return s


def ik(root, target, l1, l2, pole):
    d = sub(target, root)
    dist = min(length(d), l1 + l2 - 1e-4)
    dn = norm(d)
    a = (l1 * l1 + dist * dist - l2 * l2) / (2 * dist)
    h = sqrt(max(l1 * l1 - a * a, 0.0))
    pp = norm(sub(pole, mul(dn, dot(pole, dn))))
    return add(add(root, mul(dn, a)), mul(pp, h)), add(root, mul(dn, dist))


def front_side(d):
    """Unit vectors perpendicular to limb direction d: toward the front (+z) and to the robot's left."""
    fr = norm(sub((0, 0, 1), mul(d, d[2])))
    return fr, norm(cross(fr, d))


def perp(d, hint):
    n1 = norm(cross(d, hint))
    return n1, norm(cross(n1, d))


# ---------------------------------------------------------------- the model
def build(firing):
    G = []

    # --- head: chrome skull, red eyes ---
    h = Group("head")
    h.add(ellipsoid((0, 1.792, -0.012), (0.076, 0.096, 0.098)))
    h.add(capsule((-0.056, 1.794, 0.066), (0.056, 1.794, 0.066), 0.016))      # brow ridge
    for s in (1, -1):
        h.add(capsule((0.067 * s, 1.748, 0.028), (0.042 * s, 1.741, 0.072), 0.013))  # cheekbone
        h.add(capsule((0.062 * s, 1.725, -0.004), (0.046 * s, 1.676, 0.032), 0.012))  # jaw ramus
    h.add(box((0, 1.718, 0.054), (0.03, 0.017, 0.03), rnd=0.009))              # maxilla
    h.add(roundcone((0, 1.676, 0.012), (0, 1.672, 0.068), 0.036, 0.022))        # mandible
    for s in (1, -1):
        h.cut(sphere((0.033 * s, 1.768, 0.086), 0.024))                         # eye socket
    h.cut(box((0, 1.741, 0.086), (0.008, 0.012, 0.02)))                         # nasal cavity
    h.cut(box((0, 1.697, 0.07), (0.034, 0.006, 0.03)))                          # mouth gap
    for s in (1, -1):
        h.add(sphere((0.033 * s, 1.767, 0.062), 0.013), EYE)
        h.add(capsule((0.072 * s, 1.752, -0.012), (0.058 * s, 1.692, 0.006), 0.01), DARK)
    for y in (1.706, 1.688):                                                    # teeth rows
        h.add(grooves(box((0, y, 0.071), (0.029, 0.006, 0.01), rnd=0.003),
                      (0, 0, 0), (1, 0, 0), 0.0105, 0.004), CHROME)
    G.append(h)

    # --- neck ---
    n = Group("neck")
    n.add(grooves(capsule((0, 1.57, -0.03), (0, 1.70, -0.025), 0.024),
                  (0, 0, 0), (0, 1, 0), 0.022, 0.006), DARK)
    for s in (1, -1):
        n.add(capsule((0.02 * s, 1.57, 0.012), (0.018 * s, 1.69, 0.022), 0.009), DARK)
        n.add(capsule((0.05 * s, 1.55, 0.004), (0.046 * s, 1.70, -0.012), 0.012))
    G.append(n)

    # --- torso: ribcage, pectoral plates, clavicles, shoulders ---
    t = Group("torso")
    t.add(grooves(ellipsoid((0, 1.37, 0.0), (0.162, 0.19, 0.118)),
                  (0, 0, 0), (0, 1, 0), 0.036, 0.009, 1.20, 1.43))
    t.add(ellipsoid((0, 1.33, -0.01), (0.14, 0.17, 0.10)), DARK)               # inner core
    for s in (1, -1):
        t.add(capsule((0.03 * s, 1.566, 0.044), (0.17 * s, 1.566, 0.0), 0.019))  # clavicle
        t.add(sphere((0.205 * s, 1.52, -0.005), 0.05), DARK)                    # shoulder joint
        t.add(ellipsoid((0.218 * s, 1.548, 0.0), (0.06, 0.048, 0.066)))         # deltoid cap
    t.add(grooves(ellipsoid((0, 1.462, 0.072), (0.15, 0.058, 0.036)),
                  (0, 0, 0), (0, 1, 0), 0.03, 0.005))                           # breastplate
    t.add(capsule((0, 1.50, 0.108), (0, 1.29, 0.104), 0.016))                   # sternum
    G.append(t)

    # --- abdomen: spine, hydraulics, cables ---
    a = Group("abdomen")
    a.add(grooves(capsule((0, 1.04, -0.04), (0, 1.24, -0.04), 0.035),
                  (0, 0, 0), (0, 1, 0), 0.03, 0.008), DARK)
    for s in (1, -1):
        a.add(capsule((0.08 * s, 1.25, 0.03), (0.075 * s, 1.03, 0.03), 0.017))
        a.add(capsule((0.08 * s, 1.25, 0.03), (0.078 * s, 1.15, 0.03), 0.024), DARK)
        a.add(capsule((0.036 * s, 1.25, 0.062), (0.036 * s, 1.05, 0.052), 0.0095), DARK)
    G.append(a)

    # --- pelvis ---
    p = Group("pelvis")
    p.add(box((0, 0.985, -0.01), (0.085, 0.03, 0.055), rnd=0.028))
    p.add(box((0, 0.925, 0.025), (0.03, 0.04, 0.04), rnd=0.02))
    for s in (1, -1):
        p.add(ellipsoid((0.11 * s, 1.005, -0.005), (0.05, 0.05, 0.068)))      # ilium
        p.add(sphere((0.10 * s, 0.95, 0.0), 0.05), DARK)
    G.append(p)

    # --- legs ---
    for s, ankle, splay in ((1, (0.19, 0.085, 0.13), 16), (-1, (-0.17, 0.085, -0.11), -8)):
        hip = (0.10 * s, 0.95, 0.0)
        knee, ankle = ik(hip, ankle, 0.45, 0.44, (0.15 * s, 0, 1))
        th = Group("thigh")
        d = norm(sub(knee, hip))
        fr, n1 = front_side(d)
        th.add(roundcone(hip, knee, 0.078, 0.056))
        th.add(capsule(add(add(hip, mul(fr, 0.066)), mul(d, 0.08)),
                       add(knee, mul(fr, 0.058)), 0.022))
        th.add(capsule(add(add(hip, mul(fr, -0.062)), mul(d, 0.1)),
                       add(knee, mul(fr, -0.05)), 0.022))
        th.add(capsule(add(add(hip, mul(n1, 0.07 * s)), mul(d, 0.12)),
                       add(knee, mul(n1, 0.05 * s)), 0.02))
        G.append(th)
        sh = Group("shin")
        d = norm(sub(ankle, knee))
        fr, n1 = front_side(d)
        sh.add(sphere(knee, 0.06), DARK)
        sh.add(ellipsoid(add(knee, mul(fr, 0.055)), (0.046, 0.052, 0.026)))      # kneecap
        sh.add(roundcone(knee, ankle, 0.055, 0.037))
        sh.add(capsule(add(add(knee, mul(fr, -0.06)), mul(d, 0.04)),
                       add(ankle, mul(fr, -0.034)), 0.024))                # calf piston
        sh.add(sphere(ankle, 0.038), DARK)
        fb = yaw_basis(splay)
        fwd = fb[2]
        sh.add(box((ankle[0] + fwd[0] * 0.06, 0.05, ankle[2] + fwd[2] * 0.06),
                   (0.042, 0.035, 0.105), fb, rnd=0.015))
        sh.add(grooves(box((ankle[0] + fwd[0] * 0.19, 0.032, ankle[2] + fwd[2] * 0.19),
                           (0.042, 0.022, 0.035), fb, rnd=0.01),
                       ankle, fb[0], 0.022, 0.006))                             # toes
        G.append(sh)

    # --- plasma rifle, held at the right hip, fore-grip in the left hand ---
    gb = basis((-0.22, 0.0, 1.0))
    go = (-0.12, 1.16, 0.13)

    def gl(x, y, z):
        return add(go, add(add(mul(gb[0], x), mul(gb[1], y)), mul(gb[2], z)))

    g = Group("gun")
    g.add(box(gl(0, 0.035, 0.12), (0.028, 0.042, 0.2), gb, rnd=0.01), GUNMETAL)  # receiver
    g.add(box(gl(0, 0.09, 0.15), (0.02, 0.014, 0.17), gb, rnd=0.008), DARK)     # top shroud
    g.add(box(gl(0, 0.118, 0.09), (0.011, 0.012, 0.05), gb, rnd=0.004), DARK)   # sight
    g.add(grooves(roundcone(gl(0, 0.03, 0.32), gl(0, 0.03, 0.50), 0.031, 0.026),
                  go, gb[2], 0.016, 0.006), GUNMETAL)                           # heat fins
    g.add(capsule(gl(0, 0.03, 0.32), gl(0, 0.03, 0.64), 0.016), DARK)           # barrel
    g.add(capsule(gl(0, 0.03, 0.62), gl(0, 0.03, 0.665), 0.022), GUNMETAL)      # muzzle
    for z in (0.0, 0.065, 0.13):
        g.add(box(gl(0.03, 0.035, z), (0.004, 0.02, 0.022), gb, rnd=0.002), GLOW)  # cells
    tilt = basis(add(gb[2], mul(gb[1], 0.3)), gb[1])
    g.add(box(gl(0, -0.06, -0.01), (0.017, 0.055, 0.022), (gb[0], norm(sub(gb[1], mul(gb[2], 0.3))), tilt[2]), rnd=0.008), DARK)
    g.add(box(gl(0, -0.05, 0.17), (0.015, 0.045, 0.018), gb, rnd=0.008), DARK)  # fore-grip
    g.add(box(gl(0, -0.045, 0.27), (0.02, 0.035, 0.035), gb, rnd=0.006), GUNMETAL)  # power cell
    g.add(box(gl(0, 0.0, -0.2), (0.02, 0.038, 0.11), gb, rnd=0.012), GUNMETAL)  # stock
    G.append(g)
    if firing:
        b = Group("bolt")
        b.add(capsule(gl(0, 0.03, 0.72), gl(0, 0.03, 1.02), 0.026), BOLT)
        b.add(sphere(gl(0, 0.03, 0.68), 0.045), BOLT)
        G.append(b)

    # --- hands wrapped around the grips ---
    hands = []
    for side, gz, wrist_l in ((-1, 0.0, (-0.026, 0.0, -0.058)), (1, 0.17, (0.032, 0.0, 0.12))):
        hd = Group("hand")
        hd.add(box(gl(0.028 * side, -0.045, gz - 0.004), (0.011, 0.04, 0.03), gb, rnd=0.008))
        front = gz + 0.03
        for y in (-0.014, -0.037, -0.06, -0.082):
            hd.add(capsule(gl(0.026 * side, y, front), gl(-0.02 * side, y, front + 0.002), 0.0105))
            hd.add(capsule(gl(-0.02 * side, y, front + 0.002), gl(-0.026 * side, y, gz - 0.006), 0.0095), DARK)
        hd.add(capsule(gl(0.02 * side, 0.012, gz - 0.022), gl(-0.02 * side, 0.016, gz + 0.016), 0.0095))
        wrist = gl(*wrist_l)
        hd.add(capsule(wrist, gl(0.028 * side, -0.03, gz - 0.01), 0.019), DARK)
        G.append(hd)
        hands.append(wrist)

    # --- arms, solved to reach the wrists ---
    for s, wrist, pole in ((-1, hands[0], (-1.0, -0.5, -0.25)), (1, hands[1], (0.5, -0.8, 0.1))):
        sh = (0.205 * s, 1.52, -0.005)
        elbow, reach = ik(sh, wrist, 0.34, 0.28, pole)
        gap = length(sub(reach, wrist))
        if gap > 0.005:
            print(f"warning: arm {s} misses wrist by {gap:.3f} m", file=sys.stderr)
        ua = Group("upperarm")
        d = norm(sub(elbow, sh))
        n1, n2 = perp(d, pole)
        ua.add(roundcone(sh, elbow, 0.058, 0.044))
        ua.add(capsule(add(add(sh, mul(n2, -0.055)), mul(d, 0.07)),
                       add(add(elbow, mul(n2, -0.04)), mul(d, -0.04)), 0.022))   # bicep
        ua.add(capsule(add(add(sh, mul(n2, 0.052)), mul(d, 0.09)),
                       add(add(elbow, mul(n2, 0.038)), mul(d, -0.03)), 0.02))    # tricep
        G.append(ua)
        fa = Group("forearm")
        d = norm(sub(wrist, elbow))
        n1, n2 = perp(d, pole)
        fa.add(sphere(elbow, 0.05), DARK)
        fa.add(roundcone(elbow, lerp(elbow, wrist, 0.62), 0.052, 0.036))
        for k in (1, -1):
            fa.add(capsule(add(elbow, mul(n1, 0.022 * k)), add(wrist, mul(n1, 0.016 * k)), 0.0135), DARK)
        fa.add(sphere(wrist, 0.026), DARK)
        G.append(fa)

    for grp in G:
        grp.finish()
    return G


# ---------------------------------------------------------------- camera
YAW, PITCH = -30.0, 9.0
K = 34.0 / 1.88          # sprite pixels per metre
CX, Y0 = 33.5, 61.6      # sprite position of the model origin (between the feet)


def cam_matrix():
    a, b = math.radians(YAW), math.radians(PITCH)
    ry = ((cos(a), 0, sin(a)), (0, 1, 0), (-sin(a), 0, cos(a)))
    rx = ((1, 0, 0), (0, cos(b), -sin(b)), (0, sin(b), cos(b)))
    return tuple(tuple(sum(rx[i][k] * ry[k][j] for k in range(3)) for j in range(3)) for i in range(3))


A = cam_matrix()          # p_model = p_cam @ A, p_cam = A @ p_model


def to_model(v):
    return tuple(v[0] * A[0][j] + v[1] * A[1][j] + v[2] * A[2][j] for j in range(3))


def to_cam(v):
    return tuple(dot(A[i], v) for i in range(3))


def to_screen(v):
    c = to_cam(v)
    return CX + c[0] * K, Y0 - c[1] * K


DIR = to_model((0, 0, -1))
VIEW = mul(DIR, -1)
LIGHT = norm(to_model(norm((-0.55, 0.75, 0.55))))
RIM = norm(to_model(norm((0.8, 0.15, -0.6))))

SCENE = None
GROUND = False
RIM_ON = False


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


def normal(p):
    e = 0.0005
    k = ((1, -1, -1), (-1, -1, 1), (-1, 1, -1), (1, 1, 1))
    n = (0.0, 0.0, 0.0)
    for v in k:
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


def occlusion(p, n):
    occ, w = 0.0, 1.0
    for i in range(1, 6):
        h = 0.014 * i
        occ += (h - dist(add(p, mul(n, h)))) * w
        w *= 0.65
    return min(max(1.0 - 4.0 * occ, 0.0), 1.0)


VIEW_AZ = math.atan2(VIEW[0], VIEW[2])
STRIPS = (VIEW_AZ + math.radians(80), VIEW_AZ - math.radians(95))


def env(d):
    """Studio environment: sky dome, floor with a dark horizon band, key softbox
    and two vertical strip lights to the sides that give chrome its edge highlights."""
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
    if RIM_ON:
        c = add(c, mul((1.0, 0.33, 0.1), 0.9 * max(dot(d, RIM), 0.0) ** 6))
    return c


def shade(p, mat):
    if mat == EYE:
        return (1.0, 0.16, 0.08), True
    if mat in (GLOW, BOLT):
        return (0.45, 0.88, 1.0) if mat == GLOW else (0.75, 0.95, 1.0), True
    n = normal(p)
    ndv = max(dot(n, VIEW), 0.0)
    r = sub(mul(n, 2 * dot(n, VIEW)), VIEW)
    sh = soft_shadow(add(p, mul(n, 0.003)), LIGHT)
    ao = occlusion(p, n)
    ndl = max(dot(n, LIGHT), 0.0)
    spec = max(dot(r, LIGHT), 0.0)
    e = env(r)
    if mat == CHROME:
        fres = 0.8 + 0.2 * (1 - ndv) ** 5
        c = mul(e, fres * ao * (0.7 + 0.3 * sh))
        c = add(c, mul((0.9, 0.9, 0.95), 0.18 * ndl * sh))
        c = add(c, mul((1.0, 1.0, 1.0), 1.1 * sh * spec ** 70))
        c = (c[0] * 0.95, c[1] * 0.97, c[2])
    else:
        base = (0.30, 0.30, 0.32) if mat == DARK else (0.24, 0.25, 0.29)
        refl = 0.42 if mat == DARK else 0.38
        c = add(mul(e, refl * ao), mul(base, (0.35 + 1.3 * ndl * sh) * ao))
        c = add(c, mul((1.0, 1.0, 1.0), 0.45 * sh * spec ** 30))
    return c, False


def trace(x_cam, y_cam):
    """Returns (rgb, hit_kind, emissive) for one ray; hit_kind 0 miss, 1 robot, 2 ground."""
    o = to_model((x_cam, y_cam, 3.0))
    cands = []
    for g in SCENE:
        c = to_cam(g.c)
        if (c[0] - x_cam) ** 2 + (c[1] - y_cam) ** 2 <= g.R * g.R:
            cands.append(g)
    tmax = 6.0
    tg = None
    if GROUND and DIR[1] < 0:
        tg = -o[1] / DIR[1]
        tmax = tg
    if cands:
        t = min(3.0 - to_cam(g.c)[2] - g.R for g in cands)
        t = max(t, 0.0)
        tend = min(tmax, max(3.0 - to_cam(g.c)[2] + g.R for g in cands))
        for _ in range(220):
            p = add(o, mul(DIR, t))
            d, m = sdf(p[0], p[1], p[2], cands)
            if d < 0.0004 and m:
                c, em = shade(p, m)
                return c, 1, em
            t += max(d * 0.7, 0.0002)
            if t > tend:
                break
    if tg is not None:
        p = add(o, mul(DIR, tg))
        sh = soft_shadow(add(p, (0, 0.002, 0)), LIGHT)
        base = mul((0.16, 0.11, 0.09), 0.35 + 0.65 * sh)
        return base, 2, False
    return (0, 0, 0), 0, False


def render_rows(args):
    rows, u0, v0, scale, w = args
    out = []
    for j in rows:
        line = []
        for i in range(w):
            u = u0 + (i + 0.5) / scale
            v = v0 + (j + 0.5) / scale
            line.append(trace((u - CX) / K, (Y0 - v) / K))
        out.append((j, line))
    return out


def init(firing, ground, rim):
    global SCENE, GROUND, RIM_ON
    SCENE = build(firing)
    GROUND, RIM_ON = ground, rim


def render(firing, ground, rim, u0, v0, span, res):
    scale = res / span
    jobs = [(list(range(j, min(j + 4, res))), u0, v0, scale, res) for j in range(0, res, 4)]
    with Pool(os.cpu_count(), initializer=init, initargs=(firing, ground, rim)) as pool:
        rows = {}
        for chunk in pool.imap_unordered(render_rows, jobs):
            for j, line in chunk:
                rows[j] = line
    return [rows[j] for j in range(res)]


def clamp8(c):
    return tuple(max(0, min(255, int(v * 255 + 0.5))) for v in c)


# ---------------------------------------------------------------- outputs
def sprite(firing, ss=5):
    rows = render(firing, False, False, 0, 0, 64, 64 * ss)
    out = Image.new("RGB", (64, 64), (0, 0, 0))
    o = out.load()
    solid = [[False] * 64 for _ in range(64)]
    col = [[None] * 64 for _ in range(64)]
    for y in range(64):
        for x in range(64):
            acc, n = [0.0, 0.0, 0.0], 0
            for j in range(ss):
                for i in range(ss):
                    c, hit, _ = rows[y * ss + j][x * ss + i]
                    if hit:
                        n += 1
                        acc[0] += c[0]; acc[1] += c[1]; acc[2] += c[2]
            if n / (ss * ss) >= 0.42:
                solid[y][x] = True
                col[y][x] = clamp8(tuple((v / n) ** 0.85 for v in acc))   # lift midtones

    sh = Image.new("L", (64, 64), 0)
    ImageDraw.Draw(sh).ellipse([20, 60, 46, 63], fill=255)
    shp = sh.load()
    for y in range(64):
        for x in range(64):
            if shp[x, y]:
                o[x, y] = (255, 0, 255)
    for y in range(64):
        for x in range(64):
            if solid[y][x]:
                r, g, b = col[y][x]
                o[x, y] = (max(r, 10), max(g, 10), max(b, 12))   # never pure black/magenta
            elif any(0 <= x + dx < 64 and 0 <= y + dy < 64 and solid[y + dy][x + dx]
                     for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                o[x, y] = (20, 18, 24)
    for e in (0.033, -0.033):                                     # glowing eyes survive the downscale
        u, v = to_screen((e, 1.767, 0.07))
        if solid[int(v)][int(u)]:
            o[int(u), int(v)] = (255, 40, 24) if e > 0 else (205, 28, 18)
    for y in (62, 63):                                            # 2px free below the feet
        for x in range(64):
            if o[x, y] not in ((0, 0, 0), (255, 0, 255)):
                o[x, y] = (255, 0, 255)
    return out


def picture(res=900):
    u0, v0, span = 13.0, 23.0, 42.0
    rows = render(False, True, True, u0, v0, span, res)
    img = Image.new("RGB", (res, res))
    glow = Image.new("RGB", (res, res))
    ip, gp = img.load(), glow.load()
    for j in range(res):
        for i in range(res):
            c, hit, em = rows[j][i]
            fx, fy = i / res - 0.62, j / res - 0.55
            bg = (0.07 + 0.30 * max(0, 1 - 2.2 * sqrt(fx * fx + fy * fy)) + 0.05 * j / res,
                  0.04 + 0.07 * max(0, 1 - 2.2 * sqrt(fx * fx + fy * fy)),
                  0.05)
            if hit == 2:
                fade = min(1.0, max(0.0, (j / res - 0.80) / 0.12))
                c = lerp(bg, c, fade)
            elif hit == 0:
                c = bg
            ip[i, j] = clamp8(c)
            if em:
                gp[i, j] = clamp8(c)
    glow = glow.filter(ImageFilter.GaussianBlur(res / 90))
    return ImageChops.add(img, glow)


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    what = sys.argv[2] if len(sys.argv) > 2 else "all"
    if what in ("all", "sprite"):
        sprite(False).save(os.path.join(out, "killbot1.tga"))
        sprite(True).save(os.path.join(out, "killbot2.tga"))
    if what in ("all", "picture"):
        picture(int(sys.argv[3]) if len(sys.argv) > 3 else 900).save(
            os.path.join(out, "killbot_picture.png"))
