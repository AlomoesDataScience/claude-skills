---
name: witp-guide
description: Starter guide to War in the Pacific - Admiral's Edition (2by3 Games / Matrix, 2009), the grand-scale WWII Pacific theatre wargame (daily turns, task forces, air and naval ops, logistics) - what it is, what the user's promo manual excerpt covers and lacks, the full manual's chapter map, and what to learn next. Uses game-sources (manual lookups), game-ui (window driving), learn-to-play (method). Use when the user wants to play, learn or talk about War in the Pacific / WITP / WitP AE, or asks how one of its systems works.
---

# War in the Pacific: Admiral's Edition - starter guide

Status 2026-10-29: the PDF here is a **promo excerpt** (75 pages) of the ~300-page manual, with
an advert for the War Plan Orange add-on (1922-1930 dreadnought-era campaigns). Not played yet.

Files: `WITP-Manual-[Promo].pdf` and `.txt`. What the excerpt has: the full table of contents
(PDF p5-12), introduction and setup chapters (1.0-2.x: installation, hotkeys, game style and
realism options such as fog of war, the December 7th surprise, reliable US torpedoes, realistic R&D),
a slice of naval movement (off-map movement, the Panama canal, the Mediterranean, the sea
connection table), part of chapter 8 (ground units, PDF p37), chapter 10 (spotting, p42), the
designer's notes (21.0, p51) and the index (p66). **Missing:** sequence of play (3.0), most of the
main display, air operations (7.x), naval operations, logistics, production. Get the full manual
(it ships with the game: Matrix/Slitherine) before trying to play seriously.

## What it is (Claude's summary)

A monster wargame: the whole Pacific war from 1941 at the level of individual ships, air
squadrons and ground units on a hex map of the Pacific and Indian Ocean, played in daily (or
multi-day) turns with simultaneous plotting and resolution. Orders go mostly to task forces
(naval), air units (missions, ranges, escorts) and ground units, and logistics - fuel, supply,
port capacity, shipping - decides what is possible. Games last months to years of real time;
PBEM (play by e-mail) is the usual way to play against people. Expect to lean on the manual,
the Matrix forums and community guides far more than in the other games.

## Full manual map (printed pages, from the contents)

Introduction 13, getting started 16 (interface, hotkeys 17, main menu and options 19-27, new game
29, PBEM 31), **sequence of play 31**, main display 34 (map, terrain, tactical/jump/strategic
maps, icons), information displays 52 (intelligence, scoring, list screens), air units and the air
sequence of play 155, ground units 176, spotting, logistics and the rest, designer's notes 308,
credits, index.

## To learn next

1. Ask the user for the full manual (or find it in the game folder once installed).
2. Then: sequence of play, task force basics, air missions and logistics, in that order, with
   a small scenario (the tutorial or a short Guadalcanal-type scenario) before any campaign.

## War skills (the user 2026-11-02: call the military skills when playing; build on them)
- Level of war: **operational + strategic (theatre)**; domain: **naval+air**. Vocabulary: military-operations (FM 3-0) + military-doctrine; military-operations (strategic/operational levels, principles of war) + war-concepts' strategy section (total/limited war, escalation, war economy, war termination); soviet-doctrine for the
  opposing school; war-concepts (glossary, `warwiki.py look TERM`).
- Every turn / battle: **war-language** (UP: the situation in doctrine terms -> THINK: intent,
  form of manoeuvre, a task and purpose per unit -> DOWN: concrete orders -> CHECK) and **army-log**
  (read, log and evaluate both sides; `armylog.py`). Before the first real game write
  **`LEXICON.md`** in this skill folder (`warlang.py lexicon`): units -> roles, terrain -> OAKOC,
  rules -> effects, victory -> end state, task -> game actions.
- combat-models: Hughes' salvo model fits naval combat directly - scouting decides who fires first; war-concepts: fleet in being, sea denial, line of battle, wolfpack. air: sorties as salvos, interception, air supremacy/interdiction/close air support (war-concepts).
