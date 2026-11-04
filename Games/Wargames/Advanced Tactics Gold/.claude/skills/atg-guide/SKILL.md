---
name: atg-guide
description: Starter guide to Advanced Tactics Gold (VR Designs / Matrix, Victor Reijkersz), a hex wargame engine and construction set - random 4X-style games and scenarios, production with oil and ore, research, supply, battle stacks, combat rounds, alliances, the editor and its data structures, with a page map of ATGE-Manual-[EBOOK].pdf (140 pages, bookmarked; searchable .txt next to it). Uses game-sources (manual lookups), game-ui (window driving), learn-to-play (method). Use when the user wants to play, learn, build a scenario for or talk about Advanced Tactics / ATG, or asks how one of its rules, screens or editor features works.
---

# Advanced Tactics Gold - starter guide

Status 2026-10-29: manual outline read; introduction, starting play, general advice, the
"what changed" rules summary and the start of game flow read. Not played yet.

Files: `ATGE-Manual-[EBOOK].pdf` (140 pages, bookmarks) and `ATGE-Manual-[EBOOK].txt`. Outline:
`manual.py outline "ATGE-Manual-[EBOOK].pdf" --depth 3`; search with `manual.py grep`.

## What it is (Claude's summary)

A hex-and-counter WWII-flavoured wargame that is really a **wargame construction set**: the same
engine runs random games (everyone starts at peace with infantry spread over their cities - a 4X
start), historical operational/strategic scenarios, even ancient or space settings made by
scenario designers (community Scenariobank). The designer, Victor Reijkersz, later built Decisive
Campaigns and Shadow Empire on the same ideas - worth knowing for our own strategy game.

Key ideas (from the rules summary, p15-17 and the rules chapters):
- **Production** in cities and factories costs production points and raw materials (oil, ore);
  only plain infantry needs none, so scarce resources mean infantry-heavy armies. Research raises
  equipment tech levels; buy for a plan, don't build a bit of everything.
- **Supply** runs from cities through your territory; alliances can share supply, territory,
  units and research. Declaring war costs production points; back-stabbing earns a reputation.
- **Combat** is fought in rounds between stacks: battle-stack limits make well-defended hexes hard
  to break; non-armour attackers suffer penalties in the first two rounds; long battles cost action
  points afterwards; defence is the stronger form, but combined arms and armoured breakthroughs in
  the right terrain still work. Air, navy and motorised troops burn oil to move and fight.
- **Units**: formations of subformations (troop types such as general infantry, SMG infantry,
  tanks, artillery, aircraft, ships) each with attack/defence per terrain. The interface has `?`
  buttons with the exact numbers; the manual avoids hard statistics on purpose.

## Manual map (PDF pages)

Introduction and advice 14-17; interface 17-57 (main menu 17, new random game 19, scenario setup
22, game loop 24, main game screen 26-48, statistics 48, history 50, decision room 50, strategic
map 52, combat screens 53-54, short keys 56); ATG rules 57-71 (combat 58, troops and research 59,
landscapes 64, location types 67, peoples 70); engine rules 71-134 (game pieces 71, advanced data
structures 90, game flow 97, **combat calculations 105**, orders 115, topical 129); editor
interface 57 and data import p90+.

## Why it matters for our own game

Of all the user's games this one documents its engine most openly: the "Engine Rules" chapters
(game pieces, data structures, game-loop steps, combat calculations) are close to a design spec
for a moddable hex wargame. Read them when we design our own.

## To learn next

1. Play the tutorials (main menu) with the user's go; map the main game screen with game-ui.
2. Read combat calculations (p105-115) and game flow (p97-105) in full and summarise them here.
3. Note the short keys (p56) and what ends a turn.

## War skills (the user 2026-11-02: call the military skills when playing; build on them)
- Level of war: **operational (hex)**; domain: **land**. Vocabulary: military-operations (FM 3-0) + military-doctrine; soviet-doctrine for the
  opposing school; war-concepts (glossary, `warwiki.py look TERM`).
- Every turn / battle: **war-language** (UP: the situation in doctrine terms -> THINK: intent,
  form of manoeuvre, a task and purpose per unit -> DOWN: concrete orders -> CHECK) and **army-log**
  (read, log and evaluate both sides; `armylog.py`). Before the first real game write
  **`LEXICON.md`** in this skill folder (`warlang.py lexicon`): units -> roles, terrain -> OAKOC,
  rules -> effects, victory -> end state, task -> game actions.
- combat-models: The user's land salvo system and Lanchester (concentrate; make fights square when stronger, linear when weaker).
