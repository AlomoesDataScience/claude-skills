# FoG II Medieval - every hotkey and command (READ FIRST)
Sources: manual ch. 8.1 (EBook p.76-77), 8.4 (p.80-87), 11 (p.95-127), 28 Useful Hot Keys; plus
what the game showed me [game]. Order of truth: game > manual > hypothesis.
**Checked against the game's own F1 "USEFUL HOTKEYS" list on 2026-11-02 (Force Selection screen) -
the game list wins.** F1 opens it any time (scroll it; close with its X button at (776,651)).

## Mouse (default Left/Right mode; Settings > Mouse Button Mode)
- Left click = select a unit (or deselect by clicking another unit / empty square).
- Right click on a target square = order (the icon for the order shows when hovering the square).
- Left-only mode: left selects AND orders; right click deselects.
- Hold left + drag = scroll. Hold right + drag = rotate, and tilt (pitch). Wheel = zoom.
- Ctrl + left click a unit = Detailed Unit Info (all its POAs vs each enemy type).
- Hold Ctrl while hovering a target = detailed tooltip (combat/shooting breakdown).
- [game] When a square allows several orders, big buttons appear: green triangle = Move Unit,
  blue triple triangle = Move Whole Command (about 60 px below), green curved arrow = Undo Move;
  left-click one.
- Force selection: left click a list entry adds the unit, right click removes; right click a bought
  (brown-highlighted) unit on the map with nothing selected removes it.

