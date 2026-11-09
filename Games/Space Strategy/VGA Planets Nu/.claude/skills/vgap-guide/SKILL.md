---
name: vgap-guide
description: "Starter guide to VGA Planets Nu, the browser remake of the classic play-by-email space 4X. Use when playing, learning or discussing VGA Planets or asking about its races, ships or rules."
keywords: "browser-based, tim, wisseman's, play-by-e-mail, known, far, documentation, lives, learn, first, local, sources, yet, game-sources, fetching, help, pages, game-ui, driving, window, learn-to-play, method, play, talk, works"
---

# VGA Planets Nu - starter guide

Status 2026-10-29: the folder has no manual yet. Nothing here is checked against the game; the
summary below is Claude's general knowledge, to be verified.

## What it is (to verify)

The 1990s DOS PBEM game VGA Planets (Tim Wisseman) remade as a web game at planets.nu: up to 11
players with very different races (Feds, Lizards, Bird Men, Fascists, Privateers, Cyborgs,
Crystals, Evil Empire, Robots, Rebels, Colonies), one turn per day or so, all orders given at once
and resolved together by the host. You build starbases and ships from hulls and components,
mine minerals (neutronium, duranium, tritanium, molybdenum), tax natives and colonists, and fight
with ship-to-ship combat that is simulated by the host. It plays in a browser, so the game window is
the browser (game-ui with UI_WMCLASS=firefox, or a browser automation skill if the user has one).
Real multiplayer games involve other people: never submit turns or post anything without the
user's go.

## Sources to get

- planets.nu help and documentation pages (fetch with game-sources; check what the site allows).
- The community wiki and forums; the classic VGA Planets 3 docs explain much of the shared rules.

## To learn next

1. Ask the user whether they have an account and a game, or want a practice game against the AI.
2. Fetch the official help pages into `sources/` and summarise them here.

## War skills (the user 2026-11-02: call the military skills when playing; build on them)
- Level of war: **strategic (4X)**; domain: **space**. Vocabulary: military-operations (strategic/operational levels, principles of war) + war-concepts' strategy section (total/limited war, escalation, war economy, war termination); soviet-doctrine for the
  opposing school; war-concepts (glossary, `warwiki.py look TERM`).
- Every turn / battle: **war-language** (UP: the situation in doctrine terms -> THINK: intent,
  form of manoeuvre, a task and purpose per unit -> DOWN: concrete orders -> CHECK) and **army-log**
  (read, log and evaluate both sides; `armylog.py`). Before the first real game write
  **`LEXICON.md`** in this skill folder (`warlang.py lexicon`): units -> roles, terrain -> OAKOC,
  rules -> effects, victory -> end state, task -> game actions.
- combat-models: the salvo model plus the user's space-warfare essay (military-theory shelf) - tracking, point defence, low staying power, who launches first; war-concepts: space weapon, kill chain, A2/AD.
