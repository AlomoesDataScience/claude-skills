---
name: dom6-ui
description: "Drive the running Dominions 6 window through the game-ui guard: menus, game setup, mods, pretenders, hotkeys, font tools. Use when asked to use, look at or operate Dominions 6 itself."
keywords: "generic, screenshots, clicks, drags, scrolls, typing, waits, while, busy, has, map, start, menu, screens, click, coordinates, enables, disables, loads, unloads, reads, vision, screen, text, tesseract, normcap, sorts, windows, bars, buttons, sprites, icons, world, sky, water, land, trees, finds, saved, image, templates, scale, records, short, clips"
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

## Virtual-screen commands (dom6bg.py - the default way to look at a game, 2026-11-03)
The user: "we're using a virtual window, we should be using virtual commands." The FoG II order.py pattern:
one command = one checked action, result read back, mouse parked. READ ONLY (no orders/recruits/End Turn).
`scripts/dom6bg.py look | read REGION.. | capital | zoom out|in N | mapshot [N] | messages | goto TEXT |
exitdialog | battle NAME | park`. Named regions (title, resources, commanders, province, sites, scout,
hovername, dialog, replaylog) live in Dominions' `.claude/game-ui.json`, measured at 1912x1000, so
`bgplay.py read province` works from the Dominions folder. Prefer `read` over screenshots for text.
Never Esc to close a dialog (Esc = Options): find its Exit by OCR (`exitdialog`).

## Dominions on Claude's virtual screen (bgplay, tested 2026-11-03)
The user's own copy must be closed first. Then, from the install folder (~/.local/share/Steam/steamapps/common/Dominions6):
`bgplay.py start --size 1912x1000 --unlocked --cursor` and `bgplay.py launch ./dom6.sh -w -r 1912 1000 --softmouse`
(manual launch options: -w window, -r size, --softmouse draws Dominions' own pointer - without it the pointer is
invisible in Xephyr). 1912x1000 fits the user's 1920x1080 desktop with the window frame; move it to the top-left.
Unlocked = the user can click in it (e.g. to log in). **Never take screenshots while he types a password**; wait for his
word. Don't restart it while he's using it. dom6 scripts on this screen: run them with DISPLAY=:5; coordinates
calibrated at 1920x1044 may be off by a few pixels at 1912x1000 - check on the first shot.

## Interface lessons that apply here (game-ui "Interface lessons", from FoG II - checked against Dominions)
- Hover before acting: tooltips sit in the bottom bar (dom6-tooltips); hover the centre of text, not icons.
- Forecast vs commit: in Dominions almost nothing commits until End Turn, but orders, recruits, research and
  gem transfers ARE changes - in the user's MP game look only (right-click views; left-click on the map = move).
- Popups: find the Exit by OCR of the popup's own bounds (`exitdialog`); stop loops when the screen stops changing.
- **Esc opens Options, not cancel** - close dialogs with their Exit; Return can open Army Setup.
- Verify every action with a fresh shot; leave the camera on the armies and the mouse parked (idle-view).

## Reference files (read the one the step needs)

| File | Holds |
|---|---|
| `reference/seeing-the-screen-vision-py.md` | **Seeing the screen (`vision.py`)** - Look before clicking: vision.py scene gives every element on the screen, organised |
| `reference/enabling-and-disabling-mods-mods-py.md` | **Enabling and disabling mods (`mods.py`)** - mods.py status                  # enabled mods, read from ~/.dominions6/dom6config (no input) mods.py install |
| `reference/screen-map-window-1920x1044-full-size-co.md` | **Screen map (window 1920x1044; full-size coordinates; version 6.37)** - The menus are drawn centred, so on another window size measure again with shot --grid |

## Related skills
game-ui (the generic guard and bgplay), dom6-tooltips, dom6-game, idle-view.
Also (2026-11-03): game-ui, dom6-map.
