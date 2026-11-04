---
name: map-camera
description: How Claude drives a game's map camera so it can see everything it needs - find every camera control (in-game key list first, then manual), clear the screen of overlays, choose top-down vs angled view, zoom out for the whole board and in for detail, calibrate how far a held pan key moves the map (camcal.py) so photos overlap and moves land where intended, recentre by minimap or unit list, rotate/pitch to look behind woods and hills, and wait out camera transitions before photographing. Works with photo-map (panorama.py) and game-ui bgplay. Learned on Field of Glory II Medieval with the user, 2026-11-02. Use whenever a game has a movable map camera - before photographing the board, when something is hidden, off screen or covered, when photos don't stitch, or on a new game's first battle.
---

# Map camera - see everything you'd want to look at

The user (2026-11-02): "make a map camera skill to properly use the map camera so you can see everything
you'd want to look at." The camera is a tool to answer questions - where is the border, what is in
that square, who can see whom, what's behind that wood. Pick the view for the question.

**The goal is knowing where things are, not one stitched picture** (the user, 2026-11-02: "you don't
need to join all the map together, you just need to be able to know where something is"). Strips or
single photos are enough when each one's place is known (which border shows, the camera's offset,
landmarks). Stitch only when it's cheap; never spend a long time on joins.

## 1. Know the controls (once per game, write them into the guide's COMMANDS file)
- The game's own key list first (F1 / help / controls screen), then the manual's camera section
  (manual-first skill). Typical: pan (WASD/arrows/edge/drag), zoom (wheel/keys), rotate, pitch,
  top-down toggle, minimap click = jump, "centre on selected", overlay toggles.
- Try each one once and note: held or tapped? does a view switch reset zoom? limits?

## 2. Clear the screen
Hide every overlay that isn't needed for the question: logs, minimap, unit lists, tooltips (park
the mouse in a dead corner). Note what can't be hidden (FoG Force Selection: the Your Army panel)
and keep photos to the free area (the --band). Check the band against a photo: anything that
repeats at the same place in every photo is an overlay - shrink the band (FoG: the Force Selection
banner tip at y 190 -> band from y 200).

## 3. Choose the view
| Question | View |
|---|---|
| Whole board, terrain, who is where, distances | top-down, zoomed all the way out, panorama |
| One area / a unit's surroundings | top-down or angled, zoomed in, centred on it |
| Line of sight, what's behind woods/hills, heights | angled, rotate around it, lower pitch; plus the game's LOS overlay |
| Reading models / banners / facing | angled, zoomed in |
Top-down views pan as a plain shift (photos stitch). Angled views stretch with perspective - don't
stitch them, use them for looking.

## 4. Calibrate the pan (camcal.py) - then plan moves in pixels
`python3 -I scripts/camcal.py --keys w s a d --ms 120 [--band X0 Y0 X1 Y1]` holds each key, photographs
before/after, matches, prints px moved. Pans are NOT linear (an initial jump, then steady): measure 2-3
hold times. Choose the photo step so the map moves at most ~60% of the band height (overlap).
After any view switch or zoom change, re-calibrate - speed depends on zoom.

**Check that a key works by tapping AND holding, and calibrate at the height you work at** (Dominions replay,
2026-11-03): its camera keys did nothing when tapped (PageUp "x12" in the tool had never worked) and only
moved while held; pan speed was 103 px/100 ms low and ~40 at the top height, and not linear in hold time.
So: test tap vs hold once per game, re-measure the pan at the working height, and where speed varies, steer
by re-measuring after each move (move, look, correct) instead of summing hold times.

## 5. Move with intention
- **Show the location you want, don't steer by key presses (the user, 2026-11-02).** Put the spot on
  screen with a jump (minimap click, unit list, centre-on-unit key), then find the grid by matching
  the photo against an older one (map-measure resnap.py). Counted pan-key holds drift run to run
  (FoG II: x0 569-714 for the same holds) and pushed the camera into corners; keep them for photo strips.
- Jump: click the minimap at the spot, or select a unit (unit list) to centre on it.
- Pan: hold the key for the calibrated time for the distance wanted.
- After every move wait ~1.2-1.5 s before a photo - a camera mid-transition gives odd views
  (FoG: a tiny far-away map). If a photo looks wrong, wait and take it again before concluding.
- Know where you are: map borders, the minimap marker, a landmark.

## 5b. Idle and hand-over
When stopping to think, and ALWAYS at the end of any script that moved the camera: restore the
human view (idle-view hard rule). Measuring positions (corner pins, edge views) are never left on
screen. Have a one-call recentre per game (FoG II: minimap click, order.py present).

## 6. Hand-off
Next: map-measure (size, borders, square size) - early, before reading terrain.
Whole board -> photo-map (panorama.py with the calibrated --step; for a board wider than one
screen, do a strip per column, e.g. camera west then east). Specific squares -> photo + the game's
tooltip / LOS overlay.

## Per-game numbers
### Field of Glory II Medieval (1600x900 game in bgplay, 2026-11-02)
- Keys: WASD pan (held), R/F zoom, Q/E rotate, Shift+Up/Down pitch (bgplay `hold Shift_L+Up 700`),
  M top-down toggle (also the round button under the minimap, (1476,872)), X minimap, C log, G grid,
  L unit list (click row = select + centre), 2 LOS overlay. Switching M resets zoom - hold F 2500 after.
- Top-down, fully zoomed out: W/S/A/D 60 ms -> ~167 px, 120 ms -> ~255-285 px, 180 ms -> ~390 px.
  Photo step for the vertical strip: --step 100 (moves ~240-265 px of a 465 px band; matches 0.45-0.62).
  250-400 ms steps jumped 600-900 px and never stitched.
- Free band in Force Selection with log (C) and minimap (X) off: x 570-1595, y 200-665.
- Whole map at full zoom: 24 squares N-S (~60 px/square full-res), 32 E-W - wider than the free band:
  THREE vertical strips (west, middle, east). Space strips so neighbours overlap by >= 40% of the
  band width: ~200-250 ms of A/D between strips (450 ms = ~900 px left only ~125 px overlap and the
  east join failed at match 0.07; 450 ms west->middle joined at 0.25 only because the borders helped).
- Don't join strips side by side - note which strip shows which columns (borders, landmarks) instead.

## Related skills
photo-map (photographing), map-usage (what to look for), game-ui (bgplay keys), game-setup, manual-first (find the camera keys)
