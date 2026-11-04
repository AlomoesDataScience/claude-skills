---
name: war-concepts
description: Glossary of war concepts for playing and designing games, from Wikipedia's Index of war-related articles (local copy, Military Theory/wiki/) triaged by Claude into A (221 concepts that matter for games, full text local), B (681 specific weapons, platforms, troop types and wars, fetched on demand) and C (244 not useful - ranks, law cases, atrocities, culture, wrong links). Concepts grouped by theme in Claude's words with what each means at the table - forms of war and strategy, fronts, offence and defence moves, fire and manoeuvre, combined arms, terrain and fortification, deception and intelligence, command, logistics, morale, air, naval, space, irregular and information war, escalation and war termination, and the wargame mechanics (zone of control, order of battle, fog of war). warwiki.py looks up any term, searches the full texts and fetches more. Use when the user uses a military term, when naming what a unit or plan is doing, when a game introduces a concept, or when designing systems for our games.
---

# War concepts (Wikipedia's Index of war-related articles, triaged)

The user, 2026-11-02: "Lot of stuff to pull from that ... some of it is less useful than others."
Source: `Military Theory/wiki/Index_of_war-related_articles.wiki` (wikitext) -> `war-index.json`
(every article: title, short description, opening two sentences, tier) and `war/<title>.txt`
(full text of tier A). Wikipedia text is CC BY-SA; the files are a local reading copy; everything
below is Claude's own summary.

```
python3 -I .claude/skills/war-concepts/scripts/warwiki.py look TERM     # what it is, tier, local file
python3 -I .claude/skills/war-concepts/scripts/warwiki.py grep WORD     # search the full texts
python3 -I .claude/skills/war-concepts/scripts/warwiki.py tier B        # the reference list
python3 -I .claude/skills/war-concepts/scripts/warwiki.py fetch 'Title' # pull one more article
```
Fetching rules: the Wikipedia API rate-limits bursts - batches of 20 with 1 s gaps hit "too many
requests" a few times; one full article per 2.5 s worked. Back off and retry, never hammer.
`List of military tactics` (tier A) is the next hub worth mining. Checked against the full texts
(2026-11-02): zone of control (corrected to rigid/semi-rigid), oblique order, fleet in being.
"Dynamic defence" turned out to be a niche theory article - dropped from the list.

## The tiers
- **A** - concepts: how wars, campaigns and battles are fought, and wargame mechanics.
- **B** - specific things: weapons (Claymore, HIMARS, Spike), platforms (Centurion, Yamato), troop
  types and historic units (hussars, Janissaries, Roman legion), branches and organisations, named
  wars and operations. Look them up when a game has them (unit stats, era flavour, design).
- **C** - left out: ranks and titles, legal tribunals, atrocities, memorials and the arts, and links
  that point at the wrong thing (Firebase = Google's product, Overwatch = the video game, Scouting =
  the youth movement, Cannonade = a racehorse, Proxy fight = shareholders, Reinforcement = psychology).

## Forms of war and strategy
- **Absolute / total war** (everything mobilised, no limits) vs **limited war** (limited aims and
  means) - sets how far an AI or player escalates. **Grand strategy** - all a state's means toward
  its long-term ends; **military strategy** - force toward political aims; **operational level**
  between strategy and tactics (military-operations).
- **Attrition** (wear them down; Lanchester's square-law world) vs **manoeuvre warfare** (make
  their position useless, break cohesion; Blitzkrieg, AirLand Battle, deep operation, Soviet OMG).
