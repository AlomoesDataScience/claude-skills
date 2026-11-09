# dom6-ui - Screen map (window 1920x1044; full-size coordinates; version 6.37)

Part of the dom6-ui skill; SKILL.md links here.

## Screen map (window 1920x1044; full-size coordinates; version 6.37)

The menus are drawn centred, so on another window size measure again with `shot --grid`.

**Main menu**: Create World (920,402), Continue Old Game (920,448), Network (920,492), Tools &
Manuals (920,538), Mods (920,582), Preferences (920,628), Quit (920,674).
Hotkeys: a random map creator, c create world, e map editor, g game tools, h hide/show menu,
l continue old game, m mods, n network, o network lobby, p preferences, q quit, r new random
background world, t show a tip. (Help Exit at 959,687.)

**Create World**, in order (Cancel or Escape goes back one step):
1. *Map Settings*: size Small (622,121), Medium (622,150), Large (622,178), Enormous (622,207),
   Loaded map (622,243); main-world layouts in two rows at y 354 and 428, x 665/780/895/1010/1124/
   1238; underground layouts at y 574; water provinces (760,693), Rivers (620,724), East/West wrap
   (620,757), North/South wrap (620,785); Ok (959,826), Cancel (959,867).
2. *Enter game name*: text field, Ok (959,473).
3. *Select Era*: Early (665,202), Middle (665,373), Late (665,531); Ok (959,689), Cancel (959,720).
4. *Choose Participants*: rows start at y 336, 28 px apart; nation column x 558 (click opens the
   nation picker), Player x 945 (Human / AI level), AI type x 1081. Add new player (598,507),
   Disciple Game (531,539), Ok (959,574), Cancel (959,605).
   Hotkeys: n add player, backspace remove last, H all human, A all AI, R remove all, L / W
   random land / water nations, 0 no teams, 2/3/4 equal teams, + / - AI difficulty, esc back,
   ret done. Help Exit (960,716).
   *Nation picker*: scrolling list, rows 28 px apart from y 73, hover shows the description; at
   the bottom <Random>, <Random land nation>, <Random water nation>, <None>, Cancel; Escape closes.
5. *Nation overview* (for the human nation): Ok (959,898).
6. *Design Pretender*: Password (698,144), Select Physical Form (741,171); magic icons at y 248:
   F 711, A 765, W 817, E 868, S 920, D 973, N 1024, G 1077, B 1130 (left click +1, right click -1);
   Add Bless Effect (723,423); dominion icons at y 527: candles 710, order 772, productivity 823,
   heat 877, growth 925, luck 980, magic 1033 (left +, right -); Imprisonment Awake (665,659),
   Dormant (665,687), Imprisoned (665,716); View Nation Description (795,764); Ok (959,802).
   These positions move down as blesses are added (four blesses pushed Ok to 959,938): take a
   shot first. Design points left are at the top.
   Hotkeys: ctrl-l load design, ctrl-s save design, ctrl+shift-s save as AI template mod data,
   a add bless, b view all blesses, i/F forgeable items, n nation description, p physical form,
   r random pretender, s/F5/C researchable spells, t templated pretender, x repeat last bless.
   Help Exit (959,673).
   *Select Physical Form*: grid by starting dominion (4, 3, 2, 1 from the top), cells 122 px wide
   from x 403, rows near y 187, 318, 452, 568, 700; hover = name and cost, left click = choose,
   right click = full stat page (Exit at the bottom). Cancel (959,786).
7. *Enter the name of your God*: text field (a random name is filled in), Ok (959,458),
   Cancel (959,490). Then "All praise X" Ok (959,474): **the save folder now exists.**
8. *Game Settings*: tabs World (840,110) and Thrones (1075,110). World: starting provinces,
   independents strength, site frequency, resource multipliers, events, story events, score
   graphs, diplomacy, hall of fame, mercenary and global slots, artifact and legendary rates,
   human AI level, research speed, random start research, renaming, master password, cheat
   prevention. Thrones: victory type, cataclysm and its turn, ascension points needed, level 1-3
   throne counts. Ok (959,900) starts the game; Cancel (960,766 on Thrones, 959,932 on World)
   goes back to Participants. Hotkeys: ret ok, esc cancel, ctrl+l load saved settings, ctrl+s
   save settings. Help Exit (959,516).

**Continue Old Game** (view only): list of saves with nation flags, rows from y 258 about 28 px
apart; Play game, Delete game, Cancel (959,652). Hotkeys: n sort by name, d sort by date, ret
play, del delete, esc exit. Help Exit (958,552).

**Network**: Open Previous Connection, Enter Game Lobby, Start Game Server, Connect to a Game
Server, Cancel. Do not use any of them without the user.

**Tools & Manuals (Game Tools)**: Create a Pretender God (840,294), ... for disciple game (840,322),
Create a Disciple (840,350), View Created Pretenders (840,380), Map Editor (840,466), Random Map
Creator (840,494), Manuals & Introduction Videos (840,584), Open User Data Directory (840,612),
Exit (960,662). No hotkey list.
*View Pretenders*: saved designs by era with <del> (do not click), Exit (960,742).
*Map Editor menu* (e): New map, Load map, Upload map to Steam Workshop (never), Exit. Loading a map:
see the dom6-maps skill. After every call focus goes back to the window that was in front, or to
Claude's terminal ($WINDOWID) when the app itself was in front (a newly opened app grabs focus).

**Mods** (m), title "Mod Preferences": one list of every installed mod (rows ~26.9 px apart from
y 71, names from x 777, banner at x 655-752), scroll with the wheel (one notch ~2.6 rows); left
click on the name toggles a mod (green tick at the right when on; tooltip "Enable this mod" /
"Disable this mod, (right click) info"); at the bottom "Disable all mods (N enabled)" (grey when
none) and Exit; Escape leaves and saves. Right click opens info: description, Upload to Steam
Workshop (never),
**Error Check** (960,512) → "Mod seems ok, crc ..." or the errors, with Refresh and Ok
(959,504); Exit. Escape leaves the list. Error Check is the game's own parser: use it to confirm
`check_dm.py` and dom6-modinspector results (dom6-modding skill).

**Preferences** (p): tabs Gameplay (775,130), Graphics (895,130), 3D (1020,130), Sound (1137,130);
checkboxes; Exit (959,679). View only unless asked. No hotkey list.
