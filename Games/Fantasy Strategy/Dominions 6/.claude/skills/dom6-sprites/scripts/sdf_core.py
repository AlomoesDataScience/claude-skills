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


