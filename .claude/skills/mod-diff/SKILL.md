---
name: mod-diff
description: "Find what a mod or patch changed in any game and what got better or worse, by diffing exported tables. Use when a game runs a mod or new patch, or the user asks what changed."
keywords: "export, game's, before, after, vanilla, match, rows, sort, row, removed, mixed, ai-only, score, field, weights, lower-is-better, higher-is-better, fields, good, bad, flags, ignored, derived, columns, read, top, lists, filter, faction, check, big, ones, calculator, database, moddiff, csv, json, small, rules, file, summary, group, ranked, row's, changes"
---

# What a mod or patch changed (any game)

Generalized 2026-11-03 from dom6-mod-magic (the user: "skills to find out what magic is good/changes in a mod",
then "We're going to need to generalize all this stuff"). Mod documentation rules: mod-docs (one folder per
mod, vanilla stays vanilla). Order of truth in a modded game: game > mod files > vanilla sources.

## Method
1. **Two tables of the same thing**: export vanilla and modded data the same way (Dominions: the inspector
   with and without the mod; others: the game's CSV/XML/JSON, a modding tool's dump). Same columns, a stable
   id column.
2. **Rules file**: which fields are better lower (cost, fatigue, research level, gems), which higher (damage,
   area, range, HP), which flags are good or bad, which are AI-only (cast or build weights), which to ignore
   (derived columns). Encoded fields (ids, effect codes) stay unlisted: they land in "other" for reading.
3. `summary` (how much changed, by group) -> `diff --only better/worse/new` -> `row NAME` for anything odd.
4. **Filter to what you can use** (your faction's paths, tech, units) - a big buff to something you can't
   build doesn't matter.
5. **Check the top hits with numbers** (game-database built on the modded data, unit-combat-math, the game's
   own calculator). A field score is a pointer, not a verdict.
6. **AI-only changes** matter: if the mod makes the AI avoid something, you must order or script it yourself.
7. Write the findings into the mod's own folder with the mod version (mod-docs).

## moddiff.py
```
python3 -I scripts/moddiff.py summary OLD.csv NEW.csv --key id --rules RULES.json [--by school]
python3 -I scripts/moddiff.py diff OLD.csv NEW.csv --key id --rules RULES.json [--only better] [--top 40]
python3 -I scripts/moddiff.py row OLD.csv NEW.csv --key id --rules RULES.json NAME
```
Numbers are read from the start or end of a value ("30+", "5E", "Enchantment 4"); "6+ [2/lvl]" counts one
step of growth. Example rules: `examples/dom6-spells-rules.json`.

## Worked case: SCBM 1.13 vs vanilla Dominions 6 spells (2026-11-03)
On the spell database's CSVs: 845 of 1576 rows changed - 347 better, 23 worse, 13 mixed, 102 new, 360 other
(effect text, summoned unit ids). Destruction: better (+area per level, path E3 -> E2). The Dominions-specific
tool (dom6-mod-magic, modmagic.py on modinspector output) sees more fields (AI weights, MR flags): 421 better,
32 worse, 191 AI-only.

## Related skills
mod-docs, learn-to-mod, game-database, unit-combat-math, dom6-mod-magic, dom6-modinspector, dom6-scbm.
