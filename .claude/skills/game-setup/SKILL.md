---
name: game-setup
description: "Get a game running properly for Claude (bgplay, Steam launch options, windowed mode, GPU, logs) and parse its UI by hovering every element. Use when launching a game first time or when it lags, crashes or shows black."
keywords: "getting, parsing, before, real, play, run, graphics, locked, screen, option, resolution, set, assume, broken, until, gamecheck, says, otherwise, popups, separate, windows, drawing, through, virtualgl, wined3d, video, memory, override, fixing, lag, reading, proton, backing, settings, file, find, stands, background, hover, hoversheet, read, tooltip, manual's, annotated, screenshots"
---

# Game setup: run, graphics, UI parsing

Two jobs before playing a new game: **make it run well on Claude's screen**, then **work out what
every part of the screen does**. Builds on **game-ui** (bgplay.py, gamecheck.py, hoversheet.py,
gameui.py) and **learn-to-play** (the wider method). Steam/Lutris specifics: game-ui SKILL and
install-windows-games.

## Part 1 - Run and graphics setup

### 1. Launch where the user isn't disturbed
- Run it on the bgplay virtual screen (`bgplay.py start`, keeper running, **lock on by default**).
  the user may be at the desk; Proton games that would appear on his screen: tell him first.
- Steam games: once, set the launch option (Steam UI, game Properties)
  `env $(cat "$HOME/.cache/game-ui/steam-env" 2>/dev/null) %command%`, then always launch with
  `bgplay.py steam APPID` - it writes the env file (display, renderer, GPU, memory) and removes it
  when the first window appears, so a normal launch by the user is untouched.

### 2. Assume it's broken until shown otherwise (the user's rule)
- `UI_WMCLASS=<class> gamecheck.py --bg --secs 60 --hover X Y` - GONE / POPUP / BLANK / FROZEN / OK.
  30 s to 1 min tells. Check again after every big transition (menu -> battle load).
- Popups can be **separate windows** (launchers, error boxes; TOAW IV and RTW3 do it on purpose):
  `bgplay.py windows` after each step; an extra window of the class = read it before going on.
- Pollers only for changes that will surely come (the user: don't rely on pollers without checking they'll
  work). An AI turn may change nothing: short timeout, then a screenshot. Test a poller once on a known change.
- Loads: `mark` before the action, then `waitchange` on the whole screen - never watch one element,
  and mark first so a fast load isn't missed (`seq "mark" "click X Y" "waitchange 120"`).

### 3. Windowed, at the right size - set it yourself
- Set windowed mode and a resolution that fills the bgplay screen (1600x990 screen -> 1600x900 game)
  in the game's own settings. A game window much smaller or bigger than the screen = fix it now.
- Many games write their settings file **only on quit** - edit it only with the game closed.
  Before any edit: back up the file and write down the user's original values next to it (his settings
  are shared with his own play). FoG II: `OPTIONS.TXT` in the prefix's Documents/My Games folder.

### 4. Graphics: get it onto the GPU
The bgplay screen is Xephyr, which has **no DRI3**: Vulkan can't present, so DXVK/VKD3D games crash
at the first 3D frame. The chain that works (all set by `bgplay.py steam` automatically):

| Problem | Fix |
|---|---|
| DXVK crash (log stops at first render) | `PROTON_USE_WINED3D=1` - D3D through OpenGL |
| OpenGL falls back to llvmpipe: ~10 cores, "lagging hard" | VirtualGL (`/opt/VirtualGL`, the user installed 3.1.5 + virtualgl32): GL drawn on the Radeon, picture copied to :5 |
| 32-bit game (`file` on the exe says PE32; process is `i386-unix/wine-preloader`) | needs the **virtualgl32** package (`/usr/lib32/lib*faker.so`) |
| Steam runtime container lacks `libXv.so.1` -> every process dies at launch | preload host `libXv.so.1` (64 + 32-bit) ahead of the fakers |
| VirtualGL EGL back end: menus fine, battle black/crash | GLX back end: `VGL_DISPLAY=:0` (real X server, off-screen, nothing shows there; needs `xhost` to list `SI:localuser:<user>`) |
| Battle screen black except text, or crash in the first render with shadows on | WineD3D guessed too little video memory from an old card name: `WINE_D3D_CONFIG=VideoMemorySize=2048` |

