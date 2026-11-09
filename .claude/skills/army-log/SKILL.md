---
name: army-log
description: "Read and log both armies every wargame turn (one CSV per side), then evaluate losses, cohesion, combat power and force ratios with armylog.py. Use at the start of a battle turn, after the enemy's turn, and when reporting."
keywords: "unit, off, screen, cards, hovers, banners, never, game, data, write, type, quality, armour, points, men, action, ammo, square, facing, role, task, commanders, store, states, rout, progress, against, game's, victory, rules, units, still, break, left, sector, decisive, point, unread, flagged, diff, turns, moves, changes, feeds, war-language's"
---

# Army log - evaluate and log each army, every turn

**The user (2026-11-02):** "create a skill to evaluate and log each army."

## When
- Start of every turn after the photo (photo-map): log the enemy as found, and ours.
- After our orders (positions, AP left, tasks) - the turn's record.
- After combat or the enemy's turn - diff against the last snapshot: what did it cost, who wavered.
- In the report to the user: one evaluation block (doctrine read-out from war-language + these numbers).

## How
1. **Read, don't assume.** Every unit's card (strength, cohesion, AP, ammo, quality, armour, type,
   capabilities) and the hover tooltip (commander, terrain, height) from the screen. Units not read
   this turn get `Steady?` and blank men - the log flags them as unread instead of inventing numbers.
   FoG II: `order.py cards C R [C R ...]` hovers and OCRs (ours: card bottom-middle; theirs:
   bottom-right; the cursor tooltip names the unit's general and the terrain).
2. **CSV per side per turn** (`plans/<battle>-boards/armies/tN_<side>.csv`):
   `id,name,type,quality,armour,pts,str,max,cohesion,ap,ammo,col,row,facing,role,task[,weight]`.
   Roles and tasks in doctrine words (war-language); enemy roles are our read of them.
   `weight` = the unit's share in the game's rout count (blank = 1) - set it once the game's
   weighting is known (FoG II: "size-weighted" - check against the banner % when routs happen).
3. **Log**:
```
A=.claude/skills/army-log/scripts/armylog.py
python3 -I $A new plans/<battle>-armies.json --sides "Us,Them" --turns 24 --sectors "N:0-10,C:11-13,S:14-99" \
        [--states "Steady,Disrupted,Fragmented,Broken,Routed"] [--routed "Broken,Routed"] [--break 60 --edge 40 --margin 25]
python3 -I $A snap LOG TURN SIDE file.csv [--banner PCT] [--note "..."]
python3 -I $A eval LOG [TURN]      # the evaluation
python3 -I $A show LOG [TURN]      # both tables
python3 -I $A diff LOG T1 T2       # what changed
python3 -I $A turns LOG            # history
```
   Victory defaults are FoG II's (manual ch. 18 p.158-159: break at 60% of original troops routed or
   dispersed, or 40-59% if the enemy has lost "at least 25% less" - read here as percentage points,
   which the banner's rout-% difference suggests; unverified). "The size of units is taken into
   account" - exact weights unknown: at the first rout, compare `eval` with the banner and set
   `weight`. Set each game's own rules in `new`.

## Reading the evaluation
- **Combat power = points x men left / full** - points are the game's own value of a unit, so
  peasants don't outweigh knights the way a headcount does. Compare by **sector** for the force
  ratio at the decisive point (aim 3:1 there - soviet-doctrine; combat-models for the maths).
- **Rout progress**: how much rout weight is still needed to break them, and how close we are -
  e.g. "need ~4.8 more units" turns the objective into a target list.
- **Shaken units** (not the top cohesion state, not routed) are the targets - and on our side, the
  units to pull back or rally.
- **Ammo**: shooters with little left shoot only at shared targets.
- **Unread units**: read them next turn, or say plainly that they were not checked.

## Example (FoG II battle 2, turn 6)
English 14 units 594 pts, French 12 units 586 pts, all Steady, no losses. Combat power by sector:
north 138 v 184, centre 132 v 292, **south 324 v 110 (about 3:1 where we envelop)**; the French
reserve knights (222 pts, rows 10-12) are the force that can change the south - watch them.
French sub-generals: Knights 3, Crossbowmen 7, Knights 1 (decapitation targets); our C-in-C rides
with Knights 3.

## Related skills
war-language (UP: Troops and Enemy come from here), battle-tactics, move-phases (final check),
combat-models (turn the numbers into fight estimates), photo-map, planning (the log lives next to
the battle plan), generalize-learning.
