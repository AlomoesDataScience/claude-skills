---
name: dom6-magic-resistance
description: "Magic resistance and penetration in Dominions 6: the MR check, penetration, which spells check it, odds. Use when picking MR-checked spells, judging what lands on a monster or pretender, or protecting your own."
keywords: "manual, illwiki, drn, caster's, extra, levels, target's, level, spell's, path, caster, wins, ties, easy, hard, resist, negates, partial, secondary, effects, typical, values, human, elves, mages, pretenders, raises, overcasting, gems, primary, items, earth, bonus, table, spell, checks, shrink, torpor, holy, word, sleep, fascination, soul, slay, will"
---

# Magic resistance (Dominions 6, vanilla)

The user's list (2026-11-03). Manual p.76; illwiki `magic-resistance`.

## The check (p.76)
- Caster: **11 + DRN + (extra levels in the spell's path)/2** (rounded down) + penetration items.
- Target: **MR + DRN + (target's level in the spell's path)/2**.
- Caster wins ties. "Easy to resist" (MR easily): base 7 (manual: -4); "hard to resist": 15 (+4).
- Only for spells marked "Magic resistance negates" (inspector `mrnegates`); most damage spells use
  protection instead. Some only halve on a resist (Stellar Cascades, Shadow Bolt); secondary effects may need
  their own checks (wiki).
- Battle enchantments with lasting MR effects check every round on the same rules (p.76).

## Odds (penetration 11 vs MR), from dom6-drn "or tie"
| MR | 8 | 10 | 12 | 13 | 14 | 15 | 16 | 18 | 20 |
|---|---|---|---|---|---|---|---|---|---|
| lands % | 76 | 62 | 46 | 38 | 30 | 24 | 18 | 11 | 6 |
Each 2 extra caster levels = +1 penetration (~+7%). Gems give a level (dom6-gem-casting), so a gem on top of
one natural extra level adds a point.

## Typical MR (wiki)
Animals 5, average human 10, barbarians 9, magical humans 11, elves (Sidhe) 14, level-1 mages 13, 2-4 level
mages 15, 5+ 16, pretenders 18, Doom Horror 22. Our case: White Centaur 14 (SCBM inspector), Ghost Moose 18.

## Raising it
- Penetration: overcasting (levels above), items (+penetration), Astral/other boosts, communions (levels).
- MR: items (Amulet of Antimagic, Ring of... see dom6-items), Earth 4+ indirect magic +1 (p.75), spells
  (Antimagic, Resist Magic), pretender blesses.

## Using it
- Against MR 14+ (elves, centaurs, sacred elites, mages) single-target MR spells mostly fail at 11: prefer
  spells without MR (Earth Meld, armour damage, AoE damage) or pile casts.
- Against chaff (MR 5-10) MR spells are excellent (Sleep, Fascination, Confusion).
- Holy Word / Halt Heretic only hit sacreds and check MR: White Centaurs (MR 14) - about 30% per cast.
- Shrink on the Ghost Moose: no effect on spiritforms anyway (dom6-tactics); MR 18 = 11%.

## Related skills
dom6-drn, dom6-gem-casting, dom6-communions, dom6-magic-duel, dom6-spells, dom6-items, dom6-mechanics.
