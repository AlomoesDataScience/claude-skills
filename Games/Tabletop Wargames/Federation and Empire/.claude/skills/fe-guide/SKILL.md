---
name: fe-guide
description: Starter stub for Federation & Empire (Amarillo Design Bureau), the strategic board wargame of the Star Fleet Universe's General War - empires, fleets as counters, a hex map of the galaxy's border regions, economy and production. The user owns the physical game; no rulebook file here yet. Links to sfgc-guide (Galactic Conquest campaign, which borrows F&E's statistical combat) and sfb-guide (fighting battles out in Star Fleet Battles). Use when the user wants to play, set up or talk about Federation & Empire / F&E.
---

# Federation & Empire - starter stub

Status 2026-10-29: the user owns the boxed game ("I have federation and empire ... in person")
and has no copy of the rulebook online ("I don't have F&E manual online"). Everything below is Claude's general knowledge, to check
against the rulebook.

## What it is (to verify)

The strategic level of the Star Fleet Universe: the General War between the Federation, Klingons,
Romulans, Kzinti, Gorn, Tholians, Lyrans, Hydrans and others, with ships as counters (each with
attack and defence factors) on a hex map, turns of half a year, an economy of economic points
that pays for production and repairs, and battles resolved statistically over combat rounds.
Galactic Conquest (sfgc-guide) says its combat is modelled on F&E's; Star Fleet Battles
(sfb-guide) covers the same ships at tactical scale.

## To learn next

1. The rulebook exists only on paper: if the user photographs or scans pages, game-ui's
   `ocr.py image` / `ocr.py pdf` turns them into searchable text here. Otherwise ask rules questions
   about the physical book.
2. Then: sequence of play, combat, economics, in that order.

## War skills (the user 2026-11-02: call the military skills when playing; build on them)
- Level of war: **strategic**; domain: **space**. Vocabulary: military-operations (strategic/operational levels, principles of war) + war-concepts' strategy section (total/limited war, escalation, war economy, war termination); soviet-doctrine for the
  opposing school; war-concepts (glossary, `warwiki.py look TERM`).
- Every turn / battle: **war-language** (UP: the situation in doctrine terms -> THINK: intent,
  form of manoeuvre, a task and purpose per unit -> DOWN: concrete orders -> CHECK) and **army-log**
  (read, log and evaluate both sides; `armylog.py`). Before the first real game write
  **`LEXICON.md`** in this skill folder (`warlang.py lexicon`): units -> roles, terrain -> OAKOC,
  rules -> effects, victory -> end state, task -> game actions.
- combat-models: the salvo model plus the user's space-warfare essay (military-theory shelf) - tracking, point defence, low staying power, who launches first; war-concepts: space weapon, kill chain, A2/AD.
