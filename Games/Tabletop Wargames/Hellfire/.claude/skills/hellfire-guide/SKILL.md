---
name: hellfire-guide
description: Starter guide to Hellfire, a generic 1/300 (6mm) science-fiction tabletop miniatures wargame in a low-key, mercenary-and-militia universe (Jack Vance flavour), plus its campaign book Hellfire Campaigns - The Universe at Your Feet (building a home-made world, state finances, hiring mercenaries, drifting into war, solo campaigns) - groups, command by order points, reaction, small arms and anti-vehicle fire, artillery, close combat, morale, aliens, robots, psionics, scenarios. Uses game-sources (rule lookups), learn-to-play (method). Use when the user wants to play, learn or talk about Hellfire, set up a 6mm SF battle or a Hellfire campaign, or have Claude run one solo.
---

# Hellfire - starter guide

Status 2026-10-29: both books read in contents, introduction and sequence of play. Not played.
Purchased copies (order watermark): keep them local. A miniatures game: it may belong in
`Games/Tabletop Tactics/` if the user wants (moving it is the user's call).

Files: `Hellfire.pdf` (51 pages: the rules) and `Hellfire_Campaigns._The_Universe_at_Your_Feet..pdf`
(70 pages: campaigns), each with a `.txt`; neither has bookmarks, both have a printed contents
on the first pages (`manual.py toc Hellfire.txt --pages 4`).

## What it is (Claude's summary)

Skirmish-to-battalion SF battles with 6mm models, meant to cover many kinds of SF setting while
keeping a flavour of its own: a universe that is not over-militarised, where improvised armour,
hired regiments of engineered soldiers and local militias meet. Troops act in **groups**.

Turn (rules p7): player A moves (B may give covering fire), fires artillery, fires everything
else, fights close combat (B may fire at groups about to close), checks morale; then player B
does the same. **Command**: each turn roll d8 plus modifiers (well organised +1, personal comlinks
+2, nuclear or plasma weapons in use -2 for five moves) = number of groups that may act. Then
reaction, small arms fire with to-hit and casualty tables, anti-vehicle fire against armour,
artillery and its near misses, close combat, minefields, snipers, morale, and rules for aliens,
robots, very large vehicles and psionics; two scenarios.

**Campaigns** (second book): build a world (geography, human geography, technology), give states
an income and an army budget, cost raising troops and hiring mercenaries, let politics drift to a
crisis, fight the battles (also solo); worked examples Myopia (a civil war with mercenaries), The
Man Who Would Be King (political randomness, alliances, budgets, winning) and Community Policing.

## How Claude helps

Claude can run a campaign world (finances, politics, random events) and set up battles from
it, or act as the opponent's command in solo play. Models stay on the user's table.

## War skills (the user 2026-11-02: call the military skills when playing; build on them)
- Level of war: **tactical (sci-fi miniatures)**; domain: **land**. Vocabulary: military-doctrine (FM 3-90 tactics) first; soviet-doctrine for the
  opposing school; war-concepts (glossary, `warwiki.py look TERM`).
- Every turn / battle: **war-language** (UP: the situation in doctrine terms -> THINK: intent,
  form of manoeuvre, a task and purpose per unit -> DOWN: concrete orders -> CHECK) and **army-log**
  (read, log and evaluate both sides; `armylog.py`). Before the first real game write
  **`LEXICON.md`** in this skill folder (`warlang.py lexicon`): units -> roles, terrain -> OAKOC,
  rules -> effects, victory -> end state, task -> game actions.
- combat-models: The user's land salvo system and Lanchester (concentrate; make fights square when stronger, linear when weaker).
