---
name: dom6-ranged-math
description: Precision and ranged combat math for Dominions 6, from the manual and illwiki - where a missile lands (deviation = range x 1.25 / precision past precision/2 - 2; precision above 10 counts double), who in the square is hit, the hit roll (square size points and shield parry, no defence skill), missile damage, spell precision (caster + spell; 100 never misses), multi-bolt and AoE spells, interrupts, precision modifiers (Eagle Eyes, Trueshot, darkness, twilight, storms), arrow protection, deviation tables and the spells.py missile simulator (--data for SCBM), with a worked example of slingers and javelins vs White Centaurs. Use when judging archers, javelins, slingers or damage spells, placing missile troops, choosing precision buffs or arrow protection, or when the user asks about precision or ranged math.
---

# Precision and ranged combat math (Dominions 6, vanilla)

The user's list (2026-11-03: "precision", "Ranged combat math is also decent"). Manual pages in brackets;
illwiki `precision`, `evocation`. Mods change numbers (SCBM raised precision on 144 spells - dom6-scbm).

## Where the missile lands (p.65)
- Missiles don't use the target's defence skill. If range > precision/2 - 2 the shot deviates by
  range x 1.25 / effective precision squares (bell curve, long/short/left/right).
- **Effective precision**: above 10, each point counts double (12 -> 14, 14 -> 18, 17 -> 24).
- The landing square is hit even if it's far from the target: misses fall on whoever stands there, friend or foe.

Deviation in squares (precision down, range across):
| prec | 5 | 10 | 15 | 20 | 30 | 40 |
|---|---|---|---|---|---|---|
| 8 | 0.8 | 1.6 | 2.3 | 3.1 | 4.7 | 6.2 |
| 10 | 0.6 | 1.2 | 1.9 | 2.5 | 3.8 | 5.0 |
| 12 | 0.4 | 0.9 | 1.3 | 1.8 | 2.7 | 3.6 |
| 14 | 0 | 0.7 | 1.0 | 1.4 | 2.1 | 2.8 |
| 17 | 0 | 0.5 | 0.8 | 1.0 | 1.6 | 2.1 |
| 20 | 0 | 0.4 | 0.6 | 0.8 | 1.2 | 1.7 |
Close range is accurate; long volleys scatter over a block - fine against packed squads, bad near friends.

## Who is hit, and the hit roll (p.65; wiki)
- Target in the square: random, weighted by size (giant 6 + human 3: the giant 2 times in 3). Mounted: rider or
  mount 50/50 (dom6-mounts).
- Attacker DRN + (size points in the square)/2 (+2 magic weapon) vs defender DRN + 2 x shield parry -
  fatigue/20. Full squares (10 size points) get +5: packed infantry is easy to hit; shields matter a lot.
- Damage as melee (dom6-armor); most missiles add half strength; crossbows AP; fire AP; lightning AN.

## Spells (p.76)
- Spell lands like a missile with precision = caster precision + spell precision (spell card "Precision").
  **Precision 100** = it never misses (SCBM gives most buffs 100).
- Multi-projectile spells (Fire Flies 6+, Fire Darts 4+3/level) roll each bolt; AoE spells hit every unit in the
  area squares (both rider and mount) and use average protection (wiki).
- Interrupts: a damaged caster loses the spell with chance = % of max HP lost + 25% (combat casters and mindless
  half) (p.75).

## Modifiers (wiki precision)
+4 Gift of Eagle Eyes / Eagle-eyed Warriors / Trueshot (SCBM also +50% range), +2 Wind Guide (also halves
precision penalties), Air bless. Darkness -3 (spell Darkness -6), Twilight -2 (True Sight ignores), blind -9,
lost eye -3; Darkvision cuts darkness penalties (50/100%), spirit sight 100%. Storms: precision halved and
half the missiles lost (spells.py "storm").

## Arrow protection
Shields (2 x parry on the roll), Air Shield 80% (Protective Winds group, Lesser Arrow Ward SCBM), Arrow Ward,
Mist (battlefield). Blur doesn't affect missiles' square roll (it lowers ATTACK skill).

## Simulator
`dom6-spells/scripts/spells.py missile "Shooter" "Target" [--range R] [--x BUFFS] [--y BUFFS] [--data DIR]`
-> damage and one-shot kills per 100 shots into a packed 8x4 block of targets (range defaults to the weapon's).
BUFFS as in dom6-combat-math (prec+4, storm, airshield, fire8, poison5, magicweapon...).

## Worked example (SCBM 1.13, vs packed White Centaurs, per 100 shots, 2026-11-03)
| Shooter | plain | + Gift of Eagle Eyes (prec+4) |
|---|---|---|
| Fir Bolg Slinger (range 30, prec 10, dev 3.75) | 94 dmg (4.1 centaurs' HP) | 122 (5.3), +30% |
| Sidhe Warrior javelin (range 12, prec 10, dev 1.5) | 230 dmg (10.0) | 255 (11.1), +11% |
Precision buffs pay most for long-range shooters; javelins at close range barely miss already. Damage per hit
is the real limit against centaurs (shields 2x parry + protection 9): armour damage (Destruction) first.

## Related skills
dom6-drn, dom6-combat-math, dom6-armor, dom6-weapons, dom6-evocations (when built), dom6-spells, dom6-scbm.
