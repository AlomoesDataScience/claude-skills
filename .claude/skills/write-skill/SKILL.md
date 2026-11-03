---
name: write-skill
description: How to write a new skill (or rewrite one) so it passes the checker and gets used - the required format (folder and name rules, frontmatter, a description of at most 1024 characters that says what the skill covers AND contains the literal phrase "Use when ..."), where it goes (generic skills in .claude/skills, game-specific ones in the game folder's .claude/skills), the house layout of SKILL.md (title, the user's rule quoted with the date, method, per-game section, Related skills), scripts (scripts/, a docstring usage, run with python3 -I, must compile), keeping SKILL.md under 500 lines, linking both ways, then skills.py check and index. Use when the user asks for a new skill, when Claude has built a reusable method or tool, when renaming or splitting a skill, or when the checker warns about a skill.
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
description: <what it covers, specific nouns and methods> ... Use when <triggers>.
---
```
**The description is what decides whether the skill gets loaded, so write it for that:**
- **At most 1024 characters.** That's an error otherwise, so aim for 400-900.
- **It must contain the literal phrase "Use when"** (or "Use whenever"). The checker searches for
  those words. "Use at the start of..." FAILS. Write "Use when starting...".
- Name concrete things: the game, the tools, script names, key terms the user uses, and his rule in a few
  words.
- The triggers come last: the situations, phrases the user might say, and the moments in a workflow.
- One line, no line breaks, and no colon-space-heavy YAML tricks (keep it plain).
- Optional: other frontmatter keys only if the harness supports them. Don't invent keys.

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
