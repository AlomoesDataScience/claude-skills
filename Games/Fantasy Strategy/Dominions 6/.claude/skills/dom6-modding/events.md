# Dominions 6 events (from dom6eventman.pdf, v6.36)

Events go in the same .dm as everything else and load last (after spells and items). The PDF is
`dom6eventman.pdf` in `Games/Fantasy Strategy/Dominions 6/Manuals/`; make it searchable with
`python3 -I scripts/manual_text.py ../../../Manuals/dom6eventman.pdf /tmp/dom6eventman.txt` (run from this
skill folder), then `grep -n -A4 '^#req_targorder' /tmp/dom6eventman.txt`. Look a command up there
before using it. Dominions Enhanced has about 1,800 working events to copy patterns from
(`grep -n -A15 '#newevent' "Games/Fantasy Strategy/Dominions 6/Dominions Enhanced/DomEnhanced2_17_1.dm"`).

## Block

```
#newevent            -- or #selectevent <nbr> to change a vanilla event; #clear empties it
#rarity <nbr>
...requirements (#req_...)
...effects
#msg "text"
#end
```
`#clearallevents` removes every event in the game (almost never wanted).

## Rarity

| Nbr | Meaning |
|---|---|
| 1 / 2 | common / uncommon bad |
| -1 / -2 | common / uncommon good |
| 0 | always: every month in every province unless limited; only one rarity 0 event per province per month |
| 5 | always, unlimited: any number per province per month (global enchantment and dominion effects) |
| 10 | always global |
| 11 / 12 | common / uncommon global |
| 13 | always immediate global |

Normal random events use 1, 2, -1, -2, 11 or 12. Global events are planned 7 months ahead (so
fortune tellers can see them), except rarity 13, which happens at once. **An always event
(0, 5, 10, 13) fires everywhere every month unless requirements limit it**: give it `#req_rare`,
`#req_fornation`, an enchantment, a code, a site, `#req_pregame` or similar.

## Requirements (all must hold)

Generic
- `#req_rare <percent>` chance it is valid when rolled (with an always event = chance per province).
- `#req_turnrare <value>` chance = value + turn number; negative = 0% until that many turns passed.
- `#req_unique <n>` at most n times per game. `#req_permonth <n>` at most n times per month.
- `#req_story 0|1`, `#req_indepok 0|1` (also for independents), `#req_ai 0|1` (AI players only).
- `#req_era 1|2|3`, `#req_noera`, `#req_turn` (not before), `#req_maxturn` (not after).
- `#req_pregame 1`: happens once, right after game creation; message shows on turn 1. Needs an
  always rarity (0 or 5). Used for special start conditions (DE: start resources, population).
- `#req_season 0-3` (spring, summer, fall, winter), `#req_noseason`, `#req_month 0-11`.

Nation
- `#req_nation` (must be in play), `#req_nonation`, `#req_fornation` (only this nation; repeat for
  several), `#req_notfornation` (old name `#req_notnation`), `#req_notforally`.

Treasury and research
- `#req_gem <type>` at least one gem; `#req_gold <amount>`; `#req_path <type>` then
  `#req_pathgems <amount>`. `#req_school <school>` then `#req_minresearch <level>`.

