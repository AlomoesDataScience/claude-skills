---
name: dom6-fatigue
description: "Fatigue in Dominions 6 battles: what builds it, spell fatigue, encumbrance, unconsciousness and recovery. Use when scripting or budgeting a caster's spells, choosing armour, or reading fatigue in a battle log."
keywords: "manual, illwiki, attack, cut, skill, levels, above, requirement, spellcasting, base, cast, gems, magic, drain, scales, defence, armour-defeating, hits, likelier, unconscious, damage, past, round, while, reinvigoration, plan, mage's, script, order, value, let, pass, after, job, done, rule, except, communions, long, gem-heavy, mages, caster, thug, works"
---

# Fatigue (Dominions 6, vanilla)

The user (2026-11-03): "fatigue and communions need their own skills." Also: "reread rules on fatigue, it's not
a bad thing to get knocked out unless you're in a communion, then it's iffy, but not too iffy unless it's
gonna be a long battle with a lot of gem casts." Sources: manual (pages in brackets), illwiki `fatigue.txt`,
`magic.txt` (wiki = lower truth; marked).

## What builds fatigue
- **Attacking**: each attack adds the unit's Encumbrance (p.62).
- **Spells** (p.76): listed cost x 1/(1 + levels above the requirement): +1 level = 1/2, +2 = 1/3, +3 = 1/4.
  Gems can supply levels (dom6-gem-casting). Divine (holy) spells have no listed fatigue.
- **Spellcasting encumbrance**, every cast, holy spells too: base encumbrance + 2 x the encumbrance of armour
  worn. Skill and gems don't reduce it (p.76). A caster in plate pays for it on every spell.
- **Scales** (wiki): each Magic point in the province -10% spell fatigue, each Drain point +10% (additive).
- Some attacks and spells deal fatigue directly (Torpor, cold, Thunder effects).

## What it does
- Defence -1 per 10 fatigue; attack -1 per 20 (p.62); wiki: also -1 to defence rolls vs missiles per 20.
- Armour-defeating hits: more likely with fatigue; immobile and unconscious units count as 100 (p.61). Wiki:
  from 50 fatigue three times as likely.
- **Unconscious at 100** (p.62, p.46): can't move, attack or defend - helpless. Regains 5 a round until under
  100, then acts again. A mage can start a spell at 99: the cast can push him far over (99 + 45 = 144 = ~9
  rounds out).
- **200 cap**: fatigue beyond 200 becomes HP damage (p.62); wiki: chance = excess x 2%; communion slaves always
  take 1 HP when pushed past 200 (dom6-communions).

## Recovery
1 a round for everyone, 5 while unconscious, + Reinvigoration points (wiki). Drain damage removes fatigue
= 2x the damage (weapon drain usually capped at 10). Spells: Reinvigoration, Relief (p.76).

## Planning a caster (the user's rule)
- **Passing out after the job is done is fine.** A stay-behind mage who has cast his script did his work.
  Don't trim a script to stay under 100: order it by value - the spells that must happen first, extra casts
  last (they happen if the fight lasts, after he wakes).
- It is a cost when: enemies can reach the back (an unconscious mage is helpless: fliers, enveloping cavalry,
  assassins); he is the army's leader in a long fight; he is in a **communion** (iffy - see dom6-communions);
  a **long battle with many gem casts** (he wakes, casts once, goes out for longer each time).
- Budget in script order: per cast (spell cost after skill/gem cut x scale) + spellcasting encumbrance; mark
  the round he goes out. Light armour (robes) on pure casters; plate only on casters who must survive melee.
- Thugs and front troops: encumbrance x attacks per round; heavy infantry tire in long melees - rotate or
  give reinvigoration.

## Related skills
dom6-gem-casting (gems cut fatigue), dom6-communions (shared fatigue), dom6-mechanics, dom6-tactics,
dom6-spells, dom6-battle-view (battle logs show fatigue), mod-docs (mods may change costs).
