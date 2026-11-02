"""RGM-79 GM mobile suit sprites for Dominions 6 (size 8 unit).

Builds the GM as a signed-distance model, renders it with anime-style cel
shading and line work, and exports four 128x128 24-bit TGA sprites
(black = transparent, magenta = shadow):

  rgm_saber1.tga  shield + beam saber, idle          (#spr1)
  rgm_saber2.tga  shield + beam saber, slash         (#spr2)
  rgm_spray1.tga  shield + beam spray gun, idle      (#spr1)
  rgm_spray2.tga  shield + beam spray gun, firing    (#spr2)

Model space: y up, x = the suit's left, z = its front, feet at y=0,
head top at ~1.72 units.

usage: python3 rgm.py OUTDIR
"""
import math
import os
import sys
from multiprocessing import Pool

from PIL import Image, ImageDraw

sqrt, sin, cos = math.sqrt, math.sin, math.cos
TAU = 2 * math.pi

# materials
MINT, RED, YELLOW, SLOT, JOINT, FIST, VISOR, WHITE, GUN, SABER, ORB, GLASS = range(1, 13)
CHROME = MINT       # default material names used by the shared SDF helpers
DARK = SLOT
EMISSIVE = (SABER, ORB)

# cel palette per material: (lit, shade, deep)
PALETTE = {
    MINT: ((150, 208, 188), (84, 146, 128), (56, 104, 94)),
    RED: ((228, 60, 42), (168, 34, 32), (116, 22, 26)),
    YELLOW: ((252, 196, 52), (206, 136, 24), (150, 92, 18)),
    SLOT: ((34, 30, 44), (24, 22, 32), (18, 16, 24)),
    JOINT: ((122, 132, 138), (80, 88, 96), (56, 62, 70)),
    FIST: ((84, 116, 132), (52, 72, 86), (38, 52, 64)),
    VISOR: ((90, 220, 150), (40, 160, 104), (28, 118, 80)),
    WHITE: ((236, 238, 240), (176, 184, 196), (128, 136, 150)),
    GUN: ((140, 132, 166), (90, 84, 114), (64, 60, 84)),
    GLASS: ((118, 128, 214), (74, 80, 164), (52, 56, 124)),
}
# beam colours: the saber's pink and the orb sampled from the reference poster
SABER_EDGE, SABER_CORE = (255, 84, 196), (255, 236, 250)
ORB_EDGE, ORB_MID, ORB_CORE = (192, 112, 176), (222, 165, 206), (255, 252, 255)

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
def limb_box(a, b, half_side, half_front, rnd, fr_hint=(0, 0, 1)):
    """Rounded box running from a to b."""
    d = norm(sub(b, a))
    fr = sub(fr_hint, mul(d, dot(fr_hint, d)))
    if length(fr) < 1e-4:
        fr = sub((0, 1, 0), mul(d, d[1]))
    fr = norm(fr)
    side = cross(d, fr)
    return box(lerp(a, b, 0.5), (half_side, length(sub(b, a)) / 2, half_front), (side, d, fr), rnd)


def disc(c, axis, r, thick):
    """Short rounded cylinder (bolts, ear sensors)."""
    a = norm(axis)
    return capsule(add(c, mul(a, -thick / 2)), add(c, mul(a, thick / 2)), r)


def convex(origin, bas, planes, radius):
    """Convex solid as an intersection of half-spaces, in the local frame `bas`.
    Each plane is (normal, offset) in local (u, v, n) coordinates."""
    ox, oy, oz = origin
    e0, e1, e2 = bas
    pl = [(norm(nv), off / length(nv)) for nv, off in planes]

    def f(x, y, z):
        px, py, pz = x - ox, y - oy, z - oz
        u = px * e0[0] + py * e0[1] + pz * e0[2]
        v = px * e1[0] + py * e1[1] + pz * e1[2]
        w = px * e2[0] + py * e2[1] + pz * e2[2]
        return max(n[0] * u + n[1] * v + n[2] * w - o for n, o in pl)
    return f, origin, radius


def outline(verts):
    """Edge half-planes (u, v) of a convex polygon given counter-clockwise."""
    planes = []
    for (u0, v0), (u1, v1) in zip(verts, verts[1:] + verts[:1]):
        nu, nv = v1 - v0, -(u1 - u0)
        planes.append(((nu, nv, 0.0), nu * u0 + nv * v0))
    return planes


