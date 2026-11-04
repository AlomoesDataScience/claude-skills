---
name: dom6-battle-ai
description: How Dominions 6 battles run themselves and what the battle AI does, from the manual (pp. 44-46, 58-59, 71) and the casting-AI notes in dom6-tactics/ai-casting.md (Loggy's Dom5 reverse-engineering) - no live control, squad orders (None lets the commander decide, Attack, Fire, Hold and attack = 2 rounds then charge, Hold and fire, Fire and keep distance, Guard commander, Retreat = rout) and targets (random, archers, cavalry, fliers, large = size 7+, closest, rearmost), zone of control, commander orders (up to 5 scripted one-round steps, then a general order; no orders = the AI assigns them), mage scripting (a scripted spell is cast whenever it can be; else the AI picks), how the AI scores unscripted spells (nearest targets, resistances, rounds 1-2 buffs, enchantments it almost never casts, fatigue avoidance), and turn-limit routs. Use when writing battle scripts and army setups, predicting what an unscripted mage or squad will do, or when the user asks why the AI did something in a battle.
---

# The battle AI (Dominions 6)

Plan item 25 (the user approved the extras 2026-11-03). Manual pp.44-46 (orders), 58-59 (setup), 71 (turn
limits). Spell choice in depth: `../dom6-tactics/ai-casting.md` (measured on Dom5 - broad rules match Dom6
replays). Clicking the orders: dom6-game.

## Battles run on their own (p.58)
Attacker on the left, defender on the right; every unit follows its setup orders until it routs or the battle
ends. The plan is everything: formation, position, orders, scripts.

## Squad orders (pp.44-45)
| Order | What it does |
|---|---|
| None | the commander's AI decides |
| Attack | melee the target |
| Fire | shoot until out of ammunition (then advances if close) |
| Hold and attack | hold 2 rounds (firing if ranged), then melee - no "hold forever" |
| Hold and fire | hold 2 rounds, then fire or advance into range |
| Fire and keep distance | shoot, back off when the target comes close |
| Guard commander | stays on him (and may join assassination fights); ranged only fire at close enemies |
| Retreat | leaves the field = treated as a rout (may scatter to neighbours) |
- Targets: random, archers, cavalry (or fast), fliers, large (size 7+, else 6), closest, rearmost.
- Enemy **zone of control** can stop a squad short of its target.

## Commanders and mages (pp.45-46)
- Up to **5 specific one-round orders** (hold, hold or fire, hold or cast, cast a specific spell, attack,
  fly attack), then a **general order** (stay behind troops, attack, cast spells, advance and cast, retreat).
- **No orders = the AI assigns them.** Copy scripts: hover, ctrl+digit; paste with the digit (0-9).
- Cast a specific spell falls back to an AI pick if gems are missing or no target is in range.
- Conservative gem use: gems only for scripted spells.

## The casting AI in short (ai-casting.md)
- Scripted spells win whenever castable; with 50+ spells known, unscripted ones may not even be considered.
- Unscripted damage goes at the **nearest** good square; never into enemies that resist the element.
- Buffs rated high in rounds 1-2; Air Shield ~0 without enemy archers; resistance buffs ~0 without matching
  enemy mages.
- Some battlefield enchantments (Rain of Stones, Astral Tempest, Quagmire, Solar Brilliance, Acid Storm) are
  almost never cast unless scripted.
- Unscripted mages avoid going past 100 fatigue; **scripted mages cast themselves unconscious**.
- Mods change AI weights (`#aispellmod`, `#ainocast`): dom6-mod-magic "AI only" list = what to script.

## Turn limits (p.71)
Round 100 twilight, 150 attackers rout, 170 defenders rout, 200 the rest die (dom6-battlefield).

## Related skills
dom6-tactics (ai-casting.md, layouts), dom6-game (clicking orders), dom6-evocations, dom6-buffs,
dom6-fatigue, dom6-morale, dom6-battle-view (check what happened), dom6-mechanics.
