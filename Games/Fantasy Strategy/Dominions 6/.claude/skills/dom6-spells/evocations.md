# Evocations, ranked (first pass, 2026-10-28, for the user's review)

All 94 researchable Evocation combat spells, ranked for **winning big army battles and killing mage
corps without losing anything important** (the user's goal). Each spell is judged against the troops we
have met: packed melee infantry (Militia, sword Heavy Infantry, Barbarians), cavalry (Cataphracts),
missile troops (Archers in plate) and a mage line.

- The numbers per spell are in `evocations-table.md`, made by `scripts/spells.py damage`.
- Buffs and debuffs are in `buffs-debuffs.md`; what Pythium can cast is in `castable.md`.

## Shield correction (later on 2026-10-28): read this first

The first run of these pages ignored shields: a parser bug read every shield as an extra weapon, so every unit had parry 0. Fixed and rerun; all numbers here are the corrected ones.

The manual's rule (p. 68) is DRN + half the size points in the square, against DRN + 2 × shield parry. A missile or spell projectile that loses that roll misses entirely. What changed:

- **Blockable spells do ¼ to ⅓ as much against shielded troops.** Militia, heavy infantry and cataphracts carry shields (parry 4). Example: Ice Strike against militia, 5.3 → 1.4. Most independents and most heavy infantry are shielded.
- **Unchanged:** spells against unshielded troops (Barbarians, archers), and spells flagged *ignores shields*: Lightning Bolt, Slime, Soul Slay, Mind Burn, Incinerate, Shadow Blast, Hand of Death, Smite and the Divine words.
- **Consequences for the tiers:**
  - Against shielded heavy infantry nothing in Evocation kills well. Ice Strike (0.5-0.7 a cast) and Lightning Bolt (0.4-0.5, half the fatigue, never blocked) are about even.
  - Ice Strike's lead is against unshielded troops (3.2-4.1 Barbarians a cast).
  - Slime keeps its value against every block.
  - Stellar Cascades and Storm Wind are blocked too: about 4 and 5 heavy infantry a cast, against 12-17 Barbarians.
- **Our own Alae carry tower shields (parry 7).** Under the manual's rule they're nearly arrow-proof: 0.6 hp per 100 short-bow shots. Check this in the next battle replay.

The model also showed Pythium (shielded heavy infantry) is hard for enemy evocations to hurt. Our spell damage is best spent on unshielded targets: monsters, barbarians, archers, cavalry without shields, and mages.

## The model and its limits

One cast at a packed enemy block of 6 × 3 squares (3 men a square, 54 men), from range 25 (or the spell's own maximum if shorter), aimed at a random square of the block.

**Landing:**
- Deviation follows the manual: range × 1.25 / precision past precision/2 − 2. Precision is the mage's 10 plus the spell's; precision 100 never misses.
- The area is the nearest N squares around the landing point.
- Each man in it takes the missile hit roll: DRN + size points/2 vs DRN + 2 × shield parry, unless the spell ignores shields.
- Then the MR check where flagged: 11 + DRN + extra levels/2 vs MR + DRN, ±4 for "hard" or "easy" to resist.

**Damage:**
- 1000+N codes = N + path level ("+"); 2000+ is ×2 a level, 3000+ ×3.
- Protection is per hit location, halved for AP, ignored for AN; limb hits are capped.
- Secondary effects are included (Fireball's flames, Thunder Strike's shock, Acid Bolt's splash), and so are chain bounces.

**Mages:** one row of 6, one per square, hp 10, prot 1, MR 15. A thin line, so precision counts.

**Not modelled:**
- clouds (they linger and lose about 1 level a round);
- battlefield enchantments, burning, how long stuns last;
- **friendly fire**, morale, and the AI choosing targets.

Damage per hit ran 1-2× high against the Murias review (see `buffs-debuffs.md`), so compare spells with each other. Don't read the numbers as exact kills.

## Corrections to what I believed before (found in the data)

- **Arcane Bolt only hurts magic beings** ("harmless for humans"). It is not an answer to heavy infantry; the research plan said it was.
- **Solar Rays** hurts only undead; **Cleansing Water** only undead and demons. They're excellent against those and do nothing to men.
- **Water Strike and Gooey Water are underwater-only.**
- **Astral Geyser** does 2 AN damage (MR negates) in 12 squares, plus horror marks: about 0.4 kills a cast. It is not a communion nuke.
- **Freezing Mist** is a **level-1 frost cloud**: 2 fatigue a round, fading about 1 level a round, damage only from level 3. It's weak; the cloud's real level needs a test in battle.
- **Orb Lightning** is 5 AN damage chaining 7 times: about 0.5 kills a cast. Weak.
- **Star Fires** is 3 bolts of 4+S: 0.2-0.3 kills a cast, the bottom of the list.
- **Thunder Strike** is a 26++ AN bolt at precision −2 plus 2 shock in 10 squares. About 1 kill a cast against blocks, and only **0.1 against a mage line**: a long-range sniper bolt misses thin lines at range 25.
- **Gust of Winds** (A1, Theurgs) knocks down about **5 unshielded men a cast** (1.5 shielded) for 10 fatigue; **Storm Wind** (A2) about **17-22 unshielded** (5-6 shielded heavy infantry). That's more men a cast than Slime (about 1.3 slimed a cast at 20 fatigue). Slime's effect lasts all battle; a knockdown lasts about a round.

## Kills per cast, the headline numbers

At the spell's minimum level → +2 levels. "Mages" is kills out of a 6-mage line.

| Spell | Path, school | Range, area | Militia | HI sword | Barbarian | Archer | Mages | Fatigue / gems |
|---|---|---|---|---|---|---|---|---|
| Flame Storm | F5 Evo9 | 40+, 50 sq | 3.9 → 5.2 | 2.0 → 4.2 | 7.4 → 13.7 | 7.4 → 14.2 | 1.4 → 1.6 | 100, 1F |
| **Niefel Flames** | W5 Evo9 | 40+, 75+ sq | 3.1 → 4.2 | 1.2 → 2.0 | 4.7 → 7.7 | 4.3 → 7.4 | 1.3 → 1.6 | 100, 1W |
| Blade Wind | E3 Evo4 | 35+, ~45 blades | 2.2 → 2.6 | 0.4 → 0.5 | 3.3 → 3.7 | 1.0 → 1.1 | 3.9 → 4.3 | 80 |
| Shimmering Fields | G5 Evo7 | 25, 50 sq | 1.7 → 2.5 | 1.6 → 2.5 | 3.4 → 5.7 | 5.7 → 9.2 | 0.2 → 0.3 | 200, 2G |
| Flame Eruption | F2 Evo6 | **7+**, 15 sq | 2.0 → 2.4 | 0.8 → 1.3 | 3.0 → 4.5 | 2.7 → 4.4 | 1.0 → 1.1 | 30 |
| **Ice Strike** | W2 Evo7 | 30, 4+2/lvl sq | 1.4 → 2.0 | 0.5 → 0.7 | 3.2 → 4.1 | 1.4 → 1.8 | 0.7 → 0.8 | 20 |
| Vortex of Unlife | D5 Evo8 | 30+, 8+ sq | 1.3 → 1.8 | 1.2 → 1.6 | 4.5 → 6.4 | 5.0 → 6.0 | 0.2 → 0.3 | 20 |
| Magma Eruption | E2F2 Evo6 | 30, 6+ sq | 1.4 → 1.9 | 0.7 → 1.0 | 3.4 → 4.9 | 2.1 → 3.7 | 0.6 → 0.7 | 50 |
| Earthquake (whole field, **both sides**) | E4 Evo5 | all | 1.4 → 1.3 | 0.5 | 1.8 | 1.6 | 0.6 | 300, 3E |
| Gifts from Heaven | E3S1 Evo5 | 100, 3 × 8 sq | 1.1 → 1.2 | 0.5 | 2.1 | 2.1 → 1.9 | 0.7 → 0.8 | 50 |
| Shadow Blast | D2 Evo5 | 35+, 9+ sq | 2.3 → 3.9 | 2.3 → 4.0 | 1.1 → 2.5 | 2.1 → 4.1 | 0.2 | 100, 1D |
| Falling Fires | F3 Evo5 | 50, 6+ sq | 1.0 → 1.1 | 0.6 → 0.4 | 1.9 | 1.9 → 2.2 | 0.4 | 20 |
| **Falling Frost** | W3 Evo5 | 50, 10+ sq | 0.6 → 1.1 | 0.2 → 0.4 | 0.8 → 1.5 | 0.7 → 1.5 | 0.2 → 0.5 | 20 |
| Astral Fires | S4F1 Evo6 | 45+, 1+6 sq | 0.8 → 1.0 | 0.9 | 1.7 → 1.9 | 3.0 → 3.2 | 0.3 | 20 |
| Nether Darts | S1D1 Evo7 | 30+, 14+ darts | 0.7 → 0.9 | 0.4 → 0.5 | 1.2 → 2.3 | 1.2 → 2.1 | 0.6 → 0.8 | 15 |
| Acid Rain | W3F1 Evo4 | 30, 6+ sq | 0.7 → 0.9 | 0.3 | 1.1 → 1.5 | 1.1 → 1.4 | 0.3 → 0.4 | 30 |
| Storm of Thorns | N2 Evo7 | 35+, 6+ thorns | 0.3 → 0.7 | 0.1 → 0.2 | 0.5 → 1.2 | 0.2 → 0.6 | 0.7 → 1.1 | 20 |
| **Shock Wave** | A2 Evo2 | **2**, 6 sq | 0.8 → 1.1 | 0.9 → 1.2 | 1.6 → 2.6 | 3.2 → 4.1 | 0.5 → 0.7 | 10 |
| **Cold Blast** | W2 Evo2 | **7+1/lvl**, 3 sq | 0.4 → 0.7 | 0.1 → 0.4 | 0.6 → 1.3 | 0.5 → 1.5 | 0.3 → 0.4 | 20 |
| Fire Blast | F2 Evo2 | 7+, 3 sq | 0.6 → 0.8 | 0.3 → 0.6 | 1.2 → 2.1 | 1.1 → 2.0 | 0.4 → 0.5 | 20 |
| **Chain Lightning** | A3 Evo8 | 25, 20 bounces | 0.4 → 0.6 | 0.5 → 0.6 | 0.6 → 1.0 | 1.4 → 1.9 | 0.1 → 0.2 | 30 |
| Acid Bolt | W2F1 Evo3 | 35+, 1+6 sq | 0.4 → 0.5 | 0.2 | 0.8 | 0.6 → 0.9 | 0.2 | 30 |
| Fireball | F2 Evo3 | 35+, 1+6 sq | 0.3 → 0.4 | 0.2 | 0.6 → 0.9 | 0.5 → 0.8 | 0.2 | 20 |
| **Thunder Strike** | A3 Evo4 | 100, 1+10 sq | 0.3 | 0.4 → 0.3 | 0.9 → 0.8 | 1.1 → 1.2 | 0.1 | 50 |
| Magma Bolts | E1F1 Evo3 | 30+, 5 bolts | 0.4 | 0.3 → 0.5 | 1.4 → 1.5 | 1.1 → 1.5 | 0.6 → 0.7 | 20 |
| **Cold Bolt** | W2 Evo1 | 50+, 1 sq | 0.2 | 0.1 | 0.2 → 0.5 | 0.2 → 0.4 | 0.1 | 20 |
| **Lightning Bolt** | A2 Evo2 | 40+, 1 man | 0.4 | 0.4 → 0.5 | 0.3 → 0.4 | 0.4 → 0.5 | 0.2 | **10** |
| **Orb Lightning** | A2 Evo5 | 20, 7 bounces | 0.1 | 0.1 | 0.2 | 0.5 → 0.4 | 0.1 | 20 |
| **Astral Geyser** | S3 Evo5 | 50+, 12 sq | 0.1 | 0.1 | 0.2 | 0.4 | 0.0 | 20 |
| **Star Fires** | S1 Evo1 | 35, 3 bolts | 0.0 → 0.1 | 0.1 | 0.1 | 0.2 → 0.3 | 0.1 | 20 |

**Pythium's spells are in bold.** Other paths are listed so I recognise them when enemies use them.

**Non-damage evocations** (men affected per cast):
- **Stellar Cascades** (S2 Evo5): 25 AP fatigue to about **12.5 unshielded men**, 3.7 shielded (MR halves it).
- **Storm Wind** (A2 Evo3): knocks down **17-22 unshielded men**, 5-6 shielded.
- Rust Mist (E2W1 Evo2): rusts the armour of about 16 men.
- Breath of the Dragon (N2): poisons 6-9 men.
- Web (N1): webs about 5 men.
- **Gust of Winds** (A1): knocks down about 5 unshielded men, 1.5 shielded.
- **Slime**: about 1.3 men.

## Ranked

Tiers:
- **S**: wins big battles.
- **A**: strong main spell.
- **B**: good filler or situational.
- **C**: weak.
- **D**: useless against what we fight.

Every Evocation spell is placed. Spells in Pythium paths are marked **(P)** with the cheapest caster: Th = Theurg A1 W1 S2; Barth = Bartholomeus A2 W2 S3; AT = Arch Theurg A2 W1 S3; Comm+2 = a master with 4-5 slaves (Bartholomeus becomes A4 W4 S5); Comm+3 = 8 slaves; God = E5 N5 once awake.

### Against troop blocks (melee infantry, cavalry, missile troops)

| Tier | Spells | Why |
|---|---|---|
| S | **Niefel Flames (P, Comm+3: W5)**, Flame Storm, Shimmering Fields, Earthquake **(P, God)**, **Ice Strike (P, Barth: W2)**, Blade Wind **(P, God: E3)** | Big area or many projectiles, 5-18 kills a cast. **Ice Strike is Pythium's best**: Bartholomeus casts it **without a communion** at W2 (8 squares), or at W4 with the Communicants (12 squares), for 20 fatigue. It is slashing damage, so heavy armour resists it (1.7-2.4 kills against HI). Niefel Flames (Evo 9, 1 water gem) is the late army-killer. Earthquake hits **both armies**: only when our side is fliers or the god alone. Blade Wind is cheap kills against light troops for the awake god (80 fatigue). |
| A | **Falling Frost (P, Comm: W3)**, Falling Fires, Acid Rain, Magma Eruption, Vortex of Unlife, Shadow Blast, Astral Fires, Nether Darts, Gifts from Heaven | 2-4 kills a cast at long range. Falling Frost: Bartholomeus + 5 at W4 gets 3.7 against militia but only 1.4 against sword HI (AP cold against prot 13 plus shields). Its precision −2 makes it land up to ~4 squares off at range 25: **cast it before the lines meet** or into the rear ranks. |
| A (B vs shields) | **Storm Wind (P, Barth/AT: A2)** | Not a killer: it knocks down 17-22 unshielded men (5-6 shielded) for 10 fatigue, from range 40+. Downed men lose their action and defend badly while our line hits them. **The best value spell Pythium gets at Evocation 3.** Size and strength resist it, so it's poor against giants and monsters. |
| A (B vs shields) | **Stellar Cascades (P, Th: S2)** | Any Theurg: 25 AP fatigue to ~12 unshielded men a cast (~4 shielded) at precision 100 (never misses). Fatigue lowers defence by 1 per 10 and makes armour-defeating hits likely. Four casts put a block near collapse. **The Theurgs' best spell from Evocation 5.** |
| A (short range) | **Shock Wave (P, Barth/AT: A2)**, **Cold Blast (P, Barth: W2)**, Fire Blast, Flame Eruption, Acid Spray | Strong per cast (Shock Wave 3-4, armour-blind), but range 2 means the caster stands at the front. Cold Blast's range is 9-11. Only for a sturdy caster: an Arch Theurg with Mistform and Body Ethereal, or the god. **Not for Theurgs on Stay behind troops.** |
| B | **Chain Lightning (P, Comm+2: A3+)**, **Thunder Strike (P, Comm: A3)**, Acid Bolt, Fireball, Magma Bolts, Storm of Thorns, Poison Arrows, Poison Darts | About 1-2 kills a cast. Chain Lightning and Thunder Strike are armour-blind (AN), good against Cataphracts and heavy infantry. Thunder Strike costs 50 fatigue and is the anti-big-monster bolt. |
| B | **Gust of Winds (P, Th: A1)** | Knocks down ~5 men for 10 fatigue at range 35+. Theurgs can mix it with Slime against a packed block right before contact. |
| B (A vs shields) | **Slime (P, Th: W1)** | Ignores shields. Only ~1.3 men a cast, but the effect lasts all battle (−2 att/def, slowed); see `buffs-debuffs.md`. The user's pick for Theurgs now, and right until Stellar Cascades. |
| C | **Cold Bolt (P, Barth: W2)**, **Lightning Bolt (P, Barth/AT: A2)**, Flame Bolt, Flare, Pillar of Fire, Fire Darts, Fire Flies, Bane Fire Dart, Bane Fire, Hidden Flame, Blast/Bolt of Unlife, Geyser, Flying Shards, Vine Arrow, **Orb Lightning (P)**, **Astral Geyser (P)**, **Star Fires (P)** | Under 1 kill a cast against blocks. Lightning Bolt is the cheapest (10 fatigue) and armour-blind; Cold Bolt is OK until Evocation 2. |
| C | **Freezing Touch (P)**, **Shocking Grasp (P)**, Burning Hands | Touch range: melee spells for thugs. |
| — | Clouds: **Freezing Mist (P, Comm: W3A1)**, Fire Cloud, Poison Cloud, Poison Mist, Cloud of Death, Cloud of Dreamless Slumber | They linger and hurt whoever walks in, both sides. Freezing Mist is level 1 (fatigue only). Fire Cloud is level 8 heat (9 fatigue + 6 AN a round, fading). Test before ranking. |
| — | Battlefield: **Wrathful Skies (P, Comm+3: A5, 2A)**, **Astral Tempest (P, Comm+2: S5, 2S)**, Fire Storm, Acid Storm, Rain of Stones, Meteor Shower, Wailing Winds, Aurora Borealis, **Rain (P)** | Hit the whole field all battle. Wrathful Skies: 15 AN shock strikes, doubled in a Storm (our Storm + Wrathful Skies is a combo). Astral Tempest: 1 AN a round to all non-mindless (MR), and it hampers casting. Rain of Stones: shields protect. Most hit both sides: use when we have fewer, tougher men or fliers. |
| D | **Arcane Bolt (P)**, Hidden Flame (magic beings); **Solar Rays (P)**, **Cleansing Water (P)** (undead and demons); **Water Strike (P)** (underwater); Magic Duel (astral mages only); Ephemeral Bolt and Blast, False Fire (false damage); Healing Light (a heal); summons | No effect on living humans, or not damage. **Solar Rays and Cleansing Water become A against undead** (Cleansing Water 5+ squares at W2). Keep them in mind for an undead neighbour. |

### Against enemy mage corps (thin back line, MR 15)

1. **Many projectiles or a very big area win:**
   - Blade Wind: 3.7-4 of 6.
   - Flame Storm and Niefel Flames: 1.2-1.7.
   - Flame Eruption: about 1, short range.
   - Storm of Thorns: about 1.
   - Nether Darts and Ice Strike: 0.6-0.9.
   - Magma Bolts and Poison Arrows: about 0.6.
2. **Single bolts fail at range** against a thin line: Thunder Strike 0.1, Cold Bolt 0.1, Lightning Bolt 0.2. Deviation at range 25 is about 3 squares at precision 8-12.
3. **Pythium's mage killers, in order:**
   - **Ice Strike** (Bartholomeus, Evo 7);
   - **Falling Frost** (Comm, Evo 5: 0.3-0.5);
   - then **Niefel Flames** (Evo 9).
   - Before those, kill mages with a **flanking or flying thug** (Gift of Flight) or cavalry, not with bolts.
   - Paralyze and Soul Slay (Thaumaturgy) need MR checks: 11-30% against MR 15-18.
4. **Spells that kill our mages,** to defend against: the same big areas. So spread our mage line, put Air Shield and Body Ethereal on it, and give it a screen.

## What this means for Pythium

Evocation is our damage school. Our paths reach some of the best spells in it, and the steps that matter are big ones:

| Evocation | New for us | Use |
|---|---|---|
| 2 (next month) | Cold Blast, Lightning Bolt, Shock Wave | Bartholomeus: Lightning Bolt (10 fatigue, armour-blind) or Cold Bolt at range; Cold Blast only if the front is within 11 squares. |
| 3 (queued third) | **Storm Wind**, Freezing Mist | Bartholomeus and Arch Theurgs open with Storm Wind on the enemy block as it closes. |
| 4 | Thunder Strike | Comm, against big single targets (monsters, commanders). |
| 5 | **Stellar Cascades**, **Falling Frost**, Orb Lightning, Astral Geyser | Theurgs: Cascades instead of Slime once the enemy has reached them. Comm: Falling Frost before contact. |
| 7 | **Ice Strike** | Bartholomeus without a communion (W2), and every W2 master. |
| 8-9 | Chain Lightning, **Niefel Flames**, Astral Tempest | Comm+3 for Niefel. |

Using the user's cost estimate (50 RP for level 1, doubling each level), Evocation 5 is about 1,550 RP and Evocation 7 about 6,350 RP. At 76 RP a month that's far off, so **research speed (Owl Quills, more Theurgs) is what brings Ice Strike in**.

**Script changes this suggests** (not made yet, for the user's review):
- Bartholomeus: Communion Master, Divine Blessing, then Cold Bolt now. From Evocation 2, Lightning Bolt as the cheap armour-blind option; Cold Bolt at W4 does about as well against light troops.
- Storm Wind at Evocation 3.
- Theurgs: Air Shield, Twist Fate, Slime ×3 as now; one Gust of Winds instead of a Slime against a packed block is worth trying.

## Open questions to test in battle

- The real level of a Freezing Mist cloud, and how fast it fades.
- Do AoE evocations hit our own men when the lines touch? The model assumes yes, as for missiles.
- Does the shield hit roll apply to area spells? The model assumes yes, since some spells carry an explicit "ignores shields" flag.
- Storm Wind against a packed block in a replay: how many go down, and for how long.
