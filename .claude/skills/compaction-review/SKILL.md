---
name: compaction-review
description: "Review right after a context compaction or summary: reload skills, re-read plans and the project doc, read the user's own words (ryanwords.py, queued messages too), fix gaps, then act. Use when a session resumes from a summary."
keywords: "compaction, compacted, compact, summary, session continued, resume, context reset, lost context, forgot, let's review, ah compaction, post-compaction, ryanwords, queued messages, mid-turn messages"
---

# Compaction review - "ah compaction, let's review"

Status: active. Origin, the user 2026-11-17 (rule): "You also need a skill to say ah compaction, let's review."
Same day: "Yeah it's compaction. We already built this out. Your documentation for kursk is lacking".
What went wrong: after a compaction I acted on the summary alone. Design decisions were lost, I rebuilt code
that already existed, and I trashed a file.

## When
The first thing after "This session is being continued from a previous conversation", or a SessionStart hook
saying the source is compact/clear. Do it **before** any other tool call that changes something.

## The method
0. **Read what the hook re-injected** (2026-11-24): after a compaction the SessionStart hook (checkskills.py
   `after_compact`) adds the user's own words this session, verbatim, and `.claude/handoff/WORKING.md` (the task and
   the documents it depends on). His words win over the summary. A gap in my memory is not an error: check the
   transcript and the WORKING.md documents before raising any doubt (the user: "Chill, you're hallucinating or
   forgetting things."). **Keep WORKING.md current** whenever the task or its document set changes, before a
   compaction can hit.
1. **Say it.** One line to the user: "Compaction - reviewing before I act."
2. **Skills.** None count as loaded. Load every skill the pending work needs (check-skills), including the
   project's folder skills (Read their SKILL.md).
3. **The user's own words** since the last summary, or the whole day if unsure:
   `python3 -I .claude/skills/compaction-review/scripts/ryanwords.py SESSION --since HH:MM`.
   The session id is in the summary's transcript path. This reads queued messages too ([q]): what he typed
   while I was working is NOT stored as a user message, and a type == "user" filter misses it.
   The summary is in my words; his words win where they differ.
4. **Plans and docs.** Read the WHOLE hand-off (`.claude/handoff/HANDOFF.md`, every line) and WORKING.md
   first: their task is the task, not my reading of a phrase of the user's. Then the open plan file (planning,
   `plan.py list`) and the project doc sections for the pending work. The user 2026-11-24, after I misread "writing
   up the final shit for the demo" without the hand-off: "Did you not read the hand off?" / "you gotta make sure
   your skill causes you to do everything correct."
5. **Gap check.** For each design word or rule of the user's from step 3: is it in the project doc? Missing ->
   write it in now (doc-capture). Is it a general rule? -> memory or skill.
6. **State check.** Git branch and uncommitted work (never on main without his review), background tasks
   still running, what is half-done.
7. **Report.** A few lines to the user: what is pending, what the summary got wrong or left out, what I'm doing
   next. Then carry on. If he said "hold" or "stop" just before the compaction, wait for him.

Keep it cheap: read sections, not whole files. Cap ryanwords output with `--chars`.

## Fails when
- The transcript was cut or rotated: ryanwords finds nothing new. Then search the archive
  (`handoff.py recall WORD`) and say the review is partial.
- The decisions were never written down anywhere. This review can't recover what was only in my head, so
  doc-capture is what prevents it.

## Related skills
doc-capture (writes the user's words into the doc the same turn), check-skills (reload), planning (plan files),
unload (hand-off before a clear), chat-review (digests of old sessions; its `lessons` view misses queued
messages), archive-curator.
