#!/usr/bin/env python3
"""Prototype Dominions 6 map generator (pure Python + PIL, no MapNuke).

  python3 -I mapgen.py NAME [--players 4] [--cols 10] [--rows 6] [--size 1600x1000] [--seed N]
                            [--out DIR] [--workers 6]

Writes DIR/NAME/: NAME.map, NAME.tga, NAME_winter.tga and terrain looks (NAME_forest.tga,
NAME_forestw.tga, ... for plain, forest, farm, waste, swamp, highland), plus NAME_preview.png
(labelled, not used by the game). Check and install with the dom6-maps skill's maptool.py.

How it works:
  1. province centres on a jittered, row-offset grid; each centre has a random weight
     (a power diagram, so provinces differ in size)
  2. every pixel goes to the nearest weighted centre after its position is bent by smooth noise
     (organic borders); done in a process pool
  3. the province graph comes from touching pixels; borders that meet at a corner form chains
     (rivers flow along border chains to the sea, mountain ridges follow them too)
  4. sea, starts (spread out by graph distance), thrones (far from starts), clustered terrain,
     large/small by area, rivers, ridges with passes, roads
  5. art: noise-textured ground per terrain, props (trees, fields, huts, hills, pools, reeds,
     rocks, grass, waves) drawn province by province, borders, coast foam, rivers, mountains,
     roads; winter = snow over the ground and props
  6. .map: #terrain masks, #neighbour/#neighbourspec, #start, #pb runs. Dominions numbers
     provinces by scanning white pixels from the bottom row up, left to right, and counts #pb y
     from the bottom (both checked against a MapNuke export).
"""
import math
import os
import random
import sys
import time
from array import array
from collections import Counter, defaultdict, deque
from multiprocessing import Pool

from PIL import Image, ImageChops, ImageDraw, ImageFilter

# terrain mask bits (dom6mapman.pdf)
SMALL, LARGE, SEA, FRESH, HIGH, SWAMP, WASTE, FOREST, FARM, DEEP = 1, 2, 4, 8, 16, 32, 64, 128, 256, 2048
MOUNTAINS, GOOD_THRONE, GOOD_START = 8388608, 33554432, 67108864
BIT = {"plain": 0, "forest": FOREST, "farm": FARM, "highland": HIGH, "swamp": SWAMP, "waste": WASTE,
       "sea": SEA, "lake": SEA | FRESH, "deep": SEA | DEEP, "mountain": MOUNTAINS}
WATER = ("sea", "lake", "deep")
SPEC = {"pass": 1, "river": 2, "impassable": 4, "road": 8}
LOOKS = ("plain", "forest", "farm", "waste", "swamp", "highland")
SHARES = (("forest", 0.18), ("farm", 0.15), ("highland", 0.08), ("swamp", 0.07), ("waste", 0.07))

# ground colours: (dark, light) for the noise texture
GROUND = {"plain": ((176, 168, 102), (214, 204, 138)), "forest": ((74, 104, 52), (112, 140, 72)),
          "farm": ((188, 156, 78), (222, 192, 106)), "highland": ((142, 128, 94), (186, 172, 132)),
          "swamp": ((92, 108, 74), (130, 140, 96)), "waste": ((196, 172, 132), (228, 210, 172)),
          "sea": ((58, 104, 146), (88, 138, 178))}
INK = (52, 44, 34)

# ---------------------------------------------------------------- pixel labelling (workers)

G = {}   # shared with forked workers: W, H, WX, WY, BS, BUCKET


