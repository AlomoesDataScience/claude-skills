---
name: uscw-guide
description: Guide to GMT's The U.S. Civil War (Mark Simonitch, 3rd edition rules August 2021), a two-player strategic board wargame of the whole war that the user owns boxed - where the rules, naval rules, errata, Q&A, player aid cards, setup cards and the ZunTzu module live in the workspace (all pulled from GMT's product page as PDF + page-numbered text), the rulebook's section map, and the core loop (dice-differential action points shared by both players, SPs of 5,000 men, generals, reaction movement, supply, Special Action Cards, automatic victory). Use when the user wants to play, learn or talk about The U.S. Civil War, look up a rule, set up a scenario (1861, 1862, 1863, campaign), or compare its systems with other wargames or the 4X engine.
---

# The U.S. Civil War (GMT Games)

The user owns the boxed game (2026-11-01) and is installing Vassal. Everything below came from GMT's
product page with `docpull.py` (wiki-scout skill); `gmt/SOURCE.md` lists each file and its link.

## Files (`gmt/`, each PDF has a `.txt` beside it with `=== page N` markers)

| What | File |
|---|---|
| Rules, 3rd ed. 2021 (40 pp) | `TUSCW_RULES_2021-Final.txt` |
| Naval rules 2021 (Advanced Game) | `TUSCW_NAVAL_RULES-2021-Final.txt` |
| Player aid cards 2021 / 2017 | `TUSCW-2021-UpdateKit-Final/TUSCW-PAC-2021-Final.txt`, `TUSCW-PAC-May2017-FINAL.txt` |
| Setup cards | `TUSCW-2021-UpdateKit-Final/TUSCW_SetupCards-Final.txt` |
| Errata (Dec 2015), Q&A (Mar 2016) | older printings; the 2021 rules fold most of it in |
| Translations | French `_Regles_`, Korean `_Ko_`, Italian `ITA`, Spanish, Japanese `USCivilWar_JP/` |
| A Dutch review and its English translation | `spel_tuscw.pdf` (odd font, text garbled), `TUSCWtranslation.txt` |
| ZunTzu module (map JPG, counter sheets, decks, 1861/62/63 setups as XML) | `US Civil War.ztb/` |

Vassal module: https://vassalengine.org/wiki/Module:The_U.S._Civil_War (download it through Vassal's
own library once it is installed; the web page is a script app, so docpull can't read it).
Use `manual.py grep gmt/TUSCW_RULES_2021-Final.txt "REGEX"` and `manual.py page ... N`.

## Rulebook map (section: page)

1 Introduction 2 · 2 Components 2 · 3 Sequence of play 3 · 4 Action phases 3 · 5 Movement 4 ·
6 Control 6 · 7 Generals 8 · 8 Cavalry 9 · 9 Reaction movement 10 · 10 Fortifications 12 ·
11 Battle 14 · 12 Demoralisation and rally 16 · 13 Supply 16 · 14 Reinforcements 20 ·
15 Strategic movement 22 · 16 Leader management 23 · 17 Special rules 24 · 18 Special Action
Cards 25 · 19 Naval rules 26 · 20 End phase and automatic victory 30 · Optional rules 31 ·
Scenarios S1 1861 32, S2 1862 33, S3 1863 33, S4 Campaign 33 · Special hexes 35 · Map notes 36 ·
Hints on play 39 · Index 40.

## How it plays (in my words)

- Map in three theatres (East, West, Trans-Mississippi); Northern, Border (MO, KY, WV) and
  Southern states. Objective hexes in the North and Border give the South VPs and BPs; resource
  hexes in the South feed Confederate build points.
- Strength points (5,000 men each) are interchangeable like money; generals lead stacks.
- Turn: reinforcements (Union fixed, Confederate from resources) and Special Action Cards ->
  strategic movement (Union has far more rail, river and ocean capacity) -> leader management ->
  3 action phases in 1861, 4 later -> end phase (control, rally, automatic-victory check).
- **Action phases:** both roll a d6; the high roller goes first, and **both** players get the
  difference as action points. Doubles hand out cards and reroll. A difference of 1 gives 1 point
  in *each* theatre. So tempo is shared and swingy: a design idea worth noting for the 4X engine.
- Reaction movement lets the defender answer moves; supply and lines of communication matter;
  forts and coastal forts; naval units only in the Advanced Game.

## Systems
- **Time**: each action phase both players roll a d6; high roller moves first and both get the difference as
  action points; doubles hand out Special Action Cards and reroll; a difference of 1 gives a point in every
  theatre (4.1, p3). Shared, swingy tempo.
- **Logistics**: strategic movement by rail, river, ocean and road with fixed per-side capacities; the Union
  has far more (3.2, 15.0).
- **Economy**: Confederate reinforcements come from resource hexes (build points), the Union's are fixed
  per theatre; capturing Northern objective hexes gives the South VPs and BPs (2.1.4, 14.3).
- **Operational war**: reaction movement lets the defender answer moves (9.0); generals lead stacks (7.0).
- **Victory**: automatic victory checked each end phase (20.3).

## Needs from the user
- Which scenario to start with, and table or Vassal (General.md asks the Vassal question too).

## War skills (the user 2026-11-02: call the military skills when playing; build on them)
- Level of war: **strategic + operational**; domain: **land**. Vocabulary: military-operations (FM 3-0) + military-doctrine; military-operations (strategic/operational levels, principles of war) + war-concepts' strategy section (total/limited war, escalation, war economy, war termination); soviet-doctrine for the
  opposing school; war-concepts (glossary, `warwiki.py look TERM`).
- Every turn / battle: **war-language** (UP: the situation in doctrine terms -> THINK: intent,
  form of manoeuvre, a task and purpose per unit -> DOWN: concrete orders -> CHECK) and **army-log**
  (read, log and evaluate both sides; `armylog.py`). Before the first real game write
  **`LEXICON.md`** in this skill folder (`warlang.py lexicon`): units -> roles, terrain -> OAKOC,
  rules -> effects, victory -> end state, task -> game actions.
- combat-models: The user's land salvo system and Lanchester (concentrate; make fights square when stronger, linear when weaker).
