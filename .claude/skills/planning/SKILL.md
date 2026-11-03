---
name: planning
description: Make a detailed plan before any non-trivial work, SAVE it as a file, and USE it - re-read it whenever it should be referenced (start of a session, before each step, before a decision, when something goes off-plan, when the user asks what's next), tick steps as they're done and record changes with the reason. Generic, not tied to tactics or any game (the user, 2026-11-02). plan.py creates a plan from the template next to the work (plans/ folder), lists open plans across the workspace and shows one. Use when starting a task with more than a few steps, a game session, a battle, a build, a research or sorting job, when resuming work, or when the user says "make a plan", "what's the plan" or "stick to the plan".
---

# Planning - make it, save it, use it

The user's rule (2026-11-02): make a **detailed** plan, **save** it, and **use it when it should be
referenced**. A plan that only lives in the chat is lost at the next context reset; a plan that is
never re-read is decoration. (Battle tactics have their own skill; this is about plans in general.)

## When to make one
Any task with more than a few steps, anything that spans sessions, anything with a goal that can
be missed by drifting (a game battle, a build, a mod, a sort, research). Not for one-liners.

## Make it (detailed)
`scripts/plan.py new "<title>" --dir <folder of the work>` -> `<folder>/plans/<slug>.md` from the
template. Fill every section:
- **Goal** - what done looks like, checkable.
- **Context** - facts the plan rests on (rules, constraints, the user's instructions, verbatim if short).
- **Steps** - numbered, each concrete enough to act on and to check: `- [ ] 1. ... -> check: ...`.
- **Decisions** - choices made and why (so they aren't re-argued).
- **Risks / watch for** - what could go wrong, what would make the plan wrong.
- **References** - when to re-read this plan (the triggers below plus task-specific ones).
- **Status / changes log** - dated lines: done, changed, why.
Show the user the plan when it affects him; his edits win.

## Use it
Re-read the plan file (not memory of it):
- at the **start of every session** or after a context summary;
- **before each step**, and before any decision the plan covers;
- when something **goes off-plan** - then either get back on it or change the plan *in the file*
  with the reason, never silently;
- when the user asks what's next / what the plan is.
Tick steps `[x]` as they finish, with the check result. Finished plan -> Status "done" + a line of
lessons; keep the file.

## Find plans
`plan.py list` - open plans across the workspace (status not done), newest first.
`plan.py show <path|slug>` - print one. Mention open plans at session start with the BACKLOG.

## Related skills
battle-tactics (battle plans), learn-to-play (a plan before play), user-todo (what the user must decide), skills-manager
