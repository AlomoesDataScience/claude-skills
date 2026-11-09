---
name: war-language
description: "Translate a game's situation up into military terms (METT-TC, SALUTE, mission, intent), reason there, and back down into orders. Use when a wargame turn starts, explaining a battle, or turning a plan into orders."
keywords: "higher-order, warfare, games, going, game, units, squares, points, morale, bars, turns, oakoc, enemy, most-likely, most-dangerous, courses, action, form, maneuver, task-and-purpose, unit, control, measures, level, concrete, square, many, check, after, per-game, lexicon, element, doctrine, term, guide, written, templates, warlang, prints, back-translation, checks, nothing, lost, either, built"
---

# War language - translate up, think, translate down

**The user (2026-11-02):** "you need a skill to translate what's going on into those terms and
detranslate it from that to gameplay, like a higher order language to explain what's going on in
the warfare."

Why: game screens speak in squares, points and bars; doctrine speaks in missions, effects and
risks. Thinking at the doctrine level finds the plan (fix here, envelop there, the reserve
watches the most dangerous threat); the game level makes it happen and keeps it honest (can that
unit really reach that square this turn?). Every turn goes **up, think, down, check**.

## The lexicon - one per game, in its guide
Before the first real battle of a game, write `LEXICON.md` in the game's guide folder (game
element -> doctrine term, and back). Fill it from the manual and from play; extend it when
something new appears (manual-first). Sections:
1. **Units -> roles**: each troop type -> its arm and its natural tasks (fix, screen, attack by
   fire, envelop, reserve...) and what it must never do.
2. **Map -> terrain terms**: each terrain type -> OAKOC effect (observation and fields of fire,
   avenues of approach, key terrain, obstacles, cover and concealment) and which arm it favours.
3. **Mechanics -> effects**: game rules -> doctrine effects (ZOC = fix/block, cohesion = morale and
   unit cohesion, evade = disengage/feigned retreat, command range = command and control,
   ammo = sustainment, turn limit = time).
4. **Victory -> end state**: the game's win conditions as end state and decisive conditions.
5. **Measures -> grid**: how phase lines, objectives, boundaries and engagement areas are written
   in this game's coordinates.
6. **Back-translation table**: doctrine task -> the game actions that carry it out, with the cost
   and what to check after (the "down" dictionary).
First lexicon: Field of Glory II Medieval (`fog2m-guide/LEXICON.md`, written turn 6 of battle 2).
Troops and Enemy in the UP step come from the **army-log** skill (armylog.py eval).

## UP - game state -> military picture
Write it in this order (warlang.py prints the template). Short lines; game coordinates in
brackets so it can be translated back.
1. **Mission** - our end state from the victory conditions, and the time we have.
2. **Enemy (SALUTE)** - size, activity, location, unit types, time seen, equipment; their
   apparent **type of operation** (area defence, mobile defence, attack, delay...); their **most
   likely course of action** and **most dangerous course of action**.
3. **Terrain (OAKOC)** - fields of fire, avenues of approach, key terrain, obstacles, cover and
   concealment; where each side's arms are favoured.
4. **Troops** - our strength and state (cohesion, ammo, commanders), relative combat power at
   the likely points of contact (combat-models if numbers help).
5. **Time** - turns left, how many turns each phase needs, culmination.
6. **Read-out in one line** - "They are in an area defence on the ridge; their reserve is the
   threat; we have 19 turns to break 40%."
Name what is *happening* in doctrine words: "they are fixing us", "our screen is being
counter-screened", "we are culminating", "this is a Fabian defence", "they've left an assailable
flank".

## THINK - at the doctrine level
- **Form of maneuver** and the **defeat mechanism** (military-doctrine, military-operations).
- **Commander's intent** - purpose, key tasks, end state, in three lines.
- **Main effort**, supporting efforts, **reserve** and its commit trigger, **security** (who
  screens/guards which flank).
- **Task and purpose for every unit** - "Spears 1: *fix* French Spears 5 (22,10) *so that* they
  cannot shift south".
- **Control measures** - phase lines, objective, limit of advance, in game coordinates and turns.
- **Risk** - what the most dangerous enemy COA does to this plan and the counter.
- **Engagement and disengagement criteria** for screens and shooters.

## DOWN - military plan -> game orders
For every task and purpose, use the lexicon's back-translation table:
1. **Unit** (by its in-game name) -> **action** (move, turn, shoot, charge, hold, evade...) ->
   **destination or target** (square / enemy unit) -> **cost** (points, ammo) -> **order of
   execution** (who goes first so lanes stay open).
2. **Feasibility check** at game level: reach, points, facing, zones of control, line of sight,
   range, terrain cost, command range, what the enemy can reach next turn (move-phases).
3. If a task can't be done in game terms, change the plan *up there* (task, phase line, timing) -
   don't quietly do something else down here.
4. Draw it (draw-moves) and execute one order at a time, checking the screen after each.

## CHECK - back-translate the result
After the orders (and after the enemy turn), translate the new game state up again and compare
with the plan: did each unit achieve its task's *purpose*, not just its move? Write one line per
deviation and why. The user reviews in doctrine terms *and* game terms - give both.

## Explaining to the user
Lead with the doctrine read-out (one or two lines), then the game facts that back it, then the
orders in game terms. Keep both levels visible; never let jargon hide a game fact (always say the
square, the unit, the number).

## warlang.py (scripts/)
```
python3 -I .claude/skills/war-language/scripts/warlang.py up       # situation template (METT-TC, SALUTE, OAKOC)
python3 -I .claude/skills/war-language/scripts/warlang.py think    # intent / maneuver / tasks template
python3 -I .claude/skills/war-language/scripts/warlang.py down     # order table template + feasibility checks
python3 -I .claude/skills/war-language/scripts/warlang.py lexicon  # LEXICON.md skeleton for a new game
python3 -I .../warlang.py all > plans/<battle>-turnN-warlang.md     # all three for one turn
```

## Sources
FM 3-90 (METT-TC(I) p.24, OAKOC p.93, most dangerous / most likely COA p.107, reserve sized to the
most dangerous threat p.120, five-paragraph order), FM 3-0, war-concepts glossary.

## Related skills
military-doctrine, military-operations, soviet-doctrine, war-concepts, combat-models (the
vocabulary); battle-tactics, move-phases, draw-moves, photo-map, planning (the game-level method);
screening, scouting; generalize-learning (lexicon entries that hold for many games go back here).
