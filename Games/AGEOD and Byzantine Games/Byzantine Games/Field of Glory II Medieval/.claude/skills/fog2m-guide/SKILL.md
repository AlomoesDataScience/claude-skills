---
name: fog2m-guide
description: Guide to Field of Glory II - Medieval (Byzantine Games / Slitherine, 2021), a turn-based tactical battle wargame of medieval armies on a square grid with 3D models - where its manual (117 pages, text with page numbers) and the data and scripts copied from the install live, the manual's chapter map, how battles work (action points, Points of Advantage, shooting arcs and ranges, impact then melee, combat strength by ranks, four cohesion states tested on 2d6 with quality re-rolls, rallying, autobreak, pursuit), how it is built and modded (Archon engine BSF scripts, Squads.csv unit table, .s4f 3D models with per-unit animation .txt, global mods, map editor) and its link to Field of Glory - Kingdoms. Use when the user wants to play, learn or talk about Field of Glory II or Medieval, plan a battle, look up a combat rule, mod it, or borrow its combat and morale systems for our games.
---

# Field of Glory II: Medieval

Byzantine Games makes the tactical side of the AGEOD/Byzantine pair (the user, 2026-11-01). Installed
2026-11-01 for a look and **one game played together**, then likely uninstalled: everything worth
keeping is copied here. FoG II (ancient) is the same system with different armies.


**FIRST read `COMMANDS.md` (every hotkey and order). Before any battle read `PLAY.md` and `UNITS.md` (incl. its "Hypotheses to test" and "Game vs manual" lists) (this folder; UNITS = troop types, card terms, capabilities, army lists) - the play reference: banners, command, movement, ZOC, shooting tables, charges, POAs, cohesion, terrain, victory, hot keys. Read from the manual for playing, 2026-11-02.**

## Files

- `Manuals/FOG2 Medieval Manual Printer-Friendly.txt` (from the PDF; page markers are PDF pages,
  the printed page numbers run about 2x+ because spreads are 2 pages): the rules.
