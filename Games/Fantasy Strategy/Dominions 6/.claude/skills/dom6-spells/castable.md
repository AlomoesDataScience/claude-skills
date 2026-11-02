# Combat spells Pythium can cast

Made by `spells.py castable` from the inspector data (2026-10-28). One row per spell that at least
one of Pythium's own casters can cast; **First caster** is the cheapest one that reaches it.
Communion: the master gets +1 in every path for 2 slaves, +2 for 4, +3 for 8 (Communicants and
Theurgs as slaves). Holy spells need only the priest level; Smite and Banish come in the
god's Earth version. UNDERWATER spells are listed but useless on land.
Research at turn 6: Conjuration 0, Alteration 1, Evocation 1, Construction 0, Enchantment 1, Thaumaturgy 1, Blood 0 (✓ = castable now if a caster has the paths).

Casters: Theurg Acolyte S1H1; Theurg A1W1S2H2; Arch Theurg (+1 random F/A/W/S not counted) A2W1S3H3; Bartholomeus (hero) A2W2S3H4; Theurg + 4 slaves (master +2) A3W3S4H2; Bartholomeus + 5 Communicants (+2) A4W4S5H4; Bartholomeus + 8 slaves (+3) A5W5S6H4; Arch Theurg + 8 slaves (+3) A5W4S6H3; God: Titan of Growth (dormant until ~T10-13) E5N5H3


## Buff (137)

