"""Dominions 6 pretender design calculator: the rules of zollqir.github.io/pretenders-dom6, with
chassis stats from the dom6-inspector skill and modded nations from the dom6-modinspector skill.

  python3 -I pretender.py nations [TEXT]                    nation ids, eras and names
  python3 -I pretender.py nation NATION                     defaults, limits, bless bonus, cheap gods,
                                                            every pretender the nation can take
  python3 -I pretender.py god GOD [--nation NATION]         one chassis: form cost, new path cost,
                                                            paths, dominion, scale attunements, stats
  python3 -I pretender.py design NATION [DESIGN] [--top N] [--all]
        every chassis the nation can take, cheapest first, for the wanted paths/dominion/scales:
        points left, dominion, paths after the purchase, bless points, chassis stats
  python3 -I pretender.py optimize NATION [DESIGN] [--top N]
        the site's Bless Point Optimizer: for each chassis, how to spend the points left on more
        path levels for the most bless points
  python3 -I pretender.py build NATION GOD [DESIGN] [--bless "Name,Name x2,..."]
        one full design: itemised cost, points left, bless points, available blesses, the chosen
        blesses checked, and the AI pretender template (#newtemplate) for a mod
  python3 -I pretender.py blesses PATHS [--scales S] [--bonus N]   blesses those paths allow

DESIGN options (all optional):
  --paths "F4 S4"           wanted path levels (a chassis that already has more keeps its own)
  --dom N                   dominion strength 1-10 (a chassis with more keeps its own)
  --scales "order=2 prod=1 heat=0 growth=1 luck=-1 magic=2"
                            also turmoil, sloth, cold, death, misfortune, drain (= the negative);
                            unset scales stay at the nation's default (free)
  --prison awake|dormant|imprisoned     (+0, +150, +350 points)
  --chassis humanoid,monster,titan,immobile   the site's classes (by base dominion 1-4)
  --mod DIR                 a modded game written by dom6-modinspector (its nations, gods and the
                            nation commands in its .dm files)
  --cost ID=N[,ID=N]        form costs the data lacks (autocalculated modded gods: read them in game)
NATION is an id (5) or a name ("EA Arcoscephale", "ulm" lists the Ulms); 0 = any nation.
GOD is an id or a name.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
INSPECTOR = os.path.normpath(os.path.join(HERE, "..", "..", "dom6-inspector", "data"))
PATHS = "fawesdngb"
PATHNAME = dict(zip(PATHS, ["Fire", "Air", "Water", "Earth", "Astral", "Death", "Nature", "Glamour", "Blood"]))
SCALES = ["order", "productivity", "heat", "growth", "fortune", "magic"]
SCALE_ALIAS = {"order": ("order", 1), "turmoil": ("order", -1), "chaos": ("order", -1),
               "prod": ("productivity", 1), "productivity": ("productivity", 1), "sloth": ("productivity", -1),
               "heat": ("heat", 1), "cold": ("heat", -1), "growth": ("growth", 1), "death": ("growth", -1),
               "luck": ("fortune", 1), "fortune": ("fortune", 1), "misfortune": ("fortune", -1),
               "magic": ("magic", 1), "drain": ("magic", -1)}
MORE = {"order": "moreorder", "productivity": "moreprod", "heat": "moreheat", "growth": "moregrowth",
        "fortune": "moreluck", "magic": "moremagic"}
SHORT = {"order": "Ord", "productivity": "Prd", "heat": "Heat", "growth": "Grw", "fortune": "Luck", "magic": "Mag"}
PRISON = {"awake": 0, "dormant": 1, "imprisoned": 2, "0": 0, "1": 1, "2": 2}
PRISON_POINTS = [0, 150, 350]
CHASSIS = {"humanoid": 1, "monster": 2, "titan": 3, "immobile": 4}
CHASSIS_NAME = {v: k for k, v in CHASSIS.items()}
POINTS = 450
FLAGS = ["immobile", "flying", "immortal", "domimmortal", "regeneration", "ethereal", "invulnerable",
         "amphibian", "pooramphibian", "aquatic", "stealthy", "trample", "fear", "awe", "undead", "demon",
         "inanimate", "spiritsight", "blind", "mastersmith", "triplegod"]


def load(fn, base=DATA):
    return json.load(open(os.path.join(base, fn), encoding="utf-8"))


def num(v, default=0):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return default


def records(base, kind):
    p = os.path.join(base, "records", kind + ".jsonl")
    if not os.path.exists(p):
        return {}
    out = {}
    for line in open(p, encoding="utf-8"):
        d = json.loads(line)
        out.setdefault(str(d.get("id")).split(".")[0], d)        # skip the site's .01 duplicates
    return out


# ---------------------------------------------------------------- data (site + inspector + mods)

class Game:
    def __init__(self, mod=None, costs=None):
        self.notes = []
        self.pret = load("pretenders.json")
        for pid, c in load("pretender_costs.json").items():
            if c.get("pointcost") is None:
                self.pret.pop(pid, None)
            elif pid in self.pret:
                self.pret[pid]["pointcost"] = c["pointcost"]
        self.nations = load("nations.json")
        npret = load("nations_pretenders.json")
        remove = load("pretenders_to_remove.json")
        fix = load("nation_scales_to_fix.json")
        for nid, n in self.nations.items():
            n["scalelimits"] = n.get("scalelimits") or {}
            n["scales"] = n.get("scales") or {}
            n["bless_bonus"] = n.get("bless_bonus") or 0
            n["cheap_gods"] = n.get("cheap_gods") or {}
            n["pretenders"] = [p for p in npret.get(nid, []) if p not in remove.get(nid, [])]
            n["scales"].update(fix.get(nid, {}))
        self.units = records(INSPECTOR, "units")
        if mod:
            self.load_mod(mod)
        self.nations["0"] = {"id": "0", "name": "Any nation", "epithet": None, "era": None, "scalelimits": {},
                             "scales": {}, "bless_bonus": 0, "cheap_gods": {},
                             "pretenders": sorted({p for n in self.nations.values() for p in n["pretenders"]}, key=int)}
        for pid, c in (costs or {}).items():
            if pid in self.pret:
                self.pret[pid]["pointcost"] = c

    def load_mod(self, mod):
        """Modded game from dom6-modinspector: nations' god lists, modded gods and nation commands."""
        units = records(mod, "units")
        self.units.update(units)
        for uid, u in units.items():
            if not u.get("startdom") and not (u.get("pathcost") and u.get("typechar") == "Pretender"):
                continue
            old = self.pret.get(uid, {})
            p = {"id": uid, "name": u.get("name"), "startdom": num(u.get("startdom"), 1),
                 "pathcost": num(u.get("pathcost"), 10) or 10, "minprison": num(u.get("minprison"))}
            for s, k in MORE.items():
                p[k] = num(u.get(k))
            mp = dict(re.findall(r"([FAWESDNGB])(\d+)", str(u.get("mpath") or "")))
            for c in PATHS:
                p[c] = num(mp.get(c.upper()))
            g = num(u.get("gcost"), 10000)
            if g and g < 5000:
                p["pointcost"] = g
            elif "pointcost" in old:
                p["pointcost"] = old["pointcost"]
                if u.get("modded"):
                    self.notes.append(f"{p['name']} ({uid}) is changed by the mod; its form cost is the vanilla one")
            self.pret[uid] = p
        for nid, n in records(mod, "nations").items():
            pl = n.get("pretenders") or []
            if isinstance(pl, str):
                pl = json.loads(pl)
            base = self.nations.get(nid, {"id": nid, "scalelimits": {}, "scales": {}, "bless_bonus": 0, "cheap_gods": {}})
            base.update({"id": nid, "name": n.get("name"), "epithet": n.get("epithet"),
                         "era": {"1": "EA", "2": "MA", "3": "LA"}.get(str(n.get("era")), n.get("eracode")),
                         "pretenders": [str(p) for p in pl if str(p) in self.pret]})
            self.nations[nid] = base
        info = os.path.join(mod, "mods.json")
        for dm in (json.load(open(info))["mods"] if os.path.exists(info) else []):
            self.read_dm(dm)

    def read_dm(self, path):
        raw = open(path, "rb").read()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("latin-1")
        byname = {}
        for pid, p in self.pret.items():
            byname.setdefault(str(p.get("name", "")).lower(), pid)
        nation = None
        for line in text.splitlines():
            line = line.split("--")[0].strip()
            m = re.match(r"#(\w+)\s*(.*)", line)
            if not m:
                continue
            cmd, arg = m.group(1).lower(), m.group(2).strip()
            if cmd == "selectnation":
                nation = self.nations.get(arg)
                continue
            if cmd == "end" or nation is None:
                if cmd == "end":
                    nation = None
                continue
            ref = arg.strip('"')
            ref = ref if ref.isdigit() else byname.get(ref.lower(), ref)
            if cmd in ("cheapgod20", "cheapgod40"):
                nation["cheap_gods"][ref] = int(cmd[-2:])
            elif cmd == "blessbonus":
                nation["bless_bonus"] = num(arg)
            elif cmd.endswith("blessbonus"):
                self.notes.append(f"{nation.get('name')}: #{cmd} {arg} (extra bless points for one path only; not counted here)")
            elif cmd == "idealcold":
                nation["scales"]["heat"] = -num(arg)
            elif cmd in ("defchaos", "defsloth", "defdeath", "defmisfortune", "defdrain"):
                key = {"defchaos": "order", "defsloth": "productivity", "defdeath": "growth",
                       "defmisfortune": "fortune", "defdrain": "magic"}[cmd]
                nation["scales"][key] = -num(arg)
            elif cmd == "clearnation":
                nation["cheap_gods"], nation["bless_bonus"] = {}, 0

    # lookups
    def nation(self, q):
        q = str(q).strip()
        if q in self.nations:
            return self.nations[q]
        ql = q.lower()
        full = {nid: f"{n.get('era') or ''} {n.get('name')}".strip().lower() for nid, n in self.nations.items()}
        hits = [nid for nid, f in full.items() if f == ql] or [nid for nid, f in full.items() if ql in f]
        if len(hits) != 1:
            print(f"{len(hits)} nations match {q!r}:" if hits else f"no nation matches {q!r}")
            for nid in hits:
                print(f"  {nid:>4}  {full[nid]}")
            sys.exit(1)
        return self.nations[hits[0]]

    def god(self, q):
        q = str(q).strip()
        if q in self.pret:
            return self.pret[q]
        ql = q.lower()
        hits = [pid for pid, p in self.pret.items() if str(p.get("name", "")).lower() == ql] or \
               [pid for pid, p in self.pret.items() if ql in str(p.get("name", "")).lower()]
        if len(hits) != 1:
            print(f"{len(hits)} gods match {q!r} (give the id):" if hits else f"no god matches {q!r}")
            for pid in sorted(hits, key=int):
                print(f"  {pid:>5}  {self.pret[pid]['name']}  {paths_str(self.pret[pid])}")
            sys.exit(1)
        return self.pret[hits[0]]


