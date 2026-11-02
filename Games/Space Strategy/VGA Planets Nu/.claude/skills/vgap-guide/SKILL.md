---
name: vgap-guide
description: Starter guide to VGA Planets Nu (planets.nu, the browser-based remake of Tim Wisseman's classic play-by-e-mail space 4X VGA Planets) - what it is, what is known so far, where its documentation lives, and what to learn first. No local sources yet. Uses game-sources (fetching its help pages), game-ui (driving the browser window), learn-a-game (method). Use when the user wants to play, learn or talk about VGA Planets / Planets Nu, or asks how one of its races, ships or rules works.
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
