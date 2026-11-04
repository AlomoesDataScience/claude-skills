---
name: dom6-play
description: How to play Dominions 6 well, from the official game manual: setting up a game (eras, AI levels, thrones, settings), designing a pretender, the interface and hotkeys, a turn-by-turn checklist, expanding and running the economy, army setup, battle orders and mage scripts, research and gem use, spreading dominion, sieges, scouting, stealth and assassination, and playtesting a mod in a real game. Use when the user asks for help playing Dominions 6, wants a strategy, a pretender or army plan, advice on a turn or battle, or wants to test their mod nation in play. For exact formulas use the dom6-mechanics skill.
---

# Playing Dominions 6

Based on `dom6manual.pdf` (game manual) in `Games/Fantasy Strategy/Dominions 6/Manuals/`. The formulas behind every
tip are in the `dom6-mechanics` skill, and its `scripts/lookup.py` gives any vanilla unit, spell
or item. Advice marked *(reasoning)* follows from those rules but is not stated in the manual;
say so when giving it.

## The game in one paragraph

Each player is a pretender god leading one nation. Turns are months and are resolved for everyone
at once. You win by holding enough Thrones of Ascension (default) or by conquest, and you lose
when no province anywhere holds your dominion. Provinces give gold, resources, recruitment points
and supply. Forts collect resources and let you recruit, labs hold the research and gems, and
temples spread dominion. Battles are not controlled live: you set formations and orders
beforehand and watch the replay.

## Setting up a game (pages 14-18)

- Create World: pick map, then era. Early era has weaker troops and stronger mages; late era has
  the reverse. Each nation can appear only once.
- AI levels change the AI's gold, resources, recruitment and magic: Easy −30%, Normal 0,
  Difficult +30%, Mighty +60%, Master +100%, Impossible +150%. They get no bonus to commanders or
  holy points, and they know who owns which province.
- Settings: thrones of levels 1-3 and the ascension points needed (Thrones tab), or Conquer All.
  A Cataclysm turn forces an end. Unique artifacts are limited to one per turn and level-9 spells
  are learned one at a time by default. Score graphs change the game a lot: with them on,
  avoid leading any graph.
- Save a pretender design with Ctrl+S in the pretender screen and load it with Ctrl+L.
- Online: password your pretender or anyone can play your turn.

## Designing a pretender (pages 30-37)

For an actual design (cheapest chassis, bless points, costs, AI template) use the dom6-pretender skill.
To operate the running game itself (menus, new game setup, the pretender screen) use the dom6-ui skill.

You have 450 points. Spend them on a body (form cost), magic paths, dominion strength and scales.
Sleeping gives more points: Dormant +150 (awakens around a year in), Imprisoned +350 (around three
years).

- Magic: buying levels gets more expensive (8, 16, 24... each). A form that already has the paths
  you want is cheaper. Paths decide your blesses (each level above 1 is a bless point), your
  priests' Smite/Banishment variant (at 4+), the rituals the god can cast, and research.
- Dominion strength sets how fast faith spreads (50% + 5% per point per temple check) and your
  maximum dominion. It is also your sacred-unit recruitment cap in the capital.
- Scales: each step costs or gives 40 points. Taking bad scales pays for magic or dominion. Order
  and Productivity boost the economy, Growth helps supply and income, and Magic speeds research
  and lowers enemy MR. Steps of 4 or more have side effects.
- *(reasoning)* Match the blesses to your sacred troops: a nation with many sacreds wants bless
  points. An awake, fighting pretender (a "rush" god) needs survivability more than extra paths.
  A sleeping mage god gives a stronger late game.
- A god that dies loses a path level or a dominion point and needs about 50 priest levels of
  Call God. Immortal forms re-form instead (dominion-immortal ones only inside your dominion).

## Interface (pages 18-20, 55-58)

- Right-click a province to view it. Left-click a commander to select, then left-click a province
  to move. Right-click anything (unit, spell, item) for details.
