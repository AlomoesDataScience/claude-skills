---
name: dom6-blood-hunting
description: "Blood hunting in Dominions 6: the three checks, unrest, hunter choice, patrols and income. Use when setting Blood Hunt orders, choosing hunters or provinces, or judging a blood nation's income."
keywords: "manual, turn, step, illwiki, blood-hunting, wigglefig's, magic, guide, level, population, failure, multiply, slaves, found, site, frequency, adjusts, loss, retaliation, assassinations, bodyguards, sanguine, dowsing, rod, thorn, picking, patrollers, patrol, strength, reduces-unrest, units, unskilled, bootstrapping, success-chance, calculator, hand, raiding, enemy's, grounds, planning, spells, dom6-blood"
---

# Blood hunting (Dominions 6, vanilla)

The user (2026-11-03): "blood hunting probably should be a separate skill". Split from dom6-blood.
Turn order: hunting resolves at step 18 (after site searches, before assassinations and movement) (p.55).

## The rules (manual p.51-52; wiki)
- Order "Blood Hunt" (B) in an owned land province. Three checks, all must pass:
  1. hunting level: 10 + 30 x (Blood level + blood searcher) %, 100% at level 3;
  2. population: population / 75 % (100% at 7500+);
  3. unrest: fails with unrest / 4 % (0 unrest = always passes).
  Example (wiki): level 2, 6750 people, unrest 40 = 70% x 90% x 90% = 57%.
- Slaves found: d6 + hunting level (+-0.5 per 5 site frequency from 50; EA 65 = +1.5).
- Cost: population -10 x floor((slaves + 4)/5); unrest +d(3 x slaves + 4) (failed hunt +d6-1). Several hunters
  in one province raise unrest in turn, so later ones fail more.
- Retaliation: assassination events on hunters; bodyguards help; strong friendly dominion makes them rarer.
- Items: Sanguine Dowsing Rod (+1 blood searcher), Blood Thorn (+1 blood). A B1 hunter with a rod = 70%.
- Patrollers: ~25 patrol strength per B3-equivalent hunter keeps unrest at 0 (wiki guide);
  "reduces unrest" units cut it before it hits income.


## Quick odds (unrest 0, population 7500+)
| hunting level | B1 | B1+rod | B2 | B2+rod / B3 | B3+ |
|---|---|---|---|---|---|
| success | 40% | 70% | 70% | 100% | 100% |
| slaves (avg, site freq 50) | 4.5 | 5.5 | 5.5 | 6.5 | 6.5+ |
Unrest 40 multiplies by 0.9; population 3750 by 0.5.

## Running it
- Best provinces: 7500+ people (a bit more, so the losses don't drop it below), 0 unrest, friendly dominion
  (fewer retaliations), not on the front line.
- One or two hunters per province; put patrollers in it (troops on Patrol: patrol strength from precision and
  map move - dom6-stealth) to wipe the unrest every turn.
- Bodyguards on hunters (retaliation events). Hunters don't research - count that cost.
- Unskilled commanders hunt at 10%: only worth it to bootstrap. B1 mages need a Sanguine Dowsing Rod.
- Slaves land in the province: move them to the lab (pool) or to the army that needs them.

## Against a blood nation
Their hunting provinces are their economy: raid them, raise unrest (pillage, Unrest spells), kill or
assassinate hunters, cut population (plague, Blood Feast backfires on them).

## Related skills
dom6-blood, dom6-economy, dom6-stealth (patrol), dom6-gem-casting, dom6-mechanics.
