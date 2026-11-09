---
name: chat-review
description: "Review past Claude Code sessions without loading raw transcripts: chatreview.py makes a short digest, then summarise it or mine it for lessons and new skills. Use when reviewing an old chat or turning it into skills."
keywords: "past chat, old session, conversation history, transcript, jsonl, digest, summarise, summary, summarization, review, lessons, mining, skill building, what did we do, last time, archived sessions, context understanding"
---

# Chat review - digest, then summarise or mine

The user's proposal (2026-11-09, `Proposals/Skills for reducing context cost overhead`): "A review skill, split into
review for past chat context understanding and summarization, and review for building new skills."
Raw transcripts are megabytes (screenshots, tool dumps, thinking); a digest is ~1-2% of that.

## Tools (`scripts/chatreview.py`, from the workspace root: `python3 -I .claude/skills/chat-review/scripts/chatreview.py`)
```
chatreview.py list [--n 20]               sessions, live + archived, digest yes/no, first prompt
chatreview.py digest SESSION              -> Archive/sessions/digests/<date>-<id>.md (prints size)
chatreview.py lessons SESSION [--n 40]    the user's rule-like lines and corrections, timestamped
```
SESSION is the 8-character id from `list` or Archive/sessions/INDEX.md. Archived copies (gzip) work too.

## Mode 1 - understand and summarise a past chat
1. `digest`, then read the digest **in sections** (Read with offset/limit; grep `^### ` for the turn list).
   Compaction summaries inside it are already dense - read those first.
2. Write 5-15 lines into its `## Summary` section: goal, what was done (files, skills), decisions with the user's
   words, what was left open. Set `Status: reviewed` at the top.
3. Open items go to their real home (BACKLOG.md, a plan file, a waiting checklist) - not memory.

## Mode 2 - mine it for skills and rules
1. `lessons SESSION` - candidate rules and corrections. Confirm each in the digest around its timestamp.
2. For each real lesson: does a skill already cover it? (`checkskills.py "<lesson>"`, INDEX.md). Then it is
   an edit to that skill; a method used in 2+ games is a generic skill (generalize-learning); a fact about
   the user or a standing rule is memory.
3. Hand the list to archive-curator (proposals file) so the session is marked curated and nothing is done twice.

## Rules
- Never Read a raw .jsonl or .jsonl.gz whole. Digest first; `handoff.py recall WORDS` for one fact.
- The user's words are quoted exactly; dates kept.

## Related skills
archive-curator (where findings go, tracking), unload (archive + recall), write-skill, generalize-learning, context-hygiene.
