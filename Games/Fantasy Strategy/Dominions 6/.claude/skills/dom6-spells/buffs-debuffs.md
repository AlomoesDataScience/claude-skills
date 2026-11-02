# Buffs and debuffs, ranked (first pass, 2026-10-28, for the user's review)

This page ranks every researchable buff and debuff combat spell, grouped into **families**: the same effect sold
as a self spell, a small group, a whole-army spell and a battlefield spell. Each family is ranked twice,
once for **melee troops** and once for **missile troops**. The judgement is about fighting what we have
met so far. The full spell list is `spells.py list`; what Pythium can cast is `castable.md`.

**Enemies met (turns 1-7):** independents only.
- Militia; Heavy Infantry with spear or sword and a shield.
- Light Infantry; Barbarians with two-handed swords and mauls, no shields.
- Jaguar Tribe warriors and slingers, plus a priest and animated bushes.
- Bear Tribe spear-javelin warriors.
- Cataphracts, light cavalry and mounted commanders; Archers (Dragon Ridge).

We have met **no enemy mages** worth the name yet, and no AI nation yet.

**Our troops:**
- Alae Legionnaire: spear, javelin ×2, tower shield (parry 7), prot 14.
- Velite: javelin ×2, spear, tower shield, prot 7.
- Jaguar Warriors and Slingers (indie); Foul Spawn (mercenaries).
- Indie archers later.
- Mages: Theurgs (hp 9, prot 1); Bartholomeus (hp 8).

## How a spell earns its rank

1. **Effect size.** This comes from the calculator: `spells.py rank`, tables below.
2. **Coverage per cast.** A mage casts one spell a round, and fights are decided in 5-10 rounds; Murias routed in round 7. An area of `1` is one square, which is 3 humans (a square holds 10 size points). So:
   - A 1-square buff needs **10 casts** to cover a 30-man squad.
   - `3+1/lvl` covers 5-6 squares (15-18 men) at level 2-3.
   - `20+1/lvl` covers about 22 squares, the whole army.
   - `100% of battlefield` covers everything.
   - **Coverage multiplies the effect.**
3. **Range against where the caster stands.** With *Stay behind troops* the mages stand behind the rear squad, so the front line is several squares away.
   - Range 5 (Strength of Giants) or 10 (Body Ethereal, Gift of Flight, Trueshot) barely reaches the front from there.
   - Range 15 (most group buffs) usually does.
   - Debuffs at range 25-50 reach the enemy front easily.
4. **Magic resistance** (spells marked MR). The spell lands if 11 + DRN + extra levels/2 ≥ MR + DRN. Simulated odds:

   | Target MR | 10 (troops) | 13 | 15 (mages) | 18 |
   |---|---|---|---|---|
   | No extra levels | 62% | 38% | 24% | 11% |
   | +2 extra levels | 70% | 46% | 30% | 14% |

   MR debuffs work on troops and badly on mages. "MR easily" spells are 4 worse.
5. **Precision.** Debuffs aimed at a square use the caster's precision (10) plus the spell's. Against a packed block a near miss still lands on someone; against spread-out targets it doesn't.
6. **Cost.** Fatigue per cast: the fatigue cost × 1/(1 + levels above the requirement), plus 3 encumbrance. A Theurg gets 4-5 casts of 20-fatigue spells. Spells costing 100 or more fatigue cost gems. Communion slaves share the master's fatigue.
7. **Duration.** Nearly all buffs and debuffs last the whole battle. Mistform and Twist Fate break. Slime fades faster on targets with high MR.

## The calculator's numbers

Melee is one Alae Legionnaire against one enemy, with the buff on our side or the debuff on theirs. **Rounds to kill a fresh unit** counts every attack, including misses.

Checked against the Murias review, the model's damage per hit is 1-2× the measured value: 2.6 vs 1.4 on sword Heavy Infantry. So read the tables for comparing spells, not as absolute numbers.

**Not modelled:**
- fatigue, harassment, repel, reach, flanking;
- morale and routs, which decide most indie fights;
- resistances, and the AI picking targets.

