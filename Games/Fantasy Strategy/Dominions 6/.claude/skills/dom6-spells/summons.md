# Summoning spells, ranked by their summons (first pass, 2026-10-28, for the user's review)

All 201 researchable summoning spells of every school (generic ones plus Pythium's own), ranked by
how much fighting their summons do for the gems. The per-spell numbers are in `summons-table.md`.

## How the ranking works

The measure is **enemy men killed in melee before the summons die**, added up over everything one cast brings.

**Rate:**
- Each summon's kills a round count all its melee weapons.
- Trample counts when the summon is bigger than the foe (manual: Defence vs 3d6, else 7 + size AP damage).

**Lifetime:** the rounds it lives while 1.5 (small) to 4 (huge) enemies hit it. Awe, invulnerability, ethereal, slash/pierce/blunt resistance and regeneration count.

**Caps:** fatigue (100 / encumbrance rounds; undead and constructs don't tire) and 50 rounds.

**Foes:**
- **Heavy Infantry with sword and shield** (prot 13, the Murias type) is the main test.
- Militia is the soft test.
- Baseline: HI vs HI comes out 0.5, our Alae 0.4.

**Gems:** combat summons cost 1-2 gems a cast and last one battle. Rituals are permanent units. Compare within each group.

**Not modelled, so judge these by hand:**
- morale: undisciplined animals rout, mindless and undead never do;
- enemy missiles, spells and magic weapons. Ethereal and high-defence summons are the model's best case: they die fast to magic;
- missile summons: Harbinger's horn, Manticores, Fay Archers;
- a summoned commander's magic and priest paths;
- leadership: magic beings need magic leadership, undead need undead leadership.

## Shield correction (later on 2026-10-28)

Rerun after fixing the shield parser (`evocations.md` explains it). The enemy's shields now give shield hits in melee as the manual describes, and summons with shields no longer get a phantom shield weapon. `summons-table.md` has the new numbers. The tiers below stand; the main shifts:
- **Contact Draconians:** 51 → **80** HI kills (2.6 → **4.0** a gem). Pythium's best ritual summon, if we get an air booster.
- **Spirits of the Wood:** 63 → 137 (17 a gem).
- **Contact Angel of the Host:** 8.5 → **10.3** (1.2 → 1.5 a gem). **Angelic Host:** 87 → 104.
- **Summon Water Elemental:** 7.8 → 10.7. **Wyverns:** 1.3 → 1.8 a gem. **Contact Trolls:** 1.3 → 2.1 a gem. **Legion of Wights:** 176 → 205.
- Basically unchanged: Wisps, Living Clouds, Air Elementals, Gryphons, Iron Pigs.

## The ranking

Kills are vs heavy infantry → vs militia. **(P)** = Pythium can cast it, with the caster:
- AT = Arch Theurg or Bartholomeus (A2 W2 S3);
- AT+1 = with a path booster;
- Comm = communion master (combat spells only; communion doesn't work for rituals);
- God = Hortus once awake (E5 N5).

### Battle summons (cast in combat, last one battle)

| Tier | Spell | Path, school | Per cast | Kills HI → militia | Why |
|---|---|---|---|---|---|
| S | Will o' the Wisp | F1 Conj5 | 2 wisps, 1F | 24 → 40 | Def 20, ethereal, hp 3: mundane soldiers can't touch them. Archers, spells and magic weapons do. |
| S | **Living Clouds (P, Comm: A4)** | A4 Conj7 | 4 Air Elementals, 2A | 18 → 82 | Flying, ethereal, trample, big hp: **the best army summon we can reach**. Bartholomeus + 5 Communicants. |
| S | Conjure Phantasmal Beast / Knight / Warriors | G2-3 Conj4-7 | 1-2, 1G | 6-11 | Glamour illusions, ethereal. |
| A | **Summon Air Elemental (P, Comm: A3)** | A3 Conj5 | 1, 1A | 6.6 → 33 | A Theurg master with 4 slaves can cast it. Flies, tramples, ethereal. |
| A | **Summon Water Elemental (P, Comm: W3)** / **Living Water (P, Comm: W4)** | W3-4 Conj5-7 | 1 / 4 | 8 → 38 / 12 → 63 | Huge hp, resists every weapon type; slow and not flying. |
| A | Summon Earth Elemental / **Living Earth (P, God)** | E3-4 Conj5-7 | 1 / 4 | 5 → 28 / 14 → 73 | The god's battle summon once awake. |
| B | **Summon Lesser Air Elemental (P, Theurg: A1)** | A1 Conj3 | 1, 1A | 2.3 → 10 | **Any Theurg at Conjuration 3**: an ethereal flying trampler for a gem. That's 5× an Alae soldier's kills. |
| B | Nest of Asps / Salamanders, Phantasmal Wolves, Summon Imps, Illearth | | | 1-4 | Chaff or one decent body. |
| C | **Summon Lesser Water Elemental (P, Th)**, Lesser Fire, **School of Sharks (P)**, **Summon Hawk (P)**, Corpse Candle, Sprites | | | ≤0.5 | Chaff only: they soak arrows and a round of attacks. Sharks only underwater. |

### Permanent summons (rituals)

| Tier | Spell | Path, school, gems | Brings | Kills HI → militia (per gem) | Why |
|---|---|---|---|---|---|
| S | Legion of Wights / Revive Wights | D5 / D2, 20D | 17 / 5 Wights | 176 / 52 (8.8 / 2.6) | Prot 18 undead, tireless. |
| S | Ghost Riders, Army of the Dead | D5 Conj9 / Ench9 | 75-100 undead | 58-79 → 270-990 (8-12) | Remote, temporary or late; the late-game Death answer. |
| S | Spirits of the Wood **(P, God: N3)** | N3 Conj5, 8N | 15 ethereal, awe, regenerating spirits | 63 → 89 (7.9) | **The god's best summon per gem.** Mundane troops barely hurt them. |
| S | Iron Pigs **(P, God: E3N1)** | Alt6, 9E | 11 trampling sacred boars | 68 → 218 (7.5) | |
| A | **Contact Draconians (P, AT+1: A3)** | A3 Conj5, 20A | 30 Draconians + chief, all flying | 51 → 264 (2.6) | A flying army. With an air booster this is **Pythium's best ritual summon**. |
| A | Fay / Unseelie Footfolk and Knights | G2-3 Conj4-5, 12-15G | 3-6 heavy fay | 48-55 (3.2-4.6) | Glamour; forest only. |
| A | Kithaironic Lion **(P, God)**, Enliven Statues **(P, God)**, Clockwork Horrors / Soldiers, Mechanical Men **(P, God: Construction)** | E2-3, N3 | | 11-68 (2.1-4.1) | Earth/Construction bodies for the god once awake. |
| A | Infernal Crusade, Demon Knights, Ether Gate / Warriors | B, S3D1+ | heavy elite | 2-2.6 a gem | Not our paths (Ether needs D). |
| B | **Contact Angel of the Host (P, AT: S3)** | S3 Conj5, 7S | 1 sacred flying Angel (prot 23, awe 5, invulnerable 15) | 8.5 → 11 (1.2) | Not the most kills per gem. It flies over the line and **kills mages and archers**, ignores mundane spears, and is sacred. **The first summon to research for the mage-killing goal.** |
| B | **Angelic Host (P, AT+2: S5)**, **Heavenly Wrath (P, AT with fire random: S3F1)** | Conj7, 35-50S | 7 Angels + Arch Angel / 1 Angel of Fury | 87 / 46 (1.3-1.7) | The late astral army. |
| B | **Summon Gryphons (P, AT: A2)** | A2 Conj4, 9A | 11 flying Gryphons | 12 → 79 (1.4) | Cheap flying flankers to **run down archers and mages**. Undisciplined, so they rout. |
| B | **Summon Spring Hawks (P, AT+1)**, **Great Eagles (P, AT+1)**, **Summon Wyverns (P, AT)** | A2-3 | flyers | 1-2 a gem | Flank and harass. |
| B | Contact Trolls **(P, God)**, Manticores **(P, God)**, Tarrasque **(P, God)**, Troll King's Court **(P, God)** | E3-4, N2-5 | | 1.3-1.7 a gem | |
| B | Iron Dragon, Juggernaut, Siege Golem, Asp Turtle, Leviathan | E/S5/W/D | one big trampler | 13-26 (0.9-2.7) | Juggernaut needs S5, which is AT+2. |
| C | **Sea Serpent (P)**, **Krakens (P, AT+1)**, **Winter Wolves (P, AT+1)**, **Yetis (P)**, **Call of the Winds (P)**, **Storm / Ice Drakes (P)**, Lions, Wolves, Leogryphs, Ogres, Shades and most beasts | | | ≤1 a gem | Bodies that rout or die to heavy infantry. Krakens and Sea Serpent only fight at sea. |
| — | Commanders: **Harbinger (P, AT+1: S4)**, **Angelic Choir (P, AT)**, **Heavenly Choir (S7)**, Lar **(P, God)**, the elemental Kings and Queens, Fay Prince, Lamia Queen, Naiad, Bishop Fish, Gnome, Spectre | | mages, priests, thugs | — | Judge them by their magic, not melee. Harbinger: A3 H2 priest-mage, invulnerable 20, horn blast; a strong flying thug with a buff. Angelic Choir: 3 H2 priests with awe. |

## What this means for Pythium

Our research has Conjuration 1 queued; nothing here is reachable yet. In order of value for the goals:
- win big battles;
- kill mage corps without losing anything important.

1. **Conjuration 3: Summon Lesser Air Elemental** for any Theurg. One air gem buys an ethereal flying trampler; script one cast before the buffs when air gems allow. It's cheap research.
2. **Conjuration 4: Summon Gryphons** (Arch Theurg or Bartholomeus, 9 air gems). Eleven flyers that dive the enemy's mages and archers.
3. **Conjuration 5:**
   - **Contact Angel of the Host** (7 astral gems each), our sacred flying mage-killer;
   - **Summon Air Elemental** (communion);
   - **Contact Draconians** if we find an air booster.
4. **Conjuration 7:** Living Clouds for Bartholomeus + 5; Angelic Host and Heavenly Wrath later.
5. **The awake god:** Spirits of the Wood (8 nature gems, in a forest), Iron Pigs (Alteration 6), Living Earth, and Clockwork Soldiers or Horrors once Construction 2-4 is in.

Which gems we earn decides between these. The next step is to count our air, astral, water, earth and nature income (Statistics or the Magic screen) before choosing. Open questions for battle: how the AI targets flyers, and whether Angels and Gryphons reach mages before they cast.
