"""Dominions 6 combat spells: list them, list what Pythium can cast, and measure buffs and debuffs.

  python3 -I spells.py list [--paths A2W2S3H4] [--kind buff|debuff|damage|battlefield|summon|other]
                            [--school Evo] [--max-level 5] [--name REGEX] [--all]
      every combat spell (researchable only unless --all), with path, school, range, area,
      fatigue/gems and effect; --paths keeps spells those path levels can cast
  python3 -I spells.py castable [--out FILE]
      the combat spells Pythium's own mages can cast (each caster, plus communion levels),
      written as markdown (default: ../castable.md)
  python3 -I spells.py melee X Y [--x BUFFS] [--y BUFFS]
      X and Y fight in melee (unit ids or names from the inspector); prints hit %, damage per
      attack and rounds to kill a fresh unit, both ways
  python3 -I spells.py missile SHOOTER TARGET [--range R] [--x BUFFS] [--y BUFFS]
      SHOOTER's first missile weapon at a packed block of TARGETs; damage and kills per 100 shots
  python3 -I spells.py summons [-n 3000]
      every summoning spell (all schools, generic and Pythium's own) ranked by the enemy heavy
      infantry its summons kill in melee before they die, in total and per gem
  python3 -I spells.py rank [--melee-unit 685] [--missile-units 684,32]
      the standard battery: each buff and debuff against the enemies met so far (markdown tables)

Any command: --data DIR uses a modded game's inspector data (SCBM: ../../dom6-scbm/data/inspector).

BUFFS is a comma list: att+N def+N str+N prec+N nat+N (natural protection, like Barkskin 7,
Stoneskin 10, Ironskin 13), armor+N (worn armour, Temper Armors 3), ap (Weapons of Sharpness),
ethereal, mistform, luck, twistfate, blur, displace, airshield (80% of missiles stopped),
quick (two actions a round), slime / slow (att and def -2, half speed), storm (precision halved,
half the missiles lost), fire8 (Flaming Arrows: +8 AP fire hit), poison5 (Serpent Fang: +5 AN
on a wounding hit), magicweapon.

Rules used (dom6-mechanics, manual pp. 58-68): DRN = 2d6 open-ended (a 6 counts 5 and rolls
again); shields: an attack that beats defence minus parry but not defence is a shield hit and adds
the shield's protection; hit locations torso 50 / arms 20 / legs 20 / head 10; piercing -15%
protection, AP halves it, AN ignores it; slashing +25% damage after protection; limb hits capped at
half max hp. Missiles: deviation range x 1.25 / precision past precision/2 - 2 (precision over 10
counts double), hit roll DRN + size points/2 vs DRN + 2 x parry. Natural and worn protection
combine as armour + natural - armour x natural / 40 (checked against the inspector's totals).
Not modelled: fatigue, harassment, repel, reach, morale, flanking, resistances.
"""
import argparse
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
INSP = os.path.join(HERE, "..", "..", "dom6-inspector")
sys.path.insert(0, os.path.join(INSP, "scripts"))
import inspector  # noqa: E402

PATHS = "FAWESDNGBH"
SCHOOLS = ["Conjuration", "Alteration", "Evocation", "Construction", "Enchantment", "Thaumaturgy",
           "Blood", "Divine"]


# ---------------------------------------------------------------- spells

def parse_paths(s):
    return {p: int(n) for p, n in re.findall(r"([FAWESDNGBH])(\d+)", s or "")}


PYTHIUM = "56"              # MA Pythium's nation id


def combat_spells():
    nations = {str(r.get("id")): set((r.get("nations") or {}).keys()) for r in inspector.records("spells")}
    out = []
    for i, name, block in inspector.pages("spells"):
        L = block.split("\n")
        if len(L) > 4 and L[3] != "Combat" and L[4] == "Combat":
            L = L[:3] + L[4:]                            # national spells have a nation line here
        if len(L) < 4 or L[3] != "Combat":
            continue
        d = {"id": i, "name": L[2], "research": L[1], "path": "", "fx": []}
        if len(L) > 4 and re.match(r"^([FAWESDNGBH]\d)+$", L[4]):
            d["path"] = L[4]
        for line in L[4:]:
            m = re.match(r"^(.*?) \[(\w+)\]: (.*)$", line)
            if m:
                d.setdefault(m.group(2), m.group(3))      # the main effect's value wins over secondary effects
            elif line.startswith("description:"):
                d["desc"] = line[12:].strip()
            elif line not in ("[wiki]", d["path"]) and line.strip():
                d["fx"].append(line)
        d["flags"] = sorted(set(re.findall(r"\[(\w+)\]", " ".join(d["fx"]))))
        d["nations"] = nations.get(i, set())
        d["kind"] = kind_of(d)
        out.append(d)
    return out


def kind_of(d):
    fx = " / ".join(d["fx"])
    first = d["fx"][0] if d["fx"] else ""
    if "Enchant Battlefield" in fx:
        return "battlefield"
    if "Summon" in first or "Call Horror" in first:
        return "summon"
    if re.match(r"(Damage|Chaining Damage|Drain Life|Poison \(HP|Unlife Damage|Lingering Cloud|Cloud:|"
                r"Shatter|Disintegrate|Stream of Life)", first):
        return "damage"
    if re.search(r"Bless/Buff|Temporary Morale Boost|^Heal|Remove Fatigue|Return Home|Blink", fx):
        return "buff"
    if re.search(r"Cause Affliction|Stun/Fascinate|Cause Fear|Paralyze|Fatigue|Weaken|Damage Armor|"
                 r"Enslave|Charm|Polymorph|Petrify|Set Effect Value|Planeshift|Add To Effect|Magic Duel|"
                 r"Time Stop", fx):
        return "debuff"
    return "other"


def school_level(d):
    r = d["research"]
    if r.startswith("Divine"):
        return "Divine", 0
    m = re.match(r"(\w+) (\d+)", r)
    return (m.group(1), int(m.group(2))) if m else (r, 99)


def can_cast(d, paths):
    need = parse_paths(d["path"])
    return bool(need) and all(paths.get(p, 0) >= n for p, n in need.items())


