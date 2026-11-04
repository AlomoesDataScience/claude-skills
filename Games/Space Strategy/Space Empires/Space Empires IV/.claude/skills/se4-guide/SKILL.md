---
name: se4-guide
description: Starter guide to Space Empires IV Deluxe (Malfador Machinations, 2000/2005), a space 4X game - what it is, the first-turns flow (design a ship, build queue, research, warp-point exploration, colony ships, facilities, diplomacy), hotkeys, victory conditions, the races and modding, with a page map of SE4DeluxeManual.pdf (searchable as SE4DeluxeManual.txt; PDF page = printed page + 7). Uses game-sources (manual lookups), game-ui (driving the game window), learn-to-play (method). Use when the user wants to play, learn, mod or talk about Space Empires IV / SE4, or asks how one of its rules, screens or designs works.
---

# Space Empires IV Deluxe - starter guide

Status 2026-10-29: manual read through the introduction and the quick walkthrough ("A Day in the
Life of a Galactic Emperor"); the rest is mapped below. Not played yet. A Windows game (likely run
through Wine/Proton here: find its window class with `wmctrl -lx` when it is open).

Files: `SE4DeluxeManual.pdf` (118 pages, no bookmarks) and `SE4DeluxeManual.txt`. **PDF page =
printed page + 7** (printed contents page iv is PDF page 4; "A Day in the Life", printed p4, is PDF
p11). Look up: `manual.py grep SE4DeluxeManual.txt "warp point" -C 2`,
`manual.py toc SE4DeluxeManual.txt --pages 8` for the full contents.

## What it is (Claude's summary)

Classic space 4X (explore, expand, exploit, exterminate) by Aaron Hall: you run a whole empire, not
single ships. Star systems are joined by **warp points**; inside a system you see planets,
asteroid fields, storms and nebulae. Three resources - **minerals, organics, radioactives** (blue,
green, red) - come from planets, boosted by facilities. You **design every ship yourself** from
components on a hull, research a tech tree, colonise planets (breathable atmosphere = full
population; others need domes and stay small), build facilities, and talk, trade or fight with AI
races. Turn-based with simultaneous play options; TCP/IP and play-by-e-mail multiplayer; very
moddable (data files and graphics, mod manager).

## First turns (walkthrough, printed p4-14 / PDF p11-21)

1. Quick Start or New Game; the view opens on the home planet. Planet Report window (right): size,
   atmosphere, climate and resource percentages decide good colonies (huge, breathable, mild, high
   %). System window (left); Galaxy window (lower right) to change system. Colonisable planets carry
   an asterisk (green compatible, red needs domes); population bars mark colonies.
2. **Design** (F3): Create > Ship, choose hull size and type; every ship needs a bridge, life
   support and crew quarters, then engines, supply storage, weapons. Colony ships must be at least
   50% colony module (rock/ice/gas colony per planet type).
3. **Build queue** (Q) on a planet: add designs or facilities; click again for more, click in the
   queue to remove.
4. **Research** (F6): white topics are available, green in progress, grey done; right-click a topic
   for its description. Ship Construction early (destroyer hull).
5. **End turn** (F12 or the End Turn button) - only with the user's go once a real game runs.
6. Explore: select the ship, **Warp** (W), pick a warp point. **Colonise** (C) with a colony ship.
7. New colonies in a new system: build a **spaceport** first (shares the system's goods with the
   empire) and a **resupply depot**, then facilities matching the planet's best resource.
8. **Empires** (F9): diplomacy - start with a gift of resources, then non-aggression or trade
   alliance; fight one war at a time. Moving into an enemy location asks whether to fight.

## Manual map (printed page numbers; add 7 for the PDF)

Game interface 15-50 (opening screen, new game and its settings, victory conditions 23, main
screen panels 26-31, command panel: design, planets, colonies, ships, research, empires, log,
empire status 31-42, order buttons 42+), the races 70-74 (Eee Consortium, Fazrah, Jraenar,
Krill, Norak, Phong, Piundon, Praetorian, Sallega, Sergetti, Terran, Toltayan, Ukra-Tal, Xiati,
XiChung), communications/diplomacy 81, modding guide 85-96 (files, graphics, tools), TCP/IP games
97-99, troubleshooting, extras and cheat codes 100-106, index 108.

## To learn next

1. Read the combat chapter and ship-design details (`grep "Combat|component|hull"`), then the
   victory conditions page, and note them here.
2. With the game open: find the window class, map the main screen and the design window with
   game-ui, and play the built-in Tutorial (main menu) with the user's go.
3. Keep a design notebook here (good early hulls and component layouts) as they are tested.

## War skills (the user 2026-11-02: call the military skills when playing; build on them)
- Level of war: **strategic (4X)**; domain: **space**. Vocabulary: military-operations (strategic/operational levels, principles of war) + war-concepts' strategy section (total/limited war, escalation, war economy, war termination); soviet-doctrine for the
  opposing school; war-concepts (glossary, `warwiki.py look TERM`).
- Every turn / battle: **war-language** (UP: the situation in doctrine terms -> THINK: intent,
  form of manoeuvre, a task and purpose per unit -> DOWN: concrete orders -> CHECK) and **army-log**
  (read, log and evaluate both sides; `armylog.py`). Before the first real game write
  **`LEXICON.md`** in this skill folder (`warlang.py lexicon`): units -> roles, terrain -> OAKOC,
  rules -> effects, victory -> end state, task -> game actions.
- combat-models: the salvo model plus the user's space-warfare essay (military-theory shelf) - tracking, point defence, low staying power, who launches first; war-concepts: space weapon, kill chain, A2/AD.
- The user's WMD mod: combat design reviewed against combat-models (salvo, point defence).
