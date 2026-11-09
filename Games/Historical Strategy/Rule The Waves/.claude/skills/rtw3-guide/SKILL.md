---
name: rtw3-guide
description: "Starter guide to Rule the Waves 3, the naval ship-design and fleet-command game (1890-1970). Use when playing, learning or discussing RTW3, designing a warship, fighting a battle, or borrowing its systems."
keywords: "nws, warfare, simulations, player, grand, admiral, economy, budget, building, ships, hulls, armour, schemes, guns, torpedoes, machinery, aircraft, carriers, missiles, fleet, management, organisation, politics, influence, don't, control, wartime, operations, tactical, battles, day, night, air, strikes, radar, page, maps, manual, patch, pages, expanded, scenarios, quick, scenario, editor"
---

# Rule the Waves 3 - starter guide

Status 2026-11-01: installed (Steam, `~/.local/share/Steam/steamapps/common/Rule the Waves 3/`,
a Windows game under Proton). Manuals copied to `Manuals/` (keep the install untouched); intro
and outline read. Not played yet. (the user filed it under Space Strategy; it is a naval game.)

## Files (`Manuals/`, each with a .txt)

- `Rule the Waves 3 Manual Patch 2026.pdf` (149 pages; PDF page = printed page)
- `Rule the Waves Expanded Battles Manual EBOOK.pdf` (40 pages: scenarios, quick battles, the
  ship designer, the scenario editor)
- `RTW3 FAQ v1.00.pdf`, `Visual Parts Catalog 2.pdf` (ship parts for the designer's pictures),
  `whatsnew.pdf` (patch notes). Historical scenarios ship as text files in the install's
  `Scenarios/` (Dogger Bank, River Plate, Rheinübung, Eastern Solomons, Melee in the Med).

## What it is (Claude's summary)

You run a navy from the steam-and-iron era to early missiles. Each turn (a month) you get a
budget, design ships against a changing technology base, build, refit and scrap them, place
them in fleets and areas, and react to tension with other powers. Politics happens to you: you
can push but not decide when wars start. In war, battles are fought on a tactical map where you
command divisions (formations, speed, targets, torpedo attacks, air strikes, night actions).

## Manual map (PDF pages)

Introduction 7, installation 8, object of the game 12, world and economy 12, general 18,
building your fleet 23, construction choices 37, managing the fleet 45, fleet organisation 57,
politics and relations 59, wartime operations 67, tactical battles 77, your fleet in battle 79,
night combat 98, aircraft 104, air strikes 116, radar 123, missiles 123, Q&A 130, tips 131,
appendices 133-145.

## For our 4X engine

- Ship design against a real budget and real constraints, and the designer's balance of
  armour/speed/firepower: a model for "Component Design".
- "Influence, not decide, foreign policy" is the user's subfaction idea (play an entity inside a
  state with limited power); interfering ministers are characters with their own agendas.

## War skills (the user 2026-11-02: call the military skills when playing; build on them)
- Level of war: **tactical (fleet battles) + strategic (navy building)**; domain: **naval**. Vocabulary: military-doctrine (FM 3-90 tactics) first; military-operations (strategic/operational levels, principles of war) + war-concepts' strategy section (total/limited war, escalation, war economy, war termination); soviet-doctrine for the
  opposing school; war-concepts (glossary, `warwiki.py look TERM`).
- Every turn / battle: **war-language** (UP: the situation in doctrine terms -> THINK: intent,
  form of manoeuvre, a task and purpose per unit -> DOWN: concrete orders -> CHECK) and **army-log**
  (read, log and evaluate both sides; `armylog.py`). Before the first real game write
  **`LEXICON.md`** in this skill folder (`warlang.py lexicon`): units -> roles, terrain -> OAKOC,
  rules -> effects, victory -> end state, task -> game actions.
- combat-models: Hughes' salvo model fits naval combat directly - scouting decides who fires first; war-concepts: fleet in being, sea denial, line of battle, wolfpack.
