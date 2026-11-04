---
name: dom6-mechanics
description: Dominions 6 game rules and formulas from the official game manual (dom6manual.pdf): dice (DRN), melee, missiles, armour, shields, damage types, resistances, fatigue, morale and rout, leadership, magic penetration and fatigue, gems, research, dominion spread and scales, pretender point costs and blesses, economy (income, resources, recruitment points, upkeep, supply, unrest), forts, sieges, movement, patrol, stealth, blood hunting, turn order, and every unit, spell and item stat in the manual's tables. Use when the user asks how a Dominions 6 mechanic works, wants odds or numbers worked out, compares units or spells, or needs vanilla stats to balance a mod against.
---

# Dominions 6 mechanics

Source: `dom6manual.pdf` (game manual, Illwinter, revision 2) in `Games/Fantasy Strategy/Dominions 6/Manuals/`. PDF page
numbers equal the printed page numbers. Everything below is from the manual; when a question goes
beyond it, look it up (below) instead of guessing, and say when something is not in the manual.

## Looking things up

- `scripts/game_manual_text.py [PDF] [OUTDIR]` (needs `pdftotext`) writes `OUTDIR/rules.txt`
  (chapters, pages 1-98, columns untangled) and `OUTDIR/tables.txt` (every page in layout form, so
  table rows stay on one line). Default OUTDIR `/tmp/dom6manual/`. Each page starts `=== page N`.
- `scripts/lookup.py NAME [TABLES_TXT]` prints a whole table entry with its page: a unit's
  gold/resources/recruitment points and stats, a spell's row (and summoned creature stats), a
  ritual's description, an item. Example: `lookup.py "wind rider"`. The manual's tables only cover
  part of the game: for any vanilla unit, spell, item, site, nation or event with full stats and
  ids, use the `dom6-inspector` skill (`scripts/inspector.py unit "wind rider"`).
- `scripts/combat_calc.py table` (reproduces the page-13 odds) and
  `combat_calc.py melee --att --def --dmg --prot [...]` (hit chance, shield hits, mean damage per
  attack). Use it to check a mod unit against a vanilla one.
- `community-research.md`: rules the manual doesn't spell out, from illwiki (mostly Loggy's
  Dom5 disassembly): exact morale checks and the hidden "morale problems" counter, scout report
  error (scout ±30%, spy ±10%, scrying 0%), when the enemy AI burns gems, experience gain,
  spell timing ±500 ticks, the full Dom6 turn order, province defence thresholds. More in the
  dom6-wiki skill (`wiki.py`).
- Where things are: rules 13-89; nation lore 89-98; magic items 99-117 (path boosters 116);
  battle spells 118-140 (divine 131-132, unholy 136); summoning rituals 141-207; global
  enchantments 208-216; other rituals 217-240; nation index 241-429 (each nation: summary, then
  commanders and units with Gold, Res, Rec and full stats, then mounts); launch options 430-433.
- Row codes in the tables: `Mag: S1?2` = Astral 1 plus random picks, `Sacr` sacred, `Rec`
  recruitment points, `CS` combat speed, `MM` map move, AN armour negating, AP armour piercing,
  MR / MR- resisted / easily resisted, BE battlefield enchantment, NUW not underwater.

## Dice
Details: dom6-drn.

- DRN = 2d6, open-ended: a 6 counts 5 and that die is rolled again (and again). A lower-case drn
  is one open-ended die. "Check against 12" means value + DRN vs 12 + DRN.
- Chance that X + DRN beats Y + DRN (X − Y): −10 3%, −8 6%, −6 11%, −5 14%, −4 18%, −3 24%,
  −2 30%, −1 38%, 0 46%, +1 54%, +2 62%, +3 70%, +4 76%, +5 82%, +6 86%, +8 92%, +10 95%.
  Equal values lose more often than they win (46%).

## Melee (pages 58-64)
Details: dom6-combat-math, dom6-weapons, dom6-armor, dom6-mounts, dom6-abilities.

- Hit: Attack + DRN − fatigue penalty > Defence + DRN − fatigue penalty.
- Shield: if the attack beats Defence but not Defence + shield Parry (+ the same roll), it is a
  shield hit and the shield's Protection is added to the protection roll.
- Damage: Strength + weapon damage + DRN vs Protection + DRN (+ shield). Damage dealt = the
  difference. Two-handed weapons add 125% of Strength.
