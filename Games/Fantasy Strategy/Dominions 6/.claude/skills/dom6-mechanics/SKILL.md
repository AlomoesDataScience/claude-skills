---
name: dom6-mechanics
description: "Dominions 6 rules and formulas from the official manual: dice, melee, missiles, armour, morale, magic and more, with page refs. Use when asked how a mechanic works, for odds, or for vanilla numbers to balance a mod."
keywords: "game, dom6manual, pdf, drn, shields, damage, types, resistances, fatigue, rout, leadership, penetration, gems, research, dominion, spread, scales, pretender, point, costs, blesses, economy, income, resources, recruitment, points, upkeep, supply, unrest, forts, sieges, movement, patrol, stealth, blood, hunting, turn, order, unit, spell, item, stat, manual's, tables, worked"
---

# Dominions 6 mechanics

Source: `dom6manual.pdf` (game manual, Illwinter, revision 2) in `Games/Fantasy Strategy/Dominions 6/Manuals/`. PDF page
numbers equal the printed page numbers. Everything below is from the manual; when a question goes
beyond it, look it up (below) instead of guessing, and say when something is not in the manual.

## Dice
Details: dom6-drn.

- DRN = 2d6, open-ended: a 6 counts 5 and that die is rolled again (and again). A lower-case drn
  is one open-ended die. "Check against 12" means value + DRN vs 12 + DRN.
- Chance that X + DRN beats Y + DRN (X − Y): −10 3%, −8 6%, −6 11%, −5 14%, −4 18%, −3 24%,
  −2 30%, −1 38%, 0 46%, +1 54%, +2 62%, +3 70%, +4 76%, +5 82%, +6 86%, +8 92%, +10 95%.
  Equal values lose more often than they win (46%).

## Missiles and spells that use precision (pages 65, 75-76)
Details: dom6-ranged-math, dom6-evocations.

- Missiles land in a square: past range > Precision/2 − 2 they deviate by range × 1.25 /
  Precision. Precision above 10 counts double. Any unit in the square can be hit, friend or foe;
  bigger units are hit proportionally more often.
- Hit roll: DRN + (size points in square)/2 (+2 magic weapon) vs DRN + 2 × shield parry −
  fatigue/20. No defence skill involved. Most missiles add half Strength to damage. Crossbows are
  AP. Lightning spells are AN, fire spells AP.
- Fort wall defenders: protection 30 wall with tower-shield defence, never run out of ammo, +20%
  range.

## Damage types (pages 66-68)
Details: dom6-battlefield (clouds, false/fatigue damage), dom6-abilities.

- Resistance works like protection, and then the remaining damage is cut by 2 × resistance %
  (resistance 15: −15 then −30%; 50 means immune). Against fatigue damage elemental resistance
  counts double (shock res 15 = 30 less fatigue from Thunder Strike).
- Fire: AP; burning chance = damage before protection × 4%; burns 1d(size)/2 per round (half with
  fire res 5+); fire res 10+, chill aura, mistform or ethereal can't burn.
- Cold: may freeze, +2d6 fatigue per round until thawed (25% + cold res + heat scale × 5).
- Shock: stun chance 5% + half the % hp lost.
- Poison: total spread over rounds (10% of the rest per round), −25% att/def per full hp worth of
  poison, max −50%. Poison res only lowers the initial total.
- Acid: rust chance damage × 4% (iron gear only). Bleeding: 10 fatigue + hp/20 per round,
  stops 10% + regeneration per round.
- Life drain: heals damage/2 and removes damage × 2 fatigue, max 150% hp + 10. Lifeless targets
  take 25%.
- Paralysis: duration (damage − size)/2 rounds. Fatigue damage: 100 unconscious, 200 max, beyond
  that 1 hp per 50. False damage (glamour): kills when real + false ≥ hp, fades 2/round when the
  glamour mages are gone.
- Clouds (always AN): frost/heat 1-5+ (2-6 fatigue, damage from level 3), poison, disease,
  sulphur, rust, death, shimmering, leeching, sleep. Monster auras make level 1 clouds (max 2).

## Fatigue, morale, rout (pages 62, 69-71)
Details: dom6-fatigue, dom6-morale, dom6-battle-ai.

- Each attack adds fatigue = encumbrance. Defence −1 per 10 fatigue, attack −1 per 20.
  Unconscious at 100 (recovers 5 per round).
- Squad morale = average morale of its members. Check: morale + DRN + survivor bonus (0-5) vs
  14 + DRN; failing routs the squad. Checks happen after heavy losses (one wound per two members,
  20%+ casualties), at 4 or fewer units after damage, near Fear, after fear spells, and every turn
  once the army has lost 50% of its hp. The army routs at 75% hp lost (mounts and province defence
  count 25%, slaves 50%). Killing or routing every commander routs the whole army.
- Morale bonuses: +1 friendly dominion, +1 home province, leadership bonus, Inspirational,
  Standard (best in squad), magic bonus −10..+1 (fear lowers, Sermon of Courage raises).
  Starving −4. Routing units have −4 defence.
- Leadership and squads: a commander leads up to its leadership in units in up to 5 squads.
  Leadership 10: −1 morale, −1 more per extra squad; 50: two squads free, −1 per extra; 100: +1
  for ≤3 squads; 150: +2 for ≤4; 200: +3 for five. XP adds +25/+50 leadership (poor leaders ÷5).
  Line, double line and sparse line need good commanders; sparse line and skirmish −1 morale.
