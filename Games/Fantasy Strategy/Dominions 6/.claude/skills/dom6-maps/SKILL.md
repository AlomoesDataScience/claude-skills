---
name: dom6-maps
description: "Make Dominions 6 maps with MapNuke 2: players, era, layout, nations (mod nations too), install and check. Use when a map is wanted made, changed, checked or installed, or MapNuke questions come up."
keywords: "generate, copy, app, unity, gui, driven, through, dom6-ui, guard, wmclass, pick, including, export, exported, against, image, white, pixel, province, neighbours, starts, thrones, dominions6, covers, file, format, illwinter's, manual, terrain, masks, neighbourspec, specstart, gate, planes, mapnuke's, data, files, nation, xmls, guarded, input, screenshots, commands, added"
---

# Dom6 maps

Random maps are made with MapNuke 2 (github.com/nuke-haus/mapnuke, itch.io nuke-haus/mapnuke-2):
a Unity app that generates a balanced map for a set of nations, lets you edit it, and exports a
ready Dominions 6 map. Claude drives its window through the dom6-ui guard, then checks and installs
the export with `maptool.py`. Hand-drawn maps and the game's own random map generator are not
covered yet.

## Files

- `Games/Fantasy Strategy/Dominions 6/Maps/mapnuke/app/LINUX/MapNuke.x86_64` - the app (v1.1.2, Dom6 edition, Linux build).
  Data in `MapNuke_Data/`: `Nations/*.xml`, `Layouts/*.xml`, `NameData/`, exports in `Export/<map>/`.
- `Games/Fantasy Strategy/Dominions 6/Maps/mapnuke/source/` - its C# source. `Assets/Scripts/Output/MapFileWriter.cs` writes
  the .map, `Data/ProvinceData.cs` the terrain enum, `WorldGen/GeneratorSettings.cs` terrain and
  border frequencies, `Interactive/GenerationManager.cs` the UI actions.
- `Games/Fantasy Strategy/Dominions 6/Manuals/dom6mapman.pdf` - Illwinter's Dom6 Map Making Manual v6.26 (the format rules).
- `scripts/maptool.py` - `check PATH` (a .map or its folder), `install PATH [--force]`, `list`.
- `scripts/mapnuke_ui.sh` - `mseq "X Y" ...`: reliable MapNuke clicks (see Input below).
- Builds on **dom6-ui** (`dom6ui.py`: guard, `seq`, screenshots; `drag --slow` was added for Unity).

Run Python with `python3 -I` (system Python with PIL only; no pip).

## Launching

The user allowed this in `/permissions` (2026-10-28); running the downloaded binary is otherwise
refused by the auto-mode check, and Claude may not write that rule itself.

```
cd "<workspace>/Games/Fantasy Strategy/Dominions 6/Maps/mapnuke/app/LINUX" && (nohup ./MapNuke.x86_64 -screen-fullscreen 0 -screen-width 1600 -screen-height 900 -logFile <scratchpad>/mapnuke.log >/dev/null 2>&1 &)
```

First a "MapNuke Configuration" dialog (598x640): pick 1600 x 900 in the list (drag/scroll it),
quality Medium (memory: the laptop has ~7 GB and Dominions may be running), Windowed on, OK
(515,616). Then the main window "MapNuke" (1600x900). `UI_WMCLASS=MapNuke` (the guard compares
the class before its first dot; wmctrl shows `MapNuke.x86_64.MapNuke.x86_64`).

## Layouts and art styles

- `MapNuke_Data/Layouts/*.xml`: `<Layout>` = Name, XSize x YSize grid of province nodes (8x8 = 64
  provinces), `<Spawn>` X, Y, SpawnType PLAYER or THRONE. The Layout dropdown lists those matching
  the player count: Default (2-30 players, e.g. 3p 8x8, 9p 12x12, 30p "Big Fucking Map" 24x20),
  Compact (10, 11, 13, 14), Diagonal (5, 10, 17, 20), Hexagonal (4, 6, 8, 12, 16, 18, 20, 24),
  Throne Hoard (4; 6 players with 12 thrones; 8), Knifefight (7, 10, 11, 13, 14), TEST (2p, 47 thrones).
  New layouts are plain XML (the source has a LayoutTool).
- Art styles (Map Art dropdown): Default and Parchment. In the source an art style is
  `Assets/Gfx/MapArt/<Style>/<Terrain>/` sprites (~330 small PNGs for Default: grass, trees, huts,
  mountains, coral, bridges, cave crystals; a `...s.png` twin is the snowy version) scattered per
  terrain, `Assets/Gfx/Materials/<Style>/` noise-shader materials for province ground, and a prefab
  in `Assets/Resources/Prefabs/ArtStyles/` (cull chance, province edge threshold, sprite sizes).
  Adding one needs Unity 2019.2.11f1 and a rebuild (README). No pure white in any art.

## Input (learned the hard way, 2026-10-28)

- A click whose press lands in the same frame as the pointer move is lost: move, wait, then press
  with `--hold 100`. An opening dropdown list ignores clicks for a moment (fade-in): wait ~800 ms.
  `mapnuke_ui.sh`'s `mseq` does all this.
- Each `dom6ui.py` call ends by giving focus back to the terminal. Open dropdown lists usually stay
  open across calls, so take a screenshot before acting: clicking a header whose list is already
  open closes it.
- Keyboard: Enter opens a focused dropdown, but arrow keys move focus between widgets once the list
  is shut (focus walked down to Quit). Prefer the mouse.
- `drag` without `--slow` moves in one frame; Unity ignores it.

