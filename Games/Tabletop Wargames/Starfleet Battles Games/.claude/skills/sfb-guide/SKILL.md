---
name: sfb-guide
description: "Starter guide to Star Fleet Battles (Captain's Edition): energy allocation, impulses, weapons, damage. Use when playing or learning SFB, planning energy or fire, or answering a rules question."
keywords: "amarillo, design, bureau, basic, set, rulebook, fifth, detailed, starship-combat, board, game, universe, player, commands, few, ships, through, proportional, impulse, movement, simultaneous, shields, ship, systems, display, ssd, seeking, drones, plasma, races, federation, klingon, romulan, kzinti, gorn, tholian, cadet, training, map, page, searchable, txt, game-sources, rule, lookups"
---

# Star Fleet Battles - starter guide

Status 2026-10-29: the Basic Set rulebook read in contents, course of play, scale and sequence
of play. Not played yet. The user's purchased copy (order watermark on every page): keep it local.

Files: `Star_Fleet_Battles_Basic_Set_Rulebook_2012.pdf` (250 pages, no bookmarks) and `.txt`.
Rules are numbered `(B2.2)`: `manual.py grep Star_Fleet_Battles_Basic_Set_Rulebook_2012.txt
"\(E3\.4\)" -C 3`. The contents is on PDF p4 (three columns).

## What it is (Claude's summary)

Tactical starship duels with very detailed ships: every ship is a **ship systems display (SSD)**,
boxes for warp and impulse engines, weapons, shields, labs, shuttles; damage checks boxes off.
A hex is 10 000 km; a turn is 1/30 s of real time (about a minute as the crew feels it). Each turn
starts with **energy allocation**: power from engines, reactors and batteries is split between
movement, weapons arming, shields and other systems, so every choice trades speed against
firepower. Movement is **proportional**: a turn has 32 impulses and faster ships move on more of
them. Fire is **secret and simultaneous**: players decide, then announce together. Play ends
when one side can no longer win and disengages.

## Sequence of play (B2.2)

1 energy allocation, 2 speed determination, 3 self-destruction, 4 sensor lock-on, 5 initial
activity, 6 impulse procedure (each impulse: movement, impulse activity, dogfight resolution,
direct-fire weapons, post-combat), 7 final activity, 8 record keeping.

## Rule map (sections)

A general (introduction, course of play, scale, **cadet's game A4**, sample game A5), B how to
play (sequence, energy allocation), C movement, D combat (fire, shields, damage allocation,
sensors), E direct-fire weapons, F seeking weapons (FD drones, FP plasma torpedoes), G-J
operations, systems, shuttles and fighters, P terrain (planets, asteroids, black holes, pulsars,
nebulae), R races and ship data (Federation, Klingon, Romulan, Kzinti, Gorn, Tholian), scenarios
and annexes (annex 2 is the detailed sequence).

## To learn next

1. Play the cadet's game (A4) with the user: two ships, the basic rules, Claude doing the
   energy allocation sheet and damage tracking.
2. Learn one race's main weapon each (phasers, photon torpedoes, disruptors, plasma, drones).

## War skills (the user 2026-11-02: call the military skills when playing; build on them)
- Level of war: **tactical (ship duels)**; domain: **space**. Vocabulary: military-doctrine (FM 3-90 tactics) first; soviet-doctrine for the
  opposing school; war-concepts (glossary, `warwiki.py look TERM`).
- Every turn / battle: **war-language** (UP: the situation in doctrine terms -> THINK: intent,
  form of manoeuvre, a task and purpose per unit -> DOWN: concrete orders -> CHECK) and **army-log**
  (read, log and evaluate both sides; `armylog.py`). Before the first real game write
  **`LEXICON.md`** in this skill folder (`warlang.py lexicon`): units -> roles, terrain -> OAKOC,
  rules -> effects, victory -> end state, task -> game actions.
- combat-models: the salvo model plus the user's space-warfare essay (military-theory shelf) - tracking, point defence, low staying power, who launches first; war-concepts: space weapon, kill chain, A2/AD.
