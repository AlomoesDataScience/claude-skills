---
name: borrow-from-games
description: Use every game Claude has learned as a parts bin for designing other games (our 4X engine, Heresiarch, Pocket 4X, AMBS, anything new) - regardless of genre or theme. The user's rule - pull from all games to figure out what is what; a historical game doesn't want magic, but keep the options open and consider how a system could translate. A fixed systems taxonomy (time, map, economy, production, research, characters, politics, war, logistics, AI, victory, UI, modding...), a "## Systems" section in every game guide, borrow.py to build a cross-game catalogue (systems.md), search it, list guides still missing the section and lay out every option for a design question, and a procedure for turning a borrowed system into a design decision with its source. Use when designing or reviewing a mechanic for one of our games, when the user asks how other games handle something, after learning a new game (fill its Systems section), or when comparing games.
---

# Borrow from games

The user (2026-11-01): "we do want to pull from all games to figure out what is what for any game,
regardless of genre or theme. Obviously, for example, for a historical game, we don't care about
magic, but it is important to keep our options open to consider things."

So: every game is studied for its **systems**, not just its theme, and every design question gets
answers from **all** games, with off-theme systems translated rather than dropped.

## The taxonomy (use these exact category names)

| Category | Covers |
|---|---|
| Time | turns, phases, simultaneous orders, real time with pause, impulses, action points, initiative |
| Map | hexes, provinces, nodes/lanes, zones, procedural generation, fog, terrain, weather |
| Economy | resources, money, upkeep, trade, markets, supply chains, private sector |
| Production | building, queues, unit and ship design, components |
| Research | tech trees, cards, random draws, doctrine, magic schools as research |
| Population | pops, species, culture, religion, happiness, unrest, migration |
| Characters | leaders, generals, heroes, traits, aging, dynasties, loyalty |
| Politics | internal factions, government, councils, laws, legitimacy, collapse |
| Diplomacy | treaties, vassals, federations, AI attitudes, espionage |
| Operational war | movement, stacking, zones of control, command limits, fronts, reactions |
| Tactical combat | battle resolution, CRTs, battle maps, morale, formations, autobattles |
| Logistics | supply lines, attrition, transport, rail/river/ocean movement, depots |
| Intelligence | sensors, detection, hidden units, deception, EW |
| AI | how the computer opponent plans, cheats, escalates (AI War's AI Progress), scripts |
| Victory | win conditions, sudden death, VPs, pacing, catch-up and runaway control |
| UI | how the game shows a lot of state; what makes it thick or easy |
| Modding | data formats (text, CSV, XML, scripts), editors, what modders can change |

## In every game guide: `## Systems`

One bullet per category the game does something worth knowing, in Claude's words, with where it is
documented:
```
## Systems
- **Time**: both players roll a d6; the difference is both sides' action points; doubles give cards (rules 4.1, p3)
- **Logistics**: Union has 12 SPs of rail, Confederacy 7 (3.2)
```
Fill it when the guide is written; add to it as play teaches more. Note what makes a system good
or bad in play (the user: AGEOD games are "thick and hard to figure out for players": that is a
finding about the UI and the rules both).

## borrow.py

```
scripts/borrow.py index            # read every guide's ## Systems -> systems.md (category > game > note)
scripts/borrow.py find "supply"    # every Systems line and catalogue entry that matches
scripts/borrow.py options Logistics   # all games' entries in one category, for a design question
scripts/borrow.py gaps             # game guides without a ## Systems section yet
```

## Turning a borrowed system into a design decision

1. State the design question in the taxonomy's terms ("Time: how do turns work in our 4X?").
2. `borrow.py options <Category>`, plus `find` for keywords. Read the source rule if it matters.
3. List the options, **including off-theme ones translated**: Dominions' magic paths could be a
   historical game's doctrines or institutions; a card game's deck could be a research system;
   a roguelike's identify-by-use could be intelligence on unknown enemy tech.
4. Judge them against the design's own goals (the project's design docs: engine4x-design for the
   4X, Heresiarch's CLAUDE.md...), the user's stated taste, and what was bad in play.
5. Write the decision with its sources ("from The U.S. Civil War 4.1, changed so...") in the
   project's docs; the user makes the call on design questions that are his.

Take the **systems, not the presentation**. The user's art direction for our games (2026-11-01): cheap
Dominions-style 2D sprites for everything; everything else text, flat colours or vector-drawn UI. A
big 3D game (Field of Glory II, Kingdoms) is mined for its rules, data formats and UI ideas (odds
tooltips, map modes), never its art pipeline.

Our games: engine4x-design (the user's 4X), heresiarch-guide, Pocket 4X and AMBS in `Projects/Stuff I made/`.

## Related skills
learn-to-play and learn-to-mod (where the systems knowledge comes from), game-sources and wiki-scout (manuals, wikis), generalize-learning
