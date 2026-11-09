---
name: se4-modding
description: "Modding Space Empires IV Deluxe (v1.95): how mods load, the data files, checks, the WMD mod. Use when making, fixing, checking, comparing or installing an SE4 mod or editing its data files."
keywords: "path, txt, directory, folder, under, bitmaps, fall, back, base, game, mod-loader, modinfo, modinfo2, format, file, self-documenting, headers, field, value, records, tech, requirements, abilities, families, pictures, bundled, example, extras, se4data, list, show, fields, diff, against, vanilla, check, references, error, warn, note, tree, unlocks, dead, ends, gather"
---

# Space Empires IV modding

Status 2026-11-01: learned from the game's own data headers, the Deluxe manual's modding article
(manual PDF p92-100, `SE4DeluxeManual.txt` around line 4240), `Path.txt`, `DataFileHistory.txt`
and the mods in `Extras/`. Nothing has been loaded in game by Claude yet.

Game install: `~/.local/share/Steam/steamapps/common/Space Empires IV Deluxe/se4/` (v1.95).
**Read only.** Never edit its Data files or `Path.txt` without the user's go: installing or switching a
mod changes the game for him.

## How mods load

- `se4/Path.txt`: `Using Mod Directory := None` uses the base files; a folder name (a folder
  directly under `se4/`) makes the game load from it first.
- That folder must hold **every** data file (28 in `Data/`); only bitmaps fall back to the base
  game's `Pictures/`. All five complete mods in `Extras/` ship the full 28 (CarrierBattles lacks
  SectType). Copy unchanged files from vanilla.
- Layout mirrors the game: `Data/`, `Pictures/` (Components, Races/<race>, Planets, Events...),
  optionally `Ai/`, `Empires/` (.emp race setups), `Sounds/`.
- **Mod loader** (the user has one and can get newer ones): reads `modinfo.txt` in the mod folder, in
  the "Modinfo2" format: line `Modinfo2`, then pairs of lines `Key:-` / value for `Obsolete`,
  `ModName`, `Version`, `Author`, `EMail`, `Website`, `Description` (description runs to the end).
  It switches `Path.txt` for you.
  the user's copy: `SE4MatryxModPicker.zip` (SE4 Launcher 2.1 + SE4Launcher.doc) in the SE4 folder. Put
  `SE4 Launcher.exe` next to `Se4.exe`; it lists the folders under `se4/` as mods, can launch the
  game or the map editor with one, and finds saves in `<mod>/Savegame/` (save there so a game
  always reopens with its own mod). `Obsolete: True` hides a mod from the list.
- Saved games remember their mod; everyone in a multiplayer game needs the same mod files.
- **The user's method** (WMD): the mod's own folder holds only the files he changed, so he can see
  what differs from vanilla. A **build** = vanilla `Data/` + `Pictures/` copied into a new folder,
  the mod's files pasted over them (`se4data.py merge` does this). To play it he installs the build
  over the game's files after backing them up (or uses the mod loader). Check a mod-only folder
  with `check --overlay` (missing files = vanilla), a build without it.
- The game itself has bugs (it does not always do what its data headers say): an in-game test
  is the final word, and odd behaviour may be the engine, not the mod.

## Data file format

- Each file opens with a header that documents every field and its allowed values (Components.txt
  lines 1-165, Facility.txt to ~line 50...): **read the header before editing a file**. Then
  `*BEGIN*`, the records, `*END*`.
- A record is `Field Name   := value` lines; a new record starts at `Name`. Lists are numbered:
  `Number of Tech Req := 2` then `Tech Area Req 1/2` + `Tech Level Req 1/2`; `Number of Abilities`
  then `Ability N Type/Descr/Val 1/Val 2`. The counts must match the lines.
- Components: `Pic Num` (index into Comps.bmp), tonnage space and structure, mineral/organic/
  radioactive costs, `Vehicle Type` (Ship, Base, Fighter, Satellite, Mine, Troop, Drone,
  WeapPlatform, combos like `Ship\Base`), `Supply Amount Used`, `Restrictions` (One Per Vehicle...),
  `General Group` (design window filter), **`Family`** (same number for every roman-numeral level of
  one component, so "show latest only" works), `Roman Numeral` 0-20, then weapon fields if
  `Weapon Type` is not None. Descriptions can use `[%ShieldPointsGenerated]`-style tags.
