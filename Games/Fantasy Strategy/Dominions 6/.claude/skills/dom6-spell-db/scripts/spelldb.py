#!/usr/bin/env python3
"""Spell evaluation database for Dominions 6: every spell (combat and ritual, generic and national), sorted by
PURPOSE and scored within it, saved as SQLite + CSV + one markdown page per purpose.

  python3 -I spelldb.py build [--data DIR --label NAME] [-n 60]
        vanilla by default (label "vanilla"); a mod: --data <dom6-modinspector folder> --label scbm.
        Writes ../data/<label>/spells.sqlite and spells.csv, and ../<label>/<purpose>.md (top lists).
  python3 -I spelldb.py top PURPOSE [--paths E2N2G1H2] [--nation "Tir na"] [--max-level 6] [--school Alt]
                         [--top 25] [--label L]      --paths alone = generic spells only; --nation adds that
                                                     nation's own spells
  python3 -I spelldb.py spell NAME [--label L]           every column for matching spells
  python3 -I spelldb.py purposes [--label L]              purposes and counts
  python3 -I spelldb.py sql "SELECT ..." [--label L]      anything else (table: spells)

How scores are made (all at the spell's REQUIRED path level; read SKILL.md before trusting a number):
  damage   simulated casts (dom6-spells cast_once, real DRN, shields, MR, AP/AN) into packed Militia, sword
           Heavy Infantry and Barbarians: kills per cast (value); mages killed per cast separately (mage_k).
  summons  each summoned unit's melee trade vs sword Heavy Infantry (dom6-spells trade): enemy men killed
           before it dies x count (value); value per gem (eff).
  others   effect weight (keyword table below) x men covered (area squares x 3; battlefield = 180) x MR
           landing chance (0.45 if MR negates) -> value; eff = value / cost (fatigue/100 + gems + 0.2).
  rituals  without a model: no value; ranked by purpose and cost only (basis "cost").
  sacred-only buffs count 0.3 of the coverage; "unresearchable" entries (event or secondary effects) get tier "-".
  tier     S/A/B/C/D by percentile of score inside the purpose (S top 10%, A next 20%, B 30%, C 25%, D 15%);
  curated  my hand tiers from dom6-spells/*.md (vanilla judgements, Pythium-era), where a spell was named.
"""
import csv
import math
import os
import random
import re
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
SPELLS_DIR = os.path.join(SKILL, "..", "dom6-spells", "scripts")
sys.path.insert(0, SPELLS_DIR)


def arg(name, default=None, cast=str):
    if name in sys.argv:
        i = sys.argv.index(name)
        v = sys.argv[i + 1]
        del sys.argv[i:i + 2]
        return cast(v)
    return default


DATA = arg("--data")
LABEL = arg("--label", "vanilla" if not DATA else os.path.basename(os.path.normpath(DATA)))
N = arg("-n", 60, int)
TOP = arg("--top", 25, int)
PATHS = arg("--paths")
MAXLVL = arg("--max-level", 99, int)
SCHOOL = arg("--school", "")
NATION = arg("--nation")
saved = sys.argv
sys.argv = [saved[0]]
import spells as S  # noqa: E402
sys.argv = saved
if DATA:
    S.inspector.DATA = os.path.abspath(DATA)

DBDIR = os.path.join(SKILL, "data", LABEL)
MDDIR = os.path.join(SKILL, LABEL)

