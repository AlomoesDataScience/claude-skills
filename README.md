# Claude Skills for learning, playing and designing games

Skills for [Claude Code](https://claude.com/claude-code) built while Claude learned a library of strategy games
(4X, operational and board wargames, Dominions 6, roguelikes, tabletop RPGs), plus the tools they use and a
system that keeps Claude's context (and usage) small. Only skills and tools are here: no game files, manuals,
data dumps or screenshots.

**165 skills** - 57 generic, 66 for Dominions 6, 40 for other games, 2 theory shelves - and 2 standalone tools.
[CATALOGUE.md](CATALOGUE.md) lists every one; the routing index [.claude/skills/INDEX.md](.claude/skills/INDEX.md)
says which to load for which task.

## Quick start

1. Install [Claude Code](https://docs.claude.com/en/docs/claude-code) and Python 3.10+.
2. Clone this repository and start Claude Code inside it. The generic skills in `.claude/skills/` load at once;
   a game's skills (`Games/<Genre>/<Game>/.claude/skills/`) load when Claude works in that game's folder.
3. Install the programs the skills you use need:
   - **Linux**: [DEPENDENCIES-linux.md](DEPENDENCIES-linux.md)
   - **Windows**: [DEPENDENCIES-windows.md](DEPENDENCIES-windows.md) - recommended equivalents, which skills work
     as is (most of them) and which need porting (the ones that drive a game window, built on X11).
4. Optional but recommended: turn on the hooks below, then run the self-test.
5. Put your own manuals and game files into the matching game folders (or tell Claude where they are).

**Only the generic skills, everywhere:** copy the folders in `.claude/skills/` to `~/.claude/skills/`. Game
skills find the generic ones by walking up to a parent's `.claude/skills/`, so keep them inside this tree.

## What is inside

| Group | Skills | What they do |
|---|---|---|
| **Learning a game** | learn-to-play, learn-to-mod, learn-from-tutorials, manual-first, game-sources, source-triage, wiki-scout, video-watch, rules-skills, generalize-learning | Claude's method for a game it doesn't know: manual first, map the screen, test one thing at a time, write every lesson into a skill |
| **Seeing and driving games** | game-ui, game-setup, loading-screens, map-camera, map-measure, map-usage, photo-map, draw-map, draw-moves, idle-view, hand-back, save-scum, install-windows-games | Screenshots, clicks and keys through a guard, OCR, a lockable background screen (bgplay), whole-map photos stitched into a board |
| **Fighting and planning** | battle-tactics, move-phases, army-log, war-language, screening, scouting, delegate, planning, waiting-checklist | A turn method: picture of the battlefield, a role for every unit, drawn moves, phased orders, both armies logged each turn |
| **Military theory** | military-doctrine (FM 3-90), military-operations (FM 3-0), soviet-doctrine, war-concepts, combat-models (salvo, Lanchester), unit-combat-math, dice-math | Real doctrine and exact maths, turned into game orders and odds |
| **Designing games** | borrow-from-games, game-database, mod-diff, mod-docs | Every learned game as a parts bin; rank-everything databases; what a mod or patch changed |
| **Recording** | obs-record, stream-panel | OBS through its WebSocket; a live log and tracker window for streams |
| **Skills about skills** | skills-manager, check-skills, write-skill, skill-sync | Route a task to skills, lint and budget them, split big ones, build the index, export this repository |
| **Context efficiency** | context-hygiene, context-audit, unload, chat-review, archive-curator, doc-standards, cleanup | See below |
| **Dominions 6** (66) | dom6-* | The deepest set: every mechanic from the manual and wiki, spells, items, pretenders, thugs, battle AI, modding, sprites, maps, a local Mod Inspector |
| **Other games** (40) | `<prefix>-guide` and friends | Rules map, core loop and lessons per game: Field of Glory II and Kingdoms, Aurora 4X, Stars!, Space Empires IV, TOAW IV, War in the Pacific, OCS, Paths of Glory, Star Fleet Battles, Call of Cthulhu, Dungeon Crawl Stone Soup and more |
| **Shelves** (2) | military-theory, economic-theory | Classics as searchable text with their core ideas |

Standalone tools: `Games/Fantasy Strategy/Dominions 6/spritestudio/` (3D-to-sprite editor for Dominions, Linux
and Windows builds) and `Games/Fantasy Strategy/Dominions 6/Maps/mapgen/` (map generator and map-from-picture).

## How Claude finds the right skill

- Every skill has a **short description** (at most 40 words - it is what Claude Code shows in its skill list,
  re-sent on almost every turn) and a **`keywords:` line** with the rest of its trigger words (not shown in the
  list, read by the matcher).
- **[.claude/skills/INDEX.md](.claude/skills/INDEX.md)** is the routing index: a *Routes* table (task -> skills;
  edit it in `skills-manager/routes.md`) and one line per skill, by folder. Each game folder has its own.
- **`check-skills/scripts/checkskills.py "TASK"`** ranks skills for a task in under a second (name, folder,
  description and keywords; rare words count double). As a hook it adds the best matches to every message.
- **Load only what the current step needs**, and read one section of a big skill rather than all of it. Skills
  over 150 lines keep their detail in `reference/*.md` files listed in their SKILL.md.

## Context efficiency

Built after measuring where usage went (4.5 billion input tokens over 19,000 requests; average context 240k).
Everything that enters the context is re-sent on every following request until it is cleared, so the levers
are shorter stretches, fewer requests and less going in.

| Skill | What it does |
|---|---|
| context-hygiene | The working rules: OCR text over screenshots, crops, batched calls, capped outputs, sections not whole files. Also holds `verify.py`, the self-test |
| context-audit | `ctxaudit.py` measures requests, context size, compactions and what entered the context, from the transcripts |
| unload | Hand-off file before a clear (`handoff.py draft`), recall of old context without loading it, and the session archive |
| chat-review | `chatreview.py digest` turns a session into a short digest (a 7 MB transcript became 44 KB), then summarise it or mine it for lessons |
| archive-curator | `curate.py`: one archived session at a time -> proposals (skill edit, memory, backlog) -> a ledger of what is done |
| doc-standards | Progressive disclosure, one fact in one place, dates and sources, lifecycle labels, decision records, size budgets; `docs.py check` |
| cleanup | `cleanup.py scan` catalogues clutter (duplicates, installers, archives, caches, empty files); ticked items move to a holding folder with undo; it never deletes |

### Hooks (optional, recommended)

Add to `~/.claude/settings.json` (or `.claude/settings.json` in your clone); adjust the path if the skills live
elsewhere:

```json
{
  "cleanupPeriodDays": 365,
  "hooks": {
    "UserPromptSubmit": [{"hooks": [{"type": "command", "command": "python3 -I \"$CLAUDE_PROJECT_DIR/.claude/skills/check-skills/scripts/checkskills.py\" hook", "timeout": 10}]}],
    "SessionStart":     [{"hooks": [{"type": "command", "command": "python3 -I \"$CLAUDE_PROJECT_DIR/.claude/skills/check-skills/scripts/checkskills.py\" hook", "timeout": 10}]}],
    "PreCompact":       [{"hooks": [{"type": "command", "command": "python3 -I \"$CLAUDE_PROJECT_DIR/.claude/skills/unload/scripts/handoff.py\" precompact", "timeout": 60}]}],
    "SessionEnd":       [{"hooks": [{"type": "command", "command": "python3 -I \"$CLAUDE_PROJECT_DIR/.claude/skills/unload/scripts/handoff.py\" sessionend", "timeout": 60}]}]
  }
}
```

- The check-skills hook adds the best-matching skills to each message and, after a `/clear`, points to the
  hand-off file if there is one.
- The archive hooks copy each session's transcript (gzipped, screenshots stripped) to `Archive/sessions/` with
  one index line. Claude Code itself deletes transcripts after `cleanupPeriodDays` (default 30).
- A lower compaction trigger helps as well: this workspace compacts at 150k tokens.

### Self-test

```
python3 -I .claude/skills/context-hygiene/scripts/verify.py        # 13 checks: settings, hooks, routing, budgets, archive, tools
python3 -I .claude/skills/skills-manager/tests/routetest.py -v     # does each test task find its skill?
python3 -I .claude/skills/skills-manager/scripts/skills.py check   # lint every skill (frontmatter, budgets, links)
python3 -I .claude/skills/doc-standards/scripts/docs.py check      # document budgets, labels, dates
```
`verify.py` checks your own settings and archive too, so its settings check fails until the hooks are on.

## Adding or changing skills

```
skills.py new NAME "WHAT IT DOES. Use when ..."   # new skill from the template
skills.py check [NAME]                            # lint
skills.py split NAME [--dry]                      # move big sections of a long SKILL.md into reference/
skills.py index                                   # rebuild the routing index
```
The rules for a good skill are in `write-skill`; the documentation rules in `doc-standards`.

## Layout

The same tree as the workspace it came from: games by genre (the genre name carries the theme; computer and
paper games apart: `Wargames/` vs `Tabletop Wargames/`), publisher groups (`AGEOD and Byzantine Games/`), theory
shelves.
```
.claude/skills/<name>/                          generic skills (any game)
.claude/skills/INDEX.md                         routing index (generated)
Games/<Genre>/<Game>/.claude/skills/<name>/     one game's skills (+ that folder's INDEX.md)
Military Theory/, Economic Theory/              shelf skills
CATALOGUE.md                                    every skill (generated)
DEPENDENCIES-linux.md, DEPENDENCIES-windows.md  programs and packages, generated from the code
LEFT-OUT.txt                                    what the export skipped (data, screenshots, private notes)
```
Paths written `<workspace>` mean the folder the skills were built in; `~` is your home folder.

## Branches

- `main` - the current skills.
- `context-inefficient` - the set before the context-efficiency pass (long descriptions, unsplit skills, no
  routing index), kept for comparison.

This repository is generated by `skills-manager/scripts/export.py`; edit the skills at the source, not here.
