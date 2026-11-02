---
name: dom6-modding
description: Write, change or check Dominions 6 mod files (.dm): new nations, units and commanders, pretenders, heroes, weapons, armour, spells, magic items, sites, name lists, AI templates and events (random events, event chains, start-of-game events, global enchantment effects), plus stat balancing. Use whenever the user asks to build or rebalance a Dominions 6 mod, change a unit's stats, add a spell, item or event, or asks how a Dominions 6 modding or event command works. Not for drawing sprites (that is the dom6-sprites skill).
---

# Dominions 6 modding (.dm files)

The references are `dom6modman.pdf` (v6.36) and, for events, `dom6eventman.pdf` (v6.36), both in
`Games/Fantasy Strategy/Dominions 6/Manuals/`. Never guess a command: look it up in the manual text first. Dominions Enhanced (`Games/Fantasy Strategy/Dominions 6/Dominions Enhanced/DomEnhanced2_17_1.dm`)
is a large working mod to copy patterns from when the manual is unclear.

## Files

- `scripts/manual_text.py [PDF] [OUT]` turns a two-column manual into one searchable text file
  (needs `pdftotext`). Then `grep -n -A4 '^#noheal' OUT` shows a command and its explanation.
  Make one for each manual: `dom6modman.pdf` and `dom6eventman.pdf`.
- The `dom6-inspector` skill is a local copy of the Mod Inspector site: every vanilla unit, spell,
  item, weapon, armour, site, mercenary, event and nation with ids, stats and mod keys. Use it for
  vanilla numbers (`#copystats`, `#weapon`, `#armor`) and to compare a new unit with vanilla ones.
- The `dom6-modinspector` skill loads any .dm (yours or a downloaded one) into that site and
  reports what it adds and changes, with the site's parser errors by line and its autocalculated
  gold, recruit lists and spell chains. Useful as a second check after `check_dm.py`.
- `events.md` is the event manual condensed: block layout, rarities, every requirement and effect
  with its arguments, the order/path/affliction tables, event codes, chains, variables, global
  enchantment events, and the mistakes to avoid. Read it before writing any event.
- `scripts/check_dm.py MOD.dm [MANUAL_TEXT ...]` checks a mod file. It catches unclosed blocks,
  missing images, undefined monster, weapon and armour numbers, unknown names, two-handed weapons
  with shields, priests without `#holy`, a priest-only `#custommagic`, event mistakes (bad rarity,
  missing `[site name]` brackets, unsafe event codes, chains without `#req_code 0`, a `#delay` with
  no next event, unlimited always events, enchantment numbers no spell makes), and (with the manual
  texts) commands that are in neither manual. It prints the event codes the mod uses. Run it after
  every edit. It does not replace loading the mod
  in game; say the mod is untested until the user has loaded it.

Run Python with `python3 -I`. Only system Python with PIL is available (no pip).

## Workflow

1. Read the design notes and the existing .dm before changing anything.
2. Look up every command you are unsure of in the manual text (and Dominions Enhanced for usage).
3. Edit the .dm with small, targeted replacements inside the right `#newmonster ... #end` block, so
   one unit's edit cannot leak into another unit.
4. Run `check_dm.py` with the manual text. Fix all errors.
5. Keep the nation's design document in step with the .dm, and tell the user what to check in game
   (Ctrl+I on a unit shows its numbers and modding info).
   The dom6-ui skill can run the game's own Error Check on an installed mod (Mods > right click),
   and enable or disable a mod in the running game (`mods.py`).

## File basics

- The .dm must sit in a folder with the same name (`mods/madscience/madscience.dm`). File names
  are case sensitive and must not contain spaces. Comments start with `--`.
- Load order is fixed whatever order the file is in: mod info, weapons, armour, monsters, names,
  bless, sites, nations, spells, items, general, poptypes, mercenaries, events. So spells and items
  can refer to the nation by number even though they come later.
- Always give fixed numbers to `#newmonster`, `#newweapon`, `#newarmor` and `#newsite`, so adding
  things later does not renumber them and break saved games.
- Free ranges: weapons 1000-3999, armour 400-999, monsters 5000-8999, nametypes 170-399, sites
  1700-3999, nations 150-499, items 700+, spells by `#newspell` (no number). Descriptions max 1999
  characters.
- `#name` must come first in a new block (after `#copyweapon`/`#copystats`, which overwrite
  everything). Changing a spell's or item's name wipes its description, so set the name first.

## Facts verified in the manual

Units
- Human baseline: hp 10, str 10, att 10, def 10, prec 10, mr 10, mor 10, enc 3, size 3, ap 12,
  mapmove 14 (Dom6 values; horse 20). Mages: mr 13 at level 1, 15 at level 3, 18 is the cap.
- `#gcost N` is a fixed gold price; `10000 + base` makes it autocalculated. `#rpcost` is
  recruitment points: about 10 for a normal soldier, 1 for a simple commander, `10000` = autocalc.
