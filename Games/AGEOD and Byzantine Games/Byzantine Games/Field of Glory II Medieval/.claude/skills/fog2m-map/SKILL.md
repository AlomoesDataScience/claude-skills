---
name: fog2m-map
description: "Using the Field of Glory II Medieval battle map: layout, deployment zones, whole-map photos, reading squares and terrain. Use when deploying and on every FoG II turn, or when unsure what a square is."
keywords: "grid, grey, stone, border, enemy, front, line, label, darker, side, getting, whole, top, view, zoom, pan, numbers, recognising, type, photo, ones, invisible, need, tooltip, overlays, los, lof, command, range, zoc, move, charge, highlights, finding, identifying, units, turning, text, board, planning, game-specific, companion, generic, map-usage, map-camera"
---

# FoG II Medieval - using the map
Sources tagged: [game] = seen in game, [manual §] = manual, [hyp] = not yet checked (list at the end).
Order of truth: game > manual > hypothesis. Generic method: map-usage, map-camera, photo-map.

## 1. Layout
- Square grid, one unit per square, 8 facings; diagonal move = 1.5x AP [manual 8.3]. G shows the grid.
- Size in custom battles: Advanced Options Width x Height (V.Small/V.Narrow: 24 x 32) [game] =
  24 squares of frontage (N-S) x 32 deep (W-E) in battle 2. Measured (map-measure): top view, full
  zoom-out = 59.25 px/square; border detection --sat 14 --br 70 200 (tinted side --br 40 200).
- Battle 2 board: plans/battle2-boards/setup.txt (+ .png), squares from 3 strips (x0/y0 in map-measure).
- Border: a grey stone strip; beyond it black void [game]. Row/column 0 = first square inside it.
- Our deployment area is lit/highlighted during deployment; the enemy side is tinted darker, with a
  red "Enemy Front Line" label at its front edge [game, battle 2]. (Battle 2: we are WEST, enemy EAST,
  so the frontage runs north-south.)
- Fog of war: squares we can't see are darkened; yellow "?" marks squares at the edge of concealing
  terrain that might hide enemy (option) [manual 8.3].

## 2. Camera for this map (numbers: map-camera skill, FoG section)
- M top view + hold F 2500 = whole width-ish view; C log off, X minimap off, mouse to (1590,960).
- Panorama N->S: `panorama.py --axis v --step 100 --band 570 200 1595 665` (Force Selection) or the
  battle band `0 250 1490 725`. Whole map needs two strips (camera west, camera east).
- Jump: minimap click, or L unit list row click (selects + centres).

## 3. Terrain from a photo (top view)
| Looks like | Terrain | Status |
|---|---|---|
| plain smooth green | open | [game] |
| thin pale line | Tracks (tooltip says "Tracks") | [game]; roads/tracks effect: none listed in manual - [hyp] |
| dense dark tree clusters | woods = Difficult; blocks LOS; hides stationary foot | [manual 16] look [game] |
| concentric wavy lines | hill slopes (contours); height in tooltip; +25/+100 POA uphill | [manual 16.3]; look [game] |
| patchwork of brown/green plots | cultivated fields | [hyp] terrain class - tooltip |
| grey-brown scrub with stones | rough ground? | [hyp] - tooltip |
| rows of single trees round a block | hedge / enclosure boundary? | [hyp] - tooltip; enclosures are INVISIBLE [manual 24.1] |
| small buildings | buildings / village = built-up (blocks LOS, protects foot) | [manual 16]; look [game] |
| blue/water | stream/river - size decides difficulty; water impassable | [manual 16, 24.3] |
- INVISIBLE terrain: enclosure, medium/deep stream, dead ground, rough slopes look like their neighbours
  [manual 24.1/24.3]. For squares that matter (our line, charge lanes, flanks) hover the square and
  read the tooltip (terrain name + height; no height = 0) [game: "Tracks." tooltip seen].
- What each class does to whom: fog2m-guide PLAY.md "Terrain".

## 4. Overlays (all toggles; nothing permanent) [game, 2026-11-02]
- G grid. 2 LOS of the selected unit (lit = visible). 1 LOF of a selected shooter. 3 command range of a
  selected general (Knights & Sergeants (0) showed none). H distinct banners.
- On selecting a unit: reachable squares highlighted; enemy ZOC red (primary) / yellow (secondary)
  with dots on the unit exerting it [manual 11.1.1]; chargeable enemies get a charge icon; shooting
  targets brown (full arc 3 arrows, half arc 1) [manual 11.11.3].

## 5. Units on the map
- Each unit = several models in one square (knights: 4 horse models, each with a coloured banner;
  foot: 2 columns of figures) [game, top view]. Banners: side, general, losses, cohesion (yellow
  disrupted, red fragmented, white broken), darken once moved [manual 15, 8.5].
- Identify by hover (bottom card: name, AP, strength, type, quality, armour, capabilities) or the L list.
- Mind the font: "(1)" can look like other digits - read the card, not a guess.

## 6. Build the board
From the panorama: mark the border, lay the grid from it (measure the square at this zoom - G on),
then write a text board: rows x columns, one letter per terrain, unit marks with facing. Note the
deployment lines and the distance between them in squares. Then plan (battle-tactics).

## Hypotheses to test
- H-M1 patchwork fields: which terrain class (open? non-open?). H-M2 scrub patches = rough? H-M3 tree
  rows = hedges (obstacle) or enclosure? H-M4 tracks: any movement effect? Test: hover tooltip / move highlight.

## Related skills
fog2m-guide (rules: PLAY.md terrain, COMMANDS.md keys, UNITS.md), map-usage (generic method), map-camera, photo-map, map-measure (size, squares), draw-map (optional drawing), battle-tactics.
