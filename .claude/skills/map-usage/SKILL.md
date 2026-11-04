---
name: map-usage
description: Generic method for using any game's map or board to make decisions - what to establish about a map (layout, grid, borders, coordinates, deployment zones, sides, fog of war), reading terrain from photos and knowing which terrain is invisible and needs a tooltip, using the game's overlays (grid, line of sight, ranges, zones of control, movement and attack highlights), locating and identifying units, building a text board for geometry, and checking the map after every action. Also defines what every per-game map skill (<game>-map) must contain, and when to write one. Builds on map-camera (seeing) and photo-map (photographing); per-game rules live in each game's guide. Use when starting any game with a map, before planning moves, when a game's map skill doesn't exist yet, or when unsure what something on a map is.
---

# Map usage - generic

The map is where the decisions are made. You need to know what's on it, where the edges are, who is
where, what each square does, and what you can and can't see. Order of truth: the game, then the
manual, then a hypothesis that you test.

## 1. Establish the map once per game (and per new map type)
1. **Layout:** grid kind (squares, hexes, provinces, free), size, borders and how they look, and
   what's beyond them.
2. **Size and coordinates - early: map-measure skill** (size from the game, borders, square size,
   where square (0,0) is in each photo). **Coordinates:** an origin (the first square inside a border) and a direction. Measure the
   square or hex size at each zoom you use; never assume it.
3. **Sides:** where each side deploys, how the game marks them (tints, labels, zone lines), and
   which side colour or banner is which.
4. **Fog of war:** how unseen areas look, and what reveals them.
5. **Terrain legend:** for each terrain type,
   - what it looks like in a photo;
   - what the tooltip calls it;
   - its rule class (from the manual);
   - **whether it's invisible**, i.e. looks the same as its neighbour. Those squares need a
     tooltip check.
6. **Overlays:** every toggle and highlight (grid, line of sight, fire lines, command or supply
   range, zones of control, reachable squares, attack and charge icons). For each, note what it
   needs: a selected unit, a general, a shooter.
7. **Units on the map:** how a unit looks, how to tell sides apart, how facing, strength and
   morale show, and how to identify one (hover card, list).

## 2. Each turn
1. Photograph the whole board (photo-map, using map-camera's calibrated steps).
2. Identify the screen elements first: UI, map, borders, danger buttons.
3. Mark both sides' units, with type and facing.
4. Name the terrain where it matters. Where it could be invisible, check the tooltip.
5. Write a text board (rows × columns, terrain letters, unit marks with facing). Optional: draw it
   (draw-map) when a picture would be easier to read than the game map, or for some elements only.
6. Measure what matters in squares: reach, ranges, gaps, flanks, line of sight.
7. Plan, using battle-tactics and the turn method.
8. Act one order at a time, and photograph that area after each order.

## 3. Rules of thumb
- Photos show what things look like; tooltips and overlays show what the rules say they are.
  Use photos for the whole picture and tooltips for the squares that matter.
- Don't scan every square by hover; that's slow (FoG battle 1). Read most terrain by eye and check
  only the key squares.
- Don't learn the situation by cycling units (Tab or next unit). Look at the board.
- Distances are counted in squares or hexes, not pixels. Lay the grid from the border.
- A transient camera or overlay state can mislead. If something looks wrong, wait and look again.

## 4. Per-game map skills: write `<game>-map` for every game with a map
Write it during learn-to-play, before real play. It sits next to the game's guide
(`<game folder>/.claude/skills/<game>-map/SKILL.md`). Required sections:
1. **Layout:** grid kind and size, how the borders look, coordinates and origin, deployment or
   start zones, side markings, fog of war.
2. **Camera for this map:** keys, the best view for photos, panorama band and calibrated step
   (from map-camera), and how to jump to a spot.
3. **Terrain legend:** a table of look → tooltip name → rule class → visible or invisible, each
   row tagged [game], [manual §] or [hyp].
4. **Overlays:** every toggle and highlight, its key, and what it needs.
5. **Units on the map:** look, sides, facing, strength and morale markers, how to identify one.
6. **Building the board:** how to lay the grid and write the text board for this game.
7. **Hypotheses to test:** with how to test each.

Point to the guide for the rules (terrain effects), not a copy of them. FoG II's
`fog2m-map` is the first example.

## Grid or graph? (the user, 2026-11-03: "dominions doesn't explicitly use a grid on the map")
- Square/hex maps (FoG II, wargames): grid tools - gridshot, squares, a text board by col,row.
- **Province/area maps** (Dominions, Paradox, board games with areas): a GRAPH - provinces with neighbours. Don't
  sample them with a click grid (it misses small areas, double-reads big ones). Get the graph from the game's
  own map data when every player has it (Dominions .map: provinces, neighbours, terrain, pixel areas ->
  dom6-map provgraph.py), tie it to the screen once (snap + a few read provinces -> scale/offset), then visit
  each province at its own centre and check the panel names that province. Ownership/visibility still come
  from the screen. Reach and threats come from the neighbour lists, not dotted lines by eye.

## Related skills
map-camera, photo-map, map-measure (size and squares, early), draw-map (optional drawing), draw-moves (movement proposals), battle-tactics, planning, manual-first, learn-to-play, generalize-learning; per-game example fog2m-map