- `#magicskill <path> <level>`, paths 0 Fire, 1 Air, 2 Water, 3 Earth, 4 Astral, 5 Death,
  6 Nature, 7 Glamour, 8 Blood, 9 Priest. Priests also need `#holy`.
- `#custommagic <mask> <chance>`: masks F 128, A 256, W 512, E 1024, S 2048, D 4096, N 8192,
  G 16384, B 32768, H 65536. A mask with only the priest bit crashes the game. Chance over 100 adds
  linked levels.
- `#masterrit N` lets the mage cast rituals needing N more levels than it has.
- Mages need a lab by default; `#reqlab` makes a non-mage need one too.
- `#holy` = sacred. `#slowrec` = takes double commander points.
- Mindless units have morale 50 in vanilla (they dissolve without leadership).
- `#magicbeing` + `#noheal` = heals only in a province with a lab (good for robots). Magic beings
  need magic leadership (`#okmagicleader`/`#goodmagicleader`); undead need undead leadership.
- `#startage` and `#maxage` stop a strong mage from starting old (age grows with magic skill).
  Humans have maxage 50; only Nature magic raises it for living beings.
- Resistances: `#fireres/#coldres/#shockres/#poisonres <n>`; `#invulnerable <n>` is protection
  against non-magic weapons only.
- `#onebattlespell` only accepts vanilla spells, never one added by a mod.
- Mounts: the rider gets `#mountmnr <mount>`, `#unmountedspr1/2` (spr2 after spr1); the mount is its
  own monster. `#nofalldmg` for riders close to the ground.
- Heroes: `#hero1...10 <nbr>`, repeatable ones `#multihero1...7 <nbr>`. `#unique` for named ones.
- Pretenders need `#pathcost` (10 arch mage to 80 dragon) and `#startdom` (1 to 4); `#gcost 10000`
  prices them automatically. A nation gets them with `#addgod`, and realm gods with `#homerealm`
  (several `#homerealm` lines are allowed: 3 Mediterranean, 10 Default, etc.).

Random variants from one recruit (firstshape + montag)
- One recruitable "shell" monster carries `#firstshape -<tag>`. Each variant carries `#montag <tag>`
  (1000-100000). `#firstshape` turns a unit into its first shape "when it feels ok" (unwounded), and a
  negative number picks a random monster with that montag. So each purchase becomes one random
  variant. `#montagweight <1-100>` after `#montag` biases the pick; equal or unset weights = even chance.
- Variants must not have `#firstshape` themselves (or they keep changing), and they are not put on
  the recruit list. Give the shell the same name, stats and sprite as one variant, so the frame
  before the change looks right.
- `#copystats` copies special abilities too, so montag/firstshape may travel with it. Put the
  stats on a clean template monster (no montag, no firstshape, not recruitable) and let the shell
  and every variant `#copystats` the template; never copy the shell or a variant.
- A shape change normally keeps the commander's name, so the name comes from the shell's
  `#nametype`: use one list that suits every variant (e.g. both sexes). Dominions Enhanced does this for its random trees and animals
  (`#newmonster 9377 ... #firstshape -1028`; the variants carry `#montag 1028`).
- Works for troops (`#addrecunit`) and commanders (`#addreccom`). Montags also work in `#summonN`,
  summon spells (`#damage -<tag>`), the recruit limits `#monpresentrec`/`#ownsmonrec` and the shape
  commands (`#secondshape`, `#prophetshape`, `#xpshapemon`...).
- Untested timing: when exactly in the turn the shell changes (probably the healing step, after
  battles) is not in the manual. Check in game whether a fresh recruit fights its first battle as
  the shell.

