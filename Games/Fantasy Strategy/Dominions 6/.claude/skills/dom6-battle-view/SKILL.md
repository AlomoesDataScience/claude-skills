---
name: dom6-battle-view
description: Review a Dominions 6 battle from its replay so Claude can learn from it - battle_review.py reads the Battle Summary (units, wounded, dead per side), records the replay's detail-4 combat log with the round counter, saves the F1 Unit Overview on the last round, and writes a report (losses, per-unit attacks, hits, damage and kills, who hit whom and how hard, kills and routs by round, spells cast, every unit's end state). Uses dom6-ui for guarded input and OCR; reports feed the dom6-tactics battle log. Use when a battle has been fought, when the user asks what happened in a fight, why it was won or lost, or how a unit or layout performed.
---

# Dom6 battle view

Battles cannot be steered, only set up, so the way to improve is to read every battle
afterwards. This skill turns a replay into a report Claude can learn from (the user, turn 6:
"As long as you can learn from battles, it's a success"). Lessons go into the **dom6-tactics**
battle log; click points for the screens are in **dom6-game**; input goes through **dom6-ui**.

## Files

- `scripts/battle_review.py`: record, units and report (below).
- `scripts/round_digits.json`: digit shapes of the replay's "Combat round N" counter (OCR reads
  0 as G, 7 as /, 8 as &; the shapes are matched instead).
- `battles/NAME.md`: the reports. Raw captures (log strips, field frames, F1 pages, OCR cache)
  stay in `~/.cache/game-ui/dom6_amd64/battles/NAME/`.

## Workflow

1. Messages: click the battle message's **text** (not the space beside it) to open the Battle
   Summary.
2. `python3 -I scripts/battle_review.py record t7_copperwoods` (Bash timeout >= 900 s). It:
   - reads the summary (units, count, wounded, dead per side);
   - pass 1: View Battle, log detail `4`, round counter `r` (the toggle persists), saves the log
     panel on every change and a field frame every 3 s until the replay closes by itself;
   - pass 2: replays at turbo, slows down near the end, pauses on the second-to-last round and
     saves the F1 Unit Overview's pages, then F1 and q back to the summary.
   `--units-only` repeats pass 2; `--no-units` skips it. `units NAME` saves an F1 overview that
   is already open in a paused replay (no replay needed).
3. `python3 -I scripts/battle_review.py report t7_copperwoods` (offline, about 2 minutes of OCR;
   cached afterwards). Read `battles/t7_copperwoods.md` and `field_sheet.png`.
4. Add a row to the dom6-tactics battle log and turn repeated results into lessons there.

## How it reads the screens

- **Replay**: `4` = detail-4 log (panel x 0-935, y 44-300, lines 25 px apart), `r` round counter
  (box 1640-1830, 58-90), `t` turbo, `s` normal speed, `space` or **`p`** pause (lost if pressed before the
  replay has loaded), `q` quit, `F1` Unit Overview. **The replay closes itself at the end of the
  battle** and returns to the Battle Summary, so the log can only be read while it plays. `-` and
  `+` resize the log panel; they do not scroll it.
- **Log stitching**: the panel shows the last ~10 lines; each frame is aligned with the end of
  the text so far at the offset where most lines match (one garbled line does not break it).
  "[gap]" marks lines that scrolled past between frames. Unit names are matched to the
  summary's names (OCR writes Leaionnaire, Heavv Infantrv). About 1% of lines stay garbled;
  the report lists the ones that name a unit or a rout.
