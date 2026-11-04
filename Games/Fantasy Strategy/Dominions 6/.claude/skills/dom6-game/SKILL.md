---
name: dom6-game
description: Play an ongoing Dominions 6 game in the running client: the main map screen's hotkeys (province, commander, statistics, magic, map view, map filters, unit orders, gem transfer), what the screen shows (top bar, commander list, province panel), moving and zooming the map, browsing the menus, and the safety rules (never end the turn without the user's go: e and the end-turn button; nothing is final until then). Uses dom6-ui for guarded input and screen reading. Use when Claude plays or inspects a turn of a game in progress, needs a main-screen hotkey, or the user asks about the in-game interface.
---

# Playing a Dominions 6 game (main map screen)

Learned from the game itself (`?` on the map screen, hovering the top bar) on 2026-10-27, in
Claude's first game (MA Pythium, god Hortus Maximus). Input goes through dom6-ui's guarded
session (`session.run(work, name)`: waits for the user to be idle, stops if the game loses focus).
Strategy lives in dom6-knowledge (`play/strategy.md`, `plans/`).

## Safety rules (the user's)

- **Never end the turn without the user's go**: not `e`, not the end-turn button (top-right
  icon at about (1886, 20)). Ending a turn may raise a yes/no prompt; don't answer it unasked.
- **When in doubt, click the word**: the middle of the label's text, never the space between,
  beside or to the right of it. Take positions from OCR of the current screen (labels change
  width), and check that the expected window opened before clicking inside it.
- Ending a turn (`e`, on the user's go) gave no yes/no prompt on turn 1: it went straight to
  "AI thinking (n/36)" with a tip of the turn. Wait read-only (screen grabs, no input) until
  that text is gone. Check the game window itself (the terminal may cover it): turn 2 opened on
  the Messages list (season in the header).
- "A proclamation from X!" = X named a prophet; it quotes the god's full titles (build hints).
- Nothing is final until the turn ends, so orders, recruits and menus can be changed freely.
- Escape on the map opens Options (prefs): close it, change nothing.
- Don't touch the user's other games, the network or Steam.

## The screen (1920x1044)

- Title line: god name and titles. Second line: Treasury, Income (net of upkeep), gems
  (air, water, astral... with +per month). Hovering a gem: "Shift-click to pool ... gems".
- Left column: the selected province's commander tokens (name, unit count, order).
- Right panel: the province (terrain, population, income, resources, recruitment points,
  supplies, defence, unrest), Dominion (candles and scale icons), Buildings & Sites.
- Top-bar icons, left to right (tooltips show at the bottom centre; read them with
  dom6-knowledge `probe.tooltip`). x at y=20:

| x | Icon | x | Icon |
|---|---|---|---|
| 1255 | (t) Army Setup | 1598 | (F4) Pretenders of the World |
| 1291 | (r) Recruit | 1652 | (F5) Research |
| 1328 | (b) Bid for Mercenaries | 1688 | (F6) Global Enchantments |
| 1364 | (i) Province Chronicles | 1724 | (F7) Magic Item Treasury |
| 1418 | (m) Read Messages | 1760 | (F8) Magic Item Overview |
| 1454 | (s) Send Messages | 1797 | (F9) Thrones of Ascension |
| 1490 | (F1) Nation Overview | 1849 | (Esc) Options |
| 1526 | (F2) Score Graphs | **1886** | **(e) End Turn: never click** |
| 1562 | (F3) Hall of Fame | | |

  Row 2 (y=66): planes, (1) Pantokrator's Realm at 1812, unknown planes at 1851 and 1888.
- The menu background animates, so comparing screenshots to find changes fails; read texts.

## Provinces and commanders (the user, 2026-10-27; checked in game)

- **Right-click a province** to view it: its info fills the right panel. Most lines there are
  clickable (usually left-click). Provinces you can't see give less information.
- Back to the capital: left-click the god's name (title line), right-click the capital, or Home.
  Your provinces carry your flag.
- **Commanders** are the tokens on the left (those in the viewed province). Left-click selects
  (token turns white, tooltip "Name. Defend. (space) Change order..."); space opens the order
  menu; **left-click on the map moves** the selection there. A stealthy commander's order
  becomes **Sneak** and a grey arrow points to the target. Changeable until the turn ends.
- **The space order menu** (Theocratus, the start commander, turn 1) opens top-left over the
  commander column, titled with the commander's name; the map hides labels and flags while it is
  open. Groups (bars) and entries, with their tooltips:
  - *Move*: Defend "(D) ... the default order"; Patrol Province "(X) Try to find hidden enemy
    troops and reduce unrest by killing brigands"; Move; Pillage.
  - *Sacred*: Become Prophet, "spreads dominion like his pretender god but at a slower rate".
  - *Magic*: Empowerment "using large quantities of magic gems a commander can learn a new magic
    path or become better in one he already knows"; Blood Hunt "(B) ... very difficult ... without
    power in this path".
  - *Construction*: Demolish Fort, Demolish Lab (destructive, never pick these by accident).
  - Cancel at the bottom. Entries sit about 28 px apart, x≈100 (Defend y 90 ... Demolish Lab 430).
  The menu changes with the commander, the province and what has been researched.
- Prophet (space > Become Prophet; the token then reads "Prophet"): the user's rule is to name a prophet on turn 1 or 2 and let him expand (he spreads
  dominion and can claim thrones). The start commander (Theocratus the Centurion) has Become
  Prophet in his menu.
