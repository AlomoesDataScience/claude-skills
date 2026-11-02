"""Convert the original killbot generator into a Sprite Studio model file.

  python3 -I tools/import_killbot.py ../killbot/killbot.py models/killbot.json

Runs the original build() with recording stand-ins for the primitives, then assigns each
group to a bone. The rest pose is the killbot's own stance, so frame 1 matches the
original sprite; frame 2 adds the plasma bolt.
"""
import json
import math
import sys

sqrt, sin, cos = math.sqrt, math.sin, math.cos
TAU = 2 * math.pi

SRC, OUT = sys.argv[1], sys.argv[2]
src = open(SRC).read()
helpers = src[src.index("# ---------------------------------------------------------------- vectors"):
              src.index("# ---------------------------------------------------------------- primitives")]
groups_src = src[src.index("def sum_v(vs):"):src.index("# ---------------------------------------------------------------- the model")]
build_src = src[src.index("def build(firing):"):src.index("# ---------------------------------------------------------------- camera")]

CHROME, DARK, EYE, GUNMETAL, GLOW, BOLT = "chrome", "dark", "eye", "gunmetal", "cells", "bolt"
IDENT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))


def L(v):
    return [float(x) for x in v]


def sphere(c, r):
    return {"type": "sphere", "c": L(c), "r": r}


def capsule(a, b, r):
    return {"type": "capsule", "a": L(a), "b": L(b), "r": r}


def roundcone(a, b, r1, r2):
    return {"type": "roundcone", "a": L(a), "b": L(b), "r1": r1, "r2": r2}


def ellipsoid(c, r):
    return {"type": "ellipsoid", "c": L(c), "r": L(r)}


def box(c, half, bas=IDENT, rnd=0.0):
    p = {"type": "box", "c": L(c), "half": L(half), "rnd": rnd}
    if tuple(tuple(v) for v in bas) != IDENT:
        p["basis"] = [L(v) for v in bas]
    return p


def grooves(prim, origin, axis, period, amp, lo=-1e9, hi=1e9):
    p = dict(prim)
    g = {"origin": L(origin), "axis": L(axis), "period": period, "amp": amp}
    if lo > -1e9:
        g["lo"] = lo
    if hi < 1e9:
        g["hi"] = hi
    p["grooves"] = g
    return p


class Group:
    def __init__(self, name):
        self.name = name
        self.ops = []

    def add(self, prim, mat=CHROME):
        self.ops.append(("add", prim, mat, comment_at(sys._getframe(1).f_lineno)))

    def cut(self, prim, mat=DARK):
        self.ops.append(("cut", prim, mat, comment_at(sys._getframe(1).f_lineno)))

    def finish(self):
        pass


def comment_at(lineno):
    """The trailing comment on a line of the original build(), used as the part name."""
    line = build_src.splitlines()[lineno - 1]
    return line.split("#", 1)[1].strip() if "#" in line else ""


ns = dict(globals())
exec(helpers, ns)
exec(groups_src, ns)
ns.update(sphere=sphere, capsule=capsule, roundcone=roundcone, ellipsoid=ellipsoid, box=box,
          grooves=grooves, Group=Group)
exec(compile(build_src, "build", "exec"), ns)

basis, add, mul = ns["basis"], ns["add"], ns["mul"]
gb, go = basis((-0.22, 0.0, 1.0)), (-0.12, 1.16, 0.13)


def gl(x, y, z):
    return add(go, add(add(mul(gb[0], x), mul(gb[1], y)), mul(gb[2], z)))


