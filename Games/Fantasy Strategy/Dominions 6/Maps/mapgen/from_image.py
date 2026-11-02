#!/usr/bin/env python3
"""Make Dominions 6 maps from a finished map picture (prototype).

  python3 -I from_image.py IMAGE REPLICA_NAME PICTURE_NAME --config greyhawk_hd
                           [--players N] [--land SP] [--sea SP] [--seed N] [--out DIR]

One province layout, two maps:
  REPLICA_NAME  the picture redrawn in mapgen.py's art style (ground, props, rivers, mountains, a
                symbol for every town and capital, numbered markers for the config's SITES), with
                winter and terrain-look images
  PICTURE_NAME  the picture itself as the map image, province borders drawn over it, plus a winter tint

The config module describes the picture (greyhawk_hd.py is the full example):
  CLASSES, classify_image(im) -> grid of class indices per BLOCK px; TERRAIN_OF {class: terrain kind};
  EXTRA_BITS {class: mask bits when the class covers 30%+ of a province}; NAMES [(name, x, y)] label
  spots in picture pixels (NAME_SCALE_W if they were read off a smaller copy), WATER_NAMES;
  NAME_TERRAIN (words in a name that set the province terrain); optional CROP, WORK (work grid
  divisor), PLAYERS, LAND_SP, SEA_SP, water_mask(im), river_mask(im), find_cities(im), SITES
  [(number, x, y, text)], TITLE.

How the layout follows the picture:
  1. terrain classes per block; land/water mask (cleaned of text and rivers); rivers on land
  2. every region label seeds a province (unless an earlier label is too close); jittered grid
     centres fill the gaps, so provinces stay a standard size; islands and lakes get one each
  3. provinces grow from their centres (Dijkstra over noisy costs on the work grid, land and water
     apart) and cannot cross rivers, so borders snap to the real rivers and coasts
  4. terrain per province from the class shares, or from its name ("... Forest", "... Hills");
     fill provinces are named after the nearest label ("North Kingdom of Furyondy")
  5. borders along a river are river borders; borders through mountain ranges are impassable or
     passes (the land stays connected); provinces with an adventure site get many sites (1024)
"""
import heapq
import importlib
import math
import os
import random
import sys
import time
from collections import Counter, deque

from PIL import Image, ImageChops, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mapgen as MG  # noqa: E402

INF = float("inf")
MANY_SITES = 1024
DEFAULT_TERRAIN = {"plains": "plain", "forest": "forest", "hills": "highland", "mountains": "mountain",
                   "waste": "waste", "swamp": "swamp", "sea": "plain", "frame": "plain"}
# replica ground per picture class (falls back to the terrain kind's ground)
CLASS_GROUND = {"desert": ((222, 200, 140), (242, 226, 176)), "jungle": ((46, 80, 40), (74, 108, 56)),
                "ice": ((190, 196, 206), (226, 230, 238))}
# terrain pairs that make no sense together in one province
BAD_MIX = {frozenset(p) for p in (("swamp", "waste"), ("swamp", "mountain"), ("swamp", "highland"),
                                  ("waste", "forest"), ("mountain", "highland"))}
DIRS = ["East", "Northeast", "North", "Northwest", "West", "Southwest", "South", "Southeast"]


def components(mask, W, H, val):
    """4-connected components of pixels equal to VAL in a bytearray mask: (comp ids, sizes)."""
    comp = [-1] * (W * H)
    sizes = []
    for s in range(W * H):
        if mask[s] != val or comp[s] >= 0:
            continue
        c = len(sizes)
        comp[s] = c
        q = [s]
        n = 0
        while q:
            i = q.pop()
            n += 1
            x = i % W
            for j in ((i - 1) if x else -1, (i + 1) if x < W - 1 else -1, i - W, i + W):
                if 0 <= j < W * H and mask[j] == val and comp[j] < 0:
                    comp[j] = c
                    q.append(j)
        sizes.append(n)
    return comp, sizes