def shield_planes(inset, front, ridge):
    """The GM shield: an elongated hexagon, symmetric top to bottom, with flat
    top and bottom edges and its points on the left and right at the middle,
    and a face of two facets meeting along a vertical centre ridge."""
    top, bot, top_hw, bot_hw, hw, mid = 0.44, -0.44, 0.1, 0.1, 0.19, 0.0
    verts = [(-top_hw, top), (-hw, mid), (-bot_hw, bot), (bot_hw, bot), (hw, mid), (top_hw, top)]
    planes = outline(verts[::-1]) if _cw(verts) else outline(verts)
    planes = [(nv, off - inset * length(nv)) for nv, off in planes]
    slope = ridge / hw
    planes += [((slope, 0.0, 1.0), front + ridge), ((-slope, 0.0, 1.0), front + ridge),
               ((0.0, 0.0, -1.0), 0.012)]
    return planes


def _cw(verts):
    area = sum(u0 * v1 - u1 * v0 for (u0, v0), (u1, v1) in zip(verts, verts[1:] + verts[:1]))
    return area < 0


POSES = {
    # right wrist target, right elbow pole, weapon direction.
    # saber1: held at point, blade forward and 65 degrees above horizontal
    # saber2: straight-arm stab
    # spray1: gun arm lowered, muzzle angled down and forward (as in the stance photos)
    # spray2: arm raised, firing forward
    "saber1": ((-0.36, 1.08, 0.24), (-1.0, -0.4, -0.4),
               add(mul(norm((-0.8, 0.0, 0.6)), cos(math.radians(65))), (0, sin(math.radians(65)), 0))),
    "saber2": ((-0.4, 1.2, 0.38), (-1.0, -0.3, -0.3), (-0.8, 0.0, 0.6)),
    "spray1": ((-0.38, 0.96, 0.14), (-0.6, -0.2, -1.0), (-0.3, -0.75, 0.6)),
    "spray2": ((-0.36, 1.18, 0.32), (-1.0, -0.5, -0.3), (-0.6, 0.04, 1.0)),
}


