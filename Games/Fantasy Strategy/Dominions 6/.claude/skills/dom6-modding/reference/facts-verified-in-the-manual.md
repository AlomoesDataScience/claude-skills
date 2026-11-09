# dom6-modding - Facts verified in the manual

Part of the dom6-modding skill; SKILL.md links here.

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