def effect_text(d, width=110):
    fx = " / ".join(d["fx"])
    fx = re.sub(r"\((?:[^()]*\[\w+\],? ?)+\)", "", fx)
    fx = re.sub(r"\s*/\s*(/\s*)+", " / ", fx).strip(" /")
    fx = fx.replace("Bless/Buff: ", "").replace("details: ", "")
    return fx[:width]


def flag_text(d):
    keep = {"armornegating": "AN", "armorpiercing": "AP", "mrnegates": "MR", "mrnegateseasily": "MR-easy",
            "hardmrneg": "MR-hard", "ignoreshield": "noShield", "enemyimmune": "friends", "friendlyimmune":
            "enemies", "uwonly": "UNDERWATER", "sacredonly": "sacreds", "mind": "mind", "undeadimmune":
            "noUndead", "sizeresist": "size-resists"}
    return ",".join(v for k, v in keep.items() if k in d["flags"])


def row(d):
    sch, lvl = school_level(d)
    gems = d.get("gemcost", "")
    return (f"| {d['name']} | {sch[:5]} {lvl if lvl < 99 else ''} | {d['path']} | {d.get('rng_bat', '-')} | "
            f"{d.get('aoe_s', '-')} | {d.get('fatiguecost', '').rstrip('-')}{' ' + gems if gems else ''} | "
            f"{d['kind']} | {flag_text(d)} | {effect_text(d)} |")


HEAD = "| Spell | School | Path | Range | Area | Fatigue / gems | Kind | Flags | Effect |\n|---|---|---|---|---|---|---|---|---|"


def cmd_list(a):
    paths = parse_paths(a.paths) if a.paths else None
    print(HEAD)
    for d in sorted(combat_spells(), key=lambda d: (school_level(d), d["name"])):
        sch, lvl = school_level(d)
        if not a.all and (d["research"] == "unresearchable" or d["nations"]):
            continue
        if a.kind and d["kind"] != a.kind:
            continue
        if a.school and not sch.lower().startswith(a.school.lower()):
            continue
        if a.max_level is not None and lvl > a.max_level:
            continue
        if a.name and not re.search(a.name, d["name"], re.I):
            continue
        if paths is not None and not (can_cast(d, paths) or (sch == "Divine" and paths.get("H", 0) >= parse_paths(d["path"]).get("H", 9))):
            continue
        print(row(d))


# Pythium (MA) casters: inspector paths; communion adds +n to the master's paths for 2^n slaves.
CASTERS = [
    ("Theurg Acolyte", "S1H1"),
    ("Theurg", "A1W1S2H2"),
    ("Arch Theurg (+1 random F/A/W/S not counted)", "A2W1S3H3"),
    ("Bartholomeus (hero)", "A2W2S3H4"),
    ("Theurg + 4 slaves (master +2)", "A3W3S4H2"),
    ("Bartholomeus + 5 Communicants (+2)", "A4W4S5H4"),
    ("Bartholomeus + 8 slaves (+3)", "A5W5S6H4"),
    ("Arch Theurg + 8 slaves (+3)", "A5W4S6H3"),
    ("God: Titan of Growth (dormant until ~T10-13)", "E5N5H3"),
]
GOD_PATH = "Earth"          # the god's 4+ path that picks the Smite/Banish versions (Theocratus casts Word of Stone)


def cmd_castable(a):
    spells = combat_spells()
    researched = {"Conjuration": 0, "Alteration": 1, "Evocation": 1, "Construction": 0, "Enchantment": 1,
                  "Thaumaturgy": 1, "Blood": 0}
    lines = ["# Combat spells Pythium can cast", "",
             "Made by `spells.py castable` from the inspector data (2026-10-28). One row per spell that at least",
             "one of Pythium's own casters can cast; **First caster** is the cheapest one that reaches it.",
             "Communion: the master gets +1 in every path for 2 slaves, +2 for 4, +3 for 8 (Communicants and",
             "Theurgs as slaves). Holy spells need only the priest level; Smite and Banish come in the",
             f"god's {GOD_PATH} version. UNDERWATER spells are listed but useless on land.",
             f"Research at turn 6: {', '.join(f'{k} {v}' for k, v in researched.items())}"
             " (✓ = castable now if a caster has the paths).", "",
             "Casters: " + "; ".join(f"{n} {p}" for n, p in CASTERS), ""]
    rows = []
    for d in spells:
        if d["research"] == "unresearchable" or (d["nations"] and PYTHIUM not in d["nations"]):
            continue
        sch, lvl = school_level(d)
        if sch == "Blood":
            continue
        first = None
        for name, p in CASTERS:
            pp = parse_paths(p)
            if sch == "Divine":
                restr = " ".join(d["fx"])
                m = re.search(r"God Path Restriction : (\w+)", restr)
                if m and m.group(1) != GOD_PATH:
                    break
                if pp.get("H", 0) >= parse_paths(d["path"]).get("H", 9):
                    first = name
                    break
            elif can_cast(d, pp):
                first = name
                break
        if first:
            now = "✓" if sch == "Divine" or researched.get(sch, 0) >= lvl else ""
            rows.append((SCHOOLS.index(sch) if sch in SCHOOLS else 9, lvl, d, first, now))
    for k in ["buff", "debuff", "damage", "battlefield", "summon", "other"]:
        sel = sorted([r for r in rows if r[2]["kind"] == k], key=lambda r: (r[0], r[1], r[2]["name"]))
        if not sel:
            continue
        lines += ["", f"## {k.capitalize()} ({len(sel)})", "",
                  "| Now | Spell | School | Path | First caster | Range | Area | Fatigue / gems | Flags | Effect |",
                  "|---|---|---|---|---|---|---|---|---|---|"]
        for _, lvl, d, first, now in sel:
            sch, _ = school_level(d)
            gems = d.get("gemcost", "")
            lines.append(f"| {now} | {d['name']} | {sch[:5]} {lvl if sch != 'Divine' else ''} | {d['path']} | {first} | "
                         f"{d.get('rng_bat', '-')} | {d.get('aoe_s', '-')} | {d.get('fatiguecost', '').rstrip('-')}"
                         f"{' ' + gems if gems else ''} | {flag_text(d)} | {effect_text(d, 90)} |")
    out = a.out or os.path.join(HERE, "..", "castable.md")
    open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"{len(rows)} spells -> {os.path.normpath(out)}")


