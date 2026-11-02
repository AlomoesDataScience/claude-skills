# Summoning spells: modelled melee value (generated)

Made by `scripts/spells.py summons -n 2500` (2026-10-28, rerun after the shield fix). Every researchable summoning spell of every school (generic, plus Pythium's national ones), sorted by HI kills per gem. **Kills vs X** = enemy men of type X the spell's summons kill in melee before they die, all summons added up: each summon's kills a round (all its melee weapons, trample when bigger than the foe) × the rounds it lives while 1.5-4 foes attack it (by size). Lives are capped by fatigue (100 / encumbrance rounds) and 50 rounds. Counts are at the minimum path level. HI sword = Heavy Infantry with broadsword and shield (prot 13); Militia = id 18. Awe, invulnerability, ethereal, slash/pierce/blunt resistance and regeneration count; morale, missiles, spells and magic weapons against them don't. Ranking and caveats: `summons.md`.

| Spell | Research | Path | Gems | Summons | Kills vs HI sword | Kills vs Militia | HI kills / gem | Notes | Pythium caster |
|---|---|---|---|---|---|---|---|---|---|
| Will o' the Wisp | Conjuration 5 (combat) | F1 | 1F | 2 x Will o' the Wisp (hp 3, prot 0, def 20, MR 12, sz 1) | 25.3 | 40.3 | 25.30 | ethereal, magicbeing |  |
| Spirits of the Wood | Conjuration 5 (ritual) | N3 | 8N | 15 x Woodland Spirit (hp 10, prot 0, def 10, MR 15, sz 3) | 137.5 | 170.3 | 17.19 | awe 4, ethereal, regeneration 20 | God (awake) |
| Conjure Phantasmal Beast | Conjuration 5 (combat) | G3 | 1G | 1 x Phantasmal Beast (hp 62, prot 6, def 12, MR 15, sz 7) | 15.3 | 50.4 | 15.30 | amphibian, ethereal, magicbeing |  |
| Conjure Phantasmal Knight | Conjuration 7 (combat) | G2 | 1G | 1 x Phantasmal Knight (hp 15, prot 17, def 20, MR 14, sz 3) | 12.7 | 13.2 | 12.68 | ethereal, magicbeing |  |
| Illusory Army | Evocation 5 (combat) | G3 | 1G | 20 x Warrior Illusion (hp 1, prot 0, def 10, MR 10, sz 3) | 11.8 | 28.6 | 11.83 | amphibian, ethereal, inanimate |  |
| Ghost Riders | Conjuration 9 (ritual, remote) | D5 | 5D | 75 x Longdead Horseman (hp 5, prot 8, def 14, MR 10, sz 3); 1 x Wraith Lord (hp 33, prot 18, def 18, MR 17, sz 3) | 56.9 | 248.4 | 11.39 | amphibian, cold 3, ethereal, fear 5, inanimate, pierceres, undead |  |
| Summon Water Elemental | Conjuration 5 (combat) | W3 | 1W | 1 x Water Elemental (hp 81, prot 0, def 13, MR 16, sz 7) | 10.7 | 50.0 | 10.71 | amphibian, bluntres, inanimate, magicbeing, pierceres, slashres | Theurg + 4 slaves (master +2) |
| Legion of Wights | Conjuration 9 (ritual) | D5 | 20D | 17 x Wight (hp 20, prot 18, def 14, MR 14, sz 3) | 204.6 | 400.9 | 10.23 | cold 3, undead |  |
| Conjure Phantasmal Warriors | Conjuration 4 (combat) | G2 | 1G | 2 x Phantasmal Warrior (hp 14, prot 9, def 17, MR 14, sz 3) | 10.1 | 10.5 | 10.09 | ethereal, magicbeing |  |
| Living Clouds | Conjuration 7 (combat) | A4 | 2A | 4 x Air Elemental (hp 35, prot 0, def 14, MR 15, sz 6) | 18.2 | 82.8 | 9.12 | ethereal, flying, inanimate, magicbeing, trample | Bartholomeus + 5 Communicants (+2) |
| Living Water | Conjuration 7 (combat) | W4 | 2W | 4 x Water Elemental (hp 60, prot 0, def 12, MR 15, sz 6) | 15.9 | 79.3 | 7.94 | amphibian, bluntres, inanimate, magicbeing, pierceres, slashres | Bartholomeus + 5 Communicants (+2) |
| Living Earth | Conjuration 7 (combat) | E4 | 2E | 4 x Earth Elemental (hp 70, prot 13, def 10, MR 16, sz 6) | 15.4 | 78.6 | 7.69 | amphibian, inanimate, magicbeing, trample | God: Titan of Growth (dormant until ~T10-13) |
| Iron Pigs | Alteration 6 (ritual) | E3N1 | 9E | 11 x Iron Boar (hp 25, prot 20, def 7, MR 5, sz 5); 1 x Gladiator (hp 12, prot 10, def 9, MR 10, sz 3) | 67.2 | 205.6 | 7.47 | animal, holy, trample | God (awake) |
| Illusory Attack | Evocation 7 (ritual, remote) | G4 | 8G | 55 x Warrior Illusion (hp 1, prot 0, def 10, MR 10, sz 3); 1 x Captain Illusion (hp 1, prot 0, def 11, MR 10, sz 3); 40 x Archer Illusion (hp 1, prot 0, def 10, MR 10, sz 3); 1 x Captain Illusion (hp 1, prot 0, def 11, MR 10, sz 3) | 57.8 | 137.0 | 7.23 | amphibian, ethereal, inanimate, missile |  |
| Army of the Dead | Enchantment 9 (ritual, remote) | D5 | 10D | 100 x Mound King (hp 7, prot 12, def 13, MR 14, sz 3); 1 x Mound King (hp 7, prot 12, def 13, MR 14, sz 3) | 67.0 | 753.8 | 6.70 | inanimate, pierceres, undead |  |
| Summon Air Elemental | Conjuration 5 (combat) | A3 | 1A | 1 x Air Elemental (hp 48, prot 0, def 15, MR 16, sz 7) | 6.5 | 31.8 | 6.48 | ethereal, flying, inanimate, magicbeing, trample | Theurg + 4 slaves (master +2) |
| Summon Earth Elemental | Conjuration 5 (combat) | E3 | 1E | 1 x Earth Elemental (hp 93, prot 14, def 10, MR 16, sz 7) | 5.7 | 23.7 | 5.70 | amphibian, inanimate, magicbeing, trample | God: Titan of Growth (dormant until ~T10-13) |
| Summon Cave Crab | Conjuration 3 (ritual) | E1W1 | 4E | 1 x Cave Crab (hp 54, prot 22, def 9, MR 4, sz 6) | 18.0 | 26.3 | 4.49 | amphibian, animal, undisciplined |  |
| Summon Kithaironic Lion | Conjuration 4 (ritual) | N3E1 | 5N | 1 x Kithaironic Lion (hp 31, prot 7, def 11, MR 13, sz 4) | 22.4 | 47.7 | 4.49 | animal, invulnerable 25, magicbeing, pierceres, slashres, undisciplined | God (awake) |
| Bind Spine Devil | Blood 2 (ritual) | B2 | 2B | 1 x Spine Devil (hp 25, prot 13, def 12, MR 16, sz 3) | 8.4 | 27.8 | 4.22 | demon |  |
| Summon Fay Footfolk | Conjuration 4 (ritual) | G2N1 | 12G | 6 x Fay Footman (hp 13, prot 15, def 20, MR 14, sz 3) | 48.9 | 127.8 | 4.07 |  |  |
| Summon Unseelie Soldiers | Conjuration 4 (ritual) | G2W1 | 12G | 6 x Unseelie Soldier (hp 13, prot 15, def 20, MR 14, sz 3) | 48.6 | 134.9 | 4.05 |  |  |
| Contact Draconians | Conjuration 5 (ritual) | A3 | 20A | 1 x Draconian Chief (hp 52, prot 10, def 13, MR 14, sz 6); 30 x Draconian (hp 45, prot 9, def 12, MR 14, sz 6) | 80.3 | 369.2 | 4.01 | flying | Arch Theurg + booster |
| Bind Scorpion Beast | Conjuration 3 (ritual) | F1E1 | 2F | 1 x Scorpion Beast (hp 44, prot 16, def 7, MR 5, sz 6) | 7.9 | 19.5 | 3.94 | animal, undisciplined |  |
| Nest of Salamanders | Conjuration 4 (combat) | F2 | 1F | 10 x Salamander Asp (hp 2, prot 1, def 10, MR 12, sz 1) | 3.4 | 7.7 | 3.43 | animal, fireshield 3, magicbeing, undisciplined |  |
| Nest of Asps | Conjuration 4 (combat) | N2D1 | 1N | 10 x Asp (hp 2, prot 1, def 10, MR 4, sz 1) | 3.4 | 7.2 | 3.42 | animal, magicbeing, undisciplined |  |
| Clockwork Horrors | Construction 4 (ritual) | E2 | 9E | 15 x Clockwork Horror (hp 5, prot 18, def 10, MR 12, sz 2) | 29.9 | 189.9 | 3.33 | inanimate, magicbeing | God (awake) |
| Summon Unseelie Knights | Conjuration 5 (ritual) | G3W1 | 15G | 3 x Unseelie Knight (hp 16, prot 21, def 22, MR 14, sz 3) | 49.5 | 97.6 | 3.30 |  |  |
| Enliven Statues | Enchantment 6 (ritual) | E3 | 20E | 10 x Living Statue (hp 15, prot 20, def 14, MR 12, sz 4) | 64.6 | 174.6 | 3.23 | inanimate, magicbeing, pierceres, slashres | God (awake) |
| Summon Fay Knights | Conjuration 5 (ritual) | G3N1 | 15G | 3 x Fay Knight (hp 16, prot 21, def 22, MR 14, sz 3) | 48.1 | 100.5 | 3.21 |  |  |
| Summon Horned Serpents | Conjuration 2 (ritual) | N1 | 4N | 10 x Horned Serpent (hp 29, prot 11, def 7, MR 13, sz 4) | 12.4 | 29.0 | 3.10 | animal, undisciplined | God (awake) |
| Revive Wights | Conjuration 3 (ritual) | D2 | 20D | 5 x Wight (hp 20, prot 18, def 14, MR 14, sz 3) | 60.2 | 117.9 | 3.01 | cold 3, undead |  |
| Forces of Darkness | Blood 9 (ritual) | B6 | 50B | 22 x Fiend of Darkness (hp 30, prot 10, def 13, MR 17, sz 4) | 144.9 | 475.8 | 2.90 | demon, flying |  |
| Summon Shades | Conjuration 2 (ritual) | D2 | 5D | 6 x Shade (hp 10, prot 0, def 12, MR 13, sz 3) | 13.9 | 40.1 | 2.78 | amphibian, ethereal, undead |  |
| Conjure Phantasmal Wolves | Conjuration 3 (combat) | G1 | 1G | 2 x Phantasmal Wolf (hp 11, prot 0, def 12, MR 12, sz 3) | 2.8 | 6.1 | 2.78 | ethereal, magicbeing |  |
| Infernal Crusade | Blood 9 (ritual) | B5E2 | 50B | 10 x Demon Knight (hp 20, prot 22, def 17, MR 15, sz 3) | 137.4 | 249.0 | 2.75 | demon, fear 5 |  |
| Summon Asp Turtle | Conjuration 7 (ritual) | W3 | 10W | 1 x Asp Turtle (hp 91, prot 22, def 6, MR 13, sz 10) | 27.0 | 53.2 | 2.70 | animal, aquatic, fear 5, trample |  |
| False Horror | Evocation 6 (combat) | G3 | 0 | 1 x False Horror (hp 1, prot 0, def 13, MR 10, sz 4) | 2.7 | 7.1 | 2.68 | amphibian, ethereal, fear 5, inanimate |  |
| Summon Lesser Air Elemental | Conjuration 3 (combat) | A1 | 1A | 1 x Air Elemental (hp 15, prot 0, def 12, MR 13, sz 4) | 2.6 | 10.0 | 2.62 | ethereal, flying, inanimate, magicbeing, trample | Theurg |
| Summon Spring Hawks | Conjuration 5 (ritual) | A3 | 13A | 6 x Spring Hawk (hp 7, prot 0, def 15, MR 15, sz 3) | 31.5 | 96.8 | 2.42 | animal, ethereal, flying, magicbeing | Arch Theurg + booster |
| Clockwork Soldiers | Construction 2 (ritual) | E2 | 4E | 11 x Clockwork Soldier (hp 7, prot 18, def 11, MR 12, sz 3) | 9.5 | 66.3 | 2.38 | inanimate, magicbeing | God (awake) |
| Enliven Gargoyles | Enchantment 5 (ritual) | E3A1 | 12E | 11 x Gargoyle (hp 12, prot 20, def 10, MR 12, sz 3) | 27.6 | 217.2 | 2.30 | flying, inanimate, magicbeing, pierceres, slashres |  |
| Summon Ether Warriors | Conjuration 5 (ritual) | S3D1 | 15S | 3 x Ether Warrior (hp 22, prot 19, def 14, MR 15, sz 4) | 34.3 | 40.5 | 2.29 | amphibian, ethereal, magicbeing |  |
| Revive Bane Lord | Conjuration 5 (ritual) | D4 | 12D | 1 x Bane Lord (hp 42, prot 19, def 14, MR 16, sz 4) | 26.5 | 33.8 | 2.21 | cold 3, undead |  |
| Revive Bane | Conjuration 3 (ritual) | D2 | 7D | 1 x Bane (hp 23, prot 18, def 13, MR 15, sz 3) | 15.4 | 31.9 | 2.20 | cold 3, undead |  |
| Bind Fiend | Blood 2 (ritual) | B2 | 3B | 1 x Fiend of Darkness (hp 30, prot 10, def 13, MR 17, sz 4) | 6.6 | 21.6 | 2.20 | demon, flying |  |
| Siege Golem | Construction 8 (ritual) | E3 | 15E | 1 x Siege Golem (hp 165, prot 24, def 9, MR 12, sz 10) | 31.8 | 45.3 | 2.12 | inanimate, magicbeing | God (awake) |
| Contact Trolls | Conjuration 5 (ritual) | E3 | 10E | 6 x Troll (hp 35, prot 16, def 9, MR 14, sz 5) | 20.9 | 91.4 | 2.09 | regeneration 10 | God (awake) |
| Angelic Host | Conjuration 7 (ritual, remote) | S5 | 50S | 7 x Angel of the Host (hp 17, prot 23, def 17, MR 17, sz 5); 1 x Arch Angel (hp 49, prot 0, def 16, MR 18, sz 6) | 104.0 | 117.2 | 2.08 | F4 H3, awe 5, awe 6, flying, holy, invulnerable 15, invulnerable 25, magicbeing |  |
| Ether Gate | Conjuration 6 (ritual) | S4D1 | 90S | 1 x Ether Lord (hp 25, prot 10, def 15, MR 18, sz 4); 15 x Ether Warrior (hp 22, prot 19, def 14, MR 15, sz 4) | 185.6 | 229.8 | 2.06 | S3 D2 U1, amphibian, ethereal, magicbeing |  |
| Mechanical Men | Construction 6 (ritual) | E2 | 15E | 15 x Mechanical Man (hp 8, prot 18, def 14, MR 12, sz 3) | 30.9 | 228.8 | 2.06 | inanimate, magicbeing | God (awake) |
| Summon Lesser Earth Elemental | Conjuration 3 (combat) | E1 | 1E | 1 x Earth Elemental (hp 33, prot 12, def 10, MR 13, sz 4) | 2.0 | 9.8 | 2.01 | amphibian, inanimate, magicbeing, trample | God: Titan of Growth (dormant until ~T10-13) |
| Living Fire | Conjuration 7 (combat) | F4 | 2F | 4 x Fire Elemental (hp 53, prot 0, def 8, MR 15, sz 6) | 3.9 | 15.8 | 1.96 | ethereal, fireshield 12, heat 6, inanimate, magicbeing |  |
| Summon Illearth | Blood 5 (combat) | B2E2 | 2B | 1 x Illearth (hp 93, prot 12, def 10, MR 16, sz 7) | 3.8 | 19.3 | 1.92 | amphibian, inanimate, magicbeing, trample |  |
| Naiad Warriors | Conjuration 5 (ritual) | W3N1 | 18W | 25 x Kydnid (hp 10, prot 13, def 13, MR 15, sz 3) | 34.3 | 132.7 | 1.91 | amphibian, awe 4 |  |
| Summon Summer Lions | Conjuration 5 (ritual) | F3 | 13F | 6 x Summer Lion (hp 44, prot 0, def 11, MR 15, sz 4) | 24.5 | 146.7 | 1.89 | animal, ethereal, heat 3, magicbeing |  |
| Leviathan | Enchantment 7 (ritual) | D3W1 | 10D | 1 x Leviathan (hp 143, prot 19, def 3, MR 13, sz 10) | 18.4 | 45.2 | 1.84 | amphibian, fear 10, inanimate, trample, undead |  |
| Summon Wyverns | Conjuration 4 (ritual) | A2 | 3A | 2 x Wyvern (hp 35, prot 12, def 11, MR 14, sz 6) | 5.4 | 22.9 | 1.81 | animal, flying | Arch Theurg / Bartholomeus |
| Infernal Forces | Blood 9 (ritual) | B5F2 | 50B | 18 x Devil (hp 35, prot 8, def 13, MR 17, sz 4); 40 x Imp (hp 8, prot 6, def 15, MR 13, sz 2) | 89.8 | 523.5 | 1.80 | demon, flying, heat 3 |  |
| Awaken Tarrasque | Conjuration 9 (ritual) | N5 | 15N | 1 x Tarrasque (hp 245, prot 19, def 8, MR 18, sz 10) | 26.8 | 38.6 | 1.79 | fear 10, poisoncloud 10, regeneration 10 | God (awake) |
| Summon Manticores | Conjuration 5 (ritual) | N2E2 | 10N | 3 x Manticore (hp 62, prot 11, def 11, MR 14, sz 8) | 17.4 | 70.6 | 1.74 | fear 5, flying, missile | God (awake) |
| Contact Forest Giants | Conjuration 6 (ritual) | N3 | 2N | 2 x Forest Giant (hp 66, prot 12, def 9, MR 9, sz 8) | 3.1 | 10.8 | 1.55 | undisciplined | God (awake) |
| Summon Fire Snakes | Conjuration 6 (ritual) | F2 | 8F | 11 x Fire Snake (hp 25, prot 9, def 7, MR 15, sz 4) | 12.3 | 33.0 | 1.54 | animal, heat 3, magicbeing, undisciplined |  |
| Manifest Vitriol | Alteration 6 (ritual) | W2F1 | 3W | 1 x Green Lion (hp 34, prot 7, def 11, MR 16, sz 4) | 4.6 | 34.7 | 1.52 | ethereal, magicbeing, missile |  |
| Contact Angel of the Host | Conjuration 5 (ritual) | S3 | 7S | 1 x Angel of the Host (hp 17, prot 23, def 17, MR 17, sz 5) | 10.3 | 12.1 | 1.47 | awe 5, flying, holy, invulnerable 15, magicbeing | Arch Theurg / Bartholomeus |
| Call Abomination | Conjuration 9 (ritual) | S5W2 | 15S | 1 x Abomination (hp 266, prot 5, def 8, MR 20, sz 10) | 21.2 | 79.6 | 1.41 | amphibian, bluntres, fear 10, magicbeing, missile, regeneration 10 |  |
| Contact Hill Giant | Conjuration 6 (ritual) | E3 | 3E | 1 x Hill Giant (hp 106, prot 14, def 7, MR 9, sz 9) | 4.1 | 9.0 | 1.36 | undisciplined | God (awake) |
| Summon Sea Serpent | Conjuration 4 (ritual) | W2 | 4W | 1 x Sea Serpent (hp 70, prot 10, def 11, MR 8, sz 10) | 5.3 | 22.2 | 1.33 | animal, aquatic, fear 5, undisciplined | Arch Theurg / Bartholomeus |
| Summon Fire Elemental | Conjuration 5 (combat) | F3 | 1F | 1 x Fire Elemental (hp 70, prot 0, def 8, MR 16, sz 7) | 1.3 | 4.8 | 1.32 | ethereal, fireshield 13, heat 7, inanimate, magicbeing |  |
| Summon Gryphons | Conjuration 4 (ritual) | A2 | 9A | 11 x Gryphon (hp 44, prot 7, def 10, MR 13, sz 8) | 11.7 | 77.9 | 1.30 | animal, flying, undisciplined | Arch Theurg / Bartholomeus |
| Troll King's Court | Conjuration 6 (ritual) | E4 | 65E | 1 x Troll King (hp 42, prot 25, def 7, MR 17, sz 5); 10 x Troll (hp 35, prot 16, def 9, MR 14, sz 5); 5 x War Troll (hp 38, prot 24, def 5, MR 14, sz 5); 2 x Troll Moose Knight (hp 40, prot 24, def 11, MR 14, sz 5) | 84.5 | 230.9 | 1.30 | E3 G1, regeneration 10, regeneration 15 | God (awake) |
| Summon Cave Grubs | Conjuration 1 (ritual) | E1 | 5E | 10 x Cave Grub (hp 52, prot 6, def 7, MR 7, sz 7) | 6.4 | 15.1 | 1.28 | animal, magicbeing, undisciplined | God (awake) |
| Summon Ghosts | Conjuration 6 (ritual) | D2 | 10D | 6 x Ghost (hp 20, prot 0, def 15, MR 15, sz 3) | 12.0 | 73.7 | 1.20 | amphibian, cold 3, ethereal, fear 5, undead |  |
| Summon Fire Ants | Conjuration 2 (ritual) | F2N1 | 9F | 10 x Fire Ant (hp 21, prot 14, def 8, MR 5, sz 6) | 10.8 | 26.6 | 1.19 | animal, magicbeing, undisciplined |  |
| Heavenly Wrath | Conjuration 7 (ritual) | S3F1 | 35S | 1 x Angel of Fury (hp 49, prot 0, def 12, MR 18, sz 7) | 41.8 | 65.4 | 1.19 | fear 5, flying, holy, invulnerable 20 |  |
| Call Krakens | Conjuration 3 (ritual) | W3 | 4W | 6 x Kraken (hp 60, prot 8, def 7, MR 5, sz 8) | 4.7 | 25.5 | 1.18 | animal, aquatic, bluntres |  |
| Contact Lamias | Conjuration 6 (ritual) | N3 | 5N | 11 x Lamia (hp 14, prot 5, def 9, MR 13, sz 3) | 5.7 | 48.7 | 1.15 | regeneration 50 | God (awake) |
| Ghost Wolves | Evocation 4 (combat) | G3 | 0 | 2 x Wolf Illusion (hp 1, prot 0, def 10, MR 10, sz 3) | 1.1 | 2.5 | 1.11 | amphibian, ethereal, inanimate |  |
| Summon Great Eagles | Conjuration 6 (ritual) | A3 | 8A | 11 x Great Eagle (hp 52, prot 7, def 11, MR 14, sz 9) | 8.7 | 65.9 | 1.08 | animal, flying | Arch Theurg + booster |
| Juggernaut Construction | Construction 8 (ritual) | S5 | 25S | 1 x Juggernaut (hp 200, prot 22, def 5, MR 18, sz 10) | 26.3 | 51.4 | 1.05 | H3, bluntres, holy, inanimate, magicbeing, pierceres, trample |  |
| Iron Dragon | Construction 8 (ritual) | E4F2 | 25E | 1 x Iron Dragon (hp 150, prot 24, def 7, MR 12, sz 10) | 24.7 | 51.6 | 0.99 | fear 5, flying, inanimate, magicbeing, missile, trample |  |
| Summon Winter Wolves | Conjuration 5 (ritual) | W3 | 6W | 6 x Winter Wolf (hp 13, prot 0, def 11, MR 15, sz 3) | 5.7 | 49.5 | 0.95 | animal, cold 6, ethereal, magicbeing |  |
| Faerie Court | Conjuration 8 (ritual) | G4N1 | 60G | 1 x Faery Queen (hp 18, prot 0, def 11, MR 18, sz 5); 10 x Sprite (hp 2, prot 0, def 20, MR 14, sz 1); 3 x Fay Footman (hp 13, prot 15, def 20, MR 14, sz 3); 2 x Fay Knight (hp 16, prot 21, def 22, MR 14, sz 3) | 56.6 | 134.4 | 0.94 | N3 G3 U2, awe 4, flying, magicbeing |  |
| Sea King's Court | Conjuration 6 (ritual) | W4 | 55W | 1 x Sea King (hp 63, prot 9, def 12, MR 17, sz 6); 15 x Sea Troll (hp 52, prot 8, def 10, MR 14, sz 6); 5 x Troll Guard (hp 58, prot 16, def 10, MR 14, sz 6) | 51.8 | 151.5 | 0.94 | W3, amphibian, regeneration 10, regeneration 15 |  |
| Bind Devil | Blood 3 (ritual) | B2F2 | 5B | 1 x Devil (hp 35, prot 8, def 13, MR 17, sz 4) | 4.6 | 18.4 | 0.92 | demon, flying, heat 3 |  |
| Bind Demon Knight | Blood 5 (ritual) | B2E2 | 15B | 1 x Demon Knight (hp 20, prot 22, def 17, MR 15, sz 3) | 13.7 | 24.9 | 0.92 | demon, fear 5 |  |
| Summon Imps | Blood 1 (combat) | B1 | 1B | 5 x Imp (hp 8, prot 6, def 15, MR 13, sz 2) | 0.9 | 23.9 | 0.90 | demon, flying |  |
| Awaken Sleeper | Conjuration 5 (ritual) | G4 | 10G | 1 x Sleeper (hp 26, prot 18, def 19, MR 15, sz 4) | 8.8 | 11.8 | 0.88 | missile |  |
| Contact Forest Trolls | Conjuration 5 (ritual) | N3 | 10N | 11 x Forest Troll (hp 26, prot 13, def 9, MR 14, sz 5) | 8.8 | 56.9 | 0.88 | regeneration 10 | God (awake) |
| Summon Sea Lions | Conjuration 3 (ritual) | N2W1 | 10N | 16 x Leocampus (hp 27, prot 5, def 10, MR 6, sz 5) | 8.6 | 65.6 | 0.86 | animal, aquatic, undisciplined |  |
| Summon Leogryphs | Conjuration 4 (ritual) | N2 | 12N | 20 x Leogryph (hp 23, prot 5, def 10, MR 12, sz 4) | 10.2 | 74.0 | 0.85 | animal, undisciplined | God (awake) |
| Bind Serpent Fiends | Blood 4 (ritual) | B1 | 4B | 3 x Serpent Fiend (hp 22, prot 8, def 12, MR 16, sz 4) | 3.3 | 11.7 | 0.83 | demon, flying |  |
| Summon Killer Mantis | Conjuration 2 (ritual) | N2 | 5N | 11 x Killer Mantis (hp 18, prot 10, def 9, MR 5, sz 5) | 4.1 | 28.1 | 0.82 | animal, magicbeing, undisciplined | God (awake) |
| Plague of Locusts | Blood 7 (ritual, remote) | B5 | 88B | 11 x Demonic Locust (hp 29, prot 18, def 8, MR 16, sz 5) | 72.0 | 121.7 | 0.82 | demon, flying |  |
| Ritual of Five Gates | Blood 6 (ritual) | B5 | 33B | 1 x Fiend of Darkness (hp 30, prot 10, def 13, MR 17, sz 4); 1 x Devil (hp 35, prot 8, def 13, MR 17, sz 4); 1 x Frost Fiend (hp 25, prot 5, def 17, MR 17, sz 4); 1 x Storm Demon (hp 20, prot 5, def 14, MR 17, sz 4); 1 x Demon Knight (hp 20, prot 22, def 17, MR 15, sz 3) | 26.8 | 84.7 | 0.81 | cold 3, demon, ethereal, fear 5, flying, heat 3, missile |  |
| Earth Attack | Conjuration 8 (ritual, remote) | E5 | 5E | 1 x Earth Elemental (hp 70, prot 13, def 10, MR 16, sz 6) | 3.8 | 19.6 | 0.77 | amphibian, inanimate, magicbeing, trample | God (awake) |
| Summon Bog Beasts | Conjuration 3 (ritual) | N2W2 | 5N | 6 x Bog Beast (hp 32, prot 8, def 8, MR 7, sz 6) | 3.6 | 10.6 | 0.71 | animal, poisoncloud 5, undisciplined |  |
| Summon Fall Bears | Conjuration 5 (ritual) | E3 | 13E | 6 x Fall Bear (hp 53, prot 0, def 7, MR 15, sz 6) | 9.0 | 65.9 | 0.69 | animal, ethereal, magicbeing, regeneration 10 | God (awake) |
| Summon Fay Prince | Conjuration 6 (ritual) | G4N1 | 30G | 1 x Fay Prince (hp 18, prot 21, def 23, MR 16, sz 3) | 20.5 | 37.2 | 0.68 | N1 G2, awe 3 |  |
| Call Wraith Lord | Conjuration 8 (ritual) | D5 | 40D | 1 x Wraith Lord (hp 33, prot 18, def 16, MR 17, sz 3) | 27.2 | 32.9 | 0.68 | D3, amphibian, cold 3, ethereal, fear 8, undead |  |
| Summon Fay Archers | Conjuration 4 (ritual) | G2N1 | 10G | 6 x Fay Archer (hp 11, prot 9, def 16, MR 14, sz 3) | 6.8 | 60.8 | 0.68 | missile |  |
| Summon Unseelie Prince | Conjuration 6 (ritual) | G4W1 | 30G | 1 x Unseelie Prince (hp 18, prot 21, def 23, MR 16, sz 3) | 20.3 | 36.3 | 0.68 | D1 G2, cold 3 |  |
| Blood Rite | Blood 6 (ritual) | B2D2 | 11B | 1 x Vampire (hp 12, prot 0, def 11, MR 15, sz 3) | 7.3 | 14.9 | 0.66 | bluntres, flying, invulnerable 25, slashres, undead |  |
| Pride of Lions | Conjuration 3 (ritual) | N2 | 9N | 15 x Great Lion (hp 20, prot 4, def 10, MR 5, sz 4) | 5.8 | 43.9 | 0.64 | animal, undisciplined | God (awake) |
| Warrior Illusion | Evocation 2 (combat) | G1 | 0 | 1 x Warrior Illusion (hp 1, prot 0, def 10, MR 10, sz 3) | 0.6 | 1.4 | 0.59 | amphibian, ethereal, inanimate |  |
| Pale Riders | Enchantment 5 (ritual) | D3 | 10D | 25 x Longdead Horseman (hp 5, prot 8, def 14, MR 10, sz 3) | 5.6 | 62.4 | 0.56 | inanimate, pierceres, undead |  |
| Bind Ice Devil | Blood 6 (ritual, one of) | B3W3 | 88B | 1 x Ice Devil (hp 76, prot 15, def 14, MR 18, sz 6) | 47.9 | 88.3 | 0.54 | W3, cold 6, demon |  |
| Summon Amphiptere | Conjuration 3 (ritual) | A2N1 | 3A | 1 x Amphiptere (hp 45, prot 11, def 9, MR 14, sz 7) | 1.6 | 4.4 | 0.52 | animal, flying, missile, undisciplined |  |
| Summon Lesser Fire Elemental | Conjuration 3 (combat) | F1 | 1F | 1 x Fire Elemental (hp 25, prot 0, def 8, MR 13, sz 4) | 0.5 | 2.4 | 0.50 | ethereal, fireshield 10, heat 4, inanimate, magicbeing |  |
| Forces of Ice | Blood 9 (ritual) | B5W2 | 50B | 15 x Frost Fiend (hp 25, prot 5, def 17, MR 17, sz 4) | 24.6 | 209.4 | 0.49 | cold 3, demon, flying, missile |  |
| Bind Bone Fiends | Blood 2 (ritual) | B1D1 | 5B | 5 x Bone Fiend (hp 15, prot 0, def 13, MR 13, sz 4) | 2.5 | 28.9 | 0.49 | inanimate, pierceres, undead |  |
| Call of the Wild | Conjuration 3 (ritual, remote) | N4 | 9N | 40 x Wolf (hp 8, prot 2, def 10, MR 5, sz 3); 1 x Werewolf (hp 20, prot 6, def 11, MR 12, sz 4) | 4.4 | 60.5 | 0.49 | animal, invulnerable 15, regeneration 10, undisciplined | God (awake) |
| Ziz | Enchantment 6 (ritual) | D3A2 | 2D | 1 x Ziz (hp 78, prot 5, def 8, MR 13, sz 9) | 1.0 | 4.5 | 0.48 | cold 10, fear 5, flying, inanimate, undead |  |
| Infernal Disease | Blood 6 (ritual, remote) | B5 | 5B | 1 x Disease Demon (hp 30, prot 6, def 12, MR 17, sz 4) | 2.4 | 25.5 | 0.48 | amphibian, demon, ethereal, flying |  |
| Contact Sea Trolls | Conjuration 5 (ritual) | W3 | 10W | 11 x Sea Troll (hp 52, prot 8, def 10, MR 14, sz 6) | 4.4 | 43.9 | 0.44 | amphibian, regeneration 10 |  |
| Summon Cave Kobolds | Conjuration 4 (ritual) | G1E1 | 5G | 5 x Cave Kobold (hp 6, prot 11, def 10, MR 14, sz 2) | 2.2 | 10.3 | 0.44 | E1 G1, magicbeing |  |
| Vile Water | Enchantment 4 (ritual) | W2 | 2W | 1 x Gelatinous Cube (hp 50, prot 0, def 5, MR 13, sz 6) | 0.9 | 3.2 | 0.43 | amphibian, bluntres, magicbeing, pierceres, slashres, trample | Arch Theurg / Bartholomeus |
| Summon Calydonian Boar | Conjuration 7 (ritual) | N5 | 9N | 1 x Calydonian Boar (hp 58, prot 14, def 10, MR 14, sz 8) | 3.7 | 19.2 | 0.41 | animal, fear 5, heat 3, missile, trample, undisciplined | God (awake) |
| Summon Ogres | Conjuration 2 (ritual) | E1 | 7E | 5 x Ogre (hp 26, prot 13, def 9, MR 8, sz 5) | 2.9 | 14.7 | 0.41 |  | God (awake) |
| Summon Shade Beasts | Conjuration 4 (ritual) | D3 | 15D | 30 x Shade Beast (hp 12, prot 3, def 8, MR 12, sz 3) | 6.1 | 59.8 | 0.41 | ethereal, undead |  |
| Call of the Winds | Conjuration 3 (ritual, remote) | A2 | 8A | 51 x Black Hawk (hp 5, prot 0, def 12, MR 5, sz 3); 1 x Great Hawk (hp 15, prot 2, def 12, MR 5, sz 4) | 3.0 | 50.4 | 0.38 | animal, flying, undisciplined | Arch Theurg / Bartholomeus |
| Terracotta Army | Enchantment 4 (ritual) | F1E1 | 9F | 15 x Terracotta Soldier (hp 7, prot 10, def 9, MR 12, sz 3) | 3.3 | 21.1 | 0.37 | inanimate, magicbeing, pierceres, slashres |  |
| Summon Swamp Drake | Conjuration 4 (ritual) | N2W1 | 5N | 1 x Swamp Drake (hp 44, prot 14, def 7, MR 13, sz 6) | 1.8 | 4.5 | 0.37 | animal, undisciplined |  |
| Summon Cave Drake | Conjuration 4 (ritual) | E2 | 4E | 1 x Cave Drake (hp 58, prot 22, def 6, MR 12, sz 6) | 1.4 | 4.3 | 0.36 | animal, undisciplined | God (awake) |
| Summon Crocodiles | Conjuration 1 (ritual) | N1W1 | 4N | 10 x Crocodile (hp 23, prot 12, def 6, MR 5, sz 5) | 1.4 | 9.4 | 0.36 | animal, undisciplined |  |
| Forest Troll Tribe | Conjuration 6 (ritual) | N3 | 37N | 1 x Troll Shaman (hp 26, prot 13, def 11, MR 16, sz 5); 15 x Forest Troll (hp 26, prot 13, def 9, MR 14, sz 5) | 13.3 | 87.6 | 0.36 | D1 N1 U1, regeneration 10 | God (awake) |
| Summon Sea Dogs | Conjuration 1 (ritual) | N1W1 | 2N | 10 x Sea Dog (hp 14, prot 7, def 10, MR 6, sz 3) | 0.7 | 10.3 | 0.36 | amphibian, animal, undisciplined |  |
| Crusher Construction | Construction 4 (ritual) | E3 | 10E | 1 x Crusher (hp 110, prot 24, def 7, MR 12, sz 9) | 3.5 | 9.3 | 0.35 | inanimate, magicbeing, pierceres, slashres | God (awake) |
| Awaken Vine Ogres | Conjuration 4 (ritual) | N3 | 3N | 3 x Vine Ogre (hp 55, prot 9, def 5, MR 5, sz 6) | 1.0 | 14.5 | 0.34 | bluntres, magicbeing, pierceres | God (awake) |
| Harvester of Sorrows | Conjuration 7 (ritual) | D4 | 20D | 1 x Harvester of Sorrows (hp 66, prot 0, def 15, MR 18, sz 8) | 6.7 | 22.8 | 0.33 | ethereal, fear 15, flying, undead |  |
| Awaken Dark Vines | Blood 5 (ritual) | B1N3 | 12B | 2 x Dark Vines (hp 126, prot 9, def 5, MR 15, sz 8) | 3.8 | 31.5 | 0.32 | bluntres, magicbeing, pierceres |  |
| Claymen | Enchantment 3 (ritual) | W1E1 | 7W | 10 x Clayman (hp 15, prot 6, def 9, MR 10, sz 3) | 2.2 | 20.8 | 0.31 | bluntres, inanimate, magicbeing, pierceres |  |
| Summon Cave Cows | Conjuration 3 (ritual) | W2E2 | 3W | 11 x Cave Cow (hp 32, prot 4, def 8, MR 7, sz 6) | 0.9 | 6.7 | 0.31 | animal, missile, undisciplined |  |
| Summon Yetis | Conjuration 3 (ritual) | W2A1 | 8W | 6 x Yeti (hp 46, prot 8, def 8, MR 13, sz 6) | 2.5 | 11.5 | 0.31 | cold 3, missile | Arch Theurg / Bartholomeus |
| Pack of Wolves | Conjuration 2 (ritual) | N1 | 2N | 15 x Wolf (hp 8, prot 2, def 10, MR 5, sz 3) | 0.6 | 7.6 | 0.29 | animal, undisciplined | God (awake) |
| Summon Lesser Water Elemental | Conjuration 3 (combat) | W1 | 1W | 1 x Water Elemental (hp 27, prot 0, def 10, MR 13, sz 4) | 0.3 | 1.5 | 0.28 | amphibian, bluntres, inanimate, magicbeing, pierceres, slashres | Theurg |
| Horde from Hell | Blood 5 (ritual, remote) | B4 | 44B | 40 x Imp (hp 8, prot 6, def 15, MR 13, sz 2); 1 x Devil (hp 35, prot 8, def 13, MR 17, sz 4) | 11.8 | 209.9 | 0.27 | demon, flying, heat 3 |  |
| Revive King | Enchantment 2 (ritual) | D1 | 3D | 1 x Mound King (hp 7, prot 12, def 15, MR 14, sz 3) | 0.8 | 9.4 | 0.26 | inanimate, pierceres, undead |  |
| Call Ancient Presence | Conjuration 9 (ritual) | W5N4 | 15W | 1 x Ancient Presence (hp 197, prot 6, def 7, MR 18, sz 10) | 3.6 | 17.4 | 0.24 | W1 N1 U2, bluntres, fear 10, magicbeing, pierceres, undead |  |
| Bind Frost Fiend | Blood 3 (ritual) | B2W2 | 7B | 1 x Frost Fiend (hp 25, prot 5, def 17, MR 17, sz 4) | 1.6 | 14.0 | 0.23 | cold 3, demon, flying, missile |  |
| Shadow Servant | Conjuration 1 (ritual) | D2 | 5D | 1 x Shadow Servant (hp 18, prot 0, def 11, MR 11, sz 3) | 1.2 | 5.3 | 0.23 | amphibian, ethereal, undead |  |
| Behemoth | Enchantment 4 (ritual) | D3 | 7D | 1 x Behemoth (hp 104, prot 7, def 6, MR 13, sz 9) | 1.6 | 6.0 | 0.22 | fear 5, inanimate, trample, undead |  |
| King of Elemental Earth | Conjuration 8 (ritual, one of) | E5 | 50E | 1 x King of Deeper Earth (hp 130, prot 17, def 8, MR 18, sz 9) | 10.9 | 22.5 | 0.22 | E5, magicbeing, regeneration 10 | God (awake) |
| Bind Fiery Imps | Blood 1 (ritual) | B1F1 | 5B | 5 x Fiery Imp (hp 7, prot 5, def 12, MR 13, sz 2) | 1.0 | 8.3 | 0.19 | demon, fireshield 6, missile |  |
| Awaken Algae Men | Conjuration 2 (ritual) | N1 | 1N | 4 x Algae Man (hp 12, prot 14, def 6, MR 5, sz 3) | 0.2 | 5.2 | 0.17 | amphibian, bluntres, magicbeing, pierceres | God (awake) |
| Summon Unseelie Archers | Conjuration 4 (ritual) | G2W1 | 10G | 6 x Unseelie Archer (hp 11, prot 9, def 13, MR 14, sz 3) | 1.6 | 15.5 | 0.16 | missile |  |
| Summon Spectre | Conjuration 6 (ritual) | D3 | 22D | 1 x Spectral Mage (hp 25, prot 0, def 16, MR 16, sz 3) | 3.4 | 14.1 | 0.16 | D1 U2, cold 3, ethereal, fear 6, undead |  |
| Heavenly Choir | Conjuration 9 (ritual) | S7F2 | 144S | 1 x Seraph (hp 77, prot 0, def 14, MR 18, sz 8); 9 x Angel of the Heavenly Choir (hp 14, prot 0, def 12, MR 16, sz 5); 3 x Harbinger of the Choir (hp 35, prot 0, def 11, MR 18, sz 6) | 20.7 | 111.3 | 0.14 | F4 A4 S4 H4, H2, awe 5, awe 7, fireshield 16, flying, holy, invulnerable 15, invulnerable 20, invulnerable 30, magicbeing |  |
| Curse of Blood | Blood 8 (ritual) | B3D4 | 96B | 1 x Vampire Lord (hp 15, prot 0, def 13, MR 17, sz 3) | 13.5 | 21.5 | 0.14 | D3 B3, bluntres, flying, invulnerable 25, slashres, undead |  |
| Bind Arch Devil | Blood 7 (ritual, one of) | B4F2 | 99B | 1 x Arch Devil (hp 62, prot 12, def 14, MR 18, sz 7) | 13.3 | 51.4 | 0.13 | F4, demon, flying, heat 7 |  |
| Queen of Elemental Air | Conjuration 8 (ritual, one of) | A5 | 50A | 1 x Queen of Storms (hp 45, prot 0, def 13, MR 18, sz 8) | 6.2 | 25.5 | 0.12 | A5, ethereal, flying, magicbeing |  |
| Angelic Choir | Conjuration 6 (ritual) | S3 | 15S | 3 x Angel of the Heavenly Choir (hp 14, prot 0, def 12, MR 16, sz 5) | 1.8 | 20.2 | 0.12 | H2, awe 5, flying, holy, invulnerable 15, magicbeing | Arch Theurg / Bartholomeus |
| School of Sharks | Conjuration 4 (combat) | W2 | 1W | 10 x Small Shark (hp 2, prot 0, def 12, MR 4, sz 1) | 0.1 | 2.8 | 0.11 | animal, aquatic, undisciplined | Bartholomeus (hero) |
| Contact Lamia Queen | Conjuration 6 (ritual) | N5D2 | 25N | 1 x Lamia Queen (hp 15, prot 6, def 14, MR 17, sz 3) | 2.5 | 15.4 | 0.10 | D2 N1 U2, regeneration 50 |  |
| Construct Mandragora | Construction 4 (ritual) | N2D1 | 10N | 10 x Mandragora (hp 25, prot 5, def 9, MR 14, sz 3) | 0.9 | 16.0 | 0.09 | inanimate, magicbeing, pierceres, undead |  |
| Awaken Vine Men | Conjuration 2 (ritual) | N1 | 1N | 4 x Vine Man (hp 17, prot 7, def 6, MR 5, sz 3) | 0.1 | 2.5 | 0.09 | bluntres, magicbeing, pierceres | God (awake) |
| Summon Spine Frog | Conjuration 4 (ritual) | N2W1 | 1N | 1 x Spine Frog (hp 41, prot 7, def 8, MR 8, sz 6) | 0.1 | 0.7 | 0.09 | animal, undisciplined |  |
| Queen of Elemental Water | Conjuration 8 (ritual, one of) | W5 | 50W | 1 x Queen of the Sea (hp 65, prot 0, def 15, MR 18, sz 8) | 4.2 | 17.8 | 0.08 | W5, aquatic, bluntres, magicbeing, pierceres, slashres |  |
| Summon Flame Jellies | Conjuration 4 (ritual) | F2 | 6F | 10 x Flame Jelly (hp 25, prot 0, def 5, MR 20, sz 6) | 0.4 | 2.5 | 0.07 | animal, aquatic, bluntres, magicbeing, pierceres |  |
| Summon Mound Fiend | Conjuration 7 (ritual) | D3 | 28D | 1 x Mound Fiend (hp 20, prot 0, def 15, MR 15, sz 3) | 2.1 | 12.1 | 0.07 | D3 H2, cold 3, ethereal, fear 8, holy, undead |  |
| Contact Harbinger | Conjuration 6 (ritual) | S4 | 25S | 1 x Harbinger (hp 35, prot 0, def 11, MR 18, sz 6) | 1.8 | 9.9 | 0.07 | A3 H2, awe 5, flying, holy, invulnerable 20, magicbeing | Arch Theurg + booster |
| Infernal Tempest | Blood 9 (ritual) | B5A2 | 50B | 12 x Storm Demon (hp 20, prot 5, def 14, MR 17, sz 4) | 3.3 | 68.9 | 0.07 | demon, ethereal, flying, missile |  |
| Summon Storm Drake | Conjuration 4 (ritual) | A2 | 5A | 1 x Storm Drake (hp 25, prot 10, def 11, MR 13, sz 6) | 0.3 | 2.7 | 0.06 | animal, flying, undisciplined | Arch Theurg / Bartholomeus |
| King of Elemental Fire | Conjuration 8 (ritual, one of) | F5 | 50F | 1 x King of Flames (hp 54, prot 0, def 8, MR 18, sz 8) | 3.1 | 10.5 | 0.06 | F5, ethereal, fireshield 20, heat 15, magicbeing |  |
| Bind Demon Lord | Blood 9 (ritual, one of) | B8 | 150B | 1 x Lord of the Plague Wind (hp 88, prot 10, def 15, MR 18, sz 9) | 9.0 | 52.4 | 0.06 | A5 D3 B4, demon, fear 13, flying |  |
| Father Illearth | Blood 7 (ritual, one of) | B3E4 | 105B | 1 x Father Illearth (hp 130, prot 13, def 8, MR 18, sz 8) | 6.2 | 22.9 | 0.06 | E4 B3, fear 5, magicbeing, regeneration 15 |  |
| King of Banefires | Conjuration 8 (ritual, one of) | D3F4 | 50D | 1 x King of Banefires (hp 54, prot 0, def 8, MR 18, sz 9) | 2.9 | 10.8 | 0.06 | F4 D3, ethereal, fear 8, heat 9, magicbeing, undead |  |
| Bind Heliophagus | Blood 8 (ritual, one of) | B5 | 111B | 1 x Heliophagus (hp 55, prot 10, def 14, MR 18, sz 7) | 5.9 | 28.4 | 0.05 | B4, demon, fear 5, flying |  |
| Summon Hawk | Conjuration 2 (combat) | A1 | 0 | 1 x Black Hawk (hp 5, prot 0, def 12, MR 5, sz 3) | 0.1 | 0.9 | 0.05 | animal, flying, undisciplined | Theurg |
| Summon Ice Drake | Conjuration 4 (ritual) | W2 | 7W | 1 x Ice Drake (hp 41, prot 13, def 7, MR 13, sz 6) | 0.4 | 1.9 | 0.05 | animal, missile, undisciplined | Arch Theurg / Bartholomeus |
| Summon Flame Spirit | Conjuration 6 (ritual) | F3 | 30F | 1 x Flame Spirit (hp 15, prot 0, def 12, MR 15, sz 3) | 1.5 | 6.8 | 0.05 | F3, ethereal, fireshield 13, heat 7, magicbeing |  |
| Call the Eater of the Dead | Conjuration 8 (ritual, one of) | S4D4 | 50S | 1 x Eater of the Dead (hp 180, prot 4, def 4, MR 18, sz 10) | 2.2 | 6.1 | 0.04 | bluntres, fear 5, trample, undead |  |
| Bind Shadow Imp | Blood 1 (ritual) | B1 | 4B | 1 x Shadow Imp (hp 7, prot 5, def 13, MR 13, sz 2) | 0.2 | 1.7 | 0.04 | demon |  |
| Poison Golem | Construction 8 (ritual) | D4E2 | 35D | 1 x Poison Golem (hp 85, prot 18, def 7, MR 18, sz 7) | 1.3 | 6.3 | 0.04 | inanimate, magicbeing |  |
| Summon Catoblepas | Conjuration 7 (ritual) | W3D2 | 12W | 1 x Catoblepas (hp 75, prot 8, def 6, MR 16, sz 9) | 0.4 | 2.0 | 0.03 | fear 10, missile, poisoncloud 5 |  |
| Summon Bluecap | Conjuration 5 (ritual) | G2E1 | 20G | 1 x Bluecap (hp 7, prot 11, def 10, MR 15, sz 2) | 0.6 | 2.8 | 0.03 | E2 G1, magicbeing |  |
| Bind Storm Demon | Blood 4 (ritual) | B2A2 | 10B | 1 x Storm Demon (hp 20, prot 5, def 14, MR 17, sz 4) | 0.3 | 5.7 | 0.03 | demon, ethereal, flying, missile |  |
| Summon Fire Drake | Conjuration 4 (ritual) | F2 | 6F | 1 x Fire Drake (hp 28, prot 10, def 7, MR 13, sz 5) | 0.2 | 0.9 | 0.03 | animal, missile, undisciplined |  |
| Construct Manikin | Construction 2 (ritual) | N1D1 | 7N | 16 x Manikin (hp 12, prot 0, def 7, MR 12, sz 3) | 0.2 | 2.9 | 0.02 | inanimate, magicbeing, pierceres, undead |  |
| Reanimate Archers | Enchantment 6 (ritual) | D2F1 | 5D | 10 x Longdead Archer (hp 5, prot 0, def 8, MR 9, sz 3) | 0.1 | 1.8 | 0.02 | inanimate, missile, pierceres, undead |  |
| Awaken Ivy King | Conjuration 7 (ritual) | N4 | 30N | 1 x Ivy King (hp 63, prot 7, def 7, MR 16, sz 6) | 0.5 | 6.6 | 0.02 | N3, bluntres, magicbeing, pierceres | God (awake) |
| Awaken Hamadryad | Enchantment 5 (ritual) | N4 | 25N | 1 x Hamadryad (hp 110, prot 18, def 0, MR 18, sz 10) | 0.4 | 5.9 | 0.02 | N3, bluntres, magicbeing, pierceres | God (awake) |
| Wooden Construction | Construction 4 (ritual) | N3 | 6N | 4 x Lumber Construct (hp 49, prot 17, def 1, MR 12, sz 7) | 0.1 | 1.0 | 0.02 | bluntres, inanimate, magicbeing, pierceres | God (awake) |
| Corpse Man Construction | Construction 2 (ritual) | A1D1 | 1A | 1 x Corpse Construct (hp 25, prot 0, def 5, MR 4, sz 4) | 0.0 | 0.2 | 0.01 | inanimate, pierceres, undead |  |
| Bind Incubus | Blood 5 (ritual) | B4G1 | 66B | 1 x Incubus (hp 35, prot 0, def 12, MR 17, sz 4) | 0.9 | 3.5 | 0.01 | G2, demon, flying |  |
| Bind Succubus | Blood 5 (ritual) | B4G1 | 66B | 1 x Succubus (hp 30, prot 0, def 13, MR 17, sz 4) | 0.7 | 3.8 | 0.01 | G2, demon, flying |  |
| Golem Construction | Construction 6 (ritual) | S3E2 | 35S | 1 x Golem (hp 85, prot 6, def 7, MR 18, sz 7) | 0.3 | 2.0 | 0.01 | S2, inanimate, magicbeing, pierceres, slashres |  |
| Call the Worm That Walks | Thaumaturgy 8 (ritual) | N5 | 30N | 1 x Worm Mage (hp 10, prot 0, def 10, MR 18, sz 3) | 0.2 | 6.2 | 0.01 | N3 U0, amphibian, invulnerable 15, pierceres, regeneration 10, slashres | God (awake) |
| Contact Lar | Conjuration 5 (ritual) | N1 | 16N | 1 x Lar (hp 14, prot 0, def 11, MR 16, sz 4) | 0.1 | 1.5 | 0.01 | W1 E1 N2, ethereal, holy, magicbeing | God (awake) |
| Contact Naiad | Conjuration 5 (ritual) | W3N1 | 35W | 1 x Naiad (hp 10, prot 0, def 9, MR 18, sz 3) | 0.1 | 2.3 | 0.00 | W3 N3, amphibian, awe 6 |  |
| Summon Water Kobold | Conjuration 4 (ritual) | G1W1 | 12G | 1 x Water Kobold (hp 5, prot 0, def 13, MR 15, sz 2) | 0.0 | 0.4 | 0.00 | W1 G1, amphibian, magicbeing |  |
| Create Revenant | Enchantment 3 (ritual) | D2 | 9D | 1 x Revenant (hp 15, prot 0, def 7, MR 14, sz 3) | 0.0 | 0.2 | 0.00 | D1, inanimate, pierceres, undead |  |
| Streams from Hades | Conjuration 6 (ritual) | W4D1 | 40W | 1 x Kokythiad (hp 10, prot 0, def 9, MR 18, sz 3) | 0.0 | 0.6 | 0.00 | W3 D3, amphibian, fear 8, invulnerable 15 |  |
| Spirit Mastery | Conjuration 5 (ritual) | D1 | 4D | 25 x Dispossessed Spirit (hp 1, prot 0, def 8, MR 11, sz 2) | 0.0 | 0.0 | 0.00 | amphibian, ethereal, undead, undisciplined |  |
| Corpse Candle | Conjuration 5 (combat) | D1F1 | 1D | 3 x Corpse Candle (hp 4, prot 0, def 19, MR 13, sz 1) | 0.0 | 0.0 | 0.00 | ethereal, magicbeing |  |
| Summon Bishop Fish | Conjuration 6 (ritual) | W3 | 15W | 1 x Bishop Fish (hp 17, prot 3, def 7, MR 16, sz 3) | 0.0 | 0.0 | 0.00 | H3, aquatic, holy |  |
| Summon Sprites | Conjuration 6 (combat) | G1N1 | 1G | 6 x Sprite (hp 2, prot 0, def 20, MR 14, sz 1) | 0.0 | 0.0 | 0.00 | flying, magicbeing |  |
| Summon Gnome | Conjuration 6 (ritual) | G3E2 | 35G | 1 x Gnome (hp 6, prot 0, def 7, MR 16, sz 2) | 0.0 | 0.0 | 0.00 | E2 N2 G2 |  |
| Iron Gryphon | Construction 6 (ritual) | F3E1 | 6F | 1 x Iron Gryphon (hp 50, prot 24, def 0, MR 14, sz 5) | 0.0 | 0.0 | 0.00 | bluntres, inanimate, magicbeing, missile, pierceres, slashres |  |
| Watcher | Enchantment 5 (ritual) | A3E1 | 5A | 1 x Watcher (hp 75, prot 20, def 0, MR 14, sz 5) | 0.0 | 0.0 | 0.00 | inanimate, magicbeing, missile, pierceres, slashres |  |
| Telestic Animation | Thaumaturgy 4 (ritual) | S2 | 5S | 1 x Telestic Animate (hp 40, prot 12, def 0, MR 18, sz 5) | 0.0 | 0.0 | 0.00 | H2, amphibian, bluntres, holy, inanimate, magicbeing, pierceres | Theurg |
