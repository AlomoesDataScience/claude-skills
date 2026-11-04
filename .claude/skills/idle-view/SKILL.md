---
name: idle-view
description: Where to leave a game's camera and mouse while Claude is idle (thinking, reading the manual, writing files, waiting for the user) so the screen looks natural to anyone watching or recording - camera resting on what's being thought about, mouse parked on a neutral spot that shows no tooltip or order icon and is far from commit buttons (End Turn, Accept, Retreat), no unit left selected unless it's the subject, overlays left in a sensible state, no sudden jumps. Per-game parking spots. Use when Claude is about to stop acting for more than a few seconds, after taking photos or calibration runs, before handing control back to the user, and during recordings or streams.
---

# Idle view - a natural screen while thinking

## HARD RULE: tools restore the human view (the user, 2026-11-02)
"I can't review turn 2, because you have the camera in the corner ... the skills for making sure camera
is centered and readable to a human are just being ignored or were improperly constructed. It's popping
the camera in the corner, and that's not usable to a human."
What went wrong: this skill was only a text rule, and my measuring tools (order.py) pinned the camera
to a map corner to read the grid and LEFT it there. A rule that depends on remembering gets skipped.
So:
1. **Every script that moves the camera for its own purposes (measuring, photos, calibration) ends by
   restoring the human view.** Build it into the script (a `present()` called on every exit path,
   errors included), never leave it to memory.
2. **The human view = centred on the action.** Both armies on screen (or my army plus whatever the
   turn is about), at a zoom where units are visible. Not a corner, not an edge, not the void past
   the border.
3. **Have a one-call way to get there**, made per game: minimap click, unit-list click, a centre key.
   Measure it once, and write its coordinates into the game's tools and this skill.
4. **Before handing a turn to the user, take one photo and check: could a human review this screen?**
   If not, fix the view first.

The user (2026-11-02): "create a skill to more naturally place the camera during idles." Between actions the
screen is still on show: to the user at the desk, on a recording, on a stream. A stray tooltip, a camera
pointed at empty ground, or the mouse resting on End Turn looks careless, and the last two are risky.

## Before going idle
1. **Camera on the subject.** Leave the view on what I'm thinking about: the area being deployed, the
   front where the next orders go, the unit being considered. After photo runs and calibration (which
   leave the camera at a map edge), bring it back to that place. A human player looks at the problem
   while thinking.
2. **Zoom for a human.** Close enough to see the units involved, wide enough to show their
   surroundings, and not the extreme zoom-out used for photos unless the whole map is the subject.
3. **Mouse parked on a neutral spot inside the game window** (a pointer outside the window leaves
   the last hover active). It should show no tooltip, no order or move icon, no hover
   highlight, and be far from commit buttons (End Turn, Accept, Create, Retreat). Off-map dark areas
   or an empty part of a side panel are good. The mouse must not rest on the map where a tooltip
   would pop up, or on a unit while another is selected (that shows order icons).
4. **Selection.** Leave one selected only if it's the subject (e.g. the unit about to be ordered).
   Otherwise deselect safely: click an empty spot. Not Space or Esc in games where those advance or
   open menus.
5. **Overlays.** Turn off what was only for photos (grid, LOS, minimap hidden, log hidden) unless it
   helps the viewer follow the thinking. Close popups and lists.
6. **No jumps.** Move the camera in one or two calm pans or a minimap click, then stop. Don't make
   repeated flicks while idle.

## Coming back from idle
Start with a fresh photo of the current view. The game or the user may have changed something. Then act.

## Per-game parking spots
- **FoG II Medieval (bgplay 1600×990, game 1600×900):**
  - Battle and deployment: **(1578, 448), the Tools triangle on the right edge.** It's fixed UI and
    shows only a tiny "Tools" label (tested turn 3, 2026-11-02). NOT the score banner (170,75): the
    map's terrain tooltip comes through it whenever woods etc. lie under it. NOT the eye button
    (it shows "Toggle Top View").
    NOT outside the game picture (y 950 or y 12): the game keeps the last hover position, and its
    tooltip stays up. NOT off-map black areas: the camera pans (the AI turn and moving units both move
    it), so the map can end up under the mouse.
  - Force Selection: the empty lower part of the Your Army panel, (300, 720).
  - Not (1590,960): it can show a terrain tooltip at the top right.
  - Camera: top view (M), fully zoomed out, **centred between the two armies by a minimap click**:
    `order.py present [--view C R]` (fog2m-guide/scripts). The minimap's map rectangle starts at
    (1379.3, 776.7) with 2.68 x 2.64 px per square, and a click centres the camera on that square
    (it lands at about screen 800,465). Battle 2 default: column 19, row 11.5, which shows both
    armies whole. Every order.py command ends with it.

## Related skills
map-camera (moving the camera), game-ui (bgplay), stream-panel and obs-record (recordings; the panel
never takes focus), photo-map (photo runs leave the camera at an edge - come back after).
