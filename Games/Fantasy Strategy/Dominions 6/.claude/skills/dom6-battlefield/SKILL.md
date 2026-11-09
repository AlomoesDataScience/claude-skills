---
name: dom6-battlefield
description: "Dominions 6 battlefield conditions: clouds, darkness, night, battlefield enchantments and their effects (manual pp. 11, 49, 67-72). Use when planning long fights, fighting in clouds or darkness, or scripting cloud spells."
keywords: "frost, heat, poison, disease, sulphur, rust, death, shimmering, light, leeching, sleep, effect, level, armour-negating, fading, round, overlap, spread, battles, twilight, berserk, end, plus, prec, nightfall, attackers, rout, defenders, everyone, left, dies, mindless, dissolve, utterdark, blind, att, def, darkvision, weather, snow, cold, x15, rain, growth, x10"
---

# Battlefield conditions (Dominions 6, vanilla)

Plan item 22 (the user approved the extras 2026-11-03). Manual pp.11, 49, 67-72. Battlefield enchantment spells:
dom6-spell-db purpose "battlefield enchantment"; casting rules: dom6-evocations.

## Clouds (pp.68-69)
- Made by beings (hydra poison, heat and chill auras), spells (Fireball leaves heat) and weapons. Fade about
  1 level a round unless fed; same-type clouds don't overlap - more sources spread the cloud wider (at most +1
  level per square). Cloud damage is **armour-negating**.
| Cloud | Per level |
|---|---|
| Frost / Heat | L1 2 fat, L2 3, L3 4 + 1 dmg, L4 5 + 2, L5+ 6+ fat + 3+ dmg (frost dmg capped 1 unless frozen) |
| Poison | 1 / 2 / 3+ poison |
| Disease | disease: easy MR at L1-2, MR at L3+ |
| Sulphur | 1 fire fat + 1 poison (L1) up to 4 + 3 (L7), poison capped 1 |
| Rust | armour rusts |
| Death | 1 / 2 / 3+ damage (MR) |
| Shimmering light | 1 capped false (easy MR) ... 3+ false (MR) |
| Leeching | weakness (permanent -1 str) + 1 capped damage, MR by level |
| Sleep | sleep (easy MR at L1, MR at L2+) |
- Heat/chill aura: 3 squares by default, + heat/cold scale (p.39).

## Long battles (p.71)
| Round | Effect |
|---|---|
| 100 | Twilight: enchantments, temporary magic and berserk end; -2 precision, +1 glamour magic |
| 150 | Nightfall (or daybreak in a night battle): **attackers rout**; darkness -3 att/def/prec |
| 170 | **Defenders rout** |
| 200 | Everyone left dies |
Mindless units dissolve instead of routing. Turn-limit planning: dom6-morale.

## Darkness (p.49)
Night -3, Utterdark -6, blind -9 to attack, defence and precision; darkvision cuts it by its level (not for
the blind). Invisible units: -9 attack in melee unless spirit sight (p.39). Sun Awe fails in darkness.

## Weather (p.72)
Snow: cold scale x 15% (cold 1+); rain: growth x 10% + 10% (heat 0+); none in wastes and caves; globals
change it; assassinations mostly indoors, 50% at night.

## Special damage (pp.67-68)
- **Fatigue damage**: unconscious at 100; capped at 200, then each 50 more = 1 HP (under 50: 2% per point).
- **False damage** (glamour, illusions): kills if real + false >= HP; no afflictions; fades 2 a round once all
  enemy glamour mages die; not healed by regeneration or life drain.
- **Paralysis** while paralysed: damage = min(old, new duration) / 2 (max 5); duration = the longer.

## Ground (p.11)
Bushes, rocks and obstacles have stats, take area damage, are crushed by large monsters; small units walk
around them.

## Related skills
dom6-evocations, dom6-buffs, dom6-morale (routs), dom6-fatigue, dom6-abilities (auras, darkvision),
dom6-sieges (weather), dom6-spell-db, dom6-mechanics.