- `install/`: text copied from the install: `Data/Squads.csv` (360 unit types, one row each, with a
  comment row explaining the columns), `Data/Battle/Scripts/*.BSF` (38 battle-logic scripts:
  `CloseCombatLogic.BSF`, `FightMelee.BSF`, `FallBack.BSF`...), `Core/*.BSF` and `Core/*.TXT`,
  `Data/Battle/Units/*.txt` (each 3D unit's animation table), campaigns and tools text.
- Not copied: 3D models (`.s4f`, 1145) and textures (`.dds`, 6510), 7.9 GB.
- Read the rules with `manual.py grep "Manuals/FOG2 Medieval Manual Printer-Friendly.txt" REGEX`.

## Manual map (PDF page)

Introduction 6 · Nations 9 · Quick, Custom, Epic battles 26-32 · Multi-battle campaigns 33 · Battle
39 · Generals 46 · Deployment and orders 48 · Shooting 65 · Close combat 67 · Cohesion 73 · Banners
77 · Terrain 77 · Disorder 80 · Victory 80 · Multiplayer 87 · Hints 88 · Map editor 91 · Modding
102 · Appendices 103 · Tactics 107 · Design notes (AI) 111 · Field of Glory Kingdoms battles 114.

## How a battle works (in my words)

- Units of models (infantry usually 8 models in 2 ranks, cavalry 4; 30 or 60 men per model by battle
  size) on a square grid; each turn every unit spends action points to move, turn, shoot or charge.
- **Points of Advantage (POA)**: every factor (troop type, armour, weapon, terrain, height, general,
  flank) is a POA bonus; the net difference decides the fight. 100 POA is about 33%; the difference
  caps at 200. Separate tables for impact, melee and shooting.
- **Shooting**: range by weapon (foot bow 2/4 squares, heavy artillery 6/9); arc 45 degrees, half
  effect from 22.5; moving lowers it; armour on a sliding scale; skirmishers are hard to hit.
- **Close combat**: a charge resolves as impact (only the men in contact), then melee each turn until
  one side breaks. Combat strength counts only the first 2 ranks of foot (4 models of horse); the
  bigger side overlaps. Mouse-over shows Win:Draw:Lose from 1000 simulated resolutions.
- **Cohesion**: Steady > Disrupted > Fragmented > Broken (routing). Tests on 2d6, need 6; Untrained
  re-roll 6s, Superior 1s, Elite 1s and 2s; triggers: heavy shooting losses (~10%), losing a combat,
  a friend breaking nearby, a general lost. Rally tests each turn. Autobreak near 50% losses (sooner
  for raw troops). Broken units rout; mounted victors usually pursue.
- **AI**: same rules and no hidden bonuses at every level; difficulty changes the force balance.

## Systems
- **Tactical combat**: Points of Advantage: every factor is a bonus on one scale, 100 POA ~33%, net
  difference capped at 200; impact then melee; only front ranks count, extra ranks give staying power (13.1-13.2).
- **Tactical combat**: four cohesion states with 2d6 tests and quality as re-rolls instead of
  modifiers; autobreak by losses; pursuit chances by troop type (14).
- **UI**: Win:Draw:Lose odds shown by simulating the combat 1000 times; detailed tooltips list every
  modifier (13.6). A good answer to "rules too thick to read".
- **AI**: plays by the player's rules at all levels; difficulty = army balance; auto-deploys by
  terrain (heavy foot on open ground, cavalry on the open wing) (31.1).
- **Modding**: units in one CSV with a comment row per column; game logic in readable BSF scripts;
  global mods loaded from Documents without touching the install; 3D unit models with a text
  animation table (frame ranges per action, sounds, script calls) (25).

## Running it (learned 2026-11-02)
- Steam app **1368870**, Proton Experimental; window class `steam_app_1368870`.
- **Background play (normal way):** `bgplay.py start` then `bgplay.py steam 1368870` (the Steam launch
  option for it is set; see game-ui). The **Launcher** window (1000x537 at +300+226 on the 1600x990
  screen) comes first: **Play** at screen (1204, 370). Then the game window "FieldOfGloryMedieval"
  (1594x871 at +3+29). Runs with WineD3D in software; check with
  `gamecheck.py --bg --hover 812 402` (Battles button) for 30-60 s after launch.
- On the user's desktop (no flag file) it runs as normal with the GPU.
- **Popups:** the first launch showed "Field of Glory 2 will now attempt to connect to the internet"
  (OK) as its own small window before the game; later launches didn't. Expect others.
- Settings and logs: `~/.local/share/Steam/steamapps/compatdata/1368870/pfx/drive_c/users/steamuser/
  Documents/My Games/FieldOfGloryMedieval/` - `OPTIONS.TXT` (RezX/RezY, Fullscreen 0, WindowFrame 1),
  `error.log` (a startup trace even when nothing is wrong: a healthy start ends "TS: Ended").

## Main menu and Settings (desktop window 1914x1048 coordinates; scale for others)
- Main menu: Tutorial, Battles ("Quick, custom and historical battles"), Campaigns, Multiplayer,
  Editor, Quit Game (asks: tick = quit, cross = cancel). Top-left icons: language, **gear =
  Settings**, two more.
- Settings: Difficulty I-VI (set: II "Knight"), Mouse Button Mode, **Screen Mode Fullscreen /
  Windowed / Framed Wind.**, Cursor Lock, Game Speed, Unit Speed Turbo, Sound, Tooltips Simple /
  Detailed, Combat Log, Close Combat Reports, Minimap, Hotseat Mode, Ambient Sounds, Idle Animations,
  Question Marks, Anti-aliasing, **Game Resolution** (a list 800x600 ... 1920x1080; pick, its Accept,
  then the main Accept; "Changes will require game restart"). Options are written to OPTIONS.TXT
  **when the game quits**.
- **Danger: the X at the top right of Settings is QUIT GAME**, not close. Leave Settings with the
  back arrow at the top left or Accept.
- Set 2026-11-02: Framed Window at **1600x900** (it was 1920x1080 in a smaller window, so the picture
  was wrong).

## Playing a game with the user

The plan: Claude's first battle is against the AI; the user watches and does not play (2026-11-02). The user as opponent later (hotseat item on the backlog). Use game-ui (find the window class
first; it runs under Proton) and learn-to-play's method: read Battle 39-48 before the first move, check
the screen after every order, never end a turn without the user's go.

## Needs from the user
- When to play the battle, and which (a Quick Battle is the smallest).