def build(pose):
    """Proportions and stance follow the RGM-79 references: square red shoulder
    blocks ~44% of the height across, red chest over a wide belly block, crotch
    at ~52% and knees at ~39% of the height, broad shins, big feet planted wide,
    shield carried out at the left side."""
    G = []
    wrist_r, pole_r, wdir = POSES[pose]
    wdir = norm(wdir)

    # --- head ---
    h = Group("head")
    h.add(ellipsoid((0, 1.625, -0.005), (0.096, 0.108, 0.104)))
    for s in (1, -1):
        h.add(disc((0.096 * s, 1.62, -0.005), (1, 0, 0), 0.04, 0.024))          # ear sensors
    h.add(box((0, 1.625, 0.062), (0.078, 0.024, 0.032), rnd=0.009), VISOR)      # goggle
    h.add(box((0, 1.556, 0.054), (0.042, 0.036, 0.034), rnd=0.014))             # faceplate
    h.add(box((0, 1.73, 0.034), (0.016, 0.02, 0.04), rnd=0.007))                # crest
    h.add(box((0, 1.728, 0.074), (0.011, 0.012, 0.007), rnd=0.003), VISOR)      # crest sensor
    h.add(capsule((0, 1.47, -0.01), (0, 1.54, -0.01), 0.05), JOINT)             # neck
    G.append(h)

    # --- torso: red chest and shoulder blocks over a wide mint belly ---
    t = Group("torso")
    t.add(box((0, 1.38, -0.005), (0.15, 0.085, 0.1), rnd=0.03), RED)            # chest
    t.add(box((0, 1.26, 0.02), (0.065, 0.07, 0.09), rnd=0.022), RED)            # chest V point
    t.add(box((0, 1.28, 0.13), (0.022, 0.06, 0.005), rnd=0.003), SLOT)          # cockpit slot
    for s in (1, -1):
        t.add(grooves(box((0.098 * s, 1.355, 0.127), (0.042, 0.03, 0.007), rnd=0.003),
                      (0, 0, 0), (0, 1, 0), 0.016, 0.006), YELLOW)              # vents
        t.add(sphere((0.24 * s, 1.37, -0.005), 0.06), JOINT)
        t.add(box((0.285 * s, 1.425, -0.005), (0.072, 0.078, 0.085), rnd=0.026), RED)  # shoulder block
    t.add(box((0, 1.065, -0.005), (0.165, 0.08, 0.1), rnd=0.03))                # belly block
    t.add(box((0, 1.19, -0.015), (0.13, 0.05, 0.09), rnd=0.02))                 # waist
    t.add(box((0, 1.33, -0.15), (0.12, 0.1, 0.05), rnd=0.028))                  # backpack
    if not pose.startswith("saber"):
        t.add(capsule((-0.1, 1.4, -0.16), (-0.15, 1.62, -0.18), 0.016), WHITE)  # stowed saber
    G.append(t)

    # --- waist and skirt armour ---
    w = Group("waist")
    w.add(box((0, 0.955, 0.015), (0.05, 0.055, 0.065), rnd=0.02))               # crotch block
    for s in (1, -1):
        w.add(box((0.085 * s, 0.97, 0.1), (0.072, 0.055, 0.011),
                  yaw_basis(14 * s), rnd=0.01))                                 # front skirt
        w.add(box((0.185 * s, 0.985, -0.005), (0.011, 0.06, 0.075), rnd=0.01))  # side skirt
        w.add(sphere((0.1 * s, 0.94, 0.0), 0.055), JOINT)                       # hip joint
    G.append(w)

    # --- legs: planted wide, nearly straight, angled outward ---
    for s, ankle, splay in ((1, (0.31, 0.13, 0.03), 16), (-1, (-0.3, 0.13, -0.02), -16)):
        hip = (0.1 * s, 0.94, 0.0)
        knee, ankle = ik(hip, ankle, 0.27, 0.575, (0.2 * s, 0, 1))
        th = Group("thigh")
        th.add(limb_box(hip, knee, 0.054, 0.06, 0.02))
        G.append(th)
        sh = Group("shin")
        d = norm(sub(ankle, knee))
        fr, side = front_side(d)
        sh.add(sphere(knee, 0.052), JOINT)
        sh.add(limb_box(add(knee, mul(d, 0.04)), add(ankle, mul(d, -0.03)), 0.076, 0.085, 0.027))
        sh.add(box(add(ankle, mul(d, -0.075)), (0.088, 0.06, 0.105), (side, d, fr), 0.023))  # flare
        sh.add(ellipsoid(add(add(knee, mul(d, 0.25)), mul(fr, -0.055)), (0.071, 0.16, 0.06)))  # calf
        sh.add(box(add(add(knee, mul(fr, 0.037)), mul(d, -0.01)), (0.08, 0.072, 0.064),
                   (side, d, fr), 0.03))                                         # knee armour
        sh.add(disc(add(add(knee, mul(side, 0.088 * s)), mul(fr, 0.01)), side, 0.032, 0.022))  # knee bolt
        sh.add(disc(add(ankle, mul(side, 0.088 * s)), side, 0.028, 0.02))        # ankle bolt
        sh.add(sphere(ankle, 0.05), JOINT)
        fb = yaw_basis(splay)
        fw = fb[2]
        sh.add(box((ankle[0] + fw[0] * 0.03, 0.06, ankle[2] + fw[2] * 0.03),
                   (0.08, 0.045, 0.15), fb, rnd=0.016))                         # foot
        toe_b = (fb[0], norm(add(fb[1], mul(fw, 0.45))), norm(sub(fw, mul(fb[1], 0.45))))
        sh.add(box((ankle[0] + fw[0] * 0.18, 0.045, ankle[2] + fw[2] * 0.18),
                   (0.082, 0.03, 0.055), toe_b, rnd=0.014), RED)                # toe cap
        sh.add(box((ankle[0] + fw[0] * 0.02, 0.016, ankle[2] + fw[2] * 0.02),
                   (0.084, 0.016, 0.16), fb, rnd=0.006), RED)                   # sole
        G.append(sh)

    # --- arms ---
    arms = {}
    for s, wrist, pole in ((-1, wrist_r, pole_r), (1, (0.47, 1.04, 0.06), (1.0, -0.4, -0.6))):
        shp = (0.28 * s, 1.37, -0.005)
        elbow, wrist = ik(shp, wrist, 0.26, 0.27, pole)
        ua = Group("upperarm")
        ua.add(limb_box(add(shp, mul(norm(sub(elbow, shp)), 0.07)), elbow, 0.046, 0.05, 0.018))
        G.append(ua)
        fa = Group("forearm")
        fa.add(sphere(elbow, 0.05), JOINT)
        fa.add(limb_box(add(elbow, mul(norm(sub(wrist, elbow)), 0.025)), wrist, 0.058, 0.064, 0.024))
        d = norm(sub(wrist, elbow))
        fa.add(box(add(wrist, mul(d, 0.045)), (0.046, 0.05, 0.05), basis(d), rnd=0.017), FIST)
        G.append(fa)
        arms[s] = (elbow, wrist, d)

    # --- shield: carried out at the left side, face turned outward and forward ---
    elbow, wrist, d = arms[1]
    up = norm((-0.12, 1.0, -0.15))                                              # top leans in and back
    face = (1.0, 0.0, 0.6)
    nrm = norm(sub(face, mul(up, dot(face, up))))
    across = cross(up, nrm)
    sb = (across, up, nrm)
    fist = add(wrist, mul(d, 0.045))
    c = add(add(fist, mul(nrm, 0.095)), mul(up, 0.02))                            # strapped in front of the fist

    def sl(u, v, n):
        return add(c, add(add(mul(across, u), mul(up, v)), mul(nrm, n)))

    sg = Group("shield")
    sg.add(convex(c, sb, shield_planes(0.0, 0.012, 0.045), 0.5), WHITE)        # rim
    sg.add(convex(c, sb, shield_planes(0.03, 0.015, 0.045), 0.5), RED)         # face
    star_v, star_c = -0.12, 0.028                                               # crossing point
    star_front = [((0.0, 0.0, 1.0), 0.068), ((0.0, 0.0, -1.0), 0.0)]
    sg.add(convex(c, sb, outline([(0, star_v + 0.14), (-star_c, star_v), (0, star_v - 0.24),
                                  (star_c, star_v)]) + star_front, 0.5), YELLOW)
    sg.add(convex(c, sb, outline([(0.09, star_v), (0, star_v + star_c), (-0.09, star_v),
                                  (0, star_v - star_c)]) + star_front, 0.5), YELLOW)
    sg.add(box(sl(0, 0.26, 0.058), (0.06, 0.028, 0.006), sb, rnd=0.004), WHITE)  # window frame
    sg.add(box(sl(0, 0.26, 0.062), (0.042, 0.015, 0.004), sb, rnd=0.002), GLASS)
    sg.add(box(sl(0, 0.0, -0.05), (0.03, 0.1, 0.04), sb, rnd=0.008), JOINT)     # forearm mount
    G.append(sg)

    # --- weapon in the right hand ---
    elbow, wrist, d = arms[-1]
    grip = add(wrist, mul(d, 0.045))
    wg = Group("weapon")
    if pose.startswith("saber"):
        wg.add(capsule(add(grip, mul(wdir, -0.065)), add(grip, mul(wdir, 0.06)), 0.017), WHITE)
        wg.add(capsule(add(grip, mul(wdir, 0.08)), add(grip, mul(wdir, 0.82)), 0.03), SABER)
    else:
        gb = basis(wdir)

        def gl(x, y, z):
            return add(grip, add(add(mul(gb[0], x), mul(gb[1], y)), mul(gb[2], z)))
        wg.add(box(gl(0, 0.05, 0.09), (0.028, 0.04, 0.17), gb, rnd=0.011), GUN)       # body
        wg.add(box(gl(0, 0.1, 0.05), (0.014, 0.014, 0.07), gb, rnd=0.005), JOINT)     # sensor
        wg.add(box(gl(0, -0.01, -0.01), (0.02, 0.045, 0.024), gb, rnd=0.009), GUN)    # grip
        wg.add(box(gl(0, 0.028, 0.15), (0.023, 0.032, 0.036), gb, rnd=0.007), JOINT)  # e-cap
        wg.add(capsule(gl(0, 0.05, 0.25), gl(0, 0.05, 0.3), 0.036), JOINT)            # muzzle
        if pose == "spray2":
            wg.add(sphere(gl(0, 0.05, 0.42), 0.08), ORB)
            wg.add(capsule(gl(0, 0.05, 0.32), gl(0, 0.05, 0.42), 0.032), ORB)
    G.append(wg)

    for grp in G:
        grp.finish()
    return G


