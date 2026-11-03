---
name: fog2m-scouting
description: Scouting in Field of Glory II Medieval, where units are generally only hidden in forests (the user) - the per-turn reading routine (photos, hover every enemy unit, count and classify, diff, knight threat ranges), forests that could hide units, invisible terrain by tooltip, LOS overlay, who probes, and when a look turn is worth it under the 24-turn limit. Use when starting every FoG II turn or deployment, when planning an advance, or when something might be in a wood.
---

# FoG II scouting - almost everything is visible

Generic method: the scouting skill. This file holds the FoG II facts.

## What hides
- **Units:** generally only in forests (the user, 2026-11-02). Open ground, fields and hills show
  everything. Battle 2: the whole French army was visible at turn 2.
- **Terrain the picture doesn't show** (PLAY.md): enclosures, medium and deep streams, dead ground,
  and rough slopes. Height also needs a tooltip ("Open ground (Hill). Height: 25/50/75/100"), and
  what looks like hill can be open ground (e.g. (12,16) in battle 2).

## Each turn's reading routine
1. Wait for my turn (turnwait.py), then photograph both strips (photo-map, panorama step 100).
2. Hover every enemy unit: the tooltip gives its name, number and general. Line the photo up with the
   panorama (edge match) to get exact squares.
3. Count and classify against mine (strike, line, shooters, lights, filler). Update the board
   (draw-map) and the plan file.
4. Diff against last turn: who moved and toward what.
5. **Threat ranges:** knights have 14 AP (3 squares straight). Mark everything of mine within move
   plus charge reach.
6. **Forests near either army:** could anything be there that matters? If so, probe with lights, or
   use LOS (key 2) from a unit to see which squares it can see.

## Tools
- Hover = terrain tooltip, plus the unit name if one is there. Ctrl+left-click = detailed unit info.
  Ctrl hover = combat breakdown.
- 2 = LOS of the selected unit. 1 = LOF (shooters). 3 = command range (selected general).
- L = our unit list. K = casualties. C = combat log.

## Who scouts
Light horse first (20 AP, e.g. Light Javelin Horse), then light foot (12 AP). Keep them outside
knight reach, or where they can evade. They double as the screen (screening skill).

## Is a look turn worth it?
Usually not: 24 turns, the AI wins on time-out, and foot move 2 squares a turn. Look only when a
forest near the enemy could hide something that changes the plan.

## Related skills
scouting, screening, fog2m-map, fog2m-guide (COMMANDS, PLAY), photo-map, battle-tactics.
