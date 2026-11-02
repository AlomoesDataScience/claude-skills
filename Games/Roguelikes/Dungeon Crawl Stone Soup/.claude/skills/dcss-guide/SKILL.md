---
name: dcss-guide
description: Guide to Dungeon Crawl Stone Soup (DCSS 0.34.1, free and open source, installed as the Flatpak org.develz.Crawl), the classic roguelike of diving for the Orb of Zot - where its manual, quick-start, options and keybinding guides and its plain-text level design files (143 .des vault files, Lua) were copied in the workspace, the manual's map, how to launch and test it, and its design ideas worth borrowing (species x background, skills trained by use with chosen focus, gods with conducts, mutations, hand-made vaults mixed into random levels, the anti-tedium design philosophy). Use when the user wants to play, learn or talk about Crawl, look up a rule, read its level design language, or borrow roguelike systems for Heresiarch or other games.
---

# Dungeon Crawl Stone Soup

The user's Flatpak install (2026-11-01; "might not be working properly"). Version check works
(`flatpak run org.develz.Crawl -version` prints 0.34.1); the game window has not been tried yet, and
it has never been run (no `~/.var/app/org.develz.Crawl`). Test it with the user at the desk: launch, look
at the start screen, quit; game-ui can drive it (find the window class first).

## Files (copied from the Flatpak's `share/crawl/`)

- `docs/crawl_manual.txt` (3251 lines): the manual. Also `quickstart.txt`, `options_guide.txt`,
  `keybind.txt`, `macros_guide.txt`, `aptitudes.txt` (species x skill table), `fight_simulator.txt`,
  `arena.txt`, `tiles_help.txt`, `changelog.txt`, `develop/` (developer docs).
- `dat/des/`: 143 level design files in Crawl's vault language (hand-made rooms and levels placed into
  random dungeons); `dat/dlua`, `dat/clua`: Lua; `dat/database`, `dat/descript`: monster and item text.

## Manual map (sections)

A Overview · B Starting screen · C Attributes and stats · D Exploring · E Experience and skills ·
F Monsters · G Items · H Spellcasting · I Targeting · J Religion · K Mutations · L Licence and
history · M Macros, options, performance · N Philosophy · appendices: species, backgrounds, skills,
keys, inscriptions, sprint modes. New players: the in-game tutorial, then hints mode.

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

