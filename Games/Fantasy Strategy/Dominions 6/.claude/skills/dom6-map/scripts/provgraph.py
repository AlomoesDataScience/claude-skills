"""Province graph of a Dominions 6 map from its .map file: every province's number, map name (#landname, when
the map gives one), terrain, neighbours (#neighbour, with #neighbourspec kinds) and centre on the map image
(from the #pb pixel lines, wrap-aware). Read only. The Dominions map is provinces, not squares: this replaces a
click grid - the sweep right-clicks each province's own centre.

  python3 -I provgraph.py build MAPFILE OUT.json          parse the .map (main plane) into OUT.json
  python3 -I provgraph.py fit OUT.json SWEEP.jsonl [--period W H]
        tie map-image pixels to the game's atlas world coords (dom6-map: the resnap atlas, game-ui.json "atlas")
        from swept provinces (num + world point); writes "fit" into OUT.json and prints how well it fits
  python3 -I provgraph.py marks OUT.json                 add each province's marker (the one pure-white pixel in
                                                        the map image = where its flag and fort stand)
  python3 -I provgraph.py show OUT.json NUM [NUM..]        one province: terrain, neighbours, centre (world)

Who owns a province and what is visible come from the SCREEN (F1, flags, panels), never from this file; the
map file is what every player of the game has. Run with no arguments = this text.
"""
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "dom6-maps", "scripts"))
from maptool import TERRAIN          # noqa: E402  (bit, label) pairs from the map-making manual


def terrain_labels(mask):
    return [label for bit, label in TERRAIN if mask & bit]


def build(mapfile, out):
    W = H = None
    wrap = ""
    names, terr, nb, spec = {}, {}, {}, {}
    acc = {}                                 # prov -> [sum cos x, sum sin x, sum cos y, sum sin y, n, minx..]
    for line in open(mapfile, encoding="latin-1"):
        if line.startswith("#pb "):
            x, y, n, p = map(int, line.split()[1:5])
            a = acc.setdefault(p, [0.0, 0.0, 0.0, 0.0, 0])
            yy = H - 1 - y                  # #pb counts y from the bottom
            ay = 2 * math.pi * yy / H
            for i in range(x, x + n):       # rows are short runs; fine for 4096-wide maps
                ax = 2 * math.pi * i / W
                a[0] += math.cos(ax); a[1] += math.sin(ax)
                a[2] += math.cos(ay); a[3] += math.sin(ay)
            a[4] += n
            continue
        w = line.split()
        if not w:
            continue
        if w[0] == "#mapsize":
            W, H = int(w[1]), int(w[2])
        elif w[0] in ("#wraparound", "#hwraparound", "#vwraparound", "#nowraparound"):
            wrap = w[0][1:]
        elif w[0] == "#landname":
            names[int(w[1])] = re.search(r'"(.*)"', line).group(1)
        elif w[0] == "#terrain":
            terr[int(w[1])] = int(w[2])
        elif w[0] == "#neighbour":
            a, b = int(w[1]), int(w[2])
            nb.setdefault(a, set()).add(b); nb.setdefault(b, set()).add(a)
        elif w[0] == "#neighbourspec":
            spec[f"{min(int(w[1]), int(w[2]))}-{max(int(w[1]), int(w[2]))}"] = int(w[3])

    def circ(c, s, size):
        return (math.atan2(s, c) % (2 * math.pi)) * size / (2 * math.pi)

    provs = {}
    for p in sorted(terr):
        a = acc.get(p)
        centre = [round(circ(a[0], a[1], W)), round(circ(a[2], a[3], H))] if a else None
        provs[str(p)] = {"num": p, "name": names.get(p, ""), "terrain": terrain_labels(terr[p]),
                         "mask": terr[p], "neighbours": sorted(nb.get(p, ())), "centre": centre,
                         "pixels": a[4] if a else 0}
    d = {"map": os.path.abspath(mapfile), "size": [W, H], "wrap": wrap, "special_links": spec,
         "provinces": provs}
    json.dump(d, open(out, "w"), indent=0)
    print(f"{len(provs)} provinces, {sum(len(v['neighbours']) for v in provs.values()) // 2} links, "
          f"{len(spec)} special links, map {W}x{H} {wrap} -> {out}")


