---
name: game-ui
description: Drive any running game (or app) window on the user's X11 desktop - screenshots of that window only, clicks, drags, scrolls, hotkeys, typing - through a guard that waits while the user is busy and stops if they switch windows; or in the background on a virtual screen of its own (bgplay.py, the user's input lockable); pick the window with UI_WMCLASS / UI_WMTITLE. Also reads text off screenshots and scanned PDFs with Tesseract (ocr.py: English, Japanese horizontal and vertical, any downloadable language). Built while learning Dominions 6 (dom6-ui adds its menu map and font tools on top). Use when Claude has to look at, operate or read the screen of any game or app the user has open - a new game being learned, an emulator, a Japanese game that needs its screen read and translated, OBS - or OCR a scanned manual.
---

# Driving a game window (any game)

`scripts/gameui.py` drives a window the user already has open (it never starts a game). Run it with
`python3 -I`; it needs system Python with PIL, the X libraries (libX11, libXtst, libXss), `wmctrl`,
`xprop` and `xwininfo`.

```
UI_WMCLASS=<class> gameui.py find                # window id, size, focused or not
gameui.py shot [--full] [--grid]                 # PNG path; Read it. Half size unless --full
gameui.py zoom X Y W H [--scale 2]               # crop of the last full shot, for small text
gameui.py seq "key c" "wait 1200" "click 400 300" "wait 800" "shot --full"
gameui.py click X Y [--right] [--double] [--hold MS]
gameui.py move X Y | drag X1 Y1 X2 Y2 [--slow] | scroll up|down N [--at X Y]   (--slow: Unity apps)
gameui.py key Escape | key ctrl+s | key a b c    # X keysym names (question, Return, F5, plus)
gameui.py type "text"
```

- **Pick the window:** `wmctrl -lx` lists windows; `UI_WMCLASS` is the class before its first dot
  (`obs`, `thunar`, a Wine game's exe name). `UI_WMTITLE=<part of the title>` picks one window of
  the app (a dialog is its own window and takes focus). **There is no default window** (it used to be
  Dominions', and another game's input went there - the user, 2026-11-01): set `UI_WMCLASS`, or give the
  game folder a `.claude/game-ui.json` (`{"wmclass": "crawl"}`), found by walking up from the script
  or the current folder. Dominions' folder has one (`dom6_amd64`), so the dom6 tools still just work.
- Coordinates are **full-size window pixels** (0,0 = top-left of the drawing area). A half-size shot
  shows them halved: double what you read, or use `--grid` (labels are full-size). Keep the
  window's aspect when shrinking (Dominions' 1920x1044 is not 16:9: a squashed copy put y ~3% off).
- Prefer `seq`: one focus change for many steps; focus and pointer go back to the user's window
  afterwards. Each step re-checks that the game is still the active window. Input commands end with
  a screenshot (`--wait MS` before it, `--no-shot` to skip): read it after every step that changes
  the screen, never chain blind clicks.
- `click` glides in and holds the button 150 ms (a jump straight onto a button sometimes misses).
- Screenshots go to `~/.cache/game-ui/<class>/` (`gameui.OUT`, one folder per game); OBS's
  gameplay-session flag is `~/.cache/game-ui/recording` (`gameui.FLAG`).
- `scripts/session.py`: a guarded session object for scripted tools: `session.run(work)` waits for
  idle, focuses, runs `work(g)` with `g.grab()`, `g.burst(n, gap)` (a short clip), `g.click(x, y,
  right=, mods=("alt",))`, `g.key(...)`, `g.type(...)`, `g.scroll(...)`, then hands focus back;
  `Stop` is raised when the user takes over. `says`/`on_text` match Dominions' font (they import
  dom6-ui's textmatch, so only work from dom6 scripts).

## Playing in the background (`scripts/bgplay.py`)

The user's ask (2026-11-01): play without taking over his desktop. `bgplay.py` runs a game on its own
virtual X screen (Xephyr, display :5): Claude's keys, clicks and screenshots go there only, so no
focus stealing, no idle wait, and nothing he types reaches the game.

```
bgplay.py start                      # virtual screen + "Claude game screen" window; locked by default
bgplay.py launch flatpak run org.develz.Crawl
bgplay.py steam 1368870              # a Steam game onto the virtual screen (launch option needed, below)
bgplay.py windows | shot [--full] | zoom X Y W H
bgplay.py seq "key o" "wait 2500" "type abc" "click 400 300" "shot --full"
bgplay.py lock | unlock | locked     # lock: The user's mouse/keyboard can't touch the game (he can watch)
bgplay.py stop
```

- Lock = the Xephyr window's own mouse and keyboard devices disabled (`xinput`); Claude's input
  uses the XTEST devices, so it still works. `unlock` lets the user play along; toggle any time.
  Locked is the default and must hold (the user, 2026-11-02, "I have access"): the first lock right
  after `start` used to fail silently; now `lock` retries until both devices are off, writes
  `~/.cache/game-ui/bg5/locked`, and the keeper re-locks within 4 s if anything re-enables them.
- No window manager on the screen: keys go to the window under the pointer, so bgplay parks the
  pointer on the biggest window before keys. Coordinates are virtual-screen pixels.
