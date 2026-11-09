---
name: skills-manager
description: "Manage Claude's skills: route a task to skills, list, check budgets, make, import, disable, and generate the routing INDEX.md (skills.py). Use when adding, checking, loading or indexing skills."
keywords: "project, finds, needs, order, load, lists, builds, checks, frontmatter, name, description, length, missing, files, scripts, compile, creates, new, skill, house, style, has, built, reusable, tool, workflow, imports, folder, zip, unloads, disables, reloads, keeps, catalogue, add, save, install, remove, enable, unload, something, should, become, start, multi-part"
---

# Skills manager

`scripts/skills.py` (standard library only; run with `python3 -I` from this folder) manages the
skills of the whole project hierarchy. The catalogue is `.claude/skills/INDEX.md` (all skills,
grouped by folder); each game folder also gets its own `.claude/skills/INDEX.md`.

```
skills.py route "TASK TEXT" [--n 5]   # which skills fit, best first, with their load order
skills.py list [--all]                # every skill; --all adds user-level and disabled ones
skills.py show NAME                   # description, files, scripts, builds on, used by, see also
skills.py deps [NAME]                 # who builds on whom
skills.py check [NAME]                # lint (exit 1 on errors)
skills.py new NAME "DESCRIPTION" [--uses a,b] [--script tool.py]
skills.py import PATH [--name NAME] [--force]     # a folder, a SKILL.md or a .zip
skills.py disable NAME / enable NAME  # unload to .claude/skills-disabled/, load back
skills.py index                       # rewrite INDEX.md (routing index: routes.md + one line per skill)
skills.py split NAME [--dry]          # SKILL.md over 150 lines -> big sections to reference/*.md
```


**Rule (the user, 2026-11-02): before working anything out, check whether a skill already covers it**
(route, INDEX.md, the game's guide). If it does, load it and follow it - don't re-derive what was
figured out before ("You already figured that out yesterday!"). What I learned before is the PRIOR:
assume it was correct and act on it, but still check it as it's used (the user: "anything you learned does
need to be checked, but you should assume you were correct prior"). If the check fails, fix the skill.

## How skills load (Claude Code)

- At the start of a session Claude sees every enabled skill's **name and description** only; the
  SKILL.md body is read when the skill is used (Skill tool), and side files only when the body
  points to them. So the description decides whether a skill gets picked: it must say what the
  skill does and "Use when ...", within 1024 characters.
- A new, imported or re-enabled skill appears in the next session (or when the skill list is
  refreshed); a disabled one stops costing context from the next session.
- Skills live in `<folder>/.claude/skills/<name>/SKILL.md`; the folder name must equal `name:`.
  Claude Code finds skills **one level deep only** (`.claude/skills/group/x/SKILL.md` is not
  found), so grouping is done with folders that have their own `.claude/skills`:
  - **Generic** skills (any game, any project): the project root's `.claude/skills/`. Loaded at
    startup.
  - **Genre** skills: `Games/<Genre>/.claude/skills/` (e.g. `Games/Wargames/`); **game** skills:
    `Games/<Genre>/<Game>/.claude/skills/` (e.g. `Games/Fantasy Strategy/Dominions 6/.claude/skills/<prefix>-guide`).
    These load the first time Claude reads or edits a file in that folder (or at once with
    `/add-dir FOLDER`, or when the session is started there). So before working on a game, read
    its folder's README.md or INDEX.md: that loads its skills.
  - User-level: `~/.claude/skills/` (every project on the machine).

## Loading what a task needs

1. `skills.py route "the task"`. The top hit is the skill to invoke. **Load order** lists what it
   builds on (its scripts import their code, or its description says "Uses ..."): those are
   loaded first **only when the work touches them**, not all at once. Matches are by words of the
   description, name and headings, so phrase the task in the user's terms.
2. Invoke the chosen skill(s) with the Skill tool, in that order.
3. Nothing matches: work without a skill, and consider making one afterwards.

"Builds on" (hard dependency) differs from "see also" (mentioned in the text): only the first
goes into the load order.

## Adding skills as they are acquired

Make a skill when Claude has built a tool or worked out a workflow that will be used again
(a script that drives the game, a file format worked out, a checked procedure), or when the user
asks. Not for one-off answers.

1. `skills.py new NAME "WHAT IT DOES. Use when ..." --uses dep1,dep2 --script tool.py [--dir FOLDER]`.
   Names: lowercase with hyphens, a game prefix for game skills (`dom6-`, `coe5-`, `se4-`, `hos-`...).
   Pick the level: generic tool → no `--dir`; one game → `--dir "<Genre>/<Game>"`; shared by a
   genre → `--dir "<Genre>"`. Scripts that need a root skill find it by walking up to the first
   `.claude/skills/<name>` (a `_skill_scripts(name)` helper that walks up the folders): never hard-code depth.
2. Fill in SKILL.md in the house style of the other skills: short intro, files, commands, a
   workflow, facts verified (with their source), gotchas and the user's rules. Move the scripts in
   (`scripts/`), and point to other skills by name instead of copying them.
3. `skills.py check NAME`, then `skills.py index`. Tell the user what was added.
4. Growing an existing skill is often better than a new one: add the section there and update
   its description (keep it under 1024 characters; `check` says).

## Importing

`skills.py import PATH`: copies a skill folder, a lone SKILL.md or a .zip (one SKILL.md inside;
paths that leave the archive are refused) into `.claude/skills/`, sets `name:` to the folder
name, prints the lint. **Imported files are untrusted**: read the SKILL.md and every script before
using it, and tell the user what it does.

## Unloading and loading

`disable NAME` moves the folder to `.claude/skills-disabled/` (nothing is deleted); `enable NAME`
moves it back. Ask before disabling skills the user did not mention. The skills manager itself
cannot be disabled. Deleting a skill: only when the user asks, and `disable` first is safer.

## Current skills

`skills.py list` (every skill with its folder), `skills.py deps` (who builds on whom), INDEX.md.
Hierarchy set up 2026-10-29 (51 skills): generic game-ui, game-sources, learn-to-play, obs-record,
skills-manager at the root; the 20 dom6-* skills in `Games/Fantasy Strategy/Dominions 6/`; one starter
`<prefix>-guide` per game (coe5, se4, efs, vgap, atg, hos, witp, toaw4, giren, pog, toc, ww1dx, starfire, sfgc, sfb, fe, thirdreich, eih, vbam, hellfire, coc, mnm, paranoia, faserip, fftow);
greyhawk-lore in `Games/Tabletop RPGs/Dungeons & Dragons/`.

## Related skills
skill-sync (inside skills: updates from generic and other games' skills, load/unload single files).

write-skill (the required format and checklist for writing one), generalize-learning (when to make a generic skill), INDEX.md, learn-to-play, learn-to-mod, user-todo