### Offence: rounds for one Alae to kill one enemy (lower is better)

| Buff | Militia | HI spear | HI sword | Barbarian | Jaguar W | Bear W | Cataphract | Archer | avg |
|---|---|---|---|---|---|---|---|---|---|
| none | 5.8 | 10.5 | 21.9 | 8.3 | 6.6 | 5.1 | 47.1 | 8.9 | 0 |
| Slime / Slow on them | 4.0 | 7.2 | 13.4 | 5.7 | 4.6 | 4.1 | 28.3 | 7.5 | −30% |
| Battle Fury (att +2) | 4.0 | 7.4 | 13.6 | 5.6 | 4.7 | 4.2 | 29.2 | 7.5 | −29% |
| Strength of Giants (str +4) | 4.5 | 7.3 | 12.1 | 6.0 | 5.1 | 3.8 | 23.8 | 4.7 | −34% |
| Weapons of Sharpness (AP) | 4.9 | 7.2 | 10.0 | 6.0 | 5.5 | 3.9 | 17.7 | 3.8 | −36% |
| Quickness (two actions) | 3.0 | 5.5 | 10.7 | 4.1 | 3.4 | 2.6 | 24.3 | 4.5 | −49% |
| Quagmire (both −1/−1) | 5.7 | 11.0 | 21.3 | 8.2 | 6.7 | 5.2 | 47.6 | 9.0 | 0 |
| Darkness (both −3) | 5.9 | 10.8 | 21.3 | 8.0 | 6.6 | 5.3 | 48.6 | 8.9 | 0 |

### Defence: rounds for one enemy to kill one Alae (higher is better)

| Buff on us | Militia | HI spear | HI sword | Barbarian | Jaguar W | Bear W | Cataphract | Archer | avg |
|---|---|---|---|---|---|---|---|---|---|
| none | 48 | 28 | 15 | 7 | 10 | 24 | 14 | 24 | 0 |
| Slime / Slow on them | 170 | 95 | 53 | 25 | 31 | 79 | 46 | 82 | +239% |
| Ironskin (nat 13) | 256 | 163 | 130 | 18 | 45 | 127 | 58 | 118 | +417% |
| Mistform | 157 | 92 | 63 | 39 | 47 | 83 | 54 | 97 | +308% |
| Body Ethereal | 188 | 113 | 64 | 29 | 37 | 94 | 55 | 93 | +300% |
| Displace (their att −5) | 192 | 112 | 61 | 29 | 36 | 95 | 53 | 96 | +296% |
| Stoneskin (nat 10) | 175 | 103 | 75 | 13 | 27 | 78 | 37 | 73 | +224% |
| Luck | 105 | 63 | 40 | 23 | 27 | 53 | 34 | 58 | +152% |
| Barkskin (nat 7) | 119 | 67 | 45 | 10 | 18 | 52 | 26 | 50 | +116% |
| Blur (their att −2) | 83 | 47 | 27 | 12 | 15 | 41 | 24 | 41 | +70% |
| Temper Armors (+3 armour) | 80 | 47 | 28 | 9 | 14 | 38 | 20 | 37 | +55% |
| Twist Fate (first hit only) | 57 | 33 | 20 | 11 | 14 | 28 | 18 | 31 | +32% |

**Read-off:**
- Skins are worth much less against big two-handed hits: Barbarians kill through Barkskin almost as fast as before. Mistform and Ethereal hold against them; skins hold against spears and swords.
- Slime does double duty on the slimed men: they die about 30% faster and kill about 3× slower.

### Missiles: men's hp of damage per 100 shots into a packed block

**Shield correction (later on 2026-10-28):** the missile numbers below were made while a parser bug gave every unit parry 0. Rerun with shields (manual: DRN + half the size points vs DRN + 2 × parry):
- Velite javelins do about a third as much to shielded targets: militia 42 → 12.5, sword HI 15 → 4.2. Barbarians are unchanged (no shields).
- The **percentage change from each buff is the same**, so the missile ranking stands.
- Enemy short bows into our tower-shielded Alae (parry 7) drop from 11.3 to **0.6** hp per 100 shots. Air Shield barely matters for Alae; it matters for the mages and the unshielded.
- Melee changed little; Weapons of Sharpness is now −45% rounds to kill (was −36%), Twist Fate +11% (was +32%).
- Full new tables: `python3 -I scripts/spells.py rank`.

