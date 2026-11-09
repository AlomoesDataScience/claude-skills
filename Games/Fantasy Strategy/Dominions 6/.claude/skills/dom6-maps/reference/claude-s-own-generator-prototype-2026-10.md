# dom6-maps - Claude's own generator (prototype, 2026-10-28)

Part of the dom6-maps skill; SKILL.md links here.

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
