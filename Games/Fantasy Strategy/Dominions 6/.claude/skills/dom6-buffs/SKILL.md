---
name: dom6-buffs
description: How buffs and debuffs work in Dominions 6, from the manual (pp. 62-65, 69, 76-77), illwiki and the dom6-spells rankings - kinds (self, one target, group area, army-wide, battlefield enchantments, items), coverage per cast (1 square = ~3 humans), range from where the caster stands, duration (the battle; ended at twilight round 100; battlefield enchantments end with their caster), what doesn't stack (skin spells, same spell twice, multiple elemental shields), what does (different stats from different spells), the magic morale bonus, MR on debuffs, AI-cast vs scripted buffs (SCBM AI-avoided buffs must be scripted), measuring a buff with spells.py, and self-buff packages for thugs. Use when choosing or scripting buffs and debuffs, ordering a buff script, kitting a thug, or when the user asks about buffs. Rankings: dom6-spells buffs-debuffs.md.
---

# Buffs and debuffs (Dominions 6, vanilla)

The user's list (2026-11-03). Manual pp.62-65 (protection, skins, shields), 69 (morale bonus), 75-77 (battle
magic, enchantments); dom6-spells buffs-debuffs.md (rankings, model).

## Kinds and coverage
- Self (caster only), one person, area N squares (1 square = 10 size points = ~3 humans), army-wide
  ("20+ squares"), battlefield enchantments (everyone of a side / everyone), items (constant).
- Coverage multiplies the effect: a 1-square buff needs ~10 casts for a 30-man squad (buffs-debuffs.md).
- Range from where the caster stands: Stay Behind Troops puts mages behind the last squad - range 5-10
  buffs barely reach the front; 15 usually does.

## Duration
- Battle buffs last the battle; all temporary magic ends at round 100 (twilight) (p.71); battle
  enchantments end when their caster dies (p.75).
- Debuffs with an MR check (dom6-magic-resistance); some wear off (morale bonus recovers ~1 per 2 rounds).

## Stacking
- The same spell twice doesn't stack. Skins don't stack with each other (Barkskin 7/max 10, Stoneskin 10/15,
  Ironskin 13/20 - the best one counts) (p.64; dom6-armor).
- Different stats stack: Barkskin + Blur + Eagle Eyes + Sermon all apply.
- Morale magic bonus caps at +1 (Sermon/Fanaticism) (p.69).
- Items + spells: check each (e.g. armour protection and natural protection combine by N + A - N*A/40).

## Scripting
- Scripted buffs go out in the script's order; unscripted mages pick by AI weights. SCBM marks some buffs
  AI-avoided (Stoneskin, Shrink, Blur, Sermon) - they only happen if scripted (dom6-scbm).
- Buff first, then damage: the first rounds decide most fights (dom6-morale).
- Gems for buffs that need them must be in the caster's inventory before battle (dom6-gem-casting).

## Measuring
`dom6-spells/scripts/spells.py melee OURS THEIRS --x nat+7,blur [--data SCBM]` vs plain, then x coverage.
Worked example (Sidhe vs White Centaur): dom6-combat-math.

## Thug self-buffs - Darkwolf's "Beginner's Guide to Self Buffs" (YQUBhca-oCU, 42:32, transcribed 2026-11-03)
Video = below the manual, above the wiki. Marked (?) = he says it's from memory; check the spell card / inspector.
- **Limits first** [00:40-01:59]: fatigue over ~50 makes a thug vulnerable, over 100 it's a sitting duck - a
  20-30 round PD fight can end at 70, an 80-round fight can't. Twilight (round 100) strips self-buffs. Only 5
  script slots: other mages' buffs ("point buffs") add layers the thug can't cast itself.
- **Layering is the whole idea** [17:43, 39:34]: every layer the attacker must pass multiplies - mirror image
  -> luck (75% of hits negated) -> Mistform -> half damage (Temper Flesh / Liquid Body) -> protection -> Twist
  Fate. Order of value [29:20]: **not being attacked** (awe, Shroud of Bewilderment, Astral Shield paralysis) >
  not being hit (defence, luck, ethereal) ~ absorbing damage (prot, half damage, regen); fewer attacks also mean
  less harassment, so defence stays high.