- Armour-defeating hit (ignores 25% of protection): protection roll of 2 always; 3 if the target
  has 50+ fatigue; 4 at 100+ fatigue. Immobilised or unconscious targets count as 100 fatigue.
- Hit locations: torso 50%, arms 20%, legs 20%, head 10% (head uses the helmet's protection, plus
  the shield on a shield hit). Reach: head needs attacker size + weapon length ≥ target size,
  torso one less, arms two less. A unit 2+ sizes bigger hits head 20% / legs 10%. Lizards and
  dragons count 2 steps lower, most quadrupeds 1.
- Weapon types: piercing −15% protection before the roll (stacks with armour piercing −50% for
  −65%); slashing +25% damage after protection and chops off a limb hit for ≥50% hp; blunt +25%
  damage on head hits. Multi-type weapons pick one type per attack.
- Shields break: break value = damage before protection (+50% slashing, +25% blunt) vs shield
  resistance = shield protection (+5 magic). ≥3× damages (−20% protection), ≥5× breaks (−50%).
- Repel: a defender with a longer weapon gets a free attack; if it hits, the attacker must pass
  morale + DRN − length difference vs 10 + DRN + half the margin, or abort. Low-morale attackers
  and claws/bites (length 0) are repelled more. Size 6+ wield weapons 1 longer.
- Multiple wielded weapons: attack − sum of their lengths (Ambidextrous reduces it), +1 enc per
  extra weapon. Bonus (natural) weapons have no penalty.
- Harassment: each melee attack received gives −1 defence, decaying quickly.
- Two-handed weapon while mounted: −3 attack.
- Order inside one attack: target, early strikeback (awe, petrify), repel, strikeback, attack
  roll, damage roll, defensive abilities (mirror image, luck...), limb cap (limb hit ≤ half max
  hp), damage redistribution, deal damage.

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

## Magic (pages 73-81)
Details: dom6-magic-resistance, dom6-magic-duel, dom6-gem-casting, dom6-communions, dom6-research, dom6-site-search, dom6-forging, dom6-summoning, dom6-rituals, dom6-buffs, dom6-blood, dom6-holy, dom6-spell-db.

- Cast needs the school researched to the spell's level, the path levels and the gems. Dual-path
  spells use gems of the first path. Fatigue for a battle spell × 1/(1 + levels above the
  requirement), plus base encumbrance + 2 × armour encumbrance per cast (so armour hurts mages).
  Spells with 100+ fatigue cost 1 gem per full 100.
- Penetration (MR negates): 11 + DRN + extra levels/2 vs MR + DRN + target's levels in that
  path/2; caster wins ties. "Easily" −4, "hard to resist" +4. Magic scale −0.5 MR per step.
- Interrupt: hit while preparing (half the cast time) = % hp lost + 25% chance (half for combat
  casters and mindless).
- Gems in battle: at most as many per round as skill in that path, +1 level max, only in paths
  the mage has. Communion: master gets +n levels per 2^n slaves; fatigue split; slave fatigue ×2
  if below the master, ×4 if below half, ×½ if above.
- Research per mage = 5 + 2 × total magic levels (± bonuses), min 1. Magic scale +1 per step.
  Divine Insight researchers: at most dominion-strength of them per lab.
- Empowerment: 50 gems for a new path's first level, then 15 × target level.
- Alchemy (in a lab): any gem → astral 2:1, astral → any 2:1.
- Forging: path level 1/2/3/4/5/6/7/8 costs 5/10/15/20/30/40/55/70 gems of each path. Level 9
  construction items are unique artifacts (one per turn by default; yearning ones half price).
- Rituals take the month, need a lab, take gems from the national pool. Max gems in one ritual =
  path level × 100. Local enchantments end when the caster dies.
- Globals: slots 3/5/7/9 (default 5). A new global replaces the same spell, else fills a free
  slot, else tries to replace a random one (maybe yours). Dispel contest: +1 per extra gem, +5 per
  caster level above the requirement, + DRN each. Caster death ends it.
