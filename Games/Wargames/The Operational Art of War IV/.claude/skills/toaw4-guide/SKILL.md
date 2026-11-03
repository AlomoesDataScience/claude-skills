---
name: toaw4-guide
description: Starter guide to The Operational Art of War IV (Matrix/Slitherine 2017, the series begun by Norm Koger), an operational-level hex wargame and scenario editor covering a century of warfare - units built from individual equipment (TO&E), proficiency, readiness and supply, combat rounds that use up the player-turn (median-round turn advance and battlefield time stamps), variable initiative, the programmed opponent (Elmer), the scenario editor and equipment database, key commands, with a page map of its 176-page manual and the user's extra guides (what's new in 4.0, Elmer Assist primer, editing the equipment database, recolouring counters, scenario bitmaps, the older TOAW3 manual). Uses game-sources (manual lookups), game-ui (window driving), learn-to-play (method). Use when the user wants to play, learn or talk about The Operational Art of War / TOAW, or asks how one of its rules, screens, its editor or the equipment database works.
---

# The Operational Art of War IV - starter guide

Status 2026-10-29: the user added the manual and its companion files; read the outline,
introduction, turn and time-stamp rules, and the key commands. Not played yet.

## Files here (all in `Manuals/` since the user's reorganisation; mod scenarios in `Modded Scenarios/`)

- `Operational Art of War manual EBOOK.pdf` (176 pages, bookmarked, PDF page = printed page) and
  its `.txt`: **the TOAW IV manual, the main source**. `... TO PRINT.pdf` is damaged (no trailer,
  pdfinfo fails): use the EBOOK.
- `Whatsnew 4.0.docx` (text in `Whatsnew 4.0.txt`): changes in 4.0 that **override the manual**,
  plus appendices on naval combat, repair, sea interdiction, naval spotting, splitting TO&E lines
  and the equipment.nqp file.
- `KeyCommands.txt`: every hotkey (below are the main ones).
- Editor guides: `How to Edit the Equipment Database.pdf`, `Elmer Assist Primer.pdf` (letting the
  AI deploy and move your units), `ScenarioBMP-HowTo.pdf`, `Recoloring the Unit Counters.pdf`,
  `Equipment List.rtf` (the equipment database, 11 MB).
- Older: `TOAW3-Manual-[EBOOK].pdf` and `TOAW3 Scenario Descriptions` (many scenarios carry over).
  `Matrix_Catalog.pdf` and `Revised Catalogue sep14.pdf` are Matrix product catalogues (adverts).

## What it is (Claude's summary)

A general engine for operational warfare from WWI to modern and hypothetical wars: hexes of 2.5 to
50 km, turns of six hours to a week, units from a few vehicles to a corps. Each unit is a list of
real equipment (squads, guns, tanks, aircraft) with proficiency, readiness and supply; formations
cooperate badly with strangers; pushing troops tires them. Air, land and sea all exist, land and
sea in most detail. Hundreds of scenarios plus the same editor the designers use, with a large
equipment database and a programmed opponent (PO).

## The turn (sections 9-14)

Automatic bookkeeping (reinforcements, supply, readiness, events), then the phasing player gives
orders, then combat is resolved. Its signature: **combat uses up time**. Each battle is fought in
tactical rounds; a player-turn is ten rounds. In TOAW IV, after the combats the turn advances to
the round of the **median** combat (earlier versions used the longest one, so one stubborn fight
could "burn" the whole turn). Every unit's remaining movement is capped by the rounds left (round 7
leaves at most 30%). A battle that runs long leaves a **battlefield time stamp** on its hex: units
entering it or fighting there start from that later round. So: plan attacks to finish quickly,
mass for decisive odds, and do moves that matter before risky attacks. Variable initiative
(10.1) and loss-limit settings per unit (L key: how hard to push) shape every attack. Victory
(15) is by victory points from objectives and scenario events.

## Main keys (Manuals/KeyCommands.txt)

E end turn (only with the user's go), P combat planner, O order of battle, U unit report,
F formation dialog, D dig in, T tactical reserve, L loss limit (Shift-L the whole stack),
Z undo, M remaining movement/strength, Space hide units to read terrain, I range circles,
N/- next/previous unit, F12 Elmer deployment mode (Shift-F12 Elmer moves your units), F9 quick
save. Menu Delay 1 = "classic" right-click menus; other values = right-click moves or attacks.

## Manual map (pages)

Starting the game and options 8-19, interface 21-26, displays and menus 27-33, game definitions
and unit characteristics 34-48 (equipment 40, force 42, formation 47), the turn 49-62
(bookkeeping 50), orders 63-71 (initiative 63, control panel 64, attack planning 69), movement
72-78 (rail, sea, air, airborne, PO assist 77), engineering 79, **combat 80-91** (naval 83,
supporting fire 86, environment 87, flanks 89, assault ratios 90), turn end and time stamps
92-94, victory 94, information and player aids 95-116, **scenario editor 117-149**, scenario
design notes 150-157, appendices 158-172, hints 173.

## Modded scenarios (`Modded Scenarios/`, zipped)

Korea 2020, Hot War 1950, Astartes vs Traitors, Civil War Scenario Vanilla. Unzip one into the
game's scenario folder when the user wants to play it (check what is inside first).

## To learn next

1. Play a tutorial scenario (the game asks for a scenario folder on first start: choose
   Tutorials) with the user's go, mapping the screen with game-ui.
2. Read combat (80-91) and the what's-new naval appendices in full; summarise them here.
3. For our own game: the equipment-database and editor chapters show how a data-driven wargame
   is organised.