## Keys (manual 28 + 8.1 + 8.3 + 8.5.2)
| Key | Does |
|---|---|
| W / A / S / D | scroll up / left / down / right (held) |
| Up / Down arrow, wheel | zoom in / out |
| F / R | zoom out / in |
| Left / Right arrow, Q / E | rotate view (game list gives no direction; manual 8.1.3 Q anticlockwise, E clockwise, ch. 28 says E left - see by trying) |
| Shift + Up / Down | tilt (pitch) |
| G | toggle grid |
| H | toggle historical / distinct banners (game) |
| Tab | next unmoved unit |
| B | next unshot unit (with a target) |
| 1 | Line of Fire display (terrain only, not units) |
| 2 | Line of Sight display (terrain only) |
| 3 | command range of the selected general |
| C | combat log |
| K | casualties |
| L | unit list (moved greyed; "Can Shoot" yellow; "Melee Due" orange; click to select) |
| Space | shut popup windows, **proceed to next screen**, deselect unit (game) - NOT to close popups on setup screens: it may move on (e.g. Accept) |
| Esc | load / save / settings / exit menu (NOT a cancel) |
| **M** | **toggle top-down view** (game only - not in the manual; same as the minimap button) |
| **X** | **toggle map overview = shows/hides the MINIMAP** (game only; tried 2026-11-02 - useful to clear the bottom-right corner for photos) |
| F1 | full hot key list (the game's own) |
| F2 | screen dump, saved in Documents/My Games/FieldofGloryMedieval/SCREENS |
Keys can be rebound in Documents/My Games/FieldOfGloryMedieval/Options.txt (don't touch the user's).

## Screen buttons (8.4)
- Top left: score (% routed each side, difference green/red); the triangle under it opens the
  **Briefing panel** = victory conditions, notes, **Retreat** (concedes!), Load/Save, Settings.
- Top right: **End Turn** (turn number / limit) -> Confirm; clicking anywhere else cancels.
  **Never pressed by me - the user's call.**
- Right edge triangle: **Tools menu** = Next Unmoved, Next Unshot, LOF, LOS, Command Range, Detailed
  Unit Info, Combat Log, Casualties, Unit List, Briefing (my coordinates: fog2m-guide SKILL.md).
- Bottom: left card = selected unit, right card = hovered unit (AP, type, quality, armour,
  capabilities, cohesion).
- Bottom right: minimap with a button for top-down / isometric view.

## Commands (orders, ch. 11) - each shows its icon when hovering the target square
| Order | How / when | Key limits |
|---|---|---|
| Move | right-click a reachable square | AP: open 4 straight / 6 diagonal; ZOC stops passing; turn costs |
| Move Whole Command | blue triple-arrow option | only if no unit of the command within 5 squares of enemy; units already moved excluded |
| Pass Through | light foot moving through friends | only straight front-to-back; not through friends in combat |
| Turn | target square to the side | free within 45 deg; free 45 per turn if in range & manoeuvrable; else 4 / 8 / all AP |
| Turn Whole Command | | as above, units already moved excluded |
| Fall Back | 1-2 squares straight back keeping facing | cohesion test if in charge reach of non-light enemy; not heavy artillery |
| Form / Leave Square | units with >=25% pike, extra-deep offensive spear/heavy weapon | uses all AP |
| Undo | last single or group move/turn only | not after charge/shoot, revealing enemy, or a fall-back test |
| Add General | deployment, random-map battles, few generals | not artillery/baggage |
| Move General | once a turn to a unit of his command within 4 squares | not from combat/pursuit |
| Shoot | right-click target in arc/range | must be ordered; 5 good volleys; stationary best |
| Turn and Shoot | one order if AP allows | stays facing the target |
| Charge | Charge icon on target, click TWICE (1st shows Win:Draw:Lose) | AP to enter target square; within 45 deg; ZOC limits |
| Fight Melee | crossed swords on the tile | any time in my turn; unresolved fights resolve at End Turn |
| Switch Command | deployment only | general must move off first |
| Name Unit | campaigns, deployment | |
| Dismount / Remount | deployment only, (D) units | |
| Place / Remove Stakes | after deployment, units with stakes | uses all AP (free turn still allowed) |
| Deploy / Undeploy War Wagons, Disembark / Re-embark crew | war wagon armies | |
Deployment phase (ch. 10): drag/move/swap units in the highlighted area, set facings; then start.
[game, 2026-11-02] Placing a unit: left-click it, right-click the target square -> a button column
opens ON the target: **Deploy here** (triangle, on the square itself), Turn, Turn Whole Command (blue,
below). Left-click Deploy here (= clicking the target square again). Units of the side start facing
east (toward the enemy). Order of moves matters: clear a unit off a target square first. 14 units
placed this way with no misses (hover-check the last ones: tooltip gives unit + general + terrain).

## Map toggles tried in game (2026-11-02, Force Selection, Knights & Sergeants (0) selected)
All change nothing permanent; each is a toggle (press again to turn off).
- G grid: square lines over the map. L unit list: our units with men, AP, cohesion; clicking a row
  SELECTS the unit and centres the camera on it (used to pick units). K: "Losses" scroll - Enemy /
  Friendly original strength, killed / wounded / routing / artillery / elephants lost; tick to close.
- C combat log off/on. X minimap off/on. M top-down/isometric (resets zoom; top view = best for photos).
- R/F zoom, Q/E rotate, Shift+Up/Down pitch: all work in isometric view. After big camera moves the
  first photo can catch a transition (odd far-away view) - wait ~1.5 s and photograph again.
- 2 LOS: lights up every square the selected unit can see, the rest darkened (woods/hills cut it).
- 1 LOF: with knights (no missiles) only darkens the map - nothing to show. Try with shooters.
- 3 command range: no visible ring with Knights & Sergeants (0) selected - it shows for the selected
  GENERAL (manual 8.4.4.5); this unit apparently has none. Try with the general's unit.
- The east of the map is tinted darker beyond a N-S track: the enemy's side ("Enemy Front Line").
- bgplay `hold` now takes combos: `hold Shift_L+Up 700`.

## Turn passing (tested 2026-11-02, end of deployment)
End Turn (1485,70) -> a Confirm button drops below it at (1480,138); click it. Then the button is covered
by a crossed-swords **"Enemy Turn"** banner for ~5-8 s; then the button returns as "Turn N/24 End Turn".
The counter went 1 -> 2 across deployment + the AI's turn. The AI turn PANNED THE CAMERA (map ~395 px
east). Indicator: game-ui turnwait.py with ui/turn_mine.png (box 1385 30 1590 115, mask 1435 42 1540 92):
`turnwait.py wait ui/turn_mine.png --box 1385 30 1590 115 --mask 1435 42 1540 92 --min 8`.


## Moving units in battle (turn 2, 2026-11-02)
- Left-click the unit: white squares show where it can go. Hovering a square shows "Move Unit used/total AP"
  (Light Archers 8/12 for 2 squares; Light Javelin Horse has **20 AP**, 12/20 for 3 squares). Right-click = move.
- **The camera follows a moving unit** (it pans to keep it in view): re-measure the grid after EVERY move.
  Grid from the border: zoomed out in top view, inner west edge x, inner north (or south) edge y, square 59.25 px.
  The camera can pan past the map corners (black void beyond the stone border).
- Deselect: left-click an empty square. Park the mouse on the score banner (170,75) - see idle-view.
- **order.py** (fog2m-guide/scripts): one move order in map coordinates - pins the camera to a corner by a
  closed loop (pans vary run to run), measures the border, selects, OCR-checks the unit card name, hovers
  the target, then (--go) right-click + click the target = Move Unit; reads AP after. `where C R` = hover a
  square. Near the screen's bottom edge the buttons open sideways and the square becomes Move Whole
  Command - the script refuses squares below y 800.
- **X in battle hides the WHOLE UI** (banner, End Turn, unit card), not just the minimap.