- Indirect magic: Fire +10 leadership and +10 magic leadership per level; Air/Water/Earth/
  Glamour +10 magic leadership; Astral +20; Death +50 undead leadership; Nature +10 magic
  leadership, +10 supply, longer life; Blood +10 undead and +10 magic leadership. At level 3 and
  again at level 4: Fire res +5, Air shock res +5, Water cold res +5, Nature poison res +5, Blood
  hp +5; Earth +3 protection (3) then +1 affliction res (4); Astral +1 MR (4); Death rarely dies of
  age (3), +10 morale (4); Glamour false-damage regen (3), true sight (4).
- Divine spells need only holy levels: H1 Blessing, Banishment; H2 Sermon of Courage, Smite
  Demon, Holy Word, Holy Avenger; H3 Divine Blessing, Smite; H4 Fanaticism; H5 Divine Channeling.
  A pretender with 4+ in a path swaps Banishment and Smite for that path's version (page 81).
- Site search: the mage needs the site's level in its path (sites are level 1-4).

## Dominion and pretenders (pages 30-37, 82-88)
Details: dom6-dominion, dom6-holy, dom6-pretender.

The dom6-pretender skill's `pretender.py` applies these costs to every chassis of a nation.

- Pretender points: 450; Dormant +150 (appears ~1 year in), Imprisoned +350 (~3 years). Path
  level purchases cost 8, 16, 24... each (first point in a new path costs the form's new-path
  cost). Dominion candles above the base cost 7, 14, 21... (max 10). Each scale step 40 points
  either way; usually ±2 (attuned forms/nations go further); heat/cold give points only moving
  away from the race's preference, first 3 clicks.
- Bless points = sum over paths of (level − 1), plus nation bonuses. A bless costs the sum of its
  path requirements (page 33 lists them; * = passive, bold = only while the pretender is awake
  and alive). Blessing adds +1 morale and every chosen bless to sacred units.
- Pretender / prophet in dominion: per friendly candle +1 str, +½ MR, +10% hp; enemy the reverse
  (hp floor 10%). Pretender death: loses one path level (chance 50% + 10% per Nature level) or
  one dominion. Call God ≈ 50 priest-levels of points.
- Max dominion = pretender's dominion + 1 per 5 temples (× team size). Temple check chance = 50%
  + 5% × max dominion. Sources: pretender (one sure increase + two checks), capital, each temple,
  prophet, disciples (one check each), thrones (1-7).
- A check in friendly dominion raises it with 30% − 3% × current, otherwise passes to a random
  neighbour (and on through friendly provinces); in enemy dominion it lowers it with 50% + 5% ×
  max − 5% × enemy dominion. Crossing land/sea: 50% re-roll of the target.
- Preaching: 30% × priest level (+½ level with a temple) − 5% × enemy dominion (min 5%), only in
  that province, only up to 2 × priest level. Inquisitors count double vs enemy dominion.
  Heretic: 20% × heretic level to lower any dominion.
- Prophet: priest level +1 or 3 (whichever higher), spreads like a temple, +2 att/def/prec,
  dominion hp/str/MR like the god. A new one only 6 turns after the last died.
- No dominion anywhere = eliminated (you can win by pushing an enemy's dominion off the map).
- Scales tip toward yours each turn with 5% × dominion + 10% × difference. Per step: Order +3%
  income, +2% resources, +10% recruitment, −1 unrest, −2% events (Turmoil the reverse);
  Productivity +3% income, +15% resources; Heat/Cold −5% income, −10% supply per step from the
  race's ideal; Growth +0.2% pop growth/month, +10% supply, +1% income; Fortune +5% events, +10%
  good, +0.5% hero; Magic −0.5 MR, −10% spell fatigue, +1 research per mage, +50 start research
  (Drain the reverse). Extreme (4+) scales have side effects (page 86) and spread to neighbours.

## Economy (pages 22-29, 42)
Details: dom6-economy, dom6-sieges, dom6-blood-hunting.

- Income = population/100 × scale modifiers × (1 + fort admin/200), ÷ (1 + 0.02 × unrest). No
  income without a friendly-province link to a friendly fort.
- Resources ÷ (1 + 0.01 × unrest). A province without a fort uses half its resources; a fort uses
  all of its own plus admin% of each adjacent province's full resources (not sea for land forts,
  not provinces with their own fort, not enemy provinces).
- Recruitment points: 20 + pop/100 up to 5,000, then /200 to 10,000, /300 to 20,000, /400 to
  40,000, /500 above; then the fort bonus and Order ±10%. No recruiting at unrest 100+.
