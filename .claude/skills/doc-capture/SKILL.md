---
name: doc-capture
description: "Write the user's design words into the project's design doc the same turn he says them: verbatim quote, meaning, built-vs-documented status, never overwriting older text. Use whenever the user answers a question, decides, corrects or states a design rule."
keywords: "document everything, documentation, capture, design decision, the user's answer, the user's words, verbatim, project doc, design doc, built vs documented, status, supersedes, stale docs, compaction forgets, Kursk doc, Build Proposal"
---

# Doc capture - the user's words into the doc, the same turn

Status: active. Origin, the user 2026-11-17 (rule): "You need to create a skill to properly document everything so
compaction doesn't kill your brains and you forget." Also: "Documentation will save us." and "Just document
everything." What went wrong: his design answers lived only in the chat, compaction dropped them, and the code
was built against my own reading.

## When
Every time the user answers a question, makes a decision, corrects me, or says how something should look or
behave. That includes a one-line aside typed mid-turn. Write it **before** going on with other work in that
turn.

## The method
1. **Find the doc.** Use the project's design doc for that topic (4X engine tactical: `Build Proposal/battles/
   <battle>.md`; economy: its proposal doc; elsewhere the project's README or design folder). No doc exists ->
   ask where, or use the project's open plan file.
2. **Quote.** the user's words verbatim with the date (and time if it helps), typos and all.
3. **Means:** one or two lines of my reading. Unclear -> write `OPEN:` with the question, and ask him.
4. **Status line:** `built` (file:line) / `partly built` (what is missing) / `documented only` /
   `OPEN`. Check the code before writing "built".
5. **Never overwrite.** When it supersedes older text, mark the old text "superseded by <section>, <date>".
   Don't delete or rewrite it. Old vs new docs: neither overwrites the other; the user rules which wins
   (2026-11-17: "We have literally no idea what's stale and what's not." / "Same with the other way around.").
6. **My additions** are marked PROPOSAL with a "Fails when" (failure-clauses rule).
7. **Review copy.** Re-copy the doc to `Review/` (review-folder rule).
8. **Build from the doc.** Before writing code for a design point, re-read its section. The doc is the spec,
   not my memory of the chat.

## Fails when
- The doc grows past what can be read in a section: split it per doc-standards, with links, not rewrites.
- The user's words contradict each other on different days: record both with dates and ask; don't pick one.

## Per project
- 4X engine, Kursk tactical: `Build Proposal/battles/Kursk 1943.md`, section "the user's answers on drawing,
  2026-11-17" (engine4x-design, engine4x-dev).

## Related skills
compaction-review (finds words that never made it in), doc-standards (labels, one fact one place), planning,
own-theories (claims and Fails-when), user-todo (what only the user can decide), abc-notation (the user's music theory lessons).