# ---------------------------------------------------------------- camera
YAW, PITCH = -40.0, 7.0   # three-quarter view facing left (the game reads this as the move direction)
RES = 128
K = 85.0 / 1.72           # sprite pixels per unit: ~87 px tall for a size 8 unit
CX, Y0 = 73.0, 125.4      # sprite position of the model origin


def cam_matrix():
    a, b = math.radians(YAW), math.radians(PITCH)
    ry = ((cos(a), 0, sin(a)), (0, 1, 0), (-sin(a), 0, cos(a)))
    rx = ((1, 0, 0), (0, cos(b), -sin(b)), (0, sin(b), cos(b)))
    return tuple(tuple(sum(rx[i][k] * ry[k][j] for k in range(3)) for j in range(3)) for i in range(3))


A = cam_matrix()


def to_model(v):
    return tuple(v[0] * A[0][j] + v[1] * A[1][j] + v[2] * A[2][j] for j in range(3))


def to_cam(v):
    return tuple(dot(A[i], v) for i in range(3))


DIR = to_model((0, 0, -1))
VIEW = mul(DIR, -1)
LIGHT = norm(to_model(norm((-0.75, 0.6, 0.35))))

SCENE = None


def sdf(x, y, z, groups):
    best, bm, bg = 1e9, 0, None
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
            best, bm, bg = d, m, g
    return best, bm, bg


