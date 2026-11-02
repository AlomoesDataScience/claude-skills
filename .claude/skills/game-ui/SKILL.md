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
bgplay.py windows | shot [--full] | zoom X Y W H
bgplay.py seq "key o" "wait 2500" "type abc" "click 400 300" "shot --full"
bgplay.py lock | unlock | locked     # lock: The user's mouse/keyboard can't touch the game (he can watch)
bgplay.py stop
```

- Lock = the Xephyr window's own mouse and keyboard devices disabled (`xinput`); Claude's input
  uses the XTEST devices, so it still works. `unlock` lets the user play along; toggle any time.
- No window manager on the screen: keys go to the window under the pointer, so bgplay parks the
  pointer on the biggest window before keys. Coordinates are virtual-screen pixels.
- Proton/umu games ignore the virtual screen and open on the real desktop.
- `show` brings the window back; a keeper (started with `start`) repaints it, since with xfwm4's
  compositor Xephyr shows what was behind it after being hidden.
- Fine for 2D games and roguelikes; 3D games get software rendering there (slow or broken), so
  those still use the guarded desktop route above.

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

See `learn-a-game` for the method. Per game, record in its own skill (in the game's folder under
the genre folder): window class, window size, screen map with click points and hotkeys, which keys
are dangerous (end turn, quit, delete), and a template/glossary of what is on each screen.
