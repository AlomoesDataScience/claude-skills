# What the community guides say about combat magic (to weigh against our rankings)

Distilled 2026-10-28 from illwiki (dom6-wiki: `early_and_midgame_magic`, the expansion guide,
`fearbattleenchantments`, `user/loggy/castingai`). Opinions from multiplayer players; our own
rankings (`buffs-debuffs.md`, `kill-spells.md`, `evocations.md`) are measured with the combat
model. Where they disagree, test in a battle and record it.

## The early power spells (guide list)

- **Evocation:**
  - 1: Star Fires, Arcane Bolt;
  - 2: Solar Rays, Web, **Lightning Bolt**;
  - 3: Cloud of Dreamless Slumber, Shadow Bolt, **Magic Duel**;
  - 4: Breath of the Dragon, Ephemeral Blast, Fire Cloud.
  - **Research 5 (especially Evocation 5) is a general power spike.**
- **Enchantment:**
  - 2: Shroud of Splendor, Personal Regeneration;
  - 3: Shroud of Bewilderment, Gift of Giant Strength, Fire Shield, Regeneration;
  - 4: Spell Ward, Simulacrum, Twiceborn, Raise Dead, Cloud Trapeze.
- **Alteration:**
  - 1: Personal Barkskin;
  - 2: Personal Mistform, Blur, Personal Stoneskin, **Gift of Cheated Fate**;
  - 3: Mossbody, Group Blur, **Body Ethereal**, Barkskin, Earth Meld;
  - 4: Quickness, Mistform, Stoneskin, Curse of Stones, Group Barkskin, Swarm, Twilight, Arouse
    Hunger.
- **Construction:**
  - 2: Temper Armors;
  - 3: items (Greatsword of Sharpness stands out);
  - 4: Soldiers of Steel.
- **Conjuration 3:** Phoenix Power, **Summon Earth Power**, Call of the Winds.
- **Thaumaturgy:** 1 Personal Luck, 2 **Mind Burn**, 3 **Luck** (group).

Our plan (Evocation 2 → Construction 1 → Alteration 2 → Alteration 3) matches the guide's
"alteration buffball" path.

## The buffball

- **The best early strategy for nations with good troops and the right paths:** at Alteration
  3-4, layer every good buff onto the best troops.
  - **Body Ethereal is the defining spell:** most damage reduced to a quarter, on a whole
    square, from one cast.
  - Then Mossbody, Barkskin; at Alteration 4 Stoneskin, Group Barkskin, Mistform, Quickness;
    Luck at Thaumaturgy 3.
- **Buffs aren't linear:** a buff on an already buffed elite is worth more than on a fresh
  unit.
- **Army thugs** (mages with 5-15 gems of gear, typically a Greatsword of Sharpness) give the
  ball armour-piercing damage.
- Most answers to buffballs arrive at research 5+: big evocations and battlefield wipes.

## Midgame threats to prepare for

- **Battlefield wipes** at research 6-7: one mage, one spell, the whole army slowly dies.
- **Evocation spam** past Evocation 5: Falling Fires, Stellar Cascades, Earthquake.
- **Skeleton spam and fatigue lines:** Raise Dead and Horde of Skeletons, with Relief, Rigor
  Mortis, Quagmire and Darkness.
- **Turbo-communions:** communions of giants with regeneration, so they heal through the
  communion damage.
- **Army thugs; light supercombatants** (Invulnerability + Soul Vortex, Phoenix Pyre golems),
  usually needing Construction 5 items.
- **Remotes** (Mind Hunt, disease demons, Call of the Winds) become a real tool.
- **Chaff raiders:** scouts with the Amulet of the Dead or the Mirror of Trapped Images.

## Fear battle enchantments (Isitaris's simulation; Dom6 values, page marked unpublished)

- **Wailing Winds and Blood Rain** each hit 3% of the battlefield every 320 ticks (Dom5 Wailing
  Winds was 5%).
- **Blood Rain:** an unconditional frighten (−1 morale, max −5). A lone unit (a commander)
  must pass 5 + morale vs 14 + malus or rout. **Very good at routing commanders.**
- **Wailing Winds:** full fear, but only on units that fail 3d6 < morale. It's better against
  low-morale troops; with Blood Rain, it reaches medium-morale troops.
- The −morale decays: 50% chance a round to drop by 1.

## What the casting AI does with these (see dom6-tactics `ai-casting.md`)

- **Unscripted mages rarely cast these enchantments; script them:** Rain of Stones, Astral
  Tempest, Quagmire, Solar Brilliance and Acid Storm score only d5.
- **The AI won't cast resistance buffs or Air Shield unless it sees the threat**, and won't aim an
  elemental spell at targets that resist it.