- **Army Setup** (`t`, or the first top-bar icon) for the viewed province. A header row (province
  picture, "Pythium, 0 units in garrison", then icons: units owned here 47, supplies 1230,
  supply needed 47, siege strength 47). One row per commander: token (tooltip "Theocratus the
  Centurion"), a green box, `<set battle orders>`, and on the right four numbers (tooltips: hover the **number's
  centre**, not its icon; see dom6-tooltips): squads used / squads led without morale penalty
  (bodyguards don't count), living units led / leadership, magic beings led / magic leadership,
  and the supplies he and his units need. Header: units owned here, supplies available, supply
  needed, siege strength. Mages show their path symbols under the name on the token. Under him, one strip per
  squad (20 and 25 units, "+1 morale" = commander morale bonus), each with its own box and
  `<set battle orders>`. Exit at the bottom. Tooltips there sit over the map and often fail to read.
  `2/3` = squads used / allowed (past 3, squads lose morale; the user).
- **Battle orders**, opened by a `<set battle orders>` bar (letters are their hotkeys):
  - *Commander* ("Set battle orders for NAME"): three script bars on top (the round-by-round
    script; the last shows the main order). *Single Round Orders* add a step: Hold one turn (w),
    Attack one turn (v), Fly Attack one turn (y). *Main Order*: None (n, he decides), Stay behind
    troops (s: casts spells, fires missiles, else gets behind the rearmost unit), Attack (a),
    Retreat (r). *Target* (for Attack): none, enemy archers, cavalry, fliers, large monsters,
    closest enemy, rearmost enemies. Checkbox: Conservative magic gem usage (-) (no unscripted gem
    spells, fewer gems used for fatigue). Ok closes and the bar then shows the order.
  - *Mage scripting* (Theurg Apuleius, Pythium, turn 6): spellcasters get two more Single Round
    Orders, **Hold or Cast a spell** (AI picks the spell) and **Cast a specific spell**, and two
    more main orders, **Cast spells** and **Advance and cast spells**. Cast a specific spell
    opens **Choose spell**: every battle spell grouped by school and research level with its
    path symbols; **greyed = this mage cannot cast it** (path too low). Scroll for more (the
    Divine/priest spells are last); Exit at the bottom leaves without picking. Right-click a
    spell for its card (range, casting time, area, precision, fatigue, effect, description;
    Exit (959, 665)). A picked spell shows in the top script bar as "(Spell name)" with
    **`<del>`** at its right end to remove it. Up to five script steps, then the main order
    (the orange bar). Default for a fresh Theurg: no script, Main Order None, target none, i.e.
    the AI decides (manual p. 45: "If a commander receives no orders, the AI will assign them").
    A scripted spell falls back to an AI pick if gems are missing or no target is in range;
    gem spells need the gems in the mage's inventory before the battle. Copy a script: hover it,
    ctrl+number; then hover another commander's `<set battle orders>` and press the number.
  - *Squad* ("Set battle orders for squad"): None (the commander decides), Attack, Hold and
    attack (hold two turns; archers fire instead), Fire (until out of missiles; advances if enemies
    are close), Hold and Fire, Fire and keep distance, Retreat, Guard commander (greyed when the
    squad is too big: at most 5 bodyguards for Theocratus). Same targets. Ok closes.
  - **Position Army** (left-click a squad's box in Army Setup; also a commander's green box): the
    battlefield. My side is the lighter green on the left, the enemy's the dark green on the
    right, so the front faces right. Squads are labelled boxes ("25 Alae Legionnaires",
    "20 Velites"); the commander is a grey/white circle. **Left-click a squad (its label, not the
    circle) to select it** (it turns white; the header shows its size); **right-click the field to
    move the selected squad there**. Formations, top right, for the selected squad: Line (1300, 69),
    Sparse line (1324, 93), Double line (1323, 115), Box (1473, 68), Skirmish (1489, 92); the
    chosen one is drawn bright. The squad picture and the field don't open unit info on right-click.
    **Select by the label at the squad box's top-left corner** (a click in the middle of the
    Velites box did nothing) and check the header's unit count before giving orders: an order
    goes to whichever squad is selected. The header's `<set battle orders>` bar (524, 97) opens
    the squad order window (Attack (739, 385), Fire (731, 441), Ok (959, 631)); the window's text
    is hard to OCR, so use these positions. Army Setup then shows each squad's order under
    its size, and its small green boxes show the formation shapes.
    Exit at the bottom (959, 949).
  - Formations (manual p. 59): Box = near-square block (default); Line = one rank facing the
    enemy; Double line = two ranks; Sparse line = gaps between squares, twice as long, −1 morale;
    Skirmish = checkerboard, −1 morale (Skirmisher ability cancels it; undisciplined squads must
    use it). Line, double and sparse need a good leader. One square holds 10 size points
    (three humans).
  - **Army Setup unit strips are live**: left-click a unit = select it (it lights up), then
    left-click another squad's strip = **move it into that squad**. alt+click selects every unit
    of that type in the squad; Enter deselects. Never click a strip by accident: a missed button
    click there selects or moves troops (it happened: a Legionnaire landed in the Velites).
    Right-click a unit = its unit screen (the name is in the title bar, e.g. "Alae Legionnaire
    from Pythium"; OCR misses the title, crop it). Velite and Alae Legionnaire sprites look alike.
  - **Click the order word itself.** Once a squad has an order, its `<set battle orders>` label
    shrinks to the order ("Fire", "Attack"); only the word opens the window. Check that the
    window opened (its "Main Order" bar and Ok) before clicking inside it.
  - A lone commander's Position Army has no formations: just right-click where he stands.
    Scouts: Retreat + far rear (left edge, about x 375), so they escape at once (the user).
  - The **target column ungreys** once a main order is picked; set it too (orders read
    "Fire closest" afterwards).
  - Clicks, full screen: commander bar (645, 344); squad 1 bar (1350, 430); commander window
    Stay behind troops (790, 523), Ok (959, 771); squad window Ok (959, 631).
- Map labels are drawn on the terrain and OCR misses them: click by screen position from a
  screenshot taken at the current zoom (labels move when zooming/scrolling; press Home first).
- Start army: a commander with a small force, plus one stealthy scout. Don't move the army
  turn 1 (no scouting info yet; first reports arrive next turn), except with some awake
  pretender builds.
- Scouting: independents never search for scouts, so scouts can go anywhere; enemy nations'
  province defence and patrols can catch them. A scout hidden in a province sees it better.
- **Province reports can be wrong about numbers** (rarely 30 reported, 80 there); what kinds of
  troops are there is generally not hidden.

## Screen reference (moved to SCREENS.md, 2026-11-03)
`SCREENS.md` here: the province panel line by line, the Recruit screen (Pythium lists), Research (F5),
Mercenaries (`b`), the other top-bar screens and every menu seen. Read it before using one of those screens.

## Map reading (taught turn 2)

- Dots between provinces are connections: **yellow** = passable, **red** = blocked (needs flying
  or another way), **blue** = water. They show around the selected/viewed province.
- Map mode can be changed to taste; its hotkey is in the `?` list.
- Owned dominion glows yellow at the province edges. After turn 1, right-clicking neighbours
  shows Scout Report boxes (top-left, "about N enemy units ... mainly X") for provinces a scout
  saw or that border yours; the box pushes the commander tokens down (Latinus at about (80, 255)).
- A Scout Report is only the one-line summary ("about N enemy units ... mainly X and Y"):
  hovering the enemy figures shows the same line, and clicking the box does nothing.
  Unscouted provinces show terrain only.
- The province panel title is a bar the scene reader can miss: OCR the box (1600, 100, 1900, 132)
  directly. Some hover tooltips (recruit portraits over the map) have a grey frame that probe's
  tan-frame finder misses: screenshot the band (300..1620, 930..1044) and read it.
- Recruiting in a captured province: right-click it, `r`. It offers that province's own
  commanders and units (Helmshire: Scout, Mounted Commander, Priest (temple needed); Militia,
  Light and Heavy Cavalry) and has its own commander point ("Recruitment points: 90 / 1").
  Resources are per province: a short one shows negative resources and a dimmed queued unit.
- `Return` on the main map can open Army Setup (it is not only "deselect"); check the screen
  before the next click.
- Unit order inside an army follows recruit order; it rarely matters (the user).
- Moving a new unit into a squad: Enter, click the unit in the garrison strip, click the squad
  strip; alt+click moves all of that type. A Standard in a squad shows "+2 morale".
- A movement order shows on the token ("Move", "Sneak") and as an arrow on the map; the hover
  tip reads "X. Move to Province (n)".
- **A move is one turn's reach.** Clicking a province beyond it gives an order to a nearer one
  (Picus, turn 7: clicked Gentle Woods, got "Sneak to Azimar", straight into our own attack).
  Check the order in F1 or the token's hover tip after every long move.
- **F1 Nation Overview finds hidden scouts:** "Sneaking commanders" lists them (order "Hide" =
  arrived, idle). Clicking a name jumps the map to him with his token **already selected**;
  clicking the token again deselects it, so just click the destination.
- `y` (Army setup at destination) shows the **viewed** province: right-click the target first.

## Battle replays (taught turn 3)

- Messages list: "There was a battle in X." with Goto province / View Battle. **`v` views the
  first battle** (the Messages `?` says so); clicking "View Battle" did not open it once.
- **Battle Summary** (the user): left-click the battle message's text in Messages (top-bar
  Messages icon reopens the list). It shows "conquered by our forces" or not, then each side's
  units with counts, a slash column (wounded, by the look of it) and a figure column (dead), and
  totals; View Battle and Exit. Clicking a unit's name opens a stat card (the Centurion's showed
  type stats: XP 0, generic text). Quicker than the replay's F1 overview for losses.
