---
name: waiting-checklist
description: Make a checklist document for work that is PARKED until something happens - the game or app is free, the user gives the go, a file or answer arrives, a machine is available - so it can start cold later without re-deriving anything. checklist.py writes it into the work's folder (<folder>/checklists/<slug>.md) from a fixed template (Status / Waits on / Go from header, a gate of conditions that must all be true, the session's safety rules, numbered items each with steps, "done when" and where results go, an After section and a dated log), lists every waiting checklist in the workspace, and sets status (waiting, ready, in-progress, done). Use when the user says he'll wait for something or do it later, when a plan's remaining items need a game, screen, file or go that isn't available now, when phase 2 of a job is blocked, and at session start (checklist.py list) to see what may now be unblocked.
---

# Waiting checklists

The user (2026-11-03, Dominions 6 phase 2 needed the game): "I'm gonna wait for that, create a checklist document,
and also create a skill for doing so."

## What it's for (and what it isn't)
- **Claude's own work that can't start yet**, written so a later session (after a context reset) can pick it up
  from the file alone. The condition might be the game being free, the user's go, a download, or hardware.
- Not the user's to-do: what HE must do goes in `Stuff You Need Me To Do/` (user-todo, `needs.py add`). Usually
  both happen - the checklist holds the work, and his document holds the one line he must act on ("tell me
  when the game is free and which one").
- Not a plan: the plan (planning) says what and why. The checklist is the parked remainder, ready to run.
  Link the two both ways.

## Commands
```
scripts/checklist.py new "Title" --dir FOLDER --waits-on "condition" [--go "the user"] [--plan PATH]
scripts/checklist.py list [--all]           # session start, next to BACKLOG.md and needs.py news
scripts/checklist.py show SLUG
scripts/checklist.py status SLUG ready|in-progress|done|waiting
```

## Writing one (after `new`, fill every section)
1. **Gate**: each condition as a box, concrete and checkable ("the user's own copy of the game is closed", not
   "game ready"). Always include: the go given for THIS session, in words; and re-reading the docstrings of the
   tools to be run.
2. **Safety**: the rules for this kind of session, copied in full (MP game = look only, End Turn rule, no shots
   during passwords, which actions need a separate go). Don't just point to memory - the file must stand alone.
3. **Start**: the exact commands to get to the first item.
4. **Items**: numbered, in order. Each has *Steps* (commands with real paths), *Done when* (a number or a
   check that can fail - "matches the Battle Summary: 34 kills"), and *Results go to* (which skill, plan and file).
   Say which steps stop the rest if they fail.
5. **After**: hand back, write the results, tick the source plan, set status done, tick BACKLOG.md.
6. Then: a BACKLOG.md line pointing at the file, the user-todo line for his part, the source plan's items marked
   as moved to the checklist, and memory if the job is ongoing.

## Using one
- At session start `list`. If a condition might now be true, ask the user (one question) - never assume the gate.
- When starting: `status ... in-progress`, tick the gate boxes one by one, then work through the items, ticking
  and writing a dated log line for each result or surprise.
- If an item fails, record what was seen, stop the items that depend on it, and say so - don't improvise around it.
- If an item turns out not to be needed, strike it with a reason; don't delete it.

## Worked example
`Games/Fantasy Strategy/Dominions 6/checklists/dominions-6-game-session.md` - battle_review boxes at 1912x1000,
map tools on the real map, the wading test (own game only), parked from dom6-finish-everything.md phase 2.

## Related skills
planning (the plan it comes from), user-todo (his side), hand-back, idle-view, delegate (acting alone),
commit-only-when-certain memory, skills-manager.
