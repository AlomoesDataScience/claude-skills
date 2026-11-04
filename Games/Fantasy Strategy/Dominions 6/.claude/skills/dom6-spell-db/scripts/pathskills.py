#!/usr/bin/env python3
"""Write the per-path vanilla skills (dom6-path-fire ... dom6-path-glamour) from the spell database and the
illwiki path pages. Re-run after a database rebuild.

  python3 -I pathskills.py [--label vanilla] [--top 5]

Each skill gets SKILL.md (what the path does and gives a mage - from the wiki - plus the best generic spells
of that path per purpose from the database) and spells.md (every generic spell with that primary path, by
research level). Blood has its own skills (dom6-blood, dom6-blood-hunting); Holy is dom6-holy.
"""
import os
import re
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.path.normpath(os.path.join(HERE, "..", ".."))
WIKI = os.path.normpath(os.path.join(SKILLS, "..", "..", "illwiki", "pages"))
a = sys.argv[1:]
LABEL = a[a.index("--label") + 1] if "--label" in a else "vanilla"
MOD = LABEL != "vanilla"     # a mod: plain pages in dom6-<label>/lists/ (mod-docs), not skills


def outdir(sub):
    return os.path.join(SKILLS, f"dom6-{LABEL}", "lists", sub) if MOD else os.path.join(SKILLS, sub)


def finish(path):
    """mods: drop the skill frontmatter and rename SKILL.md -> README.md, mark the label in the title"""
    if not MOD:
        return
    t = open(path, encoding="utf-8").read()
    t = re.sub(r"\A---\n.*?\n---\n\n", "", t, flags=re.S).replace("(Dominions 6, vanilla)", f"(Dominions 6, {LABEL})")
    t = t.replace("Best in vanilla, by purpose", f"Best in {LABEL}, by purpose")
    new = os.path.join(os.path.dirname(path), "README.md")
    open(new, "w", encoding="utf-8").write(t)
    os.remove(path)
TOP = int(a[a.index("--top") + 1]) if "--top" in a else 5
PATHS = {"F": "fire", "A": "air", "W": "water", "E": "earth", "S": "astral", "D": "death", "N": "nature",
         "G": "glamour"}
ORDER = ["army damage", "single-target damage", "army buff", "group buff", "self buff", "debuff",
         "fear/morale attack", "battlefield enchantment", "battle summon", "utility (combat)", "communion",
         "summon units", "summon commander", "remote attack", "global enchantment", "province enchantment",
         "site search", "movement", "logistics", "healing", "economy", "caster upgrade", "utility", "ritual other",
         "combat other"]


def clean(t):
    t = re.sub(r"\{\{path>([A-Z0-9]+)\}\}", r"\1", t)
    t = re.sub(r"\{\{[^}]*\}\}", "", t)
    t = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"\[\[([^\]]*)\]\]", r"\1", t)
    t = t.replace("??", "").replace("**", "").replace("//", "").replace("\\\\", ";")
    return re.sub(r"[ \t]+", " ", t).strip()


def section(txt, head):
    m = re.search(r"=+ *" + head + r"[^=\n]*=+ *\n(.*?)(?=\n=+ |\Z)", txt, re.S)
    return clean(m.group(1)) if m else ""


def level_of(research):
    m = re.search(r"(\d+)$", research or "")
    return int(m.group(1)) if m else -1