Province
- `#req_capital 0|1`, `#req_nearbycapital 0|1`, `#req_owncapital 0|1` (event owner's own capital).
- `#req_poptype`, `#req_notpoptype`, `#req_pop0ok` (default: only provinces with 5+ dekapop),
  `#req_minpop`/`#req_maxpop <dekapop>` (1 dekapop = 10 people).
- `#req_mindef`/`#req_maxdef` (PD), `#req_minunrest`/`#req_maxunrest` (both ±25%).
- `#req_lab`, `#req_temple`, `#req_fort 0|1`, `#req_fortid <fort>`.
- Terrain 0|1: `#req_land` (0 = sea), `#req_coast`, `#req_mountain`, `#req_forest`, `#req_farm`,
  `#req_swamp`, `#req_waste`, `#req_cave`, `#req_kelp`, `#req_gorge`, `#req_deep`,
  `#req_forestcave` (DE also uses `#req_caveforest`), `#req_drip`, `#req_crystal`,
  `#req_freshwater`, `#req_nativesoil` (land, or underwater for underwater nations).
- Planes: `#req_plane <n>` (0 main, 1+ map planes, -1 cave, -2 nexus), `#req_void 0|1`,
  `#req_voidok 0|1`. `#req_provnbr <province>` for fixed maps.
- Corpses: `#req_mincorpses`, `#req_maxcorpses`.

Sites (put the site name in brackets at the end of `#msg`, spelled exactly as in game; 0 inverts)
- `#req_site 0|1` (present), `#req_foundsite` (found), `#req_hiddensite` (not found),
  `#req_nearbysite` (here or adjacent), `#req_nositenbr <site nbr>` (number, no brackets),
  `#req_freesites <n>` (use it whenever the event adds a site), thrones: `#req_claimedthrone`,
  `#req_unclaimedthrone`, `#req_thronesite`, `#req_nearbythrone`.

Dominion
- `#req_fullowner <nation>` (controls province and fort, positive dominion), `#req_domowner <nation>`,
  `#req_mydominion 0|1`, `#req_dominion <0-10>` (owner's candles), `#req_maxdominion <-10..10>`
  (negative = enemy dominion at least that strong), `#req_domchance <0-100>` (chance = candles ×
  value %, whoever owns the dominion).
- Pretender: `#req_godismnr` / `#req_godisnotmnr` "name"|nbr (repeatable), `#req_godawake 1`,
  `#req_pretismnr`, `#req_pretawake` (disciples use the team's pretender).

Scales, -3..3; a negative value also allows the opposite side up to that strength
(`#req_growth -1` = Growth, neutral or Death 1): `#req_chaos #req_lazy #req_cold #req_death
#req_unluck #req_unmagic #req_order #req_prod #req_heat #req_growth #req_luck #req_magic`.

Monsters ("name" | number)
- In the province: `#req_monster`, `#req_2monsters`, `#req_5monsters`, `#req_nomonster`,
  `#req_monsterbs` (also matches the birthshape), `#req_commander 0|1` (non-sneaking),
  `#req_mintroops`, `#req_maxtroops`, `#req_researcher`, `#req_humanoidres`,
  `#req_preach <value>` (chance per priest level while preaching).
- In the world: `#req_mnr`, `#req_nomnr` (repeat = all / none), `#req_deadmnr` (alive or dead
  unique), `#req_realmnr`, `#req_norealmnr` (ignore shapechanges), `#req_mnrbs`.
- Mages in the province: `#req_path<fire|air|water|earth|astral|death|nature|glamour|blood|holy>
  <level>`, `#req_nopath<...> <level>`, `#req_nopathall <level>`.

Target commander (one commander must meet all of them; repeatable ones = any of the values).
By default only commanders of the land's owner; `#req_targforeignok` allows others.
- Type: `#req_targmnr`, `#req_targnomnr`, `#req_targrealmnr`, `#req_targnorealmnr`,
  `#req_targgod 0|1|2` (2 = pretender only), `#req_targprophet 0|1`.
- Body: `#req_targhumanoid 0|1` (hands), `#req_targsight`, `#req_targmale 0|1` (0 = female),
  `#req_targminsize`, `#req_targmaxsize`, `#req_targundead #req_targdemon #req_targanimal
  #req_targinanimate #req_targmindless #req_targimmobile #req_targmagicbeing` (0|1).
- Magic: `#req_targpath1..4 <path>` (level n+), `#req_targnopath1..4 <path>` (below n),
  `#req_targmanygems <path>` (> d20 gems; 53 all, 56 all but blood).
- State: `#req_targaff` / `#req_targnoaff <bitmask>`, `#req_targhorrormark <n>`,
  `#req_targorder <order>` (repeatable), `#req_targnoorder`, `#req_targitem` /
  `#req_targnoitem "item"|nbr`, `#req_targinsane 0|1`, `#req_targminmorale`,
  `#req_targmaxmorale`, `#req_targseductions <n>`, `#req_targminkills`, `#req_targmaxkills`.
- Owner: `#req_targowner <nation>` (once, not negative), `#req_targnotowner`, `#req_targally`,
  `#req_targnotally`.

Event codes (province numbers set by `#code`; see chains below)
- `#req_code <c>` (any of several), `#req_notcode`, `#req_anycode` (anywhere), `#req_notanycode`,
  `#req_nearbycode` (neighbour), `#req_nearowncode` (here or a neighbour with the same owner).

Global enchantments (ench nbr = the spell's `#damage` with `#effect 10081`)
- `#req_ench`, `#req_noench`, `#req_myench` (owned by the event owner), `#req_friendlyench`,
  `#req_hostileench`, `#req_enchdom` (inside the enchantment owner's dominion),
  `#req_enchtarget` (origin is this province), `#req_enchnearby`, `#req_minglobals`,
  `#req_maxglobals`.

Event variables (0-9999, start at 0): `#req_varpos` (>= 1), `#req_varneg` (<= -1),
`#req_varzero`, `#req_varone`. Special numbers: -1 = receiving nation's number, -2 = 500 + player,
-3 = 1000 + province, -4 = 3000 + province (so -1 can touch vars up to 499, -3/-4 up to 4999).

Misc: `#req_arenadone 0|1`, `#req_worlditem`, `#req_noworlditem "item"|nbr`.

## Effects

Owner and message
- `#nation <nation>` owner of the event (default independents; -1 random enemy, -2 province owner;
  2 = special independents). `#nationench <ench>` = owner of that global enchantment.
- `#msg "text"` at most 2399 characters. Bracketed name at the end for site/item commands.
  Tags: `##landname## ##godname## ##fullgodname## ##disname## ##goddisname## ##targname##
  ##fulltargname## ##targhis## ##natname## ##profname##` (targ tags not in global events).
- `#header 1` (no "unexpected"), `#header 2` (no header: the first line becomes the header, end it
  with two newlines). `#notext` (no message), `#extramsg <nation>`, `#nolog` (not in the
  province chronicle). DE gives silent bookkeeping events `#msg "x"` + `#notext` + `#nolog`.

Treasury
- `#gold` (±50%), `#exactgold`, `#forcegold`, `#forceexactgold` (force = even if income cannot be
  traced to a friendly fort). Negative = loss.
- Gems (gem types 0 F, 1 A, 2 W, 3 E, 4 S, 5 D, 6 N, 7 G, 8 blood slaves): `#1d3vis #1d6vis #2d4vis
  #2d6vis #3d6vis #4d6vis <type>` (need a friendly lab to trace to) and `#force...vis` versions.
  `#gemloss` 3d6 (53 = 1d6 of each, 56 = all but blood), `#gemlosssmall` 2d6, `#gemlosslarge` 4d6.
- `#magicitem <rarity>` into the lab: 0 const 1, 1 const 1-3, 2 const 1-5, 3 const 1-7, 4 const 5-7,
  9 = the item named in brackets in `#msg`.

Scales (0 Turmoil/Order, 1 Sloth/Productivity, 2 Cold/Heat, 3 Death/Growth, 4 Misfortune/Luck,
5 Drain/Magic; inc = toward the first, dec = toward the opposite)
- `#incscale #incscale2 #incscale3 #decscale #decscale2 #decscale3 <scale>`.

Province
- `#landgold`, `#landprod` (permanent), `#taxboost <percent>` (one turn; -100 = no gold),
  `#defence <n>` (PD), `#kill <percent>`, `#killpop <dekapop>`, `#incpop <dekapop>`,
  `#emigration <percent>`, `#inccorpses`, `#unrest <n>` (the manual's example writes
  `#incunrest`, which is not a listed command: use `#unrest`), `#incdom <candles>`,
  `#newdom <n>` (owner's dominion at 1dn candles).
- `#fort <fort nbr>` (0 removes), `#temple 0|1`, `#lab 0|1`, `#revolt`, `#revealprov`,
  `#claimthrone`, `#setpoptype`, `#addgeo` / `#remgeo <terrain bitmask>` (128 = forest),
  `#newnbor` / `#remnbor <province>`, `#visitors` (Bogus the Troll attacks).
- Sites: `#revealsite` (bracket name), `#addsite <site nbr>` (found; -1 = bracket name),
  `#maybeaddsite`, `#hiddensite`, `#maybehiddensite`, `#removesite` (-1 = bracket name).

Units ("name" | number; owned by the event owner)
- Commanders: `#com`, `#2com`, `#4com`, `#5com`, `#stealthcom` (sneaking).
- Troops: `#1unit`, `#1d3units` ... `#4d3units`, `#1d6units` ... `#16d6units`, `#var0units`
  (count = event var 0). `#tempunits 1` before them = they vanish after the event (Ghost Riders).
- Attacks: `#assassin` (attacks a random commander, or the target), `#assowner <nation>`,
  `#assownerench <ench>`, `#assfollower1|2|3|1d3`. `#strikeunits <damage>` hits everyone.
- `#killmon`, `#kill2d6mon` (non-commanders), `#killcom`, `#curse <%>`, `#disease <%>`,
  `#researchaff <bitmask>`.

Target commander (set by the req_targ commands; `#cleartarg` drops it)
- `#gainaff`, `#gainaffmount <bitmask>`, `#gainmark`, `#healaff`, `#healaffmount <n>`,
  `#banished <-11 Void | -12 Inferno | -13 Kokytos>`, `#addequip <1-4 | 9 = bracket item>` (items and
  gems), `#transform`, `#forcetransform` (works on gods and polymorph-immune units; negative =
  montag), `#remount`, `#poison <dmg>`, `#killtarg`, `#xp`, `#setxp`, `#addseductions`,
  `#addkills`.
- Path boosts: `#fireboost #airboost #waterboost #earthboost #astralboost #deathboost
  #natureboost #glamourboost #bloodboost #holyboost "name"|nbr` (-1 when a target is set) or
  `#pathboost <path 0-9>` (+1, max 5).

Global (every province): `#worldincscale[2|3]`, `#worlddecscale[2|3]`, `#worldunrest`,
`#worldincdom`, `#worldritrebate <school>` (-20% ritual cost this turn; rarity 11 or 12 only),
`#worlddarkness`, `#worldcurse`, `#worlddisease`, `#worldmark`, `#worldheal <%>`, `#worldage
<years>`, `#linger <turns>` (effect lasts), `#dispglobals <str>`.

Chains, codes and variables
- `#code <c>` sets the province code (at planning for globals), `#code2` (at execution).
  `#codedelay` / `#codedelay2` set it after this turn's / next turn's events.
  `#resetcode <c>` removes it everywhere; `#resetcodedelay`, `#resetcodedelay2`.
- `#flagland 0|1` book icon on the map; needs a code, disappears when the code goes back to 0.
- `#delay <turns>`, `#delay25`, `#delay50` (±%): the **next event in the file** happens that many
  turns later and never occurs normally. `#delayskip <percent>` right after
  a delay = chance the event after next is used instead.
- `#order <bitmask>` special orders for the province: 1 Investigate, 2 Continue, 4 Accept,
  8 Decline, 16 Withdraw, 32 Attack, 64 Diplomacy, 128 Subterfuge, 256 Magic (0 clears).
  Check the choice in the next event with `#req_targorder` (100 Investigate, 101 Continue,
  102 Accept, 103 Decline, 105 Attack, 106 Diplomacy, 107 Subterfuge, 108 Magic).
- `#purgecalendar` / `#purgedelayed <1 next | 0 this | -1 previous>`.
- `#id <eventid>` identifies the event for a spell with `#effect 10042` (Cause event,
  `#damage` = event id).
- Variables: `#clearvar #incvar #decvar #inc10var #dec10var #invvar #togglevar <var>`.

Misc: `#arena`, then `#resolvearena1` (or `#resolvearena2`, no magic) the next turn;
`#addascension <AP>`, `#minascension <AP>` (thrones victory only).

## Tables

Target orders: 0 Defend, 2 Sneak, 3 Patrol, 4 Research, 6 Preach, 7 Site search, 8 Blood hunt,
14 Call God, 17 Summon allies, 18 Build lab, 19 Build temple, 20 Build fort, 44 Demolish fort,
45 Demolish lab, 50 Enter site, 52 Void summon, 100-108 event orders (above).

Paths: 0 F, 1 A, 2 W, 3 E, 4 S, 5 D, 6 N, 7 G, 8 B, 9 Priest/Holy, 50 random, 51 elemental,
52 sorcery, 53 all (not priest). Schools: 0 Conj, 1 Alt, 2 Evo, 3 Constr, 4 Ench, 5 Thaum,
6 Blood, 7 Divine.

Afflictions (bit = 2^x): 0 disease, 1 curse, 3 plague, 5 curse of stones, 6 entangle, 7 rage,
8 decay, 9 burn, 10 destroyed armour, 11 rusty armour, 12 blind, 13 bleed, 14 earth grip,
16 fire bonds, 17 false fetters, 18 limp, 19 lost eye, 20 weakness, 21 battle fright, 22 mute,
23 chest wound, 24 crippled, 25 feeble minded, 26 never healing wound, 27 slime, 28 frozen,
29 webbed, 30 arm loss. Add bits for several.

## Rules that are easy to get wrong

- **Event codes**: use only -300 to -5000 (0 = the default "no chain" code). Split the range
  between mods; two mods using the same code scramble each other's chains. Dominions Enhanced
  uses -301 to -309 and -540. Give each of the user's mods its own block (e.g. -1000s, -1100s).
- An event that sets `#code` should require `#req_code 0`, or it can break a chain already
  running in that province. The last event of a chain sets `#code 0` again.
- `#delay` points at the next `#newevent` in the file: keep a chain's events in order and
  together.
- Site, item and named-item commands read the name from brackets at the end of `#msg`; a typo
  silently matches nothing.
- Always events need limits (see Rarity). `#req_permonth 1` keeps a global effect to once a month.
- Global enchantment events: the spell has `#effect 10081` and `#damage <ench nbr>`; events use
  `#req_myench` / `#req_hostileench` / `#req_enchdom` and `#nationench` for the owner. DE numbers
  its enchantments from 200 up; pick an unused block. DE also gives enchantment numbers to
  spells with `#effect 10082`, `10084` and `10085` (province-bound enchantments such as
  Rainmaking); those effect numbers are in neither manual, so copy DE's usage exactly.
- A ritual with `#effect 10042` (Cause event) and `#damage <id>` triggers the event with `#id <id>`.
- Units from events belong to `#nation` (default independents, i.e. an attack). For a gift to the
  province owner use `#nation -2`.
- Messages over 2399 characters are cut. Descriptions elsewhere are still max 1999.

## Examples from the manual

```
-- reveal a hidden site
#newevent
#rarity -2
#req_hiddensite 1
#msg "A famous prospector has discovered previously unknown deposits of precious jewels. [Hidden Gem Deposits]"
#revealsite
#end

-- once per game: W2 D3 humanoid mage site-searching at a unique site gains W+1 D+1 and a wife
#newevent
#rarity -2
#nation -2
#req_unique 1
#req_site 1
#req_targhumanoid 1
#req_targpath2 2
#req_targpath3 5
#req_targorder 7
#msg "... [The Sea of the Tears of Men]"
#waterboost -1
#deathboost -1
#com 1477
#end

-- two-step chain: the first sets code -509 and a delay, the second fires one turn later
#newevent
#rarity 2
#req_land 1
#req_mountain 1
#req_code 0
#code -509
#flagland 1
#decscale3 5
#incscale2 3
#unrest 20
#delay 1
#magicitem 9
#msg "... [Skull Staff]"
#end
#newevent
#rarity 0
#req_code -509
#nation 2
#com "Mound Fiend"
#2d6units "Ghost"
#code 0
#msg "... the denizens of the prison have attacked the province!"
#end

-- global enchantment that gives its owner 500 gold a month and wolves in enemy forests
#newspell
#name "Illvaettitime II"
#school 4
#researchlevel 1
#path 0 6
#pathlevel 2
#fatiguecost 500
#effect 10081
#damage 201
#end
#newevent
#rarity 5
#msg "gold"
#notext
#req_myench 201
#req_permonth 1
#gold 500
#end
#newevent
#rarity 5
#msg "Wolves came out of the forest."
#notext
#req_hostileench 201
#req_rare 35
#req_forest 1
#req_enchdom 201
#req_indepok 1
#nationench 201
#com "Wolf"
#5d6units "Wolf"
#end
```