# ---------------------------------------------------------------- the site's rules

def path_cost(base, newcost, level):
    """Cost of raising one path from the chassis' BASE to LEVEL: 8, 16, 24... per level bought;
    the first level of a path the chassis lacks costs its new path cost."""
    base = base or 0
    if level <= base:
        return 0
    if base:
        newcost, level = 8, level - base
    return newcost + 8 * (level * (level + 1) // 2 - 1)


def magic_cost(p, paths):
    return sum(path_cost(p.get(c, 0), p.get("pathcost", 10), paths.get(c, 0)) for c in PATHS)


def dom_cost(startdom, dom):
    startdom = startdom or 1
    if dom <= startdom:
        return 0
    k = dom - startdom
    return 7 * k * (k + 1) // 2


def scale_costs(nation, scales):
    out = {}
    for s in SCALES:
        d = scales[s] - nation["scales"].get(s, 0)
        out[s] = -abs(d) * 40 if s == "heat" else d * 40      # heat either way from the ideal gives points
    return out


def scale_ok(p, nation, scales):
    """The site's limits: +-2 around 0, moved by the nation's limit and the chassis' attunement
    (a nation limit and a chassis attunement in the same direction do not stack)."""
    for s in SCALES:
        lim, more = nation["scalelimits"].get(s, 0), p.get(MORE[s], 0) or 0
        extra = more if (lim == 0 or (lim < 0) != (more < 0)) else 0
        if not (-2 + lim + extra <= scales[s] <= 2 + lim + extra):
            return False
    return True


def god_cost(p, nation, paths, dom):
    if p.get("pointcost") is None:
        return None
    return p["pointcost"] + magic_cost(p, paths) + dom_cost(p.get("startdom"), dom) - nation["cheap_gods"].get(p["id"], 0)


def effective(p, paths):
    return {c: max(p.get(c, 0) or 0, paths.get(c, 0)) for c in PATHS}


def bless_points(paths, bonus):
    return sum(v - 1 for v in paths.values() if v) + bonus


def bless_list():
    out = []
    for b in load("blesses.json"):
        b = dict(b)
        for c in PATHS:
            b[c] = b.get(c, 0) or 0
        b["cost"] = sum(b[c] for c in PATHS)
        out.append(b)
    return out


def bless_ok(b, paths, scales):
    if any(b[c] > paths.get(c, 0) for c in PATHS):
        return False
    for s, v in (b.get("scales") or {}).items():
        if (v > 0 and scales.get(s, 0) < v) or (v < 0 and scales.get(s, 0) > v):
            return False
    return True


def optimize(known, basep, newcost, bonus, points):
    """The site's Bless Point Optimizer (blessOptimizer.js): for 0, 1, 2... extra new paths, raise the
    cheapest levels while all of them fit; returns the designs with the most bless points."""
    inc = lambda v, b: 8 * (v - b + 1)
    base_bp = sum(known.values()) - len(known) + bonus
    best, best_bp = [], base_bp
    for n in range(0, 9 - len(known) + 1):
        g = {"known": dict(known), "new": [], "bp": base_bp, "left": points}
        if newcost * n > g["left"]:
            break
        g["left"] -= newcost * n
        g["new"] = [1] * n
        while True:
            cheapest, ck, cn = None, [], []
            for c, v in g["known"].items():
                cost = inc(v, basep[c])
                if cost > g["left"]:
                    continue
                if cost == cheapest:
                    ck.append(c)
                elif cheapest is None or cost < cheapest:
                    cheapest, ck, cn = cost, [c], []
            for i, v in enumerate(g["new"]):
                cost = inc(v, 0)
                if cost > g["left"]:
                    continue
                if cost == cheapest:
                    cn.append(i)
                elif cheapest is None or cost < cheapest:
                    cheapest, ck, cn = cost, [], [i]
            if cheapest is not None and cheapest * (len(ck) + len(cn)) <= g["left"]:
                for c in ck:
                    g["left"] -= inc(g["known"][c], basep[c])
                    g["known"][c] += 1
                    g["bp"] += 1
                for i in cn:
                    g["left"] -= inc(g["new"][i], 0)
                    g["new"][i] += 1
                    g["bp"] += 1
                continue
            extra = g["left"] // cheapest if cheapest else 0
            g["bp"] += extra
            g["extra"], g["extra_known"], g["extra_new"] = extra, ck, cn
            g["left"] = g["left"] % cheapest if cheapest else g["left"]
            break
        if g["bp"] < best_bp and best:
            break
        if g["bp"] > best_bp or not best:
            if g["bp"] > best_bp:
                best = []
            best_bp = g["bp"]
        if g["bp"] == best_bp:
            best.append(g)
    return sorted(best, key=lambda g: -g["left"]), best_bp


# ---------------------------------------------------------------- formatting

def paths_str(p):
    return " ".join(f"{c.upper()}{p[c]}" for c in PATHS if p.get(c))


def parse_paths(text):
    out = {c: 0 for c in PATHS}
    for c, v in re.findall(r"([FAWESDNGBfawesdngb])\s*(\d+)", text or ""):
        out[c.lower()] = int(v)
    return out


def parse_scales(text, nation):
    sc = {s: nation["scales"].get(s, 0) for s in SCALES}
    for k, v in re.findall(r"([a-z]+)\s*=\s*(-?\d+)", (text or "").lower()):
        if k not in SCALE_ALIAS:
            sys.exit(f"unknown scale {k!r}: use " + ", ".join(SCALE_ALIAS))
        s, sign = SCALE_ALIAS[k]
        sc[s] = sign * int(v)
    return sc


def scales_str(sc):
    names = {"order": ("Order", "Turmoil"), "productivity": ("Prod", "Sloth"), "heat": ("Heat", "Cold"),
             "growth": ("Growth", "Death"), "fortune": ("Luck", "Misfortune"), "magic": ("Magic", "Drain")}
    return " ".join(f"{names[s][0 if v > 0 else 1]} {abs(v)}" for s, v in sc.items() if v) or "all 0"


def stats(g, pid):
    u = g.units.get(str(pid))
    if not u:
        return ""
    f = [k for k in FLAGS if u.get(k) not in (None, "", "0", 0)]
    return f"hp {u.get('hp')} prot {u.get('prot') or 0} mr {u.get('mr')} sz {u.get('size')} mv {u.get('mapmove') or 0}" + \
           (" " + ",".join(f) if f else "")


def attune(p):
    return ",".join(f"{SHORT[s]}{p.get(MORE[s]):+d}" for s in SCALES if p.get(MORE[s]))


# ---------------------------------------------------------------- commands

def opts(a):
    o = {}
    i = 0
    rest = []
    while i < len(a):
        if a[i].startswith("--") and a[i] not in ("--all",):
            o[a[i][2:]] = a[i + 1]
            i += 2
        else:
            if a[i] == "--all":
                o["all"] = True
            else:
                rest.append(a[i])
            i += 1
    return o, rest


def setup(o, nation):
    paths = parse_paths(o.get("paths"))
    dom = int(o.get("dom", 1))
    if not 1 <= dom <= 10:
        sys.exit("dominion is 1-10")
    sc = parse_scales(o.get("scales"), nation)
    prison = PRISON.get(str(o.get("prison", "awake")).lower())
    if prison is None:
        sys.exit("prison: awake, dormant or imprisoned")
    chassis = {CHASSIS[c.strip()] for c in o["chassis"].split(",")} if o.get("chassis") else set(CHASSIS.values())
    left0 = POINTS + PRISON_POINTS[prison] - sum(scale_costs(nation, sc).values())
    return paths, dom, sc, prison, chassis, left0


def candidates(g, nation, sc, prison, chassis, why=None):
    out = []
    why = why if why is not None else {}
    for pid in nation["pretenders"]:
        p = g.pret.get(pid)
        if not p or (p.get("startdom") or 1) not in chassis:
            continue
        if (p.get("minprison") or 0) > prison:
            why["must sleep longer"] = why.get("must sleep longer", 0) + 1
            continue
        if not scale_ok(p, nation, sc):
            why["scales out of range"] = why.get("scales out of range", 0) + 1
            continue
        out.append(p)
    return out


def nation_head(nation):
    t = f"nation {nation['id']}: {nation.get('era') or ''} {nation.get('name')}" + (f", {nation['epithet']}" if nation.get("epithet") else "")
    lines = [t.replace("  ", " ")]
    if any(nation["scales"].values()):
        lines.append("default scales (free): " + scales_str({s: nation["scales"].get(s, 0) for s in SCALES}))
    if nation["scalelimits"]:
        lines.append("scale limits moved: " + ", ".join(f"{s} {v:+d}" for s, v in nation["scalelimits"].items()))
    if nation["bless_bonus"]:
        lines.append(f"bless bonus: +{nation['bless_bonus']}")
    return lines


def design_header(nation, paths, dom, sc, prison, left0, g):
    sc_cost = scale_costs(nation, sc)
    out = nation_head(nation)
    out.append(f"wanted: paths {paths_str(paths) or 'none'}, dominion {dom}, scales {scales_str(sc)}, "
               f"{['awake', 'dormant', 'imprisoned'][prison]}")
    out.append(f"points: 450 + {PRISON_POINTS[prison]} (sleep) - {sum(sc_cost.values())} (scales: "
               + ", ".join(f"{s} {v:+d}" for s, v in sc_cost.items() if v) + f") = {left0} before the god")
    out += [f"note: {n}" for n in g.notes]
    return out


def cmd_design(g, a, optimizer=False):
    o, rest = opts(a)
    if not rest:
        sys.exit("give a nation")
    nation = g.nation(rest[0])
    paths, dom, sc, prison, chassis, left0 = setup(o, nation)
    top = int(o.get("top", 25))
    print("\n".join(design_header(nation, paths, dom, sc, prison, left0, g)))
    rows, unknown, why = [], [], {}
    for p in candidates(g, nation, sc, prison, chassis, why):
        c = god_cost(p, nation, paths, dom)
        if c is None:
            unknown.append(p)
            continue
        eff = effective(p, paths)
        rows.append((left0 - c, p, eff))
    rows.sort(key=lambda r: -r[0])
    if not optimizer:
        shown = rows if o.get("all") else [r for r in rows if r[0] >= 0][:top]
        print(f"\n{len([r for r in rows if r[0] >= 0])} of {len(rows)} chassis affordable; cheapest first"
              + ("" if o.get("all") or len(shown) == len([r for r in rows if r[0] >= 0]) else f" (top {top}; --top N or --all)"))
        print(" left    id  god                          dom  paths after purchase      bless  attunement     stats")
        for left, p, eff in shown:
            print(f"{left:5} {p['id']:>5}  {p['name'][:28]:28} {max(p.get('startdom') or 1, dom):3}  {paths_str(eff)[:24]:24} "
                  f"{bless_points(eff, nation['bless_bonus']):5}  {attune(p):13}  {stats(g, p['id'])}")
    else:
        out = []
        for left, p, eff in rows:
            if left < 0:
                continue
            known = {c: v for c, v in eff.items() if v}
            basep = {c: (p.get(c) or 0) for c in known}
            gods, bp = optimize(known, basep, p.get("pathcost", 10), nation["bless_bonus"], left)
            out.append((bp, p, gods))
        out.sort(key=lambda r: (-r[0], -r[2][0]["left"]))
        print("\nmost bless points for the points left (the site's optimizer). new paths = extra paths the chassis "
              "lacks, at these levels;\nthen +N = levels still affordable, one each among the listed paths. "
              "Raw points only: see SKILL.md on what they can buy.")
        print("bless  left    id  god                          known paths after        new paths  then +N levels among")
        for bp, p, gods in out[:top]:
            for gd in gods[:1]:
                among = ",".join([c.upper() for c in gd.get("extra_known", [])] + [f"new{i + 1}" for i in gd.get("extra_new", [])])
                print(f"{bp:5} {gd['left']:5} {p['id']:>5}  {p['name'][:28]:28} {paths_str(gd['known'])[:24]:24} "
                      f"{','.join(map(str, gd['new'])) or '-':10} {('+' + str(gd['extra']) + ' among ' + among) if gd.get('extra') else ''}")
    if why:
        print("\nleft out: " + ", ".join(f"{n} {k}" for k, n in why.items())
              + ("; scales go to +-2 (+-1 more on an attuned chassis or nation, see `nation`/`god`)" if "scales out of range" in why else ""))
    if unknown:
        print(f"\nno form cost known (give --cost ID=N from the game's pretender screen): "
              + ", ".join(f"{p['id']} {p['name']}" for p in unknown))


def cmd_build(g, a):
    o, rest = opts(a)
    if len(rest) < 2:
        sys.exit("give a nation and a god")
    nation, p = g.nation(rest[0]), g.god(" ".join(rest[1:]))
    paths, dom, sc, prison, chassis, left0 = setup(o, nation)
    print("\n".join(design_header(nation, paths, dom, sc, prison, left0, g)))
    if p["id"] not in nation["pretenders"]:
        print(f"WARNING: {p['name']} ({p['id']}) is not in this nation's pretender list")
    if (p.get("minprison") or 0) > prison:
        print(f"WARNING: {p['name']} must be at least {['awake', 'dormant', 'imprisoned'][p['minprison']]}")
    if not scale_ok(p, nation, sc):
        print("WARNING: these scales are outside what this chassis and nation allow")
    eff = effective(p, paths)
    print(f"\ngod {p['id']}: {p['name']}  (base dominion {p.get('startdom')}, new path cost {p.get('pathcost')}, "
          f"base paths {paths_str(p) or 'none'}{', attuned ' + attune(p) if attune(p) else ''})")
    print("  " + stats(g, p["id"]))
    if p.get("pointcost") is None:
        sys.exit("no form cost known: give --cost ID=N")
    disc = nation["cheap_gods"].get(p["id"], 0)
    print(f"  form {p['pointcost']}" + (f", nation discount -{disc}" if disc else ""))
    total = p["pointcost"] - disc
    for c in PATHS:
        pc = path_cost(p.get(c, 0), p.get("pathcost", 10), paths.get(c, 0))
        if pc:
            print(f"  {PATHNAME[c]} {p.get(c, 0) or 0} -> {paths[c]}: {pc}")
            total += pc
    dc = dom_cost(p.get("startdom"), dom)
    if dc:
        print(f"  dominion {p.get('startdom')} -> {dom}: {dc}")
        total += dc
    left = left0 - total
    print(f"  god total {total}; points left {left}" + ("   OVER BUDGET" if left < 0 else ""))
    bp = bless_points(eff, nation["bless_bonus"])
    print(f"\npaths {paths_str(eff)}, dominion {max(p.get('startdom') or 1, dom)}, scales {scales_str(sc)}")
    print(f"bless points {bp} (each path level above 1" + (f", +{nation['bless_bonus']} nation bonus" if nation["bless_bonus"] else "") + ")")
    bl = bless_list()
    if o.get("bless"):
        used = 0
        byname = {b["name"].lower(): b for b in bl}
        for item in o["bless"].split(","):
            m = re.match(r"\s*(.*?)\s*(?:x(\d+))?\s*$", item)
            name, n = m.group(1).lower(), int(m.group(2) or 1)
            b = byname.get(name)
            if not b:
                print(f"  ?? unknown bless {name!r}")
                continue
            ok = bless_ok(b, eff, sc)
            if n > 1 and not b.get("multi"):
                print(f"  !! {b['name']} can only be taken once")
            used += b["cost"] * n
            print(f"  {'ok' if ok else 'NOT AVAILABLE'}  {b['name']}{' x' + str(n) if n > 1 else ''}: {b['cost'] * n} pts  ({b['shortDescription']})")
        print(f"  blesses use {used} of {bp}" + ("   TOO MANY" if used > bp else ""))
    avail = [b for b in bl if bless_ok(b, eff, sc)]
    print(f"\navailable blesses ({len(avail)}; cost = path requirement sum, * = incarnate only, + = can take several):")
    for b in sorted(avail, key=lambda b: (-b["cost"], b["name"])):
        print(f"  {b['cost']:2}  {b['name']}{' *' if b.get('incarnate') else ''}{' +' if b.get('multi') else ''}: {b['shortDescription']}"
              + ("   (costs more than the bless points)" if b["cost"] > bp else ""))
    print("\nAI template (mod file):")
    print(template(nation, p, eff, dom, prison, sc, o.get("bless")))


def template(nation, p, eff, dom, prison, sc, blesses):
    lines = [f"#newtemplate {nation['id']}", f'#form "{p["name"]} ({p["id"]})"', f"#prison {prison}"]
    lines += [f"#magic {i} {eff[c]}" for i, c in enumerate(PATHS) if eff[c]]
    lines.append(f"#domstr {max(p.get('startdom') or 1, dom)}")
    lines += [f"#scale {i} {-sc[s]}" for i, s in enumerate(SCALES) if sc[s]]   # template scales: + = Turmoil, Sloth, Cold...
    for item in (blesses or "").split(","):
        m = re.match(r"\s*(.*?)\s*(?:x(\d+))?\s*$", item)
        if m.group(1):
            lines += [f'#bless "{m.group(1)}"'] * int(m.group(2) or 1)
    lines.append("#end")
    return "\n".join(lines)


def cmd_nation(g, a):
    nation = g.nation(" ".join(a))
    print("\n".join(nation_head(nation)))
    if nation["cheap_gods"]:
        print("cheap gods: " + ", ".join(f"{g.pret[k]['name'] if k in g.pret else k} ({k}) -{v}" for k, v in nation["cheap_gods"].items()))
    print(f"\n{len(nation['pretenders'])} gods (form cost, base dominion, new path cost, paths, attunement):")
    for pid in sorted(nation["pretenders"], key=lambda k: (g.pret.get(k, {}).get("startdom") or 0, int(k))):
        p = g.pret.get(pid)
        if not p:
            continue
        disc = nation["cheap_gods"].get(pid, 0)
        cost = "?" if p.get("pointcost") is None else p["pointcost"] - disc
        print(f"  {pid:>5}  {p['name'][:28]:28} {cost!s:>4}  dom {p.get('startdom')}  new {p.get('pathcost'):3}  "
              f"{paths_str(p)[:18]:18} {attune(p)}{'  min ' + ['awake', 'dormant', 'imprisoned'][p['minprison']] if p.get('minprison') else ''}")


def cmd_god(g, a):
    o, rest = opts(a)
    p = g.god(" ".join(rest))
    print(f"god {p['id']}: {p['name']}")
    print(f"  form cost {p.get('pointcost', '?')}, base dominion {p.get('startdom')} ({CHASSIS_NAME.get(p.get('startdom'), '?')} class), "
          f"new path cost {p.get('pathcost')}, paths {paths_str(p) or 'none'}")
    if attune(p):
        print(f"  scale attunement: {attune(p)}")
    if p.get("minprison"):
        print(f"  must be at least {['awake', 'dormant', 'imprisoned'][p['minprison']]}")
    print("  " + stats(g, p["id"]))
    nats = [n for n in g.nations.values() if p["id"] in n["pretenders"] and n["id"] != "0"]
    print(f"  {len(nats)} nations: " + ", ".join(f"{n.get('era')} {n['name']}" for n in nats[:40]) + (" ..." if len(nats) > 40 else ""))
    if o.get("nation"):
        n = g.nation(o["nation"])
        print(f"  for {n['name']}: discount {n['cheap_gods'].get(p['id'], 0)}")
    print("  full page: dom6-inspector/scripts/inspector.py unit " + p["id"])


def cmd_blesses(a):
    o, rest = opts(a)
    paths = parse_paths(" ".join(rest))
    sc = {s: 0 for s in SCALES}
    for k, v in re.findall(r"([a-z]+)\s*=\s*(-?\d+)", (o.get("scales") or "").lower()):
        s, sign = SCALE_ALIAS[k]
        sc[s] = sign * int(v)
    bp = bless_points(paths, int(o.get("bonus", 0)))
    print(f"{paths_str(paths)}: {bp} bless points")
    for b in sorted([b for b in bless_list() if bless_ok(b, paths, sc)], key=lambda b: (-b["cost"], b["name"])):
        print(f"  {b['cost']:2}  {b['name']}{' *' if b.get('incarnate') else ''}{' +' if b.get('multi') else ''}: {b['shortDescription']}"
              + ("   (costs more than the bless points)" if b["cost"] > bp else ""))


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd, a = a[0], a[1:]
    if cmd == "blesses":
        return cmd_blesses(a)
    mod = a[a.index("--mod") + 1] if "--mod" in a else None
    costs = {}
    if "--cost" in a:
        for item in a[a.index("--cost") + 1].split(","):
            k, v = item.split("=")
            costs[k.strip()] = int(v)
    for flag in ("--mod", "--cost"):
        if flag in a:
            i = a.index(flag)
            a = a[:i] + a[i + 2:]
    g = Game(mod, costs)
    if cmd == "nations":
        q = " ".join(a).lower()
        for nid, n in sorted(g.nations.items(), key=lambda x: int(x[0])):
            t = f"{n.get('era') or ''} {n.get('name')}"
            if q in t.lower():
                print(f"{nid:>4}  {t}" + (f", {n['epithet']}" if n.get("epithet") else ""))
    elif cmd == "nation":
        cmd_nation(g, a)
    elif cmd == "god":
        cmd_god(g, a)
    elif cmd == "design":
        cmd_design(g, a)
    elif cmd == "optimize":
        cmd_design(g, a, optimizer=True)
    elif cmd == "build":
        cmd_build(g, a)
    else:
        sys.exit(f"unknown command {cmd!r}; see --help")


if __name__ == "__main__":
    main()
