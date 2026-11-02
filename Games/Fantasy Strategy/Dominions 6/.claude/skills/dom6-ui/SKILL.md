---
name: dom6-ui
description: Drive the running Dominions 6 window (through the generic game-ui guard: screenshots of the game only, clicks, drags, scrolls, hotkeys, typing, waits while the user is busy). Has a map of the start menu screens with hotkeys and click coordinates; mods.py, which enables and disables (loads and unloads) mods and reads which are on; and vision.py, which reads screen text (Tesseract via NormCap), sorts the screen into windows, bars, text, buttons, sprites, icons and the 3D world (sky, water, land, trees), finds saved image templates at any scale and records short clips. Use when the user asks Claude to use, look at or operate Dominions 6 itself: set up a game, enable or disable mods, design a pretender in the game's screen, save an AI template, error-check a mod in game, browse preferences, check what a screen shows, read text off a screenshot, or find a sprite or icon on screen.
---

# Driving the Dominions 6 game window

The guard, input and screenshots are the generic **game-ui** skill (project root,
`.claude/skills/game-ui/scripts/gameui.py`; its SKILL.md has every command, the coordinate rules
and the safety rules). Its window class defaults to Dominions 6 (`dom6_amd64`), so for Dominions
just run it. `scripts/dom6ui.py` here is a stand-in that runs gameui.py, so every older command
(`python3 -I dom6ui.py seq ...`) and `import dom6ui` keep working.

```
dom6ui.py find | shot [--full] [--grid] | zoom X Y W H | click X Y | key question | type "text"
dom6ui.py seq "key c" "wait 1200" "key question" "wait 800" "shot --full"
```

