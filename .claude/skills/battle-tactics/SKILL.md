---
name: battle-tactics
description: "How Claude plans and fights tactical battles in any wargame: The user's turn method, the planning questions, general principles, per-game notes. Use before and during any battle, for battle plans, or after one for lessons."
keywords: "set, picture, battlefield, assign, unit, intentional, role, draw, movement, proposals, check, work, assess, make, plan, armies, differ, ground, good, whom, decisive, point, hold, across, games, break, cohesion, bodies, concentrate, fire, pin, flank, refuse, wing, keep, reserves, terrain, decides, matchups, first, field, glory, medieval, manual, hints"
---

# Battle tactics

Built with the user from 2026-11-02 after FoG II battle 1 went badly: I moved units without a plan,
ignored terrain (knights into marsh), never asked what the enemy could reach, ended turns on my own.
**Living file - add every lesson the user gives and every battle's result.**

## The turn method (the user) - every turn, no exceptions
0. **Look** - photo-map skill, then **army-log** (read and log both armies, evaluate) and **war-language** (UP: the picture in doctrine terms): identify the screen elements, photograph the whole field, build the map.
   No tooltips-for-everything, no Tab, no auto-scripts. Play with intention: being wrong is fine,
   phoning it in is not.
1. **Picture** of the battlefield: terrain, both armies, facings.
2. **Roles** - go through my troops one by one; every unit gets an intentional job (see Roles).
3. **Draw** movement proposals on the picture (arrows: unit -> square, charge targets).
4. **Check** each one can work: AP and terrain cost, turning limits, ZOC, reach, who can hit it back
   next turn (enemy reach = their move + charge distance), line of fire.
5. **Assess** - does the whole turn serve the plan? What is the worst enemy reply?
   **Before calling the turn done, go through EVERY unit's leftover AP against its role** (the user,
   FoG II battle 2: "Is that what you want them all to do? Some units do have more movement."). A
   block advance moves everyone the same distance, but fast units (light horse, light foot, mounted
   shooters) have AP left. Use it for their job: screens further out, flank guards in place. Leave it
   unused only on purpose (e.g. the reserve stays back).
6. Execute **in phases** (move-phases skill: main body, extension pass, final check; a problem check
   after each phase), one order at a time, photo after each. **Never press End Turn** - that is the user's.

## Say the plan in doctrine (military-doctrine skill - load it with this one; the user 2026-11-02)
Before drawing moves, write in the plan file: the **type of operation** (attack, defense, movement
to contact...), the **form of maneuver** (frontal attack, penetration, envelopment...) with its
**fixing force / main effort / supporting efforts / security / reserve**, one **tactical mission
task with a purpose** per unit (fix, support by fire, attack by fire, guard, block...), **phase lines**
in map terms ("col 17 by turn 6"), the **objective**, and the **reserve's commit trigger**. Check
offense against audacity, concentration, surprise, tempo; defense against disruption, flexibility,
maneuver, mass, depth, preparation, security; and plan the switch to defense before culmination.

## Making the plan (before contact; FoG II ch. 30, my words)
Any plan beats no plan; changing it later is hard. Answer:
- **How do the armies differ?** Who has the better close-combat foot, the better cavalry, the better
  troops for rough/difficult ground, more skirmishers and shooters?
  Your best arm sets where you fight; the enemy's best arm is to be avoided, delayed or disrupted.
- **Ground:** open flat ground favours cavalry and heavy foot; rough/woods/marsh favours medium and
  light foot and disorders horse and heavies. Higher ground wins close combat (much more if steep).
  Anchor flanks on terrain the enemy can't use.
- **Decisive point:** attack with one wing (heavy troops, the best units, reserves behind) while the
  other wing skirmishes or holds a strong position (the **refused wing**). Never strip the attacking
  wing to prop up the refused one - that just makes the attack fizzle.
- **Defending:** the enemy won't attack where you want him to; a pure defence gets its weakest point
  found. Defence followed by a planned counter-attack works better.
- **Simple:** most troops in lines under commanders, no gaps unless covered; depth (second line,
  reserves) beats an over-wide front; reserves near the centre and behind the wings.

