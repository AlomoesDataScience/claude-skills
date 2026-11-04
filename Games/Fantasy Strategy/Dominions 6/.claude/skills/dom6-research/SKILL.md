---
name: dom6-research
description: Magic research in Dominions 6, from the manual (pp. 73-74, 80, turn step 2) and illwiki - the seven schools (Conjuration, Alteration, Evocation, Construction, Enchantment, Thaumaturgy, Blood), what a spell needs (school level + path levels + gems), research points per mage (5 + 2 x magic levels +- bonuses, Magic/Drain scales, dementia halves), non-mage researchers (philosophers, Divine Insight up to dominion strength), labs, legendary level 9, and how to plan research around what your mages can actually cast (dom6-spells castable). Use when setting research orders or the research queue, planning which school to push, judging research speed, or when the user asks about research.
---

# Research (Dominions 6, vanilla)

The user's list (2026-11-03). Manual pp.73-74, 80; turn order step 2 (p.55: research happens even if the mage
dies later that turn). SCBM lowers research levels on 85 spells - check dom6-scbm.

## The rules
- A spell needs: (a) its school researched to its level, (b) the mage's paths, (c) its gems (p.74).
- School level != path: Will o' the Wisp is Conjuration 5 but F1 (p.74) - plan by spells, not by schools.
- Seven schools: Conjuration (summons), Alteration (buffs, weather), Evocation (damage), Construction (items,
  constructs), Enchantment (lasting effects, globals), Thaumaturgy (sorcery, remote, scrying), Blood.
- Research order needs a friendly **lab** in the province (the books are there) (p.80).
- **RP per mage = 5 + 2 x (total magic levels)** +- research bonus, minimum 1 (p.80). Holy levels usually
  don't count (wiki). Dementia halves it. Magic scale +1 RP per mage per point (and +50 start RP), Drain -.
- Philosophers (Arcoscephale, Therodos): research without magic, helped by Sloth not Magic scales. Divine
  Insight units (Monks of Man...): a few RP, at most dominion-strength many per lab (p.80).
- Level 9 = legendary spells (all schools but Construction): pick one; the others can be researched later,
  one at a time and expensively (p.80). Construction 9 = artifacts.

## Planning
- List what your mages can cast at each level (`dom6-spells/scripts/spells.py castable --paths ...`), then
  research toward the spells you'll use: battle buffs (Alteration/Enchantment), your summons (Conjuration),
  boosters and key items (Construction 3/5/7), evocations only if your paths make them good.
- Research vs fighting/forging: every mage turn spent researching isn't spent casting, forging or hunting.
- Tir na n'Og (SCBM): research queue plan v4 is in the game's notes (dom6-spells, memory).

## Related skills
dom6-spells, dom6-forging, dom6-summoning, dom6-rituals, dom6-evocations, dom6-buffs, dom6-scbm, dom6-economy.