## Battle screen elements (hovered with hoversheet.py, 2026-11-02; game at 1600x900 on bgplay)
- Top left: battle name panel ("Custom Battle", ▼ opens more), army morale bars (Anglo-Irish / Irish, % routed).
- Top middle: deployment / help text box. Top right: Turn n/24 + **End Turn** (asks to confirm).
- Hovering terrain: tooltip with terrain and height ("Open ground (Hill). Height: 50").
- Bottom right: minimap; eye icon under it (1476,870) = Toggle Top View.
- **Right edge, middle: triangle (1578,448)** opens a column of 10 icons (x 1567):
  268 Next Unmoved (Tab) · 308 Next Unshot (B) · 353 Toggle Line of Fire (1) · 393 Toggle LOS (2) ·
  438 Toggle Command Range (3) · 480 Toggle Detailed Unit Info (Ctrl+click unit) · 525 Toggle Combat Log ·
  570 Casualties · 612 Toggle Unit List · 657 Toggle Briefing. (the user pointed the triangle out.)
- **Top left: triangle under the battle-name panel (170,113)** opens the briefing: armies and dates,
  OBJECTIVE (rout conditions), turn n of 24, turns remaining; click again to close. (the user pointed it out.)
- Camera (held keys; ~800 ms = most of a screen, use ~300 ms): W/S forward/back, A/D left/right,
- **M** = toggle top view (same as the eye under the minimap), not an overhead map. Max zoom-out shows about 2/3 of the field.
  E/Q rotate, F zoom out, R zoom in.

## Deployment (learned 2026-11-02)
- Deployment zone = the lighter grid squares (~59 px at max zoom-out). Select a unit (left click), then
  **right-click a square** to put it there. Generals can be moved too, and facing changed (the user).
- Left-click on the **already selected** unit opens a small menu: ▲ Deploy here · ↻ Turn · blue
  Turn Whole Command. Don't right-click where that menu is.
- **Escape is never "cancel": it opens the game menu** (Load/Save, Settings, Main Menu, Quit); the
  back arrow top-left (54,64) returns to the battle.
- Check the unit card after placing: knights on rough ground show "Severely Disordered" - hover the
  square first (tooltip names the terrain) and use Open ground for cavalry.
- Unit List (right panel icon) lists every unit with strength, AP and state; clicking an entry selects
  it and centres the camera. Cavalry are at the end of the list.
- Each command has its own leader (C-in-C or sub-general, SG); keep units within their own leader's
  command range (key 3 shows it). Hovering another unit while one is selected shows swap icons.

## Orders (manual ch. 11, checked 2026-11-02)
- Left click selects, right click orders; Space deselects. Each order has an icon shown when hovering the target square.
- Open ground: 1 square = 4 AP straight, 6 AP diagonal (foot 10 AP ~ 2 squares, knights 14 AP ~ 3).
- Move Whole Command (manual 11.2): all units of the command move parallel to the selected one; only
  while no unit of the command is within 5 squares of an enemy; units already moved are left out
  (triple arrowhead marks who takes part). Turn Whole Command likewise.
- ZOC: primary = square in front (red), secondary = the two beside it (yellow); a move may enter but not pass beyond.
- Knights, undrilled heavy foot, large and raw units are Unmanoeuvrable (no free 45-degree turn).
- Tab = next unmoved unit (selects it and centres it at screen ~800,465).
- **Undo**: select the unit that just moved, **right-click its own square** -> big green ↶ on the square
  ("Undo Move" on hover) -> **left-click it**. (The small green button drawn under a selected moved unit
  did nothing when clicked.) Only the last unit/group moved; not after shooting, charging
  or spotting new enemies. Plan move order so units don't block each other (move the screen of
  light troops before the knights behind them - the user).
- Order icons under the pointer show what a right-click on that square will do (▲ move with
  "Move Unit cost/AP", red ✗ = not allowed).

## Real games log
### Battle 1 (2026-11-02): Anglo-Irish (Claude) vs Irish AI, Norman Invasion of Ireland 1170, attacking
- Mine: 3 Knights & Sergeants (0 C-in-C Edmund Marshall, 1 Piers FitzMaurice SG, 2 Thomas le Boteler SG;
  superior, heavily armoured, knightly lancers/swordsmen, AP 14); Sergeants (3, armoured lancers, AP 16);
  Irish Foot 4-7 (medium foot, heavy weapon; Ralf de Cogan SG); Irish Kerns 8-12 (medium foot, light
  spear, swordsmen 50%); Light Javelinmen 13-15 and Light Archers 16 (light foot, unprotected, AP 12,
  5 turns ammo); Spearmen (Defensive) 17-20 (undrilled heavy foot, protected); Welsh Longbowmen 21-22
  (bowmen, unprotected, 5 turns ammo); Ostmen 23 (undrilled heavy foot, heavy weapon).
