---
name: generalize-learning
description: Guidelines for when and why to push what Claude learns in a game-specific skill (a game's guide, map, commands or units file) up into a generic skill (learn-to-play, map-usage, map-camera, photo-map, battle-tactics, manual-first, planning, game-ui...) - the tests (would it help in a second game? is it a method, not a number? did the user state it as a rule? did it go wrong in a way any game could?), what stays game-specific (coordinates, key bindings, unit stats, rules), how to write the generic version (abstract the method, keep the game example as an example, link back), where it goes, and when to do it (end of each lesson, when the user corrects a method, when a second game repeats a pattern, when a tool proves itself). Use when something in a game was just learned or fixed, when the user gives a rule, when writing a new game skill, at the end of a session, or when unsure where a lesson belongs.
---

# Generalize learning - game skill → generic skill

The point: every game should make the next one easier. A lesson stuck in one game's guide is lost
to every other game. The user's corrections are usually about how to work, and that applies everywhere.

## Why
- Methods carry over and numbers don't. Photographing the board, checking the manual first, and
  calibrating the camera all helped in FoG and will help in the next wargame, 4X or roguelike.
- The user teaches through one game, but the rule is meant for all of them ("This needs to become a
  skill", "a generic skill", "every time you play a new game").
- One generic copy, kept current, beats the same lesson half-remembered in five game guides.

## The tests: push it up if ANY is true
1. **A second game would use it.** It's about how to look, learn, plan, act or record, not about
   this game's content.
2. **The user stated it as a rule or a method.** "Always", "never", "every time", "this is how you…".
3. **It's a mistake any game could repeat**: phoning it in, guessing instead of reading,
   re-deriving, Tab-cycling, ending a turn.
4. **A tool proved itself** (panorama.py, camcal.py, lookup.py) and doesn't depend on the game.
   Tools go in generic skills, and their per-game numbers stay with the game.
5. **The same pattern turned up in a second game.** Promote it now, even if it looked specific
   the first time.

## Keep it game-specific when it's
- Coordinates, pixel boxes, key bindings, menu paths, timings and calibration numbers.
- Rules, unit stats, army lists, terrain effects, victory conditions. Those come from that game's
  manual or the game itself.
- A guess about this game ([hyp]) that hasn't been tested yet.
Game-specific facts can still go in the generic skill as a worked example, labelled with the game,
under a per-game section.

## How to write the generic version
1. State the method or rule in game-free words, and give the reason.
2. Keep one concrete example from the game that taught it ("FoG II: 250 ms pans never overlapped").
3. Put it in the generic skill that owns the topic. If none fits, make a new one
   (skills-manager), add it to INDEX.md and link it from the related skills.
4. Leave a pointer in the game skill ("method: map-camera") instead of a second copy.
5. Rules from the user also go in memory, so they load every session.
6. If the generic skill says how per-game skills should look (like map-usage part 4), update the
   game skills to match.

## Where things go (current owners)
| Topic | Generic skill |
|---|---|
| Learning a new game to play, order of steps, order of truth | learn-to-play |
| Learning a game to mod | learn-to-mod |
| Checking rules / anything new | manual-first |
| Running and parsing the UI | game-setup, game-ui |
| Seeing the map | map-camera |
| Photographing the board | photo-map |
| Measuring a map (size, squares) | map-measure |
| Using a map to decide | map-usage |
| Drawing a map (optional) | draw-map |
| Drawing movement plans | draw-moves |
| Battle plans and the turn method | battle-tactics |
| Plans as files | planning |
| Tutorials | learn-from-tutorials |
| Borrowing systems for our games | borrow-from-games |
| Skills housekeeping | skills-manager |

## When
- At the end of every lesson or teaching stretch with the user: go through what changed in the game
  skills and run the tests.
- Straight away when the user corrects how I'm working, or says "make this a skill".
- When a second game shows the same pattern.
- When a game tool works: move the tool to a generic skill and keep its numbers in the game guide.
- At the end of a session: anything left only in a game guide that passes a test gets promoted.

## Examples (FoG II, 2026-11-02)
- "Check the manual when something new pops up" → manual-first.
- The F1 key list beats the manual → learn-to-play step 0, manual-first.
- Camera calibration and the 100 ms step → map-camera (method and tool); the 100 ms stays as FoG's
  number.
- Invisible terrain (enclosures) → map-usage, as the general idea that some terrain is invisible
  and needs a tooltip; which FoG terrain is invisible stays in fog2m-map.
- "You already figured that out yesterday" → skills-manager (check skills before re-deriving).

## Related skills
write-skill (format checklist), save-scum (DARK ARTS, learning only: save before a test, reload after; never in real games), skills-manager, learn-to-play, learn-to-mod, and every generic skill in its table
