---
name: stars-guide
description: Starter guide to Stars! (1995-96, Jeff Johnson and Jeff McBride; Empire Interactive), the classic turn-based space 4X built for play-by-email - race creation with advantage points (primary and lesser racial traits, habitability, growth, factories and mines), production queues, research fields, ship and starbase design, fleets and waypoints, colonisation, mining the three minerals, freight, combat and battle plans, minefields, cloaking and scanning, diplomacy, and "the guts" chapters with the exact formulas, with a page map of Stars.pdf (the 277-page user guide, bookmarked; searchable .txt). Uses game-sources (lookups), learn-to-play (method). Use when the user wants to play, learn or talk about Stars!, design a race or ship, check a formula, or borrow its ideas for our own 4X engine.
---

# Stars! - starter guide

Status 2026-11-01: user guide outline read. Game not installed here.

File: `Stars.pdf` (Stars! User Guide, 277 pages) and `Stars.txt`. PDF page numbers below.

## What it is (Claude's summary)

A compact, number-rich space 4X from the mid-90s, played in simultaneous turns, classically by
email with a host generating turns. Its signature is the **race wizard**: you spend advantage
points on a primary racial trait (such as Hyper-Expansion, Super Stealth, War Monger, Claim
Adjuster, Inner Strength, Space Demolition, Packet Physics, Interstellar Traveler, Alternate
Reality, Jack of all Trades), lesser traits, the temperature/gravity/radiation range your people
can live in, growth rate and how productive factories and mines are. Minerals are Ironium,
Boranium and Germanium; planets are worth more the closer they suit your race. Ships are designed
on hull slots; battles resolve automatically on a small board from battle plans.

## Guide map (PDF pages)

Introduction 11, getting started 17, things every player should know 37, the screen 45, playing
65, production 89, research 101, ship and starbase design 107, fleets 117, navigation 129,
colonisation 135, mining 139, freight 143, combat basics 149, patrolling 167, scanning and
cloaking 171, reports 177, diplomacy and trade 181, **race creation 185**, predefined races 205,
alternate reality races 213, **the guts of combat 217, cloaking 227, mass drivers 231, minefields
235**, back of the book 239.

## For our 4X engine

- Race creation from a points budget with real trade-offs is the user's "Nation Creation"
  (points, doctrines, species biomes) in miniature; the advantage-point balance is worth copying.
- Simultaneous turns with a host = a clean multiplayer model; mass-driver packets are an early
  version of "throw rocks/missiles across systems" from his space warfare notes.

## War skills (the user 2026-11-02: call the military skills when playing; build on them)
- Level of war: **strategic (4X)**; domain: **space**. Vocabulary: military-operations (strategic/operational levels, principles of war) + war-concepts' strategy section (total/limited war, escalation, war economy, war termination); soviet-doctrine for the
  opposing school; war-concepts (glossary, `warwiki.py look TERM`).
- Every turn / battle: **war-language** (UP: the situation in doctrine terms -> THINK: intent,
  form of manoeuvre, a task and purpose per unit -> DOWN: concrete orders -> CHECK) and **army-log**
  (read, log and evaluate both sides; `armylog.py`). Before the first real game write
  **`LEXICON.md`** in this skill folder (`warlang.py lexicon`): units -> roles, terrain -> OAKOC,
  rules -> effects, victory -> end state, task -> game actions.
- combat-models: the salvo model plus the user's space-warfare essay (military-theory shelf) - tracking, point defence, low staying power, who launches first; war-concepts: space weapon, kill chain, A2/AD.
