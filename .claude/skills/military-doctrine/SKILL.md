---
name: military-doctrine
description: Real military tactics for playing and designing games, distilled in Claude's words from US Army FM 3-90 Tactics (2023, Military Theory shelf, with page refs) - types of operations, forms of maneuver (frontal attack, penetration, envelopment, turning movement, infiltration), tactical mission tasks (fix, block, disrupt, support by fire, attack by fire, seize, retain...), security operations (screen, guard, cover - narrower than the user's broad screen), recon fundamentals, movement techniques (overwatch, bounds), control measures (phase lines, objective, limit of advance), reserve, key terrain, culmination, and how each maps onto game units and turns. The base that battle-tactics, screening, scouting and move-phases build on. Use when planning or reviewing any battle or turn in a wargame or strategy game, when naming a unit's job, when the user uses a military term, or when designing combat or AI for our games.
---

# Military doctrine (FM 3-90 Tactics) for games

Source: `Military Theory/ARN38160-FM_3-90-000-WEB-1.pdf` (+ `.txt`, page markers "=== page N" =
PDF page). Search it: `python3 -I .claude/skills/game-sources/scripts/manual.py` or grep the .txt.
Everything below is Claude's own summary; PDF page numbers in brackets.

**The user's rules (2026-11-02):** load this (and the military-theory shelf) whenever a game's
tactics or strategy is in play; build the game tactics skills on it. Doctrine is necessarily
narrower than our working terms because the US Army has more roles to hand out - so we keep
The user's broad terms (e.g. his *screen*) and use the doctrine names to say *which kind*.

