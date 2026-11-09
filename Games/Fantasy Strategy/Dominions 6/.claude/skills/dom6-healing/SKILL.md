---
name: dom6-healing
description: "Hit points, healing, regeneration and afflictions in Dominions 6. Use when an elite unit or commander is wounded or afflicted, when judging regenerating thugs, or choosing healing items or blesses."
keywords: "reconstruction, manual, illwiki, full, back, turn, diseased, never, heals, in-battle, max, round, cuts, affliction, chance, reforming, flesh, undead, inanimate, lost, blow, minor, major, body, part, profuse, bleeding, limp, cripple, march, recuperation, healers, disease, gift, health, chalice, immortality, resistance, curses, stat, gains, monsters, regen"
---

# Healing, regeneration and afflictions (Dominions 6, vanilla)

The user's list (2026-11-03: "regen/reconstruction"). Manual pp.41-42, 71; illwiki `regeneration`,
`recuperation`, `healer`, `immortal`, `afflictions`, `never-heals`. Plan items 9 and 18.

## Hit points
- Units get all HP back after each turn's battles unless diseased or "Never Heals" (wiki). Damage only
  matters inside one battle - afflictions are what last.
- Magic beings with Never Heals recover HP in a lab (wiki).

## Regeneration (in battle)
- Regeneration N% restores N% of max HP every round (rounded up), only when damaged (wiki).
- Also divides affliction chance: 5% no effect, 10% halves, 15% 1/3, 20% 1/4 (n/5) (wiki).
- Undead: **Reforming Flesh**; inanimate (non-undead): **Reconstruction** - the same thing for them (Death and
  Earth blesses). Glamour mages regenerate false damage; Blood bless (Enchanted Blood) 0.5 HP a round.
- Regeneration + high protection = a unit chaff can't kill: damage under the regen rate is wasted (thugs).

## Afflictions (pp.41, 71)
- Chance per blow = % of max HP lost in that blow (a 4-damage hit on a 10-HP man: 40%); over 100% gives a
  second one. Cursed +15% first (wiki); Affliction Resistance N may set it to 0.5% (chance N/(N+1)).
- Major chance = affliction chance / 1.5, max 33%. Body part decides the kind:
  | Part | Minor | Major |
  |---|---|---|
  | any | Battle Fright (-5 morale), Profuse Bleeding | |
  | head | Eye Loss (-3 prec... ), Mute | Dementia, Feeblemind (no spells, no leading), Blindness |
  | chest | Chest Wound (+encumbrance), Never-Healing Wound (-max HP) | Disease (dies slowly) |
  | arm | Weakened (-str) | Lost an arm (slot gone) |
  | leg | Limp | Crippled |
- Profuse bleeding: -5% HP and +10 fatigue a round, 10% a round to stop (regeneration helps; underwater
  halves); it finishes routers off-map (dom6-morale).
- Limp: commanders -4 map move; troops 25% to become crippled if the army marches 2+ provinces in a month.
  Cripple: commanders lose 75% map move; troops 35% to die on any march, 70% marching 2+ provinces.
- Big units (high HP) rarely get afflicted by small hits - another reason thugs survive.

## Curing (p.41; wiki)
- **Recuperation** (unit ability; Pangaea's units, the Ghost Moose): one affliction a turn at most, by a fixed
  priority (battle fright 50%, feeblemind 25%, dementia, disease, crippled... never-healing wound 10%).
  Not for the old, undead or inanimate.
- **Healer N**: cures up to N afflictions a turn on others in the province (works on the old).
  **Disease healer** (Miraculous Cure-all Elixir): diseases only. **Corpse stitcher**: corporeal undead.
- Gift of Health (global, own dominion), The Chalice (5 a turn), healing sites, a few disease rituals.
- Immortal / dominion-immortal units reform at home and shed the worst afflictions.
- Cursed-item afflictions (Eye of Aiming, Black Heart) stay until the item comes off.
- Curses and Horror Marks are not afflictions and can't be removed.

## XP (p.41)
1 XP a month; +4 for a won battle, +1 retreat (once a month); +1 per melee strike. Stars at 15/50/100/200/400
XP: att/def/prec +1 each, str and HP at some, morale +1, leadership +25/+50, MR +1 at 400, RP +1 (mages).

## Using it
- Pull a wounded thug back when afflictions start (feeblemind ends a mage; disease kills slowly).
- Keep elite squads near a healer province; Tir na n'Og: no native healers - check items/sites.
- Regeneration thugs: kill them with big hits (AN/AP evocations, MR spells), not many small ones.

## Related skills
dom6-armor, dom6-morale, dom6-fatigue, dom6-thugs, dom6-supercombatants, dom6-items, dom6-mechanics.