| Now | Spell | School | Path | First caster | Range | Area | Fatigue / gems | Flags | Effect |
|---|---|---|---|---|---|---|---|---|---|
|  | Summon Storm Power | Conju 2 | A1 | Theurg | - | Caster | 10 | noShield | Storm Power / Grants Air magic bonus +1. |
|  | Summon Water Power | Conju 2 | W1 | Theurg | - | Caster | 20 | noShield,UNDERWATER | Water Power / Grants Water magic bonus +1. |
|  | Power of the Spheres | Conju 3 | S1 | Theurg Acolyte | - | Caster | 100 1S | noShield | Magic Power / Magic bonus: +1 for all paths except blood and holy |
|  | Summon Earthpower | Conju 3 | E2 | God: Titan of Growth (dormant until ~T10-13) | - | Caster | 20 | noShield | Earth Power / Grants Earth magic bonus +1 and Reinvigoration +4. |
|  | Strength of Gaia | Conju 4 | N3E1 | God: Titan of Growth (dormant until ~T10-13) | - | Caster | 20 | noShield | Nature Power / "Strength, Barkskin and Regeneration" / Barkskin, Limited Regeneration, Ext |
| ✓ | Air Shield | Alter 0 | A1 | Theurg | - | Caster | 10 | noShield | Air Shield / Air Shield: 80 |
| ✓ | Twist Fate | Alter 0 | S1 | Theurg Acolyte | - | Caster | 10 | noShield | Twist Fate |
| ✓ | Cat Eyes | Alter 1 | N1 | God: Titan of Growth (dormant until ~T10-13) | - | Caster | 5 | noShield | / Darkvision 50% |
| ✓ | Charge Body | Alter 1 | A1 | Theurg | - | Caster | 5 | noShield | Charged Body 20AN / Damage on attacker: 20 AN shock Damage on mage: 5 AN shock |
| ✓ | Eagle Eyes | Alter 1 | N1 | God: Titan of Growth (dormant until ~T10-13) | - | Caster | 5 | noShield | Improved Precision / Prec +4 |
| ✓ | Personal Barkskin | Alter 1 | N1 | God: Titan of Growth (dormant until ~T10-13) | - | Caster | 5 | noShield | Barkskin / Grants natural protection +7 (max up to 10), or +1 if already 9 or higher. Also |
| ✓ | Personal Poison Resistance | Alter 1 | N1 | God: Titan of Growth (dormant until ~T10-13) | - | Caster | 5 | noShield | Bless/Buff: |
|  | Enlarge | Alter 2 | N2 | God: Titan of Growth (dormant until ~T10-13) | 10 | 1 | 20 | noShield,friends | Enlargement / Size +1, HP +30%, Str +3, Def -1. |
|  | Gift of Cheated Fate | Alter 2 | S1 | Theurg Acolyte | 10 | 1 | 20 | noShield | Twist Fate |
|  | Ice Shield | Alter 2 | W1 | Theurg | - | Caster | 20 | noShield,UNDERWATER | Protective Force 20 |
|  | Personal Mistform | Alter 2 | A2 | Arch Theurg (+1 random F/A/W/S not counted) | - | Caster | 10 | noShield | Mistform / Any damage is reduced to 1 (max 25 points of reduction). A hit that would have  |
|  | Personal Stoneskin | Alter 2 | E1 | God: Titan of Growth (dormant until ~T10-13) | - | Caster | 10 | noShield | Stoneskin / Grants natural protection +10 (max up to 15), or +3 if already 12 or higher. A |
|  | Quicken Self | Alter 2 | W1 | Theurg | - | Caster | 20 | noShield | Quickness |
|  | Resist Fire | Alter 2 | W1 | Theurg | - | Caster | 10 | noShield | Fire Resistance +5 |
|  | Resist Lightning | Alter 2 | E1 | God: Titan of Growth (dormant until ~T10-13) | - | Caster | 10 | noShield | Shock Resistance +5 |
|  | Barkskin | Alter 3 | N1 | God: Titan of Growth (dormant until ~T10-13) | 10 | 1 | 20 |  | Barkskin / Grants natural protection +7 (max up to 10), or +1 if already 9 or higher. Also |
|  | Body Ethereal | Alter 3 | S1 | Theurg Acolyte | 10 | 1 | 30 | noShield | Etherealness |
|  | Fire Resistance | Alter 3 | W2 | Bartholomeus (hero) | 15 | 1 | 20 | friends | Fire Resistance +5 |
|  | Gift of Cat Eyes | Alter 3 | N1 | God: Titan of Growth (dormant until ~T10-13) | 15 | 2+ [1/lvl] | 20 | friends | / Darkvision 50% |
|  | Lightning Resistance | Alter 3 | E2 | God: Titan of Growth (dormant until ~T10-13) | 15 | 1 | 20 | friends | Shock Resistance +5 |
|  | Personal Ironskin | Alter 3 | E1 | God: Titan of Growth (dormant until ~T10-13) | - | Caster | 20 | noShield | Ironskin / Grants natural protection +13 (max up to 20), or +5 if 15 or higher. Also incur |
|  | Protective Winds | Alter 3 | A2 | Arch Theurg (+1 random F/A/W/S not counted) | 15 | 3+ [1/lvl] | 40 | friends | Air Shield / Air Shield: 80 |
|  | Elemental Fortitude | Alter 4 | N1 | God: Titan of Growth (dormant until ~T10-13) | - | Caster | 10 | noShield | Fire Resistance +5, Shock Resistance +5, Cold Resistance +5 |
|  | Group Barkskin | Alter 4 | N2 | God: Titan of Growth (dormant until ~T10-13) | 15 | 3+ [1/lvl] | 40 |  | Barkskin / Grants natural protection +7 (max up to 10), or +1 if already 9 or higher. Also |
|  | Liquid Body | Alter 4 | W1 | Theurg | - | Caster | 20 | noShield | Slashing Resistance, Bludgeoning Resistance, Piercing Resistance, Liquid Body / Grants Sla |
|  | Mistform | Alter 4 | A2 | Arch Theurg (+1 random F/A/W/S not counted) | 10 | 1 | 20 | friends | Mistform / Any damage is reduced to 1 (max 25 points of reduction). A hit that would have  |
|  | Quickness | Alter 4 | W2 | Bartholomeus (hero) | 15 | 1 | 20 | noShield | Quickness |
|  | Stoneskin | Alter 4 | E2 | God: Titan of Growth (dormant until ~T10-13) | 15 | 1 | 20 | noShield | Stoneskin / Grants natural protection +10 (max up to 15), or +3 if already 12 or higher. A |
|  | Temper Flesh | Alter 4 | E1 | God: Titan of Growth (dormant until ~T10-13) | - | Caster | 20 | noShield | Fire Resistance +5, Slashing Resistance, Bludgeoning Resistance, Piercing Resistance / Gra |
|  | Arrow Ward | Alter 5 | A3 | Theurg + 4 slaves (master +2) | 15 | 20+ [1/lvl] | 100 1A | friends | Air Shield / Air Shield: 80 |
|  | Cat-eyed Warriors | Alter 5 | N3 | God: Titan of Growth (dormant until ~T10-13) | 15 | 20+ [1/lvl] | 100 1N | friends | / Darkvision 50% |
|  | Fire Resistant Warriors | Alter 5 | W3 | Theurg + 4 slaves (master +2) | 15 | 20+ [1/lvl] | 100 1W | friends | Fire Resistance +5 |
|  | Gift of Formlessness | Alter 5 | W2 | Bartholomeus (hero) | 10 | 1 | 40 | noShield | Slashing Resistance, Bludgeoning Resistance, Piercing Resistance, Liquid Body / Grants Sla |
|  | Group Stoneskin | Alter 5 | E3 | God: Titan of Growth (dormant until ~T10-13) | 15 | 3+ [1/lvl] | 40 | noShield | Stoneskin / Grants natural protection +10 (max up to 15), or +3 if already 12 or higher. A |
|  | Ironskin | Alter 5 | E2 | God: Titan of Growth (dormant until ~T10-13) | 10 | 1 | 40 | noShield | Ironskin / Grants natural protection +13 (max up to 20), or +5 if 15 or higher. Also incur |
|  | Lightning Resistant Warriors | Alter 5 | E3 | God: Titan of Growth (dormant until ~T10-13) | 15 | 20+ [1/lvl] | 100 1E | friends | Shock Resistance +5 |
|  | Eagle-eyed Warriors | Alter 6 | N3 | God: Titan of Growth (dormant until ~T10-13) | 15 | 20+ [1/lvl] | 100 1N | friends | Improved Precision / Prec +4 |
|  | Giant Warriors | Alter 6 | N3 | God: Titan of Growth (dormant until ~T10-13) | 10 | 10 | 100 1N | noShield,friends | Enlargement / Size +1, HP +30%, Str +3, Def -1. |
|  | Group Ironskin | Alter 6 | E3 | God: Titan of Growth (dormant until ~T10-13) | 15 | 3+ [1/lvl] | 60 | noShield | Ironskin / Grants natural protection +13 (max up to 20), or +5 if 15 or higher. Also incur |
|  | Rewrite Fate | Alter 6 | S4 | Theurg + 4 slaves (master +2) | 15 | 20+ [1/lvl] | 100 1S | noShield,friends | Twist Fate |
|  | Wooden Warriors | Alter 6 | N3 | God: Titan of Growth (dormant until ~T10-13) | 15 | 20+ [1/lvl] | 100 1N | friends | Barkskin / Grants natural protection +7 (max up to 10), or +1 if already 9 or higher. Also |
|  | Arrow Fend | Alter 7 | A4 | Bartholomeus + 5 Communicants (+2) | - | 100% of battlefield | 100 1A | friends | Air Shield / Air Shield: 80 |
|  | Fog Warriors | Alter 7 | A4 | Bartholomeus + 5 Communicants (+2) | 15 | 20+ [1/lvl] | 100 1A | friends | Mistform / Any damage is reduced to 1 (max 25 points of reduction). A hit that would have  |
|  | Marble Warriors | Alter 7 | E3 | God: Titan of Growth (dormant until ~T10-13) | 15 | 20+ [1/lvl] | 100 1E | friends | Stoneskin / Grants natural protection +10 (max up to 15), or +3 if already 12 or higher. A |
|  | Oaken Army | Alter 7 | N4 | God: Titan of Growth (dormant until ~T10-13) | - | 100% of battlefield | 300 3N | friends | Barkskin / Grants natural protection +7 (max up to 10), or +1 if already 9 or higher. Also |
|  | Wave Warriors | Alter 7 | W3 | Theurg + 4 slaves (master +2) | 15 | 20+ [1/lvl] | 100 1W | noShield | Slashing Resistance, Bludgeoning Resistance, Piercing Resistance, Liquid Body / Grants Sla |
|  | Will of the Fates | Alter 7 | S5 | Bartholomeus + 5 Communicants (+2) | - | 100% of battlefield | 200 2S | friends | Twist Fate |
|  | Army of Giants | Alter 8 | N5 | God: Titan of Growth (dormant until ~T10-13) | - | 100% of battlefield | 300 3N | noShield,friends | Enlargement / Size +1, HP +30%, Str +3, Def -1. |
|  | Army of Mist | Alter 8 | A5 | Bartholomeus + 8 slaves (+3) | - | 100% of battlefield | 300 3A | friends | Mistform / Any damage is reduced to 1 (max 25 points of reduction). A hit that would have  |
|  | Frostflesh Army | Alter 8 | W4 | Bartholomeus + 5 Communicants (+2) | - | 100% of battlefield | 200 2W | friends | Fire Resistance +5 |
|  | Ground Army | Alter 8 | E4 | God: Titan of Growth (dormant until ~T10-13) | - | 100% of battlefield | 200 2E | friends | Shock Resistance +5 |
|  | Iron Warriors | Alter 8 | E4 | God: Titan of Growth (dormant until ~T10-13) | 15 | 20+ [1/lvl] | 200 2E | noShield | Ironskin / Grants natural protection +13 (max up to 20), or +5 if 15 or higher. Also incur |
|  | Marble Army | Alter 8 | E4 | God: Titan of Growth (dormant until ~T10-13) | - | 100% of battlefield | 300 3E | friends | Stoneskin / Grants natural protection +10 (max up to 15), or +3 if already 12 or higher. A |
|  | Quickening | Alter 8 | W2 | Bartholomeus (hero) | 20 | 9+ [1/lvl] | 100 1W | noShield | Quickness |
|  | Temper Armors | Const 2 | E2 | God: Titan of Growth (dormant until ~T10-13) | 15 | 5+ [1/lvl] | 30 | friends | Toughened Armor / Grants +3 prot to all armor parts. |
|  | Soldiers of Steel | Const 4 | E3 | God: Titan of Growth (dormant until ~T10-13) | 15 | 20+ [1/lvl] | 60 | friends | Toughened Armor / Grants +3 prot to all armor parts. |
|  | Legions of Steel | Const 6 | E4 | God: Titan of Growth (dormant until ~T10-13) | - | 100% of battlefield | 100 1E | friends | Toughened Armor / Grants +3 prot to all worn armor parts. |
| ✓ | Healing Touch | Encha 1 | N1 | God: Titan of Growth (dormant until ~T10-13) | 1 | 1 | 20 | AN | Heal: 30+ [10/lvl] |
| ✓ | Levitate | Encha 1 | A1 | Theurg | - | Caster | 20 | noShield | / Floating units cannot be targeted by some spells like earth grip or earthquakes. |
| ✓ | Protection from Cold | Encha 1 | W1 | Theurg | - | Caster | 5 | noShield | Bless/Buff: |
| ✓ | Protection from Lightning | Encha 1 | A1 | Theurg | - | Caster | 5 | noShield | Bless/Buff: |
| ✓ | Protection from Poison | Encha 1 | N1 | God: Titan of Growth (dormant until ~T10-13) | - | Caster | 5 | noShield | Bless/Buff: |
| ✓ | Resist Magic | Encha 1 | S1 | Theurg Acolyte | - | Caster | 20 | noShield | Magic Resistance / Grants +4 MR |
| ✓ | Strength of Giants | Encha 1 | E2 | God: Titan of Growth (dormant until ~T10-13) | 5 | 1 | 20 |  | Extra Strength / Grants Str +4 |
| ✓ | Trueshot | Encha 1 | A1 | Theurg | 10 | 1 | 5 | noShield | Improved Precision / Grants prec +4 |
| ✓ | Windrunner | Encha 1 | A1 | Theurg | - | Caster | 10 | AN,friends | Swiftness / Combat speed +50% |
|  | Breath of Winter | Encha 2 | W1 | Theurg | - | Caster | 20 | noShield | Cold Aura |
|  | Envenom Arrows | Encha 2 | N1 | God: Titan of Growth (dormant until ~T10-13) | 10 | 1 | 20 | friends | / Extra +5 AN poison dmg if wounded. |
|  | Gift of the Hare | Encha 2 | N1 | God: Titan of Growth (dormant until ~T10-13) | 15 | 1+ [1/lvl] | 20 | AN,friends | Swiftness / Combat speed +50% |
|  | Gift of the Serpent | Encha 2 | N1 | God: Titan of Growth (dormant until ~T10-13) | 15 | 1 | 20 | noShield | Bless/Buff: |
|  | Personal Flight | Encha 2 | A1 | Theurg | - | Caster | 20 | noShield | Flight |
|  | Personal Regeneration | Encha 2 | N2 | God: Titan of Growth (dormant until ~T10-13) | - | Caster | 20 | noShield | Limited Regeneration |
|  | Proud Steed | Encha 2 | N1 | God: Titan of Growth (dormant until ~T10-13) | 10 | 1 | 20 | friends,mind | Communion Master / (No Effect on Mindless [mind], Affects Friendlies Only [enemyimmune], M |
|  | Water Shield | Encha 2 | W1 | Theurg | - | Caster | 20 | noShield,UNDERWATER | +5 Defence if underwater / Grants +5 Def underwater |
|  | Astral Shield | Encha 3 | S1 | Theurg Acolyte | - | Caster | 20 | noShield | Astral Shield / Paralysis strength: 12 + astral mage level (reduced by weapon length, magi |
|  | Farflight | Encha 3 | A1 | Theurg | 10 | 1 | 20 | friends | / Missile Range: +50% |
|  | Gift of Flight | Encha 3 | A2 | Arch Theurg (+1 random F/A/W/S not counted) | 10 | 1 | 20 | noShield | Flight |
|  | Gift of Giant Strength | Encha 3 | E2 | God: Titan of Growth (dormant until ~T10-13) | 15 | 3+ [1/lvl] | 40 | friends | Extra Strength / Grants Str +4 |
|  | Heal | Encha 3 | N1 | God: Titan of Growth (dormant until ~T10-13) | 15 | 1 | 20 | AN | Heal: 30+ [10/lvl] |
|  | Lesser Thunder Ward | Encha 3 | A2 | Arch Theurg (+1 random F/A/W/S not counted) | 15 | 1 | 20 | friends | Shock Resistance +5 |
|  | Lesser Winter Ward | Encha 3 | W2 | Bartholomeus (hero) | 15 | 1 | 20 | friends | Cold Resistance +5 |
|  | Regeneration | Encha 3 | N3 | God: Titan of Growth (dormant until ~T10-13) | 15 | 1 | 40 | noShield,friends | Limited Regeneration |
|  | Astral Healing | Encha 4 | S3 | Arch Theurg (+1 random F/A/W/S not counted) | - | 100% of battlefield | 100 1S | AN,friends,mind | Heal: 2 |
|  | Earth Shatter Hammers | Encha 4 | E2 | God: Titan of Growth (dormant until ~T10-13) | 15 | 1 | 40 | friends | / Blunt and slash melee attacks will stun on hit (size or str can negate). |
|  | Haste | Encha 4 | N3 | God: Titan of Growth (dormant until ~T10-13) | 15 | 20+ [1/lvl] | 100 1N | AN,friends | Swiftness / Combat speed +50% |
|  | Immaculate Mounts | Encha 4 | N2 | God: Titan of Growth (dormant until ~T10-13) | 10 | 3+ [1/lvl] | 20 | friends,mind | Communion Master / (No Effect on Mindless [mind], Affects Friendlies Only [enemyimmune], M |
|  | Levitate Soldiers | Encha 4 | A2 | Arch Theurg (+1 random F/A/W/S not counted) | 15 | 3+ [1/lvl] | 40 | AN,friends | / Floating units cannot be targeted by some spells like earth grip or earthquakes. |
|  | Poison Ward | Encha 4 | N2 | God: Titan of Growth (dormant until ~T10-13) | 15 | 20+ [1/lvl] | 100 1N | noShield,friends | Bless/Buff: |
|  | Serpent Fang Arrows | Encha 4 | N3 | God: Titan of Growth (dormant until ~T10-13) | 15 | 20+ [1/lvl] | 100 1N | friends | / Extra +5 AN poison dmg if wounded. |
|  | Spell Ward | Encha 4 | S2 | Theurg | 15 | 20+ [1/lvl] | 100 1S | friends | Magic Resistance / Grants +4 MR |
|  | Trueshot Warriors | Encha 4 | A2 | Arch Theurg (+1 random F/A/W/S not counted) | 15 | 20+ [1/lvl] | 100 1A | friends | Improved Precision / Grants prec +4 |
|  | Farflight Arrows | Encha 5 | A2 | Arch Theurg (+1 random F/A/W/S not counted) | 15 | 20+ [1/lvl] | 100 1A | friends | / Missile Range: +50% |
|  | Giant Strength Warriors | Encha 5 | E3 | God: Titan of Growth (dormant until ~T10-13) | 15 | 20+ [1/lvl] | 100 1E | friends | Extra Strength / Grants Str +4 |
|  | Group Regeneration | Encha 5 | N3 | God: Titan of Growth (dormant until ~T10-13) | 15 | 3+ [1/lvl] | 60 | noShield,friends | Limited Regeneration |
|  | Thunder Ward | Encha 5 | A2 | Arch Theurg (+1 random F/A/W/S not counted) | 15 | 20+ [1/lvl] | 100 1A | noShield,friends | Shock Resistance +5 |
|  | Weapons of Sharpness | Encha 5 | E3 | God: Titan of Growth (dormant until ~T10-13) | 15 | 1 | 40 | friends | Armor Piercing Weapons / Targets' slash or piercing melee attacks deal AP damage. |
|  | Winter Ward | Encha 5 | W2 | Bartholomeus (hero) | 15 | 20+ [1/lvl] | 100 1W | friends | Cold Resistance +5 |
|  | Earthquake Warriors | Encha 6 | E4 | God: Titan of Growth (dormant until ~T10-13) | 15 | 20+ [1/lvl] | 100 1E | friends | / Blunt and slash melee attacks will stun on hit (size or str can negate). |
|  | Greater Farflight | Encha 6 | A4 | Bartholomeus + 5 Communicants (+2) | - | 100% of battlefield | 100 1A | friends | / Missile Range: +50% |
|  | Hail of Serpent Fangs | Encha 6 | N4 | God: Titan of Growth (dormant until ~T10-13) | - | 100% of battlefield | 200 2N | friends | / Extra +5 AN poison dmg if wounded. |
|  | Water Ward | Encha 6 | W1 | Theurg | 15 | 25 | 100 1W | noShield,friends,UNDERWATER | +5 Defence if underwater |
|  | Wind Guide | Encha 6 | A3 | Theurg + 4 slaves (master +2) | - | 100% of battlefield | 100 1A | friends | / Grants Prec +2 Halves precision penalty and negates the 50% firing chance from Storm. |
|  | Antimagic | Encha 7 | S3 | Arch Theurg (+1 random F/A/W/S not counted) | - | 100% of battlefield | 200 2S | friends | Magic Resistance / Grants +4 MR |
|  | Army of Immaculate Mounts | Encha 7 | N4 | God: Titan of Growth (dormant until ~T10-13) | - | 100% of battlefield | 200 2N | friends,mind | Communion Master / (No Effect on Mindless [mind], Affects Friendlies Only [enemyimmune], M |
|  | Featherweight Army | Encha 7 | A4 | Bartholomeus + 5 Communicants (+2) | - | 100% of battlefield | 200 2A | AN,friends | / Floating units cannot be targeted by some spells like earth grip or earthquakes. |
|  | Mass Flight | Encha 7 | A4 | Bartholomeus + 5 Communicants (+2) | 15 | 20+ [1/lvl] | 100 1A | friends | Flight |
|  | Mass Regeneration | Encha 7 | N4 | God: Titan of Growth (dormant until ~T10-13) | 15 | 20+ [1/lvl] | 100 1N | noShield | Limited Regeneration |
|  | Serpent's Blessing | Encha 7 | N4 | God: Titan of Growth (dormant until ~T10-13) | - | 100% of battlefield | 200 2N | friends | Poison Resistance +10 |
|  | Steel Slice Warriors | Encha 7 | E4 | God: Titan of Growth (dormant until ~T10-13) | 15 | 20+ [1/lvl] | 100 1E | friends | Armor Piercing Weapons / Targets' slash or piercing melee attacks deal AP damage. |
|  | Army Regeneration | Encha 8 | N5 | God: Titan of Growth (dormant until ~T10-13) | - | 100% of battlefield | 300 3N | friends | Limited Regeneration |
|  | Frost Fend | Encha 8 | W4 | Bartholomeus + 5 Communicants (+2) | - | 100% of battlefield | 100 1W | friends | Cold Resistance +5 |
|  | Soaring Army | Encha 8 | A5 | Bartholomeus + 8 slaves (+3) | - | 100% of battlefield | 300 3A | friends | Flight |
|  | Thunder Fend | Encha 8 | A4 | Bartholomeus + 5 Communicants (+2) | - | 100% of battlefield | 100 1A | friends | Shock Resistance +5 |
|  | Earth Shatter Army | Encha 9 | E5 | God: Titan of Growth (dormant until ~T10-13) | - | 100% of battlefield | 200 2E | friends | / Blunt and slash melee attacks will stun on hit (size or str can negate). |
|  | Gaia's Blessing | Encha 9 | N5E2 | God: Titan of Growth (dormant until ~T10-13) | - | 100% of battlefield | 300 3N | noShield,friends | Fire Resistance +5, Shock Resistance +5, Cold Resistance +5, Poison Resistance +10 |
| ✓ | Blink | Thaum 1 | S1 | Theurg Acolyte | - | Caster | 10 | noShield | Blink: 30 |
| ✓ | Communion Master | Thaum 1 | S1 | Theurg Acolyte | - | Caster | 20 | noShield | / AInocast: 1 / 2 slaves: +1 magic level, 4 slaves: +2 magic levels, 8 slaves: +3 magic le |
| ✓ | Communion Slave | Thaum 1 | S1 | Theurg Acolyte | - | Caster | 20 | noShield | / AInocast: 1 |
|  | Beast Fury | Thaum 2 | N1 | God: Titan of Growth (dormant until ~T10-13) | 10 | 1 | 20 | friends,mind | / Attack skill +2, morale +2. The spell only affects animals. |
|  | Returning | Thaum 2 | S2 | Theurg | - | Caster | 200 2S | AN,noShield,friends | Return Home: teleports to capital |
|  | Iron Will | Thaum 3 | E1 | God: Titan of Growth (dormant until ~T10-13) | 25 | 1 | 20 | noShield,mind | Magic Resistance |
|  | Ferocity | Thaum 4 | N2 | God: Titan of Growth (dormant until ~T10-13) | 15 | 3+ [1/lvl] | 20 | friends,mind | / Attack skill +2, morale +2. The spell only affects animals. |
|  | Rage of the Cornered Rat | Thaum 4 | N2 | God: Titan of Growth (dormant until ~T10-13) | 20 | 3+ [1/lvl] | 20 | AN,friends | Gone Berserk |
|  | Touch of Madness | Thaum 4 | N1 | God: Titan of Growth (dormant until ~T10-13) | 20 | 1 | 30 | AN,friends,mind | Gone Berserk |
|  | Pack Ferocity | Thaum 5 | N2 | God: Titan of Growth (dormant until ~T10-13) | 15 | 20+ [1/lvl] | 100 1N | friends,mind | / Attack skill +2, morale +2. The spell only affects animals. |
|  | Fury of the Wild | Thaum 7 | N4 | God: Titan of Growth (dormant until ~T10-13) | - | 100% of battlefield | 200 2N | friends,mind | / Attack skill +2, morale +2. The spell only affects animals. |
|  | Vortex of Returning | Thaum 7 | S4 | Theurg + 4 slaves (master +2) | - | 100% of battlefield | 300 3S | AN,friends | Return Home: teleports to capital / AInocast: 1 |
| ✓ | Blessing | Divin  | H1 | Theurg Acolyte | 15+ [10/lvl] | 5+ [5/lvl] |  | noShield,friends,sacreds | Blessing / AI will not cast unless path level lower than : 3 |
| ✓ | Divine Blessing | Divin  | H3 | Arch Theurg (+1 random F/A/W/S not counted) | - | 100% of battlefield |  | friends,sacreds | Blessing / Unknown Attribute (1716): -1 |
| ✓ | Fanaticism | Divin  | H4 | Bartholomeus (hero) | - | 100% of battlefield |  | AN,friends | Temporary Morale Boost: 1 / Unknown Attribute (1716): -1 |
| ✓ | Holy Avenger | Divin  | H2 | Theurg | - | Caster |  | noShield | Holy Vengeance |
| ✓ | Sermon of Courage | Divin  | H2 | Theurg | 25+ [5/lvl] | 10+ [5/lvl] |  | AN,friends | Temporary Morale Boost: 1 / AI will not cast unless path level lower than : 4 |

## Debuff (43)

| Now | Spell | School | Path | First caster | Range | Area | Fatigue / gems | Flags | Effect |
|---|---|---|---|---|---|---|---|---|---|
|  | Tangle Vines | Conju 1 | N1 | God: Titan of Growth (dormant until ~T10-13) | 20 | 1 | 20 | noShield | Cause Affliction: Entangle / Str +DRN vs 19 to get free. The difficulty is increased or de |
|  | Tangle Thicket | Conju 4 | N2 | God: Titan of Growth (dormant until ~T10-13) | 20 | 3+ [1/lvl] | 30 | noShield | Cause Affliction: Entangle / Str +DRN vs 19 to get free. The difficulty is increased or de |
|  | Wild Growth | Conju 8 | N4 | God: Titan of Growth (dormant until ~T10-13) | 20 | 10+ [2/lvl] | 40 | enemies | Cause Affliction: Entangle / Str +DRN vs 19 to get free. The difficulty is increased or de |
| ✓ | Earth Grip | Alter 1 | E1 | God: Titan of Growth (dormant until ~T10-13) | 20 | One person | 10 | noShield | Cause Affliction: Earth Grip / Str +DRN vs 23 to get free. |
|  | Gooey Water | Alter 2 | W2 | Bartholomeus (hero) | 35+ [5/lvl] | 5+ [1/lvl] | 20 | MR,UNDERWATER | Cause Affliction: Slime / Sound file played on projectile impact: 107 |
|  | Earth Meld | Alter 3 | E2 | God: Titan of Growth (dormant until ~T10-13) | 25 | 5 | 60 | noShield | Cause Affliction: Earth Grip / Str +DRN vs 23 to get free. |
|  | Freeze | Alter 3 | W2 | Bartholomeus (hero) | 25 | 1 | 20 | noShield | Cause Affliction: Freeze |
|  | Torpor | Alter 3 | N2 | God: Titan of Growth (dormant until ~T10-13) | 35 | 1 | 20 | AN,MR,noShield,mind,noUndead | Fatigue: 20+ [5/lvl] / Unknown Attribute: 1024 |
|  | Curse of Stones | Alter 4 | E3 | God: Titan of Growth (dormant until ~T10-13) | - | 100% of battlefield | 300 3E | MR-easy,enemies | Cause Affliction: Rapidly Fatigue / Will not be cast against small numbers of enemies: 1 / |
|  | Encase in Ice | Alter 4 | W2 | Bartholomeus (hero) | 25 | 1 | 20 | noShield,UNDERWATER | Add To Effect Value (10): Encase in Ice / Target is encased in ice for 10 points. Each poi |
|  | Shrink | Alter 4 | N2 | God: Titan of Growth (dormant until ~T10-13) | 20+ [2/lvl] | 1 | 20 | MR,noShield | Cause Affliction: Diminuition / Size -1, HP -30%, Str -3, Def +1, Map move -2. |
|  | Slow | Alter 4 | W2 | Bartholomeus (hero) | 30 | 1 | 20 | MR | Cause Affliction: Slow / Slow 50%, Att -2, Def -2. |
|  | Winter's Chill | Alter 5 | W3 | Theurg + 4 slaves (master +2) | 25 | 5+ [1/lvl] | 20 | enemies | Cause Affliction: Freeze |
|  | Control | Alter 6 | S3 | Arch Theurg (+1 random F/A/W/S not counted) | 25 | One person | 100 1S | AN,MR,noShield | Enslave: lose commander status |
|  | Iron Bane | Alter 6 | E3 | God: Titan of Growth (dormant until ~T10-13) | - | 100% of battlefield | 100 1E |  | Cause Affliction: |
|  | Petrify | Alter 6 | E5 | God: Titan of Growth (dormant until ~T10-13) | 30 | 1 | 40 | AN | Petrify: 999 / Petrified targets have their natural protection increased to 20 and are gra |
|  | Crawl | Alter 7 | W3 | Theurg + 4 slaves (master +2) | 30 | 6+ [2/lvl] | 100 1W | MR | Cause Affliction: Slow / Slow 50%, Att -2, Def -2. |
|  | Curse of the Frog Prince | Alter 7 | N2 | God: Titan of Growth (dormant until ~T10-13) | 25 | One person | 20 | MR,noShield,enemies,mind,noUndead | Polymorph: #2222 Frog |
|  | Doom | Alter 7 | S4 | Theurg + 4 slaves (master +2) | - | 100% of battlefield | 100 1S | enemies | Cause Affliction: Curse |
|  | Prison of Sedna | Alter 7 | W3 | Theurg + 4 slaves (master +2) | 25 | 6+ [2/lvl] | 100 1W | noShield,UNDERWATER | Add To Effect Value (10): Encase in Ice / Targets are encased in ice for 10 points. Each p |
|  | Polymorph | Alter 8 | N3 | God: Titan of Growth (dormant until ~T10-13) | 25 | 10+ [2/lvl] | 200 2N | MR,noShield,enemies,mind,noUndead | Polymorph: #549 Boar |
|  | Army of Rats | Alter 9 | N5 | God: Titan of Growth (dormant until ~T10-13) | - | 100% of battlefield | 400 4N | MR-hard,noShield,enemies | Cause Affliction: Cause Battle Fright, Diminuition / Will not be cast against small number |
|  | Time Stop | Alter 9 | S6 | Bartholomeus + 8 slaves (+3) | - | Caster | 100 1S | MR | Time Stop: Unknown Effect 133 (104)? / Time Slow: 90%. Duration: about 10 rounds of combat |
| ✓ | Gust of Winds | Evoca 1 | A1 | Theurg | 35+ [5/lvl] | 2 | 10 | size-resists | Stun/Fascinate: Unknown Effect 128 (2013)? / Minor Blunt Damage / Capped Damage: 8 |
| ✓ | Slime | Evoca 1 | W1 | Theurg | 30+ [5/lvl] | 1 | 20 | MR,noShield | Cause Affliction: Slime / Sound file played on projectile impact: 107 / Slimed units are s |
|  | Web | Evoca 2 | N1 | God: Titan of Growth (dormant until ~T10-13) | 25+ [2/lvl] | 3 | 20 | noShield,size-resists | Cause Affliction: Web (?, Dominions 3) / Str +DRN vs 22 to get free. |
|  | Magic Duel | Evoca 3 | S1 | Theurg Acolyte | 100 | One person | 100 1S | AN,noShield,mind | Magic Duel: magic duel / Unknown Attribute: 1 / Only affects creatures with astral magic:  |
|  | Storm Wind | Evoca 3 | A2 | Arch Theurg (+1 random F/A/W/S not counted) | 40+ [5/lvl] | 8+ [2/lvl] | 10 | size-resists | Stun/Fascinate: Unknown Effect 128 (2013)? / Minor Blunt Damage / Capped Damage: 8 |
|  | Astral Geyser | Evoca 5 | S3 | Arch Theurg (+1 random F/A/W/S not counted) | 50+ [5/lvl] | 1 | 20 | AN,MR,mind | Add To Effect Value (2): Horror Mark / Astral Geyser Blast / Damage: 2 |
|  | Stellar Cascades | Evoca 5 | S2 | Theurg | 35 | 7 | 20 | AP | Fatigue: 25 |
|  | Unraveling | Encha 8 | S6 | Bartholomeus + 8 slaves (+3) | - | 100% of battlefield | 600 6S | AN,MR,MR-easy | Cause Affliction: Decay / Extra feeble mind battle field / Cause Affliction: Enfeeble Mind |
| ✓ | Desiccation | Thaum 1 | W2 | Bartholomeus (hero) | 30 | 1 | 20 | AN,MR,noUndead | Set Effect Value (1) if lower: Desiccation / Affected units get 2d8 fatigue dmg each turn. |
| ✓ | Horror Mark | Thaum 1 | S2 | Theurg | 50 | One person | 20 | noShield,mind | Add To Effect Value (1): Horror Mark |
|  | Calm Emotions | Thaum 2 | W1 | Theurg | 10 | One person | 20 | MR,noShield,mind | Cause Affliction: / Str -1, Att -1, reduces berserk value by 1, -4 morale on going berserk |
|  | Steal Breath | Thaum 2 | A1 | Theurg | 30 | One person | 20 | AN,MR,noShield,noUndead | Fatigue: 40+ [5/lvl] |
|  | Panic | Thaum 3 | N2 | God: Titan of Growth (dormant until ~T10-13) | 30 | 5+ [2/lvl] | 20 | AN,enemies | Cause Fear: 1 |
|  | Curse of the Desert | Thaum 4 | W3 | Theurg + 4 slaves (master +2) | 30 | 5 | 30 | AN,MR,noUndead | Set Effect Value (1) if lower: Desiccation / Affected units get 2d8 fatigue dmg each turn. |
|  | Paralyze | Thaum 4 | S2 | Theurg | 100 | One person | 20 | AN,MR,noShield,mind | Paralyze: 60+ [9/lvl] |
|  | Wildness | Thaum 4 | N3 | God: Titan of Growth (dormant until ~T10-13) | 30 | 1 | 20 | MR,noShield | Cause Affliction: Cause Confusion (?) / Wildness can only target animals. Confused 50% of  |
|  | Charm Animal | Thaum 5 | N2 | God: Titan of Growth (dormant until ~T10-13) | 20 | One person | 20 | MR-easy,noShield | Charm: retain commander status |
|  | Serenity | Thaum 5 | W3 | Theurg + 4 slaves (master +2) | 15 | 3+ [1/lvl] | 20 | MR,noShield,mind | Cause Affliction: / Str -1, Att -1, reduces berserk value by 1, -4 morale on going berserk |
|  | Enslave Mind | Thaum 6 | S4 | Theurg + 4 slaves (master +2) | 100 | One person | 20 | AN,MR,noShield,mind | Enslave: lose commander status |
| ✓ | Holy Word | Divin  | H2 | Theurg | 25 | One person |  | MR,sacreds | Stun/Fascinate: Unknown Effect 128 (100)? |

## Damage (45)

| Now | Spell | School | Path | First caster | Range | Area | Fatigue / gems | Flags | Effect |
|---|---|---|---|---|---|---|---|---|---|
|  | Maggots | Conju 4 | N1 | God: Titan of Growth (dormant until ~T10-13) | 25 | One person | 100 1N | AN,noShield | Poison (HP damage): 50 / An unresistable poison effect that only targets undead. |
| ✓ | Poison Touch | Alter 0 | N1 | God: Titan of Growth (dormant until ~T10-13) | 1 | One person | 5 | AN | Poison (HP damage): 10+ [5/lvl] |
| ✓ | Fists of Iron | Alter 1 | E1 | God: Titan of Growth (dormant until ~T10-13) | 1 | - | 20 |  | Damage: 15 |
|  | Armor of Achilles | Alter 2 | E1 | God: Titan of Growth (dormant until ~T10-13) | 15 | 1 | 40 | AN | Damage Armor (no effect on magic items): 10 / Does not affect natural armor. |
|  | Destruction | Alter 4 | E3 | God: Titan of Growth (dormant until ~T10-13) | 30 | 6 | 40 | AN | Damage Armor (no effect on magic items): 5 / Does not affect natural armor. |
|  | Lacerating Winds | Alter 4 | A2 | Arch Theurg (+1 random F/A/W/S not counted) | 40+ [5/lvl] | 5+ [1/lvl] | 20 |  | Damage: 5+ |
|  | Blood Poisoning | Alter 5 | N2 | God: Titan of Growth (dormant until ~T10-13) | 30 | One person | 20 | AN,noShield | Poison (HP damage): 15++ |
|  | Maws of the Earth | Alter 5 | E3 | God: Titan of Growth (dormant until ~T10-13) | 30+ [5/lvl] | 7+ [1/lvl] | 100 1E | AN,AP | Damage: 15+ / earth grip / Cause Affliction: Earth Grip / Str +DRN vs 23 to get free. |
|  | Shatter | Alter 5 | E3 | God: Titan of Growth (dormant until ~T10-13) | 15 | One person | 20 | AN,MR,noShield | Shatter: 35+ [5/lvl] / extra limp / Cause Affliction: Cause Limp / extra cripple / Cause A |
|  | Frozen Heart | Alter 6 | W1 | Theurg | 25+ [5/lvl] | One person | 20 | AN,noShield | Damage: 10++ |
|  | Liquify | Alter 8 | W4 | Bartholomeus + 5 Communicants (+2) | 30 | 3 | 20 | AN,MR-easy,MR-hard | Damage: 999 / Cripple / Cause Affliction: Cripple |
| ✓ | Flying Shards | Evoca 0 | E1 | God: Titan of Growth (dormant until ~T10-13) | 30+ [5/lvl] | - | 30 |  | Damage: 7+ |
| ✓ | Freezing Touch | Evoca 0 | W1 | Theurg | 1 | One person | 10 | AN | Damage: 9+ |
| ✓ | Arcane Bolt | Evoca 1 | S2 | Theurg | 40+ [5/lvl] | 1 | 20 | AN | Damage: 10+ |
| ✓ | Cold Bolt | Evoca 1 | W2 | Bartholomeus (hero) | 50+ [5/lvl] | 1 | 20 | AP | Damage: 13+ / Sound file played on projectile impact: 106 |
| ✓ | Shocking Grasp | Evoca 1 | A1 | Theurg | 1 | One person | 5 | AN | Damage: 18+++ / Minor Area Shock / Capped Damage: 1 |
| ✓ | Star Fires | Evoca 1 | S1 | Theurg Acolyte | 35 | - | 20 | AN | Damage: 5+ |
| ✓ | Vine Arrow | Evoca 1 | N1 | God: Titan of Growth (dormant until ~T10-13) | 30+ [5/lvl] | One person | 20 | AN,noShield | Damage: 14+ / Entangle / Cause Affliction: Entangle / Str +DRN vs 19 to get free. The diff |
| ✓ | Water Strike | Evoca 1 | W1 | Theurg | 35+ [5/lvl] | 1 | 20 | noShield,UNDERWATER | Damage: 13++ |
|  | Cold Blast | Evoca 2 | W2 | Bartholomeus (hero) | 7+ [1/lvl] | 3 | 20 | AP | Damage: 12++ / Unknown Attribute: 1 |
|  | Lightning Bolt | Evoca 2 | A2 | Arch Theurg (+1 random F/A/W/S not counted) | 40+ [5/lvl] | One person | 10 | AN,noShield | Damage: 14+ / Minor Area Shock / Capped Damage: 1 |
|  | Shock Wave | Evoca 2 | A2 | Arch Theurg (+1 random F/A/W/S not counted) | 2 | 6 | 10 | AN | Damage: 9+ |
|  | Solar Rays | Evoca 2 | S2 | Theurg | 40+ [5/lvl] | 1 | 20 | AP | Damage: 14+ / Requires sun presence: 1 |
|  | Freezing Mist | Evoca 3 | W3A1 | Theurg + 4 slaves (master +2) | 30 | 10+ [1/lvl] | 20 | AN | Lingering Cloud: 1 |
|  | Blade Wind | Evoca 4 | E3 | God: Titan of Growth (dormant until ~T10-13) | 35+ [5/lvl] | - | 80 |  | Damage: 14 |
|  | Breath of the Dragon | Evoca 4 | N2 | God: Titan of Growth (dormant until ~T10-13) | 20+ [5/lvl] | 4+ [1/lvl] | 20 | AN | Poison (HP damage): 7++ |
|  | Thunder Strike | Evoca 4 | A3 | Theurg + 4 slaves (master +2) | 100 | 1 | 50 | AN | Damage: 26++ / Gifts from Heaven: 1 / Thunder Shock / Damage: 2 |
|  | Earthquake | Evoca 5 | E4 | God: Titan of Growth (dormant until ~T10-13) | - | 100% of battlefield | 300 3E | AP | Damage: 8 / Extra effect in geo : (Cave) / Will not be cast against small numbers of enemi |
|  | Falling Frost | Evoca 5 | W3 | Theurg + 4 slaves (master +2) | 50 | 10+ [1/lvl] | 20 | AP | Damage: 10+ / Unknown Attribute: 1 / Projectile falls vertically: 1 / Gifts from Heaven: 1 |
|  | Orb Lightning | Evoca 5 | A2 | Arch Theurg (+1 random F/A/W/S not counted) | 20 | One person | 20 | AN | Chaining Damage: 5 / Number of chain lightning bounces : 7 |
|  | Poison Arrows | Evoca 5 | N2 | God: Titan of Growth (dormant until ~T10-13) | 35+ [5/lvl] | - | 20 |  | Damage: 15+ / Extra poison damage: 5 / Extra +5 poison dmg. |
|  | Cleansing Water | Evoca 6 | W2 | Bartholomeus (hero) | 30+ [5/lvl] | 5+ [1/lvl] | 20 | AN | Damage: 5+ |
|  | Stream of Life | Evoca 6 | N3 | God: Titan of Growth (dormant until ~T10-13) | 40+ [5/lvl] | 1 | 20 | AN,MR,noUndead | Stream of Life: 40+ [5/lvl] / Death chance: 40% +5% per additional caster level. |
|  | Ice Strike | Evoca 7 | W2 | Bartholomeus (hero) | 30 | 4+ [2/lvl] | 20 |  | Damage: 18 / Unknown Attribute: 1 |
|  | Storm of Thorns | Evoca 7 | N2 | God: Titan of Growth (dormant until ~T10-13) | 35+ [5/lvl] | Caster | 20 | AN,noShield | Damage: 15+ / Entangle / Cause Affliction: Entangle / Str +DRN vs 19 to get free. The diff |
|  | Chain Lightning | Evoca 8 | A3 | Theurg + 4 slaves (master +2) | 25 | One person | 30 | AN | Chaining Damage: 6+ / Number of chain lightning bounces : 20 |
|  | Niefel Flames | Evoca 9 | W5 | Bartholomeus + 8 slaves (+3) | 40+ [5/lvl] | 75+ [5/lvl] | 100 1W | AP | Damage: 12+ / Unknown Attribute: 1 |
|  | Arrow of the Western Wind | Encha 3 | A2 | Arch Theurg (+1 random F/A/W/S not counted) | 50+ [5/lvl] | One person | 20 |  | Damage: 20+ / Terrain-Specific Recruit: Cave : 3 |
|  | Opposition | Encha 6 | S3 | Arch Theurg (+1 random F/A/W/S not counted) | 25 | One person | 20 | AN,MR,MR-hard,noShield | Damage: 999 / Stun Magic Being / Stun/Fascinate: Unknown Effect 128 (100)? |
|  | Mind Burn | Thaum 2 | S2 | Theurg | 100 | One person | 20 | AN,MR,noShield,mind | Damage: 12+ |
|  | Sailors' Death | Thaum 3 | W3 | Theurg + 4 slaves (master +2) | 30 | 1 | 20 | AN,MR,noUndead | Damage: 14+++ |
|  | Soul Slay | Thaum 5 | S3 | Arch Theurg (+1 random F/A/W/S not counted) | 100 | One person | 20 | AN,MR,noShield,mind | Damage: 999 |
| ✓ | Pull from the Grave | Divin  | H1 | Theurg Acolyte | 25+ [5/lvl] | 4+ [2/lvl] |  | AN,MR,noShield | Damage: 4+++ / God Path Restriction : Earth / Grip / Cause Affliction: Earth Grip |
| ✓ | Smite Demon | Divin  | H2 | Theurg | 30+ [5/lvl] | One person |  | AN,MR,noShield,noUndead | Damage: 15+ [5/lvl] |
| ✓ | Word of Stone | Divin  | H3 | Arch Theurg (+1 random F/A/W/S not counted) | 25 | One person |  | AN,MR,noShield | Damage: 10 / God Path Restriction : Earth / Petrification / Petrify: 999 |

## Battlefield (17)

| Now | Spell | School | Path | First caster | Range | Area | Fatigue / gems | Flags | Effect |
|---|---|---|---|---|---|---|---|---|---|
|  | Light of the Northern Star | Conju 4 | S3 | Arch Theurg (+1 random F/A/W/S not counted) | - | Caster | 200 2S | noShield | Enchant Battlefield | Enchant World: Light of the Northern Star / Astral magic bonus +1 to |
|  | Howl | Conju 5 | N3 | God: Titan of Growth (dormant until ~T10-13) | - | Caster | 300 3N |  | Enchant Battlefield | Enchant World: Howl / This spell is twice as effective if used in fo |
|  | Shark Attack | Conju 6 | W3 | Theurg + 4 slaves (master +2) | - | - | 300 3W | UNDERWATER | Enchant Battlefield | Enchant World: Shark Attack |
|  | Mist | Alter 3 | A3 | Theurg + 4 slaves (master +2) | - | Caster | 100 1A |  | Enchant Battlefield | Enchant World: Mists of Deception |
|  | Storm | Alter 5 | A4 | Bartholomeus + 5 Communicants (+2) | - | Caster | 100 1A |  | Enchant Battlefield | Enchant World: Storm / Cannot cast from terrain : (Cave) / Precision |
|  | Blizzard | Alter 6 | A4W3 | Bartholomeus + 5 Communicants (+2) | - | Caster | 100 1A |  | Enchant Battlefield | Enchant World: / Cannot cast from terrain : (Cave) / Unknown Attribu |
|  | Rain | Evoca 3 | W3 | Theurg + 4 slaves (master +2) | - | Caster | 100 1W |  | Enchant Battlefield | Enchant World: Rain / Cannot cast from terrain : (Cave) / Fire spell |
|  | Wrathful Skies | Evoca 6 | A5 | Bartholomeus + 8 slaves (+3) | - | Caster | 200 2A |  | Enchant Battlefield | Enchant World: Wrathful Skies / 15 AN shock dmg. Storm doubles the n |
|  | Astral Tempest | Evoca 8 | S5 | Bartholomeus + 5 Communicants (+2) | - | Caster | 200 2S |  | Enchant Battlefield | Enchant World: Astral Tempest / Continuously targets the battlefield |
|  | Friendly Currents | Encha 5 | W3 | Theurg + 4 slaves (master +2) | - | Caster | 100 1W | UNDERWATER | Enchant Battlefield | Enchant World: Friendly Currents |
|  | Quagmire | Encha 5 | W4 | Bartholomeus + 5 Communicants (+2) | - | Caster | 100 1W |  | Enchant Battlefield | Enchant World: Quagmire / All units without Swamp Survival suffer -1 |
|  | Grip of Winter | Encha 6 | W4 | Bartholomeus + 5 Communicants (+2) | - | Caster | 200 2W |  | Enchant Battlefield | Enchant World: Cold / Frost Clouds (level 1) appear all over the bat |
|  | Relief | Encha 6 | N5 | God: Titan of Growth (dormant until ~T10-13) | - | Caster | 100 1N |  | Enchant Battlefield | Enchant World: Relief / AN fatigue reduction roll +1. |
|  | Solar Brilliance | Encha 7 | S5 | Bartholomeus + 5 Communicants (+2) | - | Caster | 300 3S |  | Enchant Battlefield | Enchant World: Solar Brilliance / Requires sun presence: 1 / Dispel  |
|  | Demon Cleansing | Encha 9 | W5 | Bartholomeus + 8 slaves (+3) | - | Caster | 100 1W |  | Enchant Battlefield | Enchant World: Demon Cleansing |
|  | The Ravenous Swarm | Thaum 5 | N3 | God: Titan of Growth (dormant until ~T10-13) | - | - | 100 1N |  | Enchant Battlefield | Enchant World: Ravenous Swarm / The square with the current target i |
|  | Growing Fury | Thaum 6 | N4 | God: Titan of Growth (dormant until ~T10-13) | - | Caster | 100 1N |  | Enchant Battlefield | Enchant World: Growing Fury |

## Summon (13)

| Now | Spell | School | Path | First caster | Range | Area | Fatigue / gems | Flags | Effect |
|---|---|---|---|---|---|---|---|---|---|
|  | Summon Hawk | Conju 2 | A1 | Theurg | - | - | 20 |  | Edge of Battlefield Summon: #517 Black Hawk / Cannot cast from terrain : (Cave) |
|  | Summon Lesser Air Elemental | Conju 3 | A1 | Theurg | - | - | 100 1A |  | Summon Units: #3727 Air Elemental |
|  | Summon Lesser Earth Elemental | Conju 3 | E1 | God: Titan of Growth (dormant until ~T10-13) | - | - | 100 1E |  | Summon Units: #3743 Earth Elemental |
|  | Summon Lesser Water Elemental | Conju 3 | W1 | Theurg | - | - | 100 1W |  | Summon Units: #3735 Water Elemental |
|  | School of Sharks | Conju 4 | W2 | Bartholomeus (hero) | - | - | 100 1W | UNDERWATER | Edge of Battlefield Summon: #815 Small Shark x 10++ |
|  | Summon Air Elemental | Conju 5 | A3 | Theurg + 4 slaves (master +2) | - | - | 100 1A |  | Summon Units: #3724 Air Elemental |
|  | Summon Earth Elemental | Conju 5 | E3 | God: Titan of Growth (dormant until ~T10-13) | - | - | 100 1E |  | Summon Units: #3740 Earth Elemental |
|  | Summon Water Elemental | Conju 5 | W3 | Theurg + 4 slaves (master +2) | - | - | 100 1W |  | Summon Units: #3732 Water Elemental |
|  | Living Clouds | Conju 7 | A4 | Bartholomeus + 5 Communicants (+2) | 1 | - | 200 2A |  | Summon Units: #3725 Air Elemental x 4+ |
|  | Living Earth | Conju 7 | E4 | God: Titan of Growth (dormant until ~T10-13) | 1 | - | 200 2E |  | Summon Units: #3741 Earth Elemental x 4+ |
|  | Living Water | Conju 7 | W4 | Bartholomeus + 5 Communicants (+2) | 1 | - | 200 2W |  | Summon Units: #3733 Water Elemental x 4+ |
|  | Swarm | Alter 4 | N2 | God: Titan of Growth (dormant until ~T10-13) | - | - | 100 1N |  | Summon Units: Random Bug x 20++ |
|  | Creeping Doom | Alter 7 | N3 | God: Titan of Growth (dormant until ~T10-13) | - | - | 100 1N |  | Summon Units: Random Bug x 70+ [5/lvl] |

## Other (3)

| Now | Spell | School | Path | First caster | Range | Area | Fatigue / gems | Flags | Effect |
|---|---|---|---|---|---|---|---|---|---|
|  | Animate Tree | Alter 3 | N1 | God: Titan of Growth (dormant until ~T10-13) | 10 | 1 | 20 |  | Unknown: Unknown Effect 166 (361)? |
|  | Awaken Forest | Alter 9 | N5 | God: Titan of Growth (dormant until ~T10-13) | - | 50% of battlefield | 200 2N | noShield | Unknown: Unknown Effect 166 (361)? |
|  | Poison Darts | Evoca 3 | N1 | God: Titan of Growth (dormant until ~T10-13) | 30+ [5/lvl] | - | 20 | AP | Capped Damage: 9 / Extra poison damage: 5 / Extra +5 poison dmg. |
