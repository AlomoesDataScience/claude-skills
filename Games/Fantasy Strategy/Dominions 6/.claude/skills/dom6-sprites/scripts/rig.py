
# ---------------------------------------------------------------- rig
SL = (-0.866, 0.0, 0.5)    # model direction that points screen-left: "forward" in the sprite
OUT = (0.5, 0.0, 0.866)    # model direction toward the viewer


def W(f, y, d=0.0):
    """Point f metres screen-left of the body axis, at height y, d metres toward the viewer."""
    return (SL[0] * f + OUT[0] * d, y, SL[2] * f + OUT[2] * d)


def aim(elev, side=0.0):
    """Direction pointing screen-left, raised elev degrees (over 90 leans back to screen-right)."""
    e = math.radians(elev)
    return norm(add(add(mul(SL, cos(e)), (0, sin(e), 0)), mul(OUT, side)))


def axis_rot(k, deg):
    a = math.radians(deg)
    c, s_ = cos(a), sin(a)
    x, y, z = k
    return ((c + x * x * (1 - c), x * y * (1 - c) - z * s_, x * z * (1 - c) + y * s_),
            (y * x * (1 - c) + z * s_, c + y * y * (1 - c), y * z * (1 - c) - x * s_),
            (z * x * (1 - c) - y * s_, z * y * (1 - c) + x * s_, c + z * z * (1 - c)))


