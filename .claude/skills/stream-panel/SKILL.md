---
name: stream-panel
description: "A side window for recordings and streams: tracker on top (game, status, goals) and Claude's live log below. Use when recording or streaming gameplay or showing stats beside the game."
keywords: "right-hand, column, streamer, layout, mode, line, fields, such, place, turn, ticks, recent, events, session, timer, terminal, says, tool, call, description, full, results, messages, including, ones, typed, mid-turn, runs, hide, show, toggle, stop, never, takes, focus, python, api, feed, bgplay, reads, fill, automatically, through, block, folder's"
---

# Stream panel

Built 2026-11-01 on the user's idea: "a GUI program that tracks game information and outputs terminal
information while playing the game, and use that as a display". In OBS it is one window capture
next to the game (obs-record, "Layout: streamer style").

```
panel.py                 # start (right third of the screen, last ~60 log entries)
panel.py --fresh         # start with an empty log - use for recordings
panel.py hide | show | toggle | stop
tracker.py game "Dungeon Crawl Stone Soup" --mode "Real game: Minotaur Fighter"
tracker.py status "Clearing D:3"
tracker.py field Turn 412 Gold 230        tracker.py field --del Gold
tracker.py goal add "Find the Lair"       tracker.py goal done 1
tracker.py note "Found the +1 cloak of Starlight"
tracker.py start                          # restart the timer, clear notes
```
Run the panel as a background task (Bash `run_in_background`): a `setsid ... &` launch is
killed when the shell exits.

## What it shows
- **Top:** game (accent colour), mode, timer, status line, fields in two columns, goals (☐/☑),
  last 6 notes with times.
- **Log:** Claude's text (white), `▸ Tool  description` (blue) plus the shortened command (dim),
  full results in a smaller font, never cut (the user: "it has to display everything"; errors red), the user's messages (purple, `⮞`). The user's mid-turn messages
  come from the transcript's `queue-operation` "enqueue" lines, so they appear when he presses Enter.
  Thinking and subagent entries are left out. Header: acting / thinking / idle and the action count.
- Source: the newest `~/.claude/projects/*/*.jsonl` (re-checked every 10 s) or `--transcript`.
- Paths are shortened (workspace -> `AI`, home -> `~`, scratchpad -> `scratch/`, bgplay calls
  -> `bgplay`).
- Window keys: Space pauses the scroll, +/- font size, h hides, q quits.

## Rules (the user, 2026-11-01)
- **Never take focus**: The user may be typing. The panel hands focus back to the window that had it,
  and `show` raises it without focus. Hideable like the game screen (`hide`/`toggle`).
- **Show everything, never `...`**: long commands and results wrap (results use a font 2 sizes
  smaller); tracker values wrap and fields drop to one column when the window is narrow. If it
  still doesn't fit, make the font smaller (`--font`, +/-) or the window bigger, never cut text.
- Display correctly wherever it is: tracker text re-wraps to the window width on move or resize,
  and an off-screen start is pulled back.
- One panel at a time: starting again only shows the running one.
- **For recordings use `--fresh`**: the log shows the whole session otherwise, including work
  that has nothing to do with the game. Private material must never be on screen.

## Hooks: feeding the tracker
- **bgplay reads** (game-ui `bgplay.py read REGION`): the game folder's `.claude/game-ui.json`
  can carry
  `"tracker": {"game": "...", "fields": {"HP": ["hp", "Health:\\s*(-?\\d+/\\d+)"], ...}}`
  (field = region name + regex with one group). Every read of that region updates the field.
  A failed hook never breaks a read. DCSS has HP, MP, XL, Place, AC and EV set up.
- **Scripts:** `sys.path.insert(0, ".../stream-panel/scripts"); import tracker as T;
  T.update(fields={"Turn": 7}, note="Took Azimar", status="Ending turn")`.
- **By hand:** tracker.py commands above. Use them for goals, mode and notes as the game goes.
- Data file: `~/.cache/game-ui/tracker.json` (env `TRACKER_FILE`), written atomically.

## Ideas not built yet
Per-game tracker presets (Dominions turn/gold/gems from dom6-ui readers), a small game
thumbnail or minimap, a chat column for the online Angband plan.

## Related skills
idle-view (natural camera and mouse while idle on a recording), obs-record, game-ui
