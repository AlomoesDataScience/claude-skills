---
name: eih-guide
description: Starter guide to Empires in Harm (v5.2, a fan successor to Avalon Hill's Empires in Arms), a 7-10 player strategic and diplomatic board wargame of European wars in the 18th and early 19th centuries (the 1792 campaign: Revolutionary France against the old powers) - monthly turns with political, reinforcement, naval, land, quarterly economic and time phases, diplomacy, minor countries, status quo powers and the HRE, corps and squadrons, depots and forage, sieges, victory and political points, peace conditions, plus the Middle East in Harm (Persia) and Spanish Dynastic Crisis add-ons, with a map of the rules (Word files converted to .txt) and the counter sheets. Uses game-sources (rule lookups), learn-to-play (method). Use when the user wants to play, run, learn or talk about Empires in Harm / Empires in Arms, wants a rules question answered, a power's diplomacy or campaign planned, or Claude to keep the game's records.
---

# Empires in Harm - starter guide

Status 2026-10-29: rules v5.2 read in contents and sequence of play; add-ons skimmed. Not played.

Files (the rules came as Word .doc; converted with `manual.py doc`):
- `Version_5.2.doc` / `.txt` (94 000 words): the rules. A change list for v5.1 → 5.2 opens the
  file, then the contents, then the rules by number (`grep -n "^7\.5" Version_5.2.txt`).
- `The_Middle_East_in_Harm.doc` / `.txt` (v1.2, Thomas Baader): Persia as a new major power, on
  Bob Kraus' Middle East map or Ragnar Krempel's combined map. `Middleast_version_11.gif`: that map.
- `The_Spanish_Dynastic_Crisis.doc` / `.txt`: optional rule (test version 1.0).
- `EIHv5.2.gif`: the map; `Counters_&_National_Cards_&_Status_Card.pdf` (56 pages, bookmarked):
  counter sheets, national cards and the status card to print.

## What it is (Claude's summary)

Grand strategy for seven to ten players, each a major power (France, Britain, Austria, Prussia,
Russia, the Ottomans, Spain, sometimes Poland; Persia with the add-on). One turn is a month; the map
is divided into areas whose number is their forage value (armies live off the land or depots).
Counters are corps and squadrons; generals lead them. Diplomacy decides most of the game:
alliances, calls to allies, peace terms, control of minor countries, revolts and the Holy Roman
Empire. Most game state lives on paper (national cards, status card, forms).

## Turn (rules 3.0)

1. **Political phase** (4): diplomacy, diplomacy on minors, declarations of war, call to allies,
   peace, alliances made and broken, minor country control, combined movement, Ottoman turmoil and
   random events (optional).
2. **Reinforcements** (5): naval then army, in fixed national orders.
3. **Naval phase** (6): each power in turn (Britain first, choosing its place if predominant)
   moves, supplies and fights its fleets; privateers last.
4. **Land phase** (7): each power in turn (France first, likewise) builds or removes depots,
   moves, checks supply, fights field and siege combats, guerrillas; then conquest, plunder and
   prisoner attrition for all.
5. **Economic phase** (8, only after March, June, September, December): victory points, money
   and manpower, loans, spending, political status, civil disorder, ceding, levies.
6. **Time record** (9): next month and its weather.

Victory points come from the economic phase (8.1) and political points (10); an alternate VP
system is optional (11); peace conditions in 12; the 1792 campaign setup in 14.

## How Claude helps

A 7-10 player game lives on bookkeeping: Claude can keep the status card and national cards,
run the quarterly economy, check moves and supply, play neutral or missing powers, or advise one
power's diplomacy. Every move in a game with people needs that player's go.

## To learn next

1. Read 7.5 (land combat) and 6.7 (naval combat): both changed a lot in 5.2.
2. Read 4.8 (peace) and 12 (peace conditions): they decide how wars end.

## War skills (the user 2026-11-02: call the military skills when playing; build on them)
- Level of war: **strategic (Napoleonic grand strategy)**; domain: **land+naval**. Vocabulary: military-operations (strategic/operational levels, principles of war) + war-concepts' strategy section (total/limited war, escalation, war economy, war termination); soviet-doctrine for the
  opposing school; war-concepts (glossary, `warwiki.py look TERM`).
- Every turn / battle: **war-language** (UP: the situation in doctrine terms -> THINK: intent,
  form of manoeuvre, a task and purpose per unit -> DOWN: concrete orders -> CHECK) and **army-log**
  (read, log and evaluate both sides; `armylog.py`). Before the first real game write
  **`LEXICON.md`** in this skill folder (`warlang.py lexicon`): units -> roles, terrain -> OAKOC,
  rules -> effects, victory -> end state, task -> game actions.
- combat-models: The user's land salvo system and Lanchester (concentrate; make fights square when stronger, linear when weaker). combat-models: Hughes' salvo model fits naval combat directly - scouting decides who fires first; war-concepts: fleet in being, sea denial, line of battle, wolfpack.
