---
name: dcss-guide
description: "Guide to Dungeon Crawl Stone Soup (DCSS 0.34, flatpak): rules, species, gods, level design language. Use when playing or learning Crawl, looking up a rule, or borrowing roguelike systems for Heresiarch."
keywords: "free, open, source, installed, org, develz, classic, diving, orb, zot, manual, quick-start, options, keybinding, guides, plain-text, files, des, vault, lua, were, copied, workspace, manual's, map, launch, test, ideas, worth, background, skills, trained, chosen, focus, conducts, mutations, hand-made, vaults, mixed, random, levels, anti-tedium, philosophy, play, learn"
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
  - **Who is where (the user: screen first, never modify the game to read data; 2026-11-01):** the look
    command `x` costs no time; its cursor starts on my square and direction keys move it one square
    each; the bottom message line names what is there ("The floor.", "An orcish idol.", a monster
    with its wounds). Escape leaves. Tiles are 32 px; I am drawn at about (580, 410) on the
    1600x990 bgplay screen. To do: `near.py` (look at all 8 squares, `attack DIR` that refuses an
    empty square, kills counted from "You kill" lines, plus a zoom image as a cross-check).
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

## Reference files (read the one the step needs)

| File | Holds |
|---|---|
| `reference/playing-it-learned-2026-11-01-tutorial-l.md` | **Playing it (learned 2026-11-01, tutorial lesson 1 done)** - Run it in the background (game-ui bgplay.py): bgplay.py start (virtual screen :5, the   user's input locked  |
