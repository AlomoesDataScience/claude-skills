---
name: dom6-scbm
description: "Everything specific to the SCBM balance mod for Dominions 6, kept apart from vanilla: modded units, spells, items, numbers. Use whenever the game runs SCBM (the user's MP game), before quoting any number for it."
keywords: "sloop's, comfy, skills, whole, loaded, inspector, data, queryable, spell, change, table, spell-changes, spellchanges, school, level, filter, mage's, paths, changes, mean, play, cheaper, casting, lower, path, research, levels, cast, weights, make, buffs, script-only, multiplayer, tir, n'og, tirnanog, ghost, moose, troban, battles, dagda's, decisions, being, played, discussed"
---

# SCBM (Dominions 6 balance mod)

The user (2026-11-03): "You have to save all this to a separate SCBM folder." His multiplayer game runs SCBM, and
I had been quoting vanilla numbers for it (Destruction E3 - SCBM made it E2). Rules for keeping mod knowledge
apart: the generic **mod-docs** skill. Here: everything SCBM, nothing vanilla.

Mod files: `~/.dominions6/mods/SCBMv1.13/SCBMv1.13.dm` (installed; a copy is in the Dominions folder's
`SCBMv1.13/`). Never write into either.

## Order of truth for an SCBM game
the game screen > `SCBMv1.13.dm` (the block for that object: `#selectspell`, `#selectmonster`, `#newspell`)
> this folder's inspector data > the vanilla manual > videos > the wiki (all vanilla: check every number against SCBM)
> what the user says (test it in the game if he insists).

## Files
- `lists/` (2026-11-03): SCBM versions of dom6-best-by-purpose and the eight dom6-path-* pages, generated from the
  SCBM spell database (`dom6-spell-db/scripts/pathskills.py --label scbm`). The spell rankings are SCBM's; the wiki
  text (indirect magic, boosters) and the "Hand" tiers are VANILLA - check those against the .dm.
- `data/inspector/`: SCBM loaded into the mod inspector (dom6-modinspector `inspect_mod.py`, 2026-11-03).
  `report.txt` (counts, parser messages), `mod_pages.txt` (every new/changed object, vanilla diff and the mod
  lines), `pages/` + `records/` (the whole modded game). Query like vanilla:
  `../dom6-inspector/scripts/inspector.py --data data/inspector units "Ghost Moose"` (also spells, items,
  nations 11...). Counts: units 277 new / 3322 changed, spells 102 / 742, items 51 / 371, weapons 180 / 383,
  armour 56 / 124, sites 249 / 584, events 917 / 521, nations 104 changed.
  Inspector quirk: a range or area shown as "30+ [5/lvl]" is the value at the spell's own path level.
- `scripts/spellchanges.py`: `build` writes `spell-changes.md`; `paths E2N2G1H2 [--max-level N] [--school Alt]
  [--real]` lists the changed/new spells a mage with those paths can cast. Run bare = usage.
- `spell-changes.md`: all 844 touched spells, by school and level (generated - don't edit by hand).
- `spells.md`: the patterns and the changes that matter for Tir na n'Og (hand-written, the user's points in it).
- `tirnanog.md`: The user's MP game - decisions, Ghost Moose, Troban battles, Dagda's spell picks.
- Game records (map, provinces, battle GIFs) stay in the Dominions folder's `plans/tirnanog-scbm*`.

## A new SCBM version
1. `python3 -I ../dom6-modinspector/scripts/inspect_mod.py ~/.dominions6/mods/<new>/<new>.dm --out data/inspector`
   (move the old folder to `data/inspector-1.13` first if the game still runs the old version).
2. `python3 -I scripts/spellchanges.py build`, then re-check spells.md and tirnanog.md against the new table.
3. Write the version in this file. A game keeps the mod version it started with: record which game uses which.

## What not to put here
Vanilla rules (trample, formations, morale) stay in dom6-mechanics / dom6-tactics, even when learned in this
game; this folder links to them. A vanilla skill that names an SCBM number gets one line pointing here.

## Related skills
mod-docs (the generic rules), dom6-modinspector, dom6-inspector, dom6-tactics, dom6-spells, dom6-battle-view,
dom6-map, dom6-game.
