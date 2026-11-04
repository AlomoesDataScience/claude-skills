---
name: dom6-sieges
description: Forts and sieges in Dominions 6, from the manual (pp. 26-28, 49-52, 71-73, turn steps 25-27, 35) - entering a fort (Defend = besieged, Patrol/Move and Patrol = fight outside), reducing walls (reduction = besiegers' strength squared, fliers x2; repair = defenders' strength squared / 2, mindless 1/8, animals and undisciplined half), Maintain Siege, Storm Castle (after walls hit 0, next turn, after other battles in the province), Break Siege, supply in a siege (fort supply / turns besieged, starvation, disease), fort defenders, retreats (smart 75% into fort or friendly land, troops follow on a morale check), weather (snow cold x15%, rain growth x10% + 10%). Use when attacking or holding a fort, planning a relief force, deciding Storm vs wait, or when the user asks about forts or sieges.
---

# Forts and sieges (Dominions 6, vanilla)

Plan item 20 (the user approved the extras 2026-11-03). Manual pp.26-28 (forts), 50-52 (orders), 71-73.

## Who fights where (pp.49-51)
- No battle with forces inside a fort until the walls fall or they sortie (Break Siege).
- Moving into your own fort province = enter the fort (Defend Castle). To fight outside, use Move and
  Patrol (or Patrol). Defenders in a fort province who are only on Defend get besieged.

## Breaking the walls (pp.71-72)
- Each turn: **reduction** = besiegers' siege strength squared (fliers x2) vs **repair** = defenders' strength
  squared / 2 (fliers x2; mindless 1/8; animals, undisciplined half). If reduction wins, the difference comes
  off the fort's defence; if repair wins, walls are mended up to full.
- Only commanders on **Maintain Siege** (default for besiegers) add siege strength. The attacker can't see
  the exact wall value; the defender can (fortification button).
- Damaged forts not under siege repair fully.

## Storming (pp.52, 72)
- Walls at 0: next turn, commanders may order **Storm Castle**; defenders start behind walls plus the fort's
  own extra defenders (p.26). Storming comes after other battles in the province (step 27): a relief army
  fights the besiegers first. A storming commander killed earlier = his units don't storm.

## Supply (p.72)
- Besieged defenders get fort supply / turns besieged (300, 150, 100, 75...). Starving two turns in a row ->
  disease (dom6-healing).

## Retreats (p.72-73)
- Each commander 75% smart (second 50% chance in native terrain): smart = into the fort here, else a random
  friendly neighbour; not smart = any random neighbour (enemy = destroyed). Troops follow on a morale check
  (squad morale bonus counts double, undisciplined -3).
- Defending your own castle: retreaters hide deeper inside; if the battle is lost, all of them die.

## Weather (p.72)
Snow: cold scale x 15% (cold 1+); rain: growth x 10% + 10% (heat 0+); none in wastes or caves.

## Related skills
dom6-stealth (patrol vs defend), dom6-morale (retreats), dom6-healing (disease), dom6-economy, dom6-mechanics.
