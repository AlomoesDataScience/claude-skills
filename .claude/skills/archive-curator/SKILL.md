---
name: archive-curator
description: "Turn archived Claude Code sessions into lasting knowledge (skill edits, new skills, memory, BACKLOG, plans) and track which sessions are done with curate.py. Use when curating the session archive or after a chat review."
keywords: "archive, archived sessions, curate, curation, ledger, proposals, split info, knowledge, manage archived information, transcripts, old chats, backlog items, memory, skill edits, garbage, retrieval"
---

# Archive curator - from old sessions to the right files

The user's proposal (2026-11-09): "A skill to manage archived information and split it into proper info for
further use elsewhere." The archive (unload skill: `Archive/sessions/`) holds every transcript; this skill
moves what matters out of it into the files that get used, once per session.

## Tools (`scripts/curate.py`)
```
curate.py status                    each session: digest? proposals? curated?
curate.py next                      oldest session not curated
curate.py propose SESSION           Archive/sessions/proposals/<id>.md - candidate lessons + suggested home
curate.py mark SESSION "NOTE"       ledger line in Archive/sessions/CURATED.md
```

## Routine (one session at a time, oldest first)
1. `curate.py next`, then `propose` (it makes the chat-review digest too).
2. Read the proposals file and the digest around each timestamp (sections only). The suggested homes are
   the matcher's guess - most lines are chatter; keep only real rules, decisions, facts and open work.
3. Where each kind goes (one fact in one place - doc-standards):
   | Kind | Home |
   |---|---|
   | Method or rule for a game / tool | that skill's SKILL.md or reference file (dated, the user's words) |
   | Method seen in 2+ games | generic skill (generalize-learning) |
   | Fact about the user, standing preference | memory file + MEMORY.md line |
   | Open work | BACKLOG.md, a plan file, or a waiting checklist |
   | A real decision with reasons | decision record (doc-standards `docs.py adr`) |
4. Tick applied lines, strike rejected ones, `curate.py mark SESSION "what went where"`.
5. Digests and proposals stay in the archive (searchable); nothing is deleted.

## Rules
- Propose, check, then apply - never copy a whole transcript or digest into a skill or memory.
- Session already summarised in a skill or memory? Mark it with that note and move on.

## Related skills
chat-review (digests, lessons), unload (archive, recall), doc-standards, skills-manager, write-skill, user-todo.