What this skill adds for Dominions: `vision.py` (the screen reader below, with the game's own
font), `textmatch.py` (checks that a box says a given string, rendered in the game's font),
`mods.py` (the Mods screen), the Dominions templates and test shots, and the screen map. Scripts in
other dom6 skills put `dom6-ui/scripts` on `sys.path` and `import vision` first: vision.py adds
game-ui's scripts to the path (for `session` and `gameui`).

## Seeing the screen (`vision.py`)

**Look before clicking: `vision.py scene` gives every element on the screen, organised.**

```
vision.py scene [IMAGE] [--frames N] [--out PNG] [--json] [--no-text]
vision.py read IMAGE X0 Y0 X1 Y1 [--dark]              # the text in a box (Tesseract)
vision.py find IMAGE NAME [NAME...] [--box X0 Y0 X1 Y1] # where saved templates appear
vision.py add NAME IMAGE X0 Y0 X1 Y1 [--kind sprite|icon|ui|text] [--note TEXT]
vision.py templates                                     # the template library (templates/)
vision.py video OUT.gif [--n 16] [--gap 0.25]           # a short clip of the game
```

- With no IMAGE, `scene` and `video` grab the game under the guard (wait for idle, game in
  front only, focus given back). `--frames 16` grabs a burst first: **what moves is the 3D world**
  (the menu camera flies; the battle replay behind the menu), what stays is UI and text. Use it on
  the main menu: one still frame misses buttons whose edges blend into the backdrop.
- Output tree: `windows` (found by the tan frame round every window, and by the flat dark-grey
  panel), each with `bars` (header and group bars, with their title), `text` (lines with their
  reading, score and word boxes) and `sprites` (sprites and icons); `floating` text and sprites
  outside windows (main-menu buttons, banners, the version line); `background` shares of sky,
  water, land, trees and the biggest tree/object boxes.
- How it tells things apart: UI panels are flat, colourless grey; the frame is a tan strip with
  dark panel 10 px inside; text is grey/white/black (low saturation), sprites are coloured;
  candidates are cut from an edge mask by recursive row/column cuts (so an icon column and a
  name column split apart); a candidate that Tesseract cannot read becomes a sprite or icon.
- **Text reading: Tesseract 5 from the NormCap flatpak** (`com.github.dynobo.normcap`, installed
  by the user; run as `flatpak run --env=TESSDATA_PREFIX=/app/share/tessdata
  --command=tesseract com.github.dynobo.normcap`). `vision.ocr(img, boxes)` reads all boxes of a
  screen in one call (~1 s): each box is turned dark-on-white, enlarged 3x and stacked. It read
  30/30 nation names and 34/34 Mods rows exactly. `vision.closest(text, names, limit, margin)`
  snaps a reading to known names (margin rejects v2.1 vs v2.10 ties). Without NormCap, a pure-PIL
  glyph reader (`vision.read`) is used: about half the lines exact, every nation name snaps.
- Text and sprites change size (text-size preference, map zoom): the reader does not assume a
  size, and `find` tries each template at the scale that fits each element (0.9-1.1x of it, and
  1x), sliding a few pixels, then to the pixel. Score = mean colour difference over the
  template's own pixels (black = transparent): 0 = identical, under ~0.06 = the same picture.
- Templates: `templates/<name>.png` + `index.json` (vision.py's `TEMPLATES`; set `UI_TEMPLATES` to use another folder). Saved: the nine magic path icons of the
  design screen (`path_fire` ... `path_blood`). Add one with `add` from any screenshot.
- Test screens: `tests/shots/*.png` (full size): main menu (hills, underwater), Game Tools,
  era, nation list, nation overview, design, form chooser and tooltip, bless list, Mods.
- The world behind the menus changes per launch (hills, sea floor), so never key on it.

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

## Safety rules (from the user; follow them always)

- The user is often at the computer while Claude works ("I am doing stuff", "I might accidentally
  press a hotkey"). The tool therefore waits until keyboard and mouse have been idle 4 s
  (`--idle S`) before taking focus, refuses screenshots unless the game is the active window, and
  drops the rest of a `seq` if the user switches window ("STOPPED: ..."). When stopped, look at a
  fresh shot before going on: the user may have changed the screen.
- **Never touch ongoing games.** Do not press Play game, Delete game or Return on the Continue Old
  Game list, do not use Network > "Open Previous Connection", Enter Game Lobby or connect to a
  server, never end a turn. Viewing the list is fine.
- Never upload anything (Mods > right-click > "Upload to Steam Workshop", Map Editor upload).
- Never change Preferences or enable/disable mods unless the user asks for that change; then
  note what was enabled before (`mods.py status`).
- A new game is written to `~/.dominions6/savedgames/<name>/` as soon as the god is confirmed
  ("All praise X / Ok"), before Game Settings. Use a test name that no save has
  (`ls ~/.dominions6/savedgames/`), and if the user did not want the game, back out and delete only
  that new folder after checking its contents and timestamp.
- Never capture or click other windows. When finished, give focus back to the user's terminal
  (`wmctrl -l` to find it, `wmctrl -i -a ID`), or as asked.

## Gotchas

- Other apps, screenshot aspect, the recording hook and the screenshot folder: see game-ui.
- `?` opens a screen's hotkey list, except in text fields, where it types a `?` (game name, god
  name, password): remove it with `key BackSpace`. Not every screen has a list (Map Settings and
  Preferences have none).
- Close a hotkey list with its **Exit** button. Escape inside some lists closes the screen below
  too.
- Escape is "back" on most screens; on the main menu letters open menus directly, so a stray key
  can open the wrong menu. Look at the shot.
- Hovering shows a tooltip at the bottom centre (the form's name and cost, "Enable this mod,
  (right click) info").
- Right-click is "info" almost everywhere (a pretender form, a mod, a unit).
- **Click on the text or the sprite**, not on the blank part of a list row or a form cell: the
  game ignores those clicks (short nation and bless names end well before x 960).
- `click` glides the pointer in and holds the button 150 ms: a pointer that jumps straight onto
  a row sometimes does not register.
- Escape in the form chooser does not cancel: the design keeps the hovered (or first) form.
  Drop an unsaved tools-mode design with the design screen's Cancel.

## Screen map (window 1920x1044; full-size coordinates; version 6.37)

The menus are drawn centred, so on another window size measure again with `shot --grid`.

**Main menu**: Create World (920,402), Continue Old Game (920,448), Network (920,492), Tools &
Manuals (920,538), Mods (920,582), Preferences (920,628), Quit (920,674).
Hotkeys: a random map creator, c create world, e map editor, g game tools, h hide/show menu,
l continue old game, m mods, n network, o network lobby, p preferences, q quit, r new random
background world, t show a tip. (Help Exit at 959,687.)

**Create World**, in order (Cancel or Escape goes back one step):
1. *Map Settings*: size Small (622,121), Medium (622,150), Large (622,178), Enormous (622,207),
   Loaded map (622,243); main-world layouts in two rows at y 354 and 428, x 665/780/895/1010/1124/
   1238; underground layouts at y 574; water provinces (760,693), Rivers (620,724), East/West wrap
   (620,757), North/South wrap (620,785); Ok (959,826), Cancel (959,867).
2. *Enter game name*: text field, Ok (959,473).
3. *Select Era*: Early (665,202), Middle (665,373), Late (665,531); Ok (959,689), Cancel (959,720).
4. *Choose Participants*: rows start at y 336, 28 px apart; nation column x 558 (click opens the
   nation picker), Player x 945 (Human / AI level), AI type x 1081. Add new player (598,507),
   Disciple Game (531,539), Ok (959,574), Cancel (959,605).
   Hotkeys: n add player, backspace remove last, H all human, A all AI, R remove all, L / W
   random land / water nations, 0 no teams, 2/3/4 equal teams, + / - AI difficulty, esc back,
   ret done. Help Exit (960,716).
   *Nation picker*: scrolling list, rows 28 px apart from y 73, hover shows the description; at
   the bottom <Random>, <Random land nation>, <Random water nation>, <None>, Cancel; Escape closes.
5. *Nation overview* (for the human nation): Ok (959,898).
6. *Design Pretender*: Password (698,144), Select Physical Form (741,171); magic icons at y 248:
   F 711, A 765, W 817, E 868, S 920, D 973, N 1024, G 1077, B 1130 (left click +1, right click -1);
   Add Bless Effect (723,423); dominion icons at y 527: candles 710, order 772, productivity 823,
   heat 877, growth 925, luck 980, magic 1033 (left +, right -); Imprisonment Awake (665,659),
   Dormant (665,687), Imprisoned (665,716); View Nation Description (795,764); Ok (959,802).
   These positions move down as blesses are added (four blesses pushed Ok to 959,938): take a
   shot first. Design points left are at the top.
   Hotkeys: ctrl-l load design, ctrl-s save design, ctrl+shift-s save as AI template mod data,
   a add bless, b view all blesses, i/F forgeable items, n nation description, p physical form,
   r random pretender, s/F5/C researchable spells, t templated pretender, x repeat last bless.
   Help Exit (959,673).
   *Select Physical Form*: grid by starting dominion (4, 3, 2, 1 from the top), cells 122 px wide
   from x 403, rows near y 187, 318, 452, 568, 700; hover = name and cost, left click = choose,
   right click = full stat page (Exit at the bottom). Cancel (959,786).
7. *Enter the name of your God*: text field (a random name is filled in), Ok (959,458),
   Cancel (959,490). Then "All praise X" Ok (959,474): **the save folder now exists.**
8. *Game Settings*: tabs World (840,110) and Thrones (1075,110). World: starting provinces,
   independents strength, site frequency, resource multipliers, events, story events, score
   graphs, diplomacy, hall of fame, mercenary and global slots, artifact and legendary rates,
   human AI level, research speed, random start research, renaming, master password, cheat
   prevention. Thrones: victory type, cataclysm and its turn, ascension points needed, level 1-3
   throne counts. Ok (959,900) starts the game; Cancel (960,766 on Thrones, 959,932 on World)
   goes back to Participants. Hotkeys: ret ok, esc cancel, ctrl+l load saved settings, ctrl+s
   save settings. Help Exit (959,516).

**Continue Old Game** (view only): list of saves with nation flags, rows from y 258 about 28 px
apart; Play game, Delete game, Cancel (959,652). Hotkeys: n sort by name, d sort by date, ret
play, del delete, esc exit. Help Exit (958,552).

**Network**: Open Previous Connection, Enter Game Lobby, Start Game Server, Connect to a Game
Server, Cancel. Do not use any of them without the user.

**Tools & Manuals (Game Tools)**: Create a Pretender God (840,294), ... for disciple game (840,322),
Create a Disciple (840,350), View Created Pretenders (840,380), Map Editor (840,466), Random Map
Creator (840,494), Manuals & Introduction Videos (840,584), Open User Data Directory (840,612),
Exit (960,662). No hotkey list.
*View Pretenders*: saved designs by era with <del> (do not click), Exit (960,742).
*Map Editor menu* (e): New map, Load map, Upload map to Steam Workshop (never), Exit. Loading a map:
see the dom6-maps skill. After every call focus goes back to the window that was in front, or to
Claude's terminal ($WINDOWID) when the app itself was in front (a newly opened app grabs focus).

**Mods** (m), title "Mod Preferences": one list of every installed mod (rows ~26.9 px apart from
y 71, names from x 777, banner at x 655-752), scroll with the wheel (one notch ~2.6 rows); left
click on the name toggles a mod (green tick at the right when on; tooltip "Enable this mod" /
"Disable this mod, (right click) info"); at the bottom "Disable all mods (N enabled)" (grey when
none) and Exit; Escape leaves and saves. Right click opens info: description, Upload to Steam
Workshop (never),
**Error Check** (960,512) → "Mod seems ok, crc ..." or the errors, with Refresh and Ok
(959,504); Exit. Escape leaves the list. Error Check is the game's own parser: use it to confirm
`check_dm.py` and dom6-modinspector results (dom6-modding skill).

**Preferences** (p): tabs Gameplay (775,130), Graphics (895,130), 3D (1020,130), Sound (1137,130);
checkboxes; Exit (959,679). View only unless asked. No hotkey list.

## Workflows

- **Look first.** `find`, then `shot`. If the game is not on the main menu, ask before backing
  out of anything that might be a running game.
- **Pretender in game**: the **dom6-pretender-ingame** skill does this whole job by script
  (`build_god.py`: nation, form, paths, dominion, scales, blesses, points check, name, save).
  By hand (with dom6-pretender): design it with `pretender.py build`, then set the
  same chassis, paths, dominion, scales and blesses in the Design Pretender screen and compare the
  points left with the script; the game's numbers win. Ctrl+S saves the design (shows in Game
  Tools > View Created Pretenders); Ctrl+Shift+S writes the AI template mod data for a mod's
  `#newtemplate` (dom6-modding). Design from Game Tools > Create a Pretender God to avoid making a
  game.
- **Mod check in game**: Mods > find the mod > right click > Error Check; report the message.
  Nothing is enabled or changed by this.
- **Playtest setup** (dom6-play): only when the user asks for a new game. Create World with a new
  name, pick the nation in Participants, finish the pretender, review Game Settings, and leave the
  first turn to the user unless told otherwise.
- **Finish**: return the game to where it was (usually the main menu) and give focus back.
