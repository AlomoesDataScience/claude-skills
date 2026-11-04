---
name: dom6-stealth
description: Stealth, scouting, patrols and assassins in Dominions 6, from the manual (pp. 49-53, turn steps 20 and 33) - stealthy movement (Sneak is the default, ctrl-click to move normally, every unit with the commander must be stealthy), preaching spies (stealth bonus from population), discovery (patrol strength + 2d25 vs stealth strength + 2d25, both open-ended; stealth strength = leader's stealth - 1 per stealthy unit), patrol strength (precision + map move or 30 flying, / 20; commanders x2; undisciplined and mindless half; - unrest/2; + province defence - 14 at 15+), Patrol vs Defend vs Move and Patrol near forts, assassination (random target, bodyguards 50%, unprepared victim, location, townsfolk and guards, scale walls), seduction and other spy orders, scouting reports and their errors. Use when sending scouts or assassins, guarding against them, setting patrols to cut unrest or catch spies, or when the user asks about stealth, scouting or patrol.
---

# Stealth, scouting and patrol (Dominions 6, vanilla)

Plan item 19 (the user approved the extras 2026-11-03). Manual pp.49-53; turn order: assassinations at step 20,
sneak discovery at step 33 (p.55-56).

## Moving stealthily (pp.49-50)
- Stealthy units **Sneak** by default: they move as normal but don't fight on arrival. Ctrl-click = move
  normally (and attack). A stealthy commander sneaks only if every unit with him is stealthy.
- Hiding in an enemy province: later turns can attack it (Attack Current Province), or sneak-attack a
  neighbour.
- Stealthy priests can preach in enemy land; they get a stealth bonus from the province's population.
- Glamour units can't be seen at all in a friendly province.
- Scout reports can be wrong about numbers (the user: "30 reported, 80 there"); unit types are rarely hidden.

## Being found (pp.50-51)
- **Found if** patrol strength + 2d25 (open-ended) > stealth strength + 2d25 (open-ended).
- Stealth strength = leader's stealth - 1 per stealthy unit with him (-0.5 if the unit has stealth 50+).
- Patrol strength = sum of patrolling units' strength - unrest/2 (unrest capped at 100) + (province defence
  - 14, if defence >= 15).
- A unit's patrol strength = (precision + map move, or 30 if flying) / 20 + patrol bonus; **commanders x2**;
  undisciplined and mindless x0.5 (click a unit's precision to see it).
- Province defence 15+ searches every turn by itself (weaker than an army on Patrol).
- Found sneakers fight the whole defending force in the province (step 33).

## Patrol, Defend, Move and Patrol (pp.50-51)
- **Patrol**: lowers unrest (each point removed kills 10 population if there is unrest) and searches.
- **Defend** (default): fights non-stealthy arrivals; no search, no unrest cut. In a fort province,
  defenders get besieged; patrollers fight outside the fort.
- **Move and Patrol** (after a move order into a friendly fort province, or shift+ctrl+click): fight outside
  the fort on arrival; becomes Patrol next turn.

## Assassins and spies (pp.52-53)
- Assassinate: hits a random enemy commander in the province; the victim is unprepared (no scripts);
  location by buildings and victim (temple, tavern) with townsfolk or guards; assigned bodyguards each 50%
  to be there (Bodyguard ability raises it, the assassin's patience lowers it).
- Mounted victims are usually on foot; a dead victim's mount dies too.
- Walls: no assassination into or out of a besieged fort, unless Scale Walls, flying or teleporting.
- Seduction (opposite gender switches sides), lure, infiltration, instill uprising: other spy orders.

## Using it
- Scouts: one per front, parked where they see the enemy's moves; Retreat + far rear in battle (the user).
- Catch spies: a fast or flying commander on Patrol (x2) beats a crowd of slow infantry.
- Guard key mages: bodyguards, a fort under siege, or a province full of patrollers.

## Related skills
dom6-blood-hunting (patrollers for unrest), dom6-sieges, dom6-game (orders on screen), scouting (generic),
dom6-mechanics.
