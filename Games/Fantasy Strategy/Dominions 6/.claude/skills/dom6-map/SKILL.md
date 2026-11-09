---
name: dom6-map
description: "Reading and using the Dominions 6 strategic map from the virtual screen: panels, provinces, armies, scout reports. Use when looking at the map, finding a province or army, or planning moves and wars."
keywords: "read, elements, title, resource, bar, commander, list, panel, report, flag, strip, owners, orders, shown, arrows, terrain, photo, camera, wheel, zoom, arrow-key, pan, measured, home, capital, messages, goto, atlas, trick, fog, zoomed-out, reference, resnap, finds, later, screenshot, sits, tested, match, plus, building, board, games, game's, war"
---

# Dominions 6 strategic map

The user (2026-11-03, Tir na n'Og SCBM MP game): "apply the new map look about skills to this map" and
"you made a tool to grid out the map, and also can reset the grid location from another picture" -
the FoG II map tools brought to Dominions. Generic method: map-usage, photo-map, map-measure,
map-camera. Driving the screen: dom6-ui `scripts/dom6bg.py` (read only). Rules of looking in an MP
game: dom6-game "Looking without changing anything".

## The turn look (every turn, before any decision - the FoG II look process, 2026-11-03)
The user: "we redid the entire look process to be better and improved." Generic: photo-map, map-measure,
army-log, scouting, war-language. All on Claude's virtual screen with dom6bg.py (read only until the user says).
1. **Screen elements** known (dom6-map section 1; named regions in game-ui.json). New screen -> hover first.
2. **Messages first** (`dom6bg.py messages`): battles, deaths, events, spells. Record every battle replay
   (`dom6bg.py battle NAME`, detail `4` every replay), read the report, add it to the dom6-tactics log.
3. **Whole-map photo** (`dom6bg.py mapshot 6`), placed on the game's atlas (resnap.py); grow the atlas when
   new land is seen.
4. **Province board** in the game's plan file: owner, terrain, armies seen (with the turn seen), neighbours;
   diff with last turn - new flags, lost provinces, armies that moved.
5. **Enemy armies**: scout report of every foreign army in view (`goto`, `read scout`), classified (main
   types, commanders, pretender?), dated. Stale sightings marked stale.
6. **Our armies**: army-check per commander, army-log snapshot (both sides after each battle).
7. **Threats**: what can reach which province next turn (map move, roads, rivers), where our commanders
   and mages are exposed, where the enemy is weak.
8. **Then war-language**: UP (picture) -> THINK (plan, written) -> DOWN (orders, only with the user's go in his
   game) -> CHECK (photo after each order). End Turn only on the user's go.

## 1. Screen elements (1912x1000 virtual screen; named regions in .claude/game-ui.json)
- Top: god title (`title`), resource bar (`resources`: treasury, income (upkeep), gems by path, blood).
- Left: commander cards (`commanders`) with name, paths, order (Move/Research...).
- Right: province panel (`province`: name (number), terrain, population, income, resources, recruit
  points, supplies, defence, unrest), dominion candles, sites (`sites`).
- Top-left over the map: **Scout Report** for a province with foreign troops (`scout`).
- Bottom centre: the hovered province's name (`hovername`). Bottom right: nation flag strip.
- Map: provinces with dark borders; names in grey text; flag on a pole = owner; figures = armies.

## 2. Reading the map
- **Owner = flag colour/emblem** (ours EA Tir na n'Og: green with an orange knot; grey = independents;
  other nations: note each new flag with the nation when known - Pangaea: green with antlers).
- **Arrows** = this turn's move orders. **Dotted lines** = the viewed province's connections: yellow passable,
  red blocked, blue water (dom6-game Map reading).
- **Armies**: a crowd of figures under a flag; a temple-like sprite = a fort/temple. Size by eye only;
  the scout report gives "about N units" and the main types.
- **Terrain from the photo**: yellow fields = farmland, dark green trees = forest, olive with shrubs =
  swamp, pale with dead trees = waste, grey peaks = mountain, blue = lake/sea, white = snow/highland.
  The province panel names it exactly ("Plains & River") - trust the panel over the picture.
- Fog of war is real here: unexplored provinces show no flags or armies; seen ones can be stale.

## 3. Camera (map-camera numbers, measured 2026-11-03)
- Wheel over the map zooms (6 notches out = about 3.25x smaller). Arrow keys pan: **72 px per 100 ms
  held** at normal zoom, same all four ways (camcal.py --keys Up Down Left Right --band 260 90 1600 940).
- Home = capital. Messages (`m`) -> "Goto province" = camera to that province (dom6bg.py goto TEXT).
- Leave the camera on the subject and park the mouse (dom6bg.py park) - idle-view.

## 4. The atlas (FoG II resnap, tested 2026-11-03)
1. `dom6bg.py mapshot 6` - zoomed-out photo of the known map (zooms back after).
2. `resnap.py build atlas.png --sq 100 --cols 13 --rows 8 --margin 0 --strip FAR.png -260 -90`
   (the strip offset skips the commander list and top bars).
3. `resnap.py find atlas.png SHOT.png --zoom 1.3 3.5 --area 260 90 1600 940` -> scale and offset of
   any later screenshot on the atlas (Troban view: sq 324.94, match 0.87; under 0.5 = don't trust).
4. Mark province names and numbers on the atlas once (from the panel / hovername), then every later
   shot can be labelled from it. A bigger atlas: several mapshots panned with the arrow keys and
   pasted with `build --strip` at their measured offsets (panorama.py --fwd Down --back Up, etc.).

## 4b. The province graph (provinces, NOT a grid - the user, 2026-11-03: "dominions doesn't explicitly use a grid")
FoG II's map is squares; Dominions' is provinces. Don't sample the map with a click grid (it misses small
provinces). Use the game's own map file - the one every player of the game has:
1. Find the game's folder: `~/.dominions6/savedgames/<game>/` (newest .trn/.2h = the live game; the user's SCBM MP
   game is `mr_bEAt`), its `<map>.map` (main plane; `_plane2.map` = the second plane).
