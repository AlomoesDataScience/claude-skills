---
name: obs-record
description: Record Claude's gameplay with OBS Studio (flatpak) - launch and set up OBS through its UI with the game-ui guard pointed at the OBS window, and control it from scripts through the OBS WebSocket (obs.py - status, start, stop, pause, resume, mute, any v5 request), including a gameplay session mode where the recording runs only while Claude is acting in the game and pauses while it thinks. Video only; the user records commentary separately, so microphone and desktop audio stay muted. Use when the user wants a turn, a battle or any game session recorded, asks about OBS, or wants a recording started, paused, stopped or checked.
---

# OBS recording

The user records Claude playing and adds commentary separately (2026-10-28): **gameplay only,
never the user's voice**. OBS Studio 33 is installed as a flatpak (`com.obsproject.Studio`) on
X11. Recordings go to `~/Videos` (hybrid MP4, x264 veryfast, 1920x1080 canvas scaled to
1280x720, 60 fps).

## Files

- `scripts/obs.py`: a pure-Python OBS WebSocket v5 client (no pip). It reads the password from
  OBS's own config (`~/.var/app/com.obsproject.Studio/config/obs-studio/plugin_config/
  obs-websocket/config.json`) and never prints it.

## Setup (done 2026-10-28; check with `status`)

1. Launch: `setsid flatpak run com.obsproject.Studio >/dev/null 2>&1 &` (window class `obs`).
2. Scene "Scene" has a **Window Capture (Xcomposite)** of "Dominions 6" (dom6_amd64); it finds
   the window by title and class, so it survives a game restart.
3. **Mic/Aux muted** (the user's voice) and **Desktop Audio muted** (it would also pick up
   Discord voices and pings). Unmute Desktop Audio only if the user wants game sound and nothing
   else is making noise.
4. Tools > WebSocket Server Settings: **Enable WebSocket server** ticked, port 4455,
   authentication on (OBS generated the password).

Driving OBS's UI: the game-ui guard works on any app window with `UI_WMCLASS=obs`; a dialog is
its own window, so add `UI_WMTITLE="WebSocket Server"` (part of its title). Point at the centre
of labels (dom6-tooltips rules). Screenshots must keep the window's aspect (1920x1044: halve
both sides, don't squash to 960x540, or y comes out ~3% wrong).

## Use

    python3 -I scripts/obs.py status            # recording state, scene, sources, mutes, folder
    python3 -I scripts/obs.py begin             # gameplay session: starts paused, sets a flag
    ... play: every game-ui session.run resumes the recording, then pauses it again ...
    python3 -I scripts/obs.py end               # stops; prints the file
    python3 -I scripts/obs.py start | stop | pause | resume | mute NAME | unmute NAME
    python3 -I scripts/obs.py call GetVersion   # any v5 request

**Deciding what to record (the user asked Claude to decide):** open a session with `begin` at
the start of a turn. The hook in game-ui `session.run` (it looks for
`~/.cache/game-ui/recording`) records only while Claude's input is going to the game, so the
video skips thinking, OCR and script writing. Runs that drive another app (`UI_WMCLASS`) are
not recorded. For a battle replay worth watching, `resume` before and `pause` after. `end` when
the turn's work is done (before the user ends the turn). Tell the user the file name.

## Checks

- Before a session: `status` must show Mic/Aux MUTED and the window capture shown.
- A test recording of a few seconds shows up as 0 bytes for a moment while OBS finishes the
  file; check again after 2-3 s. The OBS log (`.../obs-studio/logs/`, newest file) shows
  "paused"/"unpaused" and Recording Start/Stop lines.

## Layout: streamer style (the user, 2026-11-01)

Viewers want Claude's terminal in real time next to the game: "record the game and the terminal
together in a streamer type set up"; don't slow down for them (YouTube can be paused). Reference:
`<workspace>/Sample Layout.png` (a Super Metroid randomizer stream):
- **Left ~2/3:** the game capture, full height.
- **Right column:** where the streamer's facecam sits (top) put the **terminal** (Claude's live
  log: thinking text, tool calls); below it a **tracker panel** - game, lesson/turn, HP, goals,
  timer - like the stream's timer, settings and item tracker. No facecam; skip the top
  recent-subscribers bar.
- **Right column = the stream-panel skill** (`panel.py --fresh`, window class `claude-panel`): live
  log plus tracker in one window; capture it next to the game.
- **Built: `scripts/stream_scene.py`** makes scene "Claude Stream" (1920x1080): a dark colour
  background, "Game screen" = capture of the bgplay window "Claude game screen" scaled into
  0,0-1280x1080, "Stream panel" = capture of "Claude stream panel" at 1280,0 (640x1080), cursor
  hidden (`show_cursor: false`, the user: "hide the mouse"); it sets the scene current. Recipe: start
  the panel with `--fresh` and OBS as background tasks (Bash `run_in_background`; `setsid &` dies
  with the shell), run stream_scene.py, check with GetSourceScreenshot, `obs.py start`, play,
  `obs.py stop` (prints the file). First used 2026-11-01 (DCSS game 1).
- **OBS crash to avoid:** creating an xcomposite input with empty settings, or calling
  GetInputPropertiesListPropertyItems on it, kills OBS ("basic_string: construction from null").
  Always pass `capture_window` filled in (`"<decimal wid>\r\n<title>\r\n<class>"`). After a crash
  OBS asks Normal/Safe mode: choose Normal (safe mode turns the WebSocket off).
- Old alternative: an OBS scene with two window captures (game or the bgplay "Claude game screen", and the
  terminal) plus a text/browser source fed by a small tracker file Claude updates.