## Species and backgrounds (read 2026-11-01, manual appendices 1-2, lines 1564-2288)
In my own words; check `docs/aptitudes.txt` for exact numbers, `%` at character choice.
- **Simple species:** Gnoll (learns every skill at once, can't focus; finds items), Minotaur
  (best physical fighter, no magic, headbutts back), Merfolk (fast in water; polearms/short
  blades, ice/alchemy), Gargoyle (low HP, big natural AC, poison-immune, blunt/unarmed, earth
  magic, flies later), Mountain Dwarf (axes/maces, fire/earth, armour hurts casting less, great
  invocations), Draconian (no body armour, slow levels, natural AC, a colour at XL7 with breath),
  Troll (very strong, fast regen, no magic, little armour), Deep Elf (all magic, frail, bows ok),
  Armataur (rolls toward foes for free moves and MP; armour/shields).
- **Intermediate:** Human (balanced; heals on exploring), Kobold (small, stealthy, short vision,
  devices), Demonspawn (random demonic mutations, invocations, no good gods), Djinn (spells come
  with XL, cast from HP, no boots, fire-resistant, cold-weak), Spriggan (very fast and dodgy, no
  armour, no destructive magic), Revenant (undead, casts through claw attacks), Tengu (fighter,
  flies later, frail), Oni (huge, double potion healing, throws rocks), Barachim (leap, slow walk).
- **Advanced:** Coglin (two weapons via exoskeleton, no jewellery), Vine Stalker (damage split
  HP/MP, no healing potions), Poltergeist (many hats/boots/cloaks, hexes, throwing), Demigod (no
  god, big stat gains, slow levels), Formicid (no teleport/haste; shield + 2-hander), Naga (slow
  move, stealth, poison spit, constrict), Octopode (8 rings, no armour, stealth), Felid (no weapons
  or armour, extra lives), Mummy (undead, can't drink, flammable).
- **Backgrounds:** warriors (Fighter: weapon, medium armour, shield, might potions; Gladiator:
  weapon, light armour, nets; Monk: piety boost on first god; Hunter: shortbow; Brigand: dagger +
  poisoned/curare darts); zealots (Berserker: Trog; Chaos Knight: Xom, random; Cinder Acolyte:
  Ignis, fire, temporary god); adventurers (Artificer: wands; Shapeshifter: talismans; Wanderer:
  random; Delver: starts deep with escape items); warrior-mages (Warper, Hexslinger, Enchanter,
  Reaver); mages (Hedge Wizard, Conjurer, Summoner, Necromancer, Forgewright, Fire/Ice/Air/Earth
  Elementalist, Alchemist). Beginner picks per the manual: Gladiator, Berserker; mages: Conjurer,
  Hedge Wizard. Brighter names in the background menu = better fits for the chosen species.
- **First real game (2026-11-01): Minotaur Berserker with an axe** - simplest strong melee,
  Trog's berserk (learned in lesson 5), axes cleave packs.

## Real games log
- **Game 1 (2026-11-01, recorded: `~/Videos/2026-11-01 22-33-52.mp4`): Minotaur Berserker,
  slain by a gnoll on D:2, XL4, 556 turns, score 95.** Morgue: `~/.crawl/morgue/morgue-Claude-20261101-225303.txt`.
  - Went well: ring mail at once (AC 2 -> 5), D:1 cleared at full HP, read-ID'd two scrolls
    (identify, which then named revelation), Strength at XL3, the axe cleaves (killed the worm
    while hitting a gnoll beside it).
  - A shaft dropped me to D:2 ("A malevolent force fills the Dungeon..." came just before it;
    meaning still unknown) - shafts are one-way, a deeper floor than planned.
  - **The death:** a gnoll pack (4 gnolls: flails, halberds, a throwing net) plus a ribbon worm
    (spits webs) met me in an open room. Berserked at 31/34 (right) but stayed in the open
    (wrong). Webs and the net held me; 3 gnolls hit at once. Berserk ended at 14/61 -> 9/41 and
    slowed. **The fatal mistake (the user spotted it):** I pressed `b` at the south-west gnoll from an
    old zoom, but it was already dead (the axe's cleave had killed it while I hit the north one),
    so `b` *walked* me off my square. Slowed, that step gave the last gnoll (halberd, 2 squares
    off) free hits: 2/41, then my one unknown potion was **moonshine** (tipsy), next hit killed me.
  - **Rules from it:**
    1. **Gnolls come in packs, carry reach weapons (halberd hits from 2 squares) and nets.** On
       "You encounter a gnoll", back into a one-wide corridor *before* they arrive, then berserk.
    2. **Berserk must end the fight.** If HP is under half while berserk and more than one strong
       foe is left, the end of berserk (HP x2/3, slowed) will kill me: kill the weakest first and
       never let it run out next to a reach weapon.
    3. **Drink-ID unknown potions when safe, at full HP, with nothing in view** - so in a crisis
       I know whether I hold healing. An unknown potion is a bad emergency button.
    4. Below half HP, `Tab` refuses ("You are too injured to fight recklessly!"): attack with the
       direction key. **While held in a web or net, `Tab` passes no turn**: press a direction
       key to struggle ("You disentangle yourself" / "You rip the net").
    5. **A direction key toward an empty square moves you**, and an axe's cleave kills
       neighbours without a clear message about which one died. After any kill, take a fresh
       zoom (`bgplay.py shot --full; zoom ...`, free, no turn used) before the next directional
       attack; never attack from an old picture. Slowed, one wasted step is often the game.
  - Tool: `scripts/crawlstep.py N` - one `o` per step, fights routine monsters one `Tab` at a
    time with a read after each, stops for items, unknown monsters, 3+ foes, low HP, prompts,
    webs/nets and "too injured". Hand play for anything it stops on.

## Systems
- **Victory**: dive for the Orb of Zot and bring it out; a single death ends the run (manual A).
- **Characters**: a species x background pick; aptitudes per species per skill (`aptitudes.txt`).
- **Research**: experience goes into skills you have used, and you can set which to focus (E): a
  use-based advancement model with player steering.
- **Politics**: gods to worship, each with conducts that grant or withdraw powers (J).
- **Map**: random levels with hand-made vaults mixed in, written in a text level language (`dat/des`).
- **UI**: designed against tedium and grinding (N, "Philosophy"); full keyboard play, tiles or console.
- **Modding**: levels in .des files, game rules partly in Lua, every option in a text init file.

## Needs from the user
- A moment at the desk to open the game window and see what "not working properly" looks like.
