---
name: skill-sync
description: Keep skills up to date with the skills they learn from, and move single files in and out of skills (sync.py). A skill's sources are the generic skills it builds on or names and its counterparts in other games (dom6-map <-> fog2m-map); mark records "up to date with these sources", status shows what changed in them since (new, changed, removed SKILL.md sections and scripts), diff shows the changes, gaps lists skills one game has and another lacks, load copies a script or side file into a skill with its origin recorded, unload retires a file to retired/ with the reason, provenance flags loaded files whose original changed. Use when a generic skill or another game's skill gained lessons or tools that should reach this game, at the start of a session with a game whose skills may be stale, after a game session that changed skills (carry it to the other games), when porting a tool from one game to another, when a file in a skill is obsolete, or when the user says skills are out of date.
---

# Skill sync

The user (2026-11-03): "create a skill to load and unload files, and update skills from generic and other specific
game skill changes" - after the Dominions skills fell "highly out of date" while FoG II gained a new look
process, camera tools and rules. Whole skills are loaded and unloaded with skills-manager (`skills.py enable /
disable`); this skill works on what is INSIDE skills.

`scripts/sync.py` (standard library; reuses skills-manager's skill finder). Ledger and snapshots:
`.claude/skill-sync/` at the project root.

## Where updates come from
- **Generic skills** a skill builds on or names (skills.py uses/related, root `.claude/skills`): game-ui,
  photo-map, map-measure, battle-tactics, planning...
- **Counterparts** in other games: the same name after the game prefix (dom6-map <-> fog2m-map, dom6-scouting
  <-> fog2m-scouting). Roles with different names are added by hand: `sources dom6-game --add fog2m-guide`.
- `gaps FROM TO` lists the skills one game has and the other lacks (fog2m-scouting, no dom6-scouting yet).

## The update loop
1. `changed --since DATE` - which skills changed lately (find the source of news; newest first).
2. `status SKILL` - per source, what changed since the last mark: `+`/`~`/`-` sections and files.
   Never synced: `diff SKILL SOURCE` lists the source's sections and marks the ones this skill lacks.
3. `diff SKILL SOURCE [--file REL]` - the changes themselves.
4. **Carry over by judgement, not by copy** (generalize-learning tests): a method or rule goes in (adapted to
   this game's screen, keys and rules - check them in the game or its manual first, manual-first); numbers,
   coordinates and keys of the other game stay out; something that doesn't apply gets a one-line "not here,
   because..." so the next sync doesn't ask again (Dominions is provinces, not squares: no grid tools).
   A lesson that is really generic goes UP into the generic skill first, then down to every game.
5. Test what can be tested (a ported tool runs on the live screen, read only where the user says so).
6. `mark SKILL --note "what was carried over"` - snapshots the sources: the next status starts from here.
7. Finish: `skills.py check` + `index`, the game's plan file ticked.

## Files in and out
- `load SRC_SKILL REL DEST_SKILL [--as REL2]` copies one file (a script, a side .md) into another skill and
  records where it came from; it refuses to overwrite (compare first, then `--force`). Then adapt it and name it
  in the skill. Prefer one shared generic script over copies: load a file only when the game needs its own
  version (dom6bg.py took order.py's snap/lookat, not a copy of order.py).
- `unload SKILL REL --why TEXT` moves a file to `SKILL/retired/` (never deleted) with the reason and prints the
  SKILL.md lines that still mention it (FoG II: board.py, terrscan.py, tilemap.py, fogadvance.py retired).
- `provenance [SKILL]` - loaded files whose original changed since (re-load or merge).
- The bare-run rule holds for loaded scripts too: run with no arguments = usage only (write-skill).

## When
- Start of a game session: `status` for that game's skills (and `changed` since the last session).
- End of a session that changed a skill: `gaps` and `status` for the other games' counterparts; note the
  carry-overs in their plan files if there is no time now.
- Before the GitHub export (skills-manager export.py): no skill left half-synced.

## Related skills
skills-manager (whole skills: route, check, index, enable/disable, export), generalize-learning (what goes up
to generic and what stays), write-skill (house style), manual-first, planning, learn-to-play.
