# SCBM 1.13 spells: what changed, and what it means for Tir na n'Og

Source: SCBM loaded into the mod inspector (`data/inspector`, built 2026-11-03 with dom6-modinspector), full
table in `spell-changes.md` (`scripts/spellchanges.py build`). For one mage's paths:
`python3 -I scripts/spellchanges.py paths E2N2G1H2 --max-level 4 --real`.

## The pattern (844 spells touched: 102 new, 551 real changes, 191 AI-weight only)
The user's tl;dr holds: SCBM makes magic cheaper and easier to land.
- Gem costs down on 136 spells (up on 24): summons especially (Cave Drake 4E -> 2E, Fay Archers 10G -> 8G).
- Path level down on 87 spells (up on 11): Destruction E3 -> E2, Eagle-eyed Warriors N3 -> N1,
  Cat-eyed Warriors N3 -> N2, Iron Pigs E3N1 -> E2N1, Dance of Ephemeral Swords G2 -> G1.
- Research level down on 85 spells (up on 3): Mechanical Men 6 -> 4, Eagle-eyed Warriors 6 -> 4.
- Precision up on 144 spells (buffs set to 100 = never miss; damage spells +2..+3), battle range up on 58.
- Fatigue down on 21 spells (up on 6): Armor of Achilles 40 -> 15, Bewitching Lights 20 -> 10,
  Fascination 20 -> 10, Flying Shards 30 -> 20, Rust Mist 30 -> 20. Earth Grip went UP 10 -> 25.
- AI weights (`aispellmod`, `aiassmod`, `ainocast`) on 275 spells: the AI is steered off most buffs
  (Stoneskin, Ironskin, Blur, Enlarge, Shrink, Sermon of Courage -90, Strength of Giants...). **Anything the AI
  avoids must be scripted** or it is never cast. Steered toward: Earth Meld +40, holy words H3 +20..+100.

## Tir na n'Og's casters (SCBM nation 11)
Commanders: Fir Bolg Druid A1 G1 +rand, Sidhe Champion N1 G1 H1, Sidhe Lord N1 G2 H2, Bean Sidhe W1 N1 G1,
Baobhan Sidhe G2, Ri N2 G2 H2 (capital), Tuatha Sorceress N2 G4 H2 (capital). Heroes (random, one at a time):
Lugh F3 A2 N2 G3 H3, Dagda E2 N2 G1 H2, Ogma E2 N3 G1 H2, Malgven F1 W2 E2 G3 H3. No native earth mage.

## Changed or new spells that matter here (research Alt 4, Conj 2, Ench 2, Const 1, Evo 0 on 2026-11-03)
Earth (Dagda):
- **Destruction** Alt 4, E2 (was E3): range 30, 6 squares at E2 (+2 per E level), armour damage 5 to armour
  and shields, 40 fatigue. The user's pick against the White Centaurs.
- **Armor of Achilles** Alt 2, E1: range 30 (was 15), precision 5 (was 3), **15 fatigue** (was 40). One target,
  armour damage 10: cheap follow-up on a big armoured target (not natural armour, so not the moose).
- **Stoneskin** Alt 4, E2: +10 natural protection (max 15), range 15, never misses. AI never casts it - script it.
  Replaces Barkskin (+7, max 10): the two don't stack.
- **Earth Meld** unchanged (Alt 3, E2, 60 fat, 5 squares, no MR); the AI likes it (+40).
- Earth Grip Alt 1: fatigue 10 -> 25, range 25. Temper Armors Alt 2 E2 (5+ squares) - AI won't cast it.
- Iron Pigs (Alt 5 ritual, E2N1, was E3N1 and level 6), Mechanical Men (Const 4, was 6), Clockwork Soldiers:
  crafting/summoning options for the crafter role.
Nature:
- **Shrink** Alt 4, N2: range 30+5/lvl (was 20+2), precision 5. One target, MR negates; no effect on spiritforms
  (the moose). Script it (AI -95).
- **Gift of Eagle Eyes** NEW, Alt 2, N1: +4 precision on 5 +2/lvl squares, range 15, 30 fat - for the slingers
  and javelins. **Eagle-eyed Warriors** Alt 4, N1 (was N3, level 6): the whole-army version, 100 fat.
- **Awaken Trees** NEW, Alt 5, N2: 10 squares of trees, 40 fat (Alt 5 is next in the queue).
- Tangle Vines/Thicket: range 25, better precision. Gift of the Hare: 2+ squares. Heal: range 30.
- Cat-eyed Warriors Alt 5, N2 (was N3). Serpent Fang Arrows / Poison Ward: N2, bigger areas.
Glamour:
- **False Fetters** Ench 1, G2: range 25 (was 15), 2+ squares, precision 3, 10 fat - MR +DRN vs 20 to get free.
- Bewitching Lights (G1, 10 fat, precision 5), Fascination (G1, 10 fat, range 30), Ephemeral Bolt (more damage,
  precision 4), Dance of Ephemeral Swords G1. Blur / Group Blur: never miss now, AI won't cast - script them.
Holy (the prophet):
- Sermon of Courage unchanged in effect but AI -90: script it on the prophet. Final Rest area 3+2/lvl. Smite
  Demon more damage. H3 words (Word of Power, Claim Life...) are AI-favoured.
Air (Lugh, Druid): Lesser Arrow Ward NEW (Alt 2, A1, one target, air shield 80); Trueshot (+4 precision, +50%
  missile range); Lacerating Winds A1 (was A2).
