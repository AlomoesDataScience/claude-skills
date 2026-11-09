---
name: mod-docs
description: "Keep modded games apart from vanilla: find the mods and versions first, one folder per mod, check the mod before quoting numbers. Use when a game may run mods, before quoting any stat."
keywords: "generic, rules, keeping, separate, base, runs, give, skill, named, game-mod, dom6-scbm, database, change, tables, playthrough, notes, skills, pointer, line, most, tag, number, source, mod's, files, manual, wiki, record, changes, diffs, against, handle, stacks, rule, after, quoted, destruction, scbm, playing, discussing, balance, overhauls, total, conversions, workshop"
---

# Documenting modded games

The user (2026-11-03): "You have to save all this to a separate SCBM folder. Add a generic skill to properly
respect and separate documentation rules separate for modded games." I had answered spell questions for his
SCBM Dominions game from the vanilla manual (Destruction needs E3; SCBM makes it E2) and written his
game's notes into the vanilla tactics skill.

## 1. Know what is loaded - before any number
- At the start of a game (or a talk about one), find out: vanilla or modded? Which mods, which versions, in
  what load order? Read it from the game (mod menu, game settings, the save's header, the lobby), or ask
  the user once and write it down in the mod folder's file and the game's plan file.
- A multiplayer game's mods are fixed when it starts: record per game which mod version it uses.
- Never change which mods are on unless the user asks (his settings).

## 2. Order of truth in a modded game
the game screen > the mod's own files (the block that changes that object) > a database built WITH the mod
(mod inspector, a modded wiki) > the vanilla manual > videos > the vanilla wiki > what the user says (test it if he insists) > a hypothesis.
- Before quoting any unit, spell, item or rule number: grep the mod's files for the object. No hit = vanilla
  holds (say so: "unchanged in SCBM"). A hit = use the mod's value and name it as such.
- Manuals and wikis describe vanilla. Rules (how trample works) usually survive mods; numbers often don't.
- Mods also change AI behaviour (cast weights, recruitment): that changes what the player must script.

## 3. One folder per mod, vanilla stays vanilla
- Each mod gets its own skill folder next to the game's skills: `<game>-<mod>` (dom6-scbm). It holds:
  - the mod loaded into whatever database the game has (Dominions: dom6-modinspector -> `data/`);
  - generated change tables (vanilla -> mod, by kind), rebuilt by a script, never edited by hand;
  - hand-written notes on what the changes mean in play;
  - playthrough notes for the games played with it (one file per game: decisions, battles, lessons).
- Vanilla skills keep only vanilla facts. A rule learned in a modded game that is vanilla anyway (checked
  in the manual) goes to the vanilla skill, marked "learned in <game>; vanilla rule". Anything that needs
  the mod's numbers goes to the mod folder. At most one pointer line in the vanilla skill.
- A total conversion (a different game on the same engine) gets the full treatment of a new game
  (learn-to-play), not just a change table.
- Game records (maps, battle replays, GIFs) stay where the game's plan files are; the mod folder links them.
- Never write documentation into the mod's own install folder (it ships with the mod and gets overwritten).

## 4. Tag sources
Every number in notes carries where it came from: `(vanilla manual p.123)`, `(SCBM 1.13 .dm)`,
`(seen in game)`, `(wiki, vanilla)`. When a mod number differs, write both: `Destruction E2 (vanilla E3)`.

## 5. Mod versions and stacks
- New version: rebuild the database and the change tables into the mod folder; keep the old version's data
  if a running game still uses it; re-check the hand-written notes against the new table.
- Several mods loaded together: the database is built with all of them in load order; the folder is named
  for the main mod, and its file lists the others. Small add-on mods can share the main mod's folder.

## 6. When the user corrects a number
Fix it in the mod folder, check whether the same mistake sits in a vanilla skill (remove the mod number from
there), and add the object to the mod notes so it isn't looked up wrong again.

## Per game
- Dominions 6: SCBM 1.13 -> `dom6-scbm` (Games/Fantasy Strategy/Dominions 6/.claude/skills). Database:
  dom6-modinspector. The user's Tir na n'Og MP game runs it.
- (Add each modded game here: SE4 WMD mod, ...)

## Related skills
learn-to-mod (making mods), manual-first (order of truth), generalize-learning (what goes up to generic),
write-skill, skills-manager, game-sources, library-intake.