- **Fabian strategy** - avoid the decisive battle, harass, let time and supply beat the stronger
  side (the French AI's time-out win in our FoG II battle is Fabian by default).
- **Conventional / irregular / asymmetric / hybrid / fourth-generation / grey-zone** - from army
  vs army to mixes of regulars, guerrillas, information and economic pressure below open war.
- **Generations of warfare** - massed line -> massed firepower -> manoeuvre -> blurred war and
  politics; a frame for era design in our games.
- **Pre-emptive war** (strike first at an imminent attack) vs **preventive war** (strike before
  they become able) - AI war-declaration logic. **Security dilemma** - my defence looks like your
  threat; arms races follow. **Deterrence**, **counterforce** (hit their weapons) vs **countervalue**
  (hit their cities), **first/second strike**, **brinkmanship**, **horizontal escalation** (widen the
  war to new places), **conflict escalation** ladders - diplomacy and AI in 4X design.
- **Pyrrhic victory** - a win that costs as much as a loss; check the exchange ratio, not the result.
- **War economy, economic warfare, blockade, mobilisation, war-weariness, war termination** - the
  economy and politics layer: wars are won by producing and sustaining more, lost when the home
  front quits; plan how a war ends before starting it.

## Fronts and space
**Theatre** (region of operations) > **front** (a sector, or the line of contact) > **front line**;
**no man's land** between lines. **Strategic depth** - distance between the front and what you
must keep; trade it for time. **Buffer zone**, **choke point** (narrow passage - where a small force
holds a big one: make it a linear-law fight), **high ground** (sight, range, downhill fighting),
**line of sight**, **enfilade** (fire along the length of an enemy line - devastating) and
**defilade** (protected from fire by terrain). **Bridgehead / beachhead** - the first foothold
across a river or shore; expand it before they seal it.

## Moving on the enemy (offence)
- **Offensive**, **pitched battle** (both choose to fight here), **invasion**, **raid** (strike and
  leave), **nuisance raid**, **coup de main** (one swift surprise blow), **sortie** (break out from a
  strongpoint), **search and destroy**, **cordon and search**.
- **Flanking manoeuvre**, **envelopment**, **pincer movement** (both flanks), **encirclement** (they
  are surrounded - supply and retreat cut), **oblique order** ("declined flank"; Frederick: mass on one wing, fix the rest of their line
  with the remainder, refuse your weak wing - local superiority with equal or weaker forces; our
  FoG II plan in shape),
  **echelon formation** (units stepped back diagonally - the refused wing), **infiltration tactics**
  (small groups bypass strongpoints, hit the rear), **leapfrogging** (bypass strong islands, take
  weak ones, cut the strong ones off).
- **Vanguard** (advance guard) and **rearguard**; **line of departure** (where the attack starts).
- **Feint** (a real but false attack) and **feigned retreat** (run to draw them out of formation,
  then turn - classic light cavalry; FoG II light horse evading does this naturally).
- **Shock and awe**, **overmatch** (decisive superiority in a domain), **full-spectrum dominance**.

## Holding and giving ground (defence)
**Fortification**, **entrenchment**, **defensive fighting position**, **redoubt**, **observation
post**, **barrier / area denial** (obstacles and mines to channel them), **defence in depth** (layers
instead of one line - the attacker wears out crossing them), **strategic defence**, **counterattack** (hit them as they are disorganised after attacking), **final
protective fire** (the last planned barrage in front of your position), **kill zone** (where an
ambush or defence means to kill them), **crossfire** (overlapping arcs - every target is hit from
two sides), **withdrawal** (keep contact while falling back, not a rout), **siege**.

## Fire and manoeuvre
**Firepower**, **fire and movement** (part fires, part moves, swap - the core small-unit tactic),
**suppressive fire** (make them duck, not kill - lowers their effect; in salvo terms it cuts their
alpha), **fire support**, **indirect fire** (no line of sight - needs an **artillery observer**),
**counter-battery fire** (kill their guns), **time on target** (all shells land at once - one big
salvo instead of a stream; salvo model), **bombardment**, **target acquisition**, **targeting**,
**kill chain** (find - fix - track - target - engage - assess; breaking any link stops the shot -
the core of space and missile war), **battle damage assessment** (did it work?). **Force
concentration** and **force multiplication** (things that make a force count for more: terrain,
tech, morale, surprise).

## Combined arms and troop types
**Combined arms** - each arm covers another's weakness (infantry holds, armour breaks, artillery
suppresses, engineers open the way, air finds and strikes). Troop roles as game archetypes:
**heavy infantry** (holds a line, slow), **light infantry** and **skirmishers** (open order, harass,
screen, rough ground), **line infantry** (massed volley fire), **phalanx** (deep spear block - linear
law, strong front, weak flanks), **cavalry / light cavalry** (shock or scouting and pursuit),
**mounted infantry** (ride, fight on foot), **mechanised infantry**, **armoured warfare**,
**anti-tank warfare**, **combat engineer**, **airborne / air assault**, **special operations**,
**long-range penetration**. Support: **combat support** (artillery, engineers, signals) and **combat
service support** (supply, repair, medical).

