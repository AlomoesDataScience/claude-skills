# dom6-maps - Editing a generated map (explored 2026-10-28)

Part of the dom6-maps skill; SKILL.md links here.

## Editing a generated map (explored 2026-10-28)

- Camera: left-drag pans the map. Right-click a node to edit it (close panels with their X, top right).
- **Province node** (the big dots) > "Province Terrain" panel at the right: Plains, Highland/Reef,
  Mountain, Swamp, Wasteland, Farm, Forest/Kelp, Sea, Deep Sea, Large/Small Province, Cold/Warm,
  Throne Spawn Point, Random Fort Spawn Point, More Magic Sites, a custom name; "Cave Layer Province
  Terrain": Has Cave Layer Province, Has Cave Layer Entrance, Cave / Drip / Crystal / Cave Forest /
  Submerged Cave, a cave name; Apply Changes.
- **Border node** (small dot halfway along a line) > "Connection": Normal, Road, Mountain
  (impassable), Mountain Pass, River, Bridged River; "Cave Connection": Normal, River. Clicking a tick
  applies it.
- **Change Viewed Layer** shows the cave plane (dark rock, cave provinces as coloured patches, the
  same nodes); click again for the surface. **Change Viewed Season** toggles the winter art (snow over everything); it takes ~3-5 s to repaint, so wait before judging the screenshot.
- **Advanced Settings** ("Advanced World Generator Settings", close with X at 1287,158, apply with
  Apply Changes, Reset Settings): min-max % of swamps 6-8, wastes 6-8, legacy mountains 5-7,
  highlands 5-7, forests 16-18, farms 14-16, extra lakes 6-8 (plains = the rest, 28%), large 28-32 and
  small 10-14 provinces, random forts 0-0, extra cave lakes 1-3, "only use mountain terrain flag for
  provinces with mountain connections"; borders (by % of connections) roads 4-6, bridged rivers 7-9,
  rivers 7-9, mountains 7-9, mountain passes 7-9; dominion overlay, province border and sea border
  colours (RGBA); Nation Themed Starts, Cluster Water Nations Together, Cluster Island Nations With
  Water, Disciples, Generic Starts, Fog Of War Effect; Procedural Name Chance 10 %, Cave Entrances
  Per Player 1, Underworld Cave Freq 6 %. Defaults are in GeneratorSettings.cs.
