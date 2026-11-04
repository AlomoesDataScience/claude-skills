# Glamour magic (Dominions 6, scbm)

The user (2026-11-03): "a skill for each elemental path in vanilla would probably good". Written by `dom6-spell-db/scripts/pathskills.py` from the scbm spell database and illwiki `glamour` - re-run it, don't hand-edit the generated parts. Mods: dom6-mod-magic and the mod's folder (dom6-scbm).

## What the path does (illwiki)
Glamour has one of the smaller spell lists in the game, dwarfing only Blood and Holy. If one counts cross-path spells, however, it also has more spells than Air. These spells are somewhat evenly split between the schools, too, though with a focus on Thaumaturgy.

## Indirect magic (what the level itself gives)
A Glamour Mage with G3 or higher has Regeneration of sorts for False Damage, letting them burn off 1 point each combat round. This is presumably due to their higher understanding of the unreal. A Glamour Mage with G4 or higher has True Sight. Illusions only matter while a Glamour Mage is on their team, making their actions seem real. Illusions are not Magic Beings; they require Glamour levels, not just any (non-Death) magic level or Magic Leadership. Without Glamour levels on their side, they dissolve a few rounds after appearing.  * False Damage behaves similarly without Glamour Mages to reinforce it, decaying at a rate of 2 points each combat round. This stacks with the effects of having G3 or higher, of course.  Last but not least, each level of Glamour skill gives its possessor 10 points of Magic Leadership. Examples of Magical Glamour beings include the Phantasms, Dreamwild entities who struggle to remain in the waking world without such magical help.

## Path boosting
There are nine Glamour-boosting items. Four are artifacts; that means they require Construction Level 9, and that only one of each may exist at a time. Four don't need Glamour as a path. Let's cover the items that require Glamour:  * The Gossamer Veil is the most straightforward one: it requires G3 and Construction Level 5. Aside from the +G1, it also makes you Stealthy and Blurry.  * The Mirage Crystal requires G3E2 and Construction Level 7. Aside from the +G1, it provides 50 points of Obfuscation.  * The Tome of Legends is an Artifact that requires G5. It provides +G2, and it allows Illusions to stick around without a Glamour Mage present; why you'd put it on a regular commander is up for debate, however. Last-but-not-least, it provides a retinue of one giant Phantasmal Beast.  * The Trapped Dreams of Hruvur is another Artifact, that requires G4S4. It provides +S1G1B1, +2 Penetration, +2 Strength, and +15 max HP. It's not all good, however; it's Cursed, it's one of the most Tainted items in the game, and it lowers Morale by 2.  * The Sword of Many Colors is a third Artifact, that requires G4F2. It provides each battle (though these don't persist past the battle) and 3 points of Awe, along with that +G1, and it's a very good weapon as well; simply swinging it deals 10 False Damage to almost every enemy nearby. Last-but-not-least, it also lets Illusions persist without proper Glamour mages, though (again) putting this on a regular guy is questionable. Glamour has a Battle Enchantment (a bit like Astral) that boosts itself, known as Twilight. It also has a ritual that boosts all paths for a single turn, Lore of Legends. The former requires G3 (and some other things), while the latter requires G4.

## Crosspaths with Glamour first (illwiki)
- Glamour/Fire: Fake Fireballs and imparting Awe upon friends.
- Glamour/Air: Sleep Clouds, Illusion-spawning mists, and Wailing Winds.
- Glamour/Water: Water Kobolds, Siren activity, and great big rainbows.
- Glamour/Earth: Cave Kobolds and Gnomes.
- Glamour/Astral: Curses, Mental Armor, Ventriloquism, and Aurora Borealis.
- Glamour/Death: Dread and Nightmares.
- Glamour/Nature: A very wide array of faery magic and summons.

## Best generic spells per purpose (database tiers S/A, top 5)
Tiers are percentiles inside a purpose across all paths; "hand" = my curated tier (dom6-spells). Trust notes: dom6-spell-db.
- **army damage**: Shimmering Fields (G5, Evocation 7, A, hand S)
- **group buff**: Group Luck (G2, Thaumaturgy 5, A, hand B); Group Blur (G2, Alteration 3, A, hand B)
- **self buff**: Personal Luck (G1, Thaumaturgy 1, A, hand B); Blurred Body (G1, Alteration 1, A); Displace Body (G2, Alteration 3, A, hand B); Shroud of Splendor (G1F1, Enchantment 2, A)
- **debuff**: Sandman's Blessing (G5, Thaumaturgy 6, S, hand A); Unending Nightmare (G3D1, Thaumaturgy 6, S); Slumber (G2, Thaumaturgy 4, A, hand A); Mass Confusion (G3, Thaumaturgy 7, A, hand A); Bewitching Lights (G1, Evocation 1, A, hand A)
- **battlefield enchantment**: Aurora Borealis (G5S1, Evocation 8, A); Twilight (G3, Alteration 4, A, hand A)
- **battle summon**: Conjure Phantasmal Beast (G3, Conjuration 5, S, hand S); Conjure Phantasmal Knight (G2, Conjuration 7, S); Illusory Army (G3, Evocation 5, A); Conjure Phantasmal Warriors (G2, Conjuration 4, A); False Horror (G3, Evocation 6, A)
- **summon units**: Illusory Attack (G4, Evocation 7, A); Summon Fay Footfolk (G2N1, Conjuration 4, A); Summon Unseelie Soldiers (G2W1, Conjuration 4, A); Summon Fay Knights (G3N1, Conjuration 5, A); Summon Unseelie Knights (G3W1, Conjuration 5, A)
- **summon commander**: Faerie Court (G4N1, Conjuration 8, S); Summon Unseelie Prince (G4W1, Conjuration 6, A); Awaken Sleeper (G3, Conjuration 5, A); Summon Fay Prince (G4N1, Conjuration 6, A)
- **remote attack**: Vengeance of the Dead (G3D1, Thaumaturgy 4, A)
- **global enchantment**: Wild Hunt (G5N3, Conjuration 7, S); Gates of Horn and Ivory (G5, Thaumaturgy 7, A)
- **province enchantment**: Tapestry of Dreams (G2, Conjuration 2, A)
- **utility**: Project Self (G3S1, Evocation 5, S)

Full list: `spells.md` (105 spells; purposes: army damage, single-target damage, army buff, group buff, self buff, debuff, battlefield enchantment, battle summon, summon units, summon commander, remote attack, global enchantment, province enchantment, site search, movement, caster upgrade, utility, combat other, fear / morale attack).

## Related skills
dom6-spell-db, dom6-spells (calculator), dom6-research, dom6-gem-casting, dom6-forging, dom6-summoning, dom6-rituals, dom6-evocations, dom6-buffs, dom6-mod-magic, dom6-mechanics.