def label_band(band):
    y0, y1 = band
    W, WX, WY, BS, BUCKET = G["W"], G["WX"], G["WY"], G["BS"], G["BUCKET"]
    nbx, nby = len(BUCKET[0]), len(BUCKET)
    out = bytearray()
    area = [0] * 256
    sx = [0] * 256
    sy = [0] * 256
    for y in range(y0, y1):
        base = y * W
        for x in range(W):
            i = base + x
            wx = x + WX[i]
            wy = y + WY[i]
            bx = int(wx // BS)
            by = int(wy // BS)
            bx = 0 if bx < 0 else (nbx - 1 if bx >= nbx else bx)
            by = 0 if by < 0 else (nby - 1 if by >= nby else by)
            best, bd = 0, 1e30
            for k, cx, cy, wt in BUCKET[by][bx]:
                dx = wx - cx
                dy = wy - cy
                d = dx * dx + dy * dy - wt
                if d < bd:
                    bd, best = d, k
            out.append(best)
            area[best] += 1
            sx[best] += x
            sy[best] += y
    return y0, bytes(out), area, sx, sy


def smooth_noise(w, h, cell, rng):
    """L image of smooth value noise with features about CELL pixels across."""
    sw, sh = max(2, int(w / cell) + 2), max(2, int(h / cell) + 2)
    small = Image.new("L", (sw, sh))
    small.putdata([rng.randrange(256) for _ in range(sw * sh)])
    return small.resize((w, h), Image.BICUBIC)


# ---------------------------------------------------------------- the map model

class Map:
    def __init__(self, name, players, cols, rows, W, H, seed, workers):
        self.name, self.players, self.cols, self.rows = name, players, cols, rows
        self.W, self.H, self.seed, self.workers = W, H, seed, workers
        self.rng = random.Random(seed)

    # 1-2: centres and pixel labels
    def make_provinces(self):
        rng, W, H = self.rng, self.W, self.H
        cw, ch = W / self.cols, H / self.rows
        cent = []
        for r in range(self.rows):
            for c in range(self.cols):
                x = (c + 0.25 + 0.5 * (r % 2) + rng.uniform(-0.2, 0.2)) * cw
                y = (r + 0.5 + rng.uniform(-0.2, 0.2)) * ch
                cent.append((min(W - 8, max(8, x)), min(H - 8, max(8, y)), rng.uniform(-1, 1) * (0.22 * cw) ** 2))
        self.n = len(cent)
        assert self.n < 255
        BS = max(cw, ch)
        nbx, nby = int(W // BS) + 1, int(H // BS) + 1
        grid = defaultdict(list)
        for k, (x, y, wt) in enumerate(cent):
            grid[(int(x // BS), int(y // BS))].append((k, x, y, wt))
        bucket = [[sum((grid[(bx + i, by + j)] for i in (-1, 0, 1) for j in (-1, 0, 1)), [])
                   for bx in range(nbx)] for by in range(nby)]
        n1, n2 = smooth_noise(W, H, 170, rng), smooth_noise(W, H, 170, rng)
        m1, m2 = smooth_noise(W, H, 45, rng), smooth_noise(W, H, 45, rng)
        a, b = 18 / 128, 4 / 128
        WX = array("f", (a * (p - 128) + b * (q - 128) for p, q in zip(n1.getdata(), m1.getdata())))
        WY = array("f", (a * (p - 128) + b * (q - 128) for p, q in zip(n2.getdata(), m2.getdata())))
        G.update(W=W, H=H, WX=WX, WY=WY, BS=BS, BUCKET=bucket)
        step = max(1, H // (self.workers * 4))
        bands = [(y, min(H, y + step)) for y in range(0, H, step)]
        lab = bytearray(W * H)
        area, sx, sy = [0] * 256, [0] * 256, [0] * 256
        with Pool(self.workers) as pool:
            for y0, data, ar, xs, ys in pool.imap_unordered(label_band, bands):
                lab[y0 * W:y0 * W + len(data)] = data
                for k in range(self.n):
                    area[k] += ar[k]
                    sx[k] += xs[k]
                    sy[k] += ys[k]
        self.lab = bytes(lab)
        self.area = area[:self.n]
        self.cent = [(sx[k] / max(1, area[k]), sy[k] / max(1, area[k])) for k in range(self.n)]

    def at(self, x, y):
        return self.lab[int(y) * self.W + int(x)]

    # 3: graph, border pixels, junctions
    def make_graph(self):
        W, H, lab = self.W, self.H, self.lab
        contact = Counter()
        bpts = defaultdict(list)
        junc = set()
        edge = set(lab[:W]) | set(lab[-W:]) | {lab[y * W] for y in range(H)} | {lab[y * W + W - 1] for y in range(H)}
        for y in range(H - 1):
            row = lab[y * W:(y + 1) * W]
            nxt = lab[(y + 1) * W:(y + 2) * W]
            for x in range(W - 1):
                a, b, c = row[x], row[x + 1], nxt[x]
                if a != b:
                    p = (a, b) if a < b else (b, a)
                    contact[p] += 1
                    bpts[p].append((x + 1, y))
                if a != c:
                    p = (a, c) if a < c else (c, a)
                    contact[p] += 1
                    bpts[p].append((x, y + 1))
                if a != b or a != c:
                    s = {a, b, c, nxt[x + 1]}
                    if len(s) >= 3:
                        junc.add(tuple(sorted(s)))
        self.pairs = {p for p, n in contact.items() if n >= 8}
        self.bpts = {p: bpts[p] for p in self.pairs}
        self.adj = defaultdict(set)
        for a, b in self.pairs:
            self.adj[a].add(b)
            self.adj[b].add(a)
        # borders that meet at a corner: (a,b) touches (b,c) and (a,c) at junction {a,b,c}
        self.btouch = defaultdict(set)
        self.junc = junc
        for t in junc:
            ps = [(t[i], t[j]) for i in range(len(t)) for j in range(i + 1, len(t)) if (t[i], t[j]) in self.pairs]
            for p in ps:
                self.btouch[p].update(q for q in ps if q != p)
        self.edge = edge
        # the white pixel: the province's own pixel nearest its centroid
        self.dot = []
        for k, (cx, cy) in enumerate(self.cent):
            x, y = int(cx), int(cy)
            if self.at(x, y) != k:
                best = None
                for r in range(1, 200):
                    for dx in range(-r, r + 1):
                        for dy in (-r, r):
                            for px, py in ((x + dx, y + dy), (x + dy, y + dx)):
                                if 0 <= px < W and 0 <= py < H and self.at(px, py) == k:
                                    best = (px, py)
                                    break
                            if best:
                                break
                        if best:
                            break
                    if best:
                        break
                x, y = best
            self.dot.append((x, y))

    def dist_from(self, starts, nodes):
        d = {s: 0 for s in starts}
        q = deque(starts)
        while q:
            a = q.popleft()
            for b in self.adj[a]:
                if b in nodes and b not in d:
                    d[b] = d[a] + 1
                    q.append(b)
        return d

    def parts(self, nodes, cut=frozenset()):
        """How many connected pieces NODES fall into when the borders in CUT are closed."""
        left, n = set(nodes), 0
        while left:
            n += 1
            q = [left.pop()]
            while q:
                a = q.pop()
                for b in self.adj[a]:
                    if b in left and ((a, b) if a < b else (b, a)) not in cut:
                        left.discard(b)
                        q.append(b)
        return n

    def connected(self, nodes, cut=frozenset()):
        nodes = set(nodes)
        if not nodes:
            return True
        s = next(iter(nodes))
        seen, q = {s}, deque([s])
        while q:
            a = q.popleft()
            for b in self.adj[a]:
                p = (a, b) if a < b else (b, a)
                if b in nodes and b not in seen and p not in cut:
                    seen.add(b)
                    q.append(b)
        return len(seen) == len(nodes)

    # 4: terrain, starts, thrones, borders
    def make_terrain(self):
        rng, n = self.rng, self.n
        self.terr = ["plain"] * n
        # sea: grow from an edge province along the edge-ish provinces
        land = set(range(n))
        sea_n = round(0.12 * n)
        seed = rng.choice(sorted(self.edge))
        sea = {seed}
        land.discard(seed)
        while len(sea) < sea_n:
            cand = sorted({b for a in sea for b in self.adj[a]} & land)
            cand.sort(key=lambda b: (b not in self.edge, rng.random()))
            for b in cand:
                if self.connected(land - {b}):
                    sea.add(b)
                    land.discard(b)
                    break
            else:
                break
        for s in sea:
            self.terr[s] = "sea"
        self.sea, self.land = sea, land
        # starts: spread out over the land graph
        land_l = sorted(land)
        first = rng.choice([p for p in land_l if len(self.adj[p] & land) >= 4] or land_l)
        starts = [first]
        while len(starts) < self.players:
            d = self.dist_from(starts, land)
            far = max(d.get(p, 0) for p in land_l if p not in starts)
            starts.append(rng.choice([p for p in land_l if p not in starts and d.get(p, 0) == far]))
        self.starts = starts
        # thrones: far from every start, apart from each other
        thr = []
        dstart = self.dist_from(starts, land)
        for _ in range(max(1, self.players - 1)):
            dthr = self.dist_from(thr, land) if thr else {}
            cand = [p for p in land_l if p not in starts and p not in thr and dstart.get(p, 0) >= 2]
            cand.sort(key=lambda p: (-(dstart.get(p, 0) * 3 + min(dthr.get(p, 9), 9)), rng.random()))
            thr.append(cand[0])
        self.thrones = thr
        # clustered terrain patches
        free = [p for p in land_l if p not in starts]
        for t, share in SHARES:
            want = round(share * len(land))
            while want > 0:
                open_ = [p for p in free if self.terr[p] == "plain"]
                if not open_:
                    break
                p = rng.choice(open_)
                patch = [p]
                while len(patch) < min(want, rng.choice((1, 2, 2, 3))):
                    nb = [b for a in patch for b in self.adj[a] if b in free and self.terr[b] == "plain" and b not in patch]
                    if not nb:
                        break
                    patch.append(rng.choice(nb))
                for q in patch:
                    self.terr[q] = t
                want -= len(patch)
        order = sorted(land, key=lambda p: self.area[p])
        self.small = set(order[:round(0.1 * len(order))])
        self.large = set(order[-round(0.25 * len(order)):])
        # borders
        lp = sorted(p for p in self.pairs if p[0] in land and p[1] in land)
        self.spec = {}
        coastal = {p for p in lp if any(set(p) | {s} <= set(t) for t in self.junc for s in sea)}
        for _ in range(2):                                   # rivers: border chains ending at the sea
            mouths = [p for p in coastal if p not in self.spec]
            if not mouths:
                break
            cur = rng.choice(mouths)
            chain = [cur]
            for _ in range(rng.randint(3, 5)):
                nxt = [q for q in self.btouch[cur] if q in lp and q not in self.spec and q not in chain
                       and q not in coastal]
                if not nxt:
                    break
                cur = rng.choice(nxt)
                chain.append(cur)
            for p in chain:
                self.spec[p] = "river"
        for _ in range(2):                                   # mountain ridges with a pass or two
            cand = [p for p in lp if p not in self.spec and not set(p) & set(starts)]
            if not cand:
                break
            cur = rng.choice(cand)
            chain = [cur]
            for _ in range(rng.randint(2, 3)):
                nxt = [q for q in self.btouch[cur] if q in cand and q not in chain]
                if not nxt:
                    break
                cur = rng.choice(nxt)
                chain.append(cur)
            for i, p in enumerate(chain):
                kind = "pass" if i % 2 else "impassable"
                if kind == "impassable":
                    cut = {q for q, v in self.spec.items() if v == "impassable"} | {p}
                    if not self.connected(land, frozenset(cut)):
                        kind = "pass"
                self.spec[p] = kind
        roads = [p for p in lp if p not in self.spec and self.terr[p[0]] not in ("forest", "swamp")
                 and self.terr[p[1]] not in ("forest", "swamp")]
        rng.shuffle(roads)
        for p in roads[:max(2, round(0.06 * len(lp)))]:
            self.spec[p] = "road"

    def mask(self, k, look=None):
        t = self.terr[k]
        if look and t not in WATER:
            t = look
        m = BIT[t]
        if k in self.small:
            m |= SMALL
        if k in self.large:
            m |= LARGE
        near = [self.spec.get((min(k, b), max(k, b))) for b in self.adj[k]]
        if "river" in near:
            m |= FRESH
        if "pass" in near or "impassable" in near:
            m |= MOUNTAINS
        if k in self.thrones:
            m |= GOOD_THRONE
        return m

    # 5: art
    def ordered(self, p):
        """Border pixels of pair P in order along the border (projected across the centre line)."""
        (ax, ay), (bx, by) = self.cent[p[0]], self.cent[p[1]]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy) or 1
        ux, uy = -dy / L, dx / L
        return sorted(self.bpts[p], key=lambda q: q[0] * ux + q[1] * uy)

    def render(self, look=None, winter=False):
        W, H, n = self.W, self.H, self.n
        rng = random.Random(self.seed * 7 + 1)
        labimg = Image.frombytes("L", (W, H), self.lab)
        kind = [("sea" if self.terr[k] == "sea" else (look or self.terr[k])) for k in range(n)]
        img = Image.new("RGB", (W, H))
        nz = [smooth_noise(W, H, c, rng) for c in (60, 14)]
        noise = Image.blend(nz[0], nz[1], 0.35)
        for t, (dark, light) in GROUND.items():
            ks = {k for k in range(n) if kind[k] == t}
            if not ks:
                continue
            lut = [255 if i in ks else 0 for i in range(256)]
            tex = Image.merge("RGB", [noise.point(lambda v, a=dark[c], b=light[c]: int(a + (b - a) * v / 255))
                                      for c in range(3)])
            img.paste(tex, mask=labimg.point(lut))
        # borders mask (for keeping props off the borders)
        bmask = ImageChops.difference(labimg.filter(ImageFilter.MaxFilter(3)), labimg.filter(ImageFilter.MinFilter(3)))
        bmask = bmask.point(lambda v: 255 if v else 0)
        far = bmask.filter(ImageFilter.MaxFilter(15)).load()
        lpx = labimg.load()
        d = ImageDraw.Draw(img)
        props = []
        for k in range(n):
            prng = random.Random(self.seed * 1000 + k)
            minx = max(0, int(self.cent[k][0] - 160)); maxx = min(W - 1, int(self.cent[k][0] + 160))
            miny = max(0, int(self.cent[k][1] - 160)); maxy = min(H - 1, int(self.cent[k][1] + 160))
            dotx, doty = self.dot[k]
            per = {"forest": 230, "plain": 380, "farm": 900, "highland": 700, "swamp": 420, "waste": 520, "sea": 900}[kind[k]]
            for _ in range(int(self.area[k] / per)):
                for _try in range(12):
                    x, y = prng.randint(minx, maxx), prng.randint(miny, maxy)
                    if lpx[x, y] == k and not far[x, y] and (x - dotx) ** 2 + (y - doty) ** 2 > 22 ** 2:
                        props.append((y, x, kind[k], prng.random(), prng.random()))
                        break
        props.sort()
        for y, x, t, r1, r2 in props:
            draw_prop(d, t, x, y, r1, r2)
        if winter:
            land = labimg.point([0 if i < n and kind[i] == "sea" else 255 for i in range(256)])
            snow = noise.point(lambda v: 150 + v // 3).resize((W, H))
            snowimg = Image.new("RGB", (W, H), (232, 236, 242))
            img = Image.composite(snowimg, img, ImageChops.multiply(snow, land))
            seamask = ImageChops.invert(land)
            img = Image.composite(Image.blend(img, Image.new("RGB", (W, H), (120, 140, 156)), 0.35), img, seamask)
            d = ImageDraw.Draw(img)
        # coast foam on the sea side, then province borders on land
        landm = labimg.point([0 if i < n and kind[i] == "sea" else 255 for i in range(256)])
        foam = ImageChops.subtract(landm.filter(ImageFilter.MaxFilter(7)), landm)
        img.paste((168, 200, 214) if not winter else (200, 214, 222), mask=foam)
        inner = ImageChops.multiply(bmask, landm)
        dark = Image.blend(img, Image.new("RGB", (W, H), INK), 0.7)
        img = Image.composite(dark, img, inner)
        d = ImageDraw.Draw(img)
        for p, v in sorted(self.spec.items()):
            pts = self.ordered(p)[::3]
            if len(pts) < 2:
                continue
            if v == "river":
                water = (66, 112, 168) if not winter else (150, 180, 205)
                d.line(pts, fill=(40, 70, 110), width=8, joint="curve")
                d.line(pts, fill=water, width=6, joint="curve")
                d.line(pts, fill=(110, 156, 200) if not winter else (205, 222, 235), width=2, joint="curve")
            elif v in ("pass", "impassable"):
                mpts = self.ordered(p)
                L = len(mpts)
                for i in range(0, L, 9):
                    if v == "pass" and 0.35 * L < i < 0.65 * L:
                        continue
                    x, y = mpts[i]
                    draw_mountain(d, x, y, 9 + (i * 7919 % 5), winter)
                if v == "pass":
                    x, y = mpts[L // 2]
                    d.line([(x - 6, y - 3), (x + 6, y + 3)], fill=(150, 112, 70), width=3)
            elif v == "road":
                (ax, ay), (bx, by) = self.dot[p[0]], self.dot[p[1]]
                L = math.hypot(bx - ax, by - ay)
                steps = int(L / 13)
                for i in range(2, steps - 1):
                    t0, t1 = i / steps, (i + 0.55) / steps
                    d.line([(ax + (bx - ax) * t0, ay + (by - ay) * t0), (ax + (bx - ax) * t1, ay + (by - ay) * t1)],
                           fill=(126, 92, 58), width=4)
        # nothing may be pure white except the province pixels
        r, g, b = img.split()
        img = Image.merge("RGB", (r.point(lambda v: 254 if v == 255 else v), g, b))
        px = img.load()
        for x, y in self.dot:
            px[x, y] = (255, 255, 255)
        return img

    # 6: files
    def image_jobs(self):
        jobs = [("", None, False), ("_winter", None, True)]
        for t in LOOKS:
            jobs += [(f"_{t}", t, False), (f"_{t}w", t, True)]
        return jobs

    def numbering(self):
        """Dominions numbers provinces by scanning white pixels bottom row first, left to right."""
        order = sorted(range(self.n), key=lambda k: (self.H - 1 - self.dot[k][1], self.dot[k][0]))
        return {k: i + 1 for i, k in enumerate(order)}

    def extra_lines(self, num):
        return []

    def province_lines(self, num):
        """#setland blocks (poptype, forts, sites...) written at the end of the file."""
        return []

    def description(self):
        return (f"Prototype map made by Claude's own Python generator (mapgen.py, seed {self.seed}). "
                f"{self.players} players, {self.n} provinces, {len(self.thrones)} thrones.")

    def write(self, out):
        os.makedirs(out, exist_ok=True)
        num = self.numbering()
        W, H, name = self.W, self.H, self.name
        L = [f"#dom2title {name}", f"#imagefile {name}.tga", f"#winterimagefile {name}_winter.tga",
             f"#mapsize {W} {H}", "#domversion 600",
             f'#description "{self.description()}"', ""]
        for k in sorted(range(self.n), key=lambda k: num[k]):
            L.append(f"#terrain {num[k]} {self.mask(k)}")
        L.append("")
        for s in self.starts:
            L.append(f"#start {num[s]}")
        L.append("")
        for k, nm in sorted(getattr(self, "names", {}).items(), key=lambda kv: num[kv[0]]):
            L.append(f'#landname {num[k]} "{nm}"')
        L.append("")
        L += self.extra_lines(num)
        for a, b in sorted(self.pairs, key=lambda p: (num[p[0]], num[p[1]])):
            L.append(f"#neighbour {num[a]} {num[b]}")
            if (a, b) in self.spec:
                L.append(f"#neighbourspec {num[a]} {num[b]} {SPEC[self.spec[(a, b)]]}")
        L.append("")
        for yb in range(H):                                  # #pb y counts from the bottom
            row = self.lab[(H - 1 - yb) * W:(H - yb) * W]
            x0 = 0
            for x in range(1, W + 1):
                if x == W or row[x] != row[x0]:
                    L.append(f"#pb {x0} {yb} {x - x0} {num[row[x0]]}")
                    x0 = x
        L += self.province_lines(num)
        with open(os.path.join(out, f"{name}.map"), "w", encoding="latin-1") as f:
            f.write("\n".join(L) + "\n")
        for suffix, look, winter in self.image_jobs():
            t0 = time.time()
            self.render(look, winter).save(os.path.join(out, f"{name}{suffix}.tga"))
            print(f"  {name}{suffix}.tga  {time.time() - t0:.1f} s", flush=True)
        prev = Image.open(os.path.join(out, f"{name}.tga")).convert("RGB")
        d = ImageDraw.Draw(prev)
        for k in range(self.n):
            x, y = self.dot[k]
            tag = "S" if k in self.starts else ("T" if k in self.thrones else "")
            d.text((x + 4, y - 6), f"{num[k]}{tag}", fill=(0, 0, 0))
        prev.save(os.path.join(out, f"{name}_preview.png"))


# ---------------------------------------------------------------- props

def draw_prop(d, t, x, y, r1, r2):
    if t == "forest":
        s = 7 + int(r1 * 5)
        if r2 < 0.65:                                        # conifer
            d.line([(x, y), (x, y - 3)], fill=(78, 56, 36), width=2)
            for i, (c, o) in enumerate((((34, 66, 40), INK), ((44, 82, 48), INK), ((58, 98, 56), INK))):
                top = y - 3 - s * (1.2 + 0.55 * i)
                w = s * (0.75 - 0.15 * i)
                d.polygon([(x, top), (x - w, y - 3 - s * 0.45 * i), (x + w, y - 3 - s * 0.45 * i)], fill=c, outline=(26, 44, 28))
        else:                                                # broadleaf
            d.line([(x, y), (x, y - s * 0.7)], fill=(84, 60, 38), width=2)
            d.ellipse([x - s * 0.8, y - s * 1.9, x + s * 0.8, y - s * 0.5], fill=(62, 104, 50), outline=(30, 52, 28))
            d.ellipse([x - s * 0.5, y - s * 1.75, x + s * 0.1, y - s * 1.15], fill=(92, 134, 64))
    elif t == "plain":
        if r2 < 0.9:
            for dx in (-2, 0, 2):
                d.line([(x, y), (x + dx * 1.5, y - 4 - r1 * 3)], fill=(132, 132, 62), width=1)
        else:
            d.ellipse([x - 5, y - 6, x + 5, y + 1], fill=(112, 132, 64), outline=(70, 82, 40))
    elif t == "farm":
        if r2 < 0.8:                                         # field with furrows
            w, h = 14 + r1 * 10, 8 + r1 * 5
            col = [(226, 196, 104), (176, 170, 82), (200, 160, 86)][int(r2 * 10) % 3]
            sk = 5
            d.polygon([(x - w, y), (x + w - sk, y), (x + w, y - h), (x - w + sk, y - h)], fill=col, outline=(150, 120, 64))
            for i in range(1, 4):
                yy = y - h * i / 4
                d.line([(x - w + sk * i / 4 + 2, yy), (x + w - sk + sk * i / 4 - 2, yy)], fill=(160, 128, 66))
        else:                                                # hut
            d.rectangle([x - 5, y - 6, x + 5, y], fill=(176, 150, 112), outline=INK)
            d.polygon([(x - 7, y - 6), (x, y - 12), (x + 7, y - 6)], fill=(140, 72, 50), outline=INK)
    elif t == "highland":
        w, h = 12 + r1 * 10, 7 + r1 * 6
        pts = [(x + w * math.cos(a), y - h * math.sin(a)) for a in [i * math.pi / 12 for i in range(13)]]
        d.polygon(pts, fill=(150, 136, 98), outline=(92, 80, 58))
        hl = [(x - w * 0.15 + w * 0.6 * math.cos(a), y - h * 0.85 * math.sin(a)) for a in [math.pi / 2 + i * math.pi / 16 for i in range(9)]]
        d.line(hl, fill=(190, 178, 136), width=2)
    elif t == "swamp":
        if r2 < 0.35:
            w = 8 + r1 * 8
            d.ellipse([x - w, y - w * 0.4, x + w, y + w * 0.4], fill=(70, 102, 98), outline=(50, 72, 62))
        else:
            for dx in (-3, 0, 3):
                d.line([(x + dx, y), (x + dx * 1.3, y - 6 - r1 * 4)], fill=(76, 92, 48), width=1)
    elif t == "waste":
        if r2 < 0.45:
            s = 3 + r1 * 4
            d.polygon([(x - s, y), (x - s * 0.4, y - s), (x + s * 0.6, y - s * 0.8), (x + s, y)], fill=(150, 138, 124), outline=(94, 84, 74))
        elif r2 < 0.8:
            pts, cx = [], x - 8
            for i in range(5):
                pts.append((cx + i * 4, y + (2 if i % 2 else -1) * (1 + r1)))
            d.line(pts, fill=(172, 146, 108), width=1)
        else:
            for a in (-0.6, 0, 0.7):
                d.line([(x, y), (x + 6 * math.sin(a), y - 6 * math.cos(a))], fill=(120, 96, 66), width=1)
    elif t == "sea":
        w = 5 + r1 * 4
        d.arc([x - w, y - 3, x, y + 3], 200, 340, fill=(130, 172, 204), width=1)
        d.arc([x, y - 3, x + w, y + 3], 200, 340, fill=(130, 172, 204), width=1)


def draw_mountain(d, x, y, s, winter):
    top = (x, y - s * 1.6)
    d.polygon([top, (x - s, y + 2), (x, y + 2)], fill=(160, 152, 144) if not winter else (220, 224, 230))
    d.polygon([top, (x, y + 2), (x + s, y + 2)], fill=(112, 104, 98) if not winter else (170, 176, 186))
    d.polygon([top, (x - s * 0.35, y - s * 1.0), (x, y - s * 1.1), (x + s * 0.3, y - s * 1.0)], fill=(236, 236, 240))
    d.line([(x - s, y + 2), top, (x + s, y + 2)], fill=(58, 52, 48), width=1)


def main(argv):
    if not argv or argv[0].startswith("-"):
        sys.exit(__doc__)
    name = argv[0]
    if not name.replace("_", "").isalpha():
        sys.exit("map names may only use a-z, A-Z and _")

    def opt(k, d):
        return argv[argv.index(k) + 1] if k in argv else d
    W, H = (int(v) for v in opt("--size", "1600x1000").split("x"))
    m = Map(name, int(opt("--players", 4)), int(opt("--cols", 10)), int(opt("--rows", 6)), W, H,
            int(opt("--seed", random.randrange(10 ** 6))), int(opt("--workers", 6)))
    out = os.path.join(opt("--out", os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")), name)
    t0 = time.time()
    m.make_provinces()
    print(f"provinces: {m.n} labelled in {time.time() - t0:.1f} s (seed {m.seed})", flush=True)
    m.make_graph()
    m.make_terrain()
    c = Counter(m.terr)
    print(f"graph: {len(m.pairs)} borders; terrain {dict(c)}; starts {m.starts}; thrones {m.thrones}; "
          f"special borders {dict(Counter(m.spec.values()))}", flush=True)
    m.write(out)
    print(f"wrote {out} in {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main(sys.argv[1:])
