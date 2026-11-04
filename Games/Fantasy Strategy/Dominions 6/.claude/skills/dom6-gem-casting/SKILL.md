---
name: dom6-gem-casting
description: How magic gems work in Dominions 6, from the manual: in battle a gem gives a mage +1 skill in its path for one spell in one round (cast one level above his skill, or halve the fatigue; max +1, gems per round <= his skill, never a path he lacks); gem-cost spells need the gems in his inventory before battle; the Conservative gem usage box; spell fatigue (cut by levels above, plus encumbrance per cast); the 40-gem carry limit and gem squires; transferring gems (F7, a commander's gem slot, the lab pool); and gems outside battle - rituals, extra gems for enchantment duration and dispel strength, forging, empowerment, alchemy, cataclysm horrors. Use when scripting mages, handing out gems before a battle, planning which spells a mage can reach with gems, budgeting fatigue, casting rituals or forging, or when the user mentions gems.
---

# Gem casting (Dominions 6, vanilla manual)

The user (2026-11-03): "go read the manual for that, gems can do a bunch of things you apparently don't know
about. As usual make it a skill." I had said Eigneach (Nature 1) couldn't cast his scripted Group Barkskin
(Nature 2) - he carries nature gems, and one gem makes him Nature 2 for that cast.

Vanilla rules, manual pages in brackets. Mods change gem COSTS of spells (SCBM: dom6-scbm `spell-changes.md`,
136 spells cheaper), not these rules unless their files say so (mod-docs).

## Gems in battle (p.79-80)
- **A gem = +1 skill in its path for ONE spell in ONE combat round.** Uses:
  1. **Reach**: cast a spell one level above the mage's skill (Nature 1 + a nature gem = Group Barkskin, N2).
  2. **Fatigue**: a spell he can already cast, cast one level above the minimum = half fatigue (below).
  3. Both at once only if he is already at the requirement (then the gem only cuts fatigue).
- Limits: **at most +1 level** from gems; **gems per round <= his skill in that path** (a Nature 1 mage uses one
  nature gem a round); **never a path he has 0 in** (gems and items only raise a path he already has, p.76).
- **Gem-cost spells** (e.g. Swarm 1N): the gems must be in the mage's own inventory BEFORE the battle (p.75).
- A scripted spell with missing gems or no target in range falls back to an AI pick (p.46).
- **Conservative magic gem usage** (the checkbox in the commander's battle orders): gems only for SCRIPTED
  spells, as sparingly as possible - saves gems for later battles. Unchecked: the AI spends them to cut fatigue
  on whatever he casts. "Otherwise there is no opportunity for the player to intervene." (p.80)
- Not the same as battle spells that raise a path for the whole battle (Power of the Spheres): a gem lasts one
  spell.
- **Overcasting, from the wiki** (illwiki `magic.txt`, Overcasting + Gems for Combat Magic; the user didn't know
  either - "good question, I actually don't know"; the manual is silent): many spells get stronger per level
  above the requirement (area, range, effects "+X per level"), measured on the PRIMARY path only, and every
  SECOND extra level adds +1 penetration (11 at the minimum). The gem's +1 counts "for making the spell better"
  - so a gem does widen "+X/lvl" spells and helps penetration on every second level.
- **Manual vs wiki on fatigue** (unresolved - check a battle log): the manual says gems never raise skill by more
  than one. The wiki says that cap is only for spell strength; for FATIGUE a mage may spend as many gems as his
  skill in that path, each counting as a level (E2 Dagda + 2 earth gems on Destruction: wiki 1/3 fatigue,
  manual 1/2). Order of truth: game > manual > wiki - until a log shows it, plan on the manual's half.
- Gem-cost spells: the required gems are spent at any skill; extra gems on top only cut fatigue (wiki example:
  Summon Fire Elemental, F3 + 1F).
- **Magic scale** (wiki): each Magic point -10% spell fatigue, each Drain point +10%, additive.
- Fatigue cap 200 (wiki fatigue page): fatigue past 200 can turn into HP damage. A mage at 100+ can't cast.

## Fatigue budget of a caster
Full rules in **dom6-fatigue**. In short: spell cost x 1/(1 + levels above, gems included) x scale, plus base
encumbrance + 2x armour encumbrance every cast (gems don't cut that part); unconscious at 100, back after
5 a round. Passing out after the script is done is fine (the user), except in communions (dom6-communions).

## Carrying and moving gems (p.46-47, 79)
- Any commander can carry gems, even a non-mage; **limit 40 per commander** -> a "gem squire" next to the mage
  (gems must be in the CASTER's inventory for battle - move them before the battle, there is no in-battle pass).
- Transfer: F7 Magic Resource Treasury -> "Transfer gems to commanders", or click a commander's personal
  gem slot (unit card) -> Transfer Magic Resources: two commanders of the province, plus the national pool if
  the province has a lab. Left-click a number = +1 to that column, right-click = -1.
- F7 "pool": collect all gems from commanders in a lab province into the national pool.
- Gems reach the treasury each turn from sites connected through friendly land to a lab province (p.79).

## Gems outside battle
- **Rituals** (p.76): gems come from the national pool, only in a lab province. Not cast = usually not enough gems.
  Shift+m = recast every month while gems last.
- **Local enchantments**: extra gems = longer duration (most 1 month per extra gem, some 3 months).
- **Global enchantments** (p.77): extra gems make it harder to dispel; max gems in a ritual = path level x 100.
- **Dispel** (p.77): each side +1 per extra gem, +5 per caster level above the requirement, + DRN; higher wins.
  Globals die with their caster - extra gems don't stop an assassin.
- **Forging items** (p.80): "Forge Item" in a lab; Construction research level + the mage's skill + the gems.
  Level 9 = unique artifacts; a "yearning" artifact costs half.
- **Empowerment** (p.75): permanent +1 path; first level 50 gems, then 15 x the target level (N1 -> N2 = 30).
  The only way to gain a new path.
- **Alchemy** (p.82): any mage in a lab province; gems -> astral pearls or pearls -> any gem at 2:1 (4:1 for a
  type-to-type swap). Earth/Fire Alteration rituals turn gems into gold.
- **Cataclysm** setting (p.17): rituals, forging and empowering may draw horrors - more gems, worse horrors.

## Scripting checklist with gems
1. For each scripted spell: path needed vs the mage's path; one short -> one gem of that path per cast.
2. Gems in his inventory (not a squire's) before End Turn; count = casts that need them.
3. Spells he already meets: a gem halves their fatigue if the AI (or conservative use) spends it.
4. Fatigue sum incl. the encumbrance part; trim the script below ~90.
5. Conservative gem usage on if the gems are for scripted spells only / to be saved.

## Related skills
dom6-mechanics (the manual), dom6-spells (spells and gem costs), dom6-items (forging), dom6-game (battle
orders screen, checkbox), dom6-tactics, dom6-scbm (SCBM gem costs), mod-docs.
