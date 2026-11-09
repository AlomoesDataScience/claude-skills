---
name: dom6-play
description: "How to play Dominions 6 well, from the manual: game setup, pretender, interface, a turn-by-turn checklist, expansion, war. Use when asked for help playing, a strategy, an army plan, or to test a mod nation in play."
keywords: "official, setting, eras, levels, thrones, settings, designing, hotkeys, expanding, running, economy, battle, orders, mage, scripts, research, gem, spreading, dominion, sieges, scouting, stealth, assassination, playtesting, real, advice, turn, exact, formulas, dom6-mechanics, skill"
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

## Reference files (read the one the step needs)

| File | Holds |
|---|---|
| `reference/designing-a-pretender-pages-30-37.md` | **Designing a pretender (pages 30-37)** - For an actual design (cheapest chassis, bless points, costs, AI template) use the dom6-pretender skill |
| `reference/interface-pages-18-20-55-58.md` | **Interface (pages 18-20, 55-58)** - Right-click a province to view it |
| `reference/economy-and-expansion-pages-21-29-42.md` | **Economy and expansion (pages 21-29, 42)** - Early game: take independent provinces with your starting army and one or two recruited   commanders |
| `reference/armies-and-battles-pages-43-46-57-72.md` | **Armies and battles (pages 43-46, 57-72)** - A commander leads up to its leadership in units, in up to 5 squads |
| `reference/sieges-scouting-and-stealth-pages-30-49-.md` | **Sieges, scouting and stealth (pages 30, 49-54, 71-72)** - A defended fort must be besieged until its walls reach 0, then stormed |

## Related skills
learn-to-play (generic method; twin learn-to-mod), battle-tactics, map-usage, dom6-modding.
Also (2026-11-03): dom6-scouting, dom6-dominion, dom6-economy, dom6-research, dom6-best-by-purpose, dom6-battle-ai.
