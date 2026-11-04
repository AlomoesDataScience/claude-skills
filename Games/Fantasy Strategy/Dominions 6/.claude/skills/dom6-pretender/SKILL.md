---
name: dom6-pretender
description: Design a Dominions 6 pretender god well, the way the Pretenders Calculator (zollqir.github.io/pretenders-dom6) does and beyond it: for a nation (vanilla or modded) and a goal, find the cheapest chassis for the wanted magic paths, dominion and scales, maximise bless points, pick blesses for the nation's sacred units, compare chassis stats, and write the final design with itemised costs and an AI pretender template. Uses the dom6-inspector, dom6-mechanics, dom6-play, dom6-modding and dom6-modinspector skills. Use whenever the user asks for a pretender or god design, which chassis or body to take, how many points something costs, what blesses or scales to take, a bless or rush or rainbow or sleeper god for a nation, or an AI god template for a mod.
---

# Designing a Dominions 6 pretender

`scripts/pretender.py` is a Python port of the Pretenders Calculator's rules and data (source,
version and commit in `data/VERSION`; site version 2.05.0 for Dominions 6.32), with chassis stats
from the dom6-inspector skill and modded nations from the dom6-modinspector skill. Run it from
this skill's folder with `python3 -I`; no pip needed.

```
scripts/pretender.py nations ulm                        # ids: 13 EA Ulm, 60 MA Ulm, 101 LA Ulm
scripts/pretender.py nation "MA Ulm"                    # default scales, scale limits, bless bonus,
                                                        # cheap gods, every god it can take
scripts/pretender.py god "Master Lich"                  # one chassis; god dragon lists the dragons
scripts/pretender.py design "MA Ulm" --paths "F4 S4" --dom 5 --scales "order=2 prod=3 misfortune=2"
scripts/pretender.py optimize "MA Ulm" --dom 4 --scales "order=2 prod=2" --prison dormant
scripts/pretender.py build 5 2785 --paths "F4 S4" --dom 4 --scales "order=2" --prison dormant \
        --bless "Solar Weapons,Magic Resistance"        # itemised design + blesses + AI template
scripts/pretender.py blesses "W9 E4 N3" --scales "magic=1"
```