BUFF_W = [("Invulnerability", 10), ("Quickness", 9), ("Body Ethereal|Ethereal", 8), ("Mistform", 8),
          ("Liquid Body", 5), ("Air Shield", 6), ("Luck", 5), ("Twist Fate", 4), ("Regeneration", 5),
          ("Limited Regeneration", -2), ("Ironskin", 7), ("Stoneskin", 6), ("Barkskin", 5),
          ("natural protection", 5), ("Extra Strength|\\bStr\\b", 4), ("Attack skill|\\bAtt\\b", 3),
          ("\\bDef\\b|Defence", 3), ("Improved Precision|Precision", 3), ("Magic Resistance", 4),
          ("Flight", 4), ("Fire Resistance|Cold Resistance|Shock Resistance|Poison Resistance", 2),
          ("Slashing Resistance|Piercing Resistance|Bludgeoning Resistance|Blunt and Pierce", 4),
          ("Swiftness", 3), ("Blessing", 3), ("Unholy Power", 4), ("Heal", 3), ("Remove Fatigue", 4),
          ("Temporary Morale Boost|Morale", 3), ("Enlargement", 4), ("Displacement|Blur", 4),
          ("Mirror Image", 5), ("Sharp|armorpiercing", 4), ("Fire Shield|Fire Flies", 3), ("Darkvision", 1),
          ("magic levels|Power of the Spheres", 6), ("Spell Ward|Arrow", 3), ("Berserk", 3), ("Awe", 4)]
DEBUFF_W = [("Time Stop", 10), ("Petrif", 8), ("Enslave", 8), ("Charm", 8), ("Paralyze", 7), ("Polymorph", 6),
            ("Blind", 6), ("Stun", 5), ("Sleep", 5), ("Enfeeble Mind|Feeblemind", 5), ("Damage Armor|Armor", 5),
            ("Fascinate", 4), ("Confusion", 4), ("Cripple", 4), ("Cause Fear|Fear", 3), ("Entangle", 3),
            ("Earth Grip", 3), ("Slime", 3), ("Fatigue", 3), ("Desiccation", 3), ("Immolate", 3), ("Magic Duel", 3),
            ("Curse", 2), ("Decay", 2), ("Disease", 2), ("Bleed", 2), ("Limp", 2), ("Weaken|Att", 2),
            ("Horror Mark", 1), ("Darkness", 3), ("Storm", 2)]
RITUAL_PURPOSE = [("Remote Site Search|Acashic", "site search"), ("Summon Commander|Unique Commander", "summon commander"),
                  ("Summon|Cross Breeding|Infernal Breeding|Winged Monkeys|Birds of Splendour|Awaken", "summon units"),
                  ("Enchant World|Global", "global enchantment"),
                  ("Fires from Afar|Remote Curse|Seeking Arrow|Affect Half of Army|Affect Province|Mind Hunt|"
                   "Astral Harpoon|Horror Seed|Leprosy|Raven Feast|Assassination|Vengeance|Crumble|Swallow",
                   "remote attack"),
                  ("Teleport|Travel|Trapeze|Wind Ride|Faery Trod|Stygian|Mirror Walk|Gateway|Beckoning|Return Home",
                   "movement"),
                  ("Transport", "logistics"), ("Enchant Province|Fort Construction|Ice Walls", "province enchantment"),
                  ("Cure|Blood Feast|Rebirth|Pyre", "healing"), ("Alchemy|Gold", "economy"),
                  ("Scry|Project|Dispel|Gift of Reason|Imprint|Mind Vessel", "utility")]
# rituals whose effect text is an opaque code: classified by name (checked first)
RITUAL_BY_NAME = [("Distill Gold|Transmut|Gem Alchemy|Alchemical", "economy"),
                  ("Disenchantment|Elemental Opposition|Project Self|Arcane Analysis|Wish", "utility"),
                  ("Nexus Gate|Returning", "movement"), ("Tartarian Gate|Manifestation", "summon units"),
                  ("Lichcraft|Twiceborn|Simulacrum|Transformation|Rejuvenate|Dragon Master|Lore of Legends|Inner Sun",
                   "caster upgrade")]
TARGETS = [("18", "Militia", 3), ("39", "Heavy Inf", 3), ("139", "Barbarian", 3)]


