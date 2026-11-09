---
name: combat-models
description: "Combat models for playing and designing games: Hughes' salvo model, Lanchester's laws, Helmbold, with combat.py. Use when judging if a fight is worth taking, how to concentrate or split fire, or designing combat."
keywords: "mathematical, words, wikipedia, articles, copies, military, theory, wiki, view, leads, relevant, today's, artillery, direct-fire, world, lanchester, generalization, many, small, exchanges, covers, hughes, offensive, salvos, minus, interceptions, over, staying, power, first, strike, decides, linear, square, half, numbers, need, four, times, quality, concentration, defeat, detail, helmbold's, parameters"
---

# Combat models - salvo first, Lanchester as its generalization

**The user's view (2026-11-02):** "I generally believe in salvo as more relevant than Lanchester's laws
right now in our artillery/direct fire based world. In general, I think of Lanchester's laws as a
generalization of squad based salvo type battles." The math agrees: with no interception (y = z = 0)
and many small salvos, the salvo exchange dA = -beta*B per salvo becomes Lanchester's square law in
the limit. So use the **salvo model by default** when fire comes in discrete, accurate, lethal pulses
that can be intercepted, suppressed or pre-empted (artillery, missiles, tank and ATGM duels, air
strikes, a squad's volley); use **Lanchester** as the smoothed big-picture view of many such
exchanges, or for fights that really are continuous streams (massed small-arms, melee lines).

Sources (CC BY-SA, summarised in Claude's words): Wikipedia "Lanchester's laws" and "Salvo combat
model", wikitext in `Military Theory/wiki/*.wiki` (fetched 2026-11-02 via the API). Further reading
named there: Lanchester, *Aircraft in Warfare* (1916, on Wikisource); Hughes (1995) salvo model;
Helmbold (2021) *The Key to Victory*; Dupuy, *Numbers, Predictions and War*; Ernest Adams'
"Kicking Butt by the Numbers" (game design column).

## Lanchester's laws (Lanchester and Osipov, 1915-16)
Attrition as a race: each side's losses per unit time depend on the other side's size and quality.
- **Linear law** - only part of each side can fight at once: one-on-one duels (phalanx against
  phalanx, a frontage-limited melee), or unaimed fire into an area (losses depend on target density).
  Strength = quality x numbers. 2,000 vs 1,000 of equal quality -> the winner keeps 1,000 (half).
- **Square law** - aimed fire where everyone can shoot at everyone: losses depend only on how many
  shoot at you. Strength = quality x numbers^2. 2,000 vs 1,000 -> the winner keeps ~1,732 and loses
  only 13%. **To make up for half the numbers you need four times the quality.** Equations:
  dA/dt = -beta*B, dB/dt = -alpha*A; invariant alpha*A^2 - beta*B^2.
- Real fights mix both; analysts often use an **exponent of 1.5**.
- Limits: pure attrition. It ignores manoeuvre, morale, terrain, command, and the fact that a whole
  army is never engaged at once - which is exactly where tactics win.

### What it means for play
- **Concentrate.** Under the square law the bigger force wins cheaply, so mass fire and force at one
  point (principle of mass; Soviet 3:1). Splitting gets you **defeated in detail**: 1,500 beat 1,000
  all at once, but in three parts of 500 each part loses and the 1,000 keep 500.
- **Choose the law the fight follows.** If you are outnumbered, make it linear: narrow frontage,
  defiles, one-on-one contact, terrain that stops their extra units joining in (Thermopylae logic).
  If you outnumber them, make it square: open ground, everyone shooting, overlap their flanks.
- **Focus fire.** Many shooters on one target at a time - every unit you remove stops shooting back.
  (FoG II: all shooters on one knight unit; Dominions: concentrate spells and archers.)
- **Quality vs numbers** in army building: with square-law fire, numbers beat a small elite unless
  the quality gap is the square of the numbers gap; with linear melee, quality goes further.

## Helmbold parameters (history-based)
From start strengths and losses: casualty fractions F_A and F_D; **defender's advantage**
mu = sqrt(F_A / F_D) (above 1 = the defender did better); **bitterness** eps = sqrt(F_A x F_D).
Helmbold (2021, from battles since 1600): P(defender wins) = logistic(-0.1794 + 5.8694 x ln mu);
the defender's advantage has stayed about constant since 1600; bitterness and casualty rates fell
steeply after 1939. Use it to rate a finished game battle the same way historians rate real ones.

## Salvo combat model (Wayne Hughes, Naval Postgraduate School, 1995)
For combat in a few big, accurate, interceptable pulses - anti-ship missiles, carrier strikes
(bombers vs fighters), torpedoes (no interception), and by analogy the user's space warfare.
Each side: A units; alpha = missiles each fires per salvo; y = incoming missiles each intercepts;
w = hits needed to put one unit out (staying power). One exchange:
`dA = -(beta*B - y*A) / w` and `dB = -(alpha*A - z*B) / x`, never below 0 or beyond the force.
- Missiles that get through = what was fired minus what was stopped; **defense only matters until it
  is saturated** - past that point every extra missile hits.
- Battles are short and lethal: often one or two salvos decide it. **Firing first** (out-scouting,
  surprise) is decisive - the side found first can be destroyed before it shoots.
- Three levers: more offence (alpha), more interception (y), more staying power (w). Scouting
  (finding them first) multiplies all three.
- Variants: area fire (target position only roughly known - spread fire), stochastic (random
  parameters), one side firing first, ballistic-missile defence (used on Iron Dome).
- Ties to the user's essay (military-theory shelf): armour is beaten by serious weapons -> staying power
  is low; the real defence is not being hit -> interception (point defence) and E-War/stealth, which
  lower the enemy's *effective* alpha. Tracking decides who fires first.

## Other domains - first review (the user: "Air, space, and naval all need to be reviewed")
Draft for the user's review - what changes from the land system in each domain:
- **Naval** - Hughes' basic model as it stands: few units, big salvos, interception (CIWS, SAMs) as
  defensive fire, staying power in hits per ship, **scouting decides who fires first**; no frontage
  (everyone in range engages), no tactics saves except EW/decoys (soft kill = lowers effective
  accuracy); gun-era fleets drift back toward Lanchester streams (many shells, low hit chance), and
  crossing the T is a frontage effect. Torpedoes: no interception.
- **Air** - sorties instead of continuous presence (salvos per period = sorties); fighters and SAMs
  are interception against the strike; escorts intercept the interceptors (a layered salvo);
  detection range and initiative dominate (bounce = first strike); fuel and time on station limit
  periods; damage is mostly binary per aircraft (staying power ~1).
- **Space** (the user's essay) - everything is tracked, so spotting is near-certain but **targeting** is
  not: EW and stealth lower accuracy, not detection; point defence = interception; armour is beaten by
  any serious weapon (staying power ~1 hit); no cover or frontage; lasers are streams (Lanchester-like),
  missiles and kinetic salvos are Hughes-like; area weapons are weak against tracked direct fire;
  ranges and travel times make initiative and pre-commitment (who launched first) the core decision.
- Common open question for all: the morale/"kick it or stick it" step and initiative, still to design.

## combat.py (scripts/)
```
python3 -I .claude/skills/combat-models/scripts/combat.py law A B ALPHA BETA [--n 2|1|1.5]
python3 -I .../combat.py sim A B ALPHA BETA [--n 2]          # the fight over time
python3 -I .../combat.py split A B ALPHA BETA K              # A split in K parts vs B: defeat in detail
python3 -I .../combat.py need A B ALPHA BETA                 # quality or numbers needed to break even
python3 -I .../combat.py salvo A B ALPHA BETA Y Z W X [--rounds N] [--first red|blue]
python3 -I .../combat.py land RED.json BLUE.json [--salvos N] [--dice] [--first red|blue]   # the user's land system
python3 -I .../combat.py helmbold A0 D0 A_LOSSES D_LOSSES
```
Checked 2026-11-02: square 2000 v 1000 -> 1732 left; linear -> 1000; need 4x quality at half numbers;
sim matches the formula; split 1500 in 3 v 1000 -> all three lose, 500 of B left.
Review 2026-11-02: `sim` was wrong for n != 2 (linear law ended at 271 instead of 1,000) - fixed with a
common factor (A*B)^(2-n), so n = 1, 1.5, 2 now match `law` exactly. Helmbold mu and eps checked against
the article.

## Using it in a game
Estimate alpha/beta from the game's own numbers (casualties per shot or per turn from the manual,
tooltips or a past fight), decide which law the engagement follows (frontage-limited melee ~ linear,
open-ground massed shooting ~ square), run `law` or `split`, and let the result shape the plan:
attack where you can make it square in your favour, defend where you can make it linear.

## Reference files (read the one the step needs)

| File | Holds |
|---|---|
| `reference/salvo-combat-system-for-land-battles.md` | **The user's Salvo Combat System for Land Battles (his design - `Military Theory/Salvo Combat System for Land Battles`)** - An earlier version of his own system (the newer one is somewhere from before the move to this PC) |

## Related skills
war-concepts (glossary: kill chain, point defence, A2/AD, time on target...), military-doctrine (mass, fix and envelop - how to make the fight lopsided), military-operations
(principles of war: mass, economy of force), soviet-doctrine (3:1 norms), battle-tactics,
scouting (finding them first = firing first), borrow-from-games and the 4X engine design (combat
resolution), military-theory shelf (the user's space-warfare essay).
