---
name: dom6-modinspector
description: Load one or more Dominions 6 mods (.dm files) into the Mod Inspector (larzm42.github.io/dom6inspector) the way its "load mods" option does, and read the result as text. Reports what the mods add and change (units, commanders, pretenders, heroes, spells, items, weapons, armour, sites, mercenaries, events, nations) with full inspector pages, field-by-field differences from vanilla, the mod lines behind each object, and the inspector parser's errors and warnings with file:line. The whole modded game can then be queried like vanilla. Use when the user wants to read, review, summarise or compare a downloaded or third-party mod, see what a balance mod changes, check how their own mod looks in the inspector (gold autocalc, recruit lists, spell chains), look up a unit or spell as a mod changes it, or check that several mods load together.
---

# Dominions 6 Mod Inspector with mods loaded

Runs the Mod Inspector site's own code headless with mods loaded (`?mod=` in the site's URL)
and writes the modded game out in the same layout as the `dom6-inspector` skill, plus a report
of what the mods touch. It needs that skill (its `build.py`, `dump.js` and vanilla `data/` for
the comparison), git and firefox. One run takes about 40 s.

## Run it (from this skill's folder, `python3 -I`)

```
scripts/inspect_mod.py path/to/mod.dm                       # writes <tmp>/dom6-modinspect/mod/
scripts/inspect_mod.py base.dm addon.dm --out DIR           # several mods, loaded in this order
scripts/inspect_mod.py mod.dm --update                      # pull the latest site first
```

Installed mods are in `~/.dominions6/mods/<name>/<name>.dm`. Older mods in latin-1 are read
fine. Output goes to a temp folder by default: never write it into a mod's folder (it would
end up in releases).

## What it writes

- `report.txt`: the mods loaded and their order, a count of new and changed objects per kind,
  every message the inspector's parser gave (`ERROR: ...`, `WARNING: ...` with `mods/x.dm:line`),
  and the list of every new and changed object with its id.
- `mod_pages.txt`: the full inspector page of each of those objects (stats with breakdowns,
  autocalculated gold, weapons, armour, recruit sites, spell effects, nation recruit lists),
  tagged `[new]` or `[changed]`. Changed objects get a `changed from vanilla:` list
  (`hp: 12 -> 15`), and pages end with `mod lines [modded]:`, the mod lines that touched the
  object (`1:347 #newmonster 6404`; the first number is the mod's place in the load order).
- `pages/`, `records/`, `mods.json`, `VERSION`: the whole modded game. Query it with the
  dom6-inspector tool by adding `--data DIR` before the command:

```
../dom6-inspector/scripts/inspector.py --data DIR unit "Hunter-Killer"
../dom6-inspector/scripts/inspector.py --data DIR nation 152          # recruit lists, heroes, gods
../dom6-inspector/scripts/inspector.py --data DIR filter unit modded "goldcost>100"
../dom6-inspector/scripts/inspector.py --data DIR grep "#gcost" --kind unit
../dom6-inspector/scripts/inspector.py --data DIR sprite "Hunter-Killer"  # the TGA in the mod's folder
```

Start with `report.txt` and use `grep -n -A40 "=== unit 6404:" mod_pages.txt` for one object.
For big mods (thousands of changes) summarise by kind and pick out what the user asked about.

## Reading the results

- The inspector's parser is not the game. An `ERROR`/`WARNING` can be a site limitation
  (`unrecognised cmd.. assuming you meant: #prot` for a command the site lacks, `command out of
  context` after a command it did not understand). Check real problems against the modding
  manual (dom6-modding skill, `check_dm.py`) and, in the end, in game (Ctrl+I).
- `WORKAROUND:` lines mean dump.js fixed a site bug so the page could load (a mod command
  such as `#coastcom` stored one value where the site expected a list). The data is still right.
- Mod events and mercenaries are not tagged by the site: new or changed ones are found by
  comparing with vanilla, so they have no `mod lines` part. Unnamed events show as `.`.
- Some units are listed twice by the site (ids like `6404.01`); the report marks the copy.
- `[changed]` objects with "no field differences the site records" were touched by a command
  the site does not show (or set to the value they already had).
- Vanilla comparison uses the dom6-inspector `data/`; if the site was updated since it was
  built, rebuild vanilla (`../dom6-inspector/scripts/build.py`) after `--update` so the diff
  does not pick up the site's own changes.

## If a run fails

`dump.js failed: {...}` gives the JavaScript error, its file and line in the site's scripts,
and the parser messages so far. The site's scripts are in `<tmp>/dom6inspector-build/repo/`.
Try the mods one at a time to find the one that breaks it, then add a workaround to
`../dom6-inspector/scripts/dump.js` like the `prepareData_PostMod` one. A page that never
finishes stops after 5 minutes (`HOLD` in build.py).
