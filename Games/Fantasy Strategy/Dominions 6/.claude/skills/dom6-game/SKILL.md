---
name: dom6-game
description: "Play an ongoing Dominions 6 game in the running client: main-screen hotkeys, what the screen shows, orders, transfers, turn routine. Use when Claude plays or inspects a turn in progress or needs a main-screen hotkey."
keywords: "main, map, screen's, province, commander, statistics, magic, view, filters, unit, gem, transfer, top, bar, list, panel, moving, zooming, browsing, menus, safety, rules, never, end, without, end-turn, button, nothing, final, until, dom6-ui, guarded, input, reading, in-game, interface"
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

## Screen reference (moved to SCREENS.md, 2026-11-03)
`SCREENS.md` here: the province panel line by line, the Recruit screen (Pythium lists), Research (F5),
Mercenaries (`b`), the other top-bar screens and every menu seen. Read it before using one of those screens.

## Mercenary bids, more

- OCR may read a whole merc row as one text ("Ferdinando's Footmen 200 <bid>"): click the
  `<bid>` word at x ~1107 on that row's y, then check the dialog names the company.
- The Land column is the province being viewed when bidding (bid while viewing where the
  company should arrive).
- Captured provinces recruit their own troops with their own resources and recruitment points
  (Nom: Jaguar Tribe Slinger 10g/2r/9rp, Warrior 10g/7r/9rp, Priest needs lab + temple).

## Map

- **Mouse wheel zooms** (wheel up = in) with the pointer over the map. Page Up/Down and
  Ctrl+Up/Down did nothing in testing.
- Arrow keys scroll; Home goes to the capital; `#` or `g` goes to a province number.
- Right click selects a province (per the hotkey list); click map = move/sneak the selected
  commanders there.
- Grey banners = independent provinces; dotted lines between provinces = movement paths.

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

## Reference files (read the one the step needs)

| File | Holds |
|---|---|
| `reference/the-screen-1920x1044.md` | **The screen (1920x1044)** - Title line: god name and titles |
| `reference/provinces-and-commanders-the-user-2026-1.md` | **Provinces and commanders (the user, 2026-10-27; checked in game)** - Right-click a province to view it: its info fills the right panel |
| `reference/map-reading-taught-turn-2.md` | **Map reading (taught turn 2)** - Dots between provinces are connections: yellow = passable, red = blocked (needs flying   or another way), bl |
| `reference/battle-replays-taught-turn-3.md` | **Battle replays (taught turn 3)** - Messages list: "There was a battle in X." with Goto province / View Battle |
| `reference/turn-5-lessons-the-user-2026-10-27.md` | **Turn-5 lessons (the user, 2026-10-27)** - Resources are not kept between turns: spend every province's resources each turn   (captured provinces too,  |
| `reference/hotkeys-from-the-game-s-list-is-keysym-q.md` | **Hotkeys (from the game's `?` list; `?` is keysym `question`)** - Misc: b mercenaries, c casualty reports, d recruit defence, e end turn, f fort info, h hide menus, i province  |

## Related skills
dom6-ui (driving the window), dom6-tooltips, dom6-army-check (before End Turn), dom6-tactics, dom6-play, delegate, planning, manual-first.
Also (2026-11-03): dom6-scouting, dom6-battle-ai, dom6-map.
