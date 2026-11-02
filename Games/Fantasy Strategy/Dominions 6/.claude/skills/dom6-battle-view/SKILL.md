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
  (box 1640-1830, 58-90), `t` turbo, `s` normal speed, `space` pause (lost if pressed before the
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

## Checks

- The report compares the F1 list with the summary's counts per type and says when they
  differ. The F1 list is read one round before the end, so a unit or two may still die after it.
- The first battle reviewed: Murias, turn 6 (`battles/t6_murias.md`): 84/84 units read.
