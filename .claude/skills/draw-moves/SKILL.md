---
name: draw-moves
description: "Draw a movement plan on a game board, all turns in one picture or one per turn, from a plan file with turnplan.py. Use when proposing or reviewing moves for a turn or a multi-turn manoeuvre."
keywords: "proposals, step, method, either, turn's, arrows, coloured, numbered, units, final, squares, outlines, started, short, start, positions, map, coordinates, top, draw-map's, drawmap, planning, advance, deployment, over, several, showing, review, checking, plan's, geometry, reach, gaps, flanks, terrain, before, giving, orders"
---

# Draw moves - movement plans as pictures

The user (2026-11-02): the turn method is "picture of the battlefield → roles → **draw your movement
proposals** → check they can work → assess". Then: "you can do it on one picture... make a skill for
both doing it in one picture, and doing it in multiple turns."

## Which mode
- **One picture** (`--mode one`): the whole plan at a glance, with every turn's arrows coloured and
  labelled T1, T2, ... and units at their final squares. Best for a short plan, for review, and for
  comparing options side by side.
- **Turn by turn** (`--mode turns`): one picture per turn, showing positions after that turn and only
  that turn's arrows. Best when moves cross or stack up, for long plans, and for checking each turn's
  AP and ZOC.
- **Both** (default): when in doubt. Show the user the one picture first.

## How
1. Have a board for the map (draw-map board file, made from photos with map-measure / map-usage).
2. Write PLAN.txt next to the battle plan (plans/):
   ```
   board: setup.txt            terrain grid source (draw-map board file)
   view: 0 21 5 18             map cols 0-21, rows 5-18 shown
   units:                      ID COLOUR COL ROW [FACING]   (map coords, start of the plan)
   S1 royalblue 9 10
   turn ADVANCE: line +2 east  each turn: ID COL ROW = destination
   S1 11 10
   marks:                      COL ROW text
   20 5 enemy front
   ```
3. `python3 -I scripts/turnplan.py PLAN.txt [--mode one|turns|both] [--cell 34]` writes
   `PLAN_one.png` and/or `PLAN_t1.png`, `PLAN_t2.png`, ...
4. Look at every picture and check each arrow against the rules before showing it:
   - AP per square, diagonals and turning costs;
   - terrain on the path (rough, woods, marsh);
   - ZOC stops, and enemy reach (charge range, missile range);
   - command range.
   An arrow that can't be done in the game is wrong, so fix it.
5. Plans for future turns are proposals. Redraw each real turn from fresh photos.

## Notes
- Map coordinates are used throughout. A `view` crop keeps the real map numbers on the axes
  (drawmap --origin), so picture labels = map squares (fixed 2026-11-02 after cropped pictures
  were numbered from 0).
- Arrows are drawn on top and stop short of the unit box; a thin outline marks where the move began.
  The colours cycle per turn: red, orange, green, purple, blue, ...
- An arrow is a start-to-end summary of the move, not its path. For a path that matters (around
  rough, through a gap), split it into two turns or add a mark.

## Example
FoG II battle 2 generic advance: `Games/.../Field of Glory II Medieval/plans/battle2-boards/advance_plan.txt`
(4 turns: look, advance as a block, north half on / south half halts behind the rough, stand-off).

## Related skills
move-phases (draw each phase: main body, extensions), draw-map (the board and drawmap.py), battle-tactics (turn method), map-usage, map-measure, photo-map,
planning (plans live next to the plan file).
