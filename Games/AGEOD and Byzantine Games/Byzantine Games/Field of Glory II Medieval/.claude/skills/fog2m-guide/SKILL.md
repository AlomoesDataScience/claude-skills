---
name: fog2m-guide
description: Guide to Field of Glory II - Medieval (Byzantine Games / Slitherine, 2021), a turn-based tactical battle wargame of medieval armies on a square grid with 3D models - where its manual (117 pages, text with page numbers) and the data and scripts copied from the install live, the manual's chapter map, how battles work (action points, Points of Advantage, shooting arcs and ranges, impact then melee, combat strength by ranks, four cohesion states tested on 2d6 with quality re-rolls, rallying, autobreak, pursuit), how it is built and modded (Archon engine BSF scripts, Squads.csv unit table, .s4f 3D models with per-unit animation .txt, global mods, map editor) and its link to Field of Glory - Kingdoms. Use when the user wants to play, learn or talk about Field of Glory II or Medieval, plan a battle, look up a combat rule, mod it, or borrow its combat and morale systems for our games.
---

# Field of Glory II: Medieval

Byzantine Games makes the tactical side of the AGEOD/Byzantine pair (the user, 2026-11-01). Installed
2026-11-01 for a look and **one game played together**, then likely uninstalled: everything worth
keeping is copied here. FoG II (ancient) is the same system with different armies.

## Files

- `Manuals/FOG2 Medieval Manual Printer-Friendly.txt` (from the PDF; page markers are PDF pages,
  the printed page numbers run about 2x+ because spreads are 2 pages): the rules.
- `install/`: text copied from the install: `Data/Squads.csv` (360 unit types, one row each, with a
  comment row explaining the columns), `Data/Battle/Scripts/*.BSF` (38 battle-logic scripts:
  `CloseCombatLogic.BSF`, `FightMelee.BSF`, `FallBack.BSF`...), `Core/*.BSF` and `Core/*.TXT`,
  `Data/Battle/Units/*.txt` (each 3D unit's animation table), campaigns and tools text.
- Not copied: 3D models (`.s4f`, 1145) and textures (`.dds`, 6510), 7.9 GB.
- Read the rules with `manual.py grep "Manuals/FOG2 Medieval Manual Printer-Friendly.txt" REGEX`.

## Manual map (PDF page)

Introduction 6 · Nations 9 · Quick, Custom, Epic battles 26-32 · Multi-battle campaigns 33 · Battle
39 · Generals 46 · Deployment and orders 48 · Shooting 65 · Close combat 67 · Cohesion 73 · Banners
77 · Terrain 77 · Disorder 80 · Victory 80 · Multiplayer 87 · Hints 88 · Map editor 91 · Modding
102 · Appendices 103 · Tactics 107 · Design notes (AI) 111 · Field of Glory Kingdoms battles 114.

## How a battle works (in my words)

- Units of models (infantry usually 8 models in 2 ranks, cavalry 4; 30 or 60 men per model by battle
  size) on a square grid; each turn every unit spends action points to move, turn, shoot or charge.
- **Points of Advantage (POA)**: every factor (troop type, armour, weapon, terrain, height, general,
  flank) is a POA bonus; the net difference decides the fight. 100 POA is about 33%; the difference
  caps at 200. Separate tables for impact, melee and shooting.
- **Shooting**: range by weapon (foot bow 2/4 squares, heavy artillery 6/9); arc 45 degrees, half
  effect from 22.5; moving lowers it; armour on a sliding scale; skirmishers are hard to hit.
- **Close combat**: a charge resolves as impact (only the men in contact), then melee each turn until
  one side breaks. Combat strength counts only the first 2 ranks of foot (4 models of horse); the
  bigger side overlaps. Mouse-over shows Win:Draw:Lose from 1000 simulated resolutions.
- **Cohesion**: Steady > Disrupted > Fragmented > Broken (routing). Tests on 2d6, need 6; Untrained
  re-roll 6s, Superior 1s, Elite 1s and 2s; triggers: heavy shooting losses (~10%), losing a combat,
  a friend breaking nearby, a general lost. Rally tests each turn. Autobreak near 50% losses (sooner
  for raw troops). Broken units rout; mounted victors usually pursue.
- **AI**: same rules and no hidden bonuses at every level; difficulty changes the force balance.

## Systems
- **Tactical combat**: Points of Advantage: every factor is a bonus on one scale, 100 POA ~33%, net
  difference capped at 200; impact then melee; only front ranks count, extra ranks give staying power (13.1-13.2).
- **Tactical combat**: four cohesion states with 2d6 tests and quality as re-rolls instead of
  modifiers; autobreak by losses; pursuit chances by troop type (14).
- **UI**: Win:Draw:Lose odds shown by simulating the combat 1000 times; detailed tooltips list every
  modifier (13.6). A good answer to "rules too thick to read".
- **AI**: plays by the player's rules at all levels; difficulty = army balance; auto-deploys by
  terrain (heavy foot on open ground, cavalry on the open wing) (31.1).
- **Modding**: units in one CSV with a comment row per column; game logic in readable BSF scripts;
  global mods loaded from Documents without touching the install; 3D unit models with a text
  animation table (frame ranges per action, sounds, script calls) (25).

## Playing a game with the user

The plan (2026-11-01): one Quick or Custom battle, the user present. Use game-ui (find the window class
first; it runs under Proton) and learn-a-game's method: read Battle 39-48 before the first move, check
the screen after every order, never end a turn without the user's go.

## Needs from the user
- When to play the battle, and which (a Quick Battle is the smallest).
