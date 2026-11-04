---
name: dom6-items
description: Claude's ranked guide to Dominions 6 magic items for its own play: every forgeable item sorted into killing items (weapons, missile and dancing weapons, offensive item spells), protection items (armour, shields, helmets, protective amulets and rings) and utility items (path boosters, penetration, research, gem income, flight, leadership), measured with the dom6-spells combat model on a Pythium Emerald Lord (heavy infantry killed a round, attacks and arrows it takes to kill the wearer), with gem cost, construction level and which Pythium mage can forge each. Uses dom6-inspector (item data), dom6-spells (combat model), dom6-mechanics (rules). Use when choosing what to forge, kitting a thug or mage, asking what an item is worth, or planning Construction research.
---

# Dom6 items

Every forgeable magic item (Construction 1-9), ranked in the user's three categories: killing,
protection and utility (2026-10-28). Killing and protection items are measured with the
dom6-spells melee and missile model; utility items are ranked by hand against the Pythium plan.
It does not cover national items of other nations, unforgeable artifacts (Construction 11+), or
items inside battles in progress.

## Files

- `items.md`: the ranking, S to D, for each category. Thug and mage protection are separate.
  Ends with the forging order for Pythium and the model's limits.
- `killing-table.md`, `protection-table.md`, `utility-table.md`: the full generated tables.
- `scripts/items.py`:
  - `killing [-n 4000]`: the item replaces the Emerald Lord's broad sword (a two-handed item
    also drops his shield); HI and Cataphracts killed a round.
  - `protection [-n 4000] [--wearer 6|42]`: the item replaces the wearer's piece in its slot;
    HI attacks to kill and hp lost to 100 short-bow arrows. 6 = Emerald Lord, 42 = Theurg.
    Another wearer needs a `KIT_DEF` entry (defence of the body armour and shield it loses).
  - `utility`: lists by category (boosters, penetration, casting, research, gems, movement,
    command, battle spells, senses).
  - `FORGERS` and `CONST_NOW` at the top: update when new mages arrive or Construction advances.
- Builds on **dom6-inspector** (item pages), **dom6-spells** (`spells.py`: `load_unit`,
  `melee_stats`, `missile_stats`) and **dom6-mechanics** (rules).

Run Python with `python3 -I` (system Python with PIL only; no pip). Each battery takes a few
minutes.

## Workflow

1. One item: `inspector.py item NAME`, then its row in the tables.
2. What to forge now: the "What to forge, in order" list in `items.md`, checked against the
   Construction level reached and the gems in the treasury.
3. A new thug or mage type: run `protection --wearer ID` (add a `KIT_DEF` entry) and compare.
4. After a battle, note real item effects (shield blocks, regeneration) under Model limits.
5. Report what was done, where it is, and what is untested.

## Facts and gotchas

- "Requires 10A to forge (A2)" on the item page is the forging path level. Bartholomeus is W2;
  the ordinary Arch Theurg is W1 + random, so W2 items need Bartholomeus or a Water roll.
- **Temporary gems** (`tmp...gems`: Water Lens, Bag of Winds, Cornucopia) are battle-only gems
  for combat spells, not income. Income items say "generates ... gems per month" (`gf`, `gs`...).
- Shields block most missiles (manual: DRN + half the size points vs DRN + 2 × parry). So a
  shield is a mage's best arrow protection, and missile items are weak against shielded troops.
- Misc-slot weapons (Dancing Trident, Death Globes) attack beside the wielder's own weapon and
  keep his shield.
- `unique` items (Armor of Virtue) can be forged once per game.
- Cursed items can't be taken off; the tables mark them.
- Not in the batteries: the Sky Metal Matrix, Ring of Returning, quickness, and other effects
  without a combat number. Judge them by hand.

## Standards (audit 2026-11-03)
- **Modded games:** numbers here are vanilla - check the mod first (dom6-scbm for SCBM; mod-docs).

## Related skills
dom6-inspector, dom6-spells, dom6-tactics (thugs.md), dom6-army-check.
Also (2026-11-03): dom6-forging, dom6-supercombatants, dom6-thugs, game-database.
