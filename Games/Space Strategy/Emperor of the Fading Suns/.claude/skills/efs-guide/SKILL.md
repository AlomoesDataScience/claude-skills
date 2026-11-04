---
name: efs-guide
description: Starter guide to Emperor of the Fading Suns (Holistic Design / SegaSoft, 1996), a hex-based space and planetary strategy game of feudal noble Houses - what it is, the turn sequence, the Regency/Emperor election (Sceptor votes, Byzantium Secundus), Church, Merchant League, labs and outlawed tech, cities, cargo pods and loyalty, scoring, with a map of the scanned manual (emperor_of_the_fading_suns_manual.pdf, OCR text in emperor_of_the_fading_suns_manual.txt). Uses game-sources (manual lookups), game-ui (window driving, OCR), learn-to-play (method). Use when the user wants to play, learn or talk about Emperor of the Fading Suns / EFS, or asks how one of its rules or screens works.
---

# Emperor of the Fading Suns - starter guide

Status 2026-10-29: manual OCR'd (the PDF is a scan; game-ui `ocr.py pdf`, 300 dpi, good quality,
a few garbled contents lines) and read for the setting, turn sequence, tech, cities, election and
victory. Not played yet. A Windows 95 game (DOSBox/Wine here; find the window class when open).

Files: the scanned PDF (52 pages) and its OCR text `emperor_of_the_fading_suns_manual.txt`
(16 700 words, "=== page N"). Search: `manual.py grep emperor_of_the_fading_suns_manual.txt
"loyalty|tithe" -C 2`. OCR errors happen in numbers: check a number that matters on the page image
(`pdftoppm -f N -l N -r 150 -png`).

## What it is (Claude's summary)

Far-future feudal space strategy (the Fading Suns tabletop RPG setting): year 4956, the suns are
dimming, the throne has been empty since the first emperor was murdered at his coronation, and
five noble Houses (default house in the tutorial: Li Halan) compete to be elected **Regent** and
then declare themselves **Emperor**. Planets are hex maps with cities and units; a starmap joins the
planets by jump routes. Other powers take turns too: the **Merchant League** (trade, Agoras,
loans, can declare a "Third Republic"), the **Church** (votes, outlaws research, the tithe),
the Imperial Ministries, rebels, and two alien threats (Symbiots and the Vau). One to five players,
hot-seat or e-mail.

## Turn and rules (manual)

- **Turn sequence:** research results → event messages (movement, combat, diplomacy, votes; must
  be read before ending the turn) → production prompts → move units (units without sentry orders
  are offered in turn) → politics (answer proposals; as Regent, make appointments) → unit upkeep
  (short of money: disband, raise taxes, cut pay or skim the tithe) → loan payments (refuse and the
  League will likely declare war) → automatic repair/healing (faster in cities).
- **Tech:** labs research technologies, but a House needs enough labs to keep its tech or loses
  it; the Church outlaws some research, and building proscribed units angers some sects.
  Monasteries and ruins (human, alien) give free tech, resources, units or holy relics (relics need
  Theurgy tech to use). Shield generators: one per planet, protect a one-hex radius from space
  attack, not from ground attack.
- **Cities and resources:** resource cities fill cargo pods each turn; pods can be captured, so
  guard them. Productivity depends on supplies in the warehouse, loyalty and health; unrest
  lowers output. Some cities can't be built by players (Agora, monasteries, ruins, alien cities).
- **Election:** 35 Sceptors (votes): each House holds five, and the League and Church hold five
  each; Sceptors can be traded or seized (and are lost with a destroyed ship carrying them). A vote
  is held every ten years or when the Regent dies. A House needs a Noble at its fort on Byzantium
  Secundus to vote, be elected or hold a ministry. The Regent appoints ministers (Imperial Eye,
  Imperial Fleet, Stigmata garrison, others); one ministry per House.
- **Winning:** become Regent, declare Emperor, then win two more votes in the next ten turns with
  a Noble alive - or eliminate every other House's Nobles. A House is out when all five of its
  Nobles are dead. Score: resources and credits, techs (10 each), each Regency (100), unit and city
  value x loyalty, penalties for Vau/Symbiot planets, for signing the hold writ and for a Third
  Republic, bonus for Emperor.

## Manual map (printed page numbers, from the contents)

Tutorial / quick start 4, house traits (positive, negative), game turn overview 14, researching
technology 14, planetary buildings 19, order buttons 20, moving units 21, loading space and naval
transports 22-23, unit information and statistics, cities players cannot build 28, managing
cities 28, resource production 29, unrest and productivity 30, the starmap 31, diplomacy and
politics 32-38, election of Regent/Emperor 39, ending and winning 40.

## To learn next

1. Play the manual's tutorial (Start New > Historical > Play; House Li Halan, Beginner) with the
   user's go, mapping each screen with game-ui.
2. Write down the hotkeys (the Orders pulldown lists them) and the unit types.
3. Diplomacy chapter in detail: how votes and proposals work is the core of winning.

## War skills (the user 2026-11-02: call the military skills when playing; build on them)
- Level of war: **strategic (4X)**; domain: **space+land**. Vocabulary: military-operations (strategic/operational levels, principles of war) + war-concepts' strategy section (total/limited war, escalation, war economy, war termination); soviet-doctrine for the
  opposing school; war-concepts (glossary, `warwiki.py look TERM`).
- Every turn / battle: **war-language** (UP: the situation in doctrine terms -> THINK: intent,
  form of manoeuvre, a task and purpose per unit -> DOWN: concrete orders -> CHECK) and **army-log**
  (read, log and evaluate both sides; `armylog.py`). Before the first real game write
  **`LEXICON.md`** in this skill folder (`warlang.py lexicon`): units -> roles, terrain -> OAKOC,
  rules -> effects, victory -> end state, task -> game actions.
- combat-models: The user's land salvo system and Lanchester (concentrate; make fights square when stronger, linear when weaker). combat-models: the salvo model plus the user's space-warfare essay (military-theory shelf) - tracking, point defence, low staying power, who launches first; war-concepts: space weapon, kill chain, A2/AD.