## How to use it in a turn
1. Name the **type of operation** you are in (attack, defense, movement to contact...).
2. Pick the **form of maneuver** (who fixes, who decides, where).
3. Give **every unit one tactical mission task** with a purpose ("Spears 1-6: *fix* the French
   line so the knights can *envelop* the south flank").
4. Name the **security** (who screens/guards which flank) and the **reserve** (and when it commits).
5. Set **control measures** in map coordinates: phase lines (columns/rows to reach on which turn),
   objective, limit of advance.
6. Check against the **characteristics** (offense: audacity, concentration, surprise, tempo;
   defense: disruption, flexibility, maneuver, mass, depth, preparation, security) and against
   **culmination**.

## Types of operations [23-25, 89-91, 169-172]
- **Offense** - defeat/destroy enemy forces, take terrain. Types: *movement to contact* (find
  the enemy, develop the situation), *attack* (defeat a known enemy / seize terrain), *exploitation*
  (after success, disorganise them in depth), *pursuit* (catch a beaten force before it escapes).
  Attack variations: ambush, counterattack, raid (seize then withdraw on purpose), spoiling attack
  (hit an enemy getting ready to attack). Deception: *feint* (real contact, only to mislead) and
  *demonstration* (show of force, no contact sought).
- **Defense** - defeat an attack, gain time, economise. *Area defense* = deny terrain for a time;
  *mobile defense* = a small fixing force holds, a big striking force destroys; *retrograde* =
  organised movement away (delay, withdrawal, retirement).
- **Enabling operations** - not decisive alone: reconnaissance, security, troop movement, passage
  of lines, relief in place, mobility/countermobility, deception, linkup.

## Forms of maneuver [72-86]
- **Frontal attack** - broad front against a weaker enemy, or to *fix* a larger one. Costly; only
  with overwhelming power or when fixing is the job. Watch for gaps to exploit, and for bait.
- **Penetration** - narrow front: breach, widen the gap (shallow envelopments, attack by fire),
  then seize the objective and exploit. Best at the seam between two enemy units. Roles: support
  force fixes broadly, breach force opens, assault force goes through, reserve exploits.
- **Envelopment** - avoid the front, hit an **assailable flank** (if none, make one by penetration).
  Roles: **fixing force** (least power that keeps them in place - frontal pressure), **enveloping
  force** (most of the power), security force, reserve. Stay within *supporting distance*. Single
  (one flank, easier) or double. Depends on surprise or overwhelming power, and speed - before the
  enemy strengthens the flank or commits a reserve.
- **Turning movement** - go deep behind them to make them leave their position (vs envelopment,
  which hits them where they are). Big formations only.
- **Infiltration** - undetected movement through their area to a position of advantage.

## Tactical mission tasks [411-424] - one per unit, always with a purpose
- Effects on the enemy: **fix** (stop them moving from a place for a time), **block** (deny an
  area/approach), **canalize** (squeeze them into a narrow zone), **turn** (push them onto another
  approach), **contain** (stop/hold/surround), **disrupt** (upset formation or tempo, make them
  attack early or piecemeal), **interdict** (deny or delay use of an area or route), **isolate**
  (cut off from support), **suppress** (temporarily degrade), **neutralize** (make incapable of
  interfering), **defeat**, **destroy** (combat-ineffective), **reduce** (destroy an encircled or
  bypassed force).
- Actions by friendly forces: **attack by fire** (engage from a distance, no closing),
  **support by fire** (fire so another unit can move), **seize** (take ground by overwhelming
  force), **secure**, **retain** (keep them off ground), **occupy** (take unopposed ground),
  **clear**, **control**, **bypass** (deliberately avoid), **breach**, **disengage** (break
  contact to avoid decisive engagement), **follow and support** / **follow and assume** (second
  echelon behind the lead), **exfiltrate**.

## Security operations [269-298] - doctrine's narrow roles inside the user's broad *screen*
Security orients on **the friendly force** (recon orients on enemy and terrain). Fundamentals:
early and accurate warning; reaction time and maneuver space; orient on the protected force (stay
between it and the enemy, move when it moves); continuous reconnaissance; keep contact once made.
- **Screen** (doctrine) - mainly early warning by observation; fights only in self-defense and
  kills enemy scouts (counterreconnaissance); least protection, can't develop the situation.
  Displaces to the next screen line by set criteria. Can watch an approach two echelons bigger.
- **Guard** - enough power to defeat, fix or turn back the enemy's lead elements before they reach
  the main body with direct fire; fights to gain time; narrower front, inside the main body's
  support. Advance guard (develops the situation, clears the axis, avoids frontal assault on
  strength, never commits the main body piecemeal), flank guard (protects an exposed flank of a
  moving force; must not fall behind), rear guard.
- **Cover** - a self-contained force, independent of the main body, fighting far forward to gain
  time and make the enemy deploy.
- **Area security / local security** - every unit always guards itself.
- Every security job needs: a focus (what is protected), a duration, and **engagement and
  disengagement criteria** (when to fight, when to fall back) - write them in the plan.

## Reconnaissance [247-268]
Fundamentals: continuous; **never keep recon in reserve**; orient on the recon objective; report
fast and accurately; keep freedom of maneuver; gain and keep contact; develop the situation fast.
Forms: *route*, *zone* (everything inside boundaries), *area*, *reconnaissance in force* (attack to
test strength, dispositions and reactions), *special*; technique: *recon by fire* (shoot at a
suspected position to see what answers).

## Movement techniques [68-72]
- **Traveling** - contact unlikely, fast. **Traveling overwatch** - contact possible: a trailing
  element follows close enough to support the lead. **Bounding overwatch** - contact expected: one
  element always halts in an overwatch (support by fire) position while the other moves;
  alternating bounds (leapfrog, faster) or successive bounds (rear catches up, slower, safer).
  Bound length = terrain and the overwatching weapons' range.

## Control measures [375-410]
Line of departure (where the attack starts), **phase lines** (lines across the advance, used to
time and coordinate - in a grid game: "col 17 by turn 6"), objective, axis of advance / direction
of attack, limit of advance, boundaries, attack/support by fire positions, battle positions,
engagement area (where you mean to kill them), trigger lines.

## Ideas that decide battles
- **Reserve** [1-94]: withheld at the start for a decisive movement - to exploit success or stop
  failure. Committing it (time, place, circumstances) is the hardest decision; once committed,
  name a new one.
- **Key terrain** gives a marked advantage to whoever holds it; **decisive terrain** must be held
  to win. Seize it early [3-21].
- **Main effort / supporting effort**: one unit or group is the main effort, everything else
  shapes for it. **Economy of force**: the minimum where you are not deciding.
- **Tempo**: keep moving so the enemy cannot plan and react. **Culminating point**: the moment the
  attacker can no longer continue - plan the switch to defense before it, not after [3-64].
- The convergence of friendly forces at the decisive point is the riskiest moment [3-53].

## Mapping to games (examples)
- Field of Glory II: line infantry = fixing force; knights = enveloping force or reserve; light
  horse / light foot = the user's screen (doctrine: guard or screen by how much they fight);
  archers = attack by fire / support by fire; "turn N reaches col C" = phase lines; the AI's
  static line = area defense; the turn limit = their time-for-space trade.
- Dominions: thugs and SCs as raids; province scouts as screen; forts as area defense.
- Grand-strategy and operational games (TOAW, Gary Grigsby, AGEOD): the full vocabulary applies at
  the higher echelon - covering forces, turning movements, exploitation, pursuit.

## Related skills
war-concepts (themed glossary of ~220 war concepts from Wikipedia's war index, warwiki.py lookup),
combat-models (Lanchester square/linear laws, salvo model, combat.py - the math behind mass and
concentration), military-operations (FM 3-0: the operational level above this - principles of war, defeat
mechanisms, main effort, culmination), soviet-doctrine (the opposing school: echelons, 3:1, attack
from the march, encirclement), battle-tactics (the turn method - uses this vocabulary), screening (the user's broad screen, mapped to
screen/guard/cover), scouting (recon fundamentals and forms), move-phases (phases as bounds and
phase lines), draw-moves (draw phase lines and objectives), military-theory shelf skill in
Military Theory/ (Clausewitz, Jomini, Corbett, Mao - strategy level), borrow-from-games (design).