- Province keys: e end turn, t army setup, y setup at destination, u patrolling setup,
  r recruit, b mercenaries, i chronicles, d buy province defence, f fortification.
- Nation keys: m messages, s send messages, gold or items, F1 nation overview (all commanders, PD,
  site searches), F2 graphs, F3 hall of fame, F4 pretenders, F5 research, F6 globals,
  F7 gem and item treasury, F8 item overview, F9 thrones. h hides the UI.
- Map: Ctrl+1-9 toggle layers. Ctrl+3 shows dominion, Ctrl+4 the income/resources capsule (unused
  hammers stay bright), Ctrl+8 neighbours. g jumps to a province by number. Home goes to the
  capital, Ctrl+Home to the god.
- Army setup: double-click selects all of a type, shift-click selects several. Over a squad,
  w selects the wounded, e selects units with 2+ XP stars and m selects the slowest.
- Battle replay: space pauses, f/t/s set speed, z is slow motion, v shows a unit's combat log,
  1-4 set log detail, F2 shows weather and scales, q quits.
- Shift+M repeats a ritual every month and Shift+O repeats a forge. To copy a mage's script,
  hover it, press Ctrl+digit, then press the digit over another commander.

## Every turn

1. Read messages (m): battles, events, research done and new heroes.
2. Recruit in every fort province (r). Check gold, the province's resources and recruitment
   points, and the commander slots. Units can be queued past the resources and recruitment points
   but not past your gold. Recruits arrive before battles, so recruiting is also emergency
   defence.
3. Put every mage that is idle in a lab on research (F5 shows the totals), or on forging, site
   searching or a ritual.
4. Give priests an order: preach (only up to twice their level), build a temple, or join the army.
5. Move armies, set formations and orders (t), and script the mages (gems in their inventory).
6. Spend spare gold on province defence where raids come, temples (600) and labs (600). Plan forts.
7. Scan Ctrl+4 for idle resources and F1 for idle commanders, then end the turn (e).

## Economy and expansion (pages 21-29, 42)

- Early game: take independent provinces with your starting army and one or two recruited
  commanders. Look at the defenders first (a scout, or the estimate shown on the province).
  *(reasoning)* Farms and rivers pay gold, while highlands, mountains and forests give resources
  and sites.
- Units need a commander to move. Units left alone in enemy land die. Armies move at the speed of
  their slowest unit.
- Forts: palisades cost 1000 gold and take 5 months. Upgrades cost 600 and take 3 months, up to
  your era's standard (masons go one level higher). A fort collects admin % of each adjacent
  province's full resources, but not from provinces that have their own fort. *(reasoning)* Space
  forts two provinces apart, next to resource-rich land.
- Income needs an unbroken chain of your provinces to a fort, and gems need one to a lab. Cut
  enemy supply lines to starve their treasury.
- Unrest cuts income and resources, and at 100 recruiting stops. Lower it with patrols, PD (−1
  per 10 points each turn) and Order scales. Enemy spies, blood hunting and some sites raise it.
- Upkeep is gold/15 each month (sacreds gold/30). Mercenaries are hired for 3 months by auction.
- Supply: big armies starve in poor provinces (morale −4, then disease). Forts feed provinces up
  to 4 away. Nature mages add supply.

## Armies and battles (pages 43-46, 57-72)

- A commander leads up to its leadership in units, in up to 5 squads. Mages often have
  leadership 10, so pair them with a real commander. Undead, demons and magic beings need the
  matching special leadership. Mindless units fall apart when their commander dies.
- The attacker deploys on the left, the defender on the right. In the setup box the left side is
  your rear.
- Squad orders: Attack, Fire, Hold and attack (holds 2 rounds), Hold and fire, Fire and keep
  distance, Guard commander (can also defend against assassins), Retreat. Targets: closest,
  archers, cavalry, flyers, large monsters, rearmost or random. Nothing holds forever.
