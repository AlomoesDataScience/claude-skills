---
name: hos-guide
description: "Starter guide to Hex of Steel, a WWII-and-beyond hex wargame in the Panzer General tradition. Use when playing, learning or discussing Hex of Steel or a rule or screen of it."
keywords: "native, linux, build, victory, points, commander, rank, core, units, unit, heroes, action, damage, modifiers, soft, hard, air, attack, armour, shares, terrain, recon, morale, encirclement, entrenchment, supply, lines, policies, page, map, manual, pdf, pages, bookmarked, searchable, txt, game-sources, lookups, game-ui, window, driving, learn-to-play, method, play, learn"
---

# Hex of Steel - starter guide

Status 2026-10-29: manual (official, updated 17/10/2024) outline read, plus victory points,
damage, supply, action points and policies. Not played yet.

Files: `Manual.pdf` (63 pages, bookmarks: one page per topic) and `Manual.txt`. PDF page numbers
match the manual's own. Search: `manual.py grep Manual.txt "entrench|encircl" -C 2`.

## What it is (Claude's summary)

A turn-based, one-unit-per-hex operational wargame in the Panzer General mould, solo-developed,
with scenarios and campaigns from WWI-era to modern and a map/scenario editor. You command a
**commander** whose rank (from XP) sets how many **core units** carry over between scenarios; core
units gain rank, XP and can become heroes; you buy, upgrade and customise units in a store.

## Rules worth knowing (manual pages)

- **Victory points** (p5-6): normal, secondary and major VPs; scenarios are usually won by taking
  all major VPs; secondary VPs give extra commander XP (more core slots later).
- **Action points** (p56): two per unit per turn - move, attack, repair or a special action, in
  any order, but not the same action twice (recon units may move twice; an overrun gives a free
  second attack; diving, paradrops and ammo/fuel resupply are free).
- **Damage** (p23): soft attack against infantry, hard against armour, air against aircraft;
  damage scales with the attacker's remaining HP; only part of the target's armour counts,
  depending on attacker type; terrain, adjacent recon, commanders, hills (defender), landings,
  morale, encirclement (from two surrounding enemies on) and entrenchment levels all modify it.
  Hold SHIFT on the battle preview to see the whole breakdown - use that instead of guessing.
- **Supply** (p38-39, complex supply on): a supply line runs to the best nearby city; villages
  give little, enemies on the line cut it, sea crossings weaken it. A unit either attacks or
  resupplies in a turn; HP comes back at most half per turn and costs XP (new recruits); resupply
  costs money (ships, planes, heavy tanks triple).
- **Policies and HQ points** (p57, optional): one policy per category, +5 HQ points a turn (+1 per
  captured enemy VP); with policies on, generals cost HQ points instead of money.
- Also covered: tiles and modifiers 7, unit types 9, stats 13, heroes 16, store 17, upgrading 22,
  morale 24, supportive fire 25, paratroopers, trains, submarines, destroyers, carriers, landings,
  engineers and bridges 26-35, generals 37, weather 40, mines 43, encirclement 45, retreat and
  surrender 46, capture 48, radar 49-50, entrenchment 51, depots 52, reinforcements 53, partisans
  54, marines 55, political units 59, zone of control 60, upkeep 61, manpower 62.

## To learn next

1. Find the window class with the game open; map the main screen and the store with game-ui.
2. Play the first tutorial scenario with the user's go; record hotkeys (p4) and what ends a turn.
3. Use the SHIFT breakdown on real attacks to build a feel for the damage model.

## War skills (the user 2026-11-02: call the military skills when playing; build on them)
- Level of war: **operational (hex)**; domain: **land**. Vocabulary: military-operations (FM 3-0) + military-doctrine; soviet-doctrine for the
  opposing school; war-concepts (glossary, `warwiki.py look TERM`).
- Every turn / battle: **war-language** (UP: the situation in doctrine terms -> THINK: intent,
  form of manoeuvre, a task and purpose per unit -> DOWN: concrete orders -> CHECK) and **army-log**
  (read, log and evaluate both sides; `armylog.py`). Before the first real game write
  **`LEXICON.md`** in this skill folder (`warlang.py lexicon`): units -> roles, terrain -> OAKOC,
  rules -> effects, victory -> end state, task -> game actions.
- combat-models: The user's land salvo system and Lanchester (concentrate; make fights square when stronger, linear when weaker).
