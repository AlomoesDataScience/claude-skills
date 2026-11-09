---
name: dice-math
description: "Exact dice odds for any game with dice.py: sums, keep-highest, exploding and open-ended dice, re-rolls, opposed rolls, chance to hit a target. Use when a game rolls dice and the odds matter."
keywords: "tabletop, computer, enumerates, outcome, simulation, 2d6, 1d20, lowest, 4d6, kh3, dominions-style, re-roll-once, rules, fog, quality, answers, questions, games, ask, distribution, roll, ties, difference, table, system, reach, expected, damage, after, armour, sides, chained, checks, must, pass, binomial, hits, tries, plus, method, find, game's, tie, rule, manual"
---

# Dice math (any game)

Generalized 2026-11-03 from the Dominions 6 set (dom6-drn, dom6-blood-hunting) at the user's request ("We're
going to need to generalize all this stuff"). Method for whole rules families: rules-skills.

## Method
1. **Find the dice in the manual**: how many, what size, open-ended or not, re-rolls, modifiers, and **who
   wins a tie** - it changes odds by up to ~8% near even (Dominions melee: attacker must be strictly higher;
   magic: the caster wins ties).
2. **Compute once, exactly** with dice.py; write the table into the game's skill with the page.
3. **Reason in differences**: in an opposed system only X - Y matters. Learn where the curve is steep (each
   point ~8% near 0 for 2d6) and where it flattens (past +-6: 2-3% a point) - that tells what a +1 buys.
4. **Long tails**: exploding dice mean hopeless rolls still sometimes succeed - masses of weak attempts beat a
   strong single target eventually (Dominions: swarms wound armoured monsters).
5. **Chains**: several checks in a row multiply (Dominions blood hunting 40% x 50% x 75% = 15%).
6. Then hand it to the combat side (unit-combat-math) for hit -> damage -> kill.

## dice.py
```
python3 -I scripts/dice.py dist "2d6!d"                     distribution, mean, P(>=k), P(<=k)
python3 -I scripts/dice.py vs "10+2d6!d" "12+2d6!d"          opposed roll: first higher / tie / second higher
python3 -I scripts/dice.py table "2d6!d" --from -10 --to 10 [--ties first]   opposed table by X - Y
python3 -I scripts/dice.py need "2d6r<=1" 6 [--under]       chance to reach a target
python3 -I scripts/dice.py damage "2d6!d"                   expected max(0, damage - armour), both rolled
python3 -I scripts/dice.py chain 40 50 75                   all checks pass
python3 -I scripts/dice.py binom 10 0.3 --atleast 3         k successes in n tries
```
Syntax: `NdM`, `+K`, `kh3`/`kl3`, `!` (explode, max counts full), `!d` (max counts max-1, rerolls - DRN),
`r<=N` / `r>=N` (re-roll once), `--depth` (explosion depth, default 7).

## Worked examples
- **Dominions 6** (dom6-drn): DRN = 2d6!d. By difference, strictly higher: -4 18%, -2 30%, 0 46%, +2 62%,
  +4 76%; ties 8.5% at 0. Damage - protection 0 -> 2.13 expected, +4 -> 4.75 (checked against dom6-drn).
- **Field of Glory II** (fog2m-guide): cohesion test 2d6 needing 6: average 72%, Superior (re-roll 1s) 85%,
  Elite (re-roll 1s and 2s) 91%, Untrained (re-roll 6s) 62%.
- d20 systems: 1d20+5 vs 1d20+3 = 57% / 4.5% tie / 38%.

## Related skills
unit-combat-math (hit, damage, kill chains), combat-models (army-scale Lanchester/salvo), rules-skills,
dom6-drn, fog2m-guide, battle-tactics, borrow-from-games (dice systems for our games).
