---
name: fogk-guide
description: Guide to Field of Glory - Kingdoms (AGEOD / Slitherine, 2024; Rajas and Tribes DLC 2025), a turn-based medieval grand strategy game of realms, vassals, dynasties and population from 1054 - where its 300-page manual (text) and the 40-odd data tables copied from the install live, the manual's map, how a turn works (regions grouped into provinces and a demesne, population by social class assigned to tasks, buildings, authority and local authority, loyalty and revolt, Peers of the Realm with traits, vassals, diplomacy and legacy points as the score), its self-describing CSV data format, and how its battles can be exported to Field of Glory II Medieval. Use when the user wants to play, learn or talk about Field of Glory Kingdoms (or Empires, its ancient predecessor), look up a rule, read its data, or borrow its population, vassal, authority and data-format systems for our 4X.
---

# Field of Glory: Kingdoms

AGEOD makes the operational and strategic side of the AGEOD/Byzantine pair (the user, 2026-11-01).
AGEOD games are "thick and hard to figure out for players": go through the manual sections below
before playing. Installed 2026-11-01 for a look; everything worth keeping is copied here.
Field of Glory: Empires (2019, ancient) is the same design one era earlier.

## Files

- `Manuals/FOG_Kingdoms_Manual_Printer-Friendly.txt`: the rules (about 300 pages, PDF pages;
  the PDF has no bookmarks, so use `manual.py toc` and `grep`).
- `install/Data/*.csv`: the whole game as tables, semicolon-separated, **row 1 the column types**
  (INT, STRING, COMMENT, INT[]), row 2 the names: `GOVERNMENTS` (190), `DECISIONS` (150), `STRUCTURES`,
  `REGIONS`, `RULERS`, `CULTURES`, `ETHNICS`, `RESOURCES`, `TREATIES`, `MODIFIERS`, `EFFECTS`,
  `PopJobsProd` (social class x job productivity), `Impulses` (turn phases by speed), `UNITS`/`SQUADS`.
- `install/Scenarios/<start>/DATA/`: each scenario's REGIONS, SETUP and SETUP_FACTIONS (1054 campaign,
  Manzikert 1059, Gigi 1154, Nevsky 1236, tutorial...).
- Not copied: graphics (9 GB of .dds/.tga/.s4f).

## Manual map (printed sections)

Overview 3 (realms and demesne size 3.3, characters 3.4, diplomacy 3.5, army 3.6, population, tasks
and buildings 3.7, vassals 3.8) · Getting started 4 (difficulty 4.1, the UI 4.4, regional management
4.5) · Legacy 7 · Decisions 8 · Authority 9 · Population and culture 10 · Economy and buildings 11
(fortifications 11.4) · Diplomacy, conquest, trade 12 · Religion 13 (crusades 13.5, the Papacy 15.5) ·
Armies 14 (naval 14.5) · Combat 16 (field battles, raiding, sieges, **export to FoG II Medieval 16.5**) ·
Ledger 18 · Player's notes 19.

## How it plays (in my words)

- Turns (2 a year recommended); orders, then simultaneous resolution. Score = **Legacy**: the leader
  by enough after turn 100 wins; legacy also cheapens wars against weaker-legacy realms.
- The map is regions grouped into provinces; what you hold directly is your **demesne**, capped in
  size; over the cap costs authority. Vassals hold the rest, with their own loyalty.
- Each region has population units by social class (peasants, nobles...) assigned to six tasks
  (food, infrastructure, money, manpower, metals/equipment, piety and stewardship); productivity varies
  by culture, religion and terrain, and some classes can't do some jobs.
- Characters: the ruler's dynasty and Peers of the Realm with traits govern provinces, command
  armies, and may revolt or attempt coups.
- Difficulty gives the AI economic help (bigger demesne, easier large cities), **never battle bonuses**.
- Multiplayer by play-by-email challenges.

## Systems
- **Population**: population units by social class assigned to tasks, productivity from a class x
  job table modified by culture, religion and terrain (`PopJobsProd.csv`, 3.7, 10).
- **Politics**: demesne size cap; authority and local authority; loyalty and revolt risk per region;
  progress and disorder tokens (3.3, 7.2, 9).
- **Characters**: Peers of the Realm with traits as governors and commanders; coups and revolts (3.4, 9.5).
- **Diplomacy**: vassals with their own loyalty; legacy changes the cost of war (3.8, 12).
- **Victory**: Legacy points as the running score and the win condition after turn 100 (7).
- **AI**: difficulty as economic bonuses only, never in battle (4.1).
- **Tactical combat**: battles auto-resolve or export to Field of Glory II Medieval and come back (16.5):
  strategy and tactics from two studios joined by a file.
- **Modding**: everything in typed CSV tables (type row above the header row) plus BSF scripts:
  a good model for our engine's data files.

## Needs from the user
- Whether to play a Kingdoms campaign too, or only read it (it is long).

## War skills (the user 2026-11-02: call the military skills when playing; build on them)
- Level of war: **strategic + operational (battles are FoG II-style)**; domain: **land**. Vocabulary: military-operations (FM 3-0) + military-doctrine; military-operations (strategic/operational levels, principles of war) + war-concepts' strategy section (total/limited war, escalation, war economy, war termination); soviet-doctrine for the
  opposing school; war-concepts (glossary, `warwiki.py look TERM`).
- Every turn / battle: **war-language** (UP: the situation in doctrine terms -> THINK: intent,
  form of manoeuvre, a task and purpose per unit -> DOWN: concrete orders -> CHECK) and **army-log**
  (read, log and evaluate both sides; `armylog.py`). Before the first real game write
  **`LEXICON.md`** in this skill folder (`warlang.py lexicon`): units -> roles, terrain -> OAKOC,
  rules -> effects, victory -> end state, task -> game actions.
- combat-models: The user's land salvo system and Lanchester (concentrate; make fights square when stronger, linear when weaker).
