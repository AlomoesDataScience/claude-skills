---
name: map-measure
description: "Get a game map's size and dimensions early so every square can be found in photos. Use when starting a new map, right after the first photos, or when squares don't line up."
keywords: "before, reading, terrain, planning, read, setup, screen, scenario, info, advanced, options, editor, manual, find, border, lines, borders, work, sits, photo, strip, check, rows, come, whole, grid, woods, units, g-grid, overlay, agrees, cut, labelled, hand, map-usage, draw-map, building, board, zoom, camera, changed"
---

# Map measure - size and dimensions first

The user (2026-11-02): "make this, get map size and dimensions, as a skill. You should probably do that
early on." Without the dimensions, "where is X" is just a pixel on a photo. With them, every square has
a number, and the photos, the board and the drawing all agree.

## When: early
Run it right after the first whole-map photos (photo-map) and before reading terrain. Run it again when
the zoom, view or map changes.

## Steps
1. **The size in squares, from the game.** Setup screens, advanced options, scenario info, the editor,
   then the manual. FoG II custom battle: Advanced Options Width x Height (24 x 32 = frontage 24
   squares, depth 32).
2. **Photos that show borders.** Top view, fully zoomed out (map-camera), in strips (photo-map). Each
   strip should show at least one border, so its position is known.
3. **Find the borders:** `borders.py IMG... [--sat 14] [--br 70 200] [--x X0 X1] [--y Y0 Y1]`.
   - The inner edge of a top or left border = the run's end + 1; of a bottom or right border = the
     run's start.
   - Tinted areas (an enemy zone) need a lower brightness floor (`--br 40 200`).
   - Keep UI out of the search with --x/--y.
4. **Square size** = (inner bottom − inner top) / rows, from a strip that shows both. Check the other
   axis gives the same value, and check the result is a whole number of rows (FoG: 1422/24 = 59.25 px;
   east strip 24.03 rows ✓).
5. **The transform for each photo:** where square (0,0)'s top-left corner would be (x0, y0).
   - From a border: a left border at x gives x0 = x; a right border gives x0 = x − cols × square.
   - Between strips that share a known border row: use the same y.
   - Strips with no border in view: pan offsets, or one landmark seen in two strips.
6. **Check it:**
   - Run `squares.py` and look. Woods, roads and units should sit inside squares, not across lines.
   - Compare with the game's grid overlay (FoG: G).
   - A unit's square from the photo should match its known position.
7. **Write it down** in the game's map skill (`<game>-map`, Layout and Camera sections): size, square
   px at that zoom, border look and detection settings, strip x0/y0.

## squares.py
`squares.py CONFIG.json` builds a labelled square grid from the strips, plus parts (2×2 by default)
with column and row numbers. These are what terrain gets read from.
```json
{"cols": 32, "rows": 24, "square": 59.25, "cell": 48, "parts": [2, 2], "out": "DIR",
 "strips": [{"file": "west.png", "x0": 229, "y0": 17, "cols": [0, 11]},
            {"file": "mid.png", "x0": -487, "y0": 274, "cols": [11, 24]},
            {"file": "east.png", "x0": -1432, "y0": 262, "cols": [24, 32]}]}
```
Then: read the parts, write the text board (map-usage), optionally draw it (draw-map) and compare
the drawing side by side with squares.png.

## resnap.py - find the grid on ANY later screenshot (the user, 2026-11-02)
"Create a tool to automatically resnap the grid based on an older picture, so you know where the grid
is at. It should also support zooming in and zooming out." Runs on Claude's side only (photos in,
numbers out). Once per map: `resnap.py build REF.png --sq S --cols C --rows R --margin 400 --strip
STRIP.png MAPX0 MAPY0 ...` pastes the measured photo strips into one reference (in map pixels, with
the border kept around it). Then for every screenshot: `resnap.py find REF.png SHOT.png [--zoom 0.9 3]`
-> `sq S x0 X y0 Y match M` = square size on screen and where map corner (0,0) is. No border needs to
be visible; units that moved since the reference only lower the score.
- Method that works: smoothed BRIGHTNESS (woods dark, tracks light), masked normalised correlation
  over the WHOLE map area with the fixed UI masked out (--ui boxes). Edge maps failed (0.11 on a right
  answer; picked a wrong zoom); a small band failed when a selected unit drew square outlines over it.
- Trust: right answers score 0.7-0.9 (selected unit ~0.7); under 0.5 look at the picture.
- Check once per map by drawing the snapped grid over a zoomed-in shot (field hedges on grid lines).
- OpenCV matchTemplate (masked) when installed: zoom search ~5.5 s, known zoom ~1.4 s; numpy FFT fallback ~13 s. FoG II reference: ui/map_ref_battle2.png (+ .json).

## FoG II numbers (battle 2, 2026-11-02)
- 32 columns (west to east) × 24 rows (north to south).
- Top view, fully zoomed out: 59.25 px per square at full resolution.
- Border = grey stone: `--sat 14 --br 70 200`; on the tinted enemy side `--br 40 200`.
- Strips, with the camera homed north: west x0 229 / y0 17; middle x0 −487 / y0 274; east
  x0 −1432 / y0 262.

## resnap zoom range (Dominions, 2026-11-03)
`find --zoom A B` searches scales A..B relative to the reference; a view outside the range fails quietly with a
low match (0.25 at a closer zoom than 1.3-3.5). Search wide (1.2-6) once, then narrow to +-4% around the found
scale; under 0.5 = re-search wide before trusting anything.

## Related skills
photo-map (the photos), map-camera (views, zoom, strips), map-usage (step 1 "establish the map" uses
this), draw-map (draw the board, compare against squares.png), per-game map skills (fog2m-map).
