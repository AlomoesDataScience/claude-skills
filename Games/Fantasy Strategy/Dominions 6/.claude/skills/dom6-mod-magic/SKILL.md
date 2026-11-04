---
name: dom6-mod-magic
description: Find out what a Dominions 6 mod does to magic and what became good - modmagic.py reads any dom6-modinspector output folder and sorts every touched spell into new / better / worse / mixed / AI-weight-only, scores the changes (path level, research level, gem cost, area, effects, damage, fatigue, precision, range, cast time, MR and shield flags), ranks what got better or worse (filtered by a mage's paths or a school), lists new spells, explains one spell's diff, and summarises by school and path; plus the method (load the mod, summary, filter by your nations' mage paths, check the top changes in the spell database and the calculator, write findings into the mod's own folder per mod-docs). Use when a game runs a mod (SCBM or any balance/magic mod), when the user asks what's good or changed in a mod, or before planning research and scripts in a modded game.
---

# What a mod does to magic (dom6-mod-magic)

The user (2026-11-03): "skills to find out what magic is good/changes in a mod". Generic over Dominions mods (any game: mod-diff); SCBM's own
findings stay in dom6-scbm (mod-docs rule: one folder per mod, vanilla stays vanilla).

## Steps
1. Load the mod: dom6-modinspector `inspect_mod.py <mod.dm> --out DATA` (SCBM's DATA already exists:
   `dom6-scbm/data/inspector`).
2. `python3 -I scripts/modmagic.py summary DATA` - how much changed, which schools and paths gained.
3. `modmagic.py better DATA --paths <your mages' paths>` and `worse`, `new` - per nation or per mage
   (e.g. Dagda E2N2G1H2). `--school Alt` narrows; `--top N`.
4. `modmagic.py spell DATA NAME` - one spell's field-by-field diff and how it was scored.
5. Check the top hits with numbers: the spell database (dom6-spell-db, `--data DATA`) and the calculator
   (`dom6-spells/scripts/spells.py melee/missile --data DATA`).
6. Write what matters into the mod's folder (`dom6-<mod>/spells.md`), with the mod version.

## Reading the scores
- Weights per changed field: path level 3, research 2, gem cost 2, area 2, effects 2, damage 2, fatigue 1,
  precision 1, range 1, cast time 1; MR-negates removed +2, ignores shields +2. Values are compared at the
  spell's own path level ("6+ [2/lvl]" at E2 = 10).
- "AI only" = only AI cast weights changed: the spell is the same, but the AI casts it more or less on its
  own. A spell the AI now avoids must be **scripted** to be used.
- "other" = changes the score can't judge (description, summoned unit, effect number): read them with `spell`.
- A score is a pointer, not a verdict: a +2 on a spell nobody casts matters less than +1 on a key buff.

## SCBM 1.13 example (2026-11-03)
844 spells touched: 421 better, 32 worse, 42 mixed, 102 new, 191 AI-only. For Dagda's paths (E2N2G1H2) the
top gains are the army precision buffs (Eagle-eyed Warriors N1 Alt 4, precision 100, 20+5/lvl squares),
Flying Shards, Destruction (E3 -> E2, area 6+2/lvl), Armor of Achilles (fatigue 40 -> 15, range 30).

## Related skills
mod-docs (the rule), dom6-modinspector (load a mod), dom6-scbm (SCBM's findings), dom6-spell-db (scores
for every spell), dom6-spells (calculator), dom6-research.