def assign(groups, frames=None):
    parts, seen = [], {}
    for g in groups:
        k = seen[g.name] = seen.get(g.name, 0) + 1
        side = {("thigh", 1): "L", ("shin", 1): "L", ("thigh", 2): "R", ("shin", 2): "R",
                ("hand", 1): "R", ("hand", 2): "L", ("upperarm", 1): "R", ("forearm", 1): "R",
                ("upperarm", 2): "L", ("forearm", 2): "L"}.get((g.name, k))
        gname = f"{g.name}.{side}" if side else g.name
        bone = {"head": "head", "gun": "gun", "bolt": "gun", "hand": "gun"}.get(g.name, "body")
        if g.name in ("thigh", "shin", "upperarm", "forearm"):
            bone = gname
        names = {}
        for i, (op, prim, mat, note) in enumerate(g.ops):
            p = dict(prim)
            p.update(op=op, mat=mat, bone=bone, group=gname)
            if g.name == "shin" and i >= len(g.ops) - 2:          # the foot keeps level when posed
                p.update(bone=f"foot.{side}", group=f"foot.{side}")
            if mat == EYE and prim["type"] == "sphere":
                s = 1 if prim["c"][0] > 0 else -1
                p.update(pin=[255, 40, 24] if s > 0 else [205, 28, 18], pin_at=[0.033 * s, 1.767, 0.07])
            if frames:
                p["frames"] = frames
            base = f"{gname} {note or (mat + ' ' + prim['type'])}"
            names[base] = names.get(base, 0) + 1
            p["name"] = base if names[base] == 1 else f"{base} {names[base]}"
            parts.append(p)
    return parts


idle = ns["build"](False)
fire = ns["build"](True)
parts = assign(idle) + assign([g for g in fire if g.name == "bolt"], ["2"])

model = {
    "name": "killbot",
    "notes": "Terminator-style chrome endoskeleton with a plasma rifle. Imported from killbot/killbot.py.",
    "render": {"style": "studio", "res": [64, 64], "px_per_m": 34.0 / 1.88, "cx": 33.5, "y0": 61.6,
               "yaw": -30.0, "pitch": 9.0, "light": [-0.55, 0.75, 0.55], "shadow": [20, 60, 46, 63],
               "outline": [20, 18, 24], "gamma": 0.85, "ss": 5, "file": "killbot"},
    "materials": {
        "chrome": {"kind": "chrome", "color": [0.95, 0.97, 1.0]},
        "dark": {"kind": "paint", "color": [0.30, 0.30, 0.32], "refl": 0.42, "spec": 0.45, "gloss": 30},
        "gunmetal": {"kind": "paint", "color": [0.24, 0.25, 0.29], "refl": 0.38, "spec": 0.45, "gloss": 30},
        "eye": {"kind": "glow", "color": [1.0, 0.16, 0.08]},
        "cells": {"kind": "glow", "color": [0.45, 0.88, 1.0]},
        "bolt": {"kind": "glow", "color": [0.75, 0.95, 1.0]},
    },
    "bones": [
        {"name": "body", "type": "free", "parent": None, "pivot": [0.0, 0.95, 0.0]},
        {"name": "head", "type": "free", "parent": "body", "pivot": [0.0, 1.62, -0.02]},
        {"name": "gun", "type": "free", "parent": None, "pivot": L(go)},
        {"name": "leg.L", "type": "ik", "parent": "body", "root": [0.10, 0.95, 0.0], "target": [0.19, 0.085, 0.13],
         "pole": [0.15, 0.0, 1.0], "l1": 0.45, "l2": 0.44, "bones": ["thigh.L", "shin.L"], "end": "foot.L"},
        {"name": "leg.R", "type": "ik", "parent": "body", "root": [-0.10, 0.95, 0.0],
         "target": [-0.17, 0.085, -0.11], "pole": [-0.15, 0.0, 1.0], "l1": 0.45, "l2": 0.44,
         "bones": ["thigh.R", "shin.R"], "end": "foot.R"},
        {"name": "arm.R", "type": "ik", "parent": "body", "root": [-0.205, 1.52, -0.005],
         "target": {"bone": "gun", "point": L(gl(-0.026, 0.0, -0.058))}, "pole": [-1.0, -0.5, -0.25],
         "l1": 0.34, "l2": 0.28, "bones": ["upperarm.R", "forearm.R"]},
        {"name": "arm.L", "type": "ik", "parent": "body", "root": [0.205, 1.52, -0.005],
         "target": {"bone": "gun", "point": L(gl(0.032, 0.0, 0.12))}, "pole": [0.5, -0.8, 0.1],
         "l1": 0.34, "l2": 0.28, "bones": ["upperarm.L", "forearm.L"]},
    ],
    "parts": parts,
    "frames": {"1": {"label": "Idle", "pose": {}}, "2": {"label": "Attack", "pose": {}}},
}
with open(OUT, "w") as f:
    json.dump(model, f, indent=1)
print(f"{len(parts)} parts, {len(model['bones'])} bones -> {OUT}")