- **In the battle replay** (the user): click a unit's name to get its battle log; right-click
  any unit on the field to see what it is. Do it for strong mages and weird units.
- In the replay, **`p` pauses** (the user, 2026-11-03), `?` lists Battle Shortcuts. Camera: **arrow keys** move (a press is a small step,
  press 10-25 times), shift+arrows slowly, Page Up/Down raise/lower, middle mouse. Replay: n next
  round, x super slow, z slow, f fast, t turbo, **q exits**. Misc: g grid, w hide world, c team
  squares, **r round counter** (top right, "Combat round N"), **1-4 battle log detail** (4 = every
  attack, damage and protection roll), +/- scroll log, hold Tab highlights commanders, **F1 Unit
  Overview** (toggle), F2 weather & dominion, ctrl+i version. Manual p. 58 adds: s normal speed, v (viewing a unit) its combat log, w = wire-frame
  grid; +/- scroll the log (confirmed). Full table: dom6-battle-view "Replay keys".
- `space` pauses the replay (tip of the turn). Top-right icons at y 34: pause (1676), slow motion z (1714), play, fast, turbo, then a list.
  `n` did nothing while paused in one test; clicking z resumed play.
- The log is dark text on a see-through white box at the top left: OCR it line by line
  (boxes 25 px high from y 44, dark text), or the words interleave.