## Workflow

1. Add any mod nations the user wants to `MapNuke_Data/Nations/ModNations.xml` (fields below);
   restart MapNuke to load them.
2. Launch, set players, age, layout and each player's nation; Generate New Map; look at it
   (Toggle Hide Settings, Change Viewed Layer for the caves). Regenerate until it looks fair.
3. Export Map Files with a name of letters and `_` only. Exporting takes about a minute (23 files
   for a 3-player map): wait until `Export/<name>/` stops changing before using it.
4. `maptool.py check Export/<name>` then `maptool.py install Export/<name>`. It copies the .map,
   the plane2 .map and every image the game reads (main, winter, terrain looks with their `w`
   winter versions, plane2 image), not the `_with_labels.png` previews.
5. Check it in game only when the user says the game is free (Dominions may be running an ongoing
   game): main menu `e` > Load map > the map's folder > `<name>.map` > Ok. The editor shows the
   province panel (Mode: Neighbors, terrain ticks, Advanced commands, Statistics, Save map, Exit).
   Statistics counts every plane (a 64-province map with a cave plane shows 128; cave walls count
   as land) and "Starts: 0" with #specstart starts. Leave with Exit, never Save map unless asked.
   ClaudeTest loaded and matched maptool.py (2026-10-28).
6. Report the map's numbers (provinces, thrones, starts) and that it is untested in game.

## MapNuke data files

- Nation XML (`<Nation>`): `Name`, `ID` (Dominions nation number), `WaterPercentage` (0-1),
  `Age` EARLY/MIDDLE/LATE, `CapRingSize` (provinces around the capital), `CapTerrain`, one
  `TerrainData` per ring province, optional `StartsUnderground`, `HasCaveEntranceInCapRing`.
  Terrain words: PLAINS FOREST HIGHLAND MOUNTAINS SWAMP WASTE FARM SEA DEEPSEA LARGEPROV SMALLPROV
  (combine with spaces: `SEA DEEPSEA`).
- ModNations.xml now holds the user's (MA) Excitorius 150, (LA) Ananke 152 and (MA) Nethris 153
  as land nations; their ring terrains are Claude's guesses. Original kept as ModNations.xml.orig.
- Layout XMLs: map size and spawn points (PLAYER / THRONE) per player count.

## Dom6 map format (dom6mapman.pdf)

- Required: `#dom2title` (first command), `#imagefile` (24/32-bit TGA, ≥256x256), `#mapsize`.
  Each pure white pixel (255,255,255) is one province; use (253,253,253) for white art.
- Install as `~/.dominions6/maps/<Name>/<Name>.map` + `<Name>.tga`; folder name = map name.
  Updating a map in an ongoing game only changes its graphics.
- `#terrain <prov> <mask>`: plains 0, small 1, large 2, sea 4, freshwater 8, highland 16, swamp 32,
  waste 64, forest 128, farm 256, nostart 512, many sites 1024, deep 2048, cave 4096, site paths
  8192-4194304, mountains (near mountains, no move cost) 8388608, good throne 33554432, good start
  67108864, bad throne 134217728, warmer 2^30, colder 2^31, cave wall 68719476736.
- `#neighbour a b`; `#neighbourspec a b n`: 1 mountain pass, 2 river, 4 impassable, 8 road.
  `#pb x y len prov` pixel ownership (editor only). `#landname prov "name"`.
- `#specstart nation prov`, `#allowedplayer nation`, `#gate prov gatenr` (cave entrances),
  `#nodeepcaves` / `#nodeepchoice`, `#mapnohide`, `#wraparound`, `#domversion`, `#description`.
- Extra planes: `<name>_plane2.map` / `.tga` ... up to 8 planes; terrain looks
  `<name>_forest.tga`, `_waste _farm _swamp _highland _plain _kelp _water`, a `w` suffix for
  winter, `<name>_winter.tga` the default winter look; plane looks `<name>_plane2_forest.tga`.

## What a MapNuke export looks like (ClaudeTest, 3 players, MA)

64 provinces on a 2048x1280 wraparound map, 21 provinces per player, 192 borders (11 mountain
passes, 11 impassable, 10 rivers, 6 roads), 3 good thrones, 3 cave gates, a cave plane of 12 cave
provinces in 52 cave walls, `#domversion 575`, `#nodeepcaves`, `#nodeepchoice`, `#mapnohide`.
MapNuke lists some borders once and some both ways; `maptool.py` counts unordered pairs.

## Reference files (read the one the step needs)

| File | Holds |
|---|---|
| `reference/main-screen-1600x900-window-pixels.md` | **Main screen (1600x900 window pixels)** - Control | Where | Notes | |---|---|---| | Nation of player 1, 2, 3.. |
| `reference/claude-s-own-generator-prototype-2026-10.md` | **Claude's own generator (prototype, 2026-10-28)** - Games/Fantasy Strategy/Dominions 6/Maps/mapgen/mapgen.py NAME [--players 4] [--cols 10] [--rows 6] [--size 160 |
| `reference/editing-a-generated-map-explored-2026-10.md` | **Editing a generated map (explored 2026-10-28)** - Camera: left-drag pans the map |
| `reference/lore-for-a-map-game-sources-wikifetch-py.md` | **Lore for a map (game-sources wikifetch.py and the LORE layer, 2026-10-29)** - Lore wikis are read with the generic game-sources skill (wikifetch.py in the project's root   .claude/skills |

## Related skills
dom6-ui, dom6-modding, map-usage, draw-map.
Also (2026-11-03): dom6-map (reading a map in play).
