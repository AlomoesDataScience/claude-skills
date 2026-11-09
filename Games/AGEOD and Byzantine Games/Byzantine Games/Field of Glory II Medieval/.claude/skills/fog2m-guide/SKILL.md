---
name: fog2m-guide
description: "Guide to Field of Glory II Medieval, a turn-based tactical battle wargame on a square grid: manual page map, rules, UI, lessons. Use when playing or planning a FoG II battle, looking up a rule or modding it."
keywords: "byzantine, games, slitherine, armies, models, pages, text, numbers, data, scripts, copied, install, live, manual's, chapter, battles, work, action, points, advantage, shooting, arcs, ranges, impact, melee, combat, strength, ranks, four, cohesion, states, tested, 2d6, quality, re-rolls, rallying, autobreak, pursuit, built, modded, archon, engine, bsf, squads, csv"
---

# Field of Glory II: Medieval

Byzantine Games makes the tactical side of the AGEOD/Byzantine pair (the user, 2026-11-01). Installed
2026-11-01 for a look and **one game played together**, then likely uninstalled: everything worth
keeping is copied here. FoG II (ancient) is the same system with different armies.


**War-language lexicon (game <-> doctrine terms, task -> game actions): `LEXICON.md`.** **FIRST read `COMMANDS.md` (every hotkey and order). Before any battle read `PLAY.md` and `UNITS.md` (incl. its "Hypotheses to test" and "Game vs manual" lists) (this folder; UNITS = troop types, card terms, capabilities, army lists) - the play reference: banners, command, movement, ZOC, shooting tables, charges, POAs, cohesion, terrain, victory, hot keys. Read from the manual for playing, 2026-11-02.**

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

## Playing a game with the user

The plan: Claude's first battle is against the AI; the user watches and does not play (2026-11-02). The user as opponent later (hotseat item on the backlog). Use game-ui (find the window class
first; it runs under Proton) and learn-to-play's method: read Battle 39-48 before the first move, check
the screen after every order, never end a turn without the user's go.

## Needs from the user
- When to play the battle, and which (a Quick Battle is the smallest).

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

## War skills (the user 2026-11-02: call the military skills when playing; build on them)
- Level of war: **tactical**; domain: **land**. Vocabulary: military-doctrine (FM 3-90 tactics) first; soviet-doctrine for the
  opposing school; war-concepts (glossary, `warwiki.py look TERM`).
- Every turn / battle: **war-language** (UP: the situation in doctrine terms -> THINK: intent,
  form of manoeuvre, a task and purpose per unit -> DOWN: concrete orders -> CHECK) and **army-log**
  (read, log and evaluate both sides; `armylog.py`). Before the first real game write
  **`LEXICON.md`** in this skill folder (`warlang.py lexicon`): units -> roles, terrain -> OAKOC,
  rules -> effects, victory -> end state, task -> game actions.
- combat-models: The user's land salvo system and Lanchester (concentrate; make fights square when stronger, linear when weaker).
- First full integration: LEXICON.md here, army log in plans/battle2-armies.json, `order.py cards` reads unit cards.

## Reference files (read the one the step needs)

| File | Holds |
|---|---|
| `reference/how-a-battle-works-in-my-words.md` | **How a battle works (in my words)** - Units of models (infantry usually 8 models in 2 ranks, cavalry 4; 30 or 60 men per model by battle   size) o |
| `reference/running-it-learned-2026-11-02.md` | **Running it (learned 2026-11-02)** - Steam app 1368870, Proton Experimental; window class steamapp1368870 |
| `reference/main-menu-and-settings-desktop-window-19.md` | **Main menu and Settings (desktop window 1914x1048 coordinates; scale for others)** - Main menu: Tutorial, Battles ("Quick, custom and historical battles"), Campaigns, Multiplayer,   Editor, Qui |
| `reference/battle-screen-elements-hovered-with-hove.md` | **Battle screen elements (hovered with hoversheet.py, 2026-11-02; game at 1600x900 on bgplay)** - Top left: battle name panel ("Custom Battle", ▼ opens more), army morale bars (Anglo-Irish / Irish, % routed |
| `reference/deployment-learned-2026-11-02.md` | **Deployment (learned 2026-11-02)** - Deployment zone = the lighter grid squares (~59 px at max zoom-out) |
| `reference/orders-manual-ch-11-checked-2026-11-02.md` | **Orders (manual ch. 11, checked 2026-11-02)** - Left click selects, right click orders; Space deselects |
| `reference/real-games-log.md` | **Real games log** - Battle 1 (2026-11-02): Anglo-Irish (Claude) vs Irish AI, Norman Invasion of Ireland 1170, attacking - Mine |
| `reference/battle-1-plan-turn-4.md` | **Battle 1 plan (turn 4, written for the user) - geometry** - Enemy: Kerns in a north-south chain of fenced enclosures ~6-7 squares east of my line; woods south- east; open |
| `reference/reading-a-unit-card-manual-29-2-29-3-13-.md` | **Reading a unit card (manual 29.2-29.3, 13.2.1-13.2.3 POA tables = printer PDF p.69-70, 11.17)** - Hover a unit in the Army Options Preview (or in battle) for: Size, Troop Type, Special features, Quality, Armo |

## Related skills
fog2m-map (using the battle map), learn-to-play (method), learn-to-mod (modding: Squads.csv, BSF), manual-first, battle-tactics, map-usage, map-camera, photo-map, planning.
- Force Selection list: hover the row ~0.6 s BEFORE clicking - 3 of 11 quick clicks (0.9 s apart,
  no hover) were dropped (2026-11-02). Check the points box (160-330, 645-677) after each buy.