2. `scripts/provgraph.py build MAP.map plans/<game>/provgraph.json` - 256 provinces, neighbours, special links,
   terrain bits, each province's centre (from the #pb pixel lines, wrap-aware).
3. Tie it to the atlas: a few provinces read on screen with their world point (`dom6bg.py sweep` once, or any
   provsweep file), then `provgraph.py fit GRAPH SWEEP.jsonl` -> scale (map px per world px, 7.50 here) and
   offset. Tir na n'Og test: median error 6.8 world px from 34 provinces (a province is ~27 wide).
4. `dom6bg.py provsweep GRAPH OUT.jsonl --views 3x3`: per view `lookat` + `snap`, right-click EVERY province
   centre on screen, check the panel's number is that province, record panel and scout report.
   Names: most come from the game (only #landname ones are in the file); unseen ones read "?".
   Tested 2026-11-03: 256/256 read, every panel number checked. Speed: one bgplay seq per view (click, wait,
   `shot --box` of the panel strip), OCR afterwards in parallel, empty views skipped.
5. Ownership and visibility come from the SCREEN (F1 for ours, flags, panels), never from the file.
Neighbours from the file are exact (`provgraph.py show GRAPH NUM`): use them for reach and threats, not the
dotted lines by eye.

## 5. Board for planning
A province board = a list of provinces with owner, terrain, armies seen (turn seen) and neighbours
(provgraph.json for terrain and neighbours, provsweep for what the screen shows this turn).
Keep it in the game's plan file (plans/), update it each turn, and diff turns (scouting).

## Status / hypotheses
- Hovering a province shows NO name label (tested 2026-11-03). OCR of map names failed (thin grey text on
  terrain); read names by eye from 1.5x crops. A province's panel: **right-click** the province (left-click on the map is a MOVE order).
- Useful map keys (dom6-game hotkeys): ctrl+9 names, ctrl+8 neighbours, ctrl+1 flags/forts, ctrl+2 armies,
  Insert fit screen, Delete whole map (atlas photo!), `g`/`#` go to a province number.
- **Wraparound confirmed** (Tir na n'Og SCBM game, 2026-11-03): the map repeats both ways. Measure the period
  by autocorrelation of the zoomed-out photo (546 x 341 px at 6 notches out = about 1775 x 1110 at normal zoom),
  cut ONE period centred on us = the whole world in one picture (plans/<game>/world.png), tile it 3x3 as the
  resnap atlas so views across the wrap edge still match (re-tested: match 0.87). There is no map edge to anchor on.
- Yellow glow at province edges = our dominion (dom6-game, taught turn 2).
- Red X over flags in the bottom strip: meaning not checked (eliminated? not met?).

## Related skills
dom6-ui (dom6bg.py, virtual screen), dom6-game (hotkeys, looking without changing), dom6-tactics,
dom6-army-check, map-usage, photo-map, map-measure (resnap.py), map-camera (camcal.py), scouting,
idle-view, draw-map, dom6-maps (maptool.py: the .map format).
