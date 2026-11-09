# dcss-guide - Playing it (learned 2026-11-01, tutorial lesson 1 done)

Part of the dcss-guide skill; SKILL.md links here.

## Playing it (learned 2026-11-01, tutorial lesson 1 done)

- **Run it in the background** (game-ui `bgplay.py`): `bgplay.py start` (virtual screen :5, the
  user's input locked out), `bgplay.py launch flatpak run org.develz.Crawl`, then
  `bgplay.py seq "key o" "wait 2500" "shot --full"`. Window class `crawl`, 1456x900 inside a
  1600x990 screen; on the user's desktop it is `UI_WMCLASS=crawl` (the folder's `.claude/game-ui.json`).
- **Screen (full-size pixels):** map top-left (player always at the centre, ~580,410; tiles 32 px);
  stats top-right (Health, Magic, AC/EV/SH, XL, Str/Int/Dex, Place, Time with the last action's
  cost in brackets); minimap ~1250-1400,400; command bar (autoexplore first) ~1110-1490,655;
  inventory grid below; messages bottom-left (~80-1070, 780-860), tutorial text in magenta.
- **Start menu:** Dungeon Crawl, Choose Game Seed, Tutorial (~780,449 full size), Hints Mode,
  Dungeon Sprint, Instructions, Arena, High Scores. Tutorial lessons: a Movement, b Monsters and
  Combat, c Items and Inventory, d Magic, e Gods. Tutorial character: Human Fighter, name typed + Return.
- **Movement:** vi keys `h j k l y u b n` (arrows work for the four straight ways). Shift + direction
  runs until something interesting: a junction, a door, an opening room, a newly seen feature.
  A step costs 1.0 time; shallow water ~1.3 (deep water impassable); stairs about 1.5.
- **Doors:** walk into a closed door to open it. `C` closes; with only one door adjacent it closes
  at once with no direction prompt (a following direction key then walks into it and reopens it).
  Doors creak: noise shows on the Noise bar.
- **Exploring:** `o` auto-explore stops on items, features, monsters; it walks around exclusions
  (red-marked dangerous ground; travel refuses to enter them). `X` level map: `<` / `>` cycles the
  cursor through up/down stairs, `.` or Enter travels there, Escape closes. `<` `>` use stairs.
- Leaving the tutorial: stand on the exit archway, `<`, then a capital `Y`; a summary card follows.
- `Ctrl-P` message history. Dangerous keys: `Ctrl-Q` (abandon character), `S` (save and quit).
- **Lesson 2 (monsters and combat) - done 2026-11-01** (XL3, no damage worth noting): `g` picks up,
  `e` equips/wields (0.34: not `w`). Attack = walk into it; `Tab` auto-fights the nearest monster
  (careful: nearest may be the lethal one). Fight in 1-wide corridors, not doorways onto rooms.
  Right-click a monster = description with HP, threat (Minor..Lethal), speed, hit chances both
  ways, max damage: read it before fighting (wyvern: Lethal, bite 20). `f` then `f`/Enter fires at
  the auto-target ("overly suicidal" = no target, the cursor was on you); boomerangs return.
  Clicks/travel go one step at a time while a monster is in view; auto-explore won't move then,
  so chaining `o` presses is safe. Resting `5`. XP needs "Next" 100%.
  Bow: wield with `e`, fire with `v` (not `f`); **clicking a monster fires at it** (easiest
  targeting); moving the aim cursor by keys can land on unseen squares.
  With a bow wielded `Tab` shoots too. A monster in view blocks auto-explore and travel even when
  it can't reach you (the worm behind lava): kill it or break line of sight. Arrows vs a worm: ~25%
  miss, 1-3 damage. Level-up attribute prompt: `S` / `I` / `D` (took Str for a fighter).
  Lesson ends on the exit stairs: `>` then `Y`.
- **Danger:** a key while in `x` examine (probably `+`) opened "ENTER EXPLORE MODE" (unscored game,
  permanent): it needs the word "explore" typed, so Escape is safe. Don't use `+` in targeting.