## Seeing and deceiving
**Reconnaissance**, **patrol**, **aerial reconnaissance**, **intelligence cycle** (direct - collect -
process - analyse - disseminate - feedback), **fog of war** (uncertainty; games model it with hidden
units), **camouflage**, **decoy**, **military deception**, **denial and deception**, **ruse de
guerre** (legal tricks: false signals, dummy positions), **electronic warfare** and **electronic
countermeasures** (jam, spoof - lowers enemy accuracy: salvo model's soft kill), **dispersal**
(spread out so one strike can't get everything).

## Command
**Command and control** (authority plus the means to direct forces), **military doctrine**,
**military operation plan**, **order of battle** (who has which units where - every wargame's
setup list), **military organisation** (squad -> platoon -> company -> battalion -> brigade ->
division -> corps -> army), **military reserve** (held back for the decisive moment), **rapid
reaction force**, **network-centric warfare** (shared sensors and data make the whole force
faster), **multi-domain operations** (land, sea, air, space and cyber together), **effects-based
operations** (plan by the effect wanted, not the target list), **decapitation** (strike the
leadership - FoG II: kill their general; Dominions: assassinate the commander).

## Logistics and morale
**Logistics / military logistics** (supply, transport, maintenance - an army's reach is its supply
line; operational reach in military-operations), **convoy**, **airlift**, **blockade**,
**expeditionary warfare** (fighting far from home - everything must be shipped).
**Morale** and **unit cohesion** (a unit breaks long before it is destroyed - FoG II cohesion
levels, Dominions morale; "break cohesion, not bodies" in battle-tactics), **war-weariness** at the
national level.

## Domains
- **Land / mountain / jungle / cold-weather / urban / subterranean / night** warfare - each changes
  speed, sight, supply and which arm dominates (urban and jungle favour infantry and short range;
  mountains favour the defender and light troops).
- **Air**: **aerial warfare**, **air supremacy** (they cannot fly at all) vs air superiority,
  **offensive counter air** (destroy their air force, on the ground best), **suppression of enemy
  air defences**, **air interdiction** (hit supply and reinforcements behind the front), **close air
  support**, **strategic** vs **tactical bombing**, **area bombardment**, **dogfight**, **drone
  warfare**, **precision-guided munitions**.
- **Naval**: **naval / surface / submarine / anti-submarine warfare**, **line of battle** (the
  broadside era: single line so every gun bears), **wolfpack** (subs mass on a convoy), **sea
  denial** (stop them using the sea without controlling it yourself), **fleet in being** (a fleet
  that never fights still pins the enemy by existing - Corbett on the shelf), **amphibious warfare
  / landing operation**.
- **Space and missiles**: **space weapon**, **kinetic bombardment** (rods from orbit), **missile
  defence**, **point defence** (defend one object - the salvo model's interception), **active
  protection system** (vehicle-level hard kill of incoming rounds), **anti-access/area denial**
  (A2/AD: make an area too costly to enter - long-range missiles, sensors, mines).
- **Information**: **information warfare**, **cyberwarfare**, **psychological warfare**,
  **political warfare**.
- **Irregular**: **guerrilla warfare**, **insurgency**, **counterinsurgency**, **people's war**
  (Mao, on the shelf), **partisans**, **unconventional warfare**, **low-intensity conflict**.

## Wargame mechanics named in the index
- **Zone of control** (board wargames: the hexes next to a unit). **Rigid** = an enemy entering it
  must stop; **semi-rigid** = it may enter but not move directly from one ZOC hex to another. Some
  games let terrain or other units cancel ZOCs, make ZOCs block retreat or supply, or even slow
  friendly units (road congestion). It stands for having to slow down near the enemy - and in
  alternating turns it limits what one side can do while the other can't react. Civilization uses
  one too; FoG II has primary and secondary ZOCs (fog2m-guide PLAY.md). (Checked against the text.)
- **Wargame**, **military simulation**, **operations research** (the science behind combat models
  - combat-models skill), **order of battle**.

## Related skills
military-doctrine (FM 3-90 terms with page refs - fuller on the tactical tasks), military-operations
(FM 3-0), soviet-doctrine, combat-models (Lanchester and salvo math), screening, scouting,
battle-tactics, military-theory shelf skill in Military Theory/ (Clausewitz, Jomini, Corbett, Mao,
The user's space essay), borrow-from-games (design).
