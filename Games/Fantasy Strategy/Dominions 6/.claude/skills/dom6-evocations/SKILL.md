---
name: dom6-evocations
description: How damage spells (evocations and other battle damage magic) work in Dominions 6, from the manual (pp. 65-66, 75-76) and the dom6-spells model - casting time and interrupts, landing (caster + spell precision, deviation, precision 100), area (nearest N squares, both armies, rider and mount), the shield roll (blockable unless "ignores shields"), damage types (AP halves protection, AN ignores it, fire/cold/shock/poison resistances x2 %), MR-checked spells, secondary effects, clouds, overcasting (+damage, +area, +range per level), fatigue, friendly fire, and what to cast against what (shields, armour, MR, packed vs spread). Use when choosing or scripting damage spells, judging an enemy's evocation threat, placing troops against area spells, or when the user asks about evocations. Rankings: dom6-spells evocations.md and kill-spells.md.
---

# Evocations and damage spells (Dominions 6, vanilla)

The user's list (2026-11-03). Manual pp.65-66, 75-76; dom6-spells evocations.md (model and rankings, shield
correction). SCBM changes many (area, precision, gem costs) - dom6-scbm/spell-changes.md.

## Casting (p.75; wiki)
- Most combat spells: half a round to prepare, half to recover; Evocation is fast (typically 75%) (wiki).
- **Interrupt**: damage while preparing loses the spell with % of max HP lost + 25% (combat caster and
  mindless half) - mages behind the line, arrow protection.
- Fatigue: spell fatigue / (1 + extra levels) + casting encumbrance (dom6-fatigue); scales +-10% a point.

## Landing and area
- Lands like a missile: precision = caster + spell; deviation as missiles (dom6-ranged-math); precision 100
  never misses (p.76).
- Area N = the N squares nearest the landing point, everyone in them, **both sides**; mounted: rider and
  mount both hit. Many grow +1 area per extra level (inspector "3+1/lvl").
- Each target in the area rolls the missile hit roll: DRN + square size/2 vs DRN + 2 x shield parry -
  **shields block most projectile spells** (1/4 to 1/3 damage vs parry-4 troops) unless the spell ignores
  shields (Lightning Bolt, Soul Slay, Mind Burn, Smite...) (dom6-spells evocations.md).

## Damage (pp.65-66, 76)
- Damage + DRN vs protection + DRN; AP: protection halved; AN: ignored.
- Elemental damage also checks resistance: resistance subtracted and then damage cut by 2 x resistance %
  (fire res 50 = immune) (p.66).
- Some spells check MR instead of protection (dom6-magic-resistance); some have secondary effects
  (burning, stun, fear, poison) with their own checks.
- Clouds (poison, frost, Freezing Mist) linger and fade about a level a round.
- Damage often grows +N per extra path level ("13+2/lvl").

## Choosing what to cast
- Against shields and heavy armour: AN and shield-ignoring spells, or MR spells on low-MR troops; armour
  damage (Destruction) and then the army does the killing.
- Against unshielded packs (barbarians, archers, cavalry): big-area blockable spells are best.
- Against mages (thin line, MR 15): precision, shield-ignoring single-target spells, or assassins.
- Against monsters/thugs: high single damage, AN, MR-check spells if their MR is low (dom6-supercombatants).
- Friendly fire: keep your melee out of the target zone; area spells at the enemy rear, not at the melee.

## Related skills
dom6-spells (rankings, spells.py damage), dom6-ranged-math, dom6-magic-resistance, dom6-fatigue,
dom6-gem-casting, dom6-battlefield, dom6-scbm.