- **F1 Unit Overview**: Type, Owner (flag), HP, FP (fatigue), XP, Status ("retreated", "dead",
  blank = still on the field). Our units first, then the enemy, then the rest of ours. Scroll it
  with the wheel; it keeps its scroll position between openings. Open it after the rout for
  casualties.
- Battle 1 (Helmshire, turn 3): 53 + Theocratus vs 44 (4 Heavy Cavalry, 12 Light Cavalry, ~24
  Militia, 3 Mounted Commanders, a priest); the scout had said "about 30". Our spears and javelins
  did 0 to the heavy cavalry most hits but all 4 died; the light cavalry's bows bounced off
  shields. Routed by round ~13; we lost about 3.

## Mercenary bids, more

- OCR may read a whole merc row as one text ("Ferdinando's Footmen 200 <bid>"): click the
  `<bid>` word at x ~1107 on that row's y, then check the dialog names the company.
- The Land column is the province being viewed when bidding (bid while viewing where the
  company should arrive).
- Captured provinces recruit their own troops with their own resources and recruitment points
  (Nom: Jaguar Tribe Slinger 10g/2r/9rp, Warrior 10g/7r/9rp, Priest needs lab + temple).

## Turn-5 lessons (the user, 2026-10-27)

- **Resources are not kept between turns**: spend every province's resources each turn
  (captured provinces too, limited by their own recruitment points). Gold carries over.
