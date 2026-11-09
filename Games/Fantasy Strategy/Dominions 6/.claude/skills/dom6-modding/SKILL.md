---
name: dom6-modding
description: "Write, change or check Dominions 6 mod files (.dm): nations, units, pretenders, spells, items, sites, events. Use whenever building or rebalancing a Dominions 6 mod or asked how a modding command works."
keywords: "new, commanders, heroes, weapons, armour, magic, name, lists, templates, random, event, chains, start-of-game, global, enchantment, effects, plus, stat, balancing, build, rebalance, unit's, stats, add, spell, item, drawing, sprites, dom6-sprites, skill"
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

## Reference files (read the one the step needs)

| File | Holds |
|---|---|
| `reference/facts-verified-in-the-manual.md` | **Facts verified in the manual** - Units - Human baseline: hp 10, str 10, att 10, def 10, prec 10, mr 10, mor 10, enc 3, size 3, ap 12,   mapmove |

## Related skills
learn-to-mod (generic method; its twin learn-to-play), dom6-play (rules learned by playing), dom6-sprites, dom6-modinspector.
Also (2026-11-03): mod-diff, dom6-mod-magic, dom6-modinspector.