Design options: `--paths`, `--dom 1-10`, `--scales` (order/turmoil, prod/sloth, heat/cold,
growth/death, luck/misfortune, magic/drain; unset ones stay at the nation's free default),
`--prison awake|dormant|imprisoned`, `--chassis humanoid,monster,titan,immobile`, `--top N`,
`--all` (also unaffordable ones). Nation 0 = any nation.

Modded nations: inspect the mod first with dom6-modinspector, then add `--mod DIR` (its output
folder). The god lists come from the modded game, and the nation's `#cheapgod20/40`,
`#blessbonus`, `#idealcold` and `#def...` scale commands from its .dm files. Modded gods with
`#gcost 10000` are autocalculated by the game and have no known form cost: read it in the game's
pretender screen and pass `--cost 6440=150`.

## The rules it uses (manual pages 30-37, checked against the site's code)

- 450 points; Dormant +150 (appears about a year in), Imprisoned +350 (about three years).
  Some gods must sleep (`minprison`); they are left out when awake.
- Form cost (minus 20 or 40 for the nation's cheap gods).
- Magic: each level bought costs 8, 16, 24... per path, counted from the chassis' own level. The
  first level of a path the chassis lacks costs its "new path cost" (10 for arch mages, up to 80
  for dragons) instead of 8.
- Dominion above the chassis' base: 7, 14, 21... per candle, max 10.
- Scales: 40 points per step from the nation's default (taking a bad side gives 40). Heat or
  cold away from the nation's ideal gives 40 per step either way. Limit ±2. A chassis attuned to
  a scale (`attunement` column, e.g. Master Lich Grw-1 = Death 3 allowed, Growth only 1) or a
  nation limit moves it by one; the two do not stack.
- Bless points = each path level above 1 (the chassis' own levels count), plus the nation's bless
  bonus. A bless costs the sum of its path requirements and may also need a scale. Incarnate
  blesses (`*`) work only while the god is awake and alive; `+` blesses can be taken more than once.
  Blessed sacred units get +1 morale and all the blesses.

## Workflow

1. **The brief.** Nation (and mod, if any), era, single player vs AI or multiplayer, and what the
   user wants the god to do. If they don't say, pick a role from the nation's strengths and say why.
2. **Read the nation** with the other skills:
   - `pretender.py nation X` for scales, limits, bless bonus, cheap gods and the god list.
   - dom6-inspector: `inspector.py nation X` (recruits, mages, national spells) and
     `inspector.py filter unit holy=1 "nationname~X"` for the sacreds, their cost and stats. Many
     good sacreds mean bless points pay off; mages that lack a path the god can supply matter for
     research and rituals.
   - dom6-mechanics for numbers: scale effects (income, resources, supply, research, events),
     dominion spread, a pretender's dominion bonus (+1 str, +½ MR and +10% hp per friendly candle),
     research per mage (5 + 2 × magic levels).
3. **Pick a role** *(reasoning, not from the manual)*:
   - Bless god: one or two paths high enough for the strong blesses (`pretender.py blesses` shows
     what each level unlocks), for nations with many sacreds. Incarnate blesses need it awake.
   - Awake fighting god: a tough chassis (hp, protection, MR, regeneration, flying, immortality in
     the stats column) with paths for its own buffs. Check fights with dom6-mechanics'
     `combat_calc.py` against the province defence and armies it will meet.
   - Sleeping mage god (dormant or imprisoned): many paths for research, rituals and the
     nation's missing paths; `optimize` finds the most bless points too.
   - Dominion and scales god: a cheap chassis (often immobile) with high dominion and strong
     scales for the economy.
4. **Scales.** Work out what each step is worth for this nation with dom6-mechanics (Order and
   Productivity for income and resources, Growth for supply, Magic for research and enemy MR,
   heat from the ideal costs income and supply). Taking Misfortune, Drain, Turmoil, Sloth or Death
   pays for magic and dominion, each with a real cost; say which you chose and why. Steps of 4+
   have side effects (manual page 86).
5. **Find the chassis.** `design` (cheapest first, with stats) and `optimize` (most bless points).
   Then compare the best 3-5 on their full pages (`inspector.py unit ID`): abilities, spells,
   item slots, immortality, mobility, starting site. Sprites are in `inspector.py sprite ID`.
6. **Finish.** `build` the chosen design with its blesses. Present: chassis, sleep, paths,
   dominion, scales, blesses, the point arithmetic, points left (unspent points are wasted:
   suggest how to use them), and the one or two alternatives you rejected and why.
7. **In game.** The pretender screen shows the real costs; ask the user to check them there and
   save the design with Ctrl+S (Ctrl+L loads). For an AI god in a mod, put the `#newtemplate`
   block from `build` into the .dm (dom6-modding skill; `#form "Name (id)"` as the modding manual
   says) and run `check_dm.py`. To playtest the god, see dom6-play.
   The dom6-pretender-ingame skill (`build_god.py`) enters and saves the design in the running
   game through Game Tools and reads the game's points back; dom6-ui drives the game by hand.

## What strong players do (illwiki, Cybertron2's "Basics of Higher Level Pretender Design", Dom6)

Read it with `wiki.py show basics_of_higher_level_pretender_design` (dom6-wiki skill).
Multiplayer advice; against the AI the early pressure is softer.

- **"To get to turn 50 you must first get past turn 10."** A late-game build is weak early, and
  other players will notice and attack it. At high level, players **trade scales for a bigger
  bless and a better god**.
- **Scales they give up first:**
  - Misfortune and temperature (they don't affect unit production);
  - then some Order and Production (keep the thresholds the nation's recruiting needs);
  - often Drain.
  - Magic is divisive: it doesn't win the first war.
- **Rainbow bless on a good sacred:** many small stats make the unit the capital already
  pumps out more efficient. Strength is +1 damage per hit; defence on high-defence cavalry
  makes it near unhittable.
- **Mage rainbow bless** (hp on communion slaves, resistances, penetration): strong late, weak
  early. The guide names **MA Pythium** as the nation it suits, because it has a strong early
  game *and* mages that want it late.
- **Incarnates are picked to synergise:**
  - Fire Shield + Fateweaving;
  - Invulnerability + Fear;
  - Hardskin + 10 fire / 10 shock resistance.
  - Blesses get better faster than linearly, so combinations beat lone picks.
  - Usually take them awake: high-level wars start before turn 12.
- **Expanders** suit MA and LA (harder independents) and nations that can't expand before
  taking their capital circle.
- **"Resist rainbows"** haven't done well in Dom6.

## Where the data and the manual disagree

The site tracks game patches; the game manual is older. Differences in the bless list (the site's
values are used; the game's own Magic screen is the final word):

| Bless | Site | Manual |
|---|---|---|
| Inspirational Presence | Fire 3 | Fire 4 |
| Fear | Death 9 + Turmoil 1 | Death 8 |
| Dread | Glamour 8 + Magic 1 | Glamour 7 |
| Heroism | +35% experience | +50% experience |

Not modelled by the site or this script: path-only bless bonuses (`#fireblessbonus` etc.,
reported as notes for mods), new or changed blesses from mods (`#selectbless`), the "first 3
clicks" cap on heat points, and form costs of autocalculated modded gods. The site's scale limits
and chassis classes (by base dominion 1-4: humanoid, monster, titan, immobile) are copied as is.

## Updating

`python3 -I scripts/update.py` re-clones github.com/zollqir/pretenders-dom6 and rewrites `data/`
(its JSON files, plus the bless list and nation fixes read from its JavaScript as plain data,
without running the site's code). Chassis stats come from dom6-inspector's `data/`; rebuild that
skill after a game patch too.

## Related skills
dom6-pretender-ingame (build it in game), dom6-nations, dom6-inspector, dom6-play.
Also (2026-11-03): dom6-dominion, dom6-holy, dom6-supercombatants.
