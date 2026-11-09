---
name: write-skill
description: "How to write or rewrite a skill so it passes the checker and gets used: format, budgets, keywords, layout, where it goes. Use when making a new skill or rewriting one."
keywords: "required, folder, name, rules, frontmatter, description, most, characters, says, covers, contains, literal, phrase, generic, skills, game-specific, ones, game, folder's, house, title, rule, quoted, date, method, per-game, section, related, scripts, docstring, usage, run, python3, must, compile, keeping, under, lines, linking, check, index, has, built, reusable, tool"
---

# Write a skill - the required format

The user (2026-11-02): "make a skill for making a skill that includes all the required formatting, like
use when." This is the checklist. skills-manager has the tools (`skills.py new | check | index`).

## 1. Decide where it goes
- **Generic** (a method useful in any game or task): `.claude/skills/<name>/` at the workspace root.
- **Game-specific** (coordinates, keys, unit stats, rules of one game): the game folder's
  `.claude/skills/<game>-<topic>/`, e.g. `fog2m-scouting`.
- Both, when a game teaches a generic method. The generic skill holds the method, and the game skill
  holds the facts and links back (generalize-learning).
- **Check first** that no existing skill covers it (`skills.py route "<task>"`, INDEX.md). Extend one
  rather than duplicate it.

## 2. Folder and name
- The folder name equals `name:` in the frontmatter.
- Lowercase letters, digits and hyphens only, max 64 characters, starting with a letter or digit.
- Game skills take a game prefix (`fog2m-`, `dom6-`, `se4-`).

## 3. Frontmatter (must be exactly this shape, at the very top)
```
---
name: <folder-name>
description: "<what it covers, specific nouns and tools>. Use when <short triggers>."
keywords: "<trigger words, terms the user uses, game names, script names, comma-separated>"
---
```
Budgets (context cost review, 2026-11-09 - the listing is re-sent nearly every turn):
- **description: at most 40 words**, in double quotes (a `: ` inside plain YAML breaks the file). What it is
  + a "Use when ..." clause (the checker also accepts Use whenever/at/for/before/after). It is what Claude
  Code shows in the skill listing.
- **keywords:** everything else that should route a task here (terms, phrases the user says, tools, games).
  Not shown in the listing; checkskills.py, `skills.py route` and INDEX.md read it.
- Add or change a task row in `skills-manager/routes.md` when the skill belongs to a common task, then
  `skills.py index`. Test routing: `skills-manager/tests/routetest.py` (add a case for the new skill).
- No other frontmatter keys.

## 4. Body layout (house style)
1. `# <Title> - <what it's for in a few words>`
2. **Origin:** the user's words, quoted, with the date. If they're a rule, mark it as one.
3. **The method:** numbered steps or short sections, imperative voice, concrete. Say what to check
   and when to stop.
4. **Per game** (in generic skills): a short note per game, with the game skill named.
5. **Status / open hypotheses** where something is untested (order of truth: game > manual >
   hypothesis).
6. `## Related skills`: names with a few words each, and the link added in BOTH directions.
- **Under 500 lines** (the checker warns over that). Move detail into side files in the folder
  (COMMANDS.md, UNITS.md) and link them from SKILL.md.
- In my own words: no pasted wiki text, and purchased manuals stay local (cite the pages).
- No secrets, and none of the user's NSFW games, anywhere.

## 5. Scripts
- Put them in `<skill>/scripts/`, each with a module docstring that gives usage (the `__doc__` is
  printed with no args).
- Run them as `python3 -I <path>`. They must compile, since the checker byte-compiles them.
- Read inputs as untrusted. Never touch End Turn, installs, the user's settings or saves.
- **Run with no arguments = print the usage and exit.** A script that drives a game must never act with
  zero arguments (2026-11-03: panorama.py run "to see its help" held FoG keys in the user's Dominions game;
  harmless that time). To read a script's usage, read its docstring (`ast.get_docstring`), don't run it.
- Refer to them from SKILL.md by relative path (scripts/NAME.py).

## 6. Finish
```
python3 -I .claude/skills/skills-manager/scripts/skills.py check    # fix every error and warning
python3 -I .claude/skills/skills-manager/scripts/skills.py index    # rebuild INDEX.md
```
- Add the new skill to the Related skills of the skills that should lead to it.
- If it changes how I work in general, add or adjust the memory pointer (MEMORY.md, one line).
- If it should go public: the claude-skills export (skills only, the user's name stripped, push only
  with the user's OK).
- Tell the user the skill's name and the one-line gist.

## Related skills
skills-manager (new/check/index/route/import), generalize-learning (what goes generic vs game),
learn-to-play / learn-to-mod (where most game skills come from), planning.