Velite javelins at range 10:

| Buff | Militia | HI spear | HI sword | Barbarian | Jaguar W | Bear W | Cataphract | Archer | avg |
|---|---|---|---|---|---|---|---|---|---|
| none | 42 | 24 | 15 | 27 | 32 | 30 | 10 | 13 | 0 |
| Trueshot (prec +4) | 47 | 27 | 16 | 30 | 35 | 33 | 12 | 14 | +11% |
| Wind Guide (prec +2, half deviation) | 50 | 28 | 18 | 32 | 38 | 34 | 12 | 15 | +18% |
| Strength of Giants (str +4; javelins add full str) | 59 | 40 | 30 | 41 | 47 | 45 | 24 | 28 | +76% |
| Flaming Arrows (+8 AP fire) | 74 | 46 | 31 | 50 | 58 | 54 | 24 | 28 | +99% |
| Serpent Fang (+5 poison when wounding) | 73 | 49 | 32 | 49 | 57 | 53 | 25 | 31 | +104% |
| Storm (both sides) | 17 | 9 | 6 | 10 | 13 | 11 | 4 | 5 | −61% |

Indie Archer short bows at range 15 show the same order: Trueshot +13%, Wind Guide +23%, Strength +40% (bows add half strength), Flaming Arrows +118%, Serpent Fang +108%, Storm −63%.

**Enemy missiles into packed Alae** (hp per 100 shots; lower is better):

| Buff on us | Archer | Bear javelin | Velite javelin |
|---|---|---|---|
| none | 11.3 | 17.6 | 14.6 |
| Air Shield family (80% stopped) | 2.2 | 3.4 | 3.0 |
| Body Ethereal | 2.8 | 4.4 | 3.7 |
| Mistform | 2.8 | 3.9 | 3.5 |
| Barkskin | 4.1 | 6.9 | 5.4 |
| Temper Armors | 5.9 | 10.0 | 8.2 |

**Precision helps less than expected against a packed block.** Inside about 10 squares the deviation (range × 1.25 / precision) is about 1 square, and a miss still lands among the enemy. Precision matters at long range and against spread-out targets: skirmishers, cavalry, lone mages.

## Ranked families

Tiers:
- **S**: changes a battle; get it and script it.
- **A**: strong.
- **B**: good in the right fight.
- **C**: niche.
- **D**: not worth a cast against what we fight.

**Who** gives the cheapest Pythium caster: Th = Theurg, Barth = Bartholomeus, AT = Arch Theurg, Comm = a communion master, God = the dormant Titan (E5 N5), "—" = not Pythium paths. School levels are in brackets.

### Buffs for melee troops

