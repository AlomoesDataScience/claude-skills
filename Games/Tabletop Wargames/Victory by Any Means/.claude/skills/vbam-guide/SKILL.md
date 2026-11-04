---
name: vbam-guide
description: Starter guide to Victory by Any Means 2nd Edition (VBAM), a generic space-empire campaign system for tabletop (freeform 4X like Master of Orion, or historical scenarios for any setting) - campaign moderator or moderator-less play, random galaxy generator, empire setup and starting forces, turn phases (economic, turn orders, movement, politics, supply, combat), diplomacy and intel missions, supply, encounters, space, orbital and ground combat, and the With a Purpose add-on (campaign objective system), with page maps of both books (searchable .txt). Uses game-sources (rule lookups), learn-to-play (method). Use when the user wants to play, run, learn or talk about VBAM / Victory by Any Means, set up a space campaign (also for Star Fleet Battles, Starfire or Hellfire battles), or have Claude be its moderator.
---

# Victory by Any Means (2nd Edition) - starter guide

Status 2026-10-29: both books read in contents, introduction and sequence of play. Not played.

Files: `Victory_by_Any_Means_Campaign_Guide_(2E).pdf` (164 pages, bookmarked) and
`With_a_Purpose_(2E).pdf` (106 pages, bookmarked: campaign objectives), each with a `.txt`.
Rules are numbered `3.4.7.1`: `manual.py grep "Victory_by_Any_Means_Campaign_Guide_(2E).txt"
"3\.6\.2"`. The contents is on PDF p2.

## What it is (Claude's summary)

A campaign layer that sits above any space battle game (or resolves battles itself): players run
empires on a star map of systems joined by jump lanes, either as open 4X competition or as a
"historical" scenario in an existing setting. A **campaign moderator** is recommended (fog of war,
hidden orders), though it can be played without one (1.4). The book suggests keeping each
empire's records in documents and spreadsheets - well suited to Claude doing the bookkeeping.

Turn (3.0): **economic** (system and commerce income, maintenance), **turn orders** (written
orders on imperial asset sheets: construction, tech, updates; resolved, then the treasury
updated), **movement** (ships, cargo, census, landings, trade routes, convoys, towing, stealth),
**politics** (intel, first and sustained contact, diplomatic states, treaties, war, armistices,
covert diplomacy, espionage, sabotage, propaganda), **supply** (supply points, depots, routes,
supply ships), **combat** (encounters, space combat, orbital bombardment, ground combat,
blockades). Setup (2): scenario, empires, period, optional rules, map (generic maps or the random
galaxy generator: hub, rings, last ring, system generation), homeworlds, colonies, starting forces.

**With a Purpose** adds a campaign objective system (goals that give empires a reason to fight),
campaign changes, scenarios and more optional rules.

## How Claude helps

Claude can be the moderator: generate the galaxy, keep each empire's asset sheet, resolve orders
in phase order with hidden information kept per player, and hand battles to SFB, Starfire or
Hellfire when the players want them fought on the table.

## War skills (the user 2026-11-02: call the military skills when playing; build on them)
- Level of war: **strategic (campaign)**; domain: **space**. Vocabulary: military-operations (strategic/operational levels, principles of war) + war-concepts' strategy section (total/limited war, escalation, war economy, war termination); soviet-doctrine for the
  opposing school; war-concepts (glossary, `warwiki.py look TERM`).
- Every turn / battle: **war-language** (UP: the situation in doctrine terms -> THINK: intent,
  form of manoeuvre, a task and purpose per unit -> DOWN: concrete orders -> CHECK) and **army-log**
  (read, log and evaluate both sides; `armylog.py`). Before the first real game write
  **`LEXICON.md`** in this skill folder (`warlang.py lexicon`): units -> roles, terrain -> OAKOC,
  rules -> effects, victory -> end state, task -> game actions.
- combat-models: the salvo model plus the user's space-warfare essay (military-theory shelf) - tracking, point defence, low staying power, who launches first; war-concepts: space weapon, kill chain, A2/AD.
