---
name: dom6-thugs
description: "Basic thugging in Dominions 6: what a thug is, kitting, buff scripts, raiding, army thugs vs solo. Use when making, kitting, scripting or sending out a thug."
keywords: "commander, whose, job, melee, killing, leaders, casting, mages, far, end, illwiki, thugs-and-supercombatants, lucidtactics, tanking, video, choosing, chassis, mage, self-buffs, right, paths, high, base, stats, slots, sacred, bless, standard, kit, armour-piercing, two-hander, brand, protection, defence, stack, reinvigoration, stay, fatigue-neutral, regeneration, chip, damage, elemental, resistance, boots, messenger"
---

# Thugs (Dominions 6)

The user's ask (2026-11-03): "basic thugging skill". Sources: illwiki `thugs-and-supercombatants` (the definitions),
LucidTactics' tanking video (kits, timestamps; dom6-supercombatants has the full archetypes and counters),
manual for rules. Darkwolf's "Guide to Thugs and SC's" (9oUdOWyzkSw, 24:41, transcribed 2026-11-03 - section below); his
"Beginner's Guide to Self Buffs" (YQUBhca-oCU) is in dom6-buffs.

## What a thug is (wiki)
- A commander whose main job is to kill or disable enemies in melee - not an army leader (leads, morale) and
  not a casting mage (buffs, evocations from afar).
- **Army thugs** fight inside an army and kill what troops can't (a commander with a Greatsword of Sharpness,
  a quickened Sidhe Lord, a Storm Captain advancing with Shock Wave).
- **Solo thugs** take provinces alone: from PD-only raiders to commanders that beat whole armies (that end
  is the supercombatant). Need killing power for many weak units (Frost Brand, Fire Brand, Fire Shield) and
  survival. Their edge: one commander moves faster than an army (Boots of the Messenger, Cloud Trapeze,
  Teleport).

## Picking a chassis
- A mage who can buff himself (Earth: Iron Skin, Temper Armor; Air: Air Shield, Mistform; Astral: Body
  Ethereal, Astral Shield; Nature: Regeneration, Barkskin; Glamour: Displaced Body; Fire: Fire Shield).
- Good base stats (attack, defence, HP, natural protection), all item slots (some races get extra misc slots:
  Ashdod 3 in the video [39:14]), sacred for the bless (unholy weapons, regeneration...).
- Not a hero you can't replace; prophets and gods are SC territory (dom6-pretender).

## The kit (one per counter you expect)
- **Kill**: an armour-piercing two-hander for single targets and SCs, or a brand / Fire Shield for chaff.
- **Survive**: pick ONE main tank style - protection (natural + armour stack) or defence (Mistform, Shroud of
  Bewilderment, Vine Shield) - plus Air Shield vs archers.
- **Fatigue-neutral**: reinvigoration >= encumbrance, or you fatigue into critical hits (dom6-fatigue, dom6-armor).
- **Chip damage**: regeneration (ring, spell, bless).
- **Holes to close**: MR (Soul Slay, Holy Word, paralysis), fire and cold resistance vs brands and evocations.
- **Move**: Boots of the Messenger, or teleport magic.
- Price it in gems: Lucid's elf defence thug was ~30-35 gems [30:46] and died to two cheap fire mages - a
  thug is worth it only if the enemy can't answer cheaply.

## Scripting (dom6-battle-ai)
- Up to 5 scripted casts, cheapest and most important first, then Attack closest (or a target). Carry the
  gems for gem spells and boosts (a F1 mage needs a fire gem for a F2 spell [44:35]).
- Buffs and battlefield enchantments end at round 100 (manual p.71): a thug must finish the fight before then.
- Standing with friendly PD or troops gives time to finish the script [27:29].

## Using them
- Army thug: script to go for the enemy's thug, SC or mages; brands and AP weapons.
- Solo thug: raid PD and weak armies; scout first and avoid the province where its counter waits (defence
  thugs vs swarms, protection thugs vs AP, everyone vs evokers); set Retreat or pull back when the counter
  shows up.
- Test a kit before forging it: spells.py melee with the buffs, as done for Tir na n'Og's Sidhe vs White
  Centaurs (dom6-scbm tirnanog.md) - same method for one thug vs the likely defenders.

## Darkwolf's guide (9oUdOWyzkSw; video = below the manual, above the wiki; auto-caption names checked)
- **The job ladder** [01:22-04:33]: *thug* = kills unsupported troops/PD, cheap is fine ("if anything truly
  exceptional comes across it, it is going to die. But that is okay" - cost matters); *counter thug* = bare
  bones, 1-2 items, kills thugs/SCs (the Greatsword of Sharpness is the default for its armour piercing [02:29]);
  *supercombatant* = kills a whole stack and survives, so it is **tailored** to what it meets (shock resistance
  vs Storm Demons [03:01]); *army thug* = works only inside an army (Ice Shield seeded into the front line blinds
  attackers [04:03]); *heavy thug* = kills a small stack with mages if no counter is around.
- **Magic-phase movement** (teleport) is prized: it hits before the target can prepare [03:32].
- **Five survival tools** [05:06, 20:49]: defence, negation (avoid damage: ethereal, Mistform, Displaced/
  Personal..., Vine Shield), protection (armour, Stoneskin, Iron Skin; half damage from Temper Flesh, Liquid
  Body), regeneration, revival (Soul Vortex, Phoenix Pyre); plus awe and fear. Repel = high attack + long weapon.
- **Twilight** (round 100): self-buffs end, and for most thugs and SCs those buffs are what keeps them alive
  [05:36] - the fight must be won before then (manual p.71 agrees).
- **Buff the thug from outside** [07:03]: other mages cast on it. Two counter thugs quickened by a mage hit
  38 damage AP with two attacks and killed a regenerating Skratti thug that troops could not touch [08:05].
- **Defence chassis** (defence ~36, rarely hit by troops) [10:36]: answer with entanglement (Web), stopping it
  in place, berserk-inducing effects, or plain magic - not more troops.
- **Returning** procs at the end of a phase [18:43]: several attacks in one phase can kill before it fires.
- **Golems** (mindless): can't retreat, so they win or die - send enough or walk away [17:43].
- **Don't get landed on** [16:11]: an SC caught where it can't escape should be able to stealth out (a stealth
  bless or a stealth item passed from a scout) - why stealth is valuable.
- **Fatigue over ~50 is dangerous for a thug** [22:25] (critical hits, dom6-fatigue).
- **Cookbook if you want only basics** [23:26]: giants + regeneration; golems + Frost Brand and protection;
  elves + Vine Shield and a brand or Mace of Eruption, armour (barding if mounted); army thugs + Ice Shield;
  counter thugs + Greatsword of Sharpness.
- **Mods change thugs** [20:19]: spell-AI mods change which spells mages cast at them (more Shatter vs golems,
  Web vs elf thugs) - in SCBM check the .dm and dom6-scbm first.

## Related skills
dom6-supercombatants (archetypes and counters), dom6-combat-math (test a kit: spells.py melee), dom6-items,
dom6-buffs, dom6-armor, dom6-fatigue, dom6-battle-ai, dom6-stealth (raiding), dom6-mechanics.