# ---------------------------------------------------------------- units and combat

WEAPONS = None


def weapon_flags(wid):
    global WEAPONS
    if WEAPONS is None:
        WEAPONS = {}
        for i, name, block in inspector.pages("weapons"):
            WEAPONS[i] = set(re.findall(r"\[(\w+)\]", block))
            m = re.search(r"ammunition \[ammo\]: (\d+)", block)
            WEAPONS[i].add(f"ammo{m.group(1)}" if m else "ammo0")
            m = re.search(r"nbr of attacks \[nratt\]: (-?\d+)", block)
            WEAPONS[i].add(f"natt{m.group(1)}" if m else "natt1")
    return WEAPONS.get(wid, set())


ARMOR_SLOTS = None


def armor_slot(aid):
    """'head', 'body', 'shield' or other (barding...), from line 2 of the armour's inspector page."""
    global ARMOR_SLOTS
    if ARMOR_SLOTS is None:
        ARMOR_SLOTS = {}
        for i, name, block in inspector.pages("armor"):
            L = block.split("\n")
            ARMOR_SLOTS[i] = "shield" if "[protshield]" in block else "head" if "[prothead]" in block else \
                "body" if "[protbody]" in block else (L[1] if len(L) > 1 else "")
    return ARMOR_SLOTS.get(aid, "")


def combine(arm, nat):
    return arm + nat - arm * nat / 40 if arm and nat else arm + nat


def load_unit(q):
    hits = inspector.find("units", q)
    if not hits:
        sys.exit(f"no unit {q!r}")
    i, name, block = hits[0]
    g = lambda k, d=0: int(re.search(rf"^{k}: (-?\d+)", block, re.M).group(1)) if re.search(rf"^{k}: (-?\d+)", block, re.M) else d
    m = re.search(r"^protection: \d+ +\(basic (\d+), head (\d+), body (\d+)\)", block, re.M)
    nat, head, body = map(int, m.groups()) if m else (g("protection"),) * 3    # no breakdown: all natural
    u = {"id": i, "name": name.split(" - ")[-1].strip("“” "), "hp": g("hit points"), "size": g("size", 3),
         "nat": nat, "head": head, "body": body, "mr": g("magic res", 10), "str": g("strength", 10),
         "def": g("defence skill"), "att": g("attack skill"), "prec": g("precision", 10),
         "weapons": [], "parry": 0, "shield": 0, "arm_body": 0, "arm_head": 0, "mor": g("morale", 10), "enc": g("encumbrance", 3),
         "ab": {k: int(v) for k, v in re.findall(r"^[a-z][^\n\[]*\[(\w+)\]: \+?(-?\d+)", block, re.M)},
         "tags": set(re.findall(r"\[(\w+)\]", " ".join(l for l in block.split("\n") if l.startswith("(")))),
         "mpath": (re.search(r"^magic paths \[mpath\]: (.*)$", block, re.M) or [None, ""])[1]}
    for line in block.split("\n"):
        w = re.match(r"^#(\d+) ([^|]*?) \| (r?-?\d+) \| (-?\d+) \| (-?\d+)$", line)   # [^|]: a shield row has 4 fields
        if w:
            fl = weapon_flags(w.group(1))
            u["weapons"].append({"name": w.group(2), "ranged": w.group(3).startswith("r"),
                                 "range": int(w.group(3).lstrip("r")), "att": int(w.group(4)),
                                 "dmg": int(w.group(5)), "flags": fl})
            continue
        r = re.match(r"^#(\d+) ([^|]*?) \| (\d+) \| (-?\d+) \| (\d*) \| (\d*)$", line)
        if r:
            prot, par, slot = int(r.group(3)), r.group(5), armor_slot(r.group(1))
            if par or slot == "shield":
                u["parry"], u["shield"] = int(par or 0), prot
            elif slot == "head":
                u["arm_head"] = prot
            elif slot == "body":
                u["arm_body"] = prot
    return u


def drn():
    t = 0
    for _ in range(2):
        d = random.randint(1, 6)
        while d == 6:
            t += 5
            d = random.randint(1, 6)
        t += d
    return t


def parse_buffs(s):
    b = {}
    for tok in filter(None, (s or "").split(",")):
        m = re.match(r"(\w+)([+-]\d+)$", tok)
        if m:
            b[m.group(1)] = b.get(m.group(1), 0) + int(m.group(2))
        else:
            b[tok] = True
    if b.get("slime") or b.get("slow"):
        b["att"] = b.get("att", 0) - 2
        b["def"] = b.get("def", 0) - 2
    return b


def prot_of(u, b, loc):
    nat = u["nat"] + b.get("nat", 0) if not b.get("nat") else max(u["nat"], min(u["nat"] + b["nat"], natcap(b["nat"])))
    if loc == "head":
        arm = u["arm_head"] + (b.get("armor", 0) if u["arm_head"] else 0)
        return combine(arm, nat) if (arm or nat) else u["head"]
    arm = u["arm_body"] + (b.get("armor", 0) if u["arm_body"] else 0)
    return combine(arm, nat) if (arm or nat) else u["body"]


def natcap(n):
    return {7: 10, 10: 15, 13: 20}.get(n, 99)        # Barkskin max 10, Stoneskin 15, Ironskin 20


