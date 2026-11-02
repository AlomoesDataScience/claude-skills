"""Dominions 6 magic items: measure and sort every forgeable item for Claude's Pythium game.

  python3 -I items.py killing [-n 4000]      weapons, dancing weapons and offensive item spells
  python3 -I items.py protection [-n 4000]   armour, shields, helmets and protective misc items
  python3 -I items.py protection --wearer 42  the same on a Theurg (mage protection)
  python3 -I items.py utility                boosters, penetration, research, gems, movement, command

Items are tried on a Pythium Emerald Lord (#6: hp 15, att 15, str 13, broad sword, plate hauberk,
legionary helmet, tower shield). Killing: the item replaces his sword (a two-handed item also drops
his shield) and he fights fresh Heavy Infantry (sword, #39) and Cataphracts (#1187); the number is
enemies killed a round (all attacks, extra effects on the struck man, dancing weapons' strikes).
Protection: the item replaces the piece in its slot (misc items add their abilities) and Heavy
Infantry attack him; the number is attacks to kill him, against his own kit. Arrows: Archers' (#32)
shots out of 100 that hit and wound. Uses the combat model of dom6-spells (spells.py).
Forgeable: Construction level 1-9 and not another nation's; the forger column is the cheapest
Pythium mage whose paths reach the item (no boosters counted).
"""
import argparse
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "dom6-spells", "scripts"))
import spells  # noqa: E402
from spells import inspector, drn, strike, location, prot_of, load_unit, melee_stats, missile_stats  # noqa: E402

PYTHIUM = "56"
THUG = "6"                                  # Emerald Lord
FORGERS = [("Theurg", "A1W1S2H2"), ("Arch Theurg / Bartholomeus", "A2W2S3H4"),
           ("God (awake)", "E5N5H3")]
CONST_NOW = 0                               # Pythium's Construction level, turn 6
PATHS = "FAWESDNGBH"
SKIN = {"barkskin": 7, "stoneskin": 10, "ironskin": 13}     # spells.natcap keys: caps 10 / 15 / 20


def gems(s):
    return sum(int(n) for n in re.findall(r"(\d+)[FAWESDNGBH]", s or ""))


def forger(mpath):
    need = spells.parse_paths(mpath)
    for name, p in FORGERS:
        have = spells.parse_paths(p)
        if all(have.get(k, 0) >= v for k, v in need.items()):
            return name
    return ""


def forgeable():
    """(record, page) for every item Construction 1-9 that Pythium may forge."""
    pages = {i: b for i, _, b in inspector.pages("items")}
    out = []
    for r in inspector.records("items"):
        if not 1 <= int(r["constlevel"]) <= 9:
            continue
        if r.get("restricted") and PYTHIUM not in [str(x) for x in r["restricted"]]:
            continue
        out.append((r, pages.get(str(r["id"]), "")))
    return out


def page_weapons(block):
    """The item's weapon and its extra effect, parsed from the item page."""
    parts = re.split(r"^Extra effect: .*$", block, flags=re.M)
    ws = []
    for part in parts:
        m = re.search(r"^weap id \[weapon\]: (\d+) \((.*?)\)", part, re.M)
        if not m:
            ws.append(None)
            continue
        g = lambda k, d=0: int(re.search(rf"\[{k}\]: \+?(-?\d+)", part).group(1)) if re.search(rf"\[{k}\]: \+?(-?\d+)", part) else d
        flags = set(re.findall(r"\[(\w+)\]", " ".join(l for l in part.split("\n") if l.startswith("("))))
        ws.append({"id": m.group(1), "name": m.group(2), "dmg": g("dmg"), "att": g("att"), "def": g("def"),
                   "range": g("range"), "natt": g("nratt", 1), "ammo": g("ammo"), "aoe": g("aoe"), "flags": flags})
    return ws[0], (ws[1] if len(ws) > 1 else None)


