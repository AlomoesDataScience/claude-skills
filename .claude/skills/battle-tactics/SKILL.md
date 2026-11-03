---
name: battle-tactics
description: How Claude plans and fights tactical battles in any wargame - the turn method the user set (picture of the battlefield, assign every unit an intentional role, draw movement proposals, check they can work, assess), the questions that make a plan (how do the armies differ, where is the ground good for whom, where is the decisive point), principles that hold across games (break cohesion not bodies, concentrate fire, pin then flank, refuse one wing, keep reserves, terrain decides matchups) and per-game notes - first Field of Glory II Medieval (manual ch. 23 Hints and ch. 30 Tactics, in Claude's words), with Dominions 6 as the comparison. Use when fighting any battle (before and during it), when making or reviewing a battle plan, when the user teaches tactics, or after a battle to record what worked.
---

# Battle tactics

Built with the user from 2026-11-02 after FoG II battle 1 went badly: I moved units without a plan,
ignored terrain (knights into marsh), never asked what the enemy could reach, ended turns on my own.
**Living file - add every lesson the user gives and every battle's result.**

## The turn method (the user) - every turn, no exceptions
0. **Look** - photo-map skill: identify the screen elements, photograph the whole field, build the map.
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

## Principles that cross games
- **Break cohesion/morale, not bodies.** Units run long before they die, and a rout shakes neighbours.
  (FoG: cohesion levels; Dominions: morale checks and army-wide rout.)
- **Concentrate.** Shoot one target with several units the same turn; gang up in melee (a unit fighting
  two enemies fights each worse). Spread damage wins nothing.
- **Pin, then flank.** Flank/rear attacks are devastating only when the target is already engaged to
  its front. Set up the frontal fight first, flank second. Don't offer your own flanks.
- **Matchups.** Charge only where you have the advantage (FoG: check the Win:Draw:Lose tooltip; Ctrl
  for detail). A strong unit loses in the wrong spot (knights in marsh).
- **Skirmishers first.** Use lights to drive off enemy lights, then shoot at the heavy wings; they
  fall back and evade. Lights die to horse in the open - keep them near cover.
- **Generals** in a fight boost it a lot but stop commanding while fighting and can be lost; commit
  them when the fight is critical or even. A general helps a wavering unit rally.
- **Pursuit:** chasing a beaten enemy with disordered troops throws away the win.
- **Use the AI's habits** (FoG ch. 31): an infantry AI that is outmatched won't advance; its cavalry
  hangs back too; lights stay near; units avoid flank exposure, seek flanks, avoid bad matchups,
  shooters stop outside enemy range, near-broken lights retreat. Bait accordingly.

## Roles (assign every unit, every turn)
Main line (holds/attacks frontally) - Strike (heavy cavalry/shock: hits flanks or disrupted units) -
Shooters (stand still, concentrate on one target) - Screen (lights in front: delay, harass, evade) -
Flank guard (stops outflanking; spears vs horse) - Reserve (behind the line: plug holes, exploit) -
Bait (draws the AI out where Strike can hit it) - Refused wing (delays, doesn't commit).

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

## Lessons log
- 2026-11-02 FoG II battle 1 (Anglo-Irish vs Irish, attacking): no plan at contact; units pushed by
  script; knights walked into marsh and were charged by skirmishers there; turns ended without the user.
  Lessons: the turn method above; terrain before movement; enemy reach before every move; roles.

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

## Related skills
move-phases (give movement in phases, check each, mandatory extension pass), scouting (what to know before committing), screening (forward units that force reactions), map-usage (read the board), photo-map + map-camera (see it), draw-moves (draw movement proposals: one picture or turn by turn), draw-map, planning (save the battle plan), learn-to-play (learn the game first), manual-first (rules before acting), generalize-learning (lessons log -> generic)