- Commander orders: up to 5 scripted actions (hold, cast a named spell, fire, attack), then a
  general order (stay behind troops, attack, cast spells, advance and cast, retreat). Tick
  "conservative gem use" to save gems.
- Win by breaking morale, not by killing everyone. A squad checks morale after heavy losses, and
  the whole army routs at 75% hp lost or when every commander is dead or fled. *(reasoning)*
  Protect your commanders (guard squads, rear placement), and use flyers, assassins or long-range
  spells on theirs.
- Rules worth exploiting:
  - Long weapons repel attackers, best against low-morale troops.
  - Shields work best against missiles (parry counts double).
  - Missiles hit friends as well as enemies.
  - Armour piercing and armour negating attacks punish heavy armour.
  - Fatigue makes armour-defeating hits likely, so tired troops die fast.
  - Mages lose more fatigue in armour.
  - Blessing (H1) adds the god's blesses to sacred units.
- Formation: box for most squads. Line, double line and sparse line need good commanders.
  Skirmish and sparse line give −1 morale, and undisciplined squads always skirmish.
- Battles run to turn 200. At 100 all enchantments end. At 150 attackers rout, at 170 defenders
  rout, and at 200 whoever remains dies.
- Retreat: 75% of commanders retreat smartly into a fort or friendly land. A retreat into enemy
  land is death.

## Magic and research (pages 73-81)

- Research only happens in labs: 5 + 2 per magic level per mage, each turn. *(reasoning)* Early
  on, put most of it into the school with your best combat spells and a little into Construction
  (items) or Conjuration (summons). Level 9 spells are learned one at a time.
- Search for sites: a mage finds sites of its own path up to its level (max 4). Forest, waste and
  deep sea have the most sites. New gem income is the main way to grow magically.
- Gems: in battle a mage can spend as many gems per round as its level in that path. Each gem
  gives +1 level for one spell, never more than +1, and never a new path. Rituals and forging draw
  on the national pool in a lab. Alchemy converts 2:1 via astral.
- Empowerment buys a new path for 50 gems, then 15 × the target level. *(reasoning)* This is
  worth it on a cheap mage only for a key path.
- Globals: 5 slots by default. A new global tries to replace a random one when the slots are
  full, even your own. Kill the caster to end it, or dispel (Dispel is Astral 3, Enchantment 5).
  Extra gems make a global harder to dispel.
- Communions (Astral or Blood) let one master cast with +1 level per 2 slaves (+2 with 4), and the
  slaves share the fatigue.

## Dominion (pages 82-88)

- Conquest does not spread dominion. Faith comes from the god, the capital, temples, the prophet
  and claimed thrones. Each temple adds a check every turn, and every 5 temples add +1 to max
  dominion.
- Name a prophet early (one at a time; 6 turns to replace a dead one). It becomes priest 3+ and
  spreads like a temple.
- Preaching works only in its own province and only up to twice the priest's level. A temple there
  adds half a level.
- Friendly dominion gives +1 morale, and your scales slowly tip the land your way. Enemy dominion
  weakens your god and prophet (−1 str, −½ MR and −10% hp per candle).
- *(reasoning)* A god parked in its capital plus many temples makes a wall of faith. To finish a
  turtling enemy, besiege the last fort and push their dominion off the map.

## Sieges, scouting and stealth (pages 30, 49-54, 71-72)

- A defended fort must be besieged until its walls reach 0, then stormed. Defenders inside repair
  the walls. Wall defenders shoot with tower-shield cover and never run out of ammo. Relief armies
  fight before the storm.
- In a fort province, Patrol fights outside the walls, while Defend (the default) goes inside and
  is besieged. Move and Patrol makes an arriving army fight outside.
- Information:
  - A scout shows the army and the fort.
  - A priest also shows dominion.
  - A spy also shows income, sites, unrest and PD.
  - Scrying shows everything.
  - Owning a province reveals its neighbours.