def all_spells():
    recs = {str(r.get("id")): r for r in S.inspector.records("spells")}
    out = []
    for i, name, block in S.inspector.pages("spells"):
        L = block.split("\n")
        nat = ""
        if len(L) > 4 and L[3] not in ("Combat", "Ritual") and L[4] in ("Combat", "Ritual"):
            nat = L[3]
            L = L[:3] + L[4:]
        if len(L) < 4 or L[3] not in ("Combat", "Ritual"):
            continue
        d = {"id": i, "name": L[2], "research": L[1], "type": L[3], "path": "", "fx": [], "kv": {}}
        if len(L) > 4 and re.match(r"^([FAWESDNGBH]\d)+$", L[4]):
            d["path"] = L[4]
        for line in L[4:]:
            m = re.match(r"^(.*?) \[(\w+)\]: (.*)$", line)
            if m:
                d["kv"].setdefault(m.group(2), m.group(3))
            elif line.startswith("description:"):
                d["desc"] = line[12:].strip()
            elif line not in ("[wiki]", d["path"]) and line.strip():
                d["fx"].append(line)
        d["flags"] = sorted(set(re.findall(r"\[(\w+)\]", " ".join(d["fx"]))))
        nats = (recs.get(i) or {}).get("nations") or {}
        vals = nats.values() if isinstance(nats, dict) else nats
        d["nations"] = "; ".join(sorted(v.get("name", str(v)) if isinstance(v, dict) else str(v) for v in vals)) or nat
        out.append(d)
    return out


def req_level(d):
    p = S.parse_paths(d["path"])
    return max(p.values()) if p else 1


def gems_of(d):
    m = re.match(r"(\d+)([FAWESDNGB]?)", d["kv"].get("gemcost", "") or "")
    return (int(m.group(1)), m.group(2)) if m else (0, "")


def fat_of(d):
    return int(re.sub(r"\D", "", d["kv"].get("fatiguecost", "0")) or 0)


def purpose(d):
    fx = " / ".join(d["fx"])
    first = d["fx"][0] if d["fx"] else ""
    if d["type"] == "Ritual":
        for rx, p in RITUAL_BY_NAME:
            if re.search(rx, d.get("name", "")):
                return p
        for rx, p in RITUAL_PURPOSE:
            if re.search(rx, first) or (p in ("site search", "global enchantment") and re.search(rx, fx)):
                return p
        return "ritual other"
    k = S.kind_of({"fx": d["fx"]})
    area = d["kv"].get("aoe_s", "")
    lvl = req_level(d)
    if k == "damage":
        n = S.area_of(area, lvl) * max(1, S.scaled(d["kv"].get("nreff", "1"), lvl) if d["kv"].get("nreff", "1").lstrip("-").isdigit() else 1)
        return "army damage" if n >= 4 or "%" in area else "single-target damage"
    if k == "summon":
        return "battle summon"
    if k == "battlefield":
        return "battlefield enchantment"
    if k == "debuff":
        return "fear / morale attack" if re.search(r"Cause Fear", fx) and not re.search(r"Stun|Paralyze|Sleep", fx) else "debuff"
    if k == "buff":
        if re.search(r"Remove Fatigue|^Heal|Return Home|Blink", first):
            return "utility (combat)"
        if area in ("Caster",):
            return "self buff"
        a = S.area_of(area, lvl)
        return "army buff" if a >= 20 or "%" in area else "group buff"
    if re.search(r"Communion|Sabbath|Chorus", d["name"]):
        return "communion"
    return "combat other"


def men_covered(d):
    area = d["kv"].get("aoe_s", "")
    if "%" in area:
        return 180
    if area in ("Caster", "One person", "", "-"):
        return 1
    a = S.area_of(area, req_level(d))
    return max(1, a) * 3


def weight(d, table):
    fx = " / ".join(d["fx"]) + " " + d["name"]
    w = 0
    for rx, v in table:
        if re.search(rx, fx):
            w += v
    return max(w, 1)


