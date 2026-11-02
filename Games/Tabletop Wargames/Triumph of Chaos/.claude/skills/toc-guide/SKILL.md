---
name: toc-guide
description: Starter guide to Triumph of Chaos v2 DELUXE (Clash of Arms, D B Dockter), a two-player card-driven board wargame of the Russian Civil War 1918-1921 (RED vs WHITE) in the Paths of Glory tradition - turn sequence (political, action, logistics phases), political cards and 18 factions, action cards (operations, events, replacements, strategic redeployment), movement, combat, supply and attrition, leaders, with a page map of the v2.3 rulebook (May 2020; searchable .txt next to it). Uses game-sources (rulebook lookups), learn-a-game (method). Use when the user wants to play, learn, set up or talk about Triumph of Chaos / ToC, wants a rules question answered, or wants help planning a move or playing it on Vassal.
---

# Triumph of Chaos v2 DELUXE - starter guide

Status 2026-10-29: the **Rulebook** v2.3 (33 pages) is here and was read in outline and
introduction. The separate **Supplement** (political phase and faction rules, campaign setup, the
1918 introductory scenario, example of play, designer notes - sections 14-19) is not in the
folder: ask the user for it before a first game.

Files: `ToCv2 Rulebook MAY 2020 v2.3.pdf` and its `.txt`. PDF page = the rulebook's page number.
Its bookmarks are messy (whole rule sentences): use the contents on PDF p2 or
`manual.py grep "ToCv2 Rulebook MAY 2020 v2.3.txt" "^ *8\.[0-9]" -C 1` style searches.

## What it is (Claude's summary)

A strategic two-player board game: RED (the Bolsheviks) against WHITE (the anti-communist side),
across Russia, its breakaway republics and the foreign interventions. Card driven: each side
plays from its own deck of action cards, and a shared political deck decides which of 18 factions
(republics, neighbouring countries, major powers) lean which way. The design borrows openly from
Paths of Glory, so CDG habits carry over. Campaign game about 8-10 hours; the 1918 introductory
scenario 2-3 hours and balanced (played at the WBC). Online play via the Vassal module.

## Turn sequence (rulebook 5.0, p9-10)

- **Prep**, then the **Political Phase** (turns 1-9): each side adds bluff and influence cards to
  its hand and secretly places three action cards, one each in the RED, WHITE and OTHER
  political boxes on the map; political cards then shift factions.
- **Action Phase** (6.0, p11): players alternate action cards, each used one way - activate spaces
  for movement and combat, play the event (an asterisk event is removed from the game afterwards),
  take replacement points, or strategic redeployment.
- **Logistics Phase** (10.6): attrition for units out of supply, rebuilding, upkeep of markers.

## Rule map (rulebook sections and pages)

Components 3.0 p4 (map, forces and leaders, info counters, political and action cards);
definitions 4.0 p8; movement 7.0 p12 (activation, special actions, stacking, seasons, supply,
neutrals); combat 8.0 p15 (sequence, modifiers and column shifts, resolution, losses, retreat,
advance, special assets); strategic redeployment 9.0 p20 (on and off map); supply and attrition
10.0 p21 (sources, limited and out of supply, control markers); replacements and reinforcements
11.0 p22; leaders 12.0 p25 (capabilities, purchase, elimination, movement, inactivity);
miscellaneous 13.0 p27 (special RED, WHITE and other forces, special geography including the Far
East, in-fighting, Socialist Revolutionaries, card clarifications, optional rules). Changes in
v2.3 against the printed rules are marked in red in the PDF.

## How Claude helps with a board game

Claude can't move the pieces: it answers rules questions with page references, keeps track of a
game state the user describes or photographs, plans card play and moves, or plays through the
Vassal module window with game-ui (with the user's go for every move in a game against a person).

## To learn next

1. Get the Supplement; read the 1918 scenario setup and the political phase rules.
2. Read combat 8.0 in full and write down the combat table logic here.
3. Ask whether the user plays on the table or on Vassal.
