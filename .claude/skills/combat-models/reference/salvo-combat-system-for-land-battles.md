# combat-models - the user's Salvo Combat System for Land Battles (his design - `Military Theory/Salvo Combat System for Land Battles`)

Part of the combat-models skill; SKILL.md links here.

## the user's Salvo Combat System for Land Battles (his design - `Military Theory/Salvo Combat System for Land Battles`)
An earlier version of his own system (the newer one is somewhere from before the move to this PC).
Hughes' salvo model taken down to company/platoon engagements, period = one hour:
- **Scale**: split the battle into many company/platoon (or battalion, 400-800 men) engagements that
  shoot, break, return; regiments were administrative, not tactical. Fast mode: armies vs armies.
- **Shot chain** (his steps 1-8): engaged strength = strength x frontage x frontage modifier (+ random
  variation) -> salvo = engaged x rate of fire (minus shots lost to movement: move scalar) -> accuracy
  (training, fatigue, equipment, range) -> hits -> **tactics saves** (nullifications, not intercepts:
  defensive tactics when holding, offensive tactics when advancing; terrain adds to one or the other -
  trenches help defense only) -> **armour** (penetration - armour) -> losses on the engaged part ->
  repeat for the period's salvos. Ammo: total and per-man local ammo; no ammo, no shooting.
- **Intercepts** are separate from saves: attacks against the salvo itself, needing accuracy and
  penetration and costing ammo (Hughes' y/z). Artillery and aircraft fire against their own
  anti-bombardment tactics values.
- **Fatigue** (turns of battle + movement + prior, minus rest) lowers frontage, accuracy and tactics:
  line troops wear the enemy down so shock troops finish them - the pre-1900 logic of fire then charge.
- **Close assault** = rounds at range 0 with assault accuracy, tactics and penetration (chinks in
  armour); decisive against fortified or fatigued, unready defenders (Verdun, Sevastopol, stormtroopers,
  Napoleonic cavalry); the formula says when a charge is the cheapest answer.
- **Clustering**: one shot can roll extra hits (trenches yes, a tank platoon in the open less).
- **To do in his notes**: initiative (who fires first on contact), spotting (spot, return-fire spot
  bonus, hide; firing only on what you see; ghost targets, friendly fire), and the morale step - after
  each round officers and troops "kick it or stick it": keep fighting, move, pinned, retreat, surrender,
  last stand, shellshock, firing at bushes, the officer who rallies - which is where the players play.
- Values: rifle ~600 m, 4 km/h but rarely; a Civil War rifleman fires ~6 times while a charge closes;
  50-100 shots per kill; tactics read off casualty ratios with similar equipment (Japan's WW2 offensives).

How it relates to the models above: **frontage is the Lanchester knob** (low frontage = linear-like,
full frontage = square-like); **initiative and spotting are Hughes' first strike and scouting**; tactics
saves are a per-hit version of staying power; intercepts are Hughes' defensive fire.

Prototype in `combat.py land RED.json BLUE.json` (expected values or `--dice`). First test
(2026-11-02): a 500-man battalion advancing (moving, offensive tactics 0.1) on 400 behind a wall
(defensive tactics 0.2, terrain 0.3), 6 salvos -> attacker loses ~165, defender ~41, about 4:1 - the
Fredericksburg pattern. Tuning note: that test kills 1 per ~28 shots; the user's 50-100:1 suggests base
accuracy ~0.01-0.02 for rifles.
