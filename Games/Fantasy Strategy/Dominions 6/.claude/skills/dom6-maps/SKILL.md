---
name: dom6-maps
description: Make Dominions 6 maps: generate them with MapNuke 2 (the user's copy in mapnuke/app, a Unity GUI driven through the dom6-ui guard with UI_WMCLASS=MapNuke), pick players, era, layout and nations (including the user's mod nations), export, check the exported .map against its image (one white pixel per province, neighbours, starts, thrones) and install it to ~/.dominions6/maps. Covers the Dom6 map file format from Illwinter's map manual (#terrain masks, #neighbourspec, #specstart, #gate, planes) and MapNuke's data files (nation and layout XMLs). Uses dom6-ui (guarded input, screenshots). Use when the user wants a Dominions 6 map made, changed, checked or installed, asks about MapNuke or map commands, or wants mod nations added to MapNuke.
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

## Main screen (1600x900 window pixels)

| Control | Where | Notes |
|---|---|---|
| Nation of player 1, 2, 3... | x 150, y 22, 56, 90... (+34 each) | green dropdowns, one per player |
| Players (2-30) | 394, 20 | list rows 20 px apart, "2 Players" at y 47 |
| Layout | 394, 50 | layouts for that player count (3 players: only Default Layout) |
| Age | 394, 80 | Early (107), Middle (127), Late (147), All (167); filters the nation lists |
| Map art | 394, 110 | Default Map Art |
| Toggle Hide Settings | 1511, 20 | hides the panels to see the map |
| Change Viewed Season / Layer | 1511, 50 / 80 | winter look; surface or cave plane |
| Advanced Settings | 1511, 110 | terrain and border frequencies (GeneratorSettings.cs) |
| Export Map Files | 1511, 140 | asks a name (field 800,450; OK 799,492) |
| Generate New Map | 1511, 170 | ~2-3 s for 3 players |
| Quit | 1565, 880 | never press Enter while it has focus |

Nation lists: 9 "Generic ..." entries, then vanilla nations of the age, then `DE -` (Dominions
Enhanced), `MOD -` (ModNations.xml, the user's nations), `BZ -` (Bozmod). The list (400 px tall,
scrollbar at x 283) does not take the mouse wheel: drag its scrollbar with `drag --slow` in the
same `seq` as the click that opens it. Player 1's list opens at y 37-433; each later player's list
starts 34 px lower.

On the map: capitals carry the nation name, thrones are labelled "Throne". Province dots are
coloured by terrain (white plains, green forest, gold farm, blue water...); lines are borders:
yellow standard, blue river, purple mountain pass, dark red impassable/cliff, orange road.

## Claude's own generator (prototype, 2026-10-28)

`Games/Fantasy Strategy/Dominions 6/Maps/mapgen/mapgen.py NAME [--players 4] [--cols 10] [--rows 6] [--size 1600x1000]
[--seed N]` writes a whole map without MapNuke in ~16 s: noisy power-diagram provinces, graph from
touching pixels, sea, spread starts (`#start`), thrones, clustered terrain, rivers and ridges along
border chains, roads, a drawn art style with winter and terrain-look images, `NAME_preview.png`
(numbers, S start, T throne). Then `maptool.py check` / `install`. Facts it relies on (checked
against a MapNuke export): Dominions numbers provinces by scanning white pixels from the bottom
row up, left to right, and `#pb x y len prov` counts y from the bottom. ClaudeGen (seed 4242,
60 provinces) loaded in the map editor with matching statistics; the user is reviewing it.

### Maps from a finished picture (2026-10-29)