- Theirs: Irish Kerns (9-18 seen; medium foot, lightly protected) in fenced enclosures and fields with
  woods both flanks; Noble Cavalry (0) behind.
- **Lesson (the user): don't accept the default deployment line.** I only moved the knights and kept the
  game's basic line, so troops started out of position. Next time: look at every unit and the enemy
  and the ground first, then deploy on purpose (shooters where they can reach the enemy's strong
  points, heavy foot for the assault, light troops screening, cavalry where the ground is open).
- Look at all units (Tab + read the card) and identify the enemy (hover) before giving any orders.
- **The camera follows a unit as it moves** (scrolled ~140 px after a move near the screen edge): every
  later coordinate goes stale. Re-identify units (hover) after each order; scripts/fogmove.py does
  this with --expect. A stale click moved the wrong unit once (Irish Foot 7 instead of Longbowmen 22).
- A right-click on a square with several possible orders opens big buttons: ▲ Move Unit on the
  target, blue ▲▲▲ Move Whole Command under it - left-click one. One possible order = moves at once.
- Plan to break them (turn 2): The user's read - the AI defends but will march on my formation as I come
  close and go for light units. So: form two lines (heavy-weapon foot centre, spearmen on the flanks,
  bowmen just behind and between, kerns second line), light screen that falls back before contact,
  knights + sergeants held on the open north flank. Advance to longbow range of the northern
  enclosures, shoot one kern unit at a time; when they come out of the fences, take them on the
  heavy foot and hit their flanks with the knights in the open. Then mass the heavy foot on the north
  end of their line (2 on 1) and roll it up; spearmen watch for the Noble Cavalry. Need 40% routed.
