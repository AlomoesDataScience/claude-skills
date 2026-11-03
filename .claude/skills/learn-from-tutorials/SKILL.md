---
name: learn-from-tutorials
description: How Claude learns any game through its built-in tutorials, lessons, training missions or hint modes - play every lesson in order, read each prompt as a rule, test each taught key once, note numbers, and update the game's skill after every lesson (the user's rule). Fast loop - background play (game-ui bgplay.py), text reads of message/stat regions instead of screenshots, batched keys, little deliberation on routine steps. Use when starting a new game that has a tutorial, when the user asks Claude to play through tutorials, or when a game offers hints or training scenarios.
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