def fit(out, sweep, period=None):
    d = json.load(open(out))
    W, H = d["size"]
    if not period:
        game = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
        period = json.load(open(os.path.join(game, ".claude", "game-ui.json")))["atlas"]["period"]
    pw, ph = period
    sx, sy = W / pw, H / ph                  # map px per world px (one world period = the whole map)
    offs = []
    for line in open(sweep):
        r = json.loads(line)
        pr = d["provinces"].get(str(r["num"]))
        if not pr or not r.get("world") or not pr["centre"]:
            continue
        # the swept point lies somewhere in the province, the centre is its middle: offset per province
        offs.append((pr["centre"][0] / sx - r["world"][0], pr["centre"][1] / sy - r["world"][1], r["num"]))
    if not offs:
        sys.exit("no swept province with a world point and a map centre")

    def cmean(vals, P):
        c = sum(math.cos(2 * math.pi * v / P) for v in vals); s = sum(math.sin(2 * math.pi * v / P) for v in vals)
        return (math.atan2(s, c) % (2 * math.pi)) * P / (2 * math.pi)

    ox, oy = cmean([o[0] for o in offs], pw), cmean([o[1] for o in offs], ph)
    res = []
    for o in offs:
        ex = (o[0] - ox + pw / 2) % pw - pw / 2; ey = (o[1] - oy + ph / 2) % ph - ph / 2
        res.append((math.hypot(ex, ey), o[2]))
    res.sort()
    d["fit"] = {"period": [pw, ph], "scale": [sx, sy], "offset": [ox, oy],
                "note": "world = (centre / scale - offset) mod period", "from": len(offs)}
    for pr in d["provinces"].values():
        if pr["centre"]:
            pr["world"] = [round((pr["centre"][0] / sx - ox) % pw, 1), round((pr["centre"][1] / sy - oy) % ph, 1)]
    json.dump(d, open(out, "w"), indent=0)
    med = res[len(res) // 2][0]
    print(f"fit from {len(offs)} provinces: scale {sx:.3f},{sy:.3f} map px per world px, offset {ox:.1f},{oy:.1f}")
    print(f"error (world px, clicked point vs province centre): median {med:.1f}, worst {res[-1][0]:.1f} "
          f"(province {res[-1][1]})  - a province is ~{math.sqrt(W * H / len(d['provinces'])) / sx:.0f} world px wide")


def marks(out):
    """Flag points: the pure-white pixel of each province in the map image (#imagefile), assigned by #pb runs."""
    import numpy as np
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    d = json.load(open(out))
    W, H = d["size"]
    folder = os.path.dirname(d["map"])
    img = None
    for line in open(d["map"], encoding="latin-1"):
        if line.startswith("#imagefile"):
            img = os.path.join(folder, line.split(None, 1)[1].strip().strip('"'))
            break
    a = np.asarray(Image.open(img).convert("RGB"))
    ys, xs = np.where((a[:, :, 0] == 255) & (a[:, :, 1] == 255) & (a[:, :, 2] == 255))
    want = {(int(y), int(x)) for y, x in zip(ys, xs)}
    rows = {}
    for y, x in want:
        rows.setdefault(H - 1 - y, []).append(x)          # #pb counts y from the bottom
    found = {}
    for line in open(d["map"], encoding="latin-1"):
        if line.startswith("#pb "):
            x, y, n, p = map(int, line.split()[1:5])
            for wx in rows.get(y, ()):
                if x <= wx < x + n:
                    found[p] = [wx, H - 1 - y]
    f = d.get("fit")
    for k, pr in d["provinces"].items():
        m = found.get(int(k))
        pr["mark"] = m
        if m and f:
            pr["mark_world"] = [round((m[0] / f["scale"][0] - f["offset"][0]) % f["period"][0], 1),
                                round((m[1] / f["scale"][1] - f["offset"][1]) % f["period"][1], 1)]
    json.dump(d, open(out, "w"), indent=0)
    print(f"{len(want)} white pixels, {len(found)} provinces marked of {len(d['provinces'])}")


def show(out, nums):
    d = json.load(open(out))
    P = d["provinces"]
    for n in nums:
        p = P[str(n)]
        nbs = ", ".join(f"{q}{' ' + P[str(q)]['name'] if P[str(q)]['name'] else ''}" for q in p["neighbours"])
        print(f"{n} {p['name']}: {'/'.join(p['terrain']) or 'plain'}; centre {p['centre']} world {p.get('world')}")
        print(f"   neighbours: {nbs}")


def main(a):
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    if a[0] == "build":
        build(a[1], a[2])
    elif a[0] == "fit":
        per = [float(a[a.index("--period") + 1]), float(a[a.index("--period") + 2])] if "--period" in a else None
        fit(a[1], a[2], per)
    elif a[0] == "marks":
        marks(a[1])
    elif a[0] == "show":
        show(a[1], [int(x) for x in a[2:]])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
