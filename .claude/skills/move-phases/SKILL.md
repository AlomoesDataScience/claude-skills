---
name: move-phases
description: Give a turn's movement in PHASES instead of all at once, with a problem check at the end of every phase and a mandatory extension pass before the turn is called done - phase 1 the main body (block advance, line kept together), phase 2 the extension pass (every unit's leftover moves or AP checked against its role - screens further out, flank guards placed, reserves held back on purpose), phase 3 the final check of the whole picture (gaps, blocked units, enemy reach next turn, nothing left unordered by accident). Each phase gets planned, drawn, executed one order at a time, verified (photo, AP read, hover) and then checked for problems before the next starts. The user's method, FoG II battle 2 (2026-11-02). Use when giving any turn's movement orders in a tactical or wargame, when a block advance is ordered, when units have different speeds, or before handing a turn to the user for review.
---

# Move in phases - and check before the turn is done

The user (2026-11-02, FoG II battle 2): after I advanced everything 2 squares and called it done, he asked
"Is that what you want them all to do? Some units do have more movement." Then: "Doing movement in
phases like this is actually a good idea and better, but you do need to make sure there's no problems
in each phase."

## Why phases
- Each phase has one purpose, so each order is intentional, not part of a long batch.
- Units of different speeds need different handling. A block advance moves everyone the same
  distance and leaves the fast units' extra moves unused.
- A check between phases catches problems while they're small and before later orders build on them.

## The phases (every turn)
**Phase 0, plan:** roles for every unit (battle-tactics), the drawn proposal (draw-moves), and the
move order. Units in front move before the units behind them. Screens move before what follows
them. Clear a target square before moving into it.

**Phase 1, main body:** the line or block moves as planned. One order at a time, each verified:
- the right unit was selected (name check);
- the target square says what was expected (terrain, move cost);
- after the move, the AP or moves left match the planned cost. If not, find out why (hidden
  rough, a diagonal, a turn). An unexplained number is a problem.
→ **Phase 1 check** (below).

**Phase 2, extension pass (MANDATORY):** go through EVERY unit and write down what it has left and
what its role wants:
| Unit | Left | Role | Extend? |
- **Screens and lights:** further out, to where they force a reaction but can't be caught next turn.
- **Flank guards:** onto the flank they guard.
- **Shooters:** into range or a better arc, or stay still if moving spoils their shooting.
- **Reserve/strike:** usually held back. Write "held, on purpose".
- **Main line:** usually nothing left, or kept together on purpose.
Draw the extensions, then execute and verify as in phase 1.
→ **Phase 2 check.**

**Phase 3, final check:** photograph the whole field and confirm that every unit is where the
plan says. Then answer: what can the enemy reach next turn (move plus charge), and which of mine are
inside that reach? Are any units unordered by accident? Is anyone blocked or in a gap? Then **restore the human view** (idle-view:
both armies centred) and hand over for review. Never press End Turn without the user's go.

## The problem check (end of every phase)
1. **Positions:** a fresh photo with the grid laid over it, every moved unit on its square. The
   camera may have followed a unit, so re-measure first.
2. **Costs:** every unit's leftover moves are what the plan expected. Find out about any surprise.
   Surprises record terrain the picture hides.
3. **Formation:** no gaps opened, no unit facing the wrong way, nobody blocking a unit still to move.
4. **Exposure:** nothing of mine ended inside enemy reach that wasn't meant to be.
5. **Near misses in the interface:** a wrong button, a stale coordinate, an overlay over a target.
   Fix the tool before the next phase, not after the next mistake.
6. Write any problem and its fix into the plan file and the game's skill.

## Per game
- **FoG II Medieval:** order.py (fog2m-guide/scripts) gives one checked order and reads AP after.
  Battle 2 turn 2:
  - Phase 1 moved the line, shooters, Kerns, knights and mounted crossbowmen 2 squares.
  - Phase 2 extended the light archers, the mounted crossbowmen (to the flank) and the light
    javelin horse (screen). The knights held on purpose.
  - Checks found hidden rough at (9,16) (2 extra AP), one unexplained 10-AP knight move, and buttons
    that open sideways near the screen's bottom edge.

## Related skills
battle-tactics (turn method and roles; step 5 points here), screening (what screens do with their
extra moves), draw-moves (draw each phase), scouting (enemy reach for the final check), planning.