- **Shift-click** on a recruit icon queues 10; shift-click on a number button (bid +) steps ~5.
- **Mercenary bids are paid once** (not monthly) for the 3-month contract. Two bids lost at
  210 and 320 to other nations: bid well over the minimum.
- Army Setup: **add a squad by clicking the commander's portrait**, not the red strip area.
  Select units in the garrison first (alt+click = all of that type), then click the portrait;
  each portrait click makes a new squad. Clicking an existing squad strip adds to it.
- `Esc` closes windows, but **on the main map it opens Options** (Quit without saving, Redo
  turn from scratch...). Close that with its Exit (959, 678) only. Don't press Esc on the map.
- A move order into a non-adjacent province shows only the first leg ("Move to Nom").
  Pythium–Copper Woods has no connection (mountains); go via Nom. Check the yellow dots.
- **Maintenance (upkeep)**: click **Income** in the top bar (top left) to see it; a unit's
  upkeep is also on its unit info page by clicking its morale (the user; not yet checked in game).
  Checked turn 5: clicking Income (330, 64) opens **Income Overview**: Income from Provinces
  (each province), Income from Units, Upkeep Cost for Units (per unit type; Theurg -10/month,
  46 Alae -30, 28 Velites -18), Exit (959, 651). The top bar's "(-105)" is that upkeep.
- **Buildings**: select a commander in the province, space, *Construction > Construct Building*:
  a dialog lists what can be built with prices; unaffordable ones are greyed. Turn 6, Ashenton
  (Pythium): Build Palisades (fort) 1000 gold, 5 months; Build lab 600; Build temple 600.
  Close it with its own Cancel (~959, 505). The god's order menu also has Research (click the
  word), Preach, Cast Ritual, Grand Communion, Forge, Alchemy, Search for Magic Sites.
- **Commander repeat** queues the commander again at the start of the next turn and pays for it
  then: the treasury shown at turn start already has the Theurg's 300 taken off.
- **Review every battle** with the **dom6-battle-view** skill (record from the Battle Summary,
  then report); lessons go into the dom6-tactics battle log.
- **Position every new squad** (the user caught this, turn 6; layouts, rules and the battle log
  are in the **dom6-tactics** skill): squads added in Army Setup and
  merc squads land stacked on one default spot. After changing an army, open Position Army
  (a squad's small green box) and lay it out: expendable troops in front, the main line behind
  them, missile troops behind that, flankers offset, commanders at the rear. Other
  commanders' squads in the province show on the same field (Urgek's Foul Spawn: a red box;
  red is not about position, it stayed red on our side). Right-click puts the box's centre
  roughly at the click; keep boxes left of the dark enemy half.
- **Undisciplined squads** (Foul Spawn mercs) show "undisciplined" where the squad order
  would be; it opens no order window. Set the commander's own order only.
- A move ordered through a province keeps going next turn by itself (Elbalus Pythium > Nom >
  Copper Woods). Two commanders entering the same province in a turn fight together.
- Captured-province recruits (turn 6): Murias Commander 55g/17r, Militia 7g/6r/3rp,
  Light Infantry 10g/7r, Heavy Infantry 10g/18r. Gold-cheap per resource: Alae (20r/10g) best.