- **Steam games** (2026-11-02, FoG II Medieval): Steam starts the game itself, so the game needs this
  Steam launch option (Properties > General > Launch Options; open it with
  `steam steam://gameproperties/APPID`, type it with gameui, then check the box's start and end):
  `env $(cat "$HOME/.cache/game-ui/steam-env" 2>/dev/null) %command%`
  No file = the game runs on the user's screen as always. `bgplay.py steam APPID` writes
  `DISPLAY=:5 PROTON_USE_WINED3D=1` there, starts the game, and removes the file when the first
  window appears (children of the launcher inherit it).
- **Why WineD3D:** Xephyr has no DRI3, so Vulkan can't present ("Could not find both graphics and
  present queues"); DXVK games crash right after loading (FoG II died at "TS: UILoaded"). With
  `PROTON_USE_WINED3D=1` Proton draws through OpenGL on llvmpipe: software, slow, fine for turn-based
  games. `start --glamor` does not help. No gamescope installed.
- Other Proton/umu games launched outside bgplay still open on the real desktop.
- `show` brings the window back; a keeper (started with `start`) repaints it, since with xfwm4's
  compositor Xephyr shows what was behind it after being hidden.
- Fine for 2D games and roguelikes; 3D games get software rendering there (slow), fine when
  turn-based. Set the game to windowed at a size that fits the virtual screen (FoG II: 1600x900 in a
  1600x990 screen) through the game's own settings.

## Waiting, held keys, hovering (bgplay seq steps and hoversheet.py)

- `mark` then `waitchange [N]`: whole-screen change against the mark, then settle (loads, turns).
- `hold KEY MS`: a key held down (3D camera keys act only while held). `scroll up|down N [X Y]`.
- `hoversheet.py --bg X,Y X,Y ...`: hover each point, find the tooltip by difference, OCR it, one
  contact sheet. Setup, GPU and UI parsing method: the **game-setup** skill.

## Is the game working? (`scripts/gamecheck.py`, the user's rule 2026-11-02)

Assume a freshly launched game is NOT working until shown otherwise, and check in periodically:
30 s to 1 min tells. Expect popups (notices, error boxes, launchers): they are separate windows.
```
UI_WMCLASS=steam_app_1368870 gamecheck.py --secs 60 --every 15 --hover X Y   # desktop window
gamecheck.py --bg --secs 60 --every 15 --hover X Y                           # bgplay screen
```
Reports GONE (window gone), POPUP (more than one window of the class), BLANK (flat picture), FROZEN
(hovering a button changes nothing), OK; then a verdict. When not OK, Read the last shot and the
game's own log (FoG II: `Documents/My Games/FieldOfGloryMedieval/error.log` in its Proton prefix).

## Reading text (`scripts/ocr.py`)

```
ocr.py image SHOT.png [--box X0 Y0 X1 Y1] [--lang eng|jpn|jpn_vert|eng+jpn] [--psm 6|7] [--scale 3] [--dark] [--tsv]
ocr.py pdf MANUAL.pdf [OUT.txt] [--lang eng] [--dpi 300] [--first N --last M]   # scanned manuals
ocr.py langs | ocr.py getlang LANG [--fast]
```

- Tesseract 5 from the NormCap flatpak (`com.github.dynobo.normcap`, the user's install), with its
  data in `~/.var/app/com.github.dynobo.normcap/data/tessdata` (eng copied from the app, jpn,
  jpn_vert and osd from tessdata_best, added 2026-10-29). Other languages: `getlang`.
- Game text: crop to the text (`--box`), `--scale 3`, `--dark` for light-on-dark, `--psm 7` for a
  single line, `--psm 6` for a block. Japanese output has Tesseract's spaces between CJK
  characters removed.
- **Japanese games** (the user's Gihren's Greed has no English): read the screen with
  `--lang jpn` and translate it yourself; keep a glossary of the game's menu words in the game's
  skill so later screens are read faster. Test: rendered menu words (生産 開発 作戦 外交 ターン終了)
  came back exact.
- Dominions has a richer reader (dom6-ui's `vision.py`: element tree, its own font) - use that one
  for Dominions screens.

## Safety rules (from the user; follow them always, in every game)

- The user is often at the computer ("I am doing stuff", "I might accidentally press a hotkey"):
  the guard waits until keyboard and mouse have been idle 4 s (`--idle S`), refuses screenshots
  unless the game is the active window, and drops the rest of a `seq` if the user switches window
  ("STOPPED: ..."). When stopped, take a fresh shot before going on. Don't fight for focus. The guard
  waits up to 3 minutes for idle: give scripts a timeout over 180 s.
- Never touch the user's ongoing games, network play, accounts or uploads (Steam Workshop and the
  like), and never change preferences or settings unless asked.
- Never capture or click other windows. When finished, give focus back to the user's terminal
  (`wmctrl -l`, `wmctrl -i -a ID`), or as asked.
- New-game saves: use a test name no save has, and only delete what you made (check contents and
  timestamp first).

## Learning a new game's screen

See `learn-to-play` for the method. Per game, record in its own skill (in the game's folder under
the genre folder): window class, window size, screen map with click points and hotkeys, which keys
are dangerous (end turn, quit, delete), and a template/glossary of what is on each screen.

## Related skills
game-setup (getting a game running), map-camera and photo-map (camera and photos on bgplay), learn-to-play, stream-panel, obs-record

## Whose turn is it? (turnwait.py)
Turn-based games: never guess from timing alone. Find the on-screen sign of "my turn" (an End Turn
button that is replaced by an enemy-turn banner, a turn counter, a side colour) by photographing the
screen every ~1.5 s through one whole enemy turn after End Turn - then cut a reference of it.
- `turnwait.py make REF.png SHOT.png --box ...` (from a screenshot on my turn)
- `turnwait.py wait REF.png --box ... --mask ... --min 8` right after confirming End Turn (the user: assume the
  AI turn takes 5-10 s); prints MINE, then take the turn's photos. `check` = one look; `test` = score frames.
- Mask anything inside the box that changes on my turn too (turn number).
- The AI turn may move the camera: park the mouse on a fixed UI panel with no tooltip (idle-view). Not
  outside the game window: the game keeps the last hover position.
FoG II: box 1385 30 1590 115, mask 1435 42 1540 92, ref in the game folder ui/turn_mine.png.

