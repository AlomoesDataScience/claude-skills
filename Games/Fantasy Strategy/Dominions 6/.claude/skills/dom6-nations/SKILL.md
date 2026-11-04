---
name: dom6-nations
description: Read Dominions 6 nations from the running game's own nation info screens (right-click a nation in Select Nation) into the knowledge base, one markdown and JSON file per nation (description, National Features - race, military, magic, priests, scales and blesses, buildings - commander, unit and site counts, a picture of the screen, and the inspector's recruit lists for vanilla nations), and build the nations overview table. Works for mod nations whose mod is enabled. Uses dom6-ui (guarded input, vision.py OCR), dom6-knowledge (where the files go) and dom6-inspector. Use when the user asks for a nation overview or nation files, wants to know what the game says about a nation (description, features), wants all nations of an era read, or wants a mod nation's in-game info checked.
---

# Nation files from the game

`scripts/nations.py` (run from this folder with `python3 -I`) drives the game, reads each
nation's info screen and writes it to **dom6-knowledge**'s `nations/` folder.

```
nations.py read ERA NATION [NATION...]   # EA / MA / LA; part of the name is enough ("Ulm")
nations.py read ERA --all                # every nation the game lists in that era
nations.py parse IMAGE [--name "Ulm, Forges of Ulm" --era MA] [--save]   # a saved screenshot
nations.py overview                      # rewrite nations/OVERVIEW.md from the nation files
nations.py list                          # what has been read
```

Output: `dom6-knowledge/nations/<ERA>/<slug>.md` + `.json` + `img/<slug>.jpg` (half-size
picture of the info screen), and `dom6-knowledge/nations/OVERVIEW.md` (a table per era: race,
military, magic, priests, scales and blesses, with links). The full-size shots of the last run
stay in `~/.cache/dom6ui/nation_<slug>.png` for re-parsing.

## How it works

1. Starts from the **main menu or Game Tools** (anything else: stop and ask). Goes Game Tools >
   Create a Pretender God (840,294) > era radio > Ok > Select Nation. No game is made.
2. Reads all list rows with one OCR call, right-clicks each wanted nation **on its text**: the
   nation info window opens (title tab with the name; description on parchment; "National
   Features" bar; Race, Military, Magic, Priests, Scales & Blesses, Buildings; then rows of
   Commanders, Units and Sites sprites; Ok).
3. Parses it with dom6-ui's `vision.py scene` (Tesseract): description = lines above the
   National Features bar, features = `Key: value` lines (a line without a key continues the one
   before), sprites grouped in rows; each row's label ("Commanders", "Units", "Sites") is read
   from just above it, a row without a label continues the section before (long lists wrap).
   Pike tips and plumes that stick out of a sprite are merged into it; the two touching site
   icons are split by their square shape.
4. Return closes the info window (the list stays where it was; checked). Scrolls 3 notches per
   page until the list stops moving. Escape goes back to Game Tools, Exit (959,662) to the main
   menu if that is where it started.
5. Vanilla nations: the nation number comes from the pretender calculator's nation list, and
   the inspector's page (commanders, units, capital-only, heroes, pretenders, start sites,
   national spells) is added. Mod nations: the number and .dm are found by `#selectnation` +
   `#name` in the installed mods.

Checked: Ulm (MA) 12 commanders / 17 units / 2 sites = the inspector's 8+4 / 16+1 / 2;
Sauromatia (EA) 12/12/4 = 9+3 / 7+5 / 4. The screen also shows terrain recruits (swamp,
underwater, forest...), so many nations show more than the inspector's regular + capital-only
lists (Ur EA: 18/14 on screen). Riders whose lances touch are split on the 61-px sprite grid.

## Limits

- OCR slips remain at line starts next to the parchment border (a lost "The", "When n men").
  The description is "as read": say so when quoting it. The picture in `img/` is the reference.
- The info screen sits over the animated world behind the menu; two reads of the same nation
  can differ by a word. Re-run a nation if its file looks wrong.
- A mod nation only shows when its mod is enabled in game (dom6-ui `mods.py status`; enabling
  is the user's decision).
- Site counts are sometimes off by one (touching icons are split by shape). The sprite counts
  are what the screen shows; names of the units are not on this screen
  (right-click a sprite for its stat page; for vanilla the inspector lists are in the file).

## Standards (audit 2026-11-03)
- **Modded games:** numbers here are vanilla - check the mod first (dom6-scbm for SCBM; mod-docs).

## Related skills
dom6-knowledge, dom6-inspector, dom6-pretender, dom6-play.
Also (2026-11-03): dom6-best-by-purpose, dom6-path-fire ... dom6-path-glamour, dom6-holy.
