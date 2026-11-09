---
name: unit-combat-math
description: "Unit-versus-unit combat math for any game: hit chance, damage after armour, rounds to kill, both ways. Use when deciding whether a unit or champion wins a fight or choosing gear and buffs."
keywords: "chain, round, judge, matchup, kills, whom, faster, measure, buff, debuff, saves, costs, stat, number, gang, because, harassment-style, penalties, make, crowds, numbers, treat, armour-piercing, armour-negating, defence, regeneration, fatigue, different, tank, axes, counters, scale, armies, combat-models, unitcombat, exactly, attack, dice-math, simulated, over, whole, fights, rule, presets, dominions"
---

# Unit combat math (any game)

Generalized 2026-11-03 from the Dominions 6 set (dom6-combat-math, -ranged-math, -armor, -fatigue,
-supercombatants) at the user's request ("We're going to need to generalize all this stuff"). Dice: dice-math.
Army scale: combat-models.

## The chain (every game has some version)
1. **Hit chance** - opposed (attack + roll vs defence + roll) or target (roll + bonus vs a number). Note the
   tie rule and the penalties: fatigue, harassment, flanking, darkness.
2. **Damage per hit** - damage minus armour (subtractive, as in Dominions and many wargames) or damage
   dice with armour as a to-hit target (d20). Armour-piercing halves armour, armour-negating ignores it.
3. **Per round** = attacks x hit x damage. **Rounds to kill** = HP / per round - simulate it, because damage is
   lumpy: the mean is above HP / rate when big rare hits overshoot.
4. **Both ways**: a matchup is the two rounds-to-kill numbers side by side. The lower one wins.
5. **Then the extras**: regeneration per round, shields and parries, luck and damage reversal, morale (units
   usually break before they die), fatigue over time.

## What to do with it
- **Measure a buff in rounds, not points.** Dominions example: Barkskin (+7 natural protection) took Sidhe
  from dying in 10.1 rounds to 16.8 against White Centaurs - from losing to even (dom6-scbm tirnanog.md).
  A +4 that moves a difference from -2 to +2 is huge; past +6 it buys little (dice-math).
- **Gang up.** Where each attack lowers the defender's defence (Dominions harassment -1 per attack), N
  attackers kill more than N times faster: 4 weak attackers on one champion were 4.5x faster than one (2.9x
  without harassment). Concentrate attacks; spread damage wins nothing (battle-tactics).
- **Know the tank axes** and their counters (dom6-supercombatants has the Dominions versions):
  | Tank | Beats | Loses to |
  |---|---|---|
  | Armour (protection) | many weak hits | armour-piercing / negating, big hits, fatigue crits |
  | Defence (dodge) | few big hits | many attacks, swarms, area attacks, accuracy buffs |
  | HP + regeneration | chip damage | burst damage, other damage types |
  | Fatigue tricks (revive) | slow killers | fast killers, fatigue damage |
  | Resistances / MR | spells of that kind | the other damage types |
  Big hitters are bad against dodge tanks and good against armour tanks; swarms are the reverse.
- **Then scale up** with combat-models (Lanchester square law: numbers count twice as much as quality when
  everyone can fight at once).

## unitcombat.py
```
python3 -I scripts/unitcombat.py expect "att=10,def=10,dmg=13,prot=8,hp=10" "att=10,def=10,dmg=10,prot=15,hp=15"
python3 -I scripts/unitcombat.py duel A B [-n 20000]
python3 -I scripts/unitcombat.py buff A B "prot+7" [--on a|b]        rounds saved or lost
python3 -I scripts/unitcombat.py crowd A B --n 4 [--harass 1]
  --rules dom6 (default) | d20 [--dmgdice 1d8] | custom --hit 2d6 --hitties first --dmgroll 2d6 --protroll 0
```
Unit keys: att, def, dmg, prot, hp, attacks, ap, an, regen. Checked: the dom6 preset reproduces dom6-drn
(45.8% hit at even skill, 1.29 damage per hit at -2, 30% any damage).
For Dominions use the game's own simulator first (dom6-spells `spells.py melee`: real unit cards, shields,
damage types, buffs); this tool is for other games, quick what-ifs and designing our own combat.

## Related skills
dice-math, combat-models, battle-tactics, dom6-combat-math, dom6-supercombatants, dom6-thugs, fog2m-guide,
borrow-from-games (combat systems for our games).