- Stealth units sneak by default; hold Ctrl when giving a move order to make them fight. Spies can
  instill uprising (unrest) or infiltrate a capital (score graphs). Assassins strike a random
  commander. Bodyguards are present 50% of the time. Walls block assassins unless they fly,
  teleport or scale walls.
- PD of 15+ and patrolling armies find hidden units. Fast and flying units and commanders patrol
  better.

## Playtesting a mod in a real game

- Put the mod in the user data directory: `~/.dominions6/mods/<modname>/<modname>.dm` on Linux.
  Game Tools → Open User Data Directory opens it.
- Enable it in the mod preferences (dom6-ui `mods.py enable NAME` does it in the running game),
  then Create World. The game keeps the mod enabled for its
  players. Launch option `--enablemod <file>` (`-M`) does the same from the command line, and
  `--listnations` prints nation numbers.
- In game, Ctrl+I on a unit, weapon or spell shows its numbers and modding info. Check recruit
  costs, holy point use, leadership limits, upkeep (gold/15), and whether lab-only healing and
  sacred blessing behave as intended.
- A quick test: play the nation against Normal AI on a small map for 20-30 turns. Watch which
  units the replays show doing the killing, and whether research, gems and dominion keep pace.
  Report what was seen. A mod is not "balanced" until it has been played.

## War skills (the user 2026-11-02: call the military skills when playing; build on them)
- Level of war: **strategic + operational**; domain: **land (fantasy)**. Vocabulary: military-operations (FM 3-0) + military-doctrine; military-operations (strategic/operational levels, principles of war) + war-concepts' strategy section (total/limited war, escalation, war economy, war termination); soviet-doctrine for the
  opposing school; war-concepts (glossary, `warwiki.py look TERM`).
- Every turn / battle: **war-language** (UP: the situation in doctrine terms -> THINK: intent,
  form of manoeuvre, a task and purpose per unit -> DOWN: concrete orders -> CHECK) and **army-log**
  (read, log and evaluate both sides; `armylog.py`). Before the first real game write
  **`LEXICON.md`** in this skill folder (`warlang.py lexicon`): units -> roles, terrain -> OAKOC,
  rules -> effects, victory -> end state, task -> game actions.
- combat-models: The user's land salvo system and Lanchester (concentrate; make fights square when stronger, linear when weaker).


## Standards (the user, 2026-11-03 - apply in every Dominions session)
- **Manual first** (manual-first): look a rule up in dom6-mechanics / the manual, then dom6-wiki, before acting
  on a belief. Order of truth: the game > mod files > the manual > videos > the wiki > what the user says (test it if he insists) > a hypothesis. Mod games: mod-docs rules; SCBM = dom6-scbm skill (its data and notes). Check the
  mod's .dm for changes before trusting vanilla numbers.
- **Commit only when absolutely certain.** End Turn only on the user's go for that turn (end-turn rule). Orders and
  battle setups are the commit in Dominions (no live control): every army through dom6-army-check first,
  failure case known (what if the battle goes wrong, who is exposed), never batch-script orders blind.
- **Acting alone** (delegate skill): write intent, bounds and report points in the plan file; self-review with
  the user's questions; hand back with a clear report.
- **Plan in doctrine** (battle-tactics, military-doctrine): roles for every army, the decisive point, concentrate,
  screen, protect commanders and mages; log lessons after every battle (dom6-battle-view -> dom6-tactics).

## Standards (audit 2026-11-03)
- **Where it runs:** prefer Claude's virtual screen (dom6-ui bgplay, dom6bg.py); lock while working, hand back after (hand-back).

## Related skills
learn-to-play (generic method; twin learn-to-mod), battle-tactics, map-usage, dom6-modding.
Also (2026-11-03): dom6-scouting, dom6-dominion, dom6-economy, dom6-research, dom6-best-by-purpose, dom6-battle-ai.
