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

## The province panel (right side), item by item (Pythium, 2026-10-27)

Left-click each line (middle of its text). Hovering gives a tooltip at the bottom (it follows the
mouse sideways on the map). Popups close with their Exit.

| Line | Click | Tooltip / what it says |
|---|---|---|
| Name (number) | nothing | none |
| Terrain | nothing | terrain effects, e.g. "Plains, Mountains (low income, excellent resources, more magic sites)" |
| Population | popup: growth breakdown | capital "ideal size for about 25000"; base growth 0.2%, density −0.2%, terrain −0.1% → −0.1% |
| Income | nothing | gold per month for this province |
| Resources | nothing | needed for metal armaments of units and commanders; local, not saved between months |
| Recruitment points `519 / 2` | nothing | units / commanders recruitable per month here |
| Supplies, Supply usage | nothing | one human-sized unit eats one supply; starvation if usage exceeds supplies |
| Defence `25+/-` | the **d** screen: gold left, defence level, unrest reduction/month, patrol strength, a picture of the Defence Units | (don't buy defence casually: it costs gold) |
| Unrest | nothing | unrest cuts tax; 100+ blocks recruiting |
| Dominion candle / scale icons | popup: dominion strength here and every scale's effect (Order 3: income +9%, resources +9%, events −6%, unrest −3, recruitment +30%; Productivity 2: income +6%, resources +30%; Magic 1: research +1 RP) | each scale icon's tooltip names it ("Order: 3") |
| Fortification | the **f** screen (fort stats) | "(f) Fort statistics" |
| Laboratory | nothing | none |
| Temple | the **o** screen (dominion stats, bless effect) | |
| A magic site (e.g. Cathedral of the Spheres) | popup "Magic Site Effects": recruits it enables, gems it produces | Cathedral: Arch Theurg, Battle Vestal; 5 astral, 2 air, 1 water a month. Swamps of Pythia: Hydra Hatchling, Hydra, Hydra Tamer |

- **Other provinces** (right-click, turn 1). An unseen province (Azimar, Fucan, Nom, Ashenton,
  Copper Woods, Saetica, Duvan, Clon) shows only its name (number), terrain and empty Dominion
  and Buildings & Sites headers. Helmshire (287), which has my dominion candle (one of the two
  converted provinces), also shows population, income, resources, recruitment points and supply
  usage, with Supplies "?". No defence, unrest, sites or armies. The commander column is empty
  unless my commanders are there. The yellow dotted lines go from the viewed province to its
  neighbours. Pythium shows only a red-and-yellow line toward Nom: probably the snowed-in pass
  (not checked).
- Province labels sit near the borders: right-clicking open land can hit the province behind it
  (a click north of Helmshire got Duvan). Check the panel title after each click.
- `probe.tooltip` finds the tooltip's frame, but the map shows through it and can hide the frame.
  If it returns "", OCR the band `(0, 940, 1590, 1044)` and drop the junk before the sentence.

## Recruit screen (`r`, or the second top-bar icon) — per province

Armies and recruiting are province-dependent: the screen recruits in the viewed province
("Recruitment in Pythium"). Two portrait grids: Commanders, then Units, each with an empty queue
strip under it and a "repeat recruitment" checkbox. Bottom: Gold, Resources, Commander Points,
Recruitment Points, Holy Points (sacred units), Reset recruitment, Exit. Hover a portrait for
"Name (gold, resources, commander/recruitment points[, max 1/month])"; a left-click would queue it.
Left-click a portrait = queue one (it appears in the strip below); **click a queued unit to
remove it**. "repeat recruitment" (click the words) keeps that list's queue for following
turns. Sacred recruits use Holy Points (the Theurg took 1). Check the bottom counters after.
Pythium turn 1 (full-screen hover points, commanders y 160/238, units y 475/556):
commanders Scout 35g, Assassin 80, Centurion 95, Legatus Legionis 150 (2 CP), Emerald Lord 125,
Serpent Lord 100, Battle Deacon 90, Theurg Acolyte 100 (2 CP), Theurg 300 (2 CP), Hydra Tamer 35,
Arch Theurg 565 (4 CP); units Slinger 7g/2r/3rp, Velite 10/10/9, Alae Legionnaire 10/20/9,
Hastatus 11/21/12, Principe 14/21/20, Triarius 15/29/25, Emerald Guard 20/30/31, Standard
20/21/21, Serpent Cataphract 45/41/41, Retiarius 10/1/9, Gladiator 10/1/9, Theurg Communicant
50/1/31 (1/month), Battle Vestal 15/4/14, Hydra Hatchling 35/1/15, Hydra 200/1/50 (1/month).

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
- In the replay, `?` lists Battle Shortcuts. Camera: **arrow keys** move (a press is a small step,
  press 10-25 times), shift+arrows slowly, Page Up/Down raise/lower, middle mouse. Replay: n next
  round, x super slow, z slow, f fast, t turbo, **q exits**. Misc: g grid, w hide world, c team
  squares, **r round counter** (top right, "Combat round N"), **1-4 battle log detail** (4 = every
  attack, damage and protection roll), +/- scroll log, hold Tab highlights commanders, **F1 Unit
  Overview** (toggle), F2 weather & dominion, ctrl+i version.
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

## Research (F5)

"Magic Research": Magic Schools (level, progress bar, RP left per school), Research speed, then
the Research Queue. **Click a school's name to queue its next level**; clicking again queues the
level after. **Click a queue entry to remove it** (remove from the bottom up, then click the
schools in the new order; the queue's entries are ~32 px apart from y≈484). The queue holds
**at most 9 entries** (the user). Research only happens with mages
on the Research order (space menu); turn 1 Pythium has none, so speed 0. School name points
(full screen): Conjuration (651, 168), Alteration (641, 204), Evocation (646, 234), Construction
(658, 264), Enchantment (661, 296), Thaumaturgy (659, 327); Blood Magic below.

## Mercenaries (`b`, third top-bar icon)

"Hire Mercenaries": Company name, Price (minimum), Employer, Bid, Land. Click `<bid>` (the word):
a dialog "X demands at least N gold", `- N +` (+ at about (1025, 440), steps of 1), Hire, Cancel.
After Hire the row shows your bid and the landing province. The bid is **charged once** (the
user), for a 3-month contract; highest bidder wins; when it runs out the old employer's bid
counts double that one turn (manual p. 29). Turn 1: bid 66 for Dagan, the Renegade Sage (Sage,
S1, adept researcher 8), landing in Pythium.

## Other top-bar screens (turn 1)

- Send Messages (`s`): a "Send Message" list: text message, gold, magic gems, blood slaves, magic
  item, diplomatic missive. Exit.
- F1 Nation Overview: one row per province (Inc., Unr., Res., Sup., S.U., Def., Sites icons,
  Searches) with its commanders and their orders underneath ("Theocratus Defend, commanding
  45 units"; "Latinus Sneak to Azimar (263)"), then "Sneaking commanders".
- F2 Score graphs: a row of nation banners to toggle, tabs Provinces, Forts, Income, Gem inc.,
  Blood inc., Research, Dominion, Army Size, Ascension Points; empty on turn 1.
- F3 Hall of Fame: Name, Nation, Kills, Exp.; empty on turn 1.
- F4 Pretenders of the World: Name (with nation banner), Relation, Controller (AI/Human),
  Blessing ("known" for my own). Scrolls (wheel). **Hover the name word** (not right of it)
  for "Nation info for X" at the bottom (low rows' tips can hide under the Exit); click the name
  for the nation info screen (description, National Features, recruits, sites, and "X worships
  the pretender NAME, TITLES": the titles hint at the god's build). Long info screens put Ok
  below the fold: scroll the wheel to reach it. Game 1 map: dom6-knowledge play/game1-pretenders.

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

## Menus seen (open by hotkey, close with Escape)

- F1 Nation Overview: provinces table (income, unrest, resources, supply, defence, sites,
  searches) and commanders with their orders.
- F2 Score Graphs: army size, provinces, ascension points, income, gem income, research...
- F4 Pretenders: every god, relation, controller (AI/Human), blessing.
- F5 Research: per school level and RP left, research speed, research queue.
- F9 Thrones: required ascension points and every throne with its points (the list scrolls).
  **Left-click a throne's name** for its effects: the unclaimed site effect, then "The throne must
  be claimed to gain the following effects" (ascension points, dominion spread, gems, gold,
  recruits, blesses). Exit closes it; closing it can shift the list, so re-read row positions
  after each popup. Game 1's list: dom6-knowledge play/game1-thrones.md.
- r Recruit: commanders and units lists, commander points, gold, holy points, recruitment
  points, resources, repeat recruitment, reset.
- d Recruit Defence: gold left, unrest reduction, patrol strength.
- f Fort info: administration, commander point bonus, recruitment point bonus, guards.
- o Temple and dominion: temples, converted provinces, dominion strength, spread chance, bless
  effects.
- i Province chronicle: description and events (e.g. a snowed-in mountain pass).
- b Mercenaries: companies, employer, price, bid.