- TechArea: `Name`, `Group`, `Maximum Level`, `Level Cost`, `Start Level`, `Raise Level`,
  `Racial Area`, `Unique Area`, `Can Be Removed`, tech requirements. Max level 0 is a common lock
  ("Inaccessible Technology") for things that must never be researched.
- Ability names come from `Abilities.txt` (each name flush left, `Value1/Value2` meanings indented
  under it); vanilla also uses a few it does not list (`Launch Drones`). 1.86 added `AI Tag ##`
  abilities to steer the AI to components, 1.90 `Generate Points` abilities.
- AI: `se4/Ai/<race>/` and `Ai/Default_AI_*.txt` (Research, DesignCreation, Construction,
  Fleets, Politics...). They name techs and components: a total conversion needs its own AI
  files or the AI researches and builds nothing useful.
- Pictures: ship sets are 128x128 portraits + 36x36 tactical images per hull; components share
  Comps.bmp. Version changes to the formats are listed in `se4/DataFileHistory.txt`.

## se4data.py (scripts/, run with `python3 -I`)

```
se4data.py list  FILE [Field=text ...]         record names, filtered by substring
se4data.py show  FILE NAME                     one record, every field
se4data.py fields FILE                         field names and counts
se4data.py diff  MOD_ROOT [--detail]           per file: same / new / removed / changed vs vanilla
se4data.py check MOD_ROOT                      ERROR / WARN / NOTE list (see below)
se4data.py tree  MOD_ROOT [GROUP]              techs by group: max, cost, needs, unlocks; dead ends
se4data.py gather NOTES_DIR BUILD_ROOT [--detail]   game-format records in design notes not in the build
se4data.py merge  NOTES_DIR BUILD_ROOT OUT_ROOT     new build: vanilla, old build over it, notes' records added
```

`--base GAME_DIR` changes the vanilla folder. `check`: ERROR = missing data file, tech or ability
that does not exist, empty or miscounted requirement lines; WARN = duplicate names (several
released mods have them; check in game which one wins), a requirement above the tech's maximum
(never unlocks); NOTE = locked behind a max-level-0 tech. Calibration: vanilla and Devnull 1.71
give no problems; Proportions 1 error, Pirates & Nomads 7, CarrierBattles 1.

## Example mods (`se4/Extras/`)

Unzip into the scratchpad, never into the install: Devnull 1.71 (cleanest, a good reference for
format), Carrier Battles 1.2, Pirates & Nomads 3.2, Proportions 3.0.4, Imperium Verus, Colony
Tech Mod 2, Fyron's Quadrant Mod, Atrocities races, TDM ModPack (an .exe), plus tools (weapon
stats, tech gridder, components repair tool, map stats, autohost). `ModDescriptions.txt` says
what each does.

## Workflow

1. Work in the workspace copy, never in the install. For the WMD mod see `wmd.md`. Don't fill
   in design decisions (which tech unlocks a weapon, costs) on the user's behalf: list them for him.
2. Edit records; keep counts in step; one `Family` per component line.
3. `check` (fix every ERROR), `diff` against the previous build, `tree` for dead ends.
4. Build with `merge` into a new `_Builds/Version N.../` folder; it writes MERGE_LOG.txt (every
   record added and its source note; where the build's version was kept; which of two
   conflicting notes was used - the newer file). Records already in the old build are never
   replaced: the build's copies are the refined ones (the notes still have placeholder pic
   numbers and roman numerals). Then `check` and save it as CHECK.txt next to the log.
5. Play-test only with the user's go: he backs up and installs the build over the game's files (or
   picks it in the mod loader). Report that it is untested until it loads in a game.

## Related skills
learn-to-mod (generic method; its twin learn-to-play), se4-guide (playing), user-todo (WMD decisions).
