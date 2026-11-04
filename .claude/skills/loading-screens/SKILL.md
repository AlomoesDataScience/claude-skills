---
name: loading-screens
description: Tell whether a game's screen is a loading screen and wait through loads properly, in any game on Claude's virtual screen - the user's method (2026-11-03) - shoot the screen BEFORE starting a load, act, grab frames as fast as possible (~33 ms) until the screen changes (else the action DID NOT TAKE), then decide with ONE GENERAL test whether what came up is a loading screen (blank, fade, spinner/progress-bar-only motion, loading words) - no per-game learning - and poll it out every second. bgplay.py act / isloading / waitload. Use whenever Claude clicks or presses something that loads (Play game, End Turn, battle replays, menus, map screens), when a script waits for a game, when a wait timed out or ended early, or to check "is it still loading?".
---

# Loading screens

The user (2026-11-03, loading Claude's Dominions game): "the checking for if stuff loading stuff is broken" ... "set up
a skill to check if something is a loading screen" ... "the necessary part is generalizing how you check if it's a
loading screen. Once you can do that, you can apply the same logic across other things." The old waits asked "has
the picture stopped changing?" - animated games never stop, and a screen already up never "changes" (map of the
old waits: `.claude/plans/fix-loading-checks.md`).

## the user's method
1. **Poll before the load is started**: a shot of the screen just before the click.
2. **Shoot immediately after the click, at the millisecond level**, until the screen changes - loading screens
   can last 1 s or less (a Dominions fade: 292 ms). No change = **the click didn't take**: stop, don't wait.
3. **Is what came up a loading screen?** (the general test below). No = it was a button click: done.
   Yes = **poll every second** (cheap) until the screen leaves it and no longer looks like one.
4. A load may be slower some day: a usually-quick transition showing a loading screen is still caught by step 3.

## The general test (`loading_signs` in bgplay.py) - any game, no learning
Watch ~1 s of frames (one every ~33 ms) and read the screen once:
| Sign | What it measures | Catches |
|---|---|---|
| blank | dark (mean < 25) or near-uniform (spread < 10) frame; or much darker than before the click | black screens, fade bottoms, plain colour |
| fade | brightness ramps one way by 6+ over the window | fade in / out |
| local motion only | the changing pixels fit in < 12% of the screen and are 0.1-3% of it - WEAK: counts only with a loading word | spinners, progress bars, "Loading..." dots |
| words | "loading", "please wait", "thinking" (Dominions "AI thinking"), "reticulating" (The Sims), ... | text loading screens |
| (temporary) | it gives way to another screen with no input - the polling | confirms it |

An animated game screen (Dominions' sea, idle units) changes all over the frame, so it is NOT "local motion".
Tested 2026-11-03 (`tests/loadtest.py`): black, fade, spinner + "Loading...", joke text ("Reticulating
Splines...") and Dominions' real fade frame -> LOADING; Dominions' real animated map and F1 screen -> not loading.
**Lesson (first real use, same day)**: local motion ALONE gave a false LOADING on the still Dominions map (one
small animation, 0% of the screen) and the wait ran on. So it is a weak sign: alone it means nothing. Cost: a
silent spinner/progress bar on a still picture with no text is missed (act then calls it a button click) -
if a game has one, add its text or picture sign here.

## Commands (game-ui `bgplay.py`)
```
bgplay.py act NAME "click X Y" [--timeout 180] [--took 3] [--tol 12]
      TOOK in N ms / DID NOT TAKE (exit 2) / LOADING: evidence -> READY (lasted N ms) / no loading screen / TIMEOUT (3)
bgplay.py isloading [--window 1] [--nowords]    LOADING (exit 10, with the evidence) / NOT LOADING
bgplay.py waitload [--timeout 600] [--name N]   if loading, poll every second until it's gone
bgplay.py waitchange --until "TEXT"             when the target screen has known text (checked at once)
```
- NAME keeps only a load-time history (`.claude/transitions/NAME.json` next to the game's game-ui.json), so a
  load slower than twice the longest seen is flagged "maybe stuck".
- **A change** (the click took / the screen left the loading screen) = mean grey difference > --tol on a 160x99 thumbnail, OR 0.2%+ of pixels changed by 40+ (a small dialog replaced in place: End Turn Yes -> "AI thinking" box read only 11.8 on the mean and act wrongly said DID NOT TAKE, 2026-11-03). `--tol 12`: mean grey-level difference on a 160x99
  thumbnail. Dominions' animated sea drifts ~8 in 10 s with no input; a real screen change is 30+. Measure a new
  game's idle drift first (10 grabs, 1 s apart, no input) and raise --tol if it's busier.
- Words cost ~5 s of OCR, so they are read only when no picture sign shows. Add new loading texts to LOADING_WORDS.
- Never pipe a wait through `tail`: its progress lines and verdict are the point.

## Applying it elsewhere
The same question - "is this a transient screen, and what are its signs?" - fits end-turn processing (Dominions
"AI thinking", FoG II's short AI turn: "FOG II generally will not take that long to do a turn"), battle replays
starting and ending, save/load, popups that appear on their own. Old waits still to move onto it: dom6bg.py /
order.py `settle`, battle_review's fixed sleeps (plan file above).

## Tests from the user
He will find a nonstandard loading screen to test on - record the result here.

## Related skills
game-ui (bgplay, the guard), game-setup (gamecheck: is the game alive at all), dom6-ui, fog2m-guide,
hand-back, idle-view.
