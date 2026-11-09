---
name: draw-map
description: "Draw a game map as a clean schematic picture (grid, terrain colours, units, arrows) from a text board with drawmap.py. Use when the in-game map is hard to read or only some map elements need laying out."
keywords: "optional, tool, reads, numbered, columns, rows, legend, sides, facing, movement, attack, notes, simple, thinking, aid, replacement, looking, it'd, easier, figure, drawn, game's, dark, tints, perspective, clutter, overlays, tiny, models, odd, fonts, flank, charge, lane, deployment, lines, ranges, drawing, proposals, plan"
---

# Draw map - optional

**Optional (the user, 2026-11-02).** Use it when a drawing beats the game's own map:
- figuring the map out would be easier from a drawn picture than from the in-game map;
- **the map is hard to read**: dark tints, angled perspective, clutter, small models, odd fonts,
  overlays on top;
- **only some map elements matter**: one flank, a charge lane, deployment lines, a range, who
  borders whom. You don't need to draw the whole map.
- drawing **movement proposals** - for that use **draw-moves** (one picture or turn by turn, on top of this).
Don't use it when the game map is already clear. Look at the game first (photo-map); the drawing is
for thinking, and the game is still the truth. Drawing is free-form: draw it however you think it
looks. Approximate is fine; mark guesses with `?`.

## How
1. From photos (photo-map, map-camera) and tooltips, write a text board (BOARD.txt):
   ```
   grid:            one line per row, one character per square (row 0 = top/north)
   ....WWW....
   TTTTTTTTTTT
   units:           ID SIDE COL ROW FACING label     (SIDE = colour name or #hex; FACING N..NW or -)
   K1 royalblue 2 2 E Knights
   moves:           ID COL ROW -> COL ROW label
   K1 2 2 -> 6 2 advance
   marks:           COL ROW note
   colour:          CHAR #hex name                     (add a terrain type)
   ```
   Default terrain characters: `.` open, `W` woods, `H` hill, `R` rough, `F` fields, `T` track,
   `B` buildings, `M` marsh, `S` water, `E` enclosure, `O` obstacle, `X` impassable, `?` unknown,
   `#` border.
2. `python3 -I scripts/drawmap.py BOARD.txt [OUT.png] [--cell 28]`, then look at the picture.
3. Keep board files next to the battle plan (plans/), named per turn (`turn03.txt`), so the next turn
   starts from the last one. Update from fresh photos; never carry an old board forward unchecked.
4. To draw a part of the map, write only that part. The column and row numbers can start from
   anything that you note at the top (e.g. `# cols 10-20 = map cols 10-20`).

## Example
`example.txt` (made up): woods, a track, rough, fields, a hill, our knights advancing east towards
a French knight unit.

## Related skills
draw-moves (movement plans, one picture or per turn), photo-map (photos the board is read from), map-measure (square grid to read from and compare against), map-camera, map-usage (the text board step - this draws
it), battle-tactics (movement proposals), planning (keep boards with the plan); per-game map skills
such as fog2m-map give the terrain legend for that game.
