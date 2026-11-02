# Killing spells, all schools, ranked (first pass, 2026-10-28, for the user's review)

Every combat spell that kills or damages: Evocation, Alteration, Thaumaturgy, Enchantment, Blood and Divine.

- The model is the one behind `evocations.md`: one cast at a packed 6 × 3 enemy block from range 25, plus a 6-mage line.
- Numbers: `kill-table.md` (all schools) and `evocations-table.md` (Evocation in full).
- Kills are per cast: at the spell's minimum level → at +2 levels.
- **(P)** = Pythium can cast it, with the caster: Th = Theurg; Barth = Bartholomeus or Arch Theurg; Comm = communion master; God = Hortus once awake.

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

## Against troop blocks

| Tier | Spell | Path, school | Range | Kills: militia / HI / mages (shielded targets; see `kill-table.md` for Barbarians) | Fatigue | Why |
|---|---|---|---|---|---|---|
| S | Flame Storm | F5 Evo9 | 40+ | 3.9 → 5.2 / 2.0 → 4.2 / 1.4 → 1.6 | 100 + 1 gem | Biggest single cast. |
| S | All-consuming Pyre | F5 Alt8 | caster | 4.9 → 5.0 / 4.1 → 4.8 / 1.8 → 1.7 | 100 | 40 squares **around the caster**: only for a fire-immune thug standing in the enemy. |
| S | **Niefel Flames (P, Comm+3)** | W5 Evo9 | 40+ | 3.1 → 4.2 / 1.2 → 2.0 / 1.3 → 1.6 | 100 + 1W | Our late-game army killer. |
| S | **Maws of the Earth (P, God: E3)** | E3 **Alt5** | 30+ | 1.8 → 2.0 / 0.8 → 1.5 / 0.8 → 0.9 | 100 | **New find outside Evocation:** the awake god (E5) gets the +2 numbers. 7+ squares, AP; survivors are stuck in the ground. |
| S | **Ice Strike (P, Barth: W2)** | W2 Evo7 | 30 | 1.4 → 2.0 / 0.5 → 0.7 / 0.7 → 0.8 | 20 | Pythium's best per fatigue, no communion needed. |
| S | Blade Wind **(P, God: E3)** | E3 Evo4 | 35+ | 2.2 → 2.6 / 0.4 → 0.5 / 3.9 → 4.3 | 80 | Light troops and **mage lines**. |
| S | Shimmering Fields, Flame Eruption, Vortex of Unlife, Magma Eruption | G5, F2, D5, E2F2 | | 1.3-2.5 militia (3-6 Barbarians) | | Other nations' AoE. |
| S (both sides) | Earthquake **(P, God: E4)** | E4 Evo5 | field | 1.4 → 1.3 / 0.5 / 0.6 | 300 + 3E | Hits our army too. |
| A | **Falling Frost (P, Comm: W3)** | W3 Evo5 | 50 | 0.6 → 1.1 / 0.2 → 0.4 / 0.2 → 0.5 | 20 | Long-range opener. |
| A | Falling Fires, Acid Rain, Shadow Blast, Astral Fires, Nether Darts, Gifts from Heaven **(P, God + astral)** | | | 0.6-2.3 militia (1-3 Barbarians) | | |
| A | Immolation | F2 Alt3 | caster | 0.7 → 1.0 / 0.3 → 0.4 / 0.3 → 0.4 | 20 | 7 squares around a fire-resistant caster. |
| A (short) | **Shock Wave (P, Barth: A2)**, **Cold Blast (P, Barth: W2)**, Fire Blast, Acid Spray | Evo2 | 2-11 | 0.4-1.2 militia (0.6-2.6 Barbarians) | 10-20 | Strong per cast, but the caster must be at the front. |
| B | **Chain Lightning (P, Comm)**, **Thunder Strike (P, Comm)**, Fireball, Acid Bolt, Magma Bolts, Storm of Thorns, Hellfire, Liquify, Boil, Bone Grinding | | | 0.2-1.2 militia (0.5-1.7 Barbarians) | | Boil ignores shields. |
| B (shielded foes) | **Lightning Bolt (P, Barth: A2)** | A2 Evo2 | 40+ | 0.4 / 0.4 / 0.2 | 10 | Never blocked, armour-negating: as good as Ice Strike against shielded heavy infantry, at half the fatigue. |
| C | **Cold Bolt (P)**, Flame Bolt, Pillar of Fire, **Orb Lightning (P)**, **Astral Geyser (P)**, **Star Fires (P)**, Lacerating Winds, Arrow of the Western Wind, Blood Burst, Harm | | | <1 | | One man at a time, or worse. |

