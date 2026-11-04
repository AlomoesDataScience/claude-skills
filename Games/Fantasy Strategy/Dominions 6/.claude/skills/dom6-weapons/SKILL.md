---
name: dom6-weapons
description: How weapons work in Dominions 6 melee, from the manual (pp. 60-65) and illwiki - the attack/defence and damage/protection rolls, weapon stats (damage, attack, defence, length, attacks), damage types (slash +25% after protection and lops limbs, pierce -15% protection, blunt +25% on heads and vs shields), armour-piercing and armour-negating, two-handed (125% strength), multiple weapons and ambidextrous, bonus weapons, repel by length (full roll sequence), reach and hit locations, harassment, lance charge bonus, dancing weapons, magic weapons vs ethereal, rusty and damaged weapons, underwater penalties, and the order of a melee attack. Use when comparing units or weapons, choosing thugs or equipment, reading a battle log's hits, judging what can hurt a monster, or when the user asks how a weapon works. Missiles: dom6-precision. Armour side: dom6-armor.
---

# Weapons (Dominions 6, vanilla)

The user's list (2026-11-03, plan `plans/dominions-mechanics-skills.md`). Manual pages in brackets; illwiki pages
named; wiki = lower truth. Mods change weapon numbers (SCBM: 180 new, 383 changed weapons - dom6-scbm).

## The melee roll (p.60)
- Attack: Attack skill + DRN - fatigue penalty. Defence: Defence + DRN - fatigue penalty (- harassment).
  Attack > defence = hit. Shield: if the attack doesn't also beat defence + **Parry**, it is a SHIELD HIT and the
  shield's protection is added to the protection roll (dom6-armor).
- Damage: Strength + weapon damage + DRN vs Protection + DRN; the difference comes off HP. A unit's Attack and
  Defence on its card already include weapon and armour modifiers.
- DRN = open-ended 2d6 (a 6 rerolls and adds, counted as 5 + reroll): dom6-drn.

## Weapon stats
Damage, Attack and Defence modifiers, **Length** (reach and repel), number of attacks, damage types, and
flags (magic, AP, AN, two-handed, on-hit effects like poison or fire).

## Damage types (p.61-62)
- **Slash**: +25% damage AFTER protection; +50% toward shield breaking; an arm/leg/head hit taking >= 50% of max
  HP chops it off (head = death if needed).
- **Pierce**: -15% of the protection before the roll; no underwater penalty.
- **Blunt**: +25% damage on head hits before protection; +25% toward shield breaking.
- A weapon with two types uses one of them per attack at random (short sword: slash or pierce).
- **Armour-piercing (AP)**: half protection; with pierce = 65% off (crossbow bolts). Fire, cold, acid are at
  least AP (wiki). **Armour-negating (AN)**: no protection; shock always AN.
- **Two-handed**: 125% of Strength to damage; -3 attack when mounted (p.64).

## Multiple weapons and attacks (p.63)
- Several WIELDED weapons: attack -(sum of their lengths); +1 encumbrance per weapon after the first.
  Ambidextrous N reduces that penalty by N. Bonus weapons (bites, hooves, natural attacks) cost nothing.
- Multiple attacks (claws, several heads) can hit different targets; a weapon with several attacks (flail)
  strikes the same target - wasted if it dies.
- Each attack (and each of a weapon's multiple attacks) gives the target 1 harassment.

## Length, reach, repel (p.61-63; wiki repel)
- Reach = size + length. Head hit needs reach >= target size; torso one less, arms two less: a size-3 human with
  a length-1 mace hits a size-7 giant only in the legs. Low-slung beasts (four-legged -1, lizards/dragons -2) are
  easier to reach. 2+ sizes larger attackers hit heads 20%, legs 10% (normal 50 torso / 20 / 20 / 10 head).
- Size 6+ wield weapons 1 longer.
- **Repel**: when attacked by a SHORTER weapon, the defender rolls attack vs the attacker's defence (repeller
  wins ties); on a hit the attacker rolls morale + DRN + (his size - repeller size) [manual: - length
  difference] vs 10 + DRN + margin/2. Lose = attack aborted and 1 damage max; win = attack goes on.
  Low-morale attackers and claws/bites (length 0) are repelled most. The repeller gets a lingering penalty
  (manual -2, wiki -1 harassment) - quick successive attacks get through. One repel roll per weapon.
  Mindless (morale 50) basically never repelled.
- Spears and pikes (length 3-4) vs short-weapon infantry and low-morale chaff = repel wall.

## Charge (wiki attack-skill/flying)
Lances (mounted units, flyers, centaurs): the FIRST hit of each battle gets extra damage = size + 1/4 combat
speed (fliers: 2 x size), capped at 1/2 strength one-handed. Fliers take no charge bonus from non-fliers.
White Centaurs (Pangaea): bronze lance, size 5, str 14 -> up to +7 on the opening hit.

## Magic weapons, ethereal and other targets
- Magic weapons (flagged on the weapon) hurt ethereal units normally; non-magic attacks on ethereal targets
  miss 75% (dom6-tactics Ghost Moose; wiki ethereal). Golden Spears (Tuatha) and Lugh's Rainbow are magic.
- Missiles from magic weapons get +2 on the hit roll (p.65).
- Damage reversal, blood bond, etc. trigger after damage (order below).

## Rust and damage (wiki rust)
Rusty weapons: 25% per landed hit to become damaged (-2 damage pierce/slash, -1 blunt), can't break; fixed after
battle with resources.

## Dancing weapons (p.64)
Items like Dancing Trident attack on their own: no multiple-weapon penalty, no fatigue, can't be repelled, can
repel for the owner (bonus per attack over 2).

## Underwater (p.62)
Slash and blunt: attack -length; pierce none; mixed pierce + other: half; flails -1 more.

## Order of a melee attack (p.63-64)
target in square -> early strikebacks (Awe, petrifying gaze) -> repel -> strikebacks (Slimer, Horror Mark
attacker...) -> attack vs defence -> damage vs protection (+shield) -> defensive abilities (Mirror Image,
Luck, Mossbody...) -> limb cap (arm/leg hit max 1/2 max HP) -> damage redistribution (Damage Reversal, Blood
Bond) -> deal damage (also to the shield).

## Using it
- Thugs: high attack + magic weapon + several attacks; harassment piles up on a single big target (a mass of
  Golden Spears grinds the moose's defence down).
- Against heavy armour: AP/AN, or Destruction/Armor of Achilles first (dom6-armor), or slashes vs light armour.
- Against cavalry/monsters: long spears repel; but trample doesn't care (dom6-tactics).

## Related skills
dom6-armor, dom6-precision (missiles), dom6-mounts, dom6-drn, dom6-morale (repel uses morale), dom6-mechanics,
dom6-items, dom6-scbm.
