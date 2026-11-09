# dom6-game - Map reading (taught turn 2)

Part of the dom6-game skill; SKILL.md links here.

## Map reading (taught turn 2)

- Dots between provinces are connections: **yellow** = passable, **red** = blocked (needs flying
  or another way), **blue** = water. They show around the selected/viewed province.
- Map mode can be changed to taste; its hotkey is in the `?` list.
- Owned dominion glows yellow at the province edges. After turn 1, right-clicking neighbours
  shows Scout Report boxes (top-left, "about N enemy units ... mainly X") for provinces a scout
  saw or that border yours; the box pushes the commander tokens down (Latinus at about (80, 255)).
- A Scout Report is only the one-line summary ("about N enemy units ... mainly X and Y"):
  hovering the enemy figures shows the same line, and clicking the box does nothing.
  Unscouted provinces show terrain only.
- The province panel title is a bar the scene reader can miss: OCR the box (1600, 100, 1900, 132)
  directly. Some hover tooltips (recruit portraits over the map) have a grey frame that probe's
  tan-frame finder misses: screenshot the band (300..1620, 930..1044) and read it.
- Recruiting in a captured province: right-click it, `r`. It offers that province's own
  commanders and units (Helmshire: Scout, Mounted Commander, Priest (temple needed); Militia,
  Light and Heavy Cavalry) and has its own commander point ("Recruitment points: 90 / 1").
  Resources are per province: a short one shows negative resources and a dimmed queued unit.
- `Return` on the main map can open Army Setup (it is not only "deselect"); check the screen
  before the next click.
- Unit order inside an army follows recruit order; it rarely matters (the user).
- Moving a new unit into a squad: Enter, click the unit in the garrison strip, click the squad
  strip; alt+click moves all of that type. A Standard in a squad shows "+2 morale".
- A movement order shows on the token ("Move", "Sneak") and as an arrow on the map; the hover
  tip reads "X. Move to Province (n)".
- **A move is one turn's reach.** Clicking a province beyond it gives an order to a nearer one
  (Picus, turn 7: clicked Gentle Woods, got "Sneak to Azimar", straight into our own attack).
  Check the order in F1 or the token's hover tip after every long move.
- **F1 Nation Overview finds hidden scouts:** "Sneaking commanders" lists them (order "Hide" =
  arrived, idle). Clicking a name jumps the map to him with his token **already selected**;
  clicking the token again deselects it, so just click the destination.
- `y` (Army setup at destination) shows the **viewed** province: right-click the target first.