- The user's correction: **the AI only comes out if threatened by the longbows.** So the longbows are the
  trigger: form up fully out of range first (no hurry - they won't move), then step the longbows
  into range with the trap already set. Ranges (manual 12.1): foot bow/longbow short 2, long 4
  squares (half effect at long); javelins 1. Bowmen can't shoot through friends unless from higher
  ground (chequerboard gaps are fine). Average longbowmen = 100% swordsmen but unprotected; only
  light foot can pass through friends, so leave gaps for bowmen to fall back.

## Giving a turn's orders (2026-11-02)
In phases with a check after each (move-phases skill); one order at a time with scripts/order.py
(COMMANDS.md). The extension pass is mandatory: lights 12 AP, light horse 20, mounted crossbow 16,
knights 14 - check every leftover against the role.

## Geometry tools (the user: "this is a geometry game ... build tools", 2026-11-02) - scripts/
- Centre the camera on a unit first: Unit List entry click, Tab or Next Unmoved put it at 800,465
  (a square centre; squares 59 px at max zoom-out, top view). Coordinates go stale when the camera moves.
- `board.py [--json F]` - hovers every square: terrain letters (. open, r rough, m marsh, W woods,
  d difficult, # obstacle/fence, t tracks/fields) and units as A ours / E enemy (side from the card
  banner of the hovered unit: blue ours, green Irish), plus a unit list with grid (col,row) from the
  centre. ~10 min for a full screen; text only. Terrain tooltips are wide and drawn left/above the
  pointer - read full-width bands.
- `terrscan.py` - terrain letters only (older, narrower read).
- `fogmove.py X Y TX TY [--expect T] [--whole]`, `--undo X Y` - one checked order.
- `fogadvance.py` - RETIRED (scripts/retired/). The user: "you should not be using an auto movement script". Every unit is moved by a deliberate order from the plan. It also didn't trust its own geometry: it doesn't know the geometry (units
  in each other's way, marsh ahead) - use board.py first. The user: "you are autopiloting into marshland".
- Card read: OCR turns (0) into (c); match unit numbers loosely.

## Movement and charge rules that shape plans (manual 11.1-11.13, read 2026-11-02)
- Open ground 4 AP straight / 6 diagonal. Foot 10 AP = 2 squares; knights 14 = 3; light foot 12 = 3.
- Turning: a move within 45 deg of current facing is free. Non-light units in command range get one
  free 45 deg turn per turn (unmanoeuvrable ones - knights, undrilled heavy foot - don't). Extra 45 = 4 AP,
  46-90 = 8 AP, more = all AP. So **non-light foot can't turn more than 45 deg and move**: face the
  enemy before closing. Mounted can turn 90 and still move a square or two.
- Move Whole Command only while no unit of the command is within 5 squares of an enemy - from ~5
  squares out every unit is ordered singly.
- Fall back 1-2 squares keeping facing; inside an enemy's charge reach = cohesion test.
- ZOC: unit's front square (primary) and the two beside it (secondary); can enter, not pass. Non-light
  ignore light troops' ZOC. In an enemy's primary ZOC you can only charge that enemy (or one whose
  primary ZOC you're also in).
- Charge: need AP to enter the target's square; target within 45 deg of front at the start; free 45
  deg turn always. Click the Charge icon twice; first click shows Win:Draw:Lose (Ctrl = detailed).
  Flank/rear charge only counts if the charger **starts its move behind the target's flank**.
  Flank-charged unit already fighting or that evaded drops a cohesion level, impact at +200 POA.
- Light foot can't charge unbroken non-light troops (except in rough/difficult terrain); they evade
  non-light chargers unless in rough/difficult or behind an obstacle. Kerns are medium (non-light).
- Light foot pass through friends only straight front-to-back.

## Battle 1 plan (turn 4, written for the user) - geometry
Enemy: Kerns in a north-south chain of fenced enclosures ~6-7 squares east of my line; woods south-
east; open ground north. Kerns AP 10 = 2 squares/turn: from 3+ squares away they can't charge in
one turn, they must step out into the open first.
1. T5: whole line advances 1 square (stays >5 from the enemy so Whole Command still works where
   possible); knights to the north wing on open ground, level with the line's north end.
2. T6: longbows 21+22 step to 3-4 squares from the NORTHERN enclosure (long range, half effect)
   with heavy-weapon foot (Irish Foot 4-7, Ostmen) on the squares either side of them, same rank,
   all facing east; javelins pass back through to the rear (straight back only); spearmen 17-20 on
   the south end facing the woods/enclosures (they stop cavalry); kerns 8-12 second rank behind gaps.
3. Shoot one enemy unit with both longbow units each turn (5 turns of ammo).
4. If Kerns come out (into the open, 1-2 squares in front of my line) - next turn charge them with
   the heavy foot head-on and the knights from the north (knights must start behind their flank).
5. If they stay in, keep shooting; when a target is Disrupted/Fragmented, assault that enclosure with
   2 heavy foot units per Kern unit; the fence helps them, so only attack weakened ones.
6. Win at 40% routed (~5 units).

## Tactics
Plan-making, principles, roles and the turn method: **battle-tactics** skill (root .claude/skills), built from manual ch. 23 Hints and ch. 30 Tactics.

## Custom Battle setup (walked through with the user, 2026-11-02; bgplay 1600x900 full coords)
- Main menu > Battles (810,404) > Custom Battle (810,452). Settings gear on the main menu (132,74), 2 pages (round arrow 250,646), Accept (800,700). Hover the CONTROL, not its label, for tooltips.
- Rows: Pick your army (624,322), Pick enemy army (624,392), allies, Scenario, Force size, Map size, Map type, Force selection (Player/Auto), Advanced options; Create at bottom.
- Army list on the right: rows 19 px apart, first row y 330, x 980; 3 wheel notches = 9 rows. Buttons A-Z / Date / W-E / Hide $ ($ = DLC lists the user does not own - a FoG II convention). Bottom box = nation history blurb (same for every period of a nation; some add special rules e.g. field defences).
- Without DLC lists run 1040 to ~1339 (Tatar 1242-1339 last).
- Enemy list is filtered by Date and Geographical buttons: FoG II pairs armies that historically could meet (the user: "the armies you can fight are generally geographically linked").
- **Army Options Preview** (the three-lines button right of each army row, (852,321) own / (852,392) enemy): every unit type of the list with cost and quantity ("1 + 0/4" = 1 compulsory + up to 4 optional), points used/budget, sort by Type/Points/Quality. ALWAYS look at both previews before a battle (the user) - it tells what the enemy can field. Close button centre (740,712).
- English 1155-1271 (V.Small, 598 pts): compulsory Knights & Sergeants 74, Spearmen (Defensive) 36, Raw Spearmen (Defensive) 24; options incl. Mounted Crossbowmen 36, Sergeants 36, Light Javelin Horse 24, Welsh Spearmen 47, Armoured Spearmen 42, Galwegian Foot 33, Irish Kerns 30, Crossbowmen 39, Welsh Longbowmen 39, Archers 36, Light Archers 30.

## Reading a unit card (manual 29.2-29.3, 13.2.1-13.2.3 POA tables = printer PDF p.69-70, 11.17)
Hover a unit in the Army Options Preview (or in battle) for: Size, Troop Type, Special features,
Quality, Armour, Capabilities, (D) = may dismount.
- Size: Large (10+ models) = unmanoeuvrable, +15 Overlappers in melee vs smaller if heavy weapon.
- Quality: -50..+100 POA in every combat; cohesion 2d6 needs 6 - Untrained re-roll 6s, Superior
  re-roll 1s, Elite re-roll 1s and 2s.
- Better Armour (melee): up to +100 vs foot, +50 vs mounted; enemy Heavy Weapon cancels the first 50.
- Knightly Lancers (impact, OPEN TERRAIN ONLY): +200 vs foot (only +150 vs steady non-charging pike/
  spearmen), +100 vs mounted. Mounted light spear / other lancers / impact foot get no bonus vs them.
- Other Lancers: +100 vs mounted except knightly lancers; +100 vs foot (+50 vs steady spear/pike).
- Mounted Swordsmen (melee): +150 if knights vs mounted; +100 vs other mounted; +100 vs foot unless
  steady pike/spearmen or behind obstacle.
- Foot Swordsmen: +100 vs mounted; +100 vs foot (+50 vs steady spearmen/obstacle).
- Defensive Spearmen: impact +100 vs anything if not charging (or vs defensive spearmen); melee +100.
- Offensive Spearmen: impact +100 unless charging mounted shock troops; melee +100.
- Heavy Weapon: impact +100 (not when charging mounted shock troops); melee +100, +10 if Armoured+.
- Pike: +100 impact (not charging), +100 more if 4 ranks deep.
- Mounted (any) +100 impact vs light foot, bowmen, mob. Higher ground +25 (<=75) / +100 (>=100).
  General with the unit +50. Flank/rear: min +50 vs unengaged, +200 vs engaged/evaded.
- Dismount (D): ONLY in the deployment phase (can remount there); never in force selection or battle.
Use: knights charge foot/cavalry in the open; disrupt steady spearmen first; never commit them in
non-open ground; on a broken map dismount them at deployment.

### Advanced Options (button "Hiding/Showing Advanced Options" ~(624,640); manual 5.8)
Right panel replaces the army list; each value has < > arrows. Rows (value box x 1028, label x 1110):
Turn Limit y 372 (24 for V.Small/V.Narrow), FP Increment y 410 (100), Force Points Side A y 450 (598),
Side B y 488 (600), Width y 526 (24 squares), Height y 566 (32). Info box: "You can tweak the game
turn limit, map size and force sizes above right." No tooltip on the value boxes.

### Force Selection screen (manual 8.2; seen 2026-11-02)
- Left "Your Army" panel: Type / Cost / Quantity list (rows x ~250, first row y ~230, ~23 px apart);
  core units already bought (1+0/4 = 1 fixed + 0 of 4 optional). Sort buttons Type (258,602),
  Points (332,602), Quality (446,602). Points left box (244,658) "464/598". Legend: left mouse =
  Increase Force, right mouse = Decrease Force. Autofill (220,760), Autodeploy (430,760).
- Centre scroll = briefing: armies, OBJECTIVE, "English Turn 1 of 24, Turns remaining: 23",
  "The enemy are offering open battle"; X to close at ~(840,680).
- Right: Combat Log panel. Bottom right: minimap. Map visible behind.

## Related skills
fog2m-map (using the battle map), learn-to-play (method), learn-to-mod (modding: Squads.csv, BSF), manual-first, battle-tactics, map-usage, map-camera, photo-map, planning.
- Force Selection list: hover the row ~0.6 s BEFORE clicking - 3 of 11 quick clicks (0.9 s apart,
  no hover) were dropped (2026-11-02). Check the points box (160-330, 645-677) after each buy.