def strike(dmg, prot, flags, ab, hp_left, hp_max, loc, db, shield_hit, sh_prot):
    """Damage from one landed attack after protection and defensive abilities."""
    if shield_hit:
        prot += sh_prot
    if "armornegating" in flags:
        prot = 0
    else:
        if "pierce" in flags:
            prot *= 0.85
        if "armorpiercing" in flags or ab.get("ap"):
            prot *= 0.5
    d = max(0, dmg + drn() - (prot + drn()))
    res = db.get("res", ())
    if any(t in flags and t + "res" in res for t in ("slash", "pierce", "blunt")):
        d //= 2                                          # slash/pierce/blunt resistance halves the damage
    if "slash" in flags:
        d = int(d * 1.25)
    if "blunt" in flags and loc == "head":
        d = int(d * 1.25)
    if loc in ("arm", "leg"):
        d = min(d, hp_max // 2)
    magic = "magic" in flags or ab.get("magicweapon")
    if d and db.get("mistform"):
        if d >= 25 or magic:
            db["mistform"] = False                       # a hard or magic hit ends it, after the reduction
        d = max(1, d - 25)
    if d >= hp_left and db.get("luck") and random.random() < 0.75:
        d = 0
    return d


def location():
    r = random.random()
    return "head" if r < .1 else "body" if r < .6 else "arm" if r < .8 else "leg"


def melee_stats(A, D, ab, db0, n=20000):
    db = dict(db0)
    w = next((w for w in A["weapons"] if not w["ranged"]), None)
    if not w:
        return None
    att = w["att"] + ab.get("att", 0) - (2 if db.get("blur") else 5 if db.get("displace") else 0)
    dfn = D["def"] + db.get("def", 0)
    dmg = w["dmg"] + ab.get("str", 0) * (1.25 if "twohanded" in w["flags"] else 1)
    hits = tot = 0
    rounds = []
    for _ in range(n // 10):
        hp, k, fate, db = D["hp"], 0, bool(db.get("twistfate")), dict(db0)
        while hp > 0 and k < 400:
            k += 1
            if db.get("awe") and A.get("mor", 10) + drn() <= 10 + db["awe"] + drn():
                continue                                   # awe: failed the morale check, no attack
            ra, rd = att + drn(), dfn + drn()
            if ra <= rd - D["parry"]:
                continue
            shield_hit = ra <= rd
            if db.get("ethereal") and "magic" not in w["flags"] and not ab.get("magicweapon") and random.random() < .75:
                continue
            if fate:
                fate = False
                continue
            loc = location()
            pr = prot_of(D, db, loc)
            if db.get("invuln") and "magic" not in w["flags"] and not ab.get("magicweapon"):
                pr = max(pr, db["invuln"])                 # invulnerability: protection against non-magic weapons
            d = strike(dmg, pr, w["flags"], ab, hp, D["hp"], loc, db, shield_hit, D["shield"])
            hits += 1
            tot += d
            hp -= d
        rounds.append(k)
    per_round = (2 if ab.get("quick") else 1) * (0.5 if ab.get("slime") or ab.get("slow") else 1)
    att_n = sum(rounds)
    return {"weapon": w["name"], "hit": hits / att_n, "dmg": tot / att_n,
            "attacks_to_kill": att_n / len(rounds), "rounds_to_kill": att_n / len(rounds) / per_round}


def missile_stats(S, T, ab, db, rng=None, n=40000, block=(8, 4)):
    w = next((w for w in S["weapons"] if w["ranged"]), None)
    if not w:
        return None
    R = rng or w["range"]
    prec = w["att"] + ab.get("prec", 0)
    if ab.get("storm"):
        prec /= 2
    peff = prec if prec <= 10 else 10 + 2 * (prec - 10)
    dev = R * 1.25 / peff if R > prec / 2 - 2 else 0
    if ab.get("windguide") and dev:
        dev /= 2
    dmg = w["dmg"] + ab.get("str", 0) * (0.5 if "halfstr" in w["flags"] else 1)
    tot = kills = 0
    for _ in range(n):
        if ab.get("storm") and random.random() < .5:
            continue
        tx, ty = random.randrange(block[0]), random.randrange(block[1])
        x = round(tx + dev * (random.random() + random.random() - 1))
        y = round(ty + dev * (random.random() + random.random() - 1))
        if not (0 <= x < block[0] and 0 <= y < block[1]):
            continue
        if db.get("airshield") and random.random() < .8:
            continue
        if not drn() + 3 * T["size"] / 2 + (2 if ab.get("magicweapon") else 0) > drn() + 2 * T["parry"]:
            continue
        if db.get("ethereal") and not ab.get("magicweapon") and random.random() < .75:
            continue
        loc = location()
        dbs = dict(db)
        d = strike(dmg, prot_of(T, db, loc), w["flags"], ab, T["hp"], T["hp"], loc, dbs, False, 0)
        if ab.get("fire8"):
            d += strike(8, prot_of(T, db, loc), {"armorpiercing"}, {}, T["hp"], T["hp"], loc, db, False, 0)
        if ab.get("poison5") and d > 0:
            d += 5
        tot += d
        kills += d >= T["hp"]
    return {"weapon": w["name"], "range": R, "prec": prec, "dev": round(dev, 2), "dmg100": 100 * tot / n,
            "kills100": 100 * kills / n, "hp_equiv100": 100 * tot / n / T["hp"]}


def cmd_melee(a):
    X, Y = load_unit(a.x_unit), load_unit(a.y_unit)
    bx, by = parse_buffs(a.x), parse_buffs(a.y)
    for A, D, ab, db in ((X, Y, bx, by), (Y, X, by, bx)):
        s = melee_stats(A, D, ab, db)
        if s:
            print(f"{A['name']} ({s['weapon']}) -> {D['name']}: hit {s['hit']:.0%}, {s['dmg']:.2f} dmg/attack, "
                  f"{s['attacks_to_kill']:.1f} attacks / {s['rounds_to_kill']:.1f} rounds to kill one")


def cmd_missile(a):
    S, T = load_unit(a.x_unit), load_unit(a.y_unit)
    s = missile_stats(S, T, parse_buffs(a.x), parse_buffs(a.y), a.range)
    print(f"{S['name']} ({s['weapon']}, range {s['range']}, prec {s['prec']}, deviation {s['dev']} sq) -> "
          f"packed {T['name']}: {s['dmg100']:.0f} dmg and {s['kills100']:.1f} one-shot kills per 100 shots "
          f"(= {s['hp_equiv100']:.1f} men's hp)")


ENEMIES = [("18", "Militia"), ("38", "Heavy Inf (spear)"), ("39", "Heavy Inf (sword)"), ("139", "Barbarian"),
           ("727", "Jaguar Warrior"), ("1592", "Bear Tribe Warrior"), ("1187", "Cataphract"), ("32", "Archer")]
OFFENCE = [("none", "", ""), ("Slime/Slow on them", "", "slime"), ("Quagmire (both -1/-1)", "att-1,def-1", "att-1,def-1"),
           ("Battle Fury (att +2)", "att+2", ""), ("Strength of Giants (str +4)", "str+4", ""),
           ("Weapons of Sharpness (AP)", "ap", ""), ("Eclipse/darkness (both -3)", "att-3,def-3", "att-3,def-3"),
           ("Quickness (2 actions)", "quick", "")]
DEFENCE = [("none", "", ""), ("Slime/Slow on them", "", "slime"), ("Barkskin (nat 7)", "nat+7", ""),
           ("Stoneskin (nat 10)", "nat+10", ""), ("Ironskin (nat 13)", "nat+13", ""), ("Temper Armors (+3)", "armor+3", ""),
           ("Blur (their att -2)", "blur", ""), ("Displace (their att -5)", "displace", ""),
           ("Body Ethereal", "ethereal", ""), ("Mistform", "mistform", ""), ("Luck", "luck", ""),
           ("Twist Fate (first hit)", "twistfate", "")]


def cmd_rank(a):
    me = load_unit(a.melee_unit)
    foes = [(load_unit(i), n) for i, n in ENEMIES]
    print(f"### Offence: rounds for one {me['name']} to kill one enemy (lower is better)\n")
    print("| Buff | " + " | ".join(n for _, n in foes) + " | avg change |")
    print("|---|" + "---|" * (len(foes) + 1))
    base = None
    for label, bx, by in OFFENCE:
        vals = [melee_stats(me, f, parse_buffs(bx), parse_buffs(by))["rounds_to_kill"] for f, _ in foes]
        base = base or vals
        ch = sum(v / b for v, b in zip(vals, base)) / len(vals) - 1
        print(f"| {label} | " + " | ".join(f"{v:.1f}" for v in vals) + f" | {ch:+.0%} |")
    print(f"\n### Defence: rounds for one enemy to kill one {me['name']} (higher is better)\n")
    print("| Buff | " + " | ".join(n for _, n in foes) + " | avg change |")
    print("|---|" + "---|" * (len(foes) + 1))
    base = None
    for label, bme, bfoe in DEFENCE:
        vals = []
        for f, _ in foes:
            s = melee_stats(f, me, parse_buffs(bfoe), parse_buffs(bme))
            vals.append(min(s["rounds_to_kill"], 400) if s else float("nan"))
        base = base or vals
        ch = sum(v / b for v, b in zip(vals, base)) / len(vals) - 1
        print(f"| {label} | " + " | ".join(f"{v:.0f}" for v in vals) + f" | {ch:+.0%} |")
    for su in a.missile_units.split(","):
        S = load_unit(su)
        w = next(w for w in S["weapons"] if w["ranged"])
        R = min(w["range"], 15)
        print(f"\n### Missiles: {S['name']} ({w['name']}, range {R}) into a packed block, men's hp of damage per 100 shots\n")
        print("| Buff | " + " | ".join(n for _, n in foes) + " | avg change |")
        print("|---|" + "---|" * (len(foes) + 1))
        base = None
        for label, bx in [("none", ""), ("Trueshot (prec +4)", "prec+4"), ("Wind Guide (prec +2, half deviation)", "prec+2,windguide"),
                          ("Strength of Giants (str +4)", "str+4"), ("Flaming Arrows (+8 AP fire)", "fire8"),
                          ("Serpent Fang (+5 poison)", "poison5"), ("Storm (both sides)", "storm")]:
            vals = [missile_stats(S, f, parse_buffs(bx), {}, R)["hp_equiv100"] for f, _ in foes]
            base = base or vals
            ch = sum(v / b for v, b in zip(vals, base) if b) / len(vals) - 1
            print(f"| {label} | " + " | ".join(f"{v:.1f}" for v in vals) + f" | {ch:+.0%} |")
    T = me
    print(f"\n### Missile defence: enemy shots into packed {T['name']}s, men's hp of damage per 100 shots (lower is better)\n")
    shooters = [(load_unit(i), n) for i, n in [("32", "Archer (short bow)"), ("1592", "Bear Tribe (javelin)"),
                                                  ("684", "Velite (javelin)")]]
    print("| Buff on us | " + " | ".join(n for _, n in shooters) + " |")
    print("|---|" + "---|" * len(shooters))
    for label, bt in [("none", ""), ("Air Shield / Protective Winds / Arrow Ward", "airshield"), ("Body Ethereal", "ethereal"),
                      ("Mistform", "mistform"), ("Barkskin (nat 7)", "nat+7"), ("Temper Armors (+3)", "armor+3")]:
        vals = [missile_stats(s, T, {}, parse_buffs(bt), min(next(w for w in s["weapons"] if w["ranged"])["range"], 15))["hp_equiv100"]
                for s, _ in shooters]
        print(f"| {label} | " + " | ".join(f"{v:.1f}" for v in vals) + " |")


# ---------------------------------------------------------------- damage spells (evocations)

def spell_blocks(q):
    """The effect blocks of a spell page: the main effect, then each secondary effect."""
    hits = [h for h in inspector.find("spells", q)]
    i, name, block = hits[0]
    L = block.split("\n")
    if len(L) > 4 and L[3] != "Combat" and L[4] == "Combat":
        L = L[:3] + L[4:]
    blocks = [{"name": L[2], "kv": {}, "fx": []}]
    for j, line in enumerate(L[5:], 5):
        if line.startswith("description:") or line == "[wiki]":
            break
        if j + 1 < len(L) and L[j + 1].startswith("spell id [id]") and j > 6:
            blocks.append({"name": line, "kv": {}, "fx": []})
            continue
        m = re.match(r"^(.*?) \[(\w+)\]: (.*)$", line)
        if m:
            blocks[-1]["kv"][m.group(2)] = m.group(3)
        else:
            blocks[-1]["fx"].append(line)
    for b in blocks:
        b["flags"] = set(re.findall(r"\[(\w+)\]", " ".join(b["fx"])))
    return {"name": L[2], "research": L[1], "path": L[4], "blocks": blocks}


def scaled(v, lvl):
    """1000+N = N + level, 2000+N = N + 2 x level, 3000+N = N + 3 x level (the inspector's +, ++, +++)."""
    v = int(v)
    if 1000 <= v < 5000:
        return v % 1000 + (v // 1000) * lvl
    return v


def area_of(aoe, lvl):
    if not aoe or aoe in ("-", "One person", "Caster"):
        return 0
    m = re.match(r"(\d+)(?:\+ \[(\d+)/lvl\])?", aoe)
    if "%" in aoe:
        return 999
    return int(m.group(1)) + (int(m.group(2)) * lvl if m.group(2) else 0) if m else 0


def range_of(r, lvl):
    m = re.match(r"(\d+)(?:\+ \[(\d+)/lvl\])?", r or "")
    return int(m.group(1)) + (int(m.group(2)) * lvl if m.group(2) else 0) if m else 0


OFFSETS = sorted(((dx, dy) for dx in range(-12, 13) for dy in range(-12, 13)), key=lambda o: o[0] ** 2 + o[1] ** 2)

MAGE = {"name": "Mage line", "hp": 10, "nat": 0, "head": 5, "body": 1, "mr": 15, "parry": 0, "shield": 0,
        "arm_body": 1, "arm_head": 5, "size": 3}


def cast_once(sp, lvl, extra, T, per_sq, block, R, mage_prec=10):
    """One cast at a block of T (per_sq men per square). Returns (hp damage, kills, fatigue dealt, men affected)."""
    main = sp["blocks"][0]
    kv = main["kv"]
    eff = kv.get("effect_number")
    nb = kv.get("nreff", "1")
    nb = scaled(nb, lvl) if nb.isdigit() else 1
    prec = int(kv.get("precision") or 0)
    W, D = block
    dmg_t = kills = fat = aff = 0
    occupied = lambda x, y: 0 <= x < W and 0 <= y < D
    for _ in range(max(1, nb)):
        tx, ty = random.randrange(W), random.randrange(D)
        if prec >= 100:
            x, y = tx, ty
        else:
            P = mage_prec + prec
            peff = P if P <= 10 else 10 + 2 * (P - 10)
            dev = R * 1.25 / max(1, peff) if R > P / 2 - 2 else 0
            x = round(tx + dev * (random.random() + random.random() - 1))
            y = round(ty + dev * (random.random() + random.random() - 1))
        for bi, b in enumerate(sp["blocks"]):
            bk = b["kv"]
            e = bk.get("effect_number")
            if e in ("147", "146", "81", "1", "23", "13", "27", "601"):
                continue                                   # clouds, enchantments, summons, buffs, heals: not counted
            if b["flags"] & {"magiconly", "demonundead"} or b["name"] == "Cave Collapse":
                continue                                   # only magic beings / undead and demons / caves; targets are living men
            n_area = area_of(bk.get("aoe_s"), lvl)
            if bi == 0 and nb > 1 and n_area <= 1:
                n_area = 0                                  # multi-bolt spells: each bolt hits one man
            squares = [(x, y)] if n_area <= 1 else [(x + dx, y + dy) for dx, dy in OFFSETS[:n_area]]
            men = []
            for sx, sy in squares:
                if occupied(sx, sy):
                    men += [1] * (per_sq if n_area >= 1 else 1)
            if n_area == 0 and men:
                men = men[:1]
            chain = e == "134"
            if chain and men:
                bounces = int(re.search(r"bounces : (\d+)", " ".join(b["fx"])).group(1)) if "bounces" in " ".join(b["fx"]) else 0
                men = [1] * min(1 + bounces, W * D * per_sq)
            fl = b["flags"]
            for _m in men:
                if "ignoreshield" not in fl and not (drn() + per_sq * T["size"] / 2 > drn() + 2 * T["parry"]):
                    continue
                half = False
                if fl & {"mrnegates", "mrnegateseasily", "hardmrneg", "mrcheckhalfdmg"}:
                    pen = 11 + drn() + extra // 2 + (4 if "hardmrneg" in fl else 0) - (4 if "mrnegateseasily" in fl else 0)
                    if pen < T["mr"] + drn():
                        if "mrcheckhalfdmg" in fl:
                            half = True
                        else:
                            continue
                aff += 1
                if e == "3":
                    fat += scaled(bk.get("damage", 0), lvl) // (2 if half else 1)
                    continue
                if e not in ("2", "134", "109", "74"):
                    continue
                dv = scaled(bk.get("damage", 0), lvl)
                if e == "109":
                    dv = int(re.search(r"Capped Damage: (\d+)", " ".join(b["fx"])).group(1)) if "Capped" in " ".join(b["fx"]) else dv
                loc = location()
                prot = 0 if "armornegating" in fl else prot_of(T, {}, loc) * (0.5 if "armorpiercing" in fl else 1) * (0.85 if "pierce" in fl else 1)
                d = max(0, dv + drn() - (prot + drn()))
                if half:
                    d //= 2
                if "slash" in fl:
                    d = int(d * 1.25)
                if loc in ("arm", "leg"):
                    d = min(d, T["hp"] // 2)
                dmg_t += min(d, T["hp"])
                kills += d >= T["hp"]
    return dmg_t, kills, fat, aff


DMG_TARGETS = [("18", "Militia", 3), ("39", "Heavy Inf (sword)", 3), ("139", "Barbarian", 3), ("1187", "Cataphract", 2),
               ("32", "Archer", 3), ("mage", "Mages (1/square, MR 15)", 1)]


def cmd_damage(a):
    names = [n.strip() for n in a.spells.split(",")] if a.spells else None
    rows = []
    for d in combat_spells():
        if names is None and (not d["research"].startswith(a.school) or d["nations"] or d["research"] == "unresearchable"):
            continue
        if names is not None and d["name"] not in names:
            continue
        sp = spell_blocks(d["id"])
        need = parse_paths(sp["path"])
        if not need:
            continue
        base = max(need.values())
        for extra in (0, 2):
            lvl = base + extra
            r = range_of(sp["blocks"][0]["kv"].get("rng_bat"), lvl)
            R = min(r, a.range) if r else a.range
            fatc = int(re.sub(r"\D", "", sp["blocks"][0]["kv"].get("fatiguecost", "0")) or 0)
            cells = []
            for tid, tname, per_sq in DMG_TARGETS:
                T = MAGE if tid == "mage" else load_unit(tid)
                block = (6, 1) if tid == "mage" else (6, 3)
                tot = [0, 0, 0, 0]
                for _ in range(a.n):
                    for k, v in enumerate(cast_once(sp, lvl, extra, T, per_sq, block, R)):
                        tot[k] += v
                tot = [v / a.n for v in tot]
                cells.append(tot)
            rows.append((sp, lvl, extra, r, R, fatc, cells))
    print("| Spell | Path @lvl | Range (used) | Fatigue | " + " | ".join(t[1] for t in DMG_TARGETS) + " |")
    print("|---|---|---|---|" + "---|" * len(DMG_TARGETS))
    for sp, lvl, extra, r, R, fatc, cells in rows:
        fc = round(fatc / (1 + extra)) if fatc < 100 else fatc
        txt = []
        for dm, k, fat, aff in cells:
            if fat:
                txt.append(f"{fat:.0f} fat ({aff:.1f} men)")
            elif dm or k:
                txt.append(f"{k:.2f} k / {dm / 10:.1f} hp")
            elif aff:
                txt.append(f"{aff:.1f} men hit")
            else:
                txt.append("–")
        print(f"| {sp['name']} | {sp['path']} @{'+' + str(extra) if extra else 'req'} | {r} ({R}) | {fc} | " + " | ".join(txt) + " |")


# ---------------------------------------------------------------- summons

SUMMON_FX = re.compile(r"Summon Units|Summon Commander|Edge of Battlefield Summon|Remote Summon|Ritual Summon Unique")
TRADE_FOES = [("39", "HI sword"), ("18", "Militia")]
RITUAL_CASTERS = [("Theurg", "A1W1S2H2"), ("Arch Theurg / Bartholomeus", "A2W2S3H4"),
                  ("Arch Theurg + booster", "A3W2S4H3"), ("God (awake)", "E5N5H3")]
SUMMON_TAGS = ["flying", "ethereal", "undead", "demon", "inanimate", "magicbeing", "holy", "stealthy", "amphibian",
               "aquatic", "trample", "berserk", "undisciplined", "mindless", "animal", "slashres", "pierceres", "bluntres"]
SUMMON_ABS = ["awe", "fear", "invulnerable", "regeneration", "poisoncloud", "fireshield", "heat", "cold", "poisonbarbs",
              "berserk", "stealth", "chillaura", "heataura", "deathcurse"]


def count_at(code, shown, lvl):
    """nreff: 1000s = base + per-level, 500s = base + level/2; the inspector shows it at level 0."""
    c = int(code) if code and code.lstrip("-").isdigit() else 0
    if c >= 1000:
        return c % 1000 + c // 1000 * lvl
    if 500 < c < 1000:
        return c - 500 + lvl // 2
    return shown


def summon_spells():
    out = []
    recs = {str(r.get("id")): r for r in inspector.records("spells")}
    for i, name, block in inspector.pages("spells"):
        L = block.split("\n")
        if len(L) > 4 and L[3] not in ("Combat", "Ritual") and L[4] in ("Combat", "Ritual"):
            L = L[:3] + L[4:]
        if len(L) < 5 or L[1] == "unresearchable":
            continue
        nats = (recs.get(i) or {}).get("nations") or {}
        if nats and PYTHIUM not in nats:
            continue
        kv, fx = {}, []
        for l in L[5:]:
            if l.startswith("description:") or l == "[wiki]":
                break
            m = re.match(r"^(.*?) \[(\w+)\]: (.*)$", l)
            if m:
                kv.setdefault(m.group(2), m.group(3))
            else:
                fx.append(l)
        fxs = " / ".join(x for x in fx if not re.match(r"(Underwater|Cold) summon", x))   # alternates, not extras
        if not SUMMON_FX.search(fxs):
            continue
        bare = re.sub(r"\[[^\]]*\]", "", fxs)                           # drop "[1/2 lvl]" scaling notes
        units = [(u, int(n) if n else 1) for u, n in re.findall(r"#(\d+) [^#/,]*?(?: x (\d+)\+*)?(?= /|,|$| #)", bare)]
        if not units:
            continue
        g = re.match(r"(\d+)([FAWESDNGBH]?)", kv.get("gemcost", "") or "")
        out.append({"id": i, "name": L[2], "research": L[1], "path": L[4], "type": L[3],
                    "nreff": kv.get("nreff"), "gems": int(g.group(1)) if g else 0, "gempath": g.group(2) if g else "",
                    "units": units, "one_of": "Ritual Summon Unique" in fxs or "Tartarian" in name,
                    "remote": "Remote Summon" in fxs, "temporary": L[3] == "Combat" or "Temporary" in fxs,
                    "national": bool(nats), "fx": fxs})
    return out


SURROUND = {1: 1.5, 2: 1.5, 3: 2, 4: 2.5, 5: 3, 6: 3.5}


def trade(S, foe, n=3000):
    """Enemy men S kills before it dies in melee: kills a round x rounds alive while SURROUND foes attack it."""
    db = {"invuln": S["ab"].get("invulnerable", 0), "awe": S["ab"].get("awe", 0),
          "ethereal": "ethereal" in S["tags"], "res": {t for t in S["tags"] if t.endswith("res")}}
    rate = 0
    for w in S["weapons"]:
        if w["ranged"]:
            continue
        one = dict(S, weapons=[w])
        r = melee_stats(one, foe, {}, {}, n=n)
        natt = next((int(f[4:]) for f in w["flags"] if f.startswith("natt")), 1)
        rate += (natt if natt > 0 else 1 / -natt if natt < 0 else 1) / r["attacks_to_kill"]
    if "trample" in S["tags"] and S["size"] > foe["size"]:
        rate = max(rate, trample_rate(S, foe, n))
    life = melee_stats(foe, S, {}, db, n=n)
    if not life or not rate:
        return 0, life and life["attacks_to_kill"]
    hold = life["attacks_to_kill"] / SURROUND.get(S["size"], 4)
    regen = S["ab"].get("regeneration", 0)
    if regen:
        hold *= 1 + min(1.5, regen / 100 * hold)        # regeneration in % of max hp a round, roughly
    hold = min(hold, 100 / S["enc"] if S["enc"] > 0 else 50, 50)   # fatigue: enc a round, spent at 100; battles end by 50
    return rate * hold, hold


def d3d6():
    return sum(random.randint(1, 6) for _ in range(3))


def trample_rate(S, foe, n):
    """Men killed a round by trampling one square (manual: Defence vs 3d6, else 7 + size AP damage, min 1)."""
    tries = 0
    for _ in range(n // 10):
        hp = foe["hp"]
        while hp > 0 and tries < 10 ** 6:
            tries += 1
            if foe["def"] >= d3d6():
                hp -= 1
                continue
            d = max(1, 7 + S["size"] + drn() - (prot_of(foe, {}, location()) / 2 + drn()))
            hp -= d // 2 if "ethereal" in S["tags"] else d
    per_square = max(1, 10 // max(foe["size"], 1))
    return per_square / (tries / (n // 10))


def cmd_summons(a):
    rows = []
    cache = {}
    for sp in summon_spells():
        need = parse_paths(sp["path"])
        base = max(need.values()) if need else 1
        cells, units_txt, tags = [], [], set()
        total = [0.0] * len(TRADE_FOES)
        for k, (uid, shown) in enumerate(sp["units"]):
            if uid not in cache:
                try:
                    U = load_unit(uid)
                except SystemExit:
                    cache[uid] = None
                    continue
                cache[uid] = (U, [trade(U, cache.setdefault("foe" + f, load_unit(f)), n=a.n) for f, _ in TRADE_FOES])
            if not cache[uid]:
                continue
            U, tr = cache[uid]
            cnt = count_at(sp["nreff"], shown, base) if k == 0 else shown
            if sp["one_of"] and k:
                continue
            for j, (t, hold) in enumerate(tr):
                total[j] += cnt * t
            tags |= {t for t in SUMMON_TAGS if t in U["tags"]}
            tags |= {f"{x} {U['ab'][x]}" for x in SUMMON_ABS if x in U["ab"]}
            if U["mpath"]:
                tags.add(U["mpath"].split(" R")[0])
            if any(w["ranged"] for w in U["weapons"]):
                tags.add("missile")
            units_txt.append(f"{cnt} x {U['name']} (hp {U['hp']}, prot {U['body']}, def {U['def']}, MR {U['mr']}, sz {U['size']})")
        if not units_txt:
            continue
        casters = [c for c, pth in (CASTERS if sp["type"] == "Combat" else RITUAL_CASTERS) if can_cast({"path": sp["path"]}, parse_paths(pth))]
        gems = sp["gems"] or 0
        rows.append((sp, units_txt, total, gems, sorted(tags), casters[0] if casters else ""))
    rows.sort(key=lambda r: -(r[2][0] / max(r[3], 1)))
    print("| Spell | Research | Path | Gems | Summons | Kills vs " + " | Kills vs ".join(f[1] for f in TRADE_FOES)
          + " | HI kills / gem | Notes | Pythium caster |")
    print("|---|---|---|---|---|" + "---|" * len(TRADE_FOES) + "---|---|---|")
    for sp, ut, total, gems, tags, cas in rows:
        kind = ("combat" if sp["type"] == "Combat" else "ritual") + (", remote" if sp["remote"] else "") + (", one of" if sp["one_of"] else "")
        print(f"| {sp['name']} | {sp['research']} ({kind}) | {sp['path']} | {gems}{sp['gempath']} | {'; '.join(ut)} | "
              + " | ".join(f"{t:.1f}" for t in total) + f" | {total[0] / max(gems, 1):.2f} | {', '.join(tags)} | {cas} |")


def main():
    random.seed(6)
    if "--data" in sys.argv:                       # a modded game (dom6-modinspector output), e.g. dom6-scbm/data/inspector
        i = sys.argv.index("--data")
        inspector.DATA = os.path.abspath(sys.argv[i + 1])
        del sys.argv[i:i + 2]
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("list")
    l.add_argument("--paths")
    l.add_argument("--kind")
    l.add_argument("--school")
    l.add_argument("--max-level", type=int)
    l.add_argument("--name")
    l.add_argument("--all", action="store_true")
    c = sub.add_parser("castable")
    c.add_argument("--out")
    for name in ("melee", "missile"):
        m = sub.add_parser(name)
        m.add_argument("x_unit")
        m.add_argument("y_unit")
        m.add_argument("--x", default="")
        m.add_argument("--y", default="")
        m.add_argument("--range", type=int)
    dm = sub.add_parser("damage")
    dm.add_argument("--school", default="Evocation")
    dm.add_argument("--spells")
    dm.add_argument("--range", type=int, default=25)
    dm.add_argument("-n", type=int, default=400)
    sm = sub.add_parser("summons")
    sm.add_argument("-n", type=int, default=3000)
    r = sub.add_parser("rank")
    r.add_argument("--melee-unit", default="685")
    r.add_argument("--missile-units", default="684,32")
    a = p.parse_args()
    {"list": cmd_list, "castable": cmd_castable, "melee": cmd_melee, "missile": cmd_missile, "rank": cmd_rank, "damage": cmd_damage,
     "summons": cmd_summons}[a.cmd](a)


if __name__ == "__main__":
    main()