def dist(p):
    return sdf(p[0], p[1], p[2], SCENE)[0]


def normal(p):
    e = 0.0006
    n = (0.0, 0.0, 0.0)
    for v in ((1, -1, -1), (-1, -1, 1), (-1, 1, -1), (1, 1, 1)):
        n = add(n, mul(v, dist(add(p, mul(v, e)))))
    return norm(n)


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


NO_CAST_SHADOW = ("torso", "waist")   # keeps the mint under the red chest readable


def shade(p, mat, part):
    n = normal(p)
    ndv = max(dot(n, VIEW), 0.0)
    if mat == SABER:
        return lerp(SABER_EDGE, SABER_CORE, min(1.0, ndv ** 2 * 1.4))
    if mat == ORB:
        k = ndv ** 1.5
        return lerp(ORB_EDGE, ORB_MID, min(1.0, k * 2)) if k < 0.5 else lerp(ORB_MID, ORB_CORE, (k - 0.5) * 2)
    lit, mid, deep = PALETTE[mat]
    v = max(dot(n, LIGHT), 0.0)
    if part.name not in NO_CAST_SHADOW:
        v *= hard_shadow(add(p, mul(n, 0.004)), LIGHT)
    c = lit if v > 0.42 else (mid if v > 0.1 else deep)
    r = sub(mul(n, 2 * dot(n, VIEW)), VIEW)
    if v > 0.42 and max(dot(r, LIGHT), 0.0) ** 24 > 0.55:                       # highlight
        c = lerp(c, (255, 255, 255), 0.35)
    return c


def trace(x_cam, y_cam):
    """Returns (rgb, material, depth, part id) for one ray; material 0 is a miss."""
    o = to_model((x_cam, y_cam, 4.0))
    cands = []
    for g in SCENE:
        c = to_cam(g.c)
        if (c[0] - x_cam) ** 2 + (c[1] - y_cam) ** 2 <= g.R * g.R:
            cands.append(g)
    if not cands:
        return (0, 0, 0), 0, 1e9, -1
    t = max(min(4.0 - to_cam(g.c)[2] - g.R for g in cands), 0.0)
    tend = max(4.0 - to_cam(g.c)[2] + g.R for g in cands)
    for _ in range(260):
        p = add(o, mul(DIR, t))
        d, m, g = sdf(p[0], p[1], p[2], cands)
        if d < 0.0005 and m:
            return shade(p, m, g), m, t, SCENE.index(g)
        t += max(d * 0.75, 0.0003)
        if t > tend:
            break
    return (0, 0, 0), 0, 1e9, -1


def render_rows(args):
    rows, scale, w = args
    out = []
    for j in rows:
        line = []
        for i in range(w):
            u = (i + 0.5) / scale
            v = (j + 0.5) / scale
            line.append(trace((u - CX) / K, (Y0 - v) / K))
        out.append((j, line))
    return out


