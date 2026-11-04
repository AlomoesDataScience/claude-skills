---
name: photo-map
description: How Claude finds out what is going on in ANY game with a map or board - identify the screen elements first (what is UI, what is map, where the map borders are), zoom all the way out, photograph the whole map in overlapping steps (north to south, west to east), stitch the photos into one picture (panorama.py) and build the map from the photos - terrain, who is where, both sides - before deciding anything. The user's rule (2026-11-02, FoG II battle 1) - "This is ALWAYS how you check what's going on. No relying on auto commands or tabbing through units." Use when starting every turn or phase of a tactical, wargame, strategy or board game, whenever the situation may have changed (enemy turn, combat), before planning moves, or when asked where things are.
---

# Photo map - always look at the whole board before acting

**Rule (the user):** play with gusto and intention - "I don't care if you're wrong. DO NOT phone it in." the situation is read from photos of the map, every turn. Not from tooltips,
not by cycling units (Tab / Next Unit), not from auto-scripts. Scripts only take and stitch the
photos; Claude looks at them and decides.

**The goal is knowing where things are, not one stitched picture** (the user, 2026-11-02: "you don't
need to join all the map together, you just need to be able to know where something is"). Strips or
single photos are enough when each one's place is known (which border shows, the camera's offset,
landmarks). Stitch only when it's cheap; never spend a long time on joins.

## 0. Use what's already worked out (the user, 2026-11-02: "You already figured that out yesterday!")
When a map needs looking at, this skill IS the method - load it and follow it; don't re-derive it
from the manual or from scratch. Same for every task: check the skills (skills-manager route, the
game's guide) before working something out again.

## 1. Identify the screen elements first - ALWAYS
Before any photo is used, know what each part of the screen is (game-setup skill, part 2):
- **UI overlays** that stay put while the map moves (banners, turn/end-turn button, minimap,
  icon columns, unit card, tooltips). Note their pixel boxes - they must be left out of the
  matching band and never mistaken for map.
- **The map area** and its **borders** (FoG II: a grey stone strip; others: black void, frame).
  Find where the borders are in each photo - that's what lines north/middle/south up and gives
  the grid its origin.
- **Grid size** at this zoom (measure a selected unit's square or a highlighted square edge to
  edge; don't assume).
- **Side colours / markers** (FoG II: blue banners ours, green Irish; minimap red ours, blue enemy).
- The **danger buttons** (End Turn!) - never in a photo sequence.

## 2. Take the photos
- Zoom all the way out (FoG II: hold F). Top view if the game has one.
- **Camera first: map-camera skill** (calibrate the pan with camcal.py; FoG top view = --step 100).
- `scripts/panorama.py` (bgplay screen): holds the back key to reach one end, then steps with the
  forward key and photographs until the picture stops changing.
  `--axis v` north->south (W/S), `--axis h` west->east (A/D); `--band X0 Y0 X1 Y1` = a strip with no
  UI overlays (FoG II battle default 0 250 1490 725; Force Selection 570 200 1595 665); `--step` ms per pan.
- **Each pan must move the map LESS than the band height** so neighbours overlap; check the
  printed shift and match score - match below ~0.25 means the pair didn't line up (step too big,
  or too little detail): retake with a smaller --step. Big pans (900 ms in FoG II) jump too far.
- `--shots A.png B.png ...` stitches existing photos.

## 3. Build the map from the photos
- **First measure it (map-measure):** size, borders, square size, then squares.py to read square by square.
- Open panorama.png. Mark the borders, then the grid from the border (row 0 = first row inside).
- Name the terrain by eye: open, fields/farms, woods, marsh, rough, hills (contour lines), roads,
  fences/enclosures, rivers, villages.
- Put every unit on it: side, type (silhouette, banner), facing. Count both armies.
- Write it as a short text board (rows x columns, letters) when planning geometry - optionally draw it (draw-map: drawmap.py) when that is easier to read than the game map: lanes, reach,
  who can hit whom next turn, flanks.
- Only then plan, and after each order take a photo of that area to check it.

## Status
- panorama.py written 2026-11-02; edge-matching works when photos overlap (FoG II test: 372 px
  pan matched 0.37). The north->middle pair from a 900 ms pan did NOT overlap (match 0.07) -
  fixed 2026-11-02: FoG top view needs --step 100 (calibrated with map-camera camcal.py) - 7 photos N->S all matched 0.45-0.62. Horizontal panning untested.
- FoG II specifics (2026-11-02): top view = round button under the minimap, tooltip "Toggle Top
  View", (1476,872) full coords, or key M; X hides/shows the minimap; switching view RESETS the zoom - hold F again after it. Map labels
  such as "Enemy Front Line" (red) mark the deployment zones and can show through the see-through
  Combat Log - they're map text, not log text. In Force Selection the Your Army panel (110-565,
  150-800) and Combat Log (1090-1510, 160-715) cover the map: photo band must avoid them or close them.
- Learned on Field of Glory II Medieval (fog2m-guide). Related: game-setup, game-ui (bgplay),
  memory grid-geometry-play.

## Apply the tools universally (the user, 2026-11-03, Dominions: "You missed a metric ton of provinces because you
## decided to arbitrarily set the zoom. We have tools for this now, man.")
- Before any sweep or board, name the tool for each step and use it: whole map first, atlas + resnap to know where
  every shot sits, the game's OWN menus for ownership and visibility (Dominions F1, map filters), click points
  from a FRESH shot (snap), every read verified (panel title / number). Never a hand-picked zoom, never
  coordinates from an older screenshot. A tool that doesn't fit gets fixed, not bypassed.
- Readable beats small: work at a zoom where names and flags read, and move the camera (lookat) instead of
  zooming far out (the user: "it's hard to see when everything is small").
- **Wraparound maps** (Dominions): no edge to anchor on. Measure the period (autocorrelation of a zoomed-out
  shot), keep ONE period as the world picture, tile it 3x3 as the resnap atlas, and do all world positions
  modulo the period (shortest way round when panning).

## Related skills
map-camera (calibrated steps), map-usage (turning photos into a board), battle-tactics, game-ui, planning
