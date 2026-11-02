# Evocation spells: modelled effect per cast (generated)

Made by `scripts/spells.py damage -n 300` (2026-10-28; rerun after the shield fix: shields now block per the manual). One cast at a packed enemy block of 6 x 3 squares, 3 men per square (2 for cavalry), aimed at a random square of it from range 25 (or the spell's own range if shorter). Mages: one row of 6, one per square, hp 10, prot 1, MR 15. Caster precision 10. Rows at the spell's minimum path level (@req) and two levels higher (@+2, a communion master with 4-5 slaves; fatigue shown divided accordingly). **k** = men killed outright, **hp** = damage in whole men's hit points (damage / 10). "fat" = fatigue dealt; "men hit" = men affected by a non-damage effect. "–" = not modelled (clouds, battlefield enchantments, summons, heals) or no effect on living humans (Arcane Bolt, Solar Rays, Cleansing Water). Ranking and caveats: `evocations.md`.

| Spell | Path @lvl | Range (used) | Fatigue | Militia | Heavy Inf (sword) | Barbarian | Cataphract | Archer | Mages (1/square, MR 15) |
|---|---|---|---|---|---|---|---|---|---|
| Fire Flies | F1 @req | 35 (25) | 20 | 0.05 k / 0.3 hp | 0.03 k / 0.2 hp | 0.07 k / 1.0 hp | 0.01 k / 0.1 hp | 0.10 k / 0.5 hp | 0.13 k / 0.4 hp |
| Fire Flies | F1 @+2 | 45 (25) | 7 | 0.08 k / 0.3 hp | 0.02 k / 0.2 hp | 0.07 k / 0.9 hp | 0.01 k / 0.1 hp | 0.09 k / 0.5 hp | 0.17 k / 0.5 hp |
| Freezing Touch | W1 @req | 1 (1) | 10 | 0.09 k / 0.2 hp | 0.08 k / 0.2 hp | 0.12 k / 0.5 hp | 0.02 k / 0.1 hp | 0.19 k / 0.5 hp | 0.16 k / 0.4 hp |
| Freezing Touch | W1 @+2 | 1 (1) | 3 | 0.09 k / 0.2 hp | 0.08 k / 0.2 hp | 0.22 k / 0.7 hp | 0.04 k / 0.1 hp | 0.26 k / 0.5 hp | 0.22 k / 0.4 hp |
| Flying Shards | E1 @req | 35 (25) | 30 | 0.04 k / 0.1 hp | 0.00 k / 0.0 hp | 0.09 k / 0.4 hp | 0.00 k / 0.0 hp | 0.00 k / 0.0 hp | 0.14 k / 0.3 hp |
| Flying Shards | E1 @+2 | 45 (25) | 10 | 0.14 k / 0.4 hp | 0.02 k / 0.1 hp | 0.21 k / 1.0 hp | 0.00 k / 0.0 hp | 0.04 k / 0.2 hp | 0.35 k / 0.7 hp |
| Burning Hands | F1 @req | 1 (1) | 5 | 0.30 k / 0.5 hp | 0.17 k / 0.4 hp | 0.56 k / 2.0 hp | 0.06 k / 0.2 hp | 0.55 k / 1.4 hp | 0.30 k / 0.4 hp |
| Burning Hands | F1 @+2 | 1 (1) | 2 | 0.35 k / 0.5 hp | 0.22 k / 0.5 hp | 0.78 k / 2.2 hp | 0.09 k / 0.2 hp | 0.75 k / 1.6 hp | 0.37 k / 0.5 hp |
| Fire Darts | F1 @req | 35 (25) | 20 | 0.10 k / 0.3 hp | 0.05 k / 0.2 hp | 0.14 k / 1.1 hp | 0.01 k / 0.1 hp | 0.12 k / 0.7 hp | 0.20 k / 0.5 hp |
| Fire Darts | F1 @+2 | 45 (25) | 7 | 0.15 k / 0.5 hp | 0.06 k / 0.3 hp | 0.20 k / 1.7 hp | 0.03 k / 0.2 hp | 0.17 k / 0.9 hp | 0.29 k / 0.7 hp |
| Flame Bolt | F2 @req | 55 (25) | 20 | 0.21 k / 0.4 hp | 0.11 k / 0.3 hp | 0.34 k / 1.4 hp | 0.04 k / 0.1 hp | 0.33 k / 0.8 hp | 0.11 k / 0.2 hp |
| Flame Bolt | F2 @+2 | 65 (25) | 7 | 0.25 k / 0.3 hp | 0.20 k / 0.3 hp | 0.65 k / 1.5 hp | 0.07 k / 0.2 hp | 0.67 k / 1.2 hp | 0.12 k / 0.2 hp |
| Shocking Grasp | A1 @req | 1 (1) | 5 | 0.13 k / 0.3 hp | 0.13 k / 0.3 hp | 0.45 k / 1.4 hp | 0.09 k / 0.2 hp | 0.58 k / 1.2 hp | 0.38 k / 0.6 hp |
| Shocking Grasp | A1 @+2 | 1 (1) | 2 | 0.19 k / 0.3 hp | 0.15 k / 0.3 hp | 0.45 k / 1.3 hp | 0.11 k / 0.2 hp | 0.57 k / 1.2 hp | 0.40 k / 0.6 hp |
| Gust of Winds | A1 @req | 40 (25) | 10 | 0.03 k / 0.2 hp | 0.00 k / 0.0 hp | 0.03 k / 0.4 hp | 0.00 k / 0.0 hp | 0.01 k / 0.0 hp | 0.05 k / 0.1 hp |
| Gust of Winds | A1 @+2 | 50 (25) | 3 | 0.03 k / 0.2 hp | 0.00 k / 0.0 hp | 0.05 k / 0.4 hp | 0.00 k / 0.0 hp | 0.00 k / 0.1 hp | 0.04 k / 0.1 hp |
| Slime | W1 @req | 35 (25) | 20 | 1.3 men hit | 1.2 men hit | 1.4 men hit | 0.9 men hit | 1.2 men hit | 0.1 men hit |
| Slime | W1 @+2 | 45 (25) | 7 | 1.4 men hit | 1.2 men hit | 1.5 men hit | 0.9 men hit | 1.4 men hit | 0.1 men hit |
| Water Strike | W1 @req | 40 (25) | 20 | 0.41 k / 1.1 hp | 0.05 k / 0.3 hp | 0.17 k / 1.0 hp | 0.02 k / 0.1 hp | 0.03 k / 0.3 hp | 0.11 k / 0.2 hp |
| Water Strike | W1 @+2 | 50 (25) | 7 | 0.81 k / 1.4 hp | 0.12 k / 0.7 hp | 0.34 k / 1.4 hp | 0.05 k / 0.4 hp | 0.13 k / 0.7 hp | 0.18 k / 0.3 hp |
| Cold Bolt | W2 @req | 60 (25) | 20 | 0.17 k / 0.4 hp | 0.06 k / 0.2 hp | 0.23 k / 1.3 hp | 0.05 k / 0.1 hp | 0.25 k / 0.9 hp | 0.12 k / 0.2 hp |
| Cold Bolt | W2 @+2 | 70 (25) | 7 | 0.22 k / 0.4 hp | 0.13 k / 0.3 hp | 0.45 k / 1.5 hp | 0.02 k / 0.1 hp | 0.39 k / 1.0 hp | 0.14 k / 0.2 hp |
| Geyser | W1F1 @req | 25 (25) | 10 | 0.08 k / 0.5 hp | 0.03 k / 0.2 hp | 0.14 k / 1.5 hp | 0.00 k / 0.1 hp | 0.10 k / 0.7 hp | 0.05 k / 0.3 hp |
| Geyser | W1F1 @+2 | 35 (25) | 3 | 0.19 k / 0.7 hp | 0.04 k / 0.3 hp | 0.20 k / 1.9 hp | 0.02 k / 0.1 hp | 0.17 k / 1.1 hp | 0.12 k / 0.4 hp |
| Acid Spray | W2F1 @req | 2 (2) | 20 | 0.42 k / 1.6 hp | 0.16 k / 1.0 hp | 0.67 k / 5.3 hp | 0.07 k / 0.3 hp | 0.61 k / 3.1 hp | 0.48 k / 1.1 hp |
| Acid Spray | W2F1 @+2 | 2 (2) | 7 | 0.44 k / 1.6 hp | 0.19 k / 0.9 hp | 0.78 k / 5.4 hp | 0.04 k / 0.3 hp | 0.67 k / 3.2 hp | 0.43 k / 1.1 hp |
| Star Fires | S1 @req | 35 (25) | 20 | 0.04 k / 0.2 hp | 0.05 k / 0.2 hp | 0.08 k / 0.7 hp | 0.03 k / 0.1 hp | 0.16 k / 0.7 hp | 0.08 k / 0.3 hp |
| Star Fires | S1 @+2 | 35 (25) | 7 | 0.08 k / 0.2 hp | 0.06 k / 0.2 hp | 0.12 k / 1.0 hp | 0.04 k / 0.1 hp | 0.33 k / 1.0 hp | 0.12 k / 0.4 hp |
| Arcane Bolt | S2 @req | 50 (25) | 20 | – | – | – | – | – | – |
| Arcane Bolt | S2 @+2 | 60 (25) | 7 | – | – | – | – | – | – |
| Vine Arrow | N1 @req | 35 (25) | 20 | 0.03 k / 0.1 hp | 0.00 k / 0.0 hp | 0.07 k / 0.3 hp | 0.01 k / 0.0 hp | 0.01 k / 0.1 hp | 0.06 k / 0.1 hp |
| Vine Arrow | N1 @+2 | 45 (25) | 7 | 0.03 k / 0.1 hp | 0.01 k / 0.1 hp | 0.08 k / 0.3 hp | 0.00 k / 0.0 hp | 0.03 k / 0.2 hp | 0.10 k / 0.1 hp |
| Bewitching Lights | G1 @req | 30 (25) | 20 | 0.4 men hit | 0.4 men hit | 1.6 men hit | 0.1 men hit | 1.3 men hit | 0.0 men hit |
| Bewitching Lights | G1 @+2 | 30 (25) | 7 | 0.5 men hit | 0.4 men hit | 1.9 men hit | 0.2 men hit | 1.7 men hit | 0.0 men hit |
| Fire Blast | F2 @req | 9 (9) | 20 | 0.63 k / 1.2 hp | 0.35 k / 1.0 hp | 1.22 k / 4.4 hp | 0.09 k / 0.3 hp | 1.06 k / 3.1 hp | 0.40 k / 0.6 hp |
| Fire Blast | F2 @+2 | 11 (11) | 7 | 0.84 k / 1.2 hp | 0.62 k / 1.1 hp | 2.14 k / 5.0 hp | 0.21 k / 0.4 hp | 2.01 k / 3.6 hp | 0.47 k / 0.6 hp |
| Flare | F3 @req | 60 (25) | 50 | 0.21 k / 0.3 hp | 0.21 k / 0.3 hp | 0.80 k / 1.6 hp | 0.08 k / 0.1 hp | 0.83 k / 1.3 hp | 0.12 k / 0.2 hp |
| Flare | F3 @+2 | 70 (25) | 17 | 0.31 k / 0.4 hp | 0.29 k / 0.4 hp | 0.94 k / 1.6 hp | 0.08 k / 0.1 hp | 0.90 k / 1.2 hp | 0.11 k / 0.2 hp |
| Sulphur Haze | F2A1 @req | 30 (25) | 20 | 5 fat (2.4 men) | 6 fat (2.5 men) | 18 fat (8.3 men) | 2 fat (1.0 men) | 20 fat (9.2 men) | 2 fat (0.9 men) |
| Sulphur Haze | F2A1 @+2 | 30 (25) | 7 | 8 fat (3.4 men) | 6 fat (3.0 men) | 23 fat (10.6 men) | 2 fat (1.2 men) | 24 fat (10.9 men) | 3 fat (1.2 men) |
| Cold Blast | W2 @req | 9 (9) | 20 | 0.38 k / 1.0 hp | 0.15 k / 0.7 hp | 0.62 k / 3.4 hp | 0.04 k / 0.2 hp | 0.52 k / 2.2 hp | 0.33 k / 0.6 hp |
| Cold Blast | W2 @+2 | 11 (11) | 7 | 0.67 k / 1.1 hp | 0.43 k / 1.0 hp | 1.32 k / 4.3 hp | 0.14 k / 0.4 hp | 1.46 k / 3.4 hp | 0.36 k / 0.6 hp |
| Lightning Bolt | A2 @req | 50 (25) | 10 | 0.38 k / 0.6 hp | 0.37 k / 0.7 hp | 0.28 k / 1.1 hp | 0.36 k / 0.6 hp | 0.42 k / 1.0 hp | 0.23 k / 0.4 hp |
| Lightning Bolt | A2 @+2 | 60 (25) | 3 | 0.42 k / 0.7 hp | 0.45 k / 0.7 hp | 0.38 k / 1.2 hp | 0.46 k / 0.7 hp | 0.47 k / 1.0 hp | 0.24 k / 0.4 hp |
| Shock Wave | A2 @req | 2 (2) | 10 | 0.83 k / 2.0 hp | 0.92 k / 2.1 hp | 1.64 k / 8.2 hp | 0.38 k / 0.8 hp | 3.17 k / 7.1 hp | 0.48 k / 1.1 hp |
| Shock Wave | A2 @+2 | 2 (2) | 3 | 1.15 k / 2.1 hp | 1.17 k / 2.2 hp | 2.59 k / 9.1 hp | 0.47 k / 0.9 hp | 4.06 k / 7.8 hp | 0.65 k / 1.1 hp |
| Rust Mist | E2W1 @req | 30 (25) | 30 | 15.2 men hit | 15.2 men hit | 14.6 men hit | 10.0 men hit | 15.5 men hit | 2.1 men hit |
| Rust Mist | E2W1 @+2 | 30 (25) | 10 | 16.9 men hit | 17.3 men hit | 18.6 men hit | 11.5 men hit | 18.1 men hit | 2.4 men hit |
| Solar Rays | S2 @req | 50 (25) | 20 | – | – | – | – | – | – |
| Solar Rays | S2 @+2 | 60 (25) | 7 | – | – | – | – | – | – |
| Web | N1 @req | 27 (25) | 20 | 5.6 men hit | 6.0 men hit | 5.6 men hit | 3.6 men hit | 5.4 men hit | 1.0 men hit |
| Web | N1 @+2 | 31 (25) | 7 | 5.5 men hit | 5.6 men hit | 5.4 men hit | 3.7 men hit | 5.5 men hit | 0.9 men hit |
| Ephemeral Bolt | G2 @req | 45 (25) | 10 | 0.04 k / 0.1 hp | 0.01 k / 0.1 hp | 0.06 k / 0.6 hp | 0.00 k / 0.0 hp | 0.09 k / 0.4 hp | 0.01 k / 0.0 hp |
| Ephemeral Bolt | G2 @+2 | 55 (25) | 3 | 0.04 k / 0.2 hp | 0.06 k / 0.2 hp | 0.06 k / 0.6 hp | 0.03 k / 0.1 hp | 0.14 k / 0.5 hp | 0.02 k / 0.0 hp |
| Warrior Illusion | G1 @req | 0 (25) | 10 | – | – | – | – | – | – |
| Warrior Illusion | G1 @+2 | 0 (25) | 3 | – | – | – | – | – | – |
| Fireball | F2 @req | 45 (25) | 20 | 0.32 k / 1.0 hp | 0.18 k / 0.6 hp | 0.56 k / 3.8 hp | 0.06 k / 0.2 hp | 0.52 k / 1.9 hp | 0.16 k / 0.5 hp |
| Fireball | F2 @+2 | 55 (25) | 7 | 0.40 k / 1.2 hp | 0.23 k / 0.6 hp | 0.88 k / 4.0 hp | 0.08 k / 0.2 hp | 0.80 k / 2.1 hp | 0.22 k / 0.6 hp |
| Storm Wind | A2 @req | 50 (25) | 10 | 0.03 k / 0.2 hp | 0.00 k / 0.0 hp | 0.02 k / 0.3 hp | 0.00 k / 0.0 hp | 0.01 k / 0.1 hp | 0.02 k / 0.1 hp |
| Storm Wind | A2 @+2 | 60 (25) | 3 | 0.02 k / 0.1 hp | 0.00 k / 0.0 hp | 0.04 k / 0.4 hp | 0.00 k / 0.0 hp | 0.01 k / 0.1 hp | 0.02 k / 0.1 hp |
| Rain | W3 @req | 0 (25) | 100 | – | – | – | – | – | – |
| Rain | W3 @+2 | 0 (25) | 100 | – | – | – | – | – | – |
| Freezing Mist | W3A1 @req | 30 (25) | 20 | – | – | – | – | – | – |
| Freezing Mist | W3A1 @+2 | 30 (25) | 7 | – | – | – | – | – | – |
| Acid Bolt | W2F1 @req | 45 (25) | 30 | 0.42 k / 1.3 hp | 0.17 k / 0.7 hp | 0.75 k / 4.4 hp | 0.07 k / 0.3 hp | 0.61 k / 2.4 hp | 0.25 k / 0.7 hp |
| Acid Bolt | W2F1 @+2 | 55 (25) | 10 | 0.47 k / 1.4 hp | 0.25 k / 0.8 hp | 0.85 k / 4.4 hp | 0.08 k / 0.2 hp | 0.89 k / 2.7 hp | 0.21 k / 0.7 hp |
| Magma Bolts | E1F1 @req | 35 (25) | 20 | 0.44 k / 0.7 hp | 0.31 k / 0.6 hp | 1.44 k / 2.8 hp | 0.14 k / 0.3 hp | 1.05 k / 2.0 hp | 0.58 k / 0.8 hp |
| Magma Bolts | E1F1 @+2 | 45 (25) | 7 | 0.40 k / 0.5 hp | 0.46 k / 0.7 hp | 1.48 k / 2.7 hp | 0.26 k / 0.4 hp | 1.49 k / 2.2 hp | 0.69 k / 0.9 hp |
| Magic Duel | S1 @req | 100 (25) | 100 | – | – | – | – | – | – |
| Magic Duel | S1 @+2 | 100 (25) | 100 | – | – | – | – | – | – |
| Healing Light | S1N1 @req | 35 (25) | 20 | – | – | – | – | – | – |
| Healing Light | S1N1 @+2 | 45 (25) | 7 | – | – | – | – | – | – |
| Shadow Bolt | D2 @req | 45 (25) | 20 | 0.26 k / 1.0 hp | 0.25 k / 1.0 hp | 0.11 k / 1.2 hp | 0.18 k / 0.7 hp | 0.24 k / 1.0 hp | 0.02 k / 0.1 hp |
| Shadow Bolt | D2 @+2 | 55 (25) | 7 | 0.41 k / 1.2 hp | 0.42 k / 1.2 hp | 0.22 k / 1.3 hp | 0.30 k / 0.8 hp | 0.43 k / 1.2 hp | 0.04 k / 0.2 hp |
| Poison Darts | N1 @req | 35 (25) | 20 | 0.10 k / 0.4 hp | 0.04 k / 0.3 hp | 0.20 k / 1.6 hp | 0.02 k / 0.2 hp | 0.21 k / 1.0 hp | 0.25 k / 0.7 hp |
| Poison Darts | N1 @+2 | 45 (25) | 7 | 0.16 k / 0.6 hp | 0.07 k / 0.3 hp | 0.28 k / 2.2 hp | 0.04 k / 0.3 hp | 0.23 k / 1.4 hp | 0.39 k / 1.1 hp |
| False Fire | G1F1 @req | 35 (25) | 20 | 0.27 k / 0.9 hp | 0.10 k / 0.5 hp | 0.43 k / 3.2 hp | 0.04 k / 0.2 hp | 0.33 k / 1.6 hp | 0.03 k / 0.1 hp |
| False Fire | G1F1 @+2 | 45 (25) | 7 | 0.31 k / 1.0 hp | 0.10 k / 0.6 hp | 0.64 k / 3.6 hp | 0.05 k / 0.2 hp | 0.48 k / 1.9 hp | 0.07 k / 0.2 hp |
| Elf Shot | G1N1 @req | 35 (25) | 20 | 9 fat (0.1 men) | 10 fat (0.1 men) | 40 fat (0.4 men) | 7 fat (0.1 men) | 40 fat (0.4 men) | 6 fat (0.1 men) |
| Elf Shot | G1N1 @+2 | 45 (25) | 7 | 11 fat (0.1 men) | 11 fat (0.1 men) | 45 fat (0.5 men) | 4 fat (0.0 men) | 39 fat (0.4 men) | 9 fat (0.1 men) |
| Dance of Ephemeral Swords | G2 @req | 0 (25) | 10 | – | – | – | – | – | – |
| Dance of Ephemeral Swords | G2 @+2 | 0 (25) | 3 | – | – | – | – | – | – |
| Cloud of Dreamless Slumber | G2A1 @req | 30 (25) | 20 | – | – | – | – | – | – |
| Cloud of Dreamless Slumber | G2A1 @+2 | 30 (25) | 7 | – | – | – | – | – | – |
| Fire Cloud | F3A1 @req | 30 (25) | 20 | – | – | – | – | – | – |
| Fire Cloud | F3A1 @+2 | 30 (25) | 7 | – | – | – | – | – | – |
| Thunder Strike | A3 @req | 100 (25) | 50 | 0.33 k / 1.0 hp | 0.41 k / 1.1 hp | 0.87 k / 4.0 hp | 0.12 k / 0.4 hp | 1.10 k / 3.5 hp | 0.15 k / 0.4 hp |
| Thunder Strike | A3 @+2 | 100 (25) | 17 | 0.30 k / 1.0 hp | 0.32 k / 1.1 hp | 0.79 k / 3.9 hp | 0.13 k / 0.4 hp | 1.16 k / 3.5 hp | 0.08 k / 0.3 hp |
| Acid Rain | W3F1 @req | 30 (25) | 30 | 0.71 k / 1.7 hp | 0.34 k / 1.4 hp | 1.15 k / 6.2 hp | 0.09 k / 0.5 hp | 1.10 k / 4.6 hp | 0.34 k / 0.7 hp |
| Acid Rain | W3F1 @+2 | 30 (25) | 10 | 0.93 k / 2.2 hp | 0.28 k / 1.5 hp | 1.50 k / 8.2 hp | 0.12 k / 0.6 hp | 1.37 k / 5.3 hp | 0.39 k / 0.8 hp |
| Blade Wind | E3 @req | 50 (25) | 80 | 2.21 k / 4.1 hp | 0.37 k / 1.5 hp | 3.34 k / 13.1 hp | 0.15 k / 0.6 hp | 1.03 k / 4.1 hp | 3.89 k / 5.8 hp |
| Blade Wind | E3 @+2 | 60 (25) | 27 | 2.64 k / 4.7 hp | 0.46 k / 1.7 hp | 3.67 k / 14.8 hp | 0.14 k / 0.6 hp | 1.10 k / 4.7 hp | 4.31 k / 6.3 hp |
| Nether Bolt | S1D1 @req | 40 (25) | 15 | 0.21 k / 0.3 hp | 0.15 k / 0.3 hp | 0.67 k / 1.4 hp | 0.06 k / 0.1 hp | 0.68 k / 1.1 hp | 0.05 k / 0.1 hp |
| Nether Bolt | S1D1 @+2 | 50 (25) | 5 | 0.26 k / 0.4 hp | 0.25 k / 0.4 hp | 0.75 k / 1.5 hp | 0.05 k / 0.1 hp | 0.80 k / 1.2 hp | 0.08 k / 0.1 hp |
| Bolt of Unlife | D2 @req | 32 (25) | 20 | 0.63 k / 0.9 hp | 0.56 k / 0.8 hp | 0.57 k / 1.3 hp | 0.42 k / 0.6 hp | 0.56 k / 0.8 hp | 0.04 k / 0.1 hp |
| Bolt of Unlife | D2 @+2 | 34 (25) | 7 | 0.70 k / 1.0 hp | 0.74 k / 1.1 hp | 0.64 k / 1.3 hp | 0.45 k / 0.7 hp | 0.75 k / 1.1 hp | 0.04 k / 0.1 hp |
| Bane Fire Dart | D1F1 @req | 35 (25) | 20 | 0.04 k / 0.1 hp | 0.04 k / 0.1 hp | 0.10 k / 0.4 hp | 0.02 k / 0.1 hp | 0.12 k / 0.3 hp | 0.13 k / 0.2 hp |
| Bane Fire Dart | D1F1 @+2 | 45 (25) | 7 | 0.08 k / 0.1 hp | 0.07 k / 0.1 hp | 0.21 k / 0.5 hp | 0.03 k / 0.1 hp | 0.22 k / 0.4 hp | 0.15 k / 0.2 hp |
| Breath of the Dragon | N2 @req | 30 (25) | 20 | 2.1 men hit | 2.1 men hit | 6.8 men hit | 0.9 men hit | 6.9 men hit | 0.7 men hit |
| Breath of the Dragon | N2 @+2 | 40 (25) | 7 | 2.5 men hit | 2.7 men hit | 8.7 men hit | 0.9 men hit | 8.6 men hit | 0.9 men hit |
| Ephemeral Blast | G3 @req | 55 (25) | 10 | 0.35 k / 1.0 hp | 0.35 k / 1.0 hp | 0.68 k / 4.4 hp | 0.12 k / 0.4 hp | 1.21 k / 3.5 hp | 0.05 k / 0.2 hp |
| Ephemeral Blast | G3 @+2 | 65 (25) | 3 | 1.03 k / 1.8 hp | 0.88 k / 1.6 hp | 2.03 k / 7.5 hp | 0.39 k / 0.7 hp | 3.19 k / 5.9 hp | 0.16 k / 0.3 hp |
| Ghost Wolves | G3 @req | 5 (5) | 10 | – | – | – | – | – | – |
| Ghost Wolves | G3 @+2 | 5 (5) | 3 | – | – | – | – | – | – |
| Falling Fires | F3 @req | 50 (25) | 20 | 0.97 k / 1.7 hp | 0.60 k / 1.6 hp | 1.88 k / 6.8 hp | 0.17 k / 0.5 hp | 1.89 k / 4.6 hp | 0.36 k / 0.6 hp |
| Falling Fires | F3 @+2 | 50 (25) | 7 | 1.11 k / 2.0 hp | 0.43 k / 1.5 hp | 1.90 k / 7.1 hp | 0.15 k / 0.6 hp | 2.21 k / 5.7 hp | 0.43 k / 0.7 hp |
| Hidden Flame | F3S1 @req | 55 (25) | 20 | 0.07 k / 0.5 hp | 0.07 k / 0.4 hp | 0.10 k / 1.7 hp | 0.03 k / 0.2 hp | 0.24 k / 1.5 hp | 0.01 k / 0.0 hp |
| Hidden Flame | F3S1 @+2 | 65 (25) | 7 | 0.07 k / 0.5 hp | 0.10 k / 0.5 hp | 0.11 k / 2.0 hp | 0.01 k / 0.2 hp | 0.31 k / 1.7 hp | 0.02 k / 0.1 hp |
| Falling Frost | W3 @req | 50 (25) | 20 | 0.61 k / 2.0 hp | 0.24 k / 1.2 hp | 0.84 k / 6.6 hp | 0.05 k / 0.4 hp | 0.73 k / 3.8 hp | 0.24 k / 0.7 hp |
| Falling Frost | W3 @+2 | 50 (25) | 7 | 1.12 k / 2.6 hp | 0.39 k / 1.8 hp | 1.47 k / 9.2 hp | 0.14 k / 0.7 hp | 1.46 k / 6.0 hp | 0.50 k / 0.9 hp |
| Orb Lightning | A2 @req | 20 (20) | 20 | 0.13 k / 0.6 hp | 0.14 k / 0.5 hp | 0.25 k / 2.0 hp | 0.10 k / 0.4 hp | 0.53 k / 1.9 hp | 0.12 k / 0.5 hp |
| Orb Lightning | A2 @+2 | 20 (20) | 7 | 0.15 k / 0.5 hp | 0.13 k / 0.5 hp | 0.19 k / 2.0 hp | 0.07 k / 0.3 hp | 0.41 k / 1.8 hp | 0.09 k / 0.4 hp |
| Earthquake | E4 @req | 0 (25) | 300 | 1.38 k / 5.8 hp | 0.49 k / 3.1 hp | 1.78 k / 18.3 hp | 0.11 k / 1.0 hp | 1.58 k / 9.8 hp | 0.63 k / 2.0 hp |
| Earthquake | E4 @+2 | 0 (25) | 300 | 1.34 k / 5.9 hp | 0.54 k / 3.1 hp | 1.78 k / 18.3 hp | 0.12 k / 1.0 hp | 1.56 k / 9.8 hp | 0.61 k / 2.0 hp |
| Gifts from Heaven | E3S1 @req | 100 (25) | 50 | 1.11 k / 3.5 hp | 0.52 k / 2.2 hp | 2.15 k / 12.4 hp | 0.23 k / 0.9 hp | 2.08 k / 8.0 hp | 0.73 k / 1.5 hp |
| Gifts from Heaven | E3S1 @+2 | 100 (25) | 17 | 1.25 k / 3.5 hp | 0.54 k / 2.4 hp | 2.14 k / 12.5 hp | 0.19 k / 0.8 hp | 1.91 k / 8.0 hp | 0.75 k / 1.7 hp |
| Stellar Cascades | S2 @req | 35 (25) | 20 | 73 fat (3.7 men) | 68 fat (3.4 men) | 271 fat (12.9 men) | 30 fat (1.5 men) | 248 fat (12.3 men) | 26 fat (1.7 men) |
| Stellar Cascades | S2 @+2 | 35 (25) | 7 | 73 fat (3.4 men) | 75 fat (3.6 men) | 278 fat (12.7 men) | 35 fat (1.6 men) | 268 fat (12.6 men) | 28 fat (1.7 men) |
| Astral Geyser | S3 @req | 65 (25) | 20 | 0.11 k / 0.7 hp | 0.15 k / 0.7 hp | 0.18 k / 2.7 hp | 0.06 k / 0.3 hp | 0.36 k / 2.3 hp | 0.02 k / 0.1 hp |
| Astral Geyser | S3 @+2 | 75 (25) | 7 | 0.12 k / 0.7 hp | 0.14 k / 0.7 hp | 0.21 k / 3.1 hp | 0.05 k / 0.3 hp | 0.39 k / 2.4 hp | 0.01 k / 0.1 hp |
| Shadow Blast | D2 @req | 45 (25) | 100 | 2.27 k / 7.9 hp | 2.27 k / 7.5 hp | 1.13 k / 8.4 hp | 1.57 k / 5.3 hp | 2.09 k / 7.4 hp | 0.16 k / 0.9 hp |
| Shadow Blast | D2 @+2 | 55 (25) | 100 | 3.87 k / 9.8 hp | 4.05 k / 10.3 hp | 2.45 k / 11.9 hp | 2.95 k / 7.1 hp | 4.12 k / 10.5 hp | 0.24 k / 1.1 hp |
| Poison Arrows | N2 @req | 45 (25) | 20 | 0.23 k / 0.5 hp | 0.05 k / 0.3 hp | 0.37 k / 1.6 hp | 0.02 k / 0.1 hp | 0.19 k / 0.8 hp | 0.44 k / 0.7 hp |
| Poison Arrows | N2 @+2 | 55 (25) | 7 | 0.41 k / 0.8 hp | 0.11 k / 0.5 hp | 0.70 k / 2.8 hp | 0.04 k / 0.2 hp | 0.34 k / 1.5 hp | 0.77 k / 1.2 hp |
| Poison Cloud | N3A1 @req | 30 (25) | 20 | – | – | – | – | – | – |
| Poison Cloud | N3A1 @+2 | 30 (25) | 7 | – | – | – | – | – | – |
| Illusory Army | G3 @req | 6 (6) | 100 | – | – | – | – | – | – |
| Illusory Army | G3 @+2 | 8 (8) | 100 | – | – | – | – | – | – |
| Flame Eruption | F2 @req | 9 (9) | 30 | 2.00 k / 4.1 hp | 0.83 k / 3.0 hp | 3.01 k / 14.5 hp | 0.24 k / 1.1 hp | 2.74 k / 10.1 hp | 0.99 k / 1.7 hp |
| Flame Eruption | F2 @+2 | 11 (11) | 10 | 2.41 k / 4.2 hp | 1.30 k / 3.6 hp | 4.49 k / 16.6 hp | 0.42 k / 1.3 hp | 4.40 k / 11.9 hp | 1.14 k / 1.8 hp |
| Wrathful Skies | A5 @req | 0 (25) | 200 | – | – | – | – | – | – |
| Wrathful Skies | A5 @+2 | 0 (25) | 200 | – | – | – | – | – | – |
| Cleansing Water | W2 @req | 40 (25) | 20 | – | – | – | – | – | – |
| Cleansing Water | W2 @+2 | 50 (25) | 7 | – | – | – | – | – | – |
| Magma Eruption | E2F2 @req | 30 (25) | 50 | 1.41 k / 2.0 hp | 0.67 k / 1.6 hp | 3.35 k / 8.5 hp | 0.15 k / 0.6 hp | 2.10 k / 5.5 hp | 0.55 k / 0.7 hp |
| Magma Eruption | E2F2 @+2 | 30 (25) | 17 | 1.85 k / 2.5 hp | 1.04 k / 2.1 hp | 4.88 k / 10.3 hp | 0.37 k / 0.9 hp | 3.67 k / 8.1 hp | 0.70 k / 1.0 hp |
| Astral Fires | S4F1 @req | 65 (25) | 20 | 0.77 k / 1.7 hp | 0.90 k / 1.8 hp | 1.74 k / 7.6 hp | 0.39 k / 0.8 hp | 3.00 k / 6.0 hp | 0.30 k / 0.6 hp |
| Astral Fires | S4F1 @+2 | 75 (25) | 7 | 0.97 k / 1.9 hp | 0.89 k / 1.9 hp | 1.87 k / 8.0 hp | 0.38 k / 0.7 hp | 3.22 k / 6.6 hp | 0.27 k / 0.6 hp |
| Blast of Unlife | D3 @req | 33 (25) | 20 | 0.27 k / 0.4 hp | 0.27 k / 0.4 hp | 1.01 k / 1.8 hp | 0.13 k / 0.2 hp | 0.86 k / 1.2 hp | 0.07 k / 0.1 hp |
| Blast of Unlife | D3 @+2 | 35 (25) | 7 | 0.29 k / 0.4 hp | 0.30 k / 0.4 hp | 1.18 k / 2.1 hp | 0.14 k / 0.2 hp | 1.07 k / 1.4 hp | 0.08 k / 0.1 hp |
| Bane Fire | D3F1 @req | 60 (25) | 20 | 0.58 k / 1.5 hp | 0.36 k / 0.9 hp | 1.07 k / 4.4 hp | 0.13 k / 0.3 hp | 1.22 k / 3.0 hp | 0.25 k / 0.6 hp |
| Bane Fire | D3F1 @+2 | 70 (25) | 7 | 0.45 k / 1.4 hp | 0.35 k / 1.0 hp | 1.32 k / 5.2 hp | 0.13 k / 0.3 hp | 1.27 k / 3.2 hp | 0.29 k / 0.6 hp |
| Stream of Life | N3 @req | 55 (25) | 20 | 0.3 men hit | 0.2 men hit | 1.1 men hit | 0.1 men hit | 1.1 men hit | 0.1 men hit |
| Stream of Life | N3 @+2 | 65 (25) | 7 | 0.4 men hit | 0.3 men hit | 1.3 men hit | 0.1 men hit | 1.2 men hit | 0.1 men hit |
| False Horror | G3 @req | 0 (25) | 10 | – | – | – | – | – | – |
| False Horror | G3 @+2 | 0 (25) | 3 | – | – | – | – | – | – |
| Fire Storm | F5 @req | 0 (25) | 300 | – | – | – | – | – | – |
| Fire Storm | F5 @+2 | 0 (25) | 300 | – | – | – | – | – | – |
| Ice Strike | W2 @req | 30 (25) | 20 | 1.37 k / 2.0 hp | 0.49 k / 1.4 hp | 3.16 k / 8.7 hp | 0.13 k / 0.5 hp | 1.40 k / 4.3 hp | 0.71 k / 0.9 hp |
| Ice Strike | W2 @+2 | 30 (25) | 7 | 1.99 k / 3.0 hp | 0.69 k / 2.0 hp | 4.09 k / 11.6 hp | 0.14 k / 0.5 hp | 1.79 k / 5.6 hp | 0.79 k / 1.1 hp |
| Acid Storm | W4F1 @req | 0 (25) | 300 | – | – | – | – | – | – |
| Acid Storm | W4F1 @+2 | 0 (25) | 300 | – | – | – | – | – | – |
| Rain of Stones | E3A1 @req | 0 (25) | 100 | – | – | – | – | – | – |
| Rain of Stones | E3A1 @+2 | 0 (25) | 100 | – | – | – | – | – | – |
| Nether Darts | S1D1 @req | 35 (25) | 15 | 0.68 k / 1.2 hp | 0.38 k / 1.1 hp | 1.22 k / 4.9 hp | 0.19 k / 0.6 hp | 1.24 k / 3.4 hp | 0.62 k / 1.0 hp |
| Nether Darts | S1D1 @+2 | 45 (25) | 5 | 0.87 k / 1.4 hp | 0.52 k / 1.2 hp | 2.32 k / 6.2 hp | 0.32 k / 0.7 hp | 2.15 k / 4.5 hp | 0.85 k / 1.3 hp |
| Cloud of Death | D4A1 @req | 30 (25) | 20 | – | – | – | – | – | – |
| Cloud of Death | D4A1 @+2 | 30 (25) | 7 | – | – | – | – | – | – |
| Wind of Death | D4A1 @req | 0 (25) | 100 | 4.0 men hit | 3.9 men hit | 16.4 men hit | 1.5 men hit | 13.4 men hit | 0.4 men hit |
| Wind of Death | D4A1 @+2 | 0 (25) | 100 | 4.9 men hit | 4.9 men hit | 20.4 men hit | 1.9 men hit | 16.6 men hit | 0.5 men hit |
| Stygian Rains | D3W2 @req | 0 (25) | 200 | – | – | – | – | – | – |
| Stygian Rains | D3W2 @+2 | 0 (25) | 200 | – | – | – | – | – | – |
| Storm of Thorns | N2 @req | 45 (25) | 20 | 0.34 k / 0.9 hp | 0.06 k / 0.5 hp | 0.54 k / 3.0 hp | 0.05 k / 0.2 hp | 0.25 k / 1.5 hp | 0.73 k / 1.1 hp |
| Storm of Thorns | N2 @+2 | 55 (25) | 7 | 0.71 k / 1.4 hp | 0.19 k / 0.8 hp | 1.24 k / 4.8 hp | 0.07 k / 0.4 hp | 0.58 k / 2.6 hp | 1.12 k / 1.7 hp |
| Poison Mist | N3A1 @req | 30 (25) | 40 | – | – | – | – | – | – |
| Poison Mist | N3A1 @+2 | 30 (25) | 13 | – | – | – | – | – | – |
| Shimmering Fields | G5 @req | 25 (25) | 200 | 1.71 k / 3.8 hp | 1.63 k / 3.9 hp | 3.41 k / 16.9 hp | 0.72 k / 1.6 hp | 5.71 k / 13.3 hp | 0.19 k / 0.5 hp |
| Shimmering Fields | G5 @+2 | 25 (25) | 200 | 2.53 k / 4.7 hp | 2.48 k / 4.7 hp | 5.66 k / 20.8 hp | 1.08 k / 2.0 hp | 9.19 k / 17.0 hp | 0.31 k / 0.6 hp |
| Wailing Winds | G4A1 @req | 0 (25) | 200 | – | – | – | – | – | – |
| Wailing Winds | G4A1 @+2 | 0 (25) | 200 | – | – | – | – | – | – |
| Pillar of Fire | F2 @req | 100 (25) | 20 | 0.24 k / 0.3 hp | 0.23 k / 0.3 hp | 0.73 k / 1.3 hp | 0.08 k / 0.1 hp | 0.70 k / 1.0 hp | 0.10 k / 0.1 hp |
| Pillar of Fire | F2 @+2 | 100 (25) | 7 | 0.22 k / 0.3 hp | 0.25 k / 0.3 hp | 0.75 k / 1.3 hp | 0.08 k / 0.1 hp | 0.80 k / 1.1 hp | 0.09 k / 0.1 hp |
| Chain Lightning | A3 @req | 25 (25) | 30 | 0.41 k / 1.3 hp | 0.45 k / 1.4 hp | 0.55 k / 4.9 hp | 0.24 k / 0.8 hp | 1.44 k / 4.9 hp | 0.11 k / 0.3 hp |
| Chain Lightning | A3 @+2 | 25 (25) | 10 | 0.56 k / 1.5 hp | 0.58 k / 1.6 hp | 1.00 k / 5.9 hp | 0.36 k / 1.0 hp | 1.93 k / 5.3 hp | 0.20 k / 0.5 hp |
| Meteor Shower | E5S4 @req | 0 (25) | 300 | – | – | – | – | – | – |
| Meteor Shower | E5S4 @+2 | 0 (25) | 300 | – | – | – | – | – | – |
| Astral Tempest | S5 @req | 0 (25) | 200 | – | – | – | – | – | – |
| Astral Tempest | S5 @+2 | 0 (25) | 200 | – | – | – | – | – | – |
| Vortex of Unlife | D5 @req | 40 (25) | 20 | 1.33 k / 1.9 hp | 1.20 k / 1.8 hp | 4.55 k / 9.5 hp | 0.58 k / 0.8 hp | 4.95 k / 7.1 hp | 0.18 k / 0.2 hp |
| Vortex of Unlife | D5 @+2 | 44 (25) | 7 | 1.83 k / 2.5 hp | 1.59 k / 2.2 hp | 6.37 k / 12.0 hp | 0.67 k / 1.0 hp | 5.97 k / 8.2 hp | 0.28 k / 0.4 hp |
| Aurora Borealis | G5S1 @req | 1 (1) | 200 | – | – | – | – | – | – |
| Aurora Borealis | G5S1 @+2 | 1 (1) | 200 | – | – | – | – | – | – |
| Flame Storm | F5 @req | 65 (25) | 100 | 3.91 k / 7.1 hp | 2.04 k / 5.8 hp | 7.40 k / 27.5 hp | 0.73 k / 2.2 hp | 7.39 k / 19.5 hp | 1.42 k / 2.3 hp |
| Flame Storm | F5 @+2 | 75 (25) | 100 | 5.23 k / 7.6 hp | 4.16 k / 7.2 hp | 13.73 k / 32.1 hp | 1.45 k / 2.8 hp | 14.17 k / 24.5 hp | 1.65 k / 2.4 hp |
| Lightning Field | A6 @req | 30 (25) | 100 | 0.08 k / 0.5 hp | 0.06 k / 0.4 hp | 0.12 k / 1.8 hp | 0.04 k / 0.3 hp | 0.28 k / 1.7 hp | 0.12 k / 0.8 hp |
| Lightning Field | A6 @+2 | 30 (25) | 100 | 0.07 k / 0.4 hp | 0.08 k / 0.5 hp | 0.13 k / 1.7 hp | 0.03 k / 0.3 hp | 0.22 k / 1.6 hp | 0.13 k / 0.8 hp |
| Niefel Flames | W5 @req | 65 (25) | 100 | 3.14 k / 7.7 hp | 1.21 k / 5.4 hp | 4.70 k / 27.7 hp | 0.38 k / 1.9 hp | 4.28 k / 17.8 hp | 1.33 k / 2.6 hp |
| Niefel Flames | W5 @+2 | 75 (25) | 100 | 4.23 k / 8.3 hp | 2.00 k / 6.6 hp | 7.65 k / 31.9 hp | 0.66 k / 2.3 hp | 7.42 k / 22.6 hp | 1.65 k / 2.7 hp |
