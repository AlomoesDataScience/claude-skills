---
name: swr-guide
description: Starter guide to Star Wars Rebellion (1998, Coolhand Interactive / LucasArts), the galactic grand-strategy game of Alliance vs Empire - sectors and systems, popular support and uprisings, mines, refineries and maintenance, construction yards, shipyards and training facilities, fleets and troops, characters with diplomacy/espionage/combat/leadership ratings and the Force, missions (diplomacy, recruitment, espionage, sabotage, assassination, abduction, rescue, inciting and subduing uprisings, Jedi training), decoys, special forces, tactical space battles, and victory by capturing the enemy headquarters and leaders - with the manual and the Prima strategy guide (both scans, OCR'd to .txt). Uses game-sources (lookups), learn-to-play (method). Use when the user wants to play, learn or talk about Star Wars Rebellion (Supremacy), or study its characters-and-agents system for our own 4X engine (the user's Tactics doc names it).
---

# Star Wars Rebellion - starter guide

Status 2026-11-01: `Star_Wars_Rebellion-Manual.pdf` (167 pages) and `Star Wars Rebellion Prima
Guide.pdf` (276 pages) are image scans; OCR to `.txt` beside them (game-ui `ocr.py pdf`, 200 dpi;
expect OCR noise, worst on art pages; check numbers against the page image with `pdftoppm -f N
-l N`). Game not installed here (the user doesn't own it on Steam).

## Page maps (PDF pages)

Prima guide (printed page + 3 = PDF page): ch.1 introduction 4, ch.2 exploring the galaxy 18,
ch.3 developing your infrastructure 30, ch.4 building fleets 54, ch.5 characters and missions 76,
ch.6 diplomacy 104, ch.7 acquiring and developing systems 121, ch.8 ship-to-ship and planetary
combat 132, ch.10 playing as the Empire 176, ch.9 playing as the Rebel Alliance 184 (the OCR'd
contents list 181/173 for ch.9/10), ch.11 head-to-head 196.

Manual (no usable bookmarks: they are just page-image names; topic hits from the OCR text,
approximate): production and resources (mines, refineries) 12, 25-36; missions 28-46, 57-68;
the Force and Jedi 43-45, 79-91; encyclopedia 39-40, 62-83; hotkeys 63-64; victory 65, 118;
uprisings 87-108; espionage, sabotage, assassination, abduction 93-100; decoys 101-102;
diplomacy 87, 102; combat 93-149 (tactical battles 138-149); bombardment 120-131; Death Star
103, 117, 122, 147; multiplayer 152-162.

## What it is (Claude's summary)

A two-sided strategy game over the whole Star Wars galaxy: the Alliance or the Empire, each with
a hidden headquarters. Systems give resources only if loyal; **popular support** decides who
holds them, and uprisings break out where support and garrisons fail. Mines and refineries feed
construction; ships and troops cost upkeep (maintenance). The heart is **characters**: named
heroes (and generic agents) with ratings in diplomacy, espionage, combat and leadership, some
Force-sensitive, sent on missions in teams with decoys against enemy defenders. You win by taking
the enemy headquarters and capturing its key leaders, or by holding the galaxy.

## For our 4X engine

The user's Tactics doc: "We're pulling from Star Wars Rebellion here" for character-vs-character and
character-vs-agent battles (with "some issues with how it does agents and characters"). Take:
missions as contests of ratings, teams and decoys, captured characters, popular support as the
real currency of control.

## Needs from the user

- Your Tactics doc says Rebellion has "some issues with how it does agents and characters".
  What are they? I'd like to know before copying its model.
