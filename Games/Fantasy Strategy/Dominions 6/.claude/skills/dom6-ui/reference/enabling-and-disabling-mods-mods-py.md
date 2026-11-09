# dom6-ui - Enabling and disabling mods (`mods.py`)

Part of the dom6-ui skill; SKILL.md links here.

## Enabling and disabling mods (`mods.py`)

```
mods.py status                  # enabled mods, read from ~/.dominions6/dom6config (no input)
mods.py installed [TEXT]        # every mod the game lists, from disk, * = enabled (no input)
mods.py list                    # the game's Mods screen: every row and its tick
mods.py enable NAME [NAME...]   # tick ("load") these mods
mods.py disable NAME [NAME...]  # untick ("unload") these mods
mods.py only NAME [NAME...]     # exactly these on, every other one off
mods.py none                    # the "Disable all mods (N enabled)" button
```

- NAME: the list name (the .dm's `#modname`; a mod in `~/.dominions6/mods` shows as
  `Name  (local)`), the .dm file or folder name (`madscience`), or a part of the name only one
  mod has. Same-name mods (four "One Age vSCBM (6.30 Zemaitia)"; a local and a workshop "Trusty
  Research") must be told apart: `Name#2`, the full local name, or the .dm file name.
- **The user decides which mods are on.** Only change them when asked, run `status` first and
  tell the user what was on, so it can be put back (`only ...` / `none`).
- The game must be on the main menu. The script opens Mods (`m`), scrolls from the top, ticks or
  unticks rows by clicking on the name's text, checks each green tick, presses Escape back to the
  main menu and prints `status`. It stops if a row it is about to click does not read as that mod.
- An enabled mod has a green tick at x 1212-1255 of its row; an enabled mod with a banner shows it
  top-right on the main menu.
- The game writes the choice to `~/.dominions6/dom6config` **when the Mods screen is left**, and
  rewrites the file on exit, so edit mods through the screen, never the file, while the game runs.
  File format (strings XOR 0x4F, NUL-terminated): a few ints, the workshop folder, then a uint32
  count and per enabled mod its .dm file name and folder (local: the folder under
  `~/.dominions6/mods`; workshop: the item id).
- The list is sorted by `#modname` ignoring case, a local copy before the workshop copy of the
  same name. `mods.py` reads all visible rows with one OCR call (vision.py) and places them by
  that order; rows it cannot read get their place from the rows around them.
- The enabled mods apply to new games, the pretender tools and the map editor. Not tested: how
  they interact with continuing a saved game, so do not change them around an ongoing game.