def main():
    db = sqlite3.connect(os.path.join(SKILLS, "dom6-spell-db", "data", LABEL, "spells.sqlite"))
    db.row_factory = sqlite3.Row
    rows = [dict(r) for r in db.execute("select * from spells where nations='' and research!='unresearchable'")]
    for letter, name in PATHS.items():
        mine = [r for r in rows if (r["path"] or "").startswith(letter)]
        wiki = open(os.path.join(WIKI, name + ".txt"), encoding="utf-8").read()
        intro = section(wiki, f"{name.title()} Spells").split("\n")[0]
        indirect = " ".join(x for x in section(wiki, "Indirect Magic").split("\n") if x.strip())
        boost = " ".join(x for x in section(wiki, "Path Boosting").split("\n") if x.strip())
        cross = [x.strip(" *") for x in section(wiki, "(?:" + name.title() + " )?Crosspaths").split("\n")
                 if x.strip().startswith("*")]
        best = []
        for p in ORDER:
            got = sorted((r for r in mine if r["purpose"] == p and r["tier"] in ("S", "A")),
                         key=lambda r: (r["rank"] or 9999))[:TOP]
            if got:
                best.append(f"- **{p}**: " + "; ".join(
                    f"{r['name']} ({r['path']}, {r['research']}, {r['tier']}"
                    + (f", hand {r['curated'].split()[0]}" if r["curated"] else "") + ")" for r in got))
        purposes = sorted({r["purpose"] for r in mine}, key=lambda p: ORDER.index(p) if p in ORDER else 99)
        desc = (f"The {name.title()} path of Dominions 6 magic, vanilla - what {name} mages get (spells by role, "
                f"indirect magic, path boosters, crosspaths, from illwiki's {name} page) and the {len(mine)} generic "
                f"spells with {name.title()} as their main path, ranked inside each purpose by the spell database "
                f"(dom6-spell-db: tiers, value, cost; best per purpose in SKILL.md, the full list by research level "
                f"in spells.md). Use when judging a {name} mage or a nation's {name} access, planning {name} "
                f"research, scripting {name} casters, choosing {name} spells for a purpose, or when the user asks what "
                f"{name} magic is good for.")
        d = outdir(f"dom6-path-{name}")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write(f"---\nname: dom6-path-{name}\ndescription: {desc}\n---\n\n"
                    f"# {name.title()} magic (Dominions 6, vanilla)\n\n"
                    f"the user (2026-11-03): \"a skill for each elemental path in vanilla would probably good\". "
                    f"Written by `dom6-spell-db/scripts/pathskills.py` from the {LABEL} spell database and illwiki "
                    f"`{name}` - re-run it, don't hand-edit the generated parts. Mods: dom6-mod-magic and the mod's "
                    f"folder (dom6-scbm).\n\n"
                    f"## What the path does (illwiki)\n{intro}\n\n"
                    f"## Indirect magic (what the level itself gives)\n{indirect or '-'}\n\n"
                    f"## Path boosting\n{boost or '-'}\n\n"
                    f"## Crosspaths with {name.title()} first (illwiki)\n" + ("\n".join(f"- {c}" for c in cross) or "-") +
                    f"\n\n## Best generic spells per purpose (database tiers S/A, top {TOP})\n"
                    "Tiers are percentiles inside a purpose across all paths; \"hand\" = my curated tier "
                    "(dom6-spells). Trust notes: dom6-spell-db.\n" + "\n".join(best) +
                    f"\n\nFull list: `spells.md` ({len(mine)} spells; purposes: {', '.join(purposes)}).\n\n"
                    f"## Related skills\ndom6-spell-db, dom6-spells (calculator), dom6-research, dom6-gem-casting, "
                    f"dom6-forging, dom6-summoning, dom6-rituals, dom6-evocations, dom6-buffs, dom6-mod-magic, "
                    f"dom6-mechanics.\n")
        with open(os.path.join(d, "spells.md"), "w", encoding="utf-8") as f:
            f.write(f"# {name.title()} spells (generic, {LABEL}) by research level\n\n"
                    "| Research | Spell | Path | Purpose | Tier | Gems | Fatigue | Area | Effect |\n"
                    "|---|---|---|---|---|---|---|---|---|\n")
            for r in sorted(mine, key=lambda r: (r["research"].split()[0], level_of(r["research"]), r["name"])):
                eff = (r["effect"] or "").replace("|", "/").replace("\n", " ")[:120]
                f.write(f"| {r['research']} | {r['name']} | {r['path']} | {r['purpose']} | {r['tier']} | "
                        f"{r['gems'] or ''} | {r['fatigue'] or ''} | {r['area'] or ''} | {eff} |\n")
        finish(os.path.join(d, "SKILL.md"))
        print(f"{d}: {len(mine)} spells, {len(best)} purposes with S/A picks")
    best_by_purpose(rows)


def best_by_purpose(rows, n=8):
    """dom6-best-by-purpose: the top generic spells of every purpose, all paths, with the research level."""
    lines = []
    for p in ORDER:
        got = sorted((r for r in rows if r["purpose"] == p), key=lambda r: (r["rank"] or 9999))[:n]
        if not got:
            continue
        lines.append(f"\n## {p.title()}\n| # | Spell | Path | Research | Tier | Hand | Why (score basis) |\n"
                     "|---|---|---|---|---|---|---|")
        for r in got:
            why = (r["detail"] or r["basis"] or "").replace("|", "/")[:90]
            lines.append(f"| {r['rank']} | {r['name']} | {r['path']} | {r['research']} | {r['tier']} | "
                         f"{(r['curated'] or '').split(' ')[0]} | {why} |")
    d = outdir("dom6-best-by-purpose")
    os.makedirs(d, exist_ok=True)
    desc = ("What's good in vanilla Dominions 6 for each purpose - the top generic spells (all paths) for army damage, "
            "single-target damage, army/group/self buffs, debuffs, fear, battlefield enchantments, battle summons, "
            "summoned units and commanders, remote attacks, globals, province enchantments, site search, movement, "
            "logistics, healing, economy, caster upgrades and utility, ranked by the spell database with tier, "
            "research level and my hand tier, plus where the item and unit rankings live. Use when choosing what to "
            "research or cast for a job, building a nation's plan, comparing options across paths, or when the user asks "
            "what's good in vanilla for something.")
    with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(f"---\nname: dom6-best-by-purpose\ndescription: {desc}\n---\n\n"
                "# Best in vanilla, by purpose (Dominions 6)\n\n"
                "the user (2026-11-03): \"lists on what's good in vanilla generally for each purpose, might be good too\". "
                f"Generated by `dom6-spell-db/scripts/pathskills.py` from the {LABEL} spell database (generic spells "
                "only - national spells are on the database's purpose pages). Rank = place inside the purpose; "
                "\"Hand\" = my curated tier (dom6-spells), which wins where they disagree. How far to trust each "
                "score: dom6-spell-db. Filter for one mage: `spelldb.py top PURPOSE --paths ... --nation ...`.\n\n"
                "Other rankings: magic items - dom6-items; spells with the calculator - dom6-spells "
                "(buffs-debuffs, evocations, summons pages); per path - dom6-path-<path>; holy - dom6-holy.\n"
                + "\n".join(lines) +
                "\n\n## Related skills\ndom6-spell-db, dom6-spells, dom6-items, dom6-path-fire ... dom6-path-glamour, "
                "dom6-research, dom6-mod-magic (modded games), dom6-mechanics.\n")
    finish(os.path.join(d, "SKILL.md"))
    print(d, "written")


if __name__ == "__main__":
    main()