- Text reading: `bgplay.py read hp msg stats` (regions in this folder's `.claude/game-ui.json`)
  costs ~1 s and few tokens; take shots only for map layout.
- **Lesson 3 (items) - done 2026-11-01** (summary keys: `,` pick up, `d` drop, `e` equip, `c` unequip,
  `r` read, `q` quaff, `V` evoke, `??` command help, `o` explore, `Ctrl-F` find).
  - **One `o` per step, then read** (the user): chained auto-explores walked past the +1 cloak of
    Starlight (AC+1 EV+4, Dazzle = blinds attackers now and then; it blinded 3 monsters in the
    last fight). `Ctrl-P` history shows what scrolled past.
  - `Ctrl-F` + a word ("cloak", "shop", "exit") lists seen items/features -> letter -> map cursor
    on it -> `.` travels. "Sorry, I don't know how to get there" = seen but no known path yet.
  - Armour and jewellery take ~5 turns to put on or take off: never mid-fight.
  - Drop menu is multi-select: letters toggle, Enter accepts.
  - Unknown scroll/potion: use to identify (fog, fear, curing). Scroll of fear made all 6 monsters
    flee, but hitting one snaps it out, and cornered ones turn to fight.
  - Wands: `V`, letter, `f` fires at the aimed target (aim line shows its wound state - a free
    check). Flame ~1/4 of a gnoll; a miss can hit the monster behind. Digging: `V`, letter,
    direction - only rock (`x` to check walls); dug to a hidden amulet.
  - Amulet of faith: useless without a god.
  - Shops: stand on it, `<` or `>`; letter, Enter, `y` to buy. They never buy. Bought a
    potion of curing (30) and a +2 buckler (165, SH 0 -> 5, EV -1; fine with a 1-handed flail).
  - Gold has no weight; tutorial gives 220 later so you can shop twice.
  - **Pick up enemy gear when it beats yours** (the user): dead monsters drop what they wielded/wore
    (the orc's +0 chain mail would have beaten my robe). Check the pile with `,` after a fight.
  - Final room: 2 orcs, an ufetubus, 3 gnolls. Won from XL3 by stepping back out of the doorway
    into the 1-wide tree corridor (one attacker at a time; spear gnolls still reach 2 squares),
    poison flail, flame wand, cloak blinds. Fell to 4/29 HP. `Tab` refuses at about half HP,
    not 1/4 - attack with direction keys. Walking away from a same-speed melee monster costs
    no hits; reach monsters still hit. Pressure-plate trap: popup (top centre) asks, `Y`.
- **Lesson 4 (magic) - done 2026-11-01** (summary keys: `M` memorise, `I` spell failure rates,
  `z` cast, `Q` quiver, `5` rest, `t` order allies, `c` take off).
  - Spellbooks add spells to a **library**; `M` memorises one into spell levels (XL and
    Spellcasting skill give levels; "too inexperienced" = the spell's level needs a higher XL;
    "can't memorise that many levels" = no free levels). Memorising takes a few turns.
    Scroll of amnesia frees a spell (relearn from the library later).
  - `z` + letter -> aim -> Enter/`.`. Risky spells ask "quite dangerous to miscast... continue?"
    -> `Y`. Miscast = turn and MP lost ("Nothing appears to happen" when lucky); casting adds
    magical contamination (Contam % on the stats panel, fades).
  - `Q` puts a spell in the quiver, then `f` + Enter repeats it. `f` with no target opens empty
    aiming: Escape.
  - Magic Dart: 1 MP, never misses, ~1/4 of a zombie. Failure 36% -> 16% with a ring of wizardry;
    INT and skill lower it further. Rings go on instantly (amulets take 5 turns). Ring of magical
    power: MP 4 -> 13.
  - Zombies and skeletons don't regenerate.
  - **Heavy armour/shields wreck casting**: kite shield took Call Imp from 24% to 58% failure.
    Casters leave ring mail and big shields.
  - Call Imp: one imp per spell (recasting dismisses the old one), it lasts a short time. Its
    hits often do no damage, but it holds a gate or corridor while you punch. Don't rest or
    auto-explore before a fight, because the imp runs out. Moving into an ally swaps places.
  - At XL3 the stat raise for a caster is `I`.
  - Fight at chokepoints: gates can be three wide; back into the one-wide corridor behind.
- **Lesson 5 (gods), attempt 1 - died 2026-11-01:**
  - Altar: stand on it, `>` prays -> god screen (powers, piety costs, `!` details) -> `J`/Enter
    joins. `^` = religion screen (OCR reads it as `*`). Kills raise piety ("Trog accepts your kill").
  - Trog: berserk, then regeneration and allies at more piety, melee weapon gifts; **no spells
    at all**; likes killing wizards.
  - `a` = abilities: Berserk is `a`; **`X` in that menu = Renounce Religion: never press it.**
  - Berserk: faster, stronger, max and current HP x1.5. Afterwards you are slowed and exhausted
    and can't berserk again for a while: rest with `5` until "fit".
  - Auto-explore walked over a +0 mace without stopping ("You see here..."). Weapons in the open
    don't always halt it: read every message.
  - **Death:** a pack (hobgoblin, rats, orc wizard: magic dart, blinks) arrived together. I fought
    in the open with `Tab` and only went berserk at 7/24. Berserk's extra HP is a share of max,
    so it went 7 -> 4/36 and one hit killed me. **Rules: berserk at the start of a hard
    fight, at full HP; back into a corridor before a pack reaches you; leave before ~1/3 HP.**
- **Lesson 5 (gods), attempt 2 - done 2026-11-01** (summary: `>` pray/join, `a` abilities,
  `^` religion screen, `.` wait one turn, `5` rest up to 100 turns, `Ctrl-0` dungeon overview with
  altars and features, `?/` description database).
  - Gnoll with a mace: one hit did 10 of 18 HP at XL1, so berserk early for any gnoll as well.
  - The pack, done right: waited in a one-wide corridor and berserked at full HP (24 -> 36) when
    the first hobgoblin showed. Killed 2 hobgoblins and 2 rats while berserk, barely hurt.
  - **After berserk you are slowed**, so the orc wizard got two actions per turn and took me from
    21 to 4. Berserk only when it can finish the fight; when it ends with enemies left, weigh
    walking away (you are slow, so mostly you can't) and fight only very weak or wounded foes.
  - "Trog appreciates your killing of a magic user": wizards are worth extra piety.
  - Direction keys: check which side the monster is on (the name label sits *above* the sprite).
    `Tab` doing nothing usually means the monster isn't adjacent or awake.
- **All five tutorials done 2026-11-01.**
- Next: real games, one `o` at a time (see "Real games log").
