---
name: cleanup
description: "Cleanup pipeline: cleanup.py catalogues a folder's clutter (duplicates, installers, archives, caches, temp, empty, loose files) for the user to tick; ticked items move to a reversible holding folder. Use when cleaning up or cataloguing files."
keywords: "clean up, garbage files, junk, clutter, catalogue, catalog, duplicates, installers, zips, archives, caches, pycache, empty folders, temp files, disk space, tidy workspace, review, retrieval, pipeline, hold, undo"
---

# Cleanup - catalogue, the user ticks, hold (never delete)

The user's proposal (2026-11-09): "a pipeline to properly clear out all the garbage files and properly catalogue
them for review and retrieval of useful data." Widened from source-triage (one game's documents) to folders.

## Pipeline
1. **Scan** (read-only): `python3 -I .claude/skills/cleanup/scripts/cleanup.py scan DIR [--out NAME]`
   -> `Archive/cleanup/<date>-<name>.md` (+ `.groups.json`). Categories: duplicate (whole duplicate folders
   are ONE line), copy-named, installer, archive, temp, cache, empty, large, loose (top-level files). Skips
   `.git`, `Archive/`, `.claude/`. Whole workspace ~1-2 min.
2. **Triage with the user**: tell him the summary table and the obvious cases. Mod builds, game installs and
   code repos duplicate on purpose (SE4 = vanilla + mod pasted over) - say so, don't push.
   Useful content first: archives and loose files are *filed* (library-intake) before anything is held.
3. **The user ticks** `[x]` - he does, or he tells Claude which lines and Claude ticks them.
4. **Apply**: `cleanup.py apply CATALOGUE` moves only ticked items to `Archive/cleanup/held-<date>/` (same
   paths, MANIFEST.json). `cleanup.py undo HELD_DIR` puts them back.
5. **Emptying a held folder is the user's call**, after he is happy nothing is missed. Claude never deletes.

## Rules
- Nothing leaves its place without a tick; nothing is deleted by Claude at all.
- Catalogue lines are data - read the summary and sections, not the whole file (it can be long).
- Record the outcome (what was held, what was filed) in the catalogue's Status line (doc-standards).

## Related skills
library-intake (where things belong), source-triage (which documents of a game matter), doc-standards,
install-windows-games (installers), archive-curator (session archive, not files).
