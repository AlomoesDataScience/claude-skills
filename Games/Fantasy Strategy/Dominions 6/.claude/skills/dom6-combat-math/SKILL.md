---
name: dom6-combat-math
description: Melee combat math for Dominions 6 - turning unit cards into hit chances, damage per attack and rounds to kill, by hand (DRN tables, shield hits, damage types, harassment, fatigue, buffs and debuffs) and with the simulator (dom6-spells spells.py melee X Y with buffs like nat+10, blur, armor-5, att+N, ethereal, luck, twistfate, --data for a modded game such as SCBM), plus how to turn one-on-one numbers into a battle judgement (concentration, harassment piles, morale breaks before deaths, Lanchester via combat-models). Worked example - our Tuatha and Sidhe against Pangaea's White Centaurs in SCBM, with Barkskin, Stoneskin, Blur and armour damage. Use when judging a fight, choosing buffs or debuffs, picking troops for a matchup, checking whether a thug wins, or when the user asks "who wins" or for combat math. Missiles: dom6-ranged-math.
---

# Combat math - melee (Dominions 6)

The user (2026-11-03): "a combat math skill probably is good." Rules: dom6-weapons, dom6-armor, dom6-drn. Method for any game: unit-combat-math.
Mods change the numbers: run the tool with the mod's data (SCBM: `--data ../../dom6-scbm/data/inspector`).

## By hand (one attack)
1. **Hit chance**: (attack - fatigue/20) vs (defence - fatigue/10 - harassment): dom6-drn table "strictly".
   Shield: chance the attack also beats defence + parry = a clean hit; the rest of the hits are shield hits.
2. **Protection used**: body (90%) or head (10%) protection, + shield protection on a shield hit; pierce x0.85,
   AP x0.5, AN 0.
3. **Damage**: (str + weapon dmg) - protection -> dom6-drn expected-damage table; slash x1.25 after; blunt
   head x1.25 before; limb hits capped at half max HP.
4. **Per round**: attacks per round (weapons, multiple attacks, quickness) x hit x damage. Rounds to kill =
   HP / damage per round (plus luck, twist fate, mirror images, regeneration to subtract).

## With the simulator
`dom6-spells/scripts/spells.py melee "Unit A" "Unit B" [--x BUFFS] [--y BUFFS] [--data DIR]`
prints hit %, damage per attack and rounds to kill, both ways (20,000 simulated fights, real DRN).
BUFFS: att+N def+N str+N prec+N nat+N (Barkskin 7, Stoneskin 10, Ironskin 13) armor+N / armor-N (worn armour,
e.g. after armour damage), ap, ethereal, mistform, luck, twistfate, blur, displace, airshield, quick, slime,
slow, storm, fire8, poison5, magicweapon. Limits: only the first melee weapon (no hooves/bites, no charge
bonus, no repel, no harassment build-up) - real fights are a little worse for the side with extra attacks.

## Worked example: Tir na n'Og vs White Centaurs (SCBM 1.13, 2026-11-03)
| Fight (rounds to kill ONE) | ours kills theirs | theirs kills ours |
|---|---|---|
| Tuatha Warrior vs White Centaur | 7.8 | 18.0 |
| Tuatha + Stoneskin (nat+10) | 7.8 | **40.8** |
| Sidhe Warrior vs White Centaur | 16.6 | 10.1 |
| Sidhe + Barkskin (nat+7) | 16.6 | **16.8** |
| Sidhe vs centaur under Blur (the enemy's) | **26.9** | 10.1 |
| Sidhe vs centaur with armour -5 (Destruction-like, assumed) | **11.1** | 9.8 |
Read: the Tuatha already beat centaurs one-on-one; Stoneskin makes them nearly unkillable by lances.
Sidhe lose one-on-one; Barkskin evens it; the centaurs' own Blur is what made our Sidhe useless at Troban;
armour damage helps the Sidhe more than any buff. (Destruction's real effect on protection is not documented:
-5 is an assumption to check in a battle log.)

## From duels to battles
- Concentration: a target attacked by several units takes harassment (-1 defence per attack): the 3rd and
  4th attacker hit far more often (dom6-weapons). Envelopment works for this reason - both ways.
- Morale breaks first: squads rout long before they die (dom6-morale); damage that lands early and at once
  (missiles, AoE, charge) breaks more than the same damage spread out.
- Numbers: combat-models skill (Lanchester square law: half the numbers need four times the quality; combat.py).
- Fatigue: long melees raise defence penalties and armour-defeating hits (dom6-fatigue).

## Related skills
dom6-drn, dom6-weapons, dom6-armor, dom6-ranged-math, dom6-spells (spells.py), combat-models, dom6-tactics,
dom6-scbm.
