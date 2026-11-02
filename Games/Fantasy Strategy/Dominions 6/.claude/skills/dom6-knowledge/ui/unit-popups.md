# Unit screen popups

What right-clicking each part of the unit stat screen shows. Read from Ulm's Black Knight and its
Black Destrier, 2026-10-26 (game screen; OCR, checked against the screenshots and the inspector).
Each popup has its own Exit, and the unit screen comes back after it. The popup is drawn *instead
of* the unit screen, not over it.

## How to click

- Right-click the **middle of the label text** (or the number). The small stat icon in front of
  the label and the label's first letters do nothing. *(game screen, 2026-10-26)*
- Gold, Resources and Recruitment points have no popup. The description has none either. *(game screen / user, 2026-10-26)*
- Weapons and armour: right-click the name. The damage-type icons and the "#" open the same
  weapon popup. *(game screen, 2026-10-26)*

## Stat popups (breakdown lines, then the game's explanation)

- **Hit Points**: Basic maximum HP, Current HP. A human has about 10, a giant about 30, a dragon over 100.
- **Strength**: Basic, Current, then a *Siege Stats* section: Siege Strength (1.7 for the knight,
  2.6 for the destrier) and Siege Defence. Strength is added to weapon damage. Siege Strength of
  all besiegers vs the defenders' Siege Defence decides wall damage.
- **Map Move**: Basic Map Move, Armor Penalty (= the armour's Map Movement Penalty), Total, and
  Mounted Map Move. The knight: 14 − 6 = 8 on foot, 16 mounted (the destrier: 20 − 4 = 16).
  Costs: Plain 6, Forest & Waste 10, Cave 12, Swamp 14, Mountain 16, Snow +2, enemy territory
  +8 (+6 stealthy), Roads −4 (min 4). Moving between provinces costs the average of the two.
  An army can always move at least one province.
- **Size**: Basic, Current, Supply Usage, then *Hit Location Details*: "Standard hit locations",
  Number of Eyes. The horse has "Lower Head: 1, Cannot be hit in arms". A combat square holds 10
  size points. Mounted units use the mount's size for space, which is why the screen shows 3(5).
- **Attack Skill**: Basic, Current, then the attack with each weapon ("Attack nr 2: 13" = 12 +
  the Morningstar's +1). Two weapons: Attack is reduced by the sum of their lengths.
- **Encumbrance**: Basic, Armors & Shields, Melee Encumbrance, Spell Casting Encumbrance
  (casting counts armour twice: 3 + 2×6 = 15). Mounts add "Burdened by Rider: +1".
- **Protection** (*Natural Protection & Armor*): natural protection, Armor Value (head/body),
  Total Protection (head/body). The destrier: natural 4 + barding 20 body / 23 head = 22 / 25
  (stacking is not simple addition: 4 + 20 gave 22).
- **Defence Skill**: Basic, Mounted (+3), Weapon Defence Modifiers, Armor+Shield modifiers,
  Shield Parry, Current Defence and Parry. The knight: 12 + 3 − 2 − 6 + 6 = 13. Defence does
  not work against missiles or spells.
- **Fatigue**: Current Fatigue. Over 100 = unconscious. Recovers 1 per combat round (5 when
  unconscious).
- **Magic Resistance**: Basic, Current. A human is 10, a strong mage 15+.
- **Precision**: Basic, Mounted (−2 for riders), Current, then *Patrol Strength* (from Map Move
  and Precision; a normal unit ≈ 1, a commander double; flyers count Map Move 30).
- **Age**: Current Age, Max Age (the knight 50, the destrier 20), and *Home*: Home Province.
  Old age lowers Att, Def, Prec, Enc, HP, Combat Speed and Map Move.
- **Morale**: Basic, modifiers (the destrier: "Skilled Rider: +2"), Current, and **Upkeep Cost**
  (knight 20 gold/year, destrier 28). Mindless 50 = never flees but dissolves without a commander.
- **Combat Speed**: Basic, Armor Encumbrance, Current. A mounted unit shows the mount's speed:
  the knight's own is 12 − 6, but it moves at 20 (the destrier's 23 − 3).
- **XP** (*Experience Points*): Current XP. Units gain about 1 per month. Levels add Prec, Att,
  Def and Morale, and for commanders also research and leadership.

## Weapon popup ("Weapon Stats")

- Title bar = weapon name. Lines: `Damage: <type icons> N` (the weapon's own damage; the unit
  screen's Dmg column adds Strength: Lance 6 + 13 = 19), notes in brackets, Attack, Defence,
  Length, then properties. *(game screen, 2026-10-26)*
- Lance: (charge bonus for first strike), (heavy weapon), Att +1, Def 0, Len 3, (this weapon
  cannot be used for repelling), "This weapon can only be used once in each battle", "Not
  dismounted". *(game screen, 2026-10-26)*
- Morningstar: (+2 Att vs shield), Att +1, Def −2, Len 1, Made of iron. Its two icons are
  bludgeoning and piercing (the inspector agrees). *(game screen + inspector, 2026-10-26)*
- Hoof (the mount's weapon): Damage 0 (+ the destrier's Strength 16), Att 0, Def 0, Len 0;
  bludgeoning (inspector: weapon 55, intrinsic). *(game screen + inspector, 2026-10-26)*
- Maul: Damage 9 (blunt), (twohanded weapon), Att 0, Def -1, Len 2. The unit table shows 22: two-handed weapons add 125% of Strength (manual), 9 + 1.25 x 11 = 22.75, rounded down. One-handed: weapon + Strength (Lance 6 + 13 = 19). *(game screen + manual, 2026-10-26)*

## Damage-type icons

- Spear tip on a brown shaft = **piercing**. Template `dmg_pierce`, picture img/dmg_pierce.png. *(game screen + inspector, 2026-10-26)*
- Spiked mace head = **bludgeoning (blunt)**. Template `dmg_blunt`, picture img/dmg_blunt.png. *(game screen + inspector, 2026-10-26)*
- Finding them: `vision.py find` with both templates and limit ≈ 0.055, keeping the best name per
  spot. On parchment both shafts look alike (false hits from 0.06), so read them inside the
  Dmg column or the popup's Damage line only. Still to learn: the slashing icon and others. *(Claude, 2026-10-26)*

## Armour popup ("Armor Stats")

- Title bar = armour name. Lines: Protection, Body / Head / Shield, Defence, Parry (shields),
  Encumbrance, Map Movement Penalty, "Made of iron", "Magic" (Ulm's blacksteel is magic armour). *(game screen, 2026-10-26)*
- Full Plate of Ulm: body 23, Def −3, Enc 4, map penalty 6. Full Helmet of Ulm: head 23, Def −1,
  Enc 0. Kite Shield of Ulm: 22, Def −2, Parry 6, Enc 2. Plate Barding of Ulm: head 23, body 20,
  Def −2, Enc 3, map penalty 4. *(game screen, 2026-10-26)*

## Ability icon popups

- Title "Name (value)" and a text. **Skilled Rider (2)**: "A skilled rider will increase the
  Morale and Defence Skill of his mount. The defence increase is most effective on lightly
  armored horses as it is reduced by the encumbrance value of the mount's armor." On the
  destrier it shows as Morale +2, and gives no defence because the barding's encumbrance 3 eats
  the 2. Template `ability_skilled_rider`. *(game screen + user, 2026-10-26)*