def init(pose):
    global SCENE
    SCENE = build(pose)


def render(pose, ss):
    n = RES * ss
    jobs = [(list(range(j, min(j + 4, n))), ss, n) for j in range(0, n, 4)]
    with Pool(os.cpu_count(), initializer=init, initargs=(pose,)) as pool:
        rows = {}
        for chunk in pool.imap_unordered(render_rows, jobs):
            for j, line in chunk:
                rows[j] = line
    return [rows[j] for j in range(n)]


# ---------------------------------------------------------------- sprite output
INK = (28, 34, 40)
INK_OFFSETS = [(dx, dy) for dx in range(-3, 4) for dy in range(-3, 4) if 0 < dx * dx + dy * dy <= 9]
BEAM_INK = (120, 24, 96)


def sprite(pose, ss=4):
    hi = render(pose, ss)
    n = RES * ss
    # ink lines where a nearer part overlaps a farther one, or where two separate
    # parts meet (anime-style contours)
    ink = [[False] * n for _ in range(n)]
    for j in range(n):
        for i in range(n):
            c, m, dep, part = hi[j][i]
            if not m or m in EMISSIVE:
                continue
            for di, dj in INK_OFFSETS:
                ii, jj = i + di, j + dj
                if 0 <= ii < n and 0 <= jj < n:
                    c2, m2, d2, part2 = hi[jj][ii]
                    if m2 and m2 not in EMISSIVE and (d2 > dep + 0.03 or (part2 != part and d2 > dep + 0.004)):
                        ink[j][i] = True
                        break

    out = Image.new("RGB", (RES, RES), (0, 0, 0))
    o = out.load()
    solid = [[0] * RES for _ in range(RES)]          # 0 empty, 1 body, 2 beam
    col = [[None] * RES for _ in range(RES)]
    for y in range(RES):
        for x in range(RES):
            acc, cnt, beams = [0.0, 0.0, 0.0], 0, 0
            for j in range(ss):
                for i in range(ss):
                    c, m, _, _ = hi[y * ss + j][x * ss + i]
                    if m:
                        if ink[y * ss + j][x * ss + i]:
                            c = INK
                        cnt += 1
                        beams += m in EMISSIVE
                        acc[0] += c[0]; acc[1] += c[1]; acc[2] += c[2]
            if cnt / (ss * ss) >= 0.4:
                solid[y][x] = 2 if beams * 2 > cnt else 1
                col[y][x] = tuple(int(v / cnt + 0.5) for v in acc)

    sh = Image.new("L", (RES, RES), 0)
    ImageDraw.Draw(sh).ellipse([40, 120, 104, 127], fill=255)
    shp = sh.load()
    for y in range(RES):
        for x in range(RES):
            if shp[x, y]:
                o[x, y] = (255, 0, 255)
    nb4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for y in range(RES):
        for x in range(RES):
            if solid[y][x]:
                r, g, b = col[y][x]
                if (r, g, b) == (255, 0, 255):
                    r = 254
                o[x, y] = (max(r, 10), max(g, 10), max(b, 12))   # never pure black
                continue
            near = [solid[y + dy][x + dx] for dx, dy in nb4
                    if 0 <= x + dx < RES and 0 <= y + dy < RES and solid[y + dy][x + dx]]
            if near:
                o[x, y] = INK if 1 in near else BEAM_INK
    # soft halo ring around the beam-spray orb
    if pose == "spray2":
        for y in range(RES):
            for x in range(RES):
                if o[x, y] in ((0, 0, 0), (255, 0, 255)) and any(
                        0 <= x + dx < RES and 0 <= y + dy < RES and solid[y + dy][x + dx] == 2
                        for dx in range(-3, 4) for dy in range(-3, 4) if dx * dx + dy * dy <= 9):
                    o[x, y] = (122, 52, 118)
    for y in (126, 127):                                    # 2px free below the feet
        for x in range(RES):
            if o[x, y] not in ((0, 0, 0), (255, 0, 255)):
                o[x, y] = (255, 0, 255)
    return out


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    poses = sys.argv[2:] or list(POSES)
    for pose in poses:
        sprite(pose).save(os.path.join(out, f"rgm_{pose}.tga"))