- Cheap/niche [03:30-09:20]: Eagle Eyes (+precision, casters); Charge Body (one use - skip); **Twist Fate**
  (negates the first successful hit - vital in one-big-hit thug duels and with Returning; Rabbit's Foot = item);
  Skeletal Body (pierce resistance - halves the lance charge from PD heavy cavalry, cheap); Cat's Eyes (dark
  vision underground); Mirror Image (strong only with high defence).
- **Resistances** [09:20]: cast only for the damage you'll meet (they cost fatigue and slots) - most often
  lightning (air elementals, Storm Demons, Lightning Bolt counter-casters); Air Shield for defence thugs vs
  arrows; Iron Will (area MR) vs Mind Burn / Frozen Heart casters.
- **Main self-buffs** [11:40-25:50]:
  - Skins: Ironskin best with natural prot; they differ in what they're weak to (dom6-armor).
  - Mistform: damage reduction (max 25), breaks on a magic weapon or a big hit; great vs chaff (manual: dom6-abilities).
  - Mossbody: in Dom6 it pops 25% of the time (?) - cast only if spare.
  - **Temper Flesh / Liquid Body: half slash, blunt and pierce damage** - the best general layer. Temper Flesh
    (+fire res) to kill, Liquid Body (wound fend, but -combat speed) to last; afflictions kill SCs.
  - Stygian Skin / Invulnerability: invulnerability (25 at D3), useless vs magic weapons - fine vs PD only.
  - Personal Luck (75% of successful hits negated); Body Ethereal (75%, no hit needed, magic weapons ignore it;
    a point buff); Personal Regeneration (10% HP a round); Personal Flight (reach the rear: commanders, mages).
  - Fatigue: **Summon Earth Power** (reinvigoration + easier earth casting) and Reinvigoration at the end of the script.
  - Temper Armor / Strength of Giants: point buffs only - get another mage to cast them.
  - Quicken Self: two attacks a phase **and double fatigue** - yes for counter thugs, think twice for fatigue tanks.
  - Ice Shield (protective force: 50% of hits -20 damage (?)) and Water Shield (+5 defence) - underwater only.
- **Hit negation** [26:00-31:30]: Astral Shield (paralyses attackers - "almost always very good"), Fire Shield
  (burns attackers, kills mounts that kick - elves suffer), Flying Shards, Shroud of Splendor (awe: morale check
  to attack; with fear/Wailing Winds), **Shroud of Bewilderment** (MR check to attack, then confused -
  true sight only weakens it), Flying Shield item (50% of hits +20 prot (?)).
- **Movement** [31:30]: Cloud Trapeze, Teleport (magic phase - hit before they prepare; why A2/S3 pretenders
  are valued). Magic Duel kills non-mindless astral thugs (S mages roll on base S) - golems are immune; Mind
  Blank negates it.
- **Late game** [34:30]: Invisibility (attack penalty, -9 or -5 (?); true sight/spirit sight beats it);
  Hell Power (complex); **Soul Vortex / Soul Drain + Phoenix Pyre** = the strongest combo: each revive costs
  fatigue (dom6-abilities: 30+d20) and the drain reinvigorates it away. Counters [38:14]: Soul Slay through the
  pyre; mindless/undead or small high-MR forces so the drain has little to feed on; spread out to reach
  twilight; fatigue and chest wounds (Life for a Life, Harm, wound axes) (dom6-thugs).
- **Starter kit**: Ironskin (or the right skin) + Temper Flesh/Liquid Body + Personal Luck + Mistform or Personal
  Regeneration + Summon Earth Power; resistances only for a known threat (dom6-thugs, dom6-supercombatants).

## Related skills
dom6-spells, dom6-combat-math, dom6-armor, dom6-morale, dom6-magic-resistance, dom6-gem-casting,
dom6-thugs, dom6-battlefield, dom6-scbm.