Weapons and armour
- Spell troops (the user's choice for troop casters): no magic paths, the "spell" is a missile
  weapon with `#magic`, `#armorpiercing` or `#armornegating`, `#nostr` and `#ammo 10xx` (fatigue per
  shot, no limit), so it acts like a cast without needing scripts or a commander.
- Missile weapons: `#range` (−1 = strength, like a javelin), `#ammo` (max 30; over 1000 means each
  shot costs that minus 1000 fatigue), `#nratt -2` = every other round, `#att` = precision.
- Only one damage type per weapon (`#dt_...`); qualifiers like `#armorpiercing`, `#armornegating`,
  `#shock`, `#magic`, `#nostr` stack. `#dt_aff` takes an affliction bitmask in `#dmg`
  (asleep = 1024). `#dt_bouncekill` needs `#aoe 1`. `#bonus` = natural weapon.
- Two-handed weapons cannot be used with a shield (great sword 11, pike 2, halberd 5, maul 14,
  quarterstaff 7...). Use a broad sword (8) or spear (1) with shields.
- Armour `#type` 4 shield, 5 body, 6 helmet, 9 barding. Body armour does not cover the head: give a
  helmet too. `#protparts <head> <body>` exists but is only used on bardings in practice.
  For shields, parry = `#def` − `#enc`.
- Common vanilla numbers: weapons spear 1, pike 2, lance 4, halberd 5, short sword 6, quarterstaff 7,
  broad sword 8, dagger 9, great sword 11, fist 92, bite 20; armour iron cap 20, full helmet 21,
  leather cuirass 5, chain mail cuirass 8, plate cuirass 9, buckler 1, round shield 2, kite 3,
  tower 4.

Spells, items, sites, nation
- Spells: `#school` (−1 unresearchable, 0 Conj, 1 Alt, 2 Evo, 3 Constr, 4 Ench, 5 Thaum, 6 Blood),
  `#researchlevel`, `#path 0/1 <path>`, `#pathlevel 0/1 <lvl>`, `#fatiguecost` (100 = 1 gem or
  slave for rituals), `#effect` (10001 summon, 10021 summon commander, 2 damage, 128 stun,
  134 chain bounce with `#maxbounces`, 20 blink), `#damage` = monster number for summons,
  `#nreff` = how many, `#spec` bitmask (AN 128, shock immunity negates 2048, MR negates 4096,
  doesn't hit friends 262144), `#restricted <nation>`.
- Items: `#constlevel` 1/3/5/7/9, `#mainpath/#mainlevel`, `#secondarypath/#secondarylevel`,
  `#type` (1 one-handed, 2 two-handed, 4 shield, 5 body, 6 helmet, 7 boots, 8 misc), `#spr` (32 or
  64 px, item at most 40 px), `#unique` = forged once, `#autospell` + `#autospellrepeat`. Many
  monster abilities also work on items (see the manual's list).
- Sites: `#newsite`, `#path`, `#level 0` (always found), `#rarity 5` (never random), `#loc 16384`
  (unique), `#gems <path> <n>`, `#lab`, `#homemon`/`#homecom` (capital-only recruits). Nations add
  start sites by name only: `#startsite "Name"`.
- Nation: `#selectnation 150+` for a new nation, then `#name`, `#epithet`, `#era` right after them.
  `#startcom` resets the start army; `#defcom1` resets province defence. `#templegems` makes
  temples give gems. AI pretender templates (dom6-pretender's `pretender.py build` writes one): `#newtemplate <nation>`, `#form`, `#prison`,
  `#magic`, `#domstr`, `#scale <0-5> <value>` (positive = Turmoil, Sloth, Cold, Death,
  Misfortune, Drain). The easiest valid template comes from Ctrl+Shift+S in the pretender screen.

## Events (details in events.md)

- `#newevent` ... `#end` with `#rarity` (1/2 bad, -1/-2 good, 11/12 global; 0/5/10/13 always),
  requirements (`#req_...`), effects, and `#msg` (max 2399 characters).
- Always events fire in every province every month unless requirements limit them
  (`#req_fornation`, `#req_rare`, `#req_myench`, `#req_code`, `#req_pregame`...).
- Units an event makes belong to `#nation` (default independents = an attack; -2 = the province
  owner). Site and named-item commands read the name from `[brackets]` at the end of `#msg`.
- Event codes: only -300 to -5000, a separate block per mod (Dominions Enhanced uses -301 to -309
  and -540). Chains start with `#req_code 0` + `#code <c>`, and end by setting `#code 0`.
  `#delay <turns>` fires the next event in the file later.
- Nation flavour: `#req_fornation <nation>` limits an event to the nation; `#req_pregame 1` with
  rarity 5 sets up start conditions; a ritual with `#effect 10081` and `#damage <ench>` plus
  rarity 5 events with `#req_myench <ench>` makes a custom global enchantment; `#effect 10042` with
  `#damage <id>` fires the event with `#id <id>`.

## Balancing against the game rules

The `dom6-mechanics` skill holds the game manual's formulas. Its `lookup.py` prints any vanilla
unit with gold, resources, recruitment points (Rec = `#rpcost`) and stats, so you can compare a
new unit with a real one. Its `combat_calc.py` gives hit and damage odds. Rules that matter
when setting stats:
- Indirect magic adds to what the .dm gives: Air 3 adds shock res +5 (Air 4 adds +10), Fire, Water
  and Nature give the same for their resistance, Earth 3 adds +3 protection. Each Fire level gives
  +10 leadership, and every path gives magic leadership.
- Resistance subtracts its value and then cuts the remaining damage by twice that %. Mindless
  units have morale 50 in vanilla. Upkeep is gold/15 (sacreds gold/30).
- Each spell a mage casts costs extra fatigue: its base encumbrance plus twice its armour's
  encumbrance. Research = 5 + 2 per magic level.

## Balance notes from the user

- Resistance 15 or more counts as strong resistance or immunity; 30 is true magical immunity.
  Don't hand out 25 casually.
- Inanimate and mindless units should usually have morale 30, not 50.
- Guns (this user's setting): cheap to train, so low recruitment points and few resources, but
  expensive in gold. Archers, by contrast, are expensive to train.
- After a balance change, list every number that changed so the user can check it in game.
