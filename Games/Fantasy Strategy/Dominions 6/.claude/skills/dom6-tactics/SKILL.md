---
name: dom6-tactics
description: How to lay out a Dominions 6 army for battle and what has worked: Position Army (squad and commander placement, formations), squad and commander battle orders, leadership and morale limits per squad, the colour legend, Army setup at destination (y) for armies that meet in one province, plus a log of every battle fought with its setup and result and the lessons drawn. Uses dom6-ui for input and dom6-game for click positions. Use when setting up or changing an army, adding squads or mercenaries, picking formations or battle orders, planning a battle, or after a battle to record what the setup did.
---

# Dom6 tactics

Battles in Dominions 6 are not controlled live: the army fights from its **setup** (where each
squad and commander starts, in what formation) and its **battle orders**. This skill holds the
rules for that setup, the layouts that are known to work, and a log of every battle with what the
setup did, so the layouts get better with each fight. It is a living file: add to the battle log
and the lessons after every battle (the user asked for this, 2026-10-28).

Click positions and the screens themselves are in **dom6-game** (sections "Army Setup",
"Battle orders", "Position Army", "Turn-5 lessons"). Input goes through **dom6-ui**'s guard.
Strategy (what to attack) is in dom6-knowledge `play/strategy.md`; formulas in dom6-mechanics.

## Files

- Builds on the **dom6-ui** skill (guarded input, vision.py).
- Builds on the **dom6-game** skill (Army Setup and Position Army click points).
- Battles are reviewed with the **dom6-battle-view** skill (`battle_review.py`); its reports
  are in `dom6-battle-view/battles/`. The army checklist is the **dom6-army-check** skill.
- `expansion.md`: every independent type rated with what beats it, party size, pinging,
  frontage, formations, impact timing, Hold and Attack vs Attack, javelins, archer orders (from
  the illwiki expansion guide). Read it before attacking an independent province.