Clouds, battlefield enchantments (Wrathful Skies, Astral Tempest, Fire Storm, Rain of Stones) and non-damage evocations (Storm Wind, Stellar Cascades, Rust Mist) are covered in `evocations.md`. Target-limited spells are in the table below.

## Against mage corps and single targets

The mage line is thin, so area spells mostly miss it. What kills mages:

| Rank | Spell | Path, school | Range | Mages killed a cast | Why |
|---|---|---|---|---|---|
| 1 | Blade Wind **(P, God)** | E3 Evo4 | 35+ | 3.9 → 4.3 of 6 | Many projectiles. |
| 2 | Flame Storm, **Niefel Flames (P)**, Flame Eruption, Storm of Thorns | | | 1-1.7 | Very large areas. |
| 3 | **Incinerate** | F3 Alt5 | 30 | 0.5 → 0.6 of 6 | 18++ AN, ignores shields, **no MR check**: one mage dead a cast at 60%. Not our path. |
| 3 | Hand of Death | D2 Alt1 | touch | 0.6 of 6 | 40+ AN; for a thug. |
| 4 | **Ice Strike (P)**, Nether Darts, Magma Bolts, Poison Arrows | | | 0.6-0.9 | |
| 5 | **Soul Slay (P, Barth: S3)** | S3 Thau5 | 100 | 0.1 → 0.2 of 6 | Precision 100, never misses; only MR 11 + DRN vs MR + DRN stops it. Better against low-MR commanders than mages. |
| 6 | **Mind Burn (P, Th: S2)** | S2 Thau2 | 100 | 0.1 → 0.2 of 6 | A Theurg can cast it; weak. |
| 7 | **Word of Stone (P, Barth: H3)** | Divine | 25 | 0.1 of 6 | MR negates; petrifies some survivors. |
| 8 | Lightning Bolt, Thunder Strike, Cold Bolt | | | 0.1-0.2 | Single bolts deviate past thin lines at range 25. |

Also: Disintegrate (D2) and Drain Life (D4) kill one target on a failed MR check (0.6-0.7 against MR 10, 0.2-0.3 against MR 15).

**For Pythium:**
- Until Ice Strike (Evocation 7) and the awake god's Blade Wind and Maws, the reliable mage killers are **flyers**, not spells: Angels of the Host, Gryphons, Air Elementals (`summons.md`).
- Bartholomeus's Soul Slay (Thaumaturgy 5) is the long-range option against low-MR commanders.

## Spells that only hit some targets (D against men, A against them)

- **Solar Rays (P, S2)**, **Cleansing Water (P, W2)** and Banishment (Divine): they hurt undead and demons only.
- **Arcane Bolt (P, S2)** and Hidden Flame: magic beings only.
- Sailors' Death: kills by drowning; needs water nearby.
- Water Strike, Gooey Water: underwater only.

Keep Solar Rays and Cleansing Water in mind against an undead neighbour or Wights.

## Corrections this pass made

- Maws of the Earth (Alteration 5) is a top area killer, and the awake god can cast it. It wasn't in the plan.
- Immolation and All-consuming Pyre are centred on the caster, not aimed.
- Incinerate is the best single-target mage killer in the game data, but it's Fire, which we don't have.
