---
name: pog-guide
description: "Starter guide to Paths of Glory (GMT), the card-driven WWI board wargame. Use when playing, learning or setting up PoG, answering a rules question or planning a move."
keywords: "games, ted, raicer, classic, two-player, first, world, war, central, powers, allies, point-to-point, map, sequence, play, mandated, offensives, six, action, rounds, attrition, siege, status, replacements, card, draw, strategy, cards, operations, strategic, redeployment, events, commitment, levels, mobilization, limited, total, track, automatic, victory, scenarios, page, rules-2010, pdf, pages"
---

# Paths of Glory - starter guide

Status 2026-10-29: the 2010 rules booklet (32 pages) read in outline, plus victory and the
sequence of play. Not played yet. This is the parent design of Triumph of Chaos (see toc-guide):
learn it first and the other comes easily.

Files: `POG_Rules-2010.pdf` and `.txt` (PDF page = booklet page). The text lost some leading
digits in headings ("0.0 Stacking" is 10.0, ".0 Movement" 11.0): search the rule number with
`manual.py grep POG_Rules-2010.txt "^ *12\.[0-9]" -C 2` style patterns.

## What it is (Claude's summary)

The whole of WWI in Europe and the Middle East on a point-to-point map (spaces joined by
lines), corps and armies as counters, and each side's own deck of strategy cards that drives
everything. The Central Powers (CP) use interior lines and German quality against a larger
alliance; the Allies (AP) must hold on until their weight (and later the USA) tells. Turns are
seasons from August 1914 on, up to 20 turns.

## Turn (6.0, p6)

A. **Mandated offensive** roll for each side (a nation may be forced to attack this turn).
B. **Action phase**: six action rounds, CP first in each; a card is played one way - as
   operations (activate spaces to move or attack, costs depend on the nation and army/corps),
   strategic redeployment, replacement points, or its event; or a one-op action without a card.
C. Attrition (out-of-supply units die), D. siege rolls against besieged forts, E. **war status**
(VP changes, automatic victory check, armistice, war commitment level rises), F. replacements
(spend RP gathered from cards, Allies first), G. draw back to seven cards, H. next turn.

## Winning (5.0, p5)

One VP track: CP wins automatically at 20+, the Allies at 0 or less (checked in the war status
phase). Otherwise the level at the end decides; Peace Terms accepted = draw. Scenarios:
introductory (ends after turn 3), Limited War (ends at turn 10, Total War, or automatic win),
Campaign (to 1918; result depends on whether Brest-Litovsk was played). Tournament play bids VP
for sides (typically 1-2 VP to play the Allies).

## Rule map (booklet pages)

Components 2; symbols and terms 3; set-up 4; victory 5; sequence of play 6; mandated offensives
7; action phase and strategy cards 7-9; stacking 10; movement 10; combat 12 (examples 16);
strategic redeployment 17; supply 18; forts 19; war and peace 19; replacements 21; card notes 22;
design notes 24; extended example 25; exceptions and special rules 31; set-up lists 32.

## To learn next

1. Read 9.0 (strategy cards) and 12.0 (combat) in full and summarise them here; play the
   introductory scenario with the user, or on Vassal.
2. Keep a list of the key events (Guns of August, Entrench, Russian revolution chain, US entry).

## War skills (the user 2026-11-02: call the military skills when playing; build on them)
- Level of war: **strategic (card-driven)**; domain: **land**. Vocabulary: military-operations (strategic/operational levels, principles of war) + war-concepts' strategy section (total/limited war, escalation, war economy, war termination); soviet-doctrine for the
  opposing school; war-concepts (glossary, `warwiki.py look TERM`).
- Every turn / battle: **war-language** (UP: the situation in doctrine terms -> THINK: intent,
  form of manoeuvre, a task and purpose per unit -> DOWN: concrete orders -> CHECK) and **army-log**
  (read, log and evaluate both sides; `armylog.py`). Before the first real game write
  **`LEXICON.md`** in this skill folder (`warlang.py lexicon`): units -> roles, terrain -> OAKOC,
  rules -> effects, victory -> end state, task -> game actions.
- combat-models: The user's land salvo system and Lanchester (concentrate; make fights square when stronger, linear when weaker).