| Tier | Family (spell versions: path, school, area) | Who | Why |
|---|---|---|---|
| S | **Mistform**: Personal Mistform A2 Alt2 (self); Mistform A2 Alt4 (1 sq, r10); **Fog Warriors** A4 Alt7 (20+ sq, 1A); Army of Mist A5 Alt8 (all, 3A) | AT; Barth+5 for Fog Warriors | +308%, best against big hits (Barbarians ×5.6), and against missiles too. A magic weapon or a 25+ hit ends it. The single version is 3 men per cast. **Fog Warriors** (one cast, the whole army) is our best mass defence; it needs Alteration 7 and A4 (Bartholomeus with 5 Communicants). |
| S | **Skins**: Barkskin N1 → Group Barkskin N2 (3+) → Wooden Warriors N3 (20+) → Oaken Army N4 (all). Stoneskin E2 → Group E3 → Marble Warriors E3 (20+) → Marble Army E4. Ironskin E2 → Group E3 → Iron Warriors E4 (20+) → Army of Bronze/Gold/Lead | God only | Stoneskin +224%, Ironskin +417% against spears and swords; much less against two-handers. Natural protection combines with armour (armour + nat − armour×nat/40). Skins bring fire, cold or shock weakness 5. **The god's job once awake**: Marble Warriors at Alt 7 is the army-wide version. |
| A | **Body Ethereal** S1 Alt3 (1 sq, r10) | Th, Acolyte | +300% against non-magic weapons and missiles. Only one square per cast at range 10, so it's for **mages and commanders**, not the line. No mass version exists. |
| A | **Quickness / Quickening** W2 Alt4 (1 sq); Quickening W2 Alt8 (9+ sq, 1W) | Barth | Two actions a round, about −49% time to kill. Quickness is small and short-ranged; Quickening is late. |
| A | **Armour-piercing weapons**: Weapons of Sharpness E3 Ench5 (1 sq); Steel Slice Warriors E4 Ench7 (20+) | God | −36%, and the best against heavy armour (Cataphract 47 → 18 rounds). Slashing and piercing only, so it works on spears. |
| A | **Strength**: Strength of Giants E2 Ench1 (1 sq, **range 5**); Gift of Giant Strength E2 Ench3 (3+); Giant Strength Warriors E3 Ench5 (20+); Rush of Strength (blood) | God | −34% melee, and +76% for javelins (full strength). Strength of Giants' range of 5 means the caster must stand in the line. |
| A | **Morale**: Sermon of Courage H2 (10+ sq); **Fanaticism** H4 (all); Blessing / **Divine Blessing** H3 (sacreds, +1 morale and the god's blesses) | Th / Barth / Theocratus | Not in the tables, but **routs decide our indie fights** (Murias routed in round 7, Nom in round 13). Holy spells cost no fatigue. Divine Blessing gives our sacred casters the god's **Reinvigoration and Resilient** (fatigue), which means more casts per battle. Our line troops aren't sacred. |
| B | **Luck**: Personal Luck, Luck, Group Luck, Battle Fortune, Dreamwild Legion (Glamour) | — | +152%, and best on few, valuable units. Not our paths. |
| B | **Displacement / Blur**: Displace Body G2 self, Gift of Displacement (1 sq), Displaced Warriors G4 (20+); Blur, Group Blur, Shadow Warriors, Army of Shades (attackers −2) | — | Displace +296% (attackers −5, the first strike −10); Blur +70%. True sight ignores both. Glamour, not ours. |
| B | **Attack and morale +2**: Battle Fury F2 Thaum2 (1 sq), Furious Warriors F2 (3+), Gift of the Furies F3 (20+); animal versions N | — | −29% time to kill plus morale. Fire, not ours unless an Arch Theurg rolls Fire. |
| B | **Twist Fate**: Twist Fate S1 (self, Alt0); Gift of Cheated Fate S1 Alt2 (1 sq, r10); Rewrite Fate S4 Alt6 (20+, 1S); Will of the Fates S5 Alt7 (all, 2S) | Th / Comm | Negates one hit per man: +32% on a line soldier, but a hit on a mage would often kill, so it's worth more there. **Rewrite Fate** is a decent army-wide opener for Comm (S4) at Alteration 6. |
| B | **Temper Armors** E2 Constr2 (5+ sq); Soldiers of Steel E3 Constr4 (20+); Legions of Steel E4 Constr6 (all, 1E) | God | +55% on armoured troops like our Alae; nothing on the unarmoured. Cheap army-wide by Construction 6. |
| B | **Regeneration**: Personal, Regeneration N3, Group N3, Mass N4 (20+), Army N5 | God | Slow healing over a long fight; it matters for thugs and big monsters, little for a 10-hp soldier. |
| B | **Size**: Enlarge N2, Giant Warriors N3 (10 sq), Army of Giants N5 (all): size +1, hp +30%, str +3, def −1 | God | Good on troops; more hits from missiles (bigger target). |
| C | **Stun weapons**: Earth Shatter Hammers E2 Ench4 (1 sq), Earthquake Warriors E4 (20+), Earth Shatter Army E5 | God | **Blunt and slash only, so not spears**: useless for Alae, Velites and Bear warriors. Good for Jaguar club-swords and Foul Spawn. |
| C | **Resistance wards**: Lesser/Thunder/Winter/Flame Ward, Fire Resistance, Resist Lightning, Fend versions | Th–Comm | Pure counters; only when the enemy has fire, shock or cold magic. None met yet. |
| C | **Mobility**: Windrunner A1 (self), Gift of the Hare N1, **Haste** N3 Ench4 (20+); **Flight**: Gift of Flight A2 Ench3, Mass Flight A4, Soaring Army A5; Levitate | Th / AT / Comm | Speed brings the line into contact sooner (good against archers) and lets flyers hit the mage line. Gift of Flight on a thug commander sends it at the enemy mages (plan). |
| C | **Liquid Body / Gift of Formlessness / Wave Warriors** W1-W3 (slash, blunt and pierce resistance, −4 str, −25% speed) | Th–Comm | Halves physical damage but makes the troops weak and slow: a defensive anvil only. |
| C | **Mossbody** N1W1 (1 sq) | — | Absorbs one hit (−15); single square. |
| D | **Charge Body** A1 self | Th | 20 shock on one attacker, once. Mages shouldn't be in melee anyway. |

### Buffs for missile troops

| Tier | Family | Who | Why |
|---|---|---|---|
| S | **Extra damage on missiles**: Flaming Arrows F3 Ench5 (20+), Ignite Arrows F2 (1 sq), Hail of Burning Embers F4 (all); **Serpent Fang Arrows** N3 Ench4 (20+), Envenom Arrows N1 (1 sq), Hail of Serpent Fangs N4 | God for the poison versions | +100-118%: doubles a missile force. The poison versions are the god's. Ammo matters: Velites carry 2 javelins, so this is for **archers** (12 arrows). |
| A | **Strength** (see above) | God | +76% for javelins (full strength), +40% for bows (half). |
| A | **Range**: Farflight A1 Ench3 (1 sq, r10), **Farflight Arrows** A2 Ench5 (20+, 1A), Greater Farflight A4 Ench6 (all) | Th / AT / Comm | +50% range means more volleys before contact. Javelins thrown at range 10 become 15, the difference between one throw and two. |
| B | **Precision**: Trueshot A1 Ench1 (1 sq, **range 10**), **Trueshot Warriors** A2 Ench4 (20+, 1A), Eagle Eyes / Eagle-eyed Warriors N (+4), **Wind Guide** A3 Ench6 (all: +2 and half the deviation; cancels Storm's 50% firing chance) | Th / AT / Comm | Only +11-23% against packed blocks at short range; more at long range and against spread-out targets. Trueshot on 3 javelin men (2 shots each) is a waste of a cast; Trueshot Warriors on an archer corps is fine. **Wind Guide** is the pick to pair with our own Storm. |
| B | **Missile protection for the shooters**: see the Air Shield family under mage protection | | Archers duel other archers. |

### Debuffs on the enemy

| Tier | Family | Who | Why |
|---|---|---|---|
| S | **Slow family**: **Slime** W1 Evo1 (1 sq, r30+, MR, ignores shields); Slow W2 Alt4 (1 sq, MR, att/def −2, half speed); **Crawl** W3 Alt7 (6+2/lvl sq, 1W, MR); Gooey Water W2 (**underwater only**) | Th; Barth; Comm | On the slimed men, our kills come 30% faster and theirs about 3× slower. It lands 62% of the time against MR 10 troops. Slime is one square per cast, but at range 30-50 it reaches the enemy front from the rear, and aimed at a packed block it lands on someone. **Crawl** is the mass version, 10-12 squares at W3-W4. The user's pick, and the numbers agree. |
| S | **Fatigue spam**: **Stellar Cascades** S2 Evo5 (7 sq, AP fatigue 25, MR halves); Curse of Stones E3 Alt4 (all, 3E: +3 enc, −25% speed); Desiccation W2 Thaum1 (1 sq, 2d8 fatigue a turn, MR); Curse of the Desert W3 Thaum4 (5 sq); Steal Breath A1 Thaum2 (1 man); Torpor N2 | Th (Cascades at S2); God (Curse of Stones) | Fatigue lowers defence by 1 per 10 and makes armour-defeating hits likely; at 100 the target is unconscious. Cascades on a whole formation from any Theurg is our best mass debuff by Evocation 5. Curse of Stones is battlefield-wide for the god. |
| A | **Battlefield darkness and terrain**: Solar Eclipse, Nightfall, Darkness (−3 att/def/prec), Quagmire W4 Ench5 (−1/−1, +2 enc, −20% speed), Twilight | Comm (Quagmire) | Even for us in melee (equal troops cancel out), but it **cuts enemy missile precision** and adds fatigue. Use when they shoot and we don't, or when our troops have darkvision or swamp survival. |
| A | **Storm** A4 Alt5 (battlefield, 1A): precision halved, half of all missiles lost, no flying | Comm | −61% to missiles on **both** sides. Strong against archer-heavy enemies when our army is melee. Wind Guide undoes it for our side. |
| A | **Knockdown**: Gust of Winds A1 Evo1 (2 sq, r35+, size resists); **Storm Wind** A2 Evo3 (8+2/lvl sq, r40+, 10 fatigue) | Th / AT | Knocked-down men lose their action and are easy to hit; no MR check (size resists). Storm Wind covers 12-16 squares from Bartholomeus or an AT for 10 fatigue, a cheap mass disruptor at Evocation 3 (queued third). |
| A | **Immobilise**: Tangle Vines N1 (1 sq), Tangle Thicket N2 (3+), Wild Growth N4 (10+); Web N1 (3 sq); Earth Grip E1 (1 man), Earth Meld E2 (5 sq); Freeze / Winter's Chill W2-W3 (slow plus fatigue) | God (N/E); Barth/Comm (Freeze) | Stuck men can't fight. The god's Tangle Thicket and Earth Meld are good wide holds. |
| A | **Mind disable**: Sleep, Slumber, Sandman's Blessing (G); Confusion, Mass Confusion (G); Bewitching Lights G1 (3 sq); Holy Word H2 (sacreds only) | Th (Holy Word only) | Very strong, but Glamour. Holy Word only stuns *sacred* enemies. |
| B | **Fear**: Panic N2 Thaum3 (5+2/lvl sq), Despair G2, Terror D3, Frighten D1, Wailing Winds, Blood Rain | God (Panic) | Indies rout early anyway; fear speeds it up. Panic is the god's. |
| B | **Armour destruction**: Rust Mist E2W1 Evo2 (9+ sq), Destruction E3 Alt4 (6 sq), Armor of Achilles E1 (1 sq), Iron Bane E3 Alt6 (all, 1E) | God | Strong against heavy infantry and cataphracts; non-magic armour only. |
| B | **Weaken**: Weakness D1, Enfeeble D2, Shrink N2, Army of Rats N5, Calm Emotions / Serenity W (str and att −1) | God (Shrink); Comm (Serenity) | Permanent but small; Serenity mostly counters berserkers. |
| C | **Curse / Doom** (S4 Alt7 battlefield, 1S): bad luck | Comm | The effect is vague; test before relying on it. |
| C | **Horror Mark** S2 Thaum1 (1 man, r50) | Th | Sets up horrors and Astral Geyser; no direct effect. |

### Keeping mages alive (the user's goal: kill enemy mages without losing ours)

| Tier | Spell | Who | Why |
|---|---|---|---|
| S | **Air Shield** A1 (self, Alt0); **Protective Winds** A2 Alt3 (3+1/lvl sq, r15); **Arrow Ward** A3 Alt5 (20+ sq, 1A); Arrow Fend A4 Alt7 (all) | Th / AT / Comm | Stops 80% of missiles. Missiles are what kills mages (hp 8-9, prot 1). Every Theurg already opens with Air Shield. Protective Winds on the mage line from one AT or Barth is next. |
| S | **Body Ethereal** S1 Alt3 (r10, 1 sq) | Th, Acolyte | 75% of non-magic hits and missiles miss. Cast on the mage's own square. Coming at Alteration 3 (queued). |
| A | **Mistform** (Personal A2 Alt2) | AT, Barth | Any non-magic hit under 25 does 1 damage. Barth and an AT get it at Alteration 2 (next in queue). |
| A | **Twist Fate** S1 Alt0 | Th | Free: negates the first hit, which on a mage is often the lethal one. Already scripted. |
| A | **Resist Magic** S1 Ench1 (+4 MR self); **Spell Ward** S2 Ench4 (20+, 1S); Antimagic S3 Ench7 (all, 2S); Mind Blank G1S1; Iron Will E1 | Th / Th / AT | Counters enemy mind spells and MR-checked damage. Needed once we meet enemy mages. |
| B | **Astral Shield** S1 Ench3 (self) | Th | Attackers must beat MR or be paralysed (strength 12 + astral level). Good against cavalry reaching the mages. |
| B | **Quicken Self** W1 Alt2 | Th | The mage dodges better and can flee; it still casts once a round. |
| — | Position | | Mages at the rear with Stay behind troops, a screen in front, a bodyguard squad (the Communicants guard Bartholomeus). |

### Killing enemy mage corps

Mages are worth killing because they are few and fragile. What reaches the back rows:
- **Long-range AoE damage:** Falling Frost (r50, 14 sq at W4), Astral Geyser (r50+, 12 sq), Stellar Cascades (fatigue); see the damage notes in `play/strategy` of dom6-knowledge.
- **Single-target at range 100:** Paralyze S2 Thaum4 (MR), Mind Burn S2 Thaum2, Soul Slay S3 Thaum5, Magic Duel S1 Evo3 (astral mages only; our god has no Astral on purpose).

Against MR 15-18 mages, MR spells land 11-30% of the time. **Damage spells without an MR check beat MR spells for mage killing.** The AI picks the targets, so long-range area spells are the dependable way.

## What this means for Pythium now (research queue: Evo2, Alt2, Evo3, Alt3, Constr1-3, ...)

1. **Now:** Slime on every Theurg (done), Air Shield and Twist Fate as openers (done), Divine Blessing on Bartholomeus (done; it also gives the sacred casters Reinvigoration). Sermon of Courage on the field priest.
2. **Alteration 2:**
   - Personal Mistform for Bartholomeus and Arch Theurgs.
   - Gift of Cheated Fate is only one square, so it's low priority.
3. **Alteration 3:**
   - **Body Ethereal** on each mage's own square.
   - **Protective Winds** from Bartholomeus (A2) over the mage line.
4. **Enchantment 4-5, Alteration 5:**
   - Trueshot Warriors and Farflight Arrows for an archer corps.
   - Spell Ward against enemy magic.
   - **Arrow Ward** from a communion master.
5. **Evocation 5:** **Stellar Cascades** on the Theurgs (fatigue over 7 squares, no MR immunity, only half damage on a successful MR check).
6. **Alteration 7:**
   - **Fog Warriors**: army-wide Mistform from Bartholomeus + 5 Communicants.
   - **Crawl**: mass Slow.
   - Rewrite Fate is at Alteration 6.
7. **The god, once awake (turns 10-13):**
   - Skins: Group Stoneskin → Marble Warriors.
   - Temper Armors → Legions of Steel.
   - Serpent Fang Arrows.
   - Panic, Tangle Thicket, Earth Meld.
   - Curse of Stones.

## Open questions to test in battles

- Whom does the AI target with a scripted 1-square buff (Body Ethereal, Gift of Cheated Fate, Trueshot): the caster, the nearest squad, or the commander? Watch the replay log.
- How far is the front line from mages on *Stay behind troops*? Do range-10 buffs reach it?
- Real hit rates of Slime against a packed block, from replays.
- Does Sermon of Courage stack with Fanaticism? (The user didn't know.)
