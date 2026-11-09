---
name: unload
description: "Unload context: write a hand-off file, then clear or compact; find old context again with recall. Use when a task ends, context passes about 100k, before switching projects, or the user says unload or clear."
keywords: "safely, state, next, steps, files, read, stretch, starts, small, without, loading, games, hand, off"
---

# Unload - hand off, clear, recall

The user (2026-11-09): "make an unload skill thing". Why: context is re-sent on every request until it is cleared
(review: `Proposals/Context cost review.md`). Compaction keeps re-injecting skills loaded earlier; `/clear`
drops everything. Claude can't run `/clear` itself - the user types it.

## Unload (end of a task, or context getting big)
1. `python3 -I .claude/skills/unload/scripts/handoff.py draft` - skeleton with the skills used and the files
   changed since the last compaction.
2. Fill it in (short: task in the user's words, state, numbered next steps, files and SECTIONS to read, rules in
   force) and write it to `.claude/handoff/HANDOFF.md`. Durable facts go to their real home first (skill,
   memory, plan file, BACKLOG) - the hand-off only points to them.
3. Tell the user in one line: "Good point to clear: type `/clear` (or `/compact <focus>`)".
4. After the clear, the SessionStart hook says a hand-off exists: read it, reload only the skills the first
   next step needs, carry on. Task finished -> `handoff.py done` (moves it to Archive/sessions/handoffs/).

## Recall (old context without loading it)
`handoff.py recall WORD [WORD...] [--n 12] [--chars 240]` - short snippets from every transcript, newest
first. Read more only around a hit that matters.

## Archive (automatic)
Hooks in ~/.claude/settings.json - PreCompact and SessionEnd run `handoff.py precompact|sessionend`: the session's
transcript is copied gzip'd (screenshots stripped) to `Archive/sessions/YYYY-MM/<date>-<session8>.jsonl.gz`
(one file per session, refreshed each time) and one line goes to `Archive/sessions/INDEX.md`: time, event,
session, project, lines, file, first prompt. `cleanupPeriodDays` is 365; the archive keeps sessions after that.
`handoff.py archive-all` backfills. `recall` searches live transcripts AND archived-only ones.
Turning archived sessions into skills, memory and backlog items: chat-review (digest) -> archive-curator.

## Related skills
context-hygiene (the working rules), context-audit (measure), chat-review + archive-curator (use the archive), check-skills (light hook), planning (plan files).
