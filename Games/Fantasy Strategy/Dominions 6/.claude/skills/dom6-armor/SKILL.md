---
name: dom6-armor
description: "How armour and protection work in Dominions 6: protection roll, natural plus armour, shields, encumbrance. Use when choosing armour for casters or thugs, working out what a hit does, or reading damage lines."
keywords: "manual, illwiki, body, head, combines, parry, shield, hits, destruction, armour-defeating, fatigue, piercing, negating, melee, spellcasting, mounted, halving, severe, heat, cold, defence, penalties, buffs, barkskin, stoneskin, ironskin, don't, stack, rust, achilles, invulnerability, unit, commander, judging, battle, log's, works"
---

# Armour and protection (Dominions 6, vanilla)

The user's list (2026-11-03). Manual pages in brackets, illwiki `protection`, `natural-protection`, `encumbrance`,
`rust`. Mods change armour numbers (SCBM: 56 new, 124 changed - dom6-scbm).

## Protection on the card
- **Body** protection (torso, arms, legs) and **Head** protection (helmet). The card's single "Protection" is the
  average (90% body + 10% head) - only AoE hits use it (wiki).
- Damage = (str + weapon dmg + DRN) - (protection + DRN [+ shield prot on a shield hit]) (p.60).
- Head hits (10%, more from bigger attackers) use helmet protection (+ shield on a shield hit) (p.60).

## Natural + armour (wiki)
Protection = N + A - (N x A / 40), rounded up; max effectively 40. 4 natural + 15 armour = 18.
Shields add on top, no reduction.

## Protection buffs (wiki natural-protection; inspector)
They set NATURAL protection and DON'T stack with each other:
- **Barkskin** (N): +7 up to 10 (+1 if already 10+); fire vulnerability -5.
- **Stoneskin** (E2): +10 up to 15 (+3 if already 13+); cold vulnerability -5.
- **Ironskin** (E2 Alt 5): +13 up to 20 (+5 if 16+); shock vulnerability -5.
- **Invulnerability** (death magic, Stygian) replaces natural protection if higher; magic damage ignores it.
With armour: a Tuatha with body armour 17 + Stoneskin 10 natural = 10 + 17 - 4.25 = 23 (vs 21 with Barkskin).
SCBM: the AI never casts the skin spells on its own - script them (dom6-scbm).

## Shields (p.60-61)
- Parry: added to defence only to decide shield hit vs clean hit; the shield's protection then adds to the
  protection roll. A shield costs a little defence (-1 typical) and encumbrance.
- Trample ignores parry (only its defence penalty counts) - dom6-tactics.
- Missiles: defender adds 2 x parry to his roll (p.65) - shields are strong vs arrows.
- **Destruction**: break value = damage before protection (+50% slash, +25% blunt) vs shield resistance (shield
  prot, +5 magic [wiki +15/+25]): >= 3x = damaged (-20% prot), >= 5x = broken (-50%); damaged again = 25%
  broken. Magic shields repair after battle unless broken (then lost); mundane ones repair with resources.

## Armour-defeating hits (p.61)
Protection DRN of 2 = only 75% of protection counts; 3 also if the target has 50+ fatigue; 4 at 100+ fatigue,
immobile or unconscious. Rare on fresh units; common on tired, entangled, melded (Earth Meld!) or sleeping ones.

## Piercing, AP, AN (p.62, 65)
Pierce -15%, AP -50% (both = -65%), AN = none. Fire is AP; lightning (shock) AN; acid and cold at least AP.

## Encumbrance (p.62, 76; wiki encumbrance)
- Base encumbrance (humans ~3, hardy 2, cold-blooded 4, demons 1, undead/inanimate 0) + armour + shield enc.
- **Melee**: fatigue = encumbrance per attack (and per flight). Mounted riders count armour enc at half.
- **Spellcasting**: base + 2 x armour/shield enc per cast, never halved (dom6-fatigue). Robes for casters.
- Temperature 3+ either way adds (temp - 1), cut 1 per 5 matching resistance; zero-base units exempt.
- Armour also lowers defence (shown on the card, e.g. scale cuirass -1).

## Armour damage
- Damaged armour -20% prot, broken -50% (wiki, same as shields).
- **Rust** (acid, rust mist, underwater): rusty iron gear may be damaged by hits (chance = (damage - shield
  prot - DRN) x 2%), replaced after battle (wiki rust).
- **Armor of Achilles** / **Destruction** / Gaia's Due (SCBM): armour-damage spells, "almost totally destroys
  the target's armor and shield", magic armour resists, natural protection untouched (game text). Exact
  amount per point of "armour damage" is not documented (wiki: "not well understood") - check in a battle log.

## Choosing armour
- Casters: as light as possible (each armour enc point = 2 fatigue per spell). Dagda's Blacksteel Plate costs
  him ~4 per cast - better on Lugh, who fights.
- Thugs/front: heavy armour + shield + skin buff; watch encumbrance in long melees (fatigue -> defence ->
  armour-defeating hits).
- Against archers: shields (2x parry) and Air Shield / Protective Winds.

## Related skills
dom6-weapons, dom6-fatigue, dom6-precision, dom6-buffs (when built), dom6-items, dom6-mechanics, dom6-scbm.
