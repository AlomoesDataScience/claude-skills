---
name: game-database
description: Build a "rank everything" database for any game - every unit, spell, item, tech or building read from the game's data files (never from memory), sorted by PURPOSE (what it's for), scored inside each purpose with value, cost, efficiency and a stated basis (simulated / weights / cost / stat), tiered by percentile (S-D), hand tiers kept beside the automatic ones, and written as SQLite + CSV + one markdown page per purpose. gamedb.py does the building and querying from a rows file plus a small scorer file (purpose() and score()); the method covers choosing purposes, scoring by simulation where possible, cost models, the trust section, and the sanity checks that catch bad rows. Worked case - Dominions 6 dom6-spell-db (1474 spells). Use when the user asks to rank or evaluate all of something in a game, wants "what's good for X" lists, when comparing options across a big catalogue, or when building an evaluation table for one of our own games.
---

# Rank-everything databases (any game)

Generalized 2026-11-03 from dom6-spell-db (the user: "just rank all the spells and make a spell evaluation
database. There might be spells you didn't catch, just do it", then "We're going to need to generalize all
this stuff"). Writing the matching skill: rules-skills section 5.

## Method
1. **Rows from data, not memory.** Export the game's files (Dominions: the inspector) to CSV/JSON - every row,
   generic and faction-specific. This is what finds the things the hand lists missed.
2. **Purposes first.** Rank inside "what it's for" (army damage, anti-armour, scouting, economy...), never
   across: an S debuff and an S summon aren't comparable. A row the rules can't place goes to "other" - read
   that list and add name or effect rules until it's small.
3. **Score with the best model available**, and record which: **simulated** (unit-combat-math, a game's own
   calculator) > **weights** (effect x coverage x chance it lands - judgement, say so) > **stat** (one number)
   > **cost** (no model: cheapest first). Value per cost = efficiency; score = sqrt(value x efficiency).
4. **Tiers by percentile inside a purpose** (S 10%, A 20%, B 30%, C 25%, D 15%). Keep **hand tiers** in their
   own column; they win where they disagree, and the disagreement is worth reading.
5. **Sanity-check every top list** before calling it done. Found in Dominions: unobtainable event entries at
   #1 (now tier "-"), faction-only buffs counted as army-wide, a nations field cut at 120 characters,
   undead-only spells scoring 0 against living targets, rituals with opaque effect codes all in "other".
6. **Trust section** in the skill: what each basis means, what the simulation leaves out, when to trust the
   hand tier instead.
7. **Mods**: build again from the mod's data with its own label; compare with mod-diff.

## gamedb.py
```
python3 -I scripts/gamedb.py build ROWS.csv SCORER.py --out DIR [--label NAME] [--name-col name]
python3 -I scripts/gamedb.py top DIR "line infantry" [--top 25] [--where "cost<=20"]
python3 -I scripts/gamedb.py purposes DIR
python3 -I scripts/gamedb.py sql DIR "SELECT name, tier FROM things WHERE basis='simulated'"
```
The scorer file defines `purpose(row)` and `score(row) -> {value, cost, basis, detail}`; optional
`exclude(row)` and `CURATED = {name: tier}`. Example: `examples/score_example.py` (units scored by a simulated
melee trade against heavy infantry, per gold, with unit-combat-math) on `examples/units_example.csv`.
Output: `<label>.sqlite` (table `things`), `<label>.csv`, `INDEX.md`, one page per purpose.

## Worked case: Dominions 6 spells (dom6-spell-db)
1474 vanilla / 1576 SCBM spells, ~25 purposes. Damage spells simulated (kills per cast into three reference
troop blocks), summons by melee trade, buffs and debuffs by weights x coverage x MR, rituals by cost; generated
skills from it: dom6-best-by-purpose and the eight dom6-path-* skills.

## Related skills
unit-combat-math (simulated scores), dice-math, mod-diff (what a mod changed), rules-skills, dom6-spell-db,
dom6-best-by-purpose, borrow-from-games (evaluation tables for our designs), skills-manager.