def mr_factor(d):
    f = set(d["flags"])
    if "sacredonly" in f:                               # only sacred units (Divine Blessing): a part of an army
        return 0.3
    if "hardmrneg" in f:
        return 0.6
    if "mrnegateseasily" in f:
        return 0.25
    if "mrnegates" in f:
        return 0.45
    return 1.0


def score_damage(d):
    try:
        sp = S.spell_blocks(d["id"])
    except Exception:
        return None
    lvl = req_level(d)
    r = S.range_of(sp["blocks"][0]["kv"].get("rng_bat"), lvl)
    R = min(r, 25) if r else 25
    kills = []
    for tid, _, per_sq in TARGETS:
        T = S.load_unit(tid)
        k = sum(S.cast_once(sp, lvl, 0, T, per_sq, (6, 3), R)[1] for _ in range(N)) / N
        kills.append(k)
    mk = sum(S.cast_once(sp, lvl, 0, S.MAGE, 1, (6, 1), R)[1] for _ in range(N)) / N
    return sum(kills) / len(kills), mk, kills


_units = {}


def score_summon(d):
    lvl = req_level(d)
    fxs = " / ".join(x for x in d["fx"] if not re.match(r"(Underwater|Cold) summon", x))
    bare = re.sub(r"\[[^\]]*\]", "", fxs)
    units = [(u, int(n) if n else 1) for u, n in re.findall(r"#(\d+) [^#/,]*?(?: x (\d+)\+*)?(?= /|,|$| #)", bare)]
    if not units:
        return None
    foe = _units.setdefault("foe", S.load_unit("39"))
    tot = 0.0
    names = []
    for k, (uid, shown) in enumerate(units[:4]):
        if uid not in _units:
            try:
                U = S.load_unit(uid)
                _units[uid] = (U, S.trade(U, foe, n=max(80, N * 2))[0])
            except BaseException:
                _units[uid] = None
        if not _units[uid]:
            continue
        U, t = _units[uid]
        cnt = S.count_at(d["kv"].get("nreff"), shown, lvl) if k == 0 else shown
        if "Unique" in fxs and k:
            continue
        tot += cnt * t
        names.append(f"{cnt} {U['name']}")
    return tot, "; ".join(names)[:160]


def evaluate(d):
    p = purpose(d)
    g, gp = gems_of(d)
    fat = fat_of(d)
    cost = fat / 100 + g + 0.2
    row = {"id": d["id"], "name": d["name"], "type": d["type"], "research": d["research"], "path": d["path"],
           "req_level": req_level(d), "nations": d["nations"], "purpose": p, "gems": f"{g}{gp}" if g else "",
           "fatigue": fat or "", "range": d["kv"].get("rng_bat", ""), "area": d["kv"].get("aoe_s", ""),
           "effects": d["kv"].get("nreff", ""), "precision": d["kv"].get("precision", ""),
           "flags": S.flag_text({"flags": d["flags"]}), "effect": S.effect_text({"fx": d["fx"]}, 200),
           "value": None, "mage_k": None, "eff": None, "basis": "cost", "detail": ""}
    if p in ("army damage", "single-target damage"):
        r = score_damage(d)
        if r:
            row["value"], row["mage_k"] = round(r[0], 3), round(r[1], 3)
            row["detail"] = "kills/cast " + ", ".join(f"{n} {k:.2f}" for (_, n, _), k in zip(TARGETS, r[2]))
            row["eff"] = round(r[0] / cost, 3)
            row["basis"] = "simulated"
    elif p in ("battle summon", "summon units", "summon commander"):
        r = score_summon(d)
        if r:
            row["value"] = round(r[0], 2)
            row["eff"] = round(r[0] / max(g, 1), 2) if d["type"] == "Ritual" else round(r[0] / cost, 2)
            row["detail"] = r[1]
            row["basis"] = "simulated"
    elif d["type"] == "Combat":
        table = DEBUFF_W if p in ("debuff", "fear / morale attack") else BUFF_W
        v = weight(d, table) * men_covered(d) * mr_factor(d)
        row["value"] = round(v, 1)
        row["eff"] = round(v / cost, 1)
        row["basis"] = "weights"
    return row


