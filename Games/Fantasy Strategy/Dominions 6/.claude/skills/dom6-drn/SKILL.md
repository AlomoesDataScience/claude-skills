---
name: dom6-drn
description: "The Dominions 6 dice roll (open-ended 2d6 DRN) with exact probability tables for opposed checks. Use when working out any odds in Dominions or reading a battle log's roll lines."
keywords: "modifiers, feed, check, chance, value, beats, another, difference, ties, reaches, expected, damage, minus, protection, wins, melee, hit, strict, penetration, repel, active, side, lower-case, list, rolls, attack, defence, morale, magic, resistance, missiles, awe, fear, afflictions, site, search, checking, comparing, drms"
---

# DRN - the Dominions dice (vanilla)

The user's list (2026-11-03: "DRMs"). Manual p.58 (dice), rules spread over pp.60-76. Tables computed exactly
(open-ended dice to 7 rerolls).
Method and tool for any game: dice-math (`dice.py table "2d6!d"` reproduces these tables).

## The roll
- **DRN** = two d6, each open-ended: a 6 counts 5 and that die rolls again (and again). Mean 8, minimum 2,
  no maximum. A lower-case **drn** is one open-ended die.
- Almost every check is **value + DRN vs value + DRN**: both sides roll. "A check against 12" = value + DRN vs
  12 + DRN.
- Battle logs print rolls as "base+DRN": "Damage roll 15+5 vs prot roll of 8+9" (dom6-battle-view).

## Chance that X + DRN beats Y + DRN (by X - Y)
| X-Y | -10 | -8 | -6 | -5 | -4 | -3 | -2 | -1 | 0 | +1 | +2 | +3 | +4 | +5 | +6 | +8 | +10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| strictly higher | 3 | 6 | 11 | 14 | 18 | 24 | 30 | 38 | 46 | 54 | 62 | 70 | 76 | 82 | 86 | 92 | 95 |
| higher or tie | 5 | 8 | 14 | 18 | 24 | 30 | 38 | 46 | 54 | 62 | 70 | 76 | 82 | 86 | 89 | 94 | 97 |
Ties are 8% at an even difference. Each point of difference near 0 is worth ~8%; past +-6 only ~2-3%.

## Who wins ties
- **Melee hit**: the attack must be GREATER than defence (p.60) - use "strictly".
- **Magic penetration**: the caster wins ties (p.76) - "or tie".
- **Repel**: the repeller wins ties (wiki).
- Damage vs protection: damage must exceed protection (equal = no damage).

## Chance DRN >= k
2:100 3:97 4:92 5:83 6:72 7:58 8:46 9:36 10:28 11:21 12:17 13:13 14:9 15:7 16:5 17:4 18:3 20:2 21:1 (%)

## Expected damage per landed hit (damage - protection, both + DRN)
| dmg-prot | -10 | -8 | -6 | -4 | -2 | 0 | +2 | +4 | +6 | +8 | +10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| expected HP | 0.13 | 0.24 | 0.43 | 0.75 | 1.3 | 2.1 | 3.3 | 4.8 | 6.4 | 8.2 | 10.1 |
| any damage % | 3 | 6 | 11 | 18 | 30 | 46 | 62 | 76 | 86 | 92 | 95 |
Open-ended dice mean even hopeless hits sometimes wound - why masses of weak attacks still kill big things.

## Rolls and their modifiers (pages)
- Melee attack: attack + DRN - fatigue/20 vs defence + DRN - fatigue/10 - harassment (+ parry for the shield
  test) (p.60, 62). Blur -2 attack on the attacker, Displacement more (spells).
- Damage: str (x1.25 two-handed) + weapon dmg + DRN vs protection + DRN (+ shield) (p.60); type modifiers
  (dom6-weapons); armour-defeating on protection DRN 2/3/4 (dom6-armor).
- Missile hit: DRN + square size points/2 (+2 magic weapon) vs DRN + 2 x parry - fatigue/20 (p.65).
- Morale: morale + DRN vs a difficulty + DRN (dom6-morale); repel: morale + DRN + size diff vs 10 + DRN +
  margin/2 (p.63).
- Penetration: 11 + DRN + extra levels/2 (+ items) vs MR + DRN + target's path/2; easy -4, hard +4 (p.76)
  (dom6-magic-resistance).
- Awe: attacker morale + DRN vs 10 + awe + DRN to attack at all (wiki awe).
- Dispel: +1 per extra gem, +5 per caster level above, + DRN each side (p.77).

## Using it
Quick odds: count the difference, read the row. Several independent chances multiply (hit 54% x damage
>0 62% = 33% of swings wound). For full fights use dom6-combat-math (spells.py simulates with these dice).

## Related skills
dom6-combat-math, dom6-ranged-math, dom6-weapons, dom6-armor, dom6-morale, dom6-magic-resistance,
dom6-mechanics.