`Games/Fantasy Strategy/Dominions 6/Maps/mapgen/from_image.py IMAGE REPLICA PICTURE --config CFG [--players N] [--land SP] [--sea SP]
[--seed N]` makes two maps with one province layout: REPLICA redrawn in mapgen's art style (plus a
house or castle symbol on every detected town/capital and a numbered tag on every adventure site),
PICTURE with the picture itself as the map (borders drawn over it, winter tint). The config module
describes the picture (docstring of from_image.py lists the fields). `greyhawk_hd.py` (for
`Greyhawk HD.png`, flat colours) is the full example: exact palette per class, water/river colours,
yellow city fill (several yellow wedges = capital star), ~140 label spots read off gridded crops
(`NAMES`, `WATER_NAMES`), `NAME_TERRAIN`, `EXTRA_BITS` (ice colder, desert/jungle warmer), `SITES`
from the adventure key. `greyhawk_classify.py` is the older painted-map config (texture colours,
dashed rivers; weaker).

- Every label seeds a province (an earlier label within 0.62 spacing wins; the later one only names
  the province it falls in); jittered grid centres fill gaps 0.8 spacing from any seed; fill
  provinces are named "<Direction> <nearest label>"; named forests/hills/marshes take that terrain.
- Provinces grow by Dijkstra on a work grid (`WORK`, 3 for 3200 px) and cannot cross rivers; the
  full-size labels are mode-filtered to remove grid steps. Labels live in bytes: under 255 provinces
  (raise --land/--sea if the assert fires).
- Provinces with an adventure site get many sites (1024); the .map lists the sites as comments.
- Greyhawk HD (seed 2026, --land 58 --sea 100): 219 provinces, 126 from labels, 203 named,
  185 cities, 26 sites, 100 river / 30 impassable / 23 pass borders, 12 starts, 11 thrones;
  ~2 min. Installed as GreyhawkHD and GreyhawkHDPicture.

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

## Lore for a map (game-sources wikifetch.py and the LORE layer, 2026-10-29)

- Lore wikis are read with the generic `game-sources` skill (`wikifetch.py` in the project's root
  `.claude/skills/game-sources/scripts/`): Wayback fetching for Cloudflare sites, page text, links,
  fact boxes (`infoboxes OUTDIR OUT.json`), or the MediaWiki API (`allpages`, `api`).
- Greyhawk lore now lives with D&D: `Games/Tabletop RPGs/Dungeons & Dragons/Worlds/Greyhawk/lore/`
  (Flanaess.html/.txt, `pages/` 143 pages, `infoboxes.json` 89 fact boxes) and the source pictures
  in `.../Worlds/Greyhawk/maps/` (`Greyhawk HD.png`, `Greyhawk.jpeg`). The `greyhawk-lore` skill
  there (`lore.py realm/list/search`, `realms.md`) is the quick way to the realm facts.
- `from_image.py` gives every province a realm (`self.realm`: its own label, or the nearest label
  for fill provinces). Config fields read by `province_lines` (written as `#setland` blocks at the
  end of the .map, after the `#pb` lines; mapgen.py's `province_lines(num)` hook):
  `LORE = {label: {"poptype": n, "people": realm population, "fort": n, "climate": "cold"|"warm"}}`
  (population spread over the realm by area, towns ×1.35 and capitals ×2 weight, `POP_SCALE`
  default 0.02, clamped 500-40000, never on start provinces; forts only where a capital symbol is),
  `SITE_FEATURES = {adventure number: [vanilla site ids]}` → `#feature id`. Climate from LORE
  replaces the picture's warm/cold bits before starts are chosen.
- Status: written and parsing, **not yet run** - the Greyhawk LORE table is still to be filled from
  infoboxes.json. Poptype numbers are in the map manual's table (`#poptype`), site ids from
  dom6-inspector (`records/sites.jsonl`). Picks so far: Temple of Darkness 843 (Temple of Elemental
  Evil), Tomb of the Grand Thaumathurg 822 (Tomb of Horrors), Slave Market 1073 (Slave Pits),
  Jungle Temple 872 (Tamoachan), The Forgotten City 732 (Forbidden City), Abandoned Laboratory 692
  (In Search of the Unknown), Circle of Standing Stones 643 (Shattered Circle), Frost Vale 544
  (Glacial Rift), Castle Arcanum 640 (Castle Greyhawk).
