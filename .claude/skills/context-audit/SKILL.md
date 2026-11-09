---
name: context-audit
description: "Measure where Claude Code's context and usage go from the session transcripts (ctxaudit.py): requests, context size, compactions, tokens by source. Use when usage runs high or before and after a context-saving change."
keywords: "average, peak, processed, entered, tool, draining"
---

# Context audit

The user (2026-11-09): "we're burning too much usage" - review in `Proposals/Context cost review.md`.

`python3 -I .claude/skills/context-audit/scripts/ctxaudit.py [FILE.jsonl ...] [--top 12]`
(no files = every transcript in ~/.claude/projects). Output stays short: one line per session, then the
source and tool tables.

## Reading it
- Cost ≈ tokens that entered x requests that re-sent them before the next compaction. Watch **avg ctx**
  (shorter stretches) and **req** (fewer, batched calls) first, then the source table (less going in).
- Content tokens are estimates (chars / 4; images w*h/750, capped at about 1,600). Request totals are exact
  (from the API usage in the transcript).
- Baseline 2026-11-09: 19,227 requests, 4.54 B input tokens, avg context ~240k, peak 368k (window 400k);
  Bash output 27%, tool inputs 21%, screenshots 17%.

## Related skills
check-skills (its hook adds to every message), game-ui (screenshot sizes), skills-manager (description sweep).
