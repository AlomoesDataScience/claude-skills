---
name: check-skills
description: Before acting on ANY request, check which skills are relevant and load them all (the user, 2026-11-03 - "make a skill that tells you to check relevant skills, and set it to auto load"; it auto-loads through a UserPromptSubmit + SessionStart hook in ~/.claude/settings.json that runs checkskills.py and names the likely matches). Covers the generic method skills AND the game/topic skills AND what they build on, game-folder skills that aren't in the list yet (Read their SKILL.md), re-checking whenever the task changes (a new game, a battle, End Turn, a new kind of screen), and saying which skills were loaded. Use when starting any task or reading a new message, when the user says "load the skills", or when unsure whether a skill exists for something.
---

# Check skills - load everything relevant before acting

The user, 2026-11-03, playing Pythium: "just remember to check everything and load all the skills" ... "you
probably want to load all the other relevant skills" ... "make a skill that yah know, tells you to check
relevant skills, and set it to auto load." What went wrong that day: I wrote the manual's battle orders into
dom6-tactics while **dom6-battle-ai already had them** - I never knew it existed. Skills only help if loaded.

## Auto-load (the hook)
`~/.claude/settings.json` runs `scripts/checkskills.py hook` on every message (UserPromptSubmit) and at session
start. It injects this rule plus the likely matches for the message's words. The matches are a **hint** - the
check below is the job. (`/hooks` shows or disables it.)

## The check - every new task or message that changes the task
1. **Name the task's parts**: the game or topic, the kind of work (play a turn, fight a battle, mod, draw,
   research, write a skill), the tools it touches (virtual screen, OCR, maps, recording).
2. **Find the skills**:
   - the hook's list, or `python3 -I .claude/skills/check-skills/scripts/checkskills.py "TASK" --n 12` (fast);
   - `skills-manager/scripts/skills.py route "TASK"` (slower, gives the load order of what each builds on);
   - the game folder's own `.claude/skills/INDEX.md` - game skills are NOT in the session list until a file in
     that folder is read; if the Skill tool says "Unknown skill", Read its SKILL.md directly.
3. **Load them all** with the Skill tool, in one batch: generic methods (MEMORY.md names many: learn-to-play,
   manual-first, planning, battle-tactics, war-language, army-log, move-phases, photo-map, idle-view,
   hand-back, loading-screens...) + the game's skills (guide, ui, map, tactics, army-check, battle view...) +
   whatever they list under "Related skills" that the task touches.
4. **Say which were loaded** in one line, so the user can spot a missing one.
5. **Re-check when the task shifts**: a battle starts, End Turn comes up, a new screen or game appears,
   the user adds a request mid-turn. Loaded skills stay loaded until a compaction; after one, load again.
6. **Found a gap?** A rule that has no skill yet - write it (write-skill, skills-manager) and index it.

## Per task (starting lists - extend them)
| Task | Load |
|---|---|
| Dominions turn | dom6-game, dom6-ui, dom6-army-check, dom6-tactics, dom6-battle-ai, dom6-map, dom6-play, dom6-battle-view, war-language, army-log, military-doctrine, loading-screens, idle-view, hand-back |
| FoG II battle | fog2m-guide, fog2m-map, fog2m-scouting, battle-tactics, move-phases, photo-map, war-language, army-log, screening, idle-view, hand-back |
| New game | learn-to-play, manual-first, game-sources, game-setup, game-ui, wiki-scout |
| Sprites / mods | the game's sprite and modding skills, art-direction memory, mod-docs |
| Skills work | skills-manager, write-skill, skill-sync, generalize-learning |

## Related skills
skills-manager (route, index, check), write-skill, generalize-learning, skill-sync.
