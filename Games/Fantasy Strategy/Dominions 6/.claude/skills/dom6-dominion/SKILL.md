---
name: dom6-dominion
description: "Dominion and scales in Dominions 6: belief vs control, max dominion, temples, prophets, preaching, scale effects. Use when planning temples, prophets and preaching, choosing scales, or fighting in enemy dominion."
keywords: "manual, military, maximum, pretender, team-size, sources, home, prophet, thrones, blood, sacrifice, temple, check, success, raise, current, spread, reduce, priest, level, minus, cap, heretics, god, bonuses, morale, six, pairs, extremes, tip, victory"
---

# Dominion and scales (Dominions 6, vanilla)

Plan item 21 (the user approved the extras 2026-11-03). Manual pp.82-87; turn order: preaching step 6,
dominion spread 42, dominion effects 43 (p.55-56). Pretender design: dom6-pretender.

## Dominion basics (pp.82-83)
- Belief, not control: conquest doesn't change dominion. One nation's dominion per province (a -3 to you is
  +3 to someone). Ctrl-3 shows enemy dominion.
- **Max dominion** in any province = pretender's dominion + 1 per (5 x team size) temples (p.83).
- **Losing all dominion = eliminated** (p.87): a besieged god can be killed by out-preaching him.

## Spreading it (pp.83-84)
- A **temple check** succeeds with 50% + 5% x max dominion. Sources: pretender (1 automatic + 2 checks),
  home province (1), prophet (1), each temple (1), thrones (1-7, once claimed), blood sacrifice for some
  nations (1 per slave, up to priest level, in a temple province).
- A successful check: neutral -> +1; friendly -> +1 with 30% - 3% x current, otherwise it spreads to a random
  neighbour (chains through friendly provinces); enemy -> -1 with 50% + 5% x max - 5% x enemy level.
  Across a sea/land border: 50% re-rolled to another neighbour.
- **Preach** (priests, own province only): 30% x priest level (+1/2 level with a temple) - 5% x enemy
  dominion, min 5%; can't push above 2 x priest level; inquisitors count double in enemy dominion. The game
  doesn't tell you when preaching stops working.
- Heretics: heretic ability x 20% a turn to lower ANY dominion there.

## Prophet (p.83)
One at a time: priest +1 (or priest 3), +2 att/def/prec, spreads like a temple, gets dominion bonuses.

## Dominion in battle and for gods (pp.85-87)
- +1 morale in friendly dominion, -1 in enemy (dom6-morale).
- Pretender and prophet per friendly level: +1 str, +1/2 MR, +10% HP; enemy: the same minus (HP min 10%).

## Scales (pp.85-86)
| Scale | Per step (positive side) |
|---|---|
| Order / Turmoil | income +-3%, resources +-2%, recruitment +-1 (%), unrest reduction +-1, events -+2% |
| Productivity / Sloth | income +-3%, resources +-15% |
| Heat / Cold | each step from a race's ideal: tax -5%, supplies -10% |
| Growth / Death | population growth +-0.2%/month, supplies +-10%, income +-1% |
| Fortune / Misfortune | 5% more events, good-event chance +-10%, hero +-0.5% |
| Magic / Drain | spells -+0.5 MR to resist (rounded down), fatigue -+10%, research +-1 per mage, start research +-50 |
- Extremes (4+): Order 4 research -2 (5: -4); Productivity 4 unrest +1-5 (5: 1-15); Heat/Cold 4 pop -0.4%
  (5: -1%); Death 4 forests and farms -> plains -> wastes; Growth 4 plains -> forests/farms; Fortune 4 income
  and resources -5% (5: -15%); Magic 4 horrors and horror marks, unrest +1-5 (5: 1-15) (p.86).
- Scales spread with dominion: each turn each scale tips one step with 5% x dominion + 10% x difference
  (p.85). Scales 4+ spread to neighbours even in other dominions.
- Seasons: summer one step warmer, winter colder (not caves or other planes); deep seas neutral.

## Using it
- Temples early raise max dominion and spread; a prophet on turn 1-2 (the user's rule).
- Fight in your own dominion (morale, god and prophet stats); a "wall of faith" of high-dominion provinces
  stops enemy spread.

## Related skills
dom6-pretender (scales and dominion at creation), dom6-holy, dom6-morale, dom6-economy, dom6-mechanics.