def score_of(r):
    if r["value"] is None:
        lvl = r["req_level"] or 1
        return -(lvl + (int(re.sub(r"\D", "", r["gems"]) or 0) / 10 if r["gems"] else 0))   # cheaper = higher
    return r["value"] * math.sqrt(max(r["eff"] or 0, 0.01) / max(r["value"], 0.01)) if r["eff"] else r["value"]


def tiers(rows):
    by = {}
    for r in rows:
        by.setdefault(r["purpose"], []).append(r)
    for p, rs in by.items():
        rs.sort(key=lambda r: (r["research"] == "unresearchable", -score_of(r)))
        n = sum(r["research"] != "unresearchable" for r in rs)   # event/effect-only entries get no tier
        for i, r in enumerate(rs):
            if r["research"] == "unresearchable":
                r["rank"], r["tier"], r["score"] = i + 1, "-", round(score_of(r), 3)
                continue
            q = i / max(n, 1)
            r["rank"] = i + 1
            r["tier"] = "S" if q < .10 else "A" if q < .30 else "B" if q < .60 else "C" if q < .85 else "D"
            r["score"] = round(score_of(r), 3)


def curated(rows):
    names = sorted({r["name"] for r in rows}, key=len, reverse=True)
    found = {}
    for f in sorted(os.listdir(os.path.join(SKILL, "..", "dom6-spells"))):
        if not f.endswith(".md"):
            continue
        for line in open(os.path.join(SKILL, "..", "dom6-spells", f), encoding="utf-8"):
            m = re.match(r"\| ([SABCDF]) \| (.*?) \|", line)
            if not m:
                continue
            cell = re.sub(r"\*|\(.*?\)", "", m.group(2))
            for nm in names:
                if re.search(r"(?<![\w'])" + re.escape(nm) + r"(?![\w'])", cell):
                    found.setdefault(nm, f"{m.group(1)} ({f[:-3]})")
                    cell = cell.replace(nm, "")
    for r in rows:
        r["curated"] = found.get(r["name"], "")


COLS = ["id", "name", "type", "research", "path", "req_level", "nations", "purpose", "tier", "rank", "score", "value",
        "eff", "mage_k", "basis", "curated", "gems", "fatigue", "range", "area", "effects", "precision", "flags",
        "effect", "detail"]


