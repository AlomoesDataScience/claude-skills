---
name: rules-skills
description: How Claude turns a game's rules into a family of mechanics skills and guides (the method behind the Dominions 6 set, 2026-11-03) - a numbered plan file first (one skill per mechanic a player decides about, pages per item, the user approves extras, ticks), sources in order of truth (game > mod files > manual > videos > wiki > user's word), citing pp. on every rule, the skill body (formulas, worked numbers or odds tables, a Using-it section, the user's examples, Related skills), computing numbers instead of eyeballing (exact dice tables, simulators, checks against game data), databases for rank-everything requests (purpose, score, basis, trust section, sanity-checked top lists), mods kept apart, videos as sources, and the finish (check, index, loose-line sweep, plan ticks, report). Use when building rules, mechanics or strategy skills or a guide for any game, when the user asks for a skill about game rules, or when ranking a game's units, spells or items.
---

# Rules into skills (rules-skills)

The user (2026-11-03): "while it's fresh, you might want to get a skill for how you did all this skill and guide
making." Learned building the Dominions 6 mechanics set (dom6-drn, -combat-math, -morale, -dominion,
-economy, -spell-db...). Format rules for any skill: write-skill. Sources: game-sources, manual-first.

## 1. Plan first (planning skill)
- One file, `plans/<game>-mechanics-skills.md`: a numbered list, one skill per **mechanic a player makes a
  decision about** (combat odds, morale, sieges, dominion), each with its sources and pages
  ("19. dom6-stealth: manual pp.49-53").
- The user's asks go in as items with his quote; extras I suggest are marked until he approves them.
- Tick items (`[x] ... DONE <date> as <skill>`) as they land; add a dated status line for anything waiting
  on the user (a download, a video transcript).
- Split when the user asks or a section grows its own decisions (blood hunting left dom6-blood).

## 2. Sources, in order of truth
1. **The game itself** (screens, tooltips, battle logs) wins.
2. **Mod files** for a modded game - in the mod's own folder (mod-docs); vanilla skills stay vanilla.
3. **The manual**: page-numbered text (game-sources manual.py). Read the whole section, not a grep hit.
   A page helper keeps it exact:
   `pg(){ a=$(grep -n "=== page $1$" $M|cut -d: -f1); b=$(grep -n "=== page $(($2+1))$" $M|cut -d: -f1); sed -n "$a,${b}p" $M; }`
   Two-column PDFs interleave lore boxes and table halves - rebuild tables by hand.
4. **Videos** (video-watch): transcript + frames, cite the timestamp. Above the wiki (the user 2026-11-03:
   "videos is above wiki") - experienced players showing the game; still check against the game.
5. **The wiki** (dom6-wiki style mirror) for what the manual lacks: spell lists, blesses, guides. Where it
   disagrees with the manual, the manual wins and the skill says so.
6. **What the user says** is below all the sources (the user: "what user says should be below all that, but test
   it if they insist") - if he insists, test it in the game and write down the result either way.
- Cite **pp.** on every rule. Don't write a number the sources don't give; mark guesses "(unchecked)".

## 3. The skill body
- Title + the user's ask with the date + sources and turn-order steps.
- **Rules**: the formulas as written (with pages), short tables.
- **Numbers worked out**: a quick-odds table or worked example (DRN difference -> chance; unrest -> income).
- **Using it**: what a player does with the rule; the user's own game as the example (his lines quoted).
- **Related skills**; the umbrella skill (dom6-mechanics) gets a "details: dom6-X" link.
- Description: what it covers + "Use when ..." within 1024 characters - list topics, not every formula.

## 4. Compute, don't eyeball
- Dice: exact tables (open-ended 2d6 enumeration), not "about half".
- Matchups: a simulator over the real stats (dom6-spells spells.py: melee, missile, cast_once, trade) for
  questions like "how do my Sidhe trade with White Centaurs" - try the buffs and report rounds-to-kill.
- Check stats against the data (inspector) before using them; modded games use the mod's data.

## 5. "Rank everything" -> a database (tool and full method: game-database)
- Build from the data files (every row, generic and national), never from memory - it finds what the hand
  lists missed.
- Each row: purpose (what it's for), tier within the purpose, value, cost-efficiency, **basis** (simulated /
  weights / cost), the hand tier if one exists, and the detail behind the score.
- Output: SQLite + CSV + one markdown page per purpose; a `top PURPOSE --paths --nation` query.
- Sanity-check the top of every list before calling it done (found: unresearchable event spells at #1,
  sacred-only buffs counted as army-wide, nation lists cut at 120 characters, undead-only spells scoring 0).
- A **trust** section in the skill says which numbers are measured and which are judgement.

## 6. Finish every skill
1. `skills.py check <name>` (skills-manager) until ok; `skills.py index`.
2. Loose-line sweep: no "p.??", "?", TODO, or claims without a source left in.
3. Umbrella link, plan tick, a short report to the user (what's new, what's still waiting).

## Pitfalls seen
- Descriptions over 1024 characters (four times) - trim the topic list, keep "Use when".
- A game-state claim written from memory was wrong (Tir na n'Og's scales) - check the save or the notes.
- Code downloads (yt-dlp, pip packages) can be refused - ask the user to run them with `!`; never work around.
- Purchased manuals stay local (skills-git export skips them).

## Related skills
write-skill (format), skills-manager (check, index), planning (the plan file), game-sources and manual-first
(sources), learn-to-play (playing, not documenting), mod-docs, video-watch, wiki-scout, generalize-learning.