- Theurg: 300 gold, 2 resources, **2 commander points**. Theurg Communicant 50 gold, max 1/month.
- Recruit screen of a captured province: commanders row y 233 (x 564, 653), units row y 469
  (x 567, 649, 736). Ashenton: Mounted Commander 70g/10r, Light Infantry 10g/10r/9rp,
  Light Cavalry 25g/9r/19rp, Cataphract 30g/40r/24rp.

## Map

- **Mouse wheel zooms** (wheel up = in) with the pointer over the map. Page Up/Down and
  Ctrl+Up/Down did nothing in testing.
- Arrow keys scroll; Home goes to the capital; `#` or `g` goes to a province number.
- Right click selects a province (per the hotkey list); click map = move/sneak the selected
  commanders there.
- Grey banners = independent provinces; dotted lines between provinces = movement paths.

## Hotkeys (from the game's `?` list; `?` is keysym `question`)

Misc: b mercenaries, c casualty reports, d recruit defence, **e end turn**, f fort info,
h hide menus, i province info and chronicle, m messages, o temple and dominion, r recruit,
s send messages, t transfer units (ctrl+t: selected commanders only), u patrollers, v battles
here, y units coming here.

Commanders: a select/deselect all, n next without orders, j previous without orders, + -
scroll, Return deselect all, > < token size, shift-click range, ctrl-click add, alt-click
same type, alt+shift-click same magic skills, ctrl+Home pretender, alt+Home prophet.

Statistics: F1 nation overview, F2 score graphs, F3 hall of fame, F4 pretenders. Magic: F5
research, F6 global enchantments, F7 item treasury, F8 item overview, F9 thrones.

Map filters: ctrl+f menu, ctrl+1 flags/forts, ctrl+2 armies, ctrl+3 dominion, ctrl+4 income,
ctrl+5 thrones/events, ctrl+6/7 troops in allied lands, ctrl+8 neighbours, ctrl+9 names,
ctrl+0 remote rituals, ctrl+m movement points, hold Tab income box. 1-9 planes. End zoom x0.5,
Insert fit screen, Delete whole map.

Unit orders (capitals): space order menu, A reanimate, B blood hunt, C cast ritual, D defend,
E break siege, F forge, G call god, H reacquire mount, I assassinate, J seduce, K blood
sacrifice, L pillage, M monthly ritual, O monthly forge, P preach, Q capture slaves, R research,
S search sites (ctrl+S auto), T storm castle, U summon allies, V pool blood slaves, W wait,
X patrol, Y shape change, Z blood slaves to lab. Map clicks: click move/sneak, shift raid,
ctrl move never sneak, ctrl+shift move & patrol, alt multi-move.

Gems from the lab: alt + f/a/w/e/s/d/n/g/b (one gem of that type), alt+Backspace returns one.

## The turn look (every turn, before any decision - the FoG II look process, 2026-11-03)
The user: "we redid the entire look process to be better and improved." Generic: photo-map, map-measure,
army-log, scouting, war-language. All on Claude's virtual screen with dom6bg.py (read only until the user says).
1. **Screen elements** known (dom6-map section 1; named regions in game-ui.json). New screen -> hover first.
2. **Messages first** (`dom6bg.py messages`): battles, deaths, events, spells. Record every battle replay
   (`dom6bg.py battle NAME`, detail `4` every replay), read the report, add it to the dom6-tactics log.
3. **Whole-map photo** (`dom6bg.py mapshot 6`), placed on the game's atlas (resnap.py); grow the atlas when
   new land is seen.
4. **Province board** in the game's plan file: owner, terrain, armies seen (with the turn seen), neighbours;
   diff with last turn - new flags, lost provinces, armies that moved.
5. **Enemy armies**: scout report of every foreign army in view (`goto`, `read scout`), classified (main
   types, commanders, pretender?), dated. Stale sightings marked stale.
6. **Our armies**: army-check per commander, army-log snapshot (both sides after each battle).
7. **Threats**: what can reach which province next turn (map move, roads, rivers), where our commanders
   and mages are exposed, where the enemy is weak.
8. **Then war-language**: UP (picture) -> THINK (plan, written) -> DOWN (orders, only with the user's go in his
   game) -> CHECK (photo after each order). End Turn only on the user's go.