- **Unit list (the user's method)**: overlapping, cropped pictures. Each page is cut to the
  list (x 650-1280, y 95-978); the overlap between two pages measures the scroll (3 wheel
  notches = 209 px), and the running total gives every row a fixed place in the whole list, so
  identical rows (two fresh Velites) stay two. Rows are found from the bright Type text (the
  brightest channel: commander names are blue). Side: our flag is purple.
- **Battle Summary**: each number is read in its own box (count 1062-1125, wounded 1169-1216,
  dead 1239-1295); an empty box reads 0 (OCR invents digits there). The game's Total row is too
  dim to read, so totals are added up from the rows.

## On Claude's virtual screen (2026-11-03)
Run with `DISPLAY=:5` when Dominions runs on bgplay (dom6-ui: virtual screen recipe) - the desktop guard
stops when the user switches windows. Boxes were calibrated at 1920x1044; at 1912x1000 check the summary numbers.

## Checks

- The report compares the F1 list with the summary's counts per type and says when they
  differ. The F1 list is read one round before the end, so a unit or two may still die after it.
- The first battle reviewed: Murias, turn 6 (`battles/t6_murias.md`): 84/84 units read.

## Replay keys, manual p. 58 (checked 2026-11-03; the game's `?` list agrees except where noted)
Arrows scroll, PageUp/PageDown camera height, Space pause (`p` too, the user), c team squares, g grid, w wire-frame
grid (battlefield graphics vanish; the `?` list calls it hide world), q quit, f fast, t fastest, **s normal
speed**, **v while viewing a unit = its combat log**, z slow motion, F1 unit list, F2 weather and scales,
? hotkeys, **1/2/3/4 log detail (press 4 every replay)**, **+/- scroll the battle log** (manual and the user agree;
my one "resize" test was wrong or hit something else). battle_review.py presses only these keys (r, 4, f, t, s,
space, F1, q) - checked against this table. On the MAIN map the same letters mean other things (s Send Messages,
f fort, t army setup, q nothing listed): only press them while the replay is open.

## Watching a battle - the replay viewer (2026-11-03, the user: "watch the guys move about", "center the map so
## everyone is seen", "make an animated gif", "include who kills who")
`battle_review.py watch NAME` from the Battle Summary, then `report NAME`, `boards NAME`, write
`NAME/commentary.txt`, `gif NAME` (field + caption + battle log + minimap of the round's board + commentary):
- **Toggles are SET, not flipped**: g (grid), c (team squares) and r (round counter) persist between replays;
  watch checks the screen first (grid_on, unit_mask_box) and presses only what is off.
- **Camera keys must be HELD** (taps do nothing - found 2026-11-03; the old "PageUp x12" never worked):
  PageUp held 3 s = top height (whole field in view from slightly back); PageDown lowers the camera in place
  (the field slides to the horizon - not a zoom). Up/Down move forward/back: forward = units lower on the
  screen AND bigger. Left/Right pan; **pan speed depends on height** (103 px/100 ms low, ~35-45 at the top)
  and is not linear in hold time: never compute positions from hold times, re-measure after every move.
- **Team squares (`c`) differ by side**: in Troban ours dark green ~(41,123,24)/(54,142,35), Pangaea light green
  ~(70,154,53), independents pale grey; the Ghost Moose's white body also reads pale. battle_review
  `square_masks` / `unit_blobs` find them (3x3 opening removes the grid lines; the see-through log panel at
  the top left and the nation-icon bar at the bottom right are masked - the icon bar once posed as "the units").
- **Find everyone, then fill the frame** (centre_on_units): back off (Down 0.6 s: the whole field is in
  view), pan toward any edge the squads touch, back off more if they touch both, centre on the middle of ALL
  squads, step forward until their lowest edge is at 85% of the screen. No sideways scan with offset sums
  (it failed: speed changes). ~6-9 s per round, paused.
- **Rounds without reading digits** (RoundTracker): the counter's white text (min channel > 235) changes only
  when the round does - a new mask on two grabs in a row = next round; a background OCR read every 3 s
  corrects the count. The old reader (shape templates, OCR fallback) failed on bright sky and its 0.75 s OCR
  starved the capture loop: rounds and log lines were lost. The summary check is OCR too: every 2 s only.
- **Grid snap** (scripts/gridsnap.py, the user's idea): the `g` grid is perspective, so: top-hat ridge mask
  (lines ~(120,134,100) on grass ~(70,90,40)), rows = horizontal runs, columns = the rest; vanishing point
  from the column lines (Hough), column crossings read on scan lines every 24 px and indexed by following
  the lines out from a reference row (a mesh - follows hills), row lines read along a central strip and
  interpolated. Every team-square pixel -> its cell = the squares each side holds. Origin = the field's
  left and far edges when in view (Troban: the field is ~86-88 columns wide). Check: `gridsnap.py check
  SHOT` draws the fit; `board SHOT` prints the board. Per round, watch takes a backed-off field shot
  (rounds/fNN.png) for the board before zooming in for the photo (rNN.png); `boards NAME` makes them all.
- **Slow motion (z)** while recording: at normal speed the detail-4 log scrolls past the 0.2 s grabs (Troban:
  ~half the lines lost, 22 of 41 deaths). Animation frames every 0.7 s -> `gif` (round, kills, tramples,
  who killed whom per round from log.txt).
- **Output** (`gif NAME`): battle.mp4 (every frame, H.264 through OpenCV's ffmpeg backend: ~2.6 MB for a
  13-round battle) and battle.gif (6 frames a round, 80%: ~13 MB). Frame = commentary strip on top, the field
  cropped around the squads (the replay camera cannot zoom: wheel = forward, PageDown = lower), a 2x MELEE
  INSET of the biggest cluster drawn in the sky, caption strip below (round, kills, tramples, who killed
  whom), right: battle log + minimap of the round's board (blue dark-green side, orange light-green side,
  grey pale, red contact; one view for the whole battle). ONE shared palette with fixed key colours: per-frame
  128-colour palettes erased the team squares. watch saves frames as full-size JPEG for sharp crops.
- **GIF details** (`gif NAME`): per frame the round, kills, tramples, who killed whom; a small battle log panel on the
  right (that round's hits/tramples/kills/spells, scrolling; kills red, tramples orange); and my COMMENTARY:
  write `NAME/commentary.txt` after watching ("0: deployment - ...", "3-5: the centaurs wrap the right"),
  then re-run `gif`. Commentary = what happened and why, in doctrine terms (battle-tactics), not a recap.
- **Tramples** are their own log lines ("X trampled Y for N", "X tried to trample Y who evaded most of the
  attack (1 point)"), they REPLACE the weapon attack: report counts them in their own columns.
- **Battle Summary** sword column = KILLS (Troban: White Centaurs 34, Minotaur Warriors 4, Ghost Moose 1,
  Centaurs 1 = our 41 dead minus one). Read it by eye or from the dialog found on screen, not fixed boxes.
- Round counter: white text over the sky; on a bright sky the shape matcher fails -> OCR fallback (_round_ocr).
- Messages can list SEVERAL battles in one province (Troban: vs independents, then vs Pangaea): check each.

## Standards (audit 2026-11-03)
- **Screen:** coordinates here were measured on the 1920x1044 desktop. On Claude's 1912x1000 virtual screen (dom6bg.py / bgplay) find positions by OCR or re-measure - never reuse a stale coordinate (memory: apply tools universally).
- **MP games (the user's):** look only - right-click views, hovers; no orders, recruits, research, transfers or End Turn.
- **Modded games:** numbers here are vanilla - check the mod first (dom6-scbm for SCBM; mod-docs).

## Related skills
dom6-tactics (lessons go there), battle-tactics (lessons log), army-log, dom6-mechanics (rules behind results).
Also (2026-11-03): dom6-battle-ai, unit-combat-math, dom6-battlefield.