def attacks_to_kill(att, dmg, flags, extra, D, n):
    """Attacks for one weapon to kill a fresh D; an extra effect lands with every hit."""
    total = 0
    for _ in range(n):
        hp, k = D["hp"], 0
        while hp > 0 and k < 300:
            k += 1
            ra, rd = att + drn(), D["def"] + drn()
            if ra <= rd - D["parry"]:
                continue
            loc = location()
            d = strike(dmg, prot_of(D, {}, loc), flags, {}, hp, D["hp"], loc, {}, ra <= rd, D["shield"])
            if extra:
                d += strike(extra["dmg"], prot_of(D, {}, loc), extra["flags"], {}, hp, D["hp"], loc, {}, False, 0)
            hp -= d
        total += k
    return total / n


def str_dmg(w, s):
    if "nostr" in w["flags"]:
        return w["dmg"]
    return w["dmg"] + (s // 2 if "halfstr" in w["flags"] else s)


def cmd_killing(a):
    T = load_unit(THUG)
    foes = [load_unit("39"), load_unit("1187")]
    base = {"name": "(Emerald Lord's broad sword)", "dmg": 6, "att": 1, "def": 1, "natt": 1, "flags": {"slash"}, "range": 0}
    rows = []
    for r, block in [(None, None)] + forgeable():
        if r is None:
            w, x, strikes, kind = base, None, 0, "1-h wpn"
        else:
            if r["type"] not in ("1-h wpn", "2-h wpn", "missile") and not r.get("dancingweapon"):
                continue
            w, x = page_weapons(block)
            if not w:
                continue
            strikes, kind = int(r.get("strikes") or 0), r["type"]
        cells = []
        for F in foes:
            if kind == "missile":
                S = dict(T, weapons=[{"name": w["name"], "ranged": True, "range": w["range"], "att": T["prec"] + w["att"],
                                      "dmg": str_dmg(w, T["str"]), "flags": w["flags"]}])
                m = missile_stats(S, F, {}, {}, rng=min(w["range"], 25), n=a.n * 5, block=(6, 3))
                shots = w["natt"] if w["natt"] > 0 else 1 / -w["natt"]      # -2 = one shot every other round
                cells.append(m["kills100"] / 100 * shots)                 # kills a round
                continue
            att = T["att"] + w["att"] - (1 if r else 0)
            if strikes:                                                   # dancing weapon: strikes of its own
                k = attacks_to_kill(T["att"] + w["att"], str_dmg(w, T["str"]), w["flags"], x, F, a.n // 4)
                own = attacks_to_kill(T["att"] + 1, 19, {"slash"}, None, F, a.n // 4)
                cells.append(strikes / k + 1 / own)
            else:
                k = attacks_to_kill(att, str_dmg(w, T["str"]), w["flags"], x, F, a.n // 4)
                cells.append(max(1, w["natt"]) / k)
        rows.append((r, w, x, kind, strikes, cells))
    rows.sort(key=lambda t: -t[5][0])
    print("| Item | Type | Const | Gems | Forger | Weapon | HI killed / round | Cataphracts / round | Notes |")
    print("|---|---|---|---|---|---|---|---|---|")
    for r, w, x, kind, strikes, cells in rows:
        tags = sorted(w["flags"] & {"armornegating", "armorpiercing", "magic", "twohanded", "slash", "pierce", "blunt", "fire", "cold", "shock", "poison"})
        if x:
            tags.append(f"+{x['name']} {x['dmg']}" + (" area" if x["aoe"] else ""))
        if strikes:
            tags.append(f"{strikes} strikes")
        if kind == "missile":
            tags.append(f"range {w['range']}, {w['natt']} shots")
        if r:
            for k in ("att", "def", "str", "quick", "luck", "fear", "awe", "mr", "fireres", "coldres", "shockres", "cursed", "berserk"):
                if r.get(k) and k not in ("att", "def"):
                    tags.append(f"{k} {r[k]}")
        name = r["name"] if r else w["name"]
        print(f"| {name} | {kind} | {r['constlevel'] if r else '-'} | {r['gemcost'] if r else '-'} | {forger(r['mpath']) if r else ''} | "
              f"dmg {w['dmg']} att {w['att']:+d} x{w['natt']} | {cells[0]:.2f} | {cells[1]:.2f} | {', '.join(tags)} |")


PROT_FIELDS = ("hpbonus", "eth", "invulnerable", "luck", "twistfate", "blur", "airshield", "regeneration", "awe",
               "barkskin", "stoneskin", "ironskin", "mr", "fireres", "coldres", "shockres", "poisonres", "fireshield",
               "reinvigoration", "woundfend", "iceprot", "defender", "stunattackers", "damagereversal", "mistform")


def wearer_with(T, r):
    W = dict(T)
    db = {}
    t = r["type"] if r else ""
    if t == "armor":
        W["arm_body"] = int(r.get("protbody") or 0)
        W["def"] = T["def"] - T.get("body_def", -2) + int(r.get("def") or 0)
    elif t in ("helm", "crown"):
        W["arm_head"] = int(r.get("prothead") or 0)
        W["def"] += int(r.get("def") or 0)
    elif t == "shield":
        W["shield"], W["parry"] = int(r.get("protshield") or 0), int(r.get("parry") or 0)
        W["def"] = T["def"] - T["parry"] - T.get("shield_def", 0) + W["parry"] + int(r.get("def") or 0)
    elif t in ("misc", "boots"):
        W["def"] += int(r.get("def") or 0)
    if r:
        W["hp"] = T["hp"] + int(r.get("hpbonus") or 0)
        for k, v in SKIN.items():
            if r.get(k):
                db["nat"] = v
        if r.get("invulnerable"):
            db["invuln"] = int(r["invulnerable"])
        if r.get("eth"):
            db["ethereal"] = True
        for k in ("luck", "twistfate", "blur"):
            if r.get(k):
                db[k] = True
        if r.get("awe"):
            db["awe"] = int(r["awe"])
        if r.get("airshield"):
            db["airshield"] = True
    return W, db


KIT_DEF = {"6": (-2, -2), "42": (0, 0)}     # wearer: (body armour def, shield def) of the kit being replaced


def cmd_protection(a):
    T = load_unit(a.wearer)
    T["body_def"], T["shield_def"] = KIT_DEF.get(a.wearer, (0, 0))
    T["body"], T["head"] = T["arm_body"], T["arm_head"]
    hi, archer = load_unit("39"), load_unit("32")
    rows = []
    base = None
    for r, block in [(None, None)] + forgeable():
        if r and not (r["type"] in ("armor", "helm", "crown", "shield")
                      or (r["type"] in ("misc", "boots") and any(r.get(k) for k in PROT_FIELDS))):
            continue
        W, db = wearer_with(T, r)
        m = melee_stats(hi, W, {}, db, n=a.n)["attacks_to_kill"]
        if r and r.get("regeneration"):
            m *= 1 + min(1.5, int(str(r["regeneration"]).rstrip("%")) / 100 * m / 2)
        s = missile_stats(archer, W, {}, db, rng=20, n=a.n * 5, block=(1, 1))
        rows.append((r, W, m, s["dmg100"]))
        if r is None:
            base = (m, s["dmg100"])
    rows.sort(key=lambda t: -t[2])
    print("| Item | Slot | Const | Gems | Forger | Prot / parry / def | Attacks to kill (HI) | x own kit | Arrow dmg / 100 shots | Notes |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for r, W, m, arrows in rows:
        if r is None:
            print(f"| (own kit: {T['name']}) | - | - | - | | {W['arm_body']}/{W['arm_head']}, shield {W['shield']} p{W['parry']}, def {W['def']} | {m:.0f} | 1.0 | {arrows:.0f} | |")
            continue
        tags = [f"{k} {r[k]}" for k in PROT_FIELDS if r.get(k) and k not in ("hpbonus",)]
        if r.get("hpbonus"):
            tags.append(f"hp +{r['hpbonus']}")
        if r.get("enc"):
            tags.append(f"enc {r['enc']}")
        if r.get("cursed"):
            tags.append("cursed")
        slot = {"armor": "body", "helm": "head", "crown": "head", "shield": "shield"}.get(r["type"], r["type"])
        p = {"body": f"body {r.get('protbody', 0)}", "head": f"head {r.get('prothead', 0)}",
             "shield": f"shield {r.get('protshield', 0)} p{r.get('parry', 0)}"}.get(slot, "-")
        print(f"| {r['name']} | {slot} | {r['constlevel']} | {r['gemcost']} | {forger(r['mpath'])} | {p}, def {W['def']} | {m:.0f} | "
              f"{m / base[0]:.1f} | {arrows:.0f} | {', '.join(tags)} |")


UTIL = [
    ("Path boosters", lambda r: [f"+{p}" for p in PATHS if r.get(p)]),
    ("Penetration", lambda r: [f"pen +{r['pen']}"] if r.get("pen") else []),
    ("Casting", lambda r: [k for k in ("fastcasting", "masterritualist", "reinvigoration") if r.get(k)]
     + [f"{k} {r[k]}" for k in r if k.endswith("range") and k not in ("firerange_",) and r.get(k) and k != "range"]),
    ("Research", lambda r: [f"research +{r['researchbonus']}"] if r.get("researchbonus") else []),
    ("Gems", lambda r: [f"{k} {r[k]}" for k in r if re.fullmatch(r"g[fawesdngb]|tmp\w+gems|goldgen", k) and r.get(k)]),
    ("Movement", lambda r: [k for k in ("fly", "flyingmapmove", "mapmovebonus", "waterbreathing", "swiftness", "wintermove",
                                        "forest", "swamp", "waste", "unhindered", "stealth", "stealthb", "invisibility") if r.get(k)]),
    ("Command", lambda r: [f"{k} {r[k]}" for k in ("ldr-n", "ldr-m", "ldr-u", "inspirational", "morale", "taskmaster",
                                                 "patrolbonus", "supplybonus", "siegebonus", "armysize") if r.get(k)]),
    ("Battle spells", lambda r: [f"{k}: {r[k]}" for k in ("startbattlespell", "autocombatspell", "itemspell") if r.get(k)]),
    ("Senses", lambda r: [k for k in ("spiritsight", "darkvision", "truesight", "healer", "autodishealer", "quick") if r.get(k)]),
]


def cmd_utility(a):
    rows = forgeable()
    for cat, f in UTIL:
        hits = [(r, f(r)) for r, _ in rows]
        hits = [(r, t) for r, t in hits if t]
        if not hits:
            continue
        print(f"\n## {cat} ({len(hits)})\n")
        print("| Item | Slot | Const | Gems | Forger | What |")
        print("|---|---|---|---|---|---|")
        for r, t in sorted(hits, key=lambda x: (x[0]["constlevel"], gems(x[0]["gemcost"]))):
            extra = " (cursed)" if r.get("cursed") else ""
            print(f"| {r['name']} | {r['type']} | {r['constlevel']} | {r['gemcost']} | {forger(r['mpath'])} | {', '.join(t)}{extra} |")


def main():
    random.seed(7)
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("killing", "protection"):
        s = sub.add_parser(name)
        s.add_argument("-n", type=int, default=4000)
        if name == "protection":
            s.add_argument("--wearer", default=THUG, help="unit id: 6 Emerald Lord (thug), 42 Theurg (mage)")
    sub.add_parser("utility")
    a = p.parse_args()
    {"killing": cmd_killing, "protection": cmd_protection, "utility": cmd_utility}[a.cmd](a)


if __name__ == "__main__":
    main()