def rot(lean=0.0, twist=0.0, axis=OUT):
    """Twist (deg) turns about y, then lean (deg) tips the top screen-left (about axis)."""
    L, T = axis_rot(axis, lean), axis_rot((0, 1, 0), twist)
    return tuple(tuple(sum(L[i][k] * T[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def mv(M, v):
    return (dot(M[0], v), dot(M[1], v), dot(M[2], v))


def mtv(M, v):
    return tuple(M[0][j] * v[0] + M[1][j] * v[1] + M[2][j] * v[2] for j in range(3))


def transformed(group, M, pivot, off):
    """Rotates a finished group by M about pivot, then moves it by off."""
    px, py, pz = add(pivot, off)
    qx, qy, qz = pivot

    def wrap(f):
        def g(x, y, z):
            p = mtv(M, (x - px, y - py, z - pz))
            return f(p[0] + qx, p[1] + qy, p[2] + qz)
        return g
    group.fns = [(k, wrap(f), m) for k, f, m in group.fns]
    group.c = add(add(mv(M, sub(group.c, pivot)), pivot), off)


PIVOT, NECK = (0, 0.92, 0), (0, 1.5, 0)
HEAD_C, HEAD_R = (0, 1.6, 0.012), (0.07, 0.094, 0.084)


class Rig:
    """Joint positions for one pose. Torso and head parts are modelled upright
    (pelvis at 0.92, shoulders at 1.4, head at 1.6) and then leaned and twisted
    into the pose; legs and arms are solved by IK in world space."""

    def __init__(self, P):
        self.P = P
        self.off = P.get("body", (0, 0, 0))
        self.M = rot(P.get("lean", 0), P.get("twist", 0))
        self.groups = []

    def T(self, p):
        return add(add(mv(self.M, sub(p, PIVOT)), PIVOT), self.off)

    def body(self, g):
        g.finish()
        transformed(g, self.M, PIVOT, self.off)
        self.groups.append(g)

    def head(self, g):
        g.finish()
        transformed(g, rot(self.P.get("nod", 0), self.P.get("turn", 0), (1, 0, 0)), NECK, (0, 0, 0))
        transformed(g, self.M, PIVOT, self.off)
        self.groups.append(g)

    def world(self, g):
        g.finish()
        self.groups.append(g)

    def leg(self, s, hip_w=0.09):
        hip = self.T((hip_w * s, 0.88, 0))
        ankle = self.P["feet"][0 if s < 0 else 1]
        knee, ankle = ik(hip, ankle, 0.42, 0.42, self.P.get("knee", (0.15 * s, 0, 1)))
        return hip, knee, ankle

    def arm(self, s, hand, pole, sh_w=0.19, l1=0.28, l2=0.25):
        sh = self.T((sh_w * s, 1.4, -0.005))
        wt = add(hand, mul(norm(sub(hand, sh)), -0.05))
        elbow, wrist = ik(sh, wt, l1, l2, pole)
        return sh, elbow, wrist, norm(sub(wrist, elbow))


# ---------------------------------------------------------------- body parts
def limb(a, b, r1, r2):
    return roundcone(a, b, r1, r2)


def disc(c, axis, r, thick, rnd=0.003):
    """Flat rounded cylinder: radius r, thickness thick along axis (brims, lenses, rotors)."""
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


def lumpy(prim, amp, freq):
    """Bumpy surface (hair, rags, quilting)."""
    f, c, r = prim

    def g(x, y, z):
        return f(x, y, z) - amp * sin(x * freq) * sin(y * freq * 0.9 + 1.3) * sin(z * freq * 1.1 + 0.7)
    return g, c, r + amp


def shell(prim, thick, ylo, yhi):
    """Thin band cut from a surface (straps, helmet trim)."""
    f, c, r = prim

    def g(x, y, z):
        return max(abs(f(x, y, z)) - thick, ylo - y, y - yhi)
    return g, c, r + thick


def cone_skirt(top, bot, r1, r2, zmin=-1.0, zmax=1.0):
    """Coat tails / gown: a flared cone flattened front to back."""
    f, c, r = roundcone(top, bot, r1, r2)

    def g(x, y, z):
        return max(f(x, y, z), zmin - z, z - zmax)
    return g, c, r


def legs(R, thigh, shin, boot, lt=1.0, boot_top=0.45, bare=False, extra=None):
    """Both legs. boot_top: how far up the shin (0..1 from the ankle) the boot shaft reaches."""
    for s in (-1, 1):
        hip, knee, ankle = R.leg(s)
        g = Group("leg")
        g.add(limb(hip, knee, 0.086 * lt, 0.066 * lt), thigh)
        g.add(limb(knee, ankle, 0.064 * lt, 0.05 * lt), shin)
        if boot_top and not bare:
            g.add(limb(lerp(ankle, knee, boot_top), ankle, 0.068 * lt, 0.056 * lt), boot)
        splay = R.P.get("splay", (-14, 12))[0 if s < 0 else 1]
        fb = yaw_basis(splay)
        fw = fb[2]
        fy = ankle[1] - 0.045
        g.add(box((ankle[0] + fw[0] * 0.05, fy, ankle[2] + fw[2] * 0.05),
                  (0.045 * lt, 0.032, 0.11 * lt), fb, rnd=0.014), shin if bare else boot)
        if extra:
            extra(g, s, hip, knee, ankle)
        R.world(g)


def arm(R, s, hand, upper, fore, glove, at=1.0, pole=None, extra=None, sh_w=0.19):
    """One arm reaching for hand; returns (shoulder, elbow, wrist, forearm dir, hand centre)."""
    if pole is None:
        pole = R.P.get("pole_r" if s < 0 else "pole_l", (1.0 * s, -0.6, -0.3))
    sh, elbow, wrist, d = R.arm(s, hand, pole, sh_w)
    g = Group("arm")
    g.add(limb(sh, elbow, 0.056 * at, 0.047 * at), upper)
    g.add(limb(elbow, wrist, 0.047 * at, 0.04 * at), fore)
    hc = add(wrist, mul(d, 0.05 * at))
    g.add(ellipsoid(hc, (0.035 * at, 0.035 * at, 0.035 * at)), glove)
    J = (sh, elbow, wrist, d, hc)
    if extra:
        extra(g, s, J)
    R.world(g)
    return J


def face(h, skin, nose=True):
    h.add(capsule((0, 1.46, -0.005), (0, 1.54, 0.005), 0.042), skin)       # neck
    h.add(ellipsoid(HEAD_C, HEAD_R), skin)
    if nose:
        h.add(ellipsoid((0, 1.588, 0.092), (0.013, 0.02, 0.018)), skin)


def hair_short(h, mat, amp=0.006):
    for prim in (ellipsoid((0, 1.648, -0.008), (0.078, 0.056, 0.088)),
                 ellipsoid((0, 1.6, -0.05), (0.075, 0.08, 0.052))):
        h.add(lumpy(prim, amp, 80), mat)


def eyes(h, mat, y=1.612, z=0.074, r=0.011, gap=0.03):
    for s in (1, -1):
        h.add(sphere((gap * s, y, z), r), mat)


# ---------------------------------------------------------------- equipment
def blade_basis(d):
    """Basis along d with the flat of a blade turned toward the viewer."""
    wa = norm(cross(d, VIEW))
    return (wa, cross(d, wa), d)


def bar_basis(d):
    up = (0, 1, 0) if abs(d[1]) < 0.9 else (0, 0, 1)
    ex = norm(cross(up, d))
    return (ex, cross(d, ex), d)


def sword(g, grip, d, blen=0.75, width=0.03, hilt=0.1, blade=STEEL, guard=GOLD, wrap=BELT, gw=0.065):
    d = norm(d)
    sb = blade_basis(d)
    g.add(capsule(add(grip, mul(d, -hilt)), add(grip, mul(d, 0.06)), 0.017), wrap)
    g.add(sphere(add(grip, mul(d, -hilt - 0.016)), 0.023), guard)
    g.add(box(add(grip, mul(d, 0.075)), (gw, 0.016, 0.014), sb, rnd=0.005), guard)
    g.add(box(add(grip, mul(d, 0.09 + blen / 2)), (width, 0.006, blen / 2), sb, rnd=0.006), blade)
    return add(grip, mul(d, 0.09 + blen))


def rifle(g, grip, d, bayonet=True, body=GUN, furn=WOOD, blade=STEEL, k=1.0):
    """Bayonet rifle held at the pistol grip; returns the muzzle point. k thickens it."""
    d = norm(d)
    rb = bar_basis(d)

    def P(a, b):
        return add(grip, add(mul(d, a), mul(rb[1], b * k)))
    g.add(box(P(-0.2, 0.0), (0.022 * k, 0.05 * k, 0.12), rb, rnd=0.012), furn)       # stock
    g.add(box(P(0.07, 0.045), (0.026 * k, 0.036 * k, 0.17), rb, rnd=0.008), body)    # receiver
    g.add(box(P(0.0, -0.01), (0.016 * k, 0.045 * k, 0.02), rb, rnd=0.006), body)     # pistol grip
    g.add(box(P(0.13, -0.025), (0.015 * k, 0.045 * k, 0.025), rb, rnd=0.005), body)  # magazine
    g.add(box(P(0.34, 0.04), (0.023 * k, 0.028 * k, 0.11), rb, rnd=0.008), furn)     # handguard
    g.add(capsule(P(0.3, 0.05), P(0.62, 0.05), 0.012 * k), body)                     # barrel
    if bayonet:
        g.add(box(P(0.73, 0.04), (0.016, 0.005, 0.12), blade_basis(d), rnd=0.004), blade)
    return P(0.63, 0.05)


def pistol(g, hand, d, body=GUN, grip=WOOD):
    d = norm(d)
    rb = bar_basis(d)

    def P(a, b):
        return add(hand, add(mul(d, a), mul(rb[1], b)))
    g.add(box(P(0.06, 0.035), (0.016, 0.022, 0.09), rb, rnd=0.006), body)
    g.add(box(P(-0.005, -0.005), (0.014, 0.04, 0.02), rb, rnd=0.006), grip)
    return P(0.15, 0.04)


def flash(g, p, d, size=1.0, mat=G_FLASH):
    """Muzzle flash: a hot ball with short spikes."""
    d = norm(d)
    a, b = perp(d, (0, 1, 0))
    g.add(sphere(add(p, mul(d, 0.04 * size)), 0.04 * size), mat)
    for v in (d, add(d, mul(a, 0.8)), sub(d, mul(a, 0.8)), add(d, mul(b, 0.8)), sub(d, mul(b, 0.8))):
        g.add(capsule(add(p, mul(d, 0.04 * size)), add(p, mul(norm(v), 0.13 * size)), 0.012 * size), mat)


def bolt(g, a, b, mat=G_SPARK, r=0.011, kinks=5, amp=0.05, seed=1.0):
    """Zig-zag lightning from a to b."""
    pts = [a]
    d = sub(b, a)
    n1, n2 = perp(norm(d), (0, 0, 1))
    for i in range(1, kinks):
        t = i / kinks
        w = amp * sin(seed * 7.3 + i * 2.9)
        pts.append(add(add(a, mul(d, t)), add(mul(n1, w), mul(n2, w * 0.4))))
    pts.append(b)
    for p, q in zip(pts, pts[1:]):
        g.add(capsule(p, q, r), mat)