- Mindless: morale 50 in the manual, never rout while led, dissolve (33%/round) without a leader,
  can't share a squad with non-mindless. Magic beings need magic leadership, undead and demons
  undead leadership; both together need undead leadership. Mixing undead or demons with living −1.
- Fear: check vs 10 (+1 per full 5 Fear) in 6 squares + the Fear value. Awe: attacker passes
  morale vs 10 + Awe or can't attack. Berserk: morale check vs 12 when wounded.
- Long battles: turn 100 all enchantments end (twilight), 150 attackers rout and darkness falls,
  170 defenders rout, 200 everyone left dies.

## Afflictions, XP, age (pages 38-41, 71)
Details: dom6-healing, dom6-abilities.

- Affliction chance = % of max hp lost in the hit; major chance = that / 1.5 (max 33%). Head: eye
  loss, mute / dementia, feeblemind, blind. Chest: chest wound / disease, never-healing wound.
  Arm: weakened / lost arm. Leg: limp / crippled. Limp −4 map move for commanders.
- XP: +1 per month, +4 for a won battle, +1 for a retreat, +1 per melee strike. Stars at 15, 50,
  100, 200, 400: each +1 att/def/prec/morale and +1 research, plus +str/+hp/−enc/+MR at some.
- Max age rises 50% per Nature level (Death for undead, Earth for inanimate, Blood for demons),
  −5% per Fire level.

## Movement, stealth, special orders (pages 47-55)
Details: dom6-stealth, dom6-sieges, dom6-blood-hunting.

- Half-step costs (leave + enter): plains 3, forest 5, waste 5, highlands 6, swamp 7, sea 5,
  cave 4, cave forest 6, crystal cave 6, drip cave 7; +4 enemy province (+3 if stealthy), +1 snow,
  roads −2 (min 2), survival −2 in that terrain. Flyers: 3 (cave 5), +1 enemy. Typical map move:
  heavy infantry 8, light infantry 14, light cavalry 20, flyer 20, commanders +2.
- Rivers only cross when both sides are cold +1 (frozen); mountain passes when both are heat +1;
  flyers, floaters and swimmers ignore rivers, flyers and mountain survival ignore passes.
- Movement into friendly provinces resolves before movement into enemy ones. Moving into a
  friendly fort province enters the fort (use Move and Patrol to fight outside it). Lone units in
  enemy provinces die.
- Patrol strength per unit = (precision + map move, or 30 if flying) / 20 + patrol bonus,
  commanders ×2, mindless/undisciplined ×½; minus unrest/2; + PD − 14. Found if patrol + 2d25 >
  stealth (leader's stealth − 1 per stealthy unit) + 2d25.
- Blood hunt: success needs 10% + 30% × blood level, pop/75 %, and not unrest/4 %; then d6 + blood
  level slaves and unrest + d(3 × slaves + 4).
- Siege: reduction strength vs repair strength (repair ×½; flyers ×2; mindless ⅛, animals and
  undisciplined ½ for repair). Storm once the walls reach 0. Fort supply in a siege = supply /
  turns of siege.
- Retreat: 75% "smart" (into the fort or a friendly neighbour), otherwise random; retreating into
  an enemy province kills. Weather: snow cold × 15%, rain growth × 10% + 10%.

## Turn order (pages 55-57, short)

Messages → research → recruitment → empowerment → forging → preaching → thrones → rituals →
remote attacks → magic battles → site searches → prophets → call god → awakening → blood hunt →
horrors → assassinations → friendly movement → other movement → battles → storming → globals →
events → item effects → sneak discovery → building → special orders → pillage → income → unrest →
starvation → upkeep → dominion spread → dominion effects → site effects → aging (midwinter) →
healing → mercenaries → heroes → PD conscription → scouting → elimination → victory. So recruits
fight the turn they arrive, and income comes after pillage.

## Reference files (read the one the step needs)

| File | Holds |
|---|---|
| `reference/looking-things-up.md` | **Looking things up** - scripts/gamemanualtext.py [PDF] [OUTDIR] (needs pdftotext) writes OUTDIR/rules.txt   (chapters, pages 1-98,  |
| `reference/melee-pages-58-64.md` | **Melee (pages 58-64)** - Details: dom6-combat-math, dom6-weapons, dom6-armor, dom6-mounts, dom6-abilities |
| `reference/magic-pages-73-81.md` | **Magic (pages 73-81)** - Details: dom6-magic-resistance, dom6-magic-duel, dom6-gem-casting, dom6-communions, dom6-research, dom6-site-s |
| `reference/dominion-and-pretenders-pages-30-37-82-8.md` | **Dominion and pretenders (pages 30-37, 82-88)** - Details: dom6-dominion, dom6-holy, dom6-pretender |
| `reference/economy-pages-22-29-42.md` | **Economy (pages 22-29, 42)** - Details: dom6-economy, dom6-sieges, dom6-blood-hunting |
| `reference/systems.md` | **Systems** - (borrow-from-games taxonomy; parts bin for our 4X, Heresiarch and others - 2026-11-03) - Time: simultaneous or |

## Related skills
dom6-wiki (community detail), dom6-inspector (numbers), dom6-tactics, manual-first, dom6-supercombatants and dom6-thugs
(tanks and counters), dom6-best-by-purpose and dom6-path-<path> (what is good), dom6-spell-db, rules-skills (how this set was made).
