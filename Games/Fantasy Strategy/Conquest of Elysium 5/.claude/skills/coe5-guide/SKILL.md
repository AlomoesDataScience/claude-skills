---
name: coe5-guide
description: Starter guide to Conquest of Elysium 5 (Illwinter, the makers of Dominions) - what the game is, how a turn works, resources, commanders and armies, combat, magic and the 24 classes, with a page map of the manual (coe5manual.pdf, searchable as coe5manual.txt) and what is still to learn. Uses game-sources (manual lookups), game-ui (driving the game window), learn-to-play (method). Use when the user wants to play, learn, mod or talk about Conquest of Elysium 5 / CoE5, or asks how one of its rules, classes or screens works.
---

# Conquest of Elysium 5 - starter guide

Status 2026-10-29: manual read in outline (introduction, map, recruitment, commanders, combat,
afflictions, classes overview). Not played yet; the game window has not been looked at.

Files (this folder): `coe5manual.pdf` (70 pages, bookmarked) and `coe5manual.txt` (page-numbered
text). Look things up with game-sources:
`manual.py grep coe5manual.txt "regex" -C 2` and `manual.py page coe5manual.txt N`.
The text is two-column: lines from both columns interleave; read the page image if it matters.

## What it is (Claude's summary)

A fast turn-based fantasy strategy game with a rogue-like streak, by Illwinter (same studio,
same art style and many of the same monsters as Dominions 6, which we know well: see the dom6
skills in `../Dominions 6/`). One turn = one month; seasons change income and movement (snow slows
armies). Random maps, random starting rituals and spells, random events and aggressive
independents. Last player standing wins; a player dies at once on losing every citadel on
Elysium (or the Sky / Agartha planes next to it) or every commander.

The heart of CoE5 is that each of the 24 **classes** plays a different game: different resources,
recruitment and win paths (a Druid grows forests and summons from herbs, a Dwarf Queen gets
workers on a schedule, a Scourge Lord drains life force through pyramids, a Necromancer raises
the dead, a Demonologist bargains with Inferno). Ten **planes** (Elysium, the Sky, Agartha, Inferno,
the Underworld, the elemental planes, the Primal plane, the Void...) mostly run in the background
and are reached by special sites and rituals.

## Core loop and rules (manual pages)

- **Map** (p11-15): squares; moving a commander into a square flags it, and resource squares stay
  yours until someone takes them. Shroud, then fog of war: you only see next to your armies and
  owned squares. Hotkeys p11 (`r` recruit, `y` END TURN - never without the user's go, `n`/`j`
  next/previous commander, `t` transfer troops, `?` hotkey list, F1 unit overview, F2 players).
- **Resources** (p9, p12): gold (population centres, mines, big citadels), iron (mines), gems,
  herbs and fungi (forest, swamp, jungle; seasonal), sacrifices, hands of glory, relics, weed and
  others: each class needs a different set. Structures can give fortification, vision, trade
  points (towns, ports, cities: trade administration `l`).
- **Recruitment** (p16-17): only in citadels; units cost once, **no upkeep**. Special recruitment
  offers (mercenaries, commanders in green/blue text) arrive at the start of a turn and are gone
  next turn; temples, libraries and towns raise their odds. Auto-recruit with Ctrl+click.
  Special locations (castle, desert palace...) sell their own units.
- **Commanders** (p17-20): only commanders move; ordinary units must be led. Commanders have
  action points; some gather a special resource (blue text) and are worth protecting.
- **Armies and combat** (p26-30): units deploy by placement rank (front = melee, middle = ranged
  and spells, back = pure mages and non-combat leaders), highest-HP units in the centre; large
  units take 2x2, giants 3x3. Stealth and scouts (stealth + acute senses) find hidden armies.
- **Damage, afflictions, healing** (p30-35): exhaustion, weakness, immobilising effects (earth
  grip, entanglement, ice, paralysis) with strength checks to break free; units heal 10% max HP a
  month; many non-living units never heal; regenerators on the winning side may rise again.
  Resistance rolls p35.
- **Magic** (p35-37): spell levels per discipline, boosters (generic and per path), scrolls (new
  spells, magic maps, teleports), magic armour.
- **Classes** (p37-66): class powers and rituals; Rituals of Mastery (lesser/normal/grand) teach
  new rituals of level 1/2/3 and can promote the caster. One page per class: Baron p40,
  Necromancer 41, Demonologist 42, Witch 43, High Priestess 44, Bakemono 45, Barbarian 46,
  Senator 47, Pale One 48, Druid 49, Burgmeister 50, Warlock 51, Priest King 52, Troll King 53,
  Enchanter 54, High Cultist 55, Dwarf Queen 56, Voice of El 57, Illusionist 58, Markgraf 59,
  Dryad Queen 60, Scourge Lord 61, Cloud Lord 62, Kobold King 63, Monkey Maharaja 64,
  Raksharaja 65, Guildmaster 66.
- Command line options p67 (modding, map editor from the Mods menu p8).

## Carry-over from Dominions

Same studio: expect familiar ideas (commanders lead units, independents defend squares, mod
files in a .dm-like format, Steam Workshop mods, `?` for hotkeys, right-click for info). Check
each assumption in the manual or the game before relying on it.

## To learn next

1. Find the game window's class (`wmctrl -lx` with the game open) and map the main screens with
   game-ui (main menu, new game, map, recruit, army screen), following learn-to-play.
2. Pick one simple class to learn first (the manual's class pages: Baron or Barbarian look the most
   conventional) and play a small solo map with the user's go.
3. Record the screen map, hotkeys and the "what is final" rules here (End Turn `y`).