- `ai-casting.md`: how the battle AI scores and picks spells (Loggy's reverse engineering),
  and what to script because of it. Read it before scripting mages.
- `thugs.md`: thugs, supercombatants and how to kill them (the illwiki thug guide):
  the defensive onion, armour-defeating hits and fatigue, target choice, counters.
- The full guides are in the illwiki mirror: **dom6-wiki** (`wiki.py show PAGE`).

## Workflow: every time an army changes

1. **Army Setup** (`t` in the province, or **`y` = Army setup at destination**, which shows
   every army that will be in the target province next turn: use it when two commanders attack
   together). Put units into squads: select (alt+click or double-click = all of that type,
   shift+click = several), then click the **commander's portrait** for a new squad or an
   existing **squad strip** to add to it. Enter deselects.
2. **Orders** for each commander and squad (the order word or `<set battle orders>` bar).
3. **Position Army** (left-click a squad's or a commander's small green box). Lay out *every*
   squad and every commander. New squads and mercenaries land stacked on one default spot
   (the user caught this, turn 6).
4. Check the result on the small green boxes in Army Setup (they are mini-maps), then Exit.
5. After the battle: review it with **dom6-battle-view**, read the report, and **add a row
   to the battle log** with the setup and what happened. Turn a repeated result into a lesson.

## The field (Position Army)

- Left is the back, right is the front (we face right). The dark green right part is the
  enemy's half: keep every box on the light green side.
- Squads are boxes sized by their units, commanders are circles. **Select a squad by its label
  at the box's top-left corner** (check the unit count in the header), select a commander by its
  circle or from its own green box, or draw a rectangle to select a group. **Right-click** moves
  the selection; the box's centre lands roughly on the click.
- Formations (top right, for the selected squad): Box (default), Line, Double line, Sparse line
  (−1 morale), Skirmish (−1 morale). Line types need a good leader. Undisciplined squads are
  always Skirmish (manual p. 59).
- Colour legend (manual p. 44): white = selected; grey circle = commander; purple circle =
  commander with a Cast order; yellow = Retreat; grey box = squad with default orders;
  turquoise = Attack Rear; dark blue = Guard Commander; light blue = Hold and Attack;
  **red box = squad with undisciplined units** (not a position warning: tested, turn 6).

## Layout rules

From the user:
- **Commanders centred** on the army's line, behind the troops, not off to one side (turn 6).
- **Scouts**: Retreat order and the far rear (left edge), so they escape at once.
- Every squad positioned after any change (above).

From the manual (pp. 43-46, 57-60) and reasoning, to test:
- The whole army routs when **all its commanders are dead or routed**, or when it has lost 75%
  of its hit points. So commanders stay behind and centred, out of missile lines.
- Units halt in an enemy's **zone of control** when adjacent; routing units ignore it.
- One grid square holds 10 size points (three humans). Box = near-square block.
- Unassigned garrison units (no fort) fight as one big squad in the centre.
- Front to back that has worked so far: expendable or melee screen → heavy line (Alae with tower
  shields) → javelin and missile troops → commanders. Flank squads offset up or down.

## Leadership and squads (manual p. 59)

A commander leads at most 5 squads and no more units than his leadership. Morale effect by base
leadership: 10: −1 for one squad, another −1 to all per extra squad; 50: no penalty for 1-2
squads, −1 per extra; 100: +1 to all for up to 3 squads, −1 per squad above 3; 150: +2 for up
to 4, −1 to all with a fifth; 200: +3 for all five. The Army Setup row shows squads used/allowed
(Theocratus 2/3, Urgek 1/2) and units led (44/125). Mixing undisciplined units into a squad
makes the whole squad undisciplined with −1 morale; undead or demons mixed with living, −1.
Experience raises leadership (units led) but not these morale bonuses.

## Battle orders

- Squad orders (manual p. 45): None (the commander decides), Attack*, Fire*, Guard commander,
  Hold and attack*, Hold and fire*, Fire and keep distance*, Retreat. * = takes a target: None,
  Archers, Cavalry, Fliers, Large monsters (size 7+, else 6), Closest, Rearmost.
- Commander orders: None, Stay behind troops, Attack, Retreat, plus single-round steps.
- **Undisciplined squads take no squad orders** (Foul Spawn: the label reads "undisciplined" and
  opens nothing). Only their commander's order can be set. Tight Rein lifts this.
- In use: Alae Legionnaires and Velites "Fire closest" (javelins first); commanders "Stay
  behind troops"; Jaguar slingers + warriors in one squad "Fire closest".

## Battle log

| Reported | Province | Our setup | Enemy | Result | Notes |
|---|---|---|---|---|---|
| T3 | Helmshire | Theocratus: Alae + Velites squads | 44 independents | Won, ~3 lost | First fight. |
| T4 | Nom | Theocratus, 51 men | 43 Jaguar Tribe + a priest + animated bushes | Won, enemy routed round 13; 2 Velites dead | Enemy lost 19 dead. |
| T5 | Ashenton | Theocratus: Alae (29) + Standards (2) + Velites (17), Fire closest, Stay behind | 3 Mounted Commanders, 4 Cataphracts, 3 Light Cav, 25 Light Inf | Won; 1 Alae + 2 Velites dead (7 + 9 wounded) | Enemy lost 18. |
| T6 | Murias | Theocratus: 28 Alae + 2 Std, 15 Velites, Fire closest; Box (default) | 3 Commanders, 9 Heavy Inf, 4 Light Inf, 22 Militia | Won; enemy routed round 7; 1 Alae dead, 21 wounded | First reviewed battle (`dom6-battle-view/battles/t6_murias.md`). Enemy lost 22. Alae spear ~5 dmg/hit on Militia, ~1.4 on Heavy Inf; Velite javelins ~11/hit on Militia. Enemy Heavy Inf hit Alae 7 times for 3 damage total. Theocratus: Holy Avenger r0, Sermon of Courage r1, Word of Stone r3. |
| T7 | Copper Woods | Elbalus: Alae 19 + Std, Velites 13, Jaguars 14 (Fire closest); Urgek: 30 Foul Spawn in front; both commanders centred at the rear | ~60 Barbarians (two-handed swords and mauls, no shields) | Won; enemy routed round 5; all 30 Foul Spawn and 3 Velites dead | `battles/t7_copperwoods.md`. Barbarians lost 16. The Foul Spawn took the charge (13 barbarian hits, ~15 damage each, one dead per hit); the Alae took only 2 hits. Velites ~4.3 dmg/hit, Alae ~2.7. |
| T7 | Dragon Ridge | Theocratus: Alae + 2 Std, 15 Velites, Fire closest | 3 Commanders, 14 Archers, 20 Heavy Inf, 14 Militia | Won; enemy routed round 10; none of ours dead (27 wounded) | `battles/t7_dragonridge.md`. Heavy Inf hit Alae 23 times for 9 damage (0.4/hit); 32 archer hits did 14 damage in all. Alae spear 2.8/hit on Heavy Inf, 6.9 on Militia. Theocratus: Sermon of Courage r0, Holy Avenger r1, Word of Stone r3. |
| T8 | Azimar (ordered T7) | Elbalus (Alae 19 + Std centre, Velites, Jaguars lower flank) + Lampronius (18 Alae in Line on the upper flank front, 8 Velites behind), 71 men, commanders at the rear | ~40 Bear Tribe | — | First two-commander attack and first Line formation. Check: does the Line hold the flank? |

"Reported" is the turn the battle message arrived (the fight was during the previous turn's
processing). The squads' positions in the first four fights were set on turn 1 (Alae in front of Velites) and are not
recorded in detail; read them from Army Setup before the next Theocratus fight and fill in.

## Lessons (from the reviews)

- Alae Legionnaires (tower shield, armour) shrug off independent infantry: in Murias 7 Heavy
  Infantry hits did 3 damage in total. Their spears struggle against armour (~1.4 per hit on
  Heavy Infantry), so let javelins and Velites soften armoured enemies.
- Independents rout early (round 7 in Murias) once their commanders and a third of the men fall.
- **A chaff screen works against barbarians** (Copper Woods): 30 Foul Spawn soaked the charge
  and died to it, and the legion behind took 2 hits. Without it the Alae would have eaten those
  ~15-damage blows. The screen is spent, though: replace it before the next barbarian fight.
- Against archers + heavy infantry (Dragon Ridge) the legion alone was enough: tower shields
  turned 32 arrows into 14 damage in total. Heavy infantry independents are no threat to Alae.

## Open questions (test and record)

- Does "Fire closest" on Alae make them throw javelins and then close to melee on their own, or
  do they wait? Compare with "Attack closest" in a later fight.
- Line vs Box for the Alae front against Barbarians (frontage vs depth). The expansion guide
  says a line as wide as the barbarian blob (spears, repel) plus archers; test it in Copper Woods.
- How far behind the line should commanders stand to stay out of enemy missile range?
- ~~Does putting a screen (Foul Spawn) in front change our losses?~~ Yes (T7 Copper Woods, above).
- Does Line on a flank squad (Lampronius, Azimar T8) hold better than Box?