Check it took: `grep vglfaker /proc/PID/maps`, `top` CPU (FoG II: ~1000% software -> 30-150% GPU),
then time a camera move with `mark` + `hold KEY MS` + `waitchange`.
Wrapping a Steam game in `vglrun` doesn't work (container); env vars + absolute LD_PRELOAD do.
`bgplay.py steam APPID --nogpu` = software only; `BGPLAY_VGL=egl` = EGL back end.
In-game options that cost a lot on weak rendering: shadows, anti-aliasing, idle animations,
level-of-detail distance. The user doesn't care about looks - lower whatever helps.

### 5. When it fails, read the logs (don't guess)
- The game's own log/trace (FoG II: `error.log` - "TS: Ended" = started; a stack trace names the
  function, e.g. `CBattleDisplay::Render` = first battle frame).
- Steam: `~/.local/share/Steam/logs/console-linux.txt` - `ld.so` / "error while loading shared
  libraries" lines (wrong-ELF-class lines for the other bitness are harmless).
- Proton: launch with `--env PROTON_LOG=1 --env "WINEDEBUG=err+all,fixme-all"` -> `~/steam-APPID.log`;
  `grep err: | sort | uniq -c | sort -rn` - one error repeated thousands of times is the cause.
- Process hunting: patterns like `pgrep -f "[F]OG2Med"` (the bracket stops pgrep matching its own
  shell); Windows exe names may be upper case (`.EXE`). Closing: the game's own Quit first; `kill PID`
  if it's wedged (nothing unsaved).

## Part 2 - UI parsing setup (the user: "you want to learn")

Before clicking anything on a new screen:

1. **Manual first.** Manuals usually have annotated screenshots of each screen - find them
   (game-sources `manual.py` grep/outline, then look at the page) and match labels to what is on
   screen. Cheaper than probing.
2. **List every element that stands out from the background.** UI has frames, bevels, plates,
   round icon buttons, arrows, sliders, bars, a minimap; scenery and art don't. Look in the
   **corners and edges** first - small icon rows there hold the important things (FoG II top-left:
   Go Back, Settings, **Load/Save**, Help - Load/Save is not in the main menu).
3. **Hover each one and read what it says:** `hoversheet.py --bg [--park X Y] X,Y X,Y ...` - hovers in
   turn, finds the tooltip by difference (ignoring whatever moves by itself), OCRs it and saves one
   contact sheet (`hoversheet.png`) to Read. Hover only; nothing is clicked.
4. **Then test the safe ones** one at a time with a screenshot after each. Know the dangerous ones
   first (end turn, quit, delete, a top-right X that means Quit Game) and leave them.
5. **Keys too:** read the key bindings screen; some keys act only **while held** (3D camera pan/rotate/
   zoom) - `seq "hold d 1000"`; a tap does nothing.
6. **Write it down** in the game's guide skill: per screen, element -> position -> what it does,
   hotkeys, danger list, window class and size, the settings changed and why.

## FoG II Medieval as the worked example
Launcher Play (1204,370) -> main menu; icons top-left (66/124/184/244, 74): Back, Settings, Load/Save,
Help. Battle: End Turn top right; eye under the minimap = Toggle Top View; terrain tooltips on hover;
camera W/A/S/D Q/E R/F held. Settings changed for Claude: listed in `SETTINGS-BEFORE-CLAUDE.txt`
beside `OPTIONS.TXT` (a dated backup copy next to it).

## Related skills
game-ui (bgplay, input), map-camera (camera controls once running), manual-first (UI pages), learn-to-play, learn-to-mod (loading mods), install-windows-games