def build():
    random.seed(6)
    sp = all_spells()
    rows = []
    for k, d in enumerate(sp):
        rows.append(evaluate(d))
        if k % 100 == 0:
            print(f"  {k}/{len(sp)}", file=sys.stderr)
    tiers(rows)
    curated(rows)
    os.makedirs(DBDIR, exist_ok=True)
    os.makedirs(MDDIR, exist_ok=True)
    dbp = os.path.join(DBDIR, "spells.sqlite")
    if os.path.exists(dbp):
        os.remove(dbp)
    con = sqlite3.connect(dbp)
    con.execute("CREATE TABLE spells (" + ", ".join(COLS) + ")")
    con.executemany("INSERT INTO spells VALUES (" + ",".join("?" * len(COLS)) + ")", [[r.get(c) for c in COLS] for r in rows])
    con.commit()
    with open(os.path.join(DBDIR, "spells.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    by = {}
    for r in rows:
        by.setdefault(r["purpose"], []).append(r)
    idx = [f"# Spell database: {LABEL} ({len(rows)} spells)", "",
           "Generated by dom6-spell-db/scripts/spelldb.py. Score basis per row: simulated / weights / cost. "
           "Read the skill's caveats before trusting a number.", "", "| Purpose | Spells | Page |", "|---|---|---|"]
    for p, rs in sorted(by.items(), key=lambda kv: -len(kv[1])):
        fn = re.sub(r"[^a-z0-9]+", "-", p.lower()).strip("-") + ".md"
        idx.append(f"| {p} | {len(rs)} | [{fn}]({fn}) |")
        rs.sort(key=lambda r: r["rank"])
        o = [f"# {p} ({LABEL}, {len(rs)} spells)", "", "Generic (researchable by anyone) first; national spells after.", ""]
        for title, part in (("Generic", [r for r in rs if not r["nations"] and r["research"] != "unresearchable"]),
                            ("National / unresearchable", [r for r in rs if r["nations"] or r["research"] == "unresearchable"])):
            if not part:
                continue
            o += [f"## {title}", "", "| # | Tier | Spell | Research | Path | Gems | Fat | Area | Value | Eff | Curated | Detail / effect |",
                  "|---|---|---|---|---|---|---|---|---|---|---|---|"]
            for r in part:
                o.append(f"| {r['rank']} | {r['tier']} | {r['name']} | {r['research']} | {r['path']} | {r['gems']} | {r['fatigue']} | "
                         f"{r['area']} | {r['value'] if r['value'] is not None else ''} | {r['eff'] if r['eff'] is not None else ''} | "
                         f"{r['curated']} | {(r['detail'] or r['effect'])[:150].replace('|', '/')} |")
            o.append("")
        open(os.path.join(MDDIR, fn), "w").write("\n".join(o))
    open(os.path.join(MDDIR, "INDEX.md"), "w").write("\n".join(idx) + "\n")
    print(f"{len(rows)} spells -> {dbp}, {MDDIR}/")


def db():
    p = os.path.join(DBDIR, "spells.sqlite")
    if not os.path.exists(p):
        sys.exit(f"no database for '{LABEL}' yet: spelldb.py build" + (f" --data {DATA} --label {LABEL}" if DATA else ""))
    con = sqlite3.connect(p)
    con.row_factory = sqlite3.Row
    return con


def show(rows, cols=("rank", "tier", "name", "research", "path", "gems", "fatigue", "area", "value", "eff", "curated", "detail")):
    rows = list(rows)
    print("| " + " | ".join(cols) + " |\n|" + "---|" * len(cols))
    for r in rows:
        print("| " + " | ".join(str(r[c] if r[c] is not None else "")[:90].replace("|", "/") for c in cols) + " |")
    print(f"\n{len(rows)} rows")


def castable(path):
    if not PATHS:
        return True
    return S.can_cast({"path": path}, S.parse_paths(PATHS))


def for_nation(r):
    """--nation X: generic spells + X's own; --paths without --nation: generic only."""
    if not r["nations"]:
        return r["research"] != "unresearchable"
    if NATION:
        return NATION.lower() in r["nations"].lower()
    return not PATHS


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    c = a[0]
    if c == "build":
        build()
    elif c == "purposes":
        for r in db().execute("SELECT purpose, count(*) n FROM spells GROUP BY purpose ORDER BY n DESC"):
            print(f"{r['n']:4} {r['purpose']}")
    elif c == "top":
        p = " ".join(a[1:])
        rows = [r for r in db().execute("SELECT * FROM spells WHERE purpose LIKE ? ORDER BY rank", (f"%{p}%",))
                if castable(r["path"]) and for_nation(r) and r["research"].startswith(SCHOOL)
                and (not re.search(r"\d", r["research"]) or int(re.search(r"\d+", r["research"]).group()) <= MAXLVL)]
        show(rows[:TOP])
    elif c == "spell":
        q = " ".join(a[1:])
        for r in db().execute("SELECT * FROM spells WHERE name LIKE ?", (f"%{q}%",)):
            print("\n".join(f"{k}: {r[k]}" for k in r.keys()) + "\n")
    elif c == "sql":
        cur = db().execute(a[1])
        show(cur.fetchall(), [x[0] for x in cur.description])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
