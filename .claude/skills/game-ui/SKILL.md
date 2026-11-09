---
name: game-ui
description: "Drive any game or app window on the X11 desktop or the background bgplay screen: shots, clicks, keys, typing, plus Tesseract OCR. Use when Claude must look at, operate or read the screen of a game or app."
keywords: "running, screenshots, drags, scrolls, hotkeys, through, guard, waits, while, busy, stops, switch, windows, virtual, input, lockable, pick, wmclass, wmtitle, reads, text, off, scanned, pdfs, english, japanese, horizontal, vertical, downloadable, language, built, learning, dominions, dom6-ui, adds, menu, map, font, tools, top, has, open, new, being, learned"
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

## Text before pictures (the user, 2026-11-09 - context-hygiene)
`bgplay.py text [X0 Y0 X1 Y1] [--find WORD] [--dark]` = OCR lines with their centre ("960,560  NEW GAME"):
find and click without a screenshot. Then `read REGION`; a picture only as a crop (`shot --box`) or the
half-size `shot`; `--full` only when the picture itself is the point. (ocr.py tsv fixed the same day: the
NormCap tessdata has no "tsv" config, so `-c tessedit_create_tsv=1` is used.)

## Waiting, held keys, hovering (bgplay seq steps and hoversheet.py)

- **`waitchange --until "TEXT" [--box X0 Y0 X1 Y1]`: READY when the target screen's text shows** (checked at once,
  so a screen already up counts) - use this for loads and turns. `mark` then `waitchange [N]` (change, then
  settle) is a fallback only: animated screens fool it (2026-11-03, `.claude/plans/fix-loading-checks.md`).
  Never pipe a wait through `tail`.
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

## Sharing the virtual screen with the user (Dominions, 2026-11-03)
- Size it to fit HIS desktop with the window frame (1920x1080 desktop: 1912x1000 fits); move it to the top-left.
- `start --cursor` draws the pointer; games with their own cursor may need their soft-mouse option (Dominions
  `--softmouse`). `start --unlocked` / `unlock` when he must click or log in; `lock` while Claude works.
- **No screenshots while he types a password** - wait for his word. Don't restart it while he is in it.
- Long jobs (replays, many steps) belong on the virtual screen: the desktop guard stops the moment he
  switches windows (a Dominions replay record died that way).

## Fast screen sweeps (Dominions province sweep, 2026-11-03: The user "Is there any way you can make this faster?")
- Don't start a driver process and an OCR per item. Build ONE `bgplay.py seq` per view with every
  click/wait/`shot --full` step, then OCR the saved shots afterwards in a thread pool (Tesseract is a
  subprocess; threads are fine), off the game. Verify each read (expected id in the text); wrong or unread
  items get a second pass with a longer wait. Province sweep: ~12 min -> a few minutes.
- Slow searches (resnap zoom range) narrow after the first good match; widen again only when a match fails.

## Detect changes before reading them (Dominions replay, 2026-11-03)
A slow reader in a capture loop loses what it is meant to capture: OCR of the round counter took 0.75 s per
grab, so rounds and log lines scrolled past unseen. When only "did it change?" matters, compare a cheap
signature (a thresholded mask of the text's pixels, hashed) and count changes; confirm a change on two grabs;
read the actual value now and then in a background thread to correct the count. Slow checks (is the battle
over?) run on a timer, not every loop.

## Which button does what - check the game, not memory (Dominions, 2026-11-03)
I planned province reads with left-clicks; in Dominions a left-click on the map MOVES the selected commander and
a right-click views the province (the user: "I believe it's right click, go check"). Before any click in a game
that isn't mine (an MP game, the user's save), re-read the game skill's click rules and its "looking without
changing anything" list, and prefer the read-only button. Write the answer into the game skill.

## Python libraries on this PC (2026-11-02, system packages - visible to `python3 -I`)
numpy, Pillow, scipy 1.11, OpenCV 4.6 (`cv2`: template/feature matching, resizing, blob and line
finding - used by map-measure resnap.py), scikit-image 0.22 (`skimage`: registration, peak/blob
detection, measuring - for later unit-figure counting). Write scripts so they still run without the
optional ones (try/except import, numpy fallback).

## Reference files (read the one the step needs)

| File | Holds |
|---|---|
| `reference/playing-in-the-background-scripts-bgplay.md` | **Playing in the background (`scripts/bgplay.py`)** - the user's ask (2026-11-01): play without taking over his desktop |
| `reference/reading-text-scripts-ocr-py.md` | **Reading text (`scripts/ocr.py`)** - ocr.py image SHOT.png [--box X0 Y0 X1 Y1] [--lang eng|jpn|jpnvert|eng+jpn] [--psm 6|7] [--scale 3] [--dark] [ |
| `reference/interface-lessons-from-field-of-glory-ii.md` | **Interface lessons from Field of Glory II (battle 2, 2026-11-02/03) - apply in every game** - Hover before acting |
| `reference/whose-turn-is-it-turnwait-py.md` | **Whose turn is it? (turnwait.py)** - Unreliable (the user, 2026-11-03: it "works funky" in FoG II; not yet diagnosed) |

## Related skills
game-setup (getting a game running), map-camera and photo-map (camera and photos on bgplay), learn-to-play, stream-panel, obs-record
