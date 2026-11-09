---
name: learn-from-tutorials
description: "Learn any game through its built-in tutorials, lessons and hint modes: play every lesson, read each prompt as a rule, write it down. Use when a new game has a tutorial or the user asks Claude to play through one."
keywords: "learns, training, missions, order, test, taught, key, once, note, numbers, update, game's, skill, after, fast, loop, background, game-ui, bgplay, text, reads, message, stat, regions, instead, screenshots, batched, keys, little, deliberation, routine, steps, starting, offers, hints, scenarios"
---

# Learn a game from its tutorials

The user's rules (2026-11-01): play through the tutorials; **after every tutorial, update the skills**;
maximise action speed (the bottleneck is thinking or the game itself, not input).

## Loop per lesson
1. Run the game in the background where possible (game-ui `bgplay.py start`, `launch ...`;
   the user's input locked). 3D games: the guarded desktop route.
2. Set up text regions first (game folder `.claude/game-ui.json` "regions": msg, stats, hp) and
   read them with `bgplay.py read msg hp` after each batch; screenshot only for layout/positions.
3. Do exactly what each tutorial prompt teaches, once, then check the message text. The tutorial
   prompt is the rule; write the key and its effect down.
4. Batch routine input in one `seq`, **but one "explore/advance" step per batch, then read**
   (the user, 2026-11-01: chained auto-explores walked past a tutorial artefact, a cloak worth EV+4,
   and the next fight nearly killed the character). Batch only keys whose result you don't need
   to see; stop at new prompts, items, enemies, choices or anything final.
5. Record numbers the game shows (time per action, hit chances, damage, costs).
6. Note dangerous keys and prompts (permanent modes, quit, abandon) the moment one appears;
   cancel with Escape; never type confirmation words.
7. **End of lesson:** read the summary card, then update the game's `<prefix>-guide` (controls,
   screen map, mechanics, dangers, what's next) and add any generic lesson here or to
   learn-to-play / game-ui. Then the next lesson.

## After all lessons
Fill the guide's "## Systems" section (borrow-from-games), then play a real game in reviewed steps
(learn-to-play step 7).

## Example
Dungeon Crawl Stone Soup (dcss-guide): lesson 1 movement done, lesson 2 monsters half done.

## Related skills
learn-to-play (the full method; tutorials are one part), manual-first, generalize-learning, game-ui