- Unit costs: gold = training, resources = equipment, recruitment points = rarity of the
  recruits; sacred units also need holy points (home province limit = current max dominion).
  Upkeep = gold / 15 per month (sacred and slaves / 30). Queue up to 250 per province.
  Vanilla examples (nation index): Slinger 7 gold / 2 res / 3 rec, Cardaces 10/8/9, Myrmidon
  15/29/21, Wind Rider (sacred flyer) 70/27/31, commanders 1-4 rec.
- Forts (gold, months, admin, extra commander slots, recruitment bonus): palisades 1000/5/15/+0/
  +50%, fortress 600/3/30/+1/+75%, castle 600/3/45/+1/+100%, citadel 600/3/60/+2/+125%, grand
  citadel 1000/5/70/+2/+150%. Age standard: early fortress, middle castle, late citadel; masons
  build one level higher. Fort supply to provinces = admin × 6 / (distance + 1), up to 4 away.
- Temples and labs 600 gold (some nations cheaper). Temples need a sacred commander to build,
  labs a mage. Gem income needs a link to a lab.
- Supply: 1 per 30 population up to 15,000, then 1 per 60, × growth and heat modifiers, + fort
  supply. Units eat size − 2 (size 1-2 eat ½, animals half). Starving: −4 morale, 5% disease (50%
  if already starving).
- Province defence: level N costs N gold (level 1 free), needs 10 population per point, −1 unrest
  per 10 PD each turn, patrols from 15 (PD − 14 patrol strength), extra unit types at 20.
- Unrest: max 500 or pop/10. Patrol removes unrest (−10 population per point removed).

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

## Systems
(borrow-from-games taxonomy; parts bin for our 4X, Heresiarch and others - 2026-11-03)
- **Time**: simultaneous orders, one turn = one month; a fixed 45-step resolution order decides who acts
  first (research 2, rituals 10, movement 24-25, battles 26, income 38) - order matters as much as the rules
  (manual pp.55-56; dom6-mechanics "Turn order").
- **Economy**: income = population/100 x scale modifiers x fort admin, divided by unrest; resources collected
  by forts from neighbours; recruitment points by population band; upkeep gold/15 - a chain of formulas, each
  with a lever (dom6-economy). Blood slaves: a risk economy (three chained checks, unrest as the price;
  dom6-blood-hunting).
- **Research**: magic schools x levels; research points from mages' path levels; legendary level 9 picked one
  at a time (dom6-research).
- **Population / Politics**: dominion = belief as a second territory layer on top of military control,
  spreading by checks from temples, prophet and god; scales (order, growth, magic...) tip provinces towards
  the god's choice; losing all dominion = elimination (dom6-dominion). A strong "belief map" system.
- **Production**: magic items forged by path and construction level, gem costs; summons as production in a
  different currency (dom6-forging, dom6-summoning).
- **Tactical combat**: autobattle from a setup (formations, positions, scripts of 5 orders + a general order)
  with no live control; opposed open-ended 2d6 for everything; harassment makes crowds win; morale per squad
  and army-wide rout at 75% losses; round limits (100 twilight, 150/170 routs, 200 death) (dom6-battle-ai,
  dom6-morale, unit-combat-math, dice-math).
- **Intelligence**: stealth strength vs patrol strength + 2d25 open-ended, both sides; scouts' reports can be
  wrong about numbers; PD 15+ patrols on its own (dom6-stealth).
- **Logistics**: supply from population and fort admin x 6 / (distance + 1), starvation -> disease; sieges as
  wall damage (strength squared) vs repair (strength squared / 2) (dom6-economy, dom6-sieges).
- **Characters**: commanders with leadership caps, mages with paths, heroes, a single prophet; afflictions and
  ageing by path (dom6-abilities, dom6-healing).
- **Modding**: plain-text .dm commands over every object; the mod inspector loads mods for reading
  (dom6-modding, dom6-modinspector, mod-diff).
- **UI**: thick - ~500 abilities explained only by hover; the inspector site and wiki fill the gaps.

## Related skills
dom6-wiki (community detail), dom6-inspector (numbers), dom6-tactics, manual-first, dom6-supercombatants and dom6-thugs
(tanks and counters), dom6-best-by-purpose and dom6-path-<path> (what is good), dom6-spell-db, rules-skills (how this set was made).