## Roles (assign every unit, every turn)
Main line (holds/attacks frontally) - Strike (heavy cavalry/shock: hits flanks or disrupted units) -
Shooters (stand still, concentrate on one target) - Screen (lights in front: delay, harass, evade) -
Flank guard (stops outflanking; spears vs horse) - Reserve (behind the line: plug holes, exploit) -
Bait (draws the AI out where Strike can hit it) - Refused wing (delays, doesn't commit).
Doctrine names for the same jobs (military-doctrine): main line = fixing force (fix) or support
force; strike = enveloping force / main effort; shooters = attack by fire or support by fire;
screen = the user's screen, i.e. doctrine screen or guard; flank guard = flank guard (guard or block);
reserve = reserve; bait = feint / demonstration; refused wing = economy of force (delay).

## Field of Glory II specifics
Rules that shape tactics are in the fog2m-guide skill ("Movement and charge rules"). In short: foot
can't turn >45 deg and move; knights unmanoeuvrable; Whole Command moves stop within 5 squares of
the enemy; flank charge counts only if the charger STARTS behind the target's flank; light foot
can't charge unbroken non-lights in the open and evade non-light chargers; shooting is better
stationary, short range, full arc - 5 good shots of ammo, so hold fire at long range unless several
units can shoot the same target; troops behind obstacles lose cover if they move; charging enemy in
disordering terrain disorders the charger as if it were in it; foot shock troops follow up only if
they charged.

## Dominions 6 comparison
Dominions battles run from the setup (formations, positions, orders) - no live control - so the plan
is everything there; FoG lets me adjust every turn but the same principles hold: screen, concentrate,
protect the flanks and the commanders, break morale. Dominions tactics notes: dom6-tactics skill.
Lessons from the Dominions mechanics work (2026-11-03) that hold in any game:
- **Measure a buff or a matchup in rounds-to-kill** both ways before spending on it (unit-combat-math):
  Barkskin turned Sidhe vs White Centaurs from losing to even.
- **Every strong unit has a hard counter** (armour vs armour-piercing, dodge vs many attacks, HP vs burst,
  everything vs spells): send mixes that answer what's likely there, and carry a countermeasure against the
  enemy's likely trick (dom6-supercombatants).
- **Scripted casters**: an AI left to choose picks the nearest target and avoids some spells entirely -
  script what matters, within the fatigue budget (dom6-battle-ai).

## Matchups: area and trample attackers eat crowds (Dominions, Troban vs a Ghost Moose, 2026-11-03)
I called trample "minor"; it killed the user's army (the user: "trampled killed my army"). One trample hits every small
unit it rolls over, so cheap massed infantry feeds it. Against tramplers, area spells, breath, sweeps: fight
with FEW strong units (a tank, missiles from behind, elite single units) and keep the crowd away or spread;
against single big targets, concentrate missiles and armour-negating/magic damage. Read the enemy's special
abilities (manual/inspector/mod file) before choosing what to send - not after the battle.

## Don't commit (the user, 2026-11-03)
**Only commit when absolutely certain of the decision - "You're too hasty."** Slow down before every
irreversible order: plan agreed, numbers checked, failure case known, go given for this order.
Any order that can't be undone (charge, shot, End Turn, often moves) waits for an explicit go when the user is
planning the turn with me. Forecast, report, stop - commit as a separate step. A foot charge can't pin
mounted troops: unengaged horse charged by foot can break off after impact (FoG II 11.13.5 - "Enemy unit
Falls Back", turn 9). Plot where every evade and pursuit ends; ZOC doesn't stop them.

## Load the game's guide first (the user, 2026-11-02: "I kinda thought you read the manual")
- At the start of every session with a game and before every battle/turn sequence, load that game's
  guide skill and read its play reference (FoG II: fog2m-guide PLAY.md). Game guides live in the
  game's folder and do not surface on their own - invoke them.
- When learning a game, read the manual **to play it**: unit types and capabilities, combat tables,
  terrain, morale, victory conditions, hot keys - written into a play reference file. A design
  summary (Systems section) is a separate job and is not enough to play.

## Scouting costs turns (lesson, FoG II battle 2, 2026-11-02) - full method: scouting skill; screens: screening skill
Before spending turns to scout, check what can actually be hidden in this game (FoG II: only units in
forests). If the board shows the whole enemy, skip the look phase and use the time - on a turn limit,
waiting is a cost. Plans written before seeing the board should say "look IF something can be hidden".
Per game, write down what fog of war hides (in its guide) - it differs a lot:
- FoG II: almost nothing; units are generally only hidden in forests (the user).
- TOAW IV: fog of war is a real concern (the user, 2026-11-02) - expect unknown enemy positions and
  strengths; recon, probing and reading reports matter there. Check its manual's fog-of-war rules
  first (manual-first) before planning.

## Reference files (read the one the step needs)

| File | Holds |
|---|---|
| `reference/principles-that-cross-games.md` | **Principles that cross games** - Break cohesion/morale, not bodies |
| `reference/lessons-log.md` | **Lessons log** - 2026-11-02 FoG II battle 1 (Anglo-Irish vs Irish, attacking): no plan at contact; units pushed by   script;  |
| `reference/recipe-break-a-line-fog-ii-battle-2.md` | **Recipe: break a line (the user, FoG II battle 2 turn 8 - "you can break their entire line")** - Hammer and anvil, slightly modified: the line is the anvil and SUPPORTS the cavalry; knights are the hammer |

## Related skills
delegate (acting alone on the user's behalf: self-review checklist and certainty test), military-doctrine (FM 3-90 vocabulary and methods - the base this skill builds on), military-operations (FM 3-0: end state, defeat mechanisms, principles of war - check the whole plan), soviet-doctrine (echelons, wedge formations, encirclement), war-concepts (glossary and lookup of war terms: oblique order, enfilade, feigned retreat, ZOC...), combat-models (Lanchester: concentrate, make fights square when stronger and linear when weaker; combat.py), military-theory (strategy classics, in Military Theory/), move-phases (give movement in phases, check each, mandatory extension pass), scouting (what to know before committing), screening (forward units that force reactions), map-usage (read the board), photo-map + map-camera (see it), draw-moves (draw movement proposals: one picture or turn by turn), draw-map, planning (save the battle plan), learn-to-play (learn the game first), manual-first (rules before acting), generalize-learning (lessons log -> generic)
