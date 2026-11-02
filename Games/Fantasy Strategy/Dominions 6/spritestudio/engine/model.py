"""Model files -> posed SDF scenes.

A model (models/<name>.json) holds:
  materials  name -> {kind: paint|chrome|glow, color: [r,g,b] 0-1, ...}
  bones      solved in order. "free" bones turn (rot, degrees XYZ) and move about a pivot,
             following their parent. "ik" chains reach from a root (carried by the parent)
             toward a target with two segments (bones[0], bones[1]); an optional "end" bone
             sits at the reached point and keeps its own world rotation (feet stay level).
  parts      SDF primitives authored in rest-pose coordinates, each carried by one bone.
             op "cut" subtracts from the parts before it in the same group (group defaults
             to the bone). frames: list of frame keys the part shows in (default all).
  frames     "1" (idle), "2" (attack): a pose (per-bone overrides of the rest values).
  render     camera, scale, canvas and style settings (see render.py).

The same solve is mirrored in web/app.js for the live 3D view.
"""
import math

from sdf import add, sub, mul, dot, cross, norm, length, ik, make_prim

IDENT = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))


def mat_mul(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def mat_vec(A, v):
    return (dot(A[0], v), dot(A[1], v), dot(A[2], v))


def mat_tvec(A, v):
    """Transpose(A) @ v."""
    return tuple(A[0][j] * v[0] + A[1][j] * v[1] + A[2][j] * v[2] for j in range(3))


def euler(r):
    """Rotation matrix for XYZ Euler angles in degrees (three.js order: Rx @ Ry @ Rz)."""
    x, y, z = (math.radians(a) for a in r)
    cx, sx, cy, sy, cz, sz = math.cos(x), math.sin(x), math.cos(y), math.sin(y), math.cos(z), math.sin(z)
    Rx = ((1, 0, 0), (0, cx, -sx), (0, sx, cx))
    Ry = ((cy, 0, sy), (0, 1, 0), (-sy, 0, cy))
    Rz = ((cz, -sz, 0), (sz, cz, 0), (0, 0, 1))
    return mat_mul(mat_mul(Rx, Ry), Rz)


def frame_of(root, joint, pole):
    """Orthonormal frame of a limb segment (columns x, y along the segment, z)."""
    y = norm(sub(joint, root))
    x = cross(y, pole)
    if length(x) < 1e-9:
        x = cross(y, (0.0, 0.0, 1.0)) if abs(y[2]) < 0.9 else cross(y, (1.0, 0.0, 0.0))
    x = norm(x)
    z = cross(x, y)
    return ((x[0], y[0], z[0]), (x[1], y[1], z[1]), (x[2], y[2], z[2]))


def apply(T, p):
    R, t = T
    return add(mat_vec(R, p), t)


def compose(P, L):
    """Parent transform P after local transform L."""
    return mat_mul(P[0], L[0]), add(mat_vec(P[0], L[1]), P[1])


def segment(root0, joint0, pole0, root, joint, pole):
    """Rigid transform taking a rest segment onto its posed segment."""
    F0, F = frame_of(root0, joint0, pole0), frame_of(root, joint, pole)
    R = mat_mul(F, tuple(zip(*F0)))
    return R, sub(root, mat_vec(R, root0))


def solve(model, frame_key):
    """Bone name -> (R, t) mapping rest coordinates to posed coordinates, plus IK joint
    positions for display: {chain: {"root", "mid", "end", "target"}}."""
    pose = model.get("frames", {}).get(frame_key, {}).get("pose", {})
    T = {}
    joints = {}

    def target_point(tg, rest):
        if isinstance(tg, dict):
            return apply(IDENT_T if rest else T[tg["bone"]], tuple(tg["point"]))
        return tuple(tg)

    for b in model["bones"]:
        name = b["name"]
        P = T[b["parent"]] if b.get("parent") else IDENT_T
        p = pose.get(name, {})
        if b["type"] == "free":
            R = euler(p.get("rot", (0, 0, 0)))
            pv = tuple(b.get("pivot", (0, 0, 0)))
            mv = tuple(p.get("move", (0, 0, 0)))
            T[name] = compose(P, (R, sub(add(pv, mv), mat_vec(R, pv))))
        elif b["type"] == "ik":
            root0 = tuple(b["root"])
            mid0, end0 = ik(root0, target_point(b["target"], True), b["l1"], b["l2"], tuple(b["pole"]))
            root = apply(P, root0)
            tgt = target_point(p.get("target", b["target"]), False)
            pole = tuple(p.get("pole", b["pole"]))
            mid, end = ik(root, tgt, b["l1"], b["l2"], pole)
            s1, s2 = b["bones"]
            T[s1] = segment(root0, mid0, tuple(b["pole"]), root, mid, pole)
            T[s2] = segment(mid0, end0, tuple(b["pole"]), mid, end, pole)
            if b.get("end"):
                Re = euler(p.get("end_rot", (0, 0, 0)))
                T[b["end"]] = (Re, sub(end, mat_vec(Re, end0)))
            T[name] = T[s1]
            joints[name] = {"root": root, "mid": mid, "end": end, "target": tgt}
        else:
            raise ValueError(f"unknown bone type {b['type']!r}")
    return T, joints


IDENT_T = (IDENT, (0.0, 0.0, 0.0))


def is_identity(Tr):
    R, t = Tr
    return all(abs(R[i][j] - (1.0 if i == j else 0.0)) < 1e-12 for i in range(3) for j in range(3)) \
        and all(abs(v) < 1e-12 for v in t)


class Group:
    """Parts sharing one bone; cuts subtract from the parts added before them."""

    def __init__(self, name):
        self.name = name
        self.ops = []

    def finish(self):
        adds = [p for k, p, m in self.ops if k == 0]
        if not adds:
            return False
        c = (0.0, 0.0, 0.0)
        for p in adds:
            c = add(c, p[1])
        c = mul(c, 1.0 / len(adds))
        self.c = c
        self.R = max(length(sub(p[1], c)) + p[2] for p in adds) + 0.01
        self.fns = [(k, p[0], m) for k, p, m in self.ops]
        return True

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

    def transform(self, Tr):
        """Carry the finished group by a bone transform (evaluate in rest coordinates)."""
        R, t = Tr
        tx, ty, tz = t

        def wrap(f):
            def g(x, y, z):
                q = mat_tvec(R, (x - tx, y - ty, z - tz))
                return f(q[0], q[1], q[2])
            return g
        self.fns = [(k, wrap(f), m) for k, f, m in self.fns]
        self.c = apply(Tr, self.c)


def visible(part, frame_key):
    fr = part.get("frames")
    return not part.get("hidden") and (not fr or frame_key in fr)


SPLIT = 16


def split(g):
    """A big group without cuts (e.g. a sprite converted to hundreds of pixel blocks) becomes
    several small ones, halved along their longest side, so each ray only tests nearby parts."""
    if len(g.ops) <= SPLIT or any(k for k, _, _ in g.ops):
        return [g]
    cs = [p[1] for _, p, _ in g.ops]
    ax = max(range(3), key=lambda i: max(c[i] for c in cs) - min(c[i] for c in cs))
    ops = sorted(g.ops, key=lambda o: o[1][1][ax])
    out = []
    for half in (ops[:len(ops) // 2], ops[len(ops) // 2:]):
        h = Group(g.name)
        h.ops = half
        out += split(h)
    return out


def build_scene(model, frame_key, mat_ids, per_part=False, keep=None):
    """Posed groups for one frame, and the posed centres of pinned glow parts.

    per_part: label every surface with its part number + 1 instead of its material id
    (the wireframe look needs to know which part each pixel belongs to); also returns
    each solid part on its own as (part id, posed group) for drawing hidden lines.
    keep(centre, radius): posed bounding sphere -> False leaves the part out (off the canvas)."""
    T, _ = solve(model, frame_key)
    groups, order = {}, []
    pins, singles = [], []
    for idx, part in enumerate(model["parts"]):
        if not visible(part, frame_key):
            continue
        key = (part["bone"], part.get("group") or part["bone"])
        if key not in groups:
            groups[key] = Group(key[1])
            order.append(key)
        prim = make_prim(part)
        label = idx + 1 if per_part else mat_ids[part["mat"]]
        cut = part.get("op") == "cut"
        if keep and not cut and not keep(apply(T.get(part["bone"], IDENT_T), prim[1]), prim[2]):
            continue
        groups[key].ops.append((1 if cut else 0, prim, label))
        if per_part and not cut:
            g = Group(part.get("name", ""))
            g.ops.append((0, prim, label))
            g.finish()
            Tr = T.get(part["bone"], IDENT_T)
            if not is_identity(Tr):
                g.transform(Tr)
            singles.append((label, g))
        if part.get("pin"):            # force one pixel to this colour so tiny lights survive
            at = tuple(part["pin_at"]) if part.get("pin_at") else prim[1]
            pins.append((apply(T.get(part["bone"], IDENT_T), at), tuple(part["pin"])))
    out = []
    for key in order:
        Tr = T.get(key[0], IDENT_T)
        for g in split(groups[key]):
            if not g.finish():
                continue
            if not is_identity(Tr):
                g.transform(Tr)
            out.append(g)
    if per_part:
        return out, pins, singles
    return out, pins
