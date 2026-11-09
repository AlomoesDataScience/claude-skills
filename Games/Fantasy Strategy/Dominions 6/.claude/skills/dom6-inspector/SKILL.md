---
name: dom6-inspector
description: "Local copy of the Dominions 6 Mod Inspector with every vanilla unit, spell, item, site, nation and event, searchable from scripts. Use for any vanilla Dominions 6 lookup or the ids and numbers a mod needs."
keywords: "larzm42, github, dom6inspector, commander, pretender, hero, magic, weapon, armour, mercenary, band, stats, shows, gold, resource, costs, recruit, lists, breakdowns, effects, requirements, descriptions, internal, keys, plus, sprites, icons, specific, copystats, armor, selectmonster, req, monster, compare, modded, ones, sprite, look, recruits"
---

# Dominions 6 Mod Inspector (local copy)

Everything on https://larzm42.github.io/dom6inspector/ stored as files in `data/`, built by
running the site's own code headless, so the numbers are exactly what the site shows. The
source commit and the counts are in `data/VERSION` (first build: site commit of 2026-09-18,
4348 units, 1474 spells, 529 items, 885 weapons, 296 armours, 1253 sites, 78 mercenary bands,
3300 events, 135 nations). It is a community database, not Illwinter's: when it disagrees with
the game or the manuals, trust the game (Ctrl+I in game shows the modding info).

## Query it (run from this skill's folder, `python3 -I`, no pip needed)

```
scripts/inspector.py unit "Black Templar"        # full page: stats, weapons, armour, abilities, description
scripts/inspector.py unit 738                    # by id (nation variants have ids like 239.01)
scripts/inspector.py spell fireball | item "amulet of clarity" | weapon 7 | armor 7
scripts/inspector.py site "keep of ulm" | merc arnaud | event 268 | nation ulm   (several matches -> list)
scripts/inspector.py grep "trample" --kind unit  # every object whose page matches a regex
scripts/inspector.py filter unit holy=1 "goldcost<20" "nationname~Ulm"   # table of matches
scripts/inspector.py filter spell "research~Evocation 3" "mpath~F"
scripts/inspector.py keys unit                   # field names usable in filter, with counts
scripts/inspector.py sprite "Black Templar"      # paths of the unit's sprite images
scripts/inspector.py version
scripts/inspector.py --data DIR unit "name"      # query a modded game instead (see below)
```

Filter conditions: `key=v`, `key!=v`, `key<n`, `key>n`, `key<=n`, `key>=n`, `key~text`
(substring, also searches lists like nations), or a bare `key` (set and not 0). Unset fields
count as 0.

## What is in data/

- `pages/<kind>.txt`: one block per object, starting `=== unit 738: Black Templar`, as the site's
  detail page in text: `label: value [mod key]   (breakdown)`. The `[key]` after a value is the
  site's internal key, usually the mod command without `#` (`[holy]`, `[mountmnr]`, `[req_minpop]`).
  Breakdowns explain derived numbers, e.g. `defence skill: 13 (12 +3 (mounted), -2 (weapons),
  -6 (armor), +6 (shield parry))`. References carry ids: `#4 Lance`, `#3584 Black Destrier`.
  Units list weapons (length, attack, damage) and armour (protection, defence, parry, encumbrance),
  sprite paths and the description; spells include the next-spell chain, effect numbers, damage,
  spec, details and descriptions; events show requirements and effects with their mod keys;
  nations list commanders, units, capital-only and terrain recruits, heroes, pretenders, start
  sites, national spells and home realms.
- `records/<kind>.jsonl`: the same objects as computed fields (one JSON per line), for filtering:
  `goldcost` (the site's autocalc, mounts included), `rcost`, `typechar` (unit, commander,
  pretender, hero, "unit (cap only)"...), `nations`, `nationname`, `mpath`, `research`,
  `recruitedby`, `summonedby`, weapons and armour as `{id, name}`. `rpcost 10000` means
  autocalculated and is not worked out.
- `gamedata/*.csv`: the site's raw tables (BaseU units, BaseI items, spells, weapons, armors,
  MagicSites, Mercenary, events, nations, attribute_keys and attributes_by_*, effects_*, recruit
  lists by nation...), tab separated, for anything the pages do not show.
- `images/sprites/NNNN_1.png` and `_2.png` (idle and attack, `_rider_` for mounted units),
  `images/items/itemN.png`, `images/sites/`. The vanilla sprites are good stance and scale
  references for the dom6-sprites skill.

## Typical uses

- Modding: find vanilla ids and stats to copy (`#copystats 738`, `#weapon 4`, `#armor 215`),
  check what a vanilla command looks like on a real unit (`grep "\[slaver\]" --kind unit`),
  compare a modded unit's stats and cost with vanilla units of the same role (`filter unit`).
- Events: `inspector.py grep "req_anycode" --kind event` shows vanilla events using a command,
  with every requirement and effect spelled out (see dom6-modding's events.md for the commands).
  Keys the site has no name for appear as raw numbers (`req_9600 [req_9600]: 70`, `[2700]`).
- Playing: what a nation recruits, its heroes and pretenders, what a site or item does.

## Mods

To read a mod (or several) as the site shows it with mods loaded, use the `dom6-modinspector`
skill: it writes the modded game in this same layout plus a report of what the mods add and
change, and `--data DIR` points every command here at it.

## Updating

`python3 -I scripts/build.py` re-clones the site (github.com/larzm42/dom6inspector), runs it in
headless firefox with `scripts/dump.js` injected, and rewrites `data/` (about 30 s; 68 MB with
images, `--no-images` skips the 42 MB of pictures). Needs git and firefox. If the site changes its
page layout, dump.js may need a new hook: it wraps `DMI.initGrids`, then calls each object's
`renderOverlay`. `build.dump(repo, out, query)` and `write_data(..., data=DIR)` are also used by
dom6-modinspector; dump.js also collects the mod parser's console messages and works around a
site crash on some nation commands.

## Related skills
dom6-modinspector (mods loaded), dom6-modding, dom6-spells, dom6-items, dom6-tactics (matchups).
Also (2026-11-03): dom6-spell-db, game-database, dom6-abilities.
