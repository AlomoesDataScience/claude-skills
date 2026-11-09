# TOAW IV commands and screens (manual pp. 8-33, KeyCommands.txt, Whatsnew 4.1) - read before playing

Not checked in the game yet (2026-11-03): every line is "manual says"; the game wins when it disagrees - note
differences in SKILL.md "Game vs manual".

## Danger list (never without the user's go / never by accident)
- **E** = "Resolves all combats or ends the Turn" (p.22) - pressing it with attacks planned RESOLVES them (a
  commit); pressing it again ends the turn. Both need the user's go (end-turn rule, commit-only-when-certain).
- Play menu: End Scenario, Computer Player (hands the side to the AI). File: Close.
- **F9** quick save, **Z** undo (undo is logged in PBEM playback). Shift-F12 / `|` = the AI (Elmer) moves
  every unit under PO Assist - a mass order.
- Editor-only keys (F4-F8, F11, X) write files - not during play.

## Start-up chain (p.8-10)
Steam -> **Game Menu** launcher (autorun.exe, "The Operational Art of War IV Gamemenu", 900x550) -> "Play"
option -> first run: language -> intro -> **five buttons: Play New Game, Resume Saved Game, Play Online, Edit
Scenario, Quit**. Play New Game -> Select New Game: scenario list (left), info (right), Default Directory
(scenarios under Documents/My Games/The Operational Art of War IV/Scenarios; first time = Tutorials), a
player-mode button cycling Hotseat / PBEM / Computer vs Human / Human vs Computer / Computer vs Computer,
Set Game Options, Scenario Documents, Play, Cancel. Autosave.SAL every 5 min in Saves (optional).

## Options (p.10-19) - set once, they persist
- Game Parameters (both players, fixed once the game starts): Command and Control, Scenario Variability, Fog
  of War, Environment, Active Disengagement, No Borders, High Supply, New Flanking/Turn Order/Supply/Bridge
  Rules, Advanced Rules; 4.1 adds Variable Initiative and New Density Rules options.
- Player Options (any time): **Menu Show Delay** (1 = classic: right-click opens a menu; else right-click
  moves/attacks and right-HOLD opens the menu), Tool Tip Show/Hide, Moving Selects Next Unit, Detailed
  Combat Reports, Show PO Assist Buttons, Double click opens planner, Allow Huge Map View, mouse-wheel zoom,
  animation timers, No Delay, Intelligence/Handicap of the AI, brightness/contrast, volumes, logs (SitRep log
  = a text file of the turn's news - useful for reading).
- **For Claude**: Menu Show Delay 1 (menus are explicit, no accidental moves), tool tips on, Detailed Combat
  Reports on, SitRep Log on, Intro Cinematic off (View menu). Write the user's old values down first.

## Mouse (p.21-23, KeyCommands)
Left = select; right = orders or menu (by Menu Delay); drag = like right click in most places; double-click
an enemy = combat planner (option); left click on some dialogs hides them. Wheel = zoom (5 2D levels + 2 3D;
Y / Shift-Y = picture zoom). Map edge scroll; drag on an empty hex moves the map. **The Information Panel at
the bottom describes what each click will do** - read it before clicking (p.23).

## Keys (not case sensitive)
| Key | Does | Key | Does |
|---|---|---|---|
| N or Shift + | next unit that can act | + / - | next / previous unit |
| G | next unit in this stack | H | HQs (then artillery) to top of stacks |
| U | Unit Report | F | Formation Report |
| O | Order of Battle | A / Shift-A | air units / air briefing |
| C or F2 | Group Composition of the hex under the cursor | P | Attack Planning for the hex under the cursor |
| D | dig in (+ next unit) | T | tactical reserve (+ next unit) |
| L / Shift-L | loss tolerance of the unit / the stack | M | counters show movement <-> strengths |
| I | range circles | W | weather view |
| Space (hold) | hide units (see terrain), hide dialogs | B / Ctrl-B | find place / next |
| `/` `?` | formation path / all paths | `.` | disembark / next embarked unit |
| `,` | split or recombine units | Shift-T | Theater Options |
| Arrows | scroll map (Shift/Ctrl: microview) | Numpad 1-9 | scroll; 5 = centre on current unit |
| 1-9 | choose a button in a vertical message box | Esc / Enter | cancel / accept a dialog |
| F1 | help | R | refresh the current unit |
| Shift / Caps Lock | speed up battles and AI moves | F12 or `\` | PO Assist mode (Elmer plans) |
| E | resolve combats / END TURN (danger) | Z | undo |
"A unit that can act" = next land unit not selected for combat, dug in, entrenched, fortified, in reserve or
out of movement (p.21).

## Screen (p.23-26)
- **Map Panel**: the map; click to order or select.
- **Information Panel** (bottom): prompts and feedback - always read it.
- **Microview** (lower left): whole map small; click to re-centre; double-click = full-screen jump map.
- **Unit Panel**: 1 date, force roundel, owning force; 2 the stack (or group composition) with parent
  formation, unit name, deployment/mission; 3 health, attack, defence, movement (original/remaining); 4
  proficiency, readiness, supply (numbers + pie); 5 current round and the progress pane (rounds used and
  planned). Left click = centre on the unit; right click on the stack = Unit Report; move slowly along the
  stack edge to see each unit.
- **Air War Panel** (below): AS air superiority, INT % chance of interception, LOST.
- **Panels Control Panel** and **Button Panel** (6 toggle buttons, terrain info lines); the Legacy Control
  Panel is obsolete.
## Menus (p.27-33)
File (new/resume/save game, map images, Close), Play (End Scenario, End Turn, Computer Player, Undo, Game /
Player / Default Options, PO Assist Plan / Execute Moves / Move One Formation, Objective Tracks), View
(Scenario / Situation / Weather / Air Briefing, Theater Options, Order of Battle, Recent News, Expected /
Recent Reinforcements, Inventory and Replacements, formation paths, display toggles: place names, hex grid,
movement paths, formation highlight, possession flags/borders, unit icons strength/movement, text contrast,
intro cinematic).
