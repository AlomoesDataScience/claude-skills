# How the battle AI picks spells (and what that means for scripts)

Distilled 2026-10-28 from Loggy's reverse-engineering notes on illwiki
(`wiki.py show user/loggy/castingai`, with the worked example in `user/loggy/castingaiexample`).
**Measured on Dominions 5 (5.54-5.57).** Dom6 may differ in detail; the broad rules match what we
see in replays. Use this to decide what to script and what to leave to the AI.

## Scripted spells

- A scripted spell gets **+1,000,000** to its score, so it is cast whenever it *can* be: the
  mage has the path (communion boost and one gem boost count), the gems are in his inventory, and
  a valid target is in range.
- Scripted spells skip the "stupid" check and the `#ainocast` check, and may spend gems even with
  conservative gem usage on.
- If a scripted spell can't be cast (no gems, no target), the mage falls back to the AI's choice.
- **So script everything that matters**, especially when the mage knows many spells: with more
  than 50 spell choices, every unscripted spell has a 1% chance per choice over 50 (max 50%) of
  not even being considered.

## How the AI scores an unscripted spell

1. **Can it be cast at all?** Wrong terrain or underwater, missing paths (communion and one gem
   boost count), gem cost it may not spend (conservative gem usage forbids unscripted gem
   spells), `#aibadlvl`/`#ainocast` → no.
2. **"Stupid" check** (unscripted only): battlefield-wide damage spells are skipped when we
   outnumber the enemy hugely (10-20 to 1) and they have fewer than 3 mages. Wrathful Skies,
   Fire Storm, Acid Storm, Astral Tempest and Meteor Shower have their own version of this.
3. **Battlefield-wide spells** (Doom, Wind of Death, mass enslave...) need enough enemies: each
   enemy unit counts 1 and each commander 3, against a small random number plus fatigue cost/200.
4. **Summons** score (att + def + str + hp) × 2, plus 4 × hp if ethereal, plus 4 × hp if trampler
   or fire-shielded, × the number summoned, × 2-3 if long-lasting, then randomised (×0.4-1.6).
5. **Battle enchantments** score 0 if already active. Some get high random scores (Soul Drain,
   Fire Storm, Wailing Winds, Grip of Winter, Wrathful Skies, Rigor Mortis for undead casters),
   while Rain of Stones, Astral Tempest, Quagmire, Solar Brilliance and Acid Storm get only d5,
   so **the AI almost never casts those unless scripted**.
6. **Everything else is scored square by square:** the AI checks the squares in range and adds
   up a per-unit score for each unit the spell would hit in the target square (and, for area or
   inaccurate spells, the squares around it). It then picks the best square.
   - **Single-target spells into a crowded square have their score divided by the number of units
     in it.**
   - **Distance:** an offensive spell aimed within 10 squares scores × 10 / distance, so **the AI
     prefers the nearest targets**. Farther aims score × 15 / distance (× 10 for precision under 20).
   - Precision 90+ (or a target within precision/3) counts as hitting the aimed square only.
7. **Final score = score × 100 / (fatigue cost + 90)**: cheap spells win ties.
   - If the cast would push the caster over 100 fatigue, the score is divided by 3 (except Drain
     Life and reinvigoration spells). **Unscripted mages avoid casting themselves unconscious;
     scripted ones don't.**

## The per-unit score (what the AI thinks a spell is worth on a target)

- **Damage spells:** damage after resistances, minus protection (armour-negating ignores it,
  armour-piercing halves it), capped at the victim's hp + 5. Then:
  - MR checks cut it by bands: MR ≥ penetration + 8 → ×2/3, +11 → ½, +14 → ⅓, +17 → ⅙...
  - Blockable single-target spells count ×2/3 (shields).
  - **If the target's resistance is at least the damage, the score is 0: the AI never casts an
    elemental evocation into enemies that resist it.**
- **Buffs:** worth more in rounds 1-2 (×2) and on the caster himself in round 1 (×2).
  - Ethereal ×10 hp; invulnerability ×50 hp if protection is low; Mistform ×5; Quickness ×4;
    Regeneration ×3-4 max hp; Stoneskin ×4 if natural protection < 13; Barkskin ×2 if natural
    protection < 8, otherwise almost nothing.
  - **Air Shield is scored ~0 if the enemy has no ranged units.**
  - Resistance buffs (fire, cold, shock, poison) score high only when the matching storm is up or
    the enemy has mages of that path; otherwise ~0.
  - +4 MR is near 0 if the enemy has no mages.
  - Power of the Spheres is a flat 25 for a mage: modest.
  - A buff the target already has scores 0. Capped buffs check the *total* already present (a unit
    with 10 fire resistance won't take another +10).
- **Debuffs and afflictions:**
  - plague ×10;
  - blind, confusion and rage ×5;
  - slow and decay ×4;
  - curse of stones and fire bonds ×3;
  - entangle, web, net and earth grip ×2;
  - sleep ×1.5;
  - Slime scores only by the victim's armour, so the AI rates it low.
  - Already-paralysed or long-stunned targets score ~0.
- **Fear and morale:** targets with morale 20+ are worthless to fear spells; routing targets
  count half.
- **Once one side has wholly routed**, offensive spells on it count ×3.

## Practical rules for our scripts

- **Script buffs for rounds 1-2:** the AI already likes buffs then, but only the ones it rates.
  - It won't cast Air Shield against an army without archers.
  - It won't cast resistance buffs unless it sees enemy mages of the right path.
- **Script the battle enchantments we want:** the AI scores Astral Tempest, Rain of Stones and
  Solar Brilliance at d5, so it nearly never picks them.
- **Leave the AI to aim damage spells only when the nearest target is the right one.** It aims at
  the closest juicy square. To hit far targets (enemy mages), use spells whose best target is
  far, or accept the AI's choice.
- **Unscripted mages stop before 100 fatigue; scripted mages keep casting into unconsciousness.**
  Keep scripts within the fatigue budget: count the casts' fatigue plus encumbrance.
- Gem spells: the gems must be on the mage before battle. Conservative gem usage forbids
  unscripted gem spells.
- **The AI uses resistance to choose:** fire evocations won't be aimed at fire-resistant blocks,
  so against a fire-immune army a fire mage casts something else, or nothing.
