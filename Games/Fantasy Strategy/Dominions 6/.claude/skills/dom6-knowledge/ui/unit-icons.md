# Unit screen icons: gear slots and abilities

Found with `scripts/probe.py --icons` (hover tooltip + right-click popup per icon). Pictures in
`img/`, templates of the same names in dom6-ui.

## Tooltips

- Hovering almost anything shows a tooltip in a small dark box with a tan frame at the bottom
  centre of the screen (about y 975-1035). Stat labels, weapon and armour names have none; icons
  do. *(user + game screen, 2026-10-26)*

## Gear slots (commanders)

- Commanders have a row of item slots under the stats: Hand, Hand, Bow (or Hand), Head, Body,
  Feet, Misc, Misc, then a wide box "Personal magic gems". Tooltip "Hand, no magic item" etc.
  Slot types vary with the body (the Priest Smith's third slot had no tooltip read). Ordinary
  units (Black Knight) have no slots. *(game screen, 2026-10-26)*
- Commanders can hold gear. Promoting a unit to commander technically gives it the same
  capability; it rarely matters, since such units usually have better commander versions or
  differ only in weapons and armour. *(user, 2026-10-26)*

## Ability icons (tooltip = popup title; right-click for the text)

- **Skilled Rider (N)**: horse and rider. Raises the mount's Morale and Defence; the defence is
  reduced by the mount's armour encumbrance. `ability_skilled_rider`. *(game screen + user)*
- **Sacred**: unlit white candelabra. "Sacred troops are extremely devoted to the god's cause.
  They can be blessed and only require half the usual cost to maintain." `ability_sacred`
- **Inquisitor**: red-crossed figure with chains. "The priest is very efficient when preaching
  against other faiths. The priest level is doubled for this purpose." `ability_inquisitor`
- **Unhindered Researcher**: dark orb crossed in red. "Will not have his magic research
  hindered by a drain scale in any way." (mod: #drainimmune). No template: it is too dark for
  the matcher; read its tooltip. picture img/ability_unhindered_researcher.png
- **Resource Bonus (N)**: hammer on an anvil. "Aids in the production of armaments for new
  warriors. Extra resources are granted to the fort this unit is located in." (Master Smith 10)
  `ability_resource_bonus`
- **Forge Bonus (N)**: a hammer. "Very efficient when forging magic items. The bonus is the
  cost reduction in gems." (Master Smith 2, Priest Smith 1) `ability_forge_bonus`

*(game screen, 2026-10-26)*

## Damage type icons (weapon table and weapon popups)

- They have tooltips explaining the type: blunt = "Blunt damage. On head hits, damage is
  increased by 25% before armor is deducted." Piercing = spear tip, blunt = mace head
  (`dmg_pierce`, `dmg_blunt`). *(game screen, 2026-10-26)*

## Leadership (commanders)

- Leadership, Magic Ldr, Undead Ldr all open the same popup: Normal Units, Undead/Demons, Magic
  Beings, "Squad morale bonus: +0 for up to 2 squads". Undead and magic beings are led in
  addition to normal units; only undead commanders and Death/Blood mages lead undead, only
  mages and some monsters lead magic beings. *(game screen, 2026-10-26)*

## Abilities seen on Pythium's units

- Grand Communicant: "able to lead or join a Grand Communion. If joining, his magic skill in the path of the ritual cast by another Grand Communicant will be added to the power of the ritual. Only global spells or dispels are affected." (Theurg Acolyte, Theurg, Arch Theurg; the inspector does not show it). Fortune Teller (N): can prevent bad events (inspector nobadevents N%). Communion Slave: lets the communion masters use its life force; takes much of their fatigue. Old Age, A (B): current age and start of old age; popup lists the penalties. Stealthy (N): patrollers needed for a 50% chance to find it. Assassin (N): patience bonus. Ambidextrous (N): lower penalty for several weapons. Mountain / Swamp Survival, Swimming (cross rivers; small underwater penalty). Tight Rein: undisciplined units under him can take normal battle orders. Beastmaster (+N): animals get more morale. *(game screen, 2026-10-27, 2026-10-27)*