## Looking without changing anything (the user's MP game, 2026-11-03: "click around, just don't change anything")
Safe: wheel zoom (pointer over the map), arrow keys, Home, `m` Messages -> "Goto province" / "Goto commander"
(camera only; a province with an enemy army shows its Scout Report top-left), **right-click a province
to view it** (panel fills; this skill's "Provinces and commanders"), F1-F9 overviews, tooltips.
NOT safe: **left-click on the map** (moves/sneaks the selected commander there), left-click on commander
tokens (selects them; the next map click would then be an order), anything in the order menu (space),
recruitment, research/spell queues, transfers, Return (can open Army Setup), Esc (Options), `e`/End Turn.
(Corrected 2026-11-03 - the user: "I believe it's right click, go check"; the first version said left-click.) Lock the virtual screen while looking; unlock when the user wants it.
Interface lessons that hold in every game (hover first, forecast vs commit, verify, popups): game-ui skill.

## Unit cards close by THEIR Exit - its height varies (2026-11-03, near miss in the user's MP game)
Right-click a unit in Army Setup = its card (Army Setup hides behind it). The card's height follows its
weapons/armour lines, so Exit moves: Tuatha Warrior (956,686), Sidhe Warrior (956,656), Fir Bolg Slinger
(956,684) at 1912x1000. Clicking a fixed point missed three times (landed outside the card; no effect - checked
with F1, orders unchanged). Always find Exit on a fresh shot before clicking, and check the screen after.
Army Setup's own Exit moves with its rows too (Vician 3 squads (956,708), Gila 2 squads (956,604)).

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

## Turn and battle tools (generic skills, Dominions settings - 2026-11-03)
Scripts in `AI Development/.claude/skills/<skill>/scripts/`. All read or write files only - none touch the game.
- **army-log** (`armylog.py`), one log per battle in the game's plans folder:
  `armylog.py new LOG.json --sides "Tir na n'Og,Pangaea" --states "Fighting,Routed,Dead" --routed "Routed,Dead"
  --break 75 --edge 50 --turns 150`. Dominions routs on **HP lost**, not units (dom6-morale p.70): every squad
  checks from 50% lost, the army routs at 75% - so put each unit's HP in `weight` (mounts and PD x0.25, slaves
  x0.5). `col,row` = battlefield square from Position Army or the replay grid (dom6-battle-view gridsnap);
  `ap`/`ammo` blank except archers (ammo). Fill from the Battle Summary + F1 Unit Overview, never from data files.
  Turn snapshots of our own stacks (strategic map) go in the game's plan file instead (tirnanog-scbm-game.md).
- **war-language** (`warlang.py up | think | down`), with `dom6-tactics/LEXICON.md` for the terms.
- **planning** (`plan.py new "Title" --dir "Games/Fantasy Strategy/Dominions 6"`) -> `plans/<slug>.md`.
- **combat-models** (`combat.py law A B ALPHA BETA --n 2`): first-look force ratio only (Lanchester square law
  for missile-heavy fights, n 1 for melee lines). Dominions numbers come from unit-combat-math / dom6-combat-math
  (per-attack odds from the real stats); combat.py says whether concentrating changes the answer.
  Round limits for any battle plan: 100 twilight (buffs end), 150 attackers rout, 170 defenders rout (p.71).

## Interface lessons that apply here (game-ui "Interface lessons", from FoG II - checked against Dominions)
- Hover before acting: tooltips sit in the bottom bar (dom6-tooltips); hover the centre of text, not icons.
- Forecast vs commit: in Dominions almost nothing commits until End Turn, but orders, recruits, research and
  gem transfers ARE changes - in the user's MP game look only (right-click views; left-click on the map = move).
- Popups: find the Exit by OCR of the popup's own bounds (`exitdialog`); stop loops when the screen stops changing.
- **Esc opens Options, not cancel** - close dialogs with their Exit; Return can open Army Setup.
- Verify every action with a fresh shot; leave the camera on the armies and the mouse parked (idle-view).

## Standards (audit 2026-11-03)
- **Screen:** coordinates here were measured on the 1920x1044 desktop. On Claude's 1912x1000 virtual screen (dom6bg.py / bgplay) find positions by OCR or re-measure - never reuse a stale coordinate (memory: apply tools universally).

## Related skills
dom6-ui (driving the window), dom6-tooltips, dom6-army-check (before End Turn), dom6-tactics, dom6-play, delegate, planning, manual-first.
Also (2026-11-03): dom6-scouting, dom6-battle-ai, dom6-map.
