---
name: ocs-guide
description: Starter guide to the Operational Combat Series (OCS) rules v4.3 (The Gamers / Multi-Man Publishing, Dean Essig) - operational WWII-era hex wargames at ~5 miles per hex and half-week turns - sequence of play (weather, reinforcements, movement, supply, reaction, combat, exploitation), units and modes (combat, move, strategic, reserve), zones of control, overruns, ground combat with action ratings and surprise, barrages, supply points as physical counters (combat supply, fuel, trace supply, extenders, internal stocks, attrition), specialised units, air power and air bases, hedgehogs, naval power, ports and shipping, breakdowns, optional rules - with a local copy of the online rules site (rules-site/, OCS-4.3-rules.txt) and the series errata. Uses game-sources (lookups), learn-to-play (method). Use when the user wants to play, learn or talk about OCS or any OCS game (DAK, Case Blue, Tunisia, Burma...), answer a rules question, plan a turn, or study its supply model for our own 4X engine.
---

# Operational Combat Series v4.3 - starter guide

Status 2026-11-01: the rules site (https://dornshuld.chemistry.msstate.edu/rules/ocs43/, the user's
link) mirrored to `rules-site/` (26 pages) and joined into `OCS-4.3-rules.txt` (pages start with
`=== <page>.html`). The server leaves out its intermediate certificate: fetch with the chain
completed from the CA's own AIA URL, never with verification off. `pdf/OCSSeriesRulesErrata.pdf`
from MMP. OCS Depot refused direct PDF downloads (rules, charts, turn checklist): get them from
The user if needed. Which OCS game the user plays is not known yet.

## What it is (Claude's summary)

A rules series shared by many operational games: units from company to division, 5 miles per
hex (2.5 in some), half-week turns. The heart is **supply**: supply points (SP) are counters
that you move by truck, rail, sea or air, and spend for combat (attack and defence), fuel and
barrages. Units in **modes** (combat, move, strategic for double movement, reserve to react)
trade combat power for mobility. The non-phasing player gets a **reaction phase** in the middle
of your turn, and you get an **exploitation phase** after combat for reserves. Combat uses odds,
terrain columns, **action ratings** (quality) and a **surprise** roll that shifts columns.

## Rule map (sections; search `OCS-4.3-rules.txt`)

1 scale, **2 sequence of play** (2.2b extended sequence with rule references), 3 units and
markers, 4 general concepts (ZOC 4.5), 5 modes, 6 ground movement, 7 reaction phase, 8 overrun,
**9 ground combat** (9.6 action rating, 9.7 odds, 9.8 surprise: 2D6 + attacker AR − defender AR,
9.10 results), 10 barrage, 11 exploitation, **12 supply** (12.1 SP, 12.4 combat supply, 12.5 fuel,
12.6 trace, 12.7 extenders, 12.8 attrition, 12.10 internal stocks), 13 specialised units
(replacements 13.5, reinforcements 13.6, engineers 13.8), 14 air power, 15 air bases, 16
hedgehogs, 17 weather, 18 naval, 19 ports and shipping, 20 breakdowns, 21 optional; house rules,
terms, notes, summaries.

## For our 4X engine

OCS is the model for semi-abstract logistics that still matter (the user: "you do have to manage
supply chains somewhat"): physical supply that must be moved and spent, reach limited by HQs and
extenders, attrition when cut off, and quality (action rating) mattering as much as strength.