class ImageMap(MG.Map):
    def __init__(self, image, players, land_sp, sea_sp, seed, cfg):
        super().__init__("x", players, 0, 0, 0, 0, seed, 6)
        src = Image.open(image).convert("RGB")
        if hasattr(cfg, "CROP"):
            src = src.crop(cfg.CROP)
        self.src = src
        self.W, self.H = self.src.size
        self.land_sp, self.sea_sp, self.cfg = land_sp, sea_sp, cfg
        self.F = getattr(cfg, "WORK", 2)
        self.terrain_of = getattr(cfg, "TERRAIN_OF", DEFAULT_TERRAIN)
        self.extra = {}

    # ------------------------------------------------------------ reading the picture
    def read_picture(self):
        W, H, cfg = self.W, self.H, self.cfg
        self.grid, _ = cfg.classify_image(self.src)
        gw, gh = len(self.grid[0]), len(self.grid)
        cls = Image.new("L", (gw, gh))
        cls.putdata([c for row in self.grid for c in row])
        self.cls = cls.resize((W, H), Image.NEAREST).filter(ImageFilter.ModeFilter(9))
        if hasattr(cfg, "water_mask"):
            water, rb, thin = self.flat_water_rivers()
        else:
            water, rb, thin = self.textured_water_rivers()
        self.river_full = bytearray(1 if v else 0 for v in thin.getdata())
        F = self.F
        self.W2, self.H2 = W // F, H // F
        w2 = water.resize((self.W2, self.H2), Image.BOX).point(lambda v: 255 if v >= 128 else 0)
        self.dom = bytearray(0 if v else 1 for v in w2.getdata())            # 1 land, 0 water
        r2 = rb.resize((self.W2, self.H2), Image.BOX).point(lambda v: 255 if v >= 40 else 0)
        self.wall = bytearray(1 if v and self.dom[i] else 0 for i, v in enumerate(r2.getdata()))
        self.cities = cfg.find_cities(self.src) if hasattr(cfg, "find_cities") else []
        fo = [i for i, c in enumerate(cfg.CLASSES) if self.terrain_of.get(c) == "forest"]
        # a city symbol inside a forest is usually a dark speck of the trees
        cpx = self.cls.load()
        self.cities = [c for c in self.cities if cpx[c[0], c[1]] not in fo or c[2] == "capital"]

    def flat_water_rivers(self):
        """Flat-colour maps: water and river colours are exact."""
        W, H = self.W, self.H
        water = self.cfg.water_mask(self.src).filter(ImageFilter.MedianFilter(11))   # drops rivers, text
        riv = ImageChops.subtract(self.cfg.river_mask(self.src), water.filter(ImageFilter.MaxFilter(5)))
        jb = bytearray(1 if v else 0 for v in riv.getdata())
        comp, sizes = components(jb, W, H, 1)
        keep = Image.frombytes("L", (W, H), bytes(255 if c >= 0 and sizes[c] >= 150 else 0 for c in comp))
        return water, keep.filter(ImageFilter.MaxFilter(3)), keep

    def textured_water_rivers(self):
        """Painted maps: water is clearly blue; rivers are thin dark bluish dashed lines."""
        W, H, C = self.W, self.H, self.cfg.CLASSES
        bl = self.src.filter(ImageFilter.BoxBlur(3))
        r, g, b = bl.split()
        water = ImageChops.subtract(b, r).point(lambda v: 255 if v > 30 else 0)
        water = water.filter(ImageFilter.MedianFilter(9))
        lum = self.src.convert("L")
        dark = ImageChops.subtract(lum.filter(ImageFilter.BoxBlur(5)), lum).point(lambda v: 255 if v > 18 else 0)
        sr, sg, sb = self.src.split()
        blu = ImageChops.subtract(sb, sr).point(lambda v: 255 if v > 4 else 0)
        riv = ImageChops.multiply(dark, blu)
        near_water = water.filter(ImageFilter.MaxFilter(13))
        forest = self.cls.point(lambda v: 255 if v == C.index("forest") else 0).filter(ImageFilter.MaxFilter(9))
        riv = ImageChops.subtract(riv, ImageChops.lighter(near_water, forest))
        joined = riv.filter(ImageFilter.MaxFilter(7))           # join the dashes
        jb = bytearray(1 if v else 0 for v in joined.getdata())
        comp, sizes = components(jb, W, H, 1)
        box = [[W, H, 0, 0] for _ in sizes]
        for i, c in enumerate(comp):
            if c >= 0:
                x, y, bb = i % W, i // W, box[c]
                bb[0], bb[2] = min(bb[0], x), max(bb[2], x)
                bb[1], bb[3] = min(bb[1], y), max(bb[3], y)
        # rivers are long and thin; textured ground joins into blobs; fold lines are straight
        ok = [n >= 700 and n / max(b[2] - b[0], b[3] - b[1], 1) <= 18
              and min(b[2] - b[0], b[3] - b[1]) > 12 for n, b in zip(sizes, box)]
        keep = Image.frombytes("L", (W, H), bytes(255 if c >= 0 and ok[c] else 0 for c in comp))
        thin = ImageChops.multiply(riv.filter(ImageFilter.MaxFilter(3)), keep)
        return water, ImageChops.multiply(riv.filter(ImageFilter.MaxFilter(5)), keep), thin

    # ------------------------------------------------------------ provinces
    def snap(self, x, y, want, rmax=30):
        """Nearest work-grid cell to picture point (x, y) in domain WANT and not on a river."""
        W2, H2, F = self.W2, self.H2, self.F
        cx, cy = int(x / F), int(y / F)
        for r in range(rmax):
            best = None
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    if max(abs(dx), abs(dy)) != r:
                        continue
                    px, py = cx + dx, cy + dy
                    if 1 <= px < W2 - 1 and 1 <= py < H2 - 1:
                        i = py * W2 + px
                        if self.dom[i] == want and not self.wall[i]:
                            d = dx * dx + dy * dy
                            if best is None or d < best[0]:
                                best = (d, i)
            if best:
                return best[1]
        return None

    def make_provinces(self):
        self.read_picture()
        rng, W2, H2, cfg = self.rng, self.W2, self.H2, self.cfg
        dom = self.dom
        min_land = int(600 / self.F ** 2)           # islands and lakes smaller than this melt away
        for val, keep in ((1, min_land), (0, 2 * min_land)):
            comp, sizes = components(dom, W2, H2, val)
            for i, c in enumerate(comp):
                if c >= 0 and sizes[c] < keep // 4:
                    dom[i] = 1 - val
        self.wcomp, wsizes = components(dom, W2, H2, 0)
        edge = {self.wcomp[i] for i in list(range(W2)) + list(range(W2 * (H2 - 1), W2 * H2))
                + [y * W2 for y in range(H2)] + [y * W2 + W2 - 1 for y in range(H2)] if self.wcomp[i] >= 0}
        self.lake_comps = {c for c in range(len(wsizes)) if c not in edge}
        lcomp, lsizes = components(dom, W2, H2, 1)
        # 1. every label seeds a province unless an earlier label is too close
        scale = self.W / getattr(cfg, "NAME_SCALE_W", self.W)
        water_names = getattr(cfg, "WATER_NAMES", set())
        seeds, self.minor = [], []                  # (work idx, name)
        for name, x, y in cfg.NAMES:
            want = 0 if name in water_names else 1
            i = self.snap(x * scale, y * scale, want)
            if i is None:
                continue
            sp = self.land_sp if want else self.sea_sp
            ix, iy = i % W2, i // W2
            if any(dom[j] == want and (j % W2 - ix) ** 2 + (j // W2 - iy) ** 2 < (0.62 * sp) ** 2 for j, _ in seeds):
                self.minor.append((i, name))
                continue
            seeds.append((i, name))
        cent = [i for i, _ in seeds]
        self.seed_names = [nm for _, nm in seeds]
        # 2. jittered grid centres fill the gaps
        for val, sp in ((1, self.land_sp), (0, self.sea_sp)):
            near = [(i % W2, i // W2) for i in cent if dom[i] == val]
            rows = int(H2 / (sp * 0.87)) + 1
            for r in range(rows):
                for c in range(int(W2 / sp) + 1):
                    x = int((c + 0.5 * (r % 2) + rng.uniform(-0.25, 0.25)) * sp)
                    y = int((r + 0.5 + rng.uniform(-0.25, 0.25)) * sp * 0.87)
                    if 2 <= x < W2 - 2 and 2 <= y < H2 - 2:
                        i = y * W2 + x
                        if dom[i] == val and not self.wall[i] and \
                                all((x - a) ** 2 + (y - b) ** 2 >= (0.8 * sp) ** 2 for a, b in near):
                            cent.append(i)
        have = Counter((dom[i], (lcomp if dom[i] else self.wcomp)[i]) for i in cent)
        for val, comp, sizes, keep in ((1, lcomp, lsizes, min_land), (0, self.wcomp, wsizes, 2 * min_land)):
            for c, n in enumerate(sizes):
                if n >= keep and not have[(val, c)]:
                    pts = [i for i in range(W2 * H2) if comp[i] == c and not self.wall[i]]
                    if not pts:
                        continue
                    mx = sum(i % W2 for i in pts) / len(pts)
                    my = sum(i // W2 for i in pts) / len(pts)
                    cent.append(min(pts, key=lambda i: (i % W2 - mx) ** 2 + (i // W2 - my) ** 2))
        # 3. grow; add centres to big unreached pockets (land fenced off by rivers) and grow again
        for _ in range(4):
            lab = self.grow(cent)
            un = bytearray(1 if lab[i] == 255 and not self.wall[i] else 0 for i in range(W2 * H2))
            comp, sizes = components(un, W2, H2, 1)
            big = [c for c, n in enumerate(sizes) if n >= (self.land_sp ** 2) * 0.3]
            if not big:
                break
            for c in big:
                cent.append(next(i for i in range(W2 * H2) if comp[i] == c))
        assert len(cent) < 255, f"{len(cent)} provinces: raise --land / --sea"
        self.n = len(cent)
        self.cent_idx = cent
        # leftovers (river cells, tiny pockets, tiny islands): take a neighbour's province
        q = deque(i for i in range(W2 * H2) if lab[i] != 255)
        for same_domain in (True, False):
            while q:
                i = q.popleft()
                x = i % W2
                for j in ((i - 1) if x else -1, (i + 1) if x < W2 - 1 else -1, i - W2, i + W2):
                    if 0 <= j < W2 * H2 and lab[j] == 255 and (not same_domain or dom[j] == dom[i]):
                        lab[j] = lab[i]
                        q.append(j)
            q = deque(i for i in range(W2 * H2) if lab[i] != 255)
        full = Image.frombytes("L", (W2, H2), bytes(lab)).resize((self.W, self.H), Image.NEAREST)
        if self.F > 2:
            full = full.filter(ImageFilter.ModeFilter(self.F * 2 + 1))     # round off the grid steps
        self.lab = full.tobytes()
        area, sx, sy = [0] * self.n, [0] * self.n, [0] * self.n
        W = self.W
        for i, k in enumerate(self.lab):
            area[k] += 1
            sx[k] += i % W
            sy[k] += i // W
        self.area = area
        self.cent = [(sx[k] / max(1, area[k]), sy[k] / max(1, area[k])) for k in range(self.n)]
        self.half_lab = lab
        self.name_provinces()

    def name_provinces(self):
        F, W2 = self.F, self.W2
        self.names = {k: nm for k, nm in enumerate(self.seed_names)}
        self.realm = dict(self.names)                # province -> the label whose land it is
        for i, nm in self.minor:                     # small features name their province if free
            k = self.half_lab[i]
            if k not in self.names:
                self.names[k] = nm
            self.realm.setdefault(k, nm)
        used = set(self.names.values())
        seeds = [(k, (self.cent_idx[k] % W2) * F, (self.cent_idx[k] // W2) * F) for k in range(len(self.seed_names))]
        for k in range(self.n):
            if k in self.names:
                continue
            cx, cy = self.cent[k]
            d0 = self.dom[self.cent_idx[k]]
            sp = (self.land_sp if d0 else self.sea_sp) * F
            cand = [(math.hypot(cx - x, cy - y), s, x, y) for s, x, y in seeds if self.dom[self.cent_idx[s]] == d0]
            if not cand:
                continue
            d, s, x, y = min(cand)
            self.realm.setdefault(k, self.names[s])
            if d > 2.6 * sp:
                continue
            ang = math.degrees(math.atan2(-(cy - y), cx - x)) % 360
            base = self.names[s]
            base = base[4:] if base.startswith("The ") else base
            nm = f"{DIRS[int((ang + 22.5) // 45) % 8]} {base}"
            if nm not in used:
                self.names[k] = nm
                used.add(nm)

    def grow(self, cent):
        """Multi-source Dijkstra over noisy step costs; land and water apart; rivers stop growth."""
        W2, H2, dom, wall = self.W2, self.H2, self.dom, self.wall
        nz = MG.smooth_noise(W2, H2, 35, random.Random(self.seed + 5))
        cost = [1.0 + 2.2 * v / 255 for v in nz.getdata()]
        rng = random.Random(self.seed + 9)
        dist = [INF] * (W2 * H2)
        lab = bytearray([255]) * (W2 * H2)
        heap = []
        for k, i in enumerate(cent):
            d0 = rng.uniform(0, 0.35) * (self.land_sp if dom[i] else self.sea_sp)
            if d0 < dist[i]:
                dist[i] = d0
                lab[i] = k
                heap.append((d0, i))
        heapq.heapify(heap)
        pop, push = heapq.heappop, heapq.heappush
        while heap:
            d, i = pop(heap)
            if d > dist[i] or wall[i]:
                continue                                   # a river cell is entered, never crossed
            k, di, x = lab[i], dom[i], i % W2
            ci = cost[i]
            for j in ((i - 1) if x else -1, (i + 1) if x < W2 - 1 else -1, i - W2, i + W2):
                if 0 <= j < W2 * H2 and dom[j] == di:
                    nd = d + (ci + cost[j]) * 0.5
                    if nd < dist[j]:
                        dist[j] = nd
                        lab[j] = k
                        push(heap, (nd, j))
        return lab

    # ------------------------------------------------------------ terrain and borders
    def make_terrain(self):
        rng, n, W, cfg = self.rng, self.n, self.W, self.cfg
        C = cfg.CLASSES
        shares = [Counter() for _ in range(n)]
        clsd = self.cls.tobytes()
        for i in range(0, len(self.lab), 3):                 # every third pixel is plenty
            shares[self.lab[i]][C[clsd[i]]] += 1
        dom_of = [self.dom[c] for c in self.cent_idx]
        self.terr = []
        for k in range(n):
            tot = max(1, sum(shares[k].values()))
            fc = {c: shares[k][c] / tot for c in C}         # by picture class
            ft = Counter()                                  # by terrain kind
            for c, v in fc.items():
                ft[self.terrain_of.get(c, "plain")] += v
            name = self.names.get(k, "")
            t = None
            if not dom_of[k]:
                t = "lake" if self.wcomp[self.cent_idx[k]] in self.lake_comps else "sea"
            else:
                for words, kind, cname, thr in getattr(cfg, "NAME_TERRAIN", []):
                    if any(w in name for w in words) and fc.get(cname, 0) + (ft[kind] if cname not in fc else 0) >= thr:
                        t = kind
                        break
            if t is None:
                if ft["mountain"] >= 0.42:
                    t = "mountain"
                elif ft["forest"] >= 0.3:
                    t = "forest"
                elif ft["swamp"] >= 0.35:
                    t = "swamp"
                elif ft["waste"] >= 0.4:
                    t = "waste"
                elif ft["highland"] + ft["mountain"] >= 0.35:
                    t = "highland"
                else:
                    t = "plain"
            self.terr.append(t)
            if dom_of[k] and t != "plain":
                # mixed land: a second terrain that covers a good share joins the first
                for t2 in ("forest", "highland", "swamp", "waste", "mountain"):
                    share = ft[t2] + (ft["mountain"] if t2 == "highland" else 0)
                    if t2 != t and share >= 0.15 and frozenset((t, t2)) not in BAD_MIX:
                        self.extra[k] = self.extra.get(k, 0) | MG.BIT[t2]
            elif dom_of[k]:
                for t2 in ("forest", "highland", "swamp", "waste"):   # wooded, hilly, marshy, barren plains
                    if ft[t2] >= 0.18:
                        self.extra[k] = self.extra.get(k, 0) | MG.BIT[t2]
            if dom_of[k]:
                for c, bit in getattr(cfg, "EXTRA_BITS", {}).items():
                    if fc.get(c, 0) >= 0.3:
                        self.extra[k] = self.extra.get(k, 0) | bit
        lore = getattr(cfg, "LORE", {})
        for k in range(n):
            if dom_of[k]:
                c = lore.get(self.realm.get(k), {}).get("climate")
                if c:
                    self.extra[k] = (self.extra.get(k, 0) & ~(2 ** 30 | 2 ** 31)) | (2 ** 31 if c == "cold" else 2 ** 30)
        land = {k for k in range(n) if self.terr[k] not in MG.WATER}
        sea = set(range(n)) - land
        for k in sea:                                        # open ocean far from any coast
            if self.terr[k] == "sea" and not self.adj[k] & land:
                self.terr[k] = "deep"
        self.land, self.sea = land, sea
        order = sorted(land, key=lambda p: self.area[p])
        self.small = set(order[:round(0.1 * len(order))])
        self.large = set(order[-round(0.2 * len(order)):])
        # adventure sites: many sites in their province
        self.site_prov = []
        for num, x, y, text in getattr(cfg, "SITES", []):
            k = self.lab[min(self.H - 1, int(y)) * W + min(W - 1, int(x))]
            self.extra[k] = self.extra.get(k, 0) | MANY_SITES
            self.site_prov.append((num, x, y, text, k))
        # borders: rivers where the border runs along a river; mountains through ranges
        near_riv = Image.frombytes("L", (self.W, self.H), bytes(255 if v else 0 for v in self.river_full))
        near_riv = near_riv.filter(ImageFilter.MaxFilter(9)).tobytes()
        mtn = {i for i, c in enumerate(C) if self.terrain_of.get(c) == "mountain"}
        self.spec = {}
        lp = sorted(p for p in self.pairs if p[0] in land and p[1] in land)
        cand_mtn = []
        for p in lp:
            pts = self.bpts[p]
            rshare = sum(1 for x, y in pts if near_riv[y * W + x]) / len(pts)
            mshare = sum(1 for x, y in pts if clsd[y * W + x] in mtn) / len(pts)
            if rshare >= 0.45:
                self.spec[p] = "river"
            elif mshare >= 0.6:
                cand_mtn.append(p)
        rng.shuffle(cand_mtn)
        pieces = self.parts(land)                           # islands are pieces of their own
        for p in cand_mtn:
            kind = "impassable" if rng.random() < 0.5 else "pass"
            if kind == "impassable":
                cut = frozenset({q for q, v in self.spec.items() if v == "impassable"} | {p})
                if self.parts(land, cut) > pieces:
                    kind = "pass"
            self.spec[p] = kind
        # farms: plains along rivers and lakes, and plains around capitals
        caps = Counter(self.lab[y * W + x] for x, y, kind in self.cities if kind == "capital")
        for k in sorted(land):
            if self.terr[k] == "plain":
                wet = any(self.spec.get((min(k, b), max(k, b))) == "river" or self.terr[b] == "lake" for b in self.adj[k])
                if (wet and rng.random() < 0.25) or caps[k]:
                    self.terr[k] = "farm"
        # starts spread over good land, thrones away from them
        good = sorted(k for k in land if self.terr[k] in ("plain", "farm", "forest", "highland")
                      and k not in self.small and not self.extra.get(k, 0) & (2 ** 31))
        landg = set(land)
        starts = [rng.choice(good)]
        while len(starts) < self.players:
            d = self.dist_from(starts, landg)
            far = max(d.get(p, 0) for p in good if p not in starts)
            starts.append(rng.choice([p for p in good if p not in starts and d.get(p, 0) == far]))
        self.starts = starts
        thr = []
        dstart = self.dist_from(starts, landg)
        for _ in range(max(1, self.players - 1)):
            dthr = self.dist_from(thr, landg) if thr else {}
            cand = [p for p in sorted(land) if p not in starts and p not in thr and dstart.get(p, 0) >= 2]
            cand.sort(key=lambda p: (-(dstart.get(p, 0) * 3 + min(dthr.get(p, 9), 9)), rng.random()))
            thr.append(cand[0])
        self.thrones = thr

    def mask(self, k, look=None):
        return super().mask(k, look) | self.extra.get(k, 0)

    def description(self):
        what = ("redrawn in Claude's map style" if self.mode == "replica"
                else "with the original picture as the map")
        sites = f", {len(self.site_prov)} adventure sites (many magic sites)" if self.site_prov else ""
        return (f"{self.cfg.TITLE}, {what}. Made by Claude's from_image.py prototype (seed {self.seed}): "
                f"{len(self.land)} land and {len(self.sea)} water provinces, {self.players} starts, "
                f"{len(self.thrones)} thrones{sites}. Borders follow the picture's coasts and rivers.")

    def extra_lines(self, num):
        L = ["#maptextcol 0.0 0.0 0.0 1.0"]                # black province names
        if self.mode == "picture":
            L.append("#nonamefilter")                       # the picture prints its own place names
        L += [f"-- adventure site {s} in province {num[k]}: {text}" for s, x, y, text, k in self.site_prov]
        return L + [""]

    def province_lines(self, num):
        """Lore: population type, population, forts, specific magic sites per province."""
        cfg, W = self.cfg, self.W
        lore = getattr(cfg, "LORE", {})
        if not lore and not getattr(cfg, "SITE_FEATURES", None):
            return []
        towns, caps = Counter(), Counter()
        for x, y, kind in self.cities:
            (caps if kind == "capital" else towns)[self.lab[y * W + x]] += 1
        # realm population spread over its land provinces by area, towns and capitals pull more
        weight = {k: self.area[k] * (1 + 0.35 * towns[k] + 1.0 * caps[k]) for k in self.land}
        members = {}
        for k in self.land:
            members.setdefault(self.realm.get(k), []).append(k)
        popscale = getattr(cfg, "POP_SCALE", 0.02)          # Dominions people per realm person
        block = {k: [] for k in range(self.n)}
        for r, ks in members.items():
            L = lore.get(r, {})
            tot = sum(weight[k] for k in ks)
            for k in ks:
                if "poptype" in L:
                    block[k].append(f"#poptype {L['poptype']}")
                if "people" in L and k not in self.starts:
                    pop = int(L["people"] * popscale * weight[k] / max(1, tot))
                    block[k].append(f"#population {max(500, min(40000, pop // 100 * 100))}")
                if caps[k] and k not in self.starts and "fort" in L:
                    block[k].append(f"#fort {L['fort']}")
        for k in self.sea:
            L = lore.get(self.realm.get(k), {})
            if "poptype" in L:
                block[k].append(f"#poptype {L['poptype']}")
        for snum, x, y, text, k in self.site_prov:
            for sid in getattr(cfg, "SITE_FEATURES", {}).get(snum, []):
                if f"#feature {sid}" not in block[k]:
                    block[k].append(f"#feature {sid}")
        out = ["", "-- lore: population types, populations, forts and adventure sites"]
        for k in sorted(range(self.n), key=lambda k: num[k]):
            if block[k]:
                out.append(f"#setland {num[k]}  -- {self.names.get(k, '')} ({self.realm.get(k, '')})")
                out += block[k]
        return out

    def image_jobs(self):
        if self.mode == "picture":
            return [("", None, False), ("_winter", None, True)]
        return super().image_jobs()

    # ------------------------------------------------------------ art
    def render(self, look=None, winter=False):
        return self.render_picture(winter) if self.mode == "picture" else self.render_replica(look, winter)

    def masks(self):
        W, H, n = self.W, self.H, self.n
        labimg = Image.frombytes("L", (W, H), self.lab)
        landk = [255 if k < n and self.terr[k] not in MG.WATER else 0 for k in range(256)]
        landm = labimg.point(landk)
        bmask = ImageChops.difference(labimg.filter(ImageFilter.MaxFilter(3)), labimg.filter(ImageFilter.MinFilter(3)))
        bmask = bmask.point(lambda v: 255 if v else 0)
        return labimg, landm, bmask

    def special_borders(self, d, winter, picture=False):
        for p, v in sorted(self.spec.items()):
            pts = self.ordered(p)
            if v in ("pass", "impassable") and not picture:
                L = len(pts)
                for i in range(0, L, 9):
                    if v == "pass" and 0.35 * L < i < 0.65 * L:
                        continue
                    x, y = pts[i]
                    MG.draw_mountain(d, x, y, 8 + (i * 7919 % 4), winter)
                if v == "pass":
                    x, y = pts[L // 2]
                    d.line([(x - 6, y - 3), (x + 6, y + 3)], fill=(150, 112, 70), width=3)
            elif v in ("pass", "impassable"):
                for i in range(0, len(pts) - 1, 2 if v == "impassable" else 8):
                    seg = pts[i:i + (2 if v == "impassable" else 5)]
                    if len(seg) > 1:
                        d.line(seg, fill=(150, 30, 30), width=3)

    def render_picture(self, winter):
        W, H = self.W, self.H
        labimg, landm, bmask = self.masks()
        img = self.src.copy()
        if winter:
            snow = MG.smooth_noise(W, H, 40, random.Random(self.seed + 3)).point(lambda v: 110 + v // 3)
            img = Image.composite(Image.new("RGB", (W, H), (236, 240, 246)), img, ImageChops.multiply(snow, landm))
        # land-land borders dark, sea borders pale; the coast is already on the picture
        coast = ImageChops.subtract(landm.filter(ImageFilter.MaxFilter(3)), landm.filter(ImageFilter.MinFilter(3)))
        inner_land = ImageChops.subtract(ImageChops.multiply(bmask, landm), coast)
        inner_sea = ImageChops.subtract(ImageChops.multiply(bmask, ImageChops.invert(landm)), coast)
        img = Image.composite(Image.blend(img, Image.new("RGB", (W, H), (40, 30, 24)), 0.75), img, inner_land)
        img = Image.composite(Image.blend(img, Image.new("RGB", (W, H), (230, 240, 250)), 0.6), img, inner_sea)
        self.special_borders(ImageDraw.Draw(img), winter, picture=True)
        return self.finish(img)

    def render_replica(self, look, winter):
        W, H, n, C = self.W, self.H, self.n, self.cfg.CLASSES
        rng = random.Random(self.seed * 7 + 1)
        labimg, landm, bmask = self.masks()
        ground = dict(MG.GROUND)
        ground["mountain"] = ((118, 100, 80), (158, 138, 110))
        ground["lake"] = ((70, 120, 160), (100, 150, 186))
        ground["deep"] = ((40, 80, 126), (66, 110, 156))
        ground.update(CLASS_GROUND)
        gkey = {c: (c if c in CLASS_GROUND else self.terrain_of.get(c, "plain")) for c in C}
        noise = Image.blend(MG.smooth_noise(W, H, 60, rng), MG.smooth_noise(W, H, 14, rng), 0.35)
        cls = self.cls
        farmm = labimg.point([255 if k < n and self.terr[k] == "farm" else 0 for k in range(256)])
        img = Image.new("RGB", (W, H))
        layers = {}
        for ci, cname in enumerate(C):
            layers.setdefault(look or gkey[cname], []).append(ci)
        plains_ci = [i for i, c in enumerate(C) if self.terrain_of.get(c) == "plain" and c not in ("sea", "frame")]
        for t, cis in layers.items():
            m = ImageChops.multiply(cls.point([255 if v in cis else 0 for v in range(256)]), landm)
            img.paste(self.tex(noise, ground[t]), mask=m)
        if not look:
            pm = cls.point([255 if v in plains_ci else 0 for v in range(256)])
            img.paste(self.tex(noise, ground["farm"]), mask=ImageChops.multiply(ImageChops.multiply(farmm, landm), pm))
        for t in ("sea", "lake", "deep"):
            m = labimg.point([255 if k < n and self.terr[k] == t else 0 for k in range(256)])
            img.paste(self.tex(noise, ground[t]), mask=m)
        # props, sorted top to bottom; none on borders, province dots, cities or site markers
        far = bmask.filter(ImageFilter.MaxFilter(15)).load()
        lpx, cpx, rpx = labimg.load(), cls.load(), self.river_full
        keepout = set()
        for x, y in self.dot + [(c[0], c[1]) for c in self.cities] + [(s[1], s[2]) for s in self.site_prov]:
            for dx in range(-20, 21, 4):
                for dy in range(-20, 21, 4):
                    keepout.add(((int(x) + dx) // 4, (int(y) + dy) // 4))
        per = {"forest": 230, "plain": 420, "farm": 800, "highland": 650, "mountain": 330, "swamp": 420,
               "waste": 520, "sea": 900, "lake": 900, "deep": 1400, "desert": 700, "jungle": 200, "ice": 900}
        props = []
        prng = random.Random(self.seed * 1000)
        for _ in range(int(W * H / 230)):
            x, y = prng.randrange(4, W - 4), prng.randrange(14, H - 2)
            k = lpx[x, y]
            if far[x, y] or (x // 4, y // 4) in keepout or rpx[y * W + x]:
                continue
            t = self.terr[k]
            if t not in MG.WATER:
                t = look or gkey[C[cpx[x, y]]]
                if t == "plain" and not look and self.terr[k] == "farm":
                    t = "farm"
            if prng.random() > 230 / per[t]:
                continue
            props.append((y, x, t, prng.random(), prng.random()))
        props.sort()
        d = ImageDraw.Draw(img)
        for y, x, t, r1, r2 in props:
            if t == "mountain":
                MG.draw_mountain(d, x, y, 6 + int(r1 * 5), winter)
            elif t == "jungle":
                MG.draw_prop(d, "forest", x, y, r1, 0.7 + 0.3 * r2)      # broadleaf only
            elif t == "desert":
                w = 7 + r1 * 7
                d.arc([x - w, y - 4, x + w, y + 4], 190, 350, fill=(196, 170, 112), width=2)
            elif t == "ice":
                MG.draw_prop(d, "waste", x, y, r1, 0.2)                  # rocks
            else:
                MG.draw_prop(d, "sea" if t in MG.WATER else t, x, y, r1, r2)
        if winter:
            snow = noise.point(lambda v: 150 + v // 3)
            img = Image.composite(Image.new("RGB", (W, H), (232, 236, 242)), img, ImageChops.multiply(snow, landm))
            sea = ImageChops.invert(landm)
            img = Image.composite(Image.blend(img, Image.new("RGB", (W, H), (120, 140, 156)), 0.35), img, sea)
        foam = ImageChops.subtract(landm.filter(ImageFilter.MaxFilter(7)), landm)
        img.paste((168, 200, 214) if not winter else (200, 214, 222), mask=foam)
        inner = ImageChops.multiply(bmask, landm)
        img = Image.composite(Image.blend(img, Image.new("RGB", (W, H), MG.INK), 0.7), img, inner)
        # the picture's rivers (thin), river borders (wide), mountain borders
        riv = ImageChops.multiply(Image.frombytes("L", (W, H), bytes(255 if v else 0 for v in self.river_full)), landm)
        img.paste((40, 70, 110), mask=riv.filter(ImageFilter.MaxFilter(3)))
        img.paste((66, 112, 168) if not winter else (150, 180, 205), mask=riv)
        d = ImageDraw.Draw(img)
        for p, v in sorted(self.spec.items()):
            if v == "river":
                pts = self.ordered(p)[::3]
                if len(pts) > 1:
                    d.line(pts, fill=(40, 70, 110), width=7, joint="curve")
                    d.line(pts, fill=(66, 112, 168) if not winter else (150, 180, 205), width=5, joint="curve")
        self.special_borders(d, winter)
        for x, y, kind in self.cities:
            draw_city(d, x, y, kind == "capital", winter)
        for num, x, y, text, k in self.site_prov:
            draw_site(d, int(x), int(y), num)
        return self.finish(img)

    @staticmethod
    def tex(noise, colours):
        dark, light = colours
        return Image.merge("RGB", [noise.point(lambda v, a=dark[c], b=light[c]: int(a + (b - a) * v / 255))
                                   for c in range(3)])

    def finish(self, img):
        r, g, b = img.split()
        img = Image.merge("RGB", (r.point(lambda v: 254 if v == 255 else v), g, b))
        px = img.load()
        for x, y in self.dot:
            px[x, y] = (255, 255, 255)
        return img


def draw_city(d, x, y, capital, winter):
    roof = (150, 70, 50) if not winter else (226, 230, 236)
    if capital:                                              # walled town with a keep and a flag
        d.rectangle([x - 9, y - 6, x + 9, y + 3], fill=(196, 180, 150), outline=MG.INK)
        for cx in range(x - 9, x + 9, 4):
            d.rectangle([cx, y - 8, cx + 2, y - 6], fill=(196, 180, 150), outline=MG.INK)
        d.rectangle([x - 3, y - 15, x + 3, y - 6], fill=(214, 200, 170), outline=MG.INK)
        d.polygon([(x - 4, y - 15), (x, y - 21), (x + 4, y - 15)], fill=roof, outline=MG.INK)
        d.line([(x, y - 21), (x, y - 27)], fill=MG.INK)
        d.polygon([(x, y - 27), (x + 6, y - 25), (x, y - 23)], fill=(200, 40, 40))
        d.rectangle([x - 1, y - 2, x + 1, y + 3], fill=MG.INK)
    else:                                                    # a few houses
        for dx, dy in ((-4, 0), (3, -2)):
            hx, hy = x + dx, y + dy
            d.rectangle([hx - 3, hy - 3, hx + 3, hy + 2], fill=(206, 190, 150), outline=MG.INK)
            d.polygon([(hx - 4, hy - 3), (hx, hy - 7), (hx + 4, hy - 3)], fill=roof, outline=MG.INK)


def draw_site(d, x, y, num):
    """A small parchment tag with the adventure number, like the boxes on the picture."""
    t = str(num)
    w = 5 + 6 * len(t)
    d.rectangle([x - w // 2 - 1, y - 8, x + w // 2 + 1, y + 7], fill=(120, 30, 30))
    d.rectangle([x - w // 2 + 1, y - 6, x + w // 2 - 1, y + 5], fill=(246, 236, 200))
    d.text((x - 3 * len(t), y - 6), t, fill=(60, 20, 20))


def main(argv):
    if len(argv) < 3 or argv[0].startswith("-"):
        sys.exit(__doc__)
    image, rep_name, pic_name = argv[:3]
    for nm in (rep_name, pic_name):
        if not nm.replace("_", "").isalpha():
            sys.exit("map names may only use a-z, A-Z and _")

    def opt(k, d):
        return argv[argv.index(k) + 1] if k in argv else d
    cfg = importlib.import_module(opt("--config", "greyhawk_hd"))
    m = ImageMap(image, int(opt("--players", getattr(cfg, "PLAYERS", 8))),
                 int(opt("--land", getattr(cfg, "LAND_SP", 53))), int(opt("--sea", getattr(cfg, "SEA_SP", 90))),
                 int(opt("--seed", random.randrange(10 ** 6))), cfg)
    out = opt("--out", os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"))
    t0 = time.time()
    m.make_provinces()
    print(f"provinces: {m.n} in {time.time() - t0:.1f} s (seed {m.seed}); {len(m.seed_names)} from labels, "
          f"{len(m.names)} named, {len(m.cities)} cities", flush=True)
    m.make_graph()
    print(f"graph in {time.time() - t0:.1f} s", flush=True)
    m.make_terrain()
    print(f"graph: {len(m.pairs)} borders; terrain {dict(Counter(m.terr))}; starts {m.starts}; "
          f"thrones {m.thrones}; special borders {dict(Counter(m.spec.values()))}; "
          f"{len(m.site_prov)} adventure sites", flush=True)
    for mode, nm in (("replica", rep_name), ("picture", pic_name)):
        m.mode, m.name = mode, nm
        m.write(os.path.join(out, nm))
    print(f"done in {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main(sys.argv[1:])
