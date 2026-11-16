---
name: summarize-logic
description: "Write down what a text actually says, line by line and in order (code, a paper, a rules document), before judging or changing it. Use when asked to summarize, explain how something works, or before any bug or logic check."
keywords: "summarize, summary, summarise, line by line, what it reads, how does this work, explain the code, logic report, read the file, understand, walkthrough, code read, paper summary, restate"
---

# Summarize logic - what the text reads, not what I think it does

**Origin (the user, 2026-11-10, rule):** "You want to first summarize the entire logic of whatever you are bug
checking. Not what you think it is, but line by line, what it reads." And: "Go read each code and inspect one
file at a time ... summarize the logic in a report. I will check it. I need to understand how everything works
here."

The summary is step 1 of three: summarize (this skill), check it (logic-check), then test only what the
reading raised (solve-once). It is also a product in itself: The user reads it to learn how the thing works and to
check my reading.

## The method

1. **One text at a time, whole, in order.** One file, one chapter, one section. Read all of it before writing.
   Do not skip a part because its name says what it does.
2. **Order the texts by dependence.** Definitions and data first, then what uses them (for code: data
   definitions, the model, the main loop, then each step in the order the loop calls it).
3. **Restate each block in plain words, with its line numbers.** A block is a function, a loop, a formula or
   a paragraph that does one thing. For each one write:
   - what goes in (which values, and where they were set),
   - what it does, with the formula written out exactly as the text has it (same operators, same order,
     same constants),
   - what comes out or is changed (which values, who reads them next).
4. **Write what is there.** If the comment says one thing and the code another, write both. If a name
   promises something the body does not do, write what the body does. Never fill a gap from memory of an
   earlier version or from what would be sensible.
5. **Give every quantity its unit and kind** the first time it appears: stock or flow, per month or per year,
   money, goods, people, a share from 0 to 1. Units are what the check works with later.
6. **Mark, do not fix.** Anything odd gets a mark in the summary (`[?]` with the line number and one sentence)
   and goes on a findings list. No edits during the read.
7. **Keep a ledger of loose ends:** values that are set and never read, read and never set, constants
   repeated in two places, the same thing computed twice in different ways.
8. **Stop when** every line of the text is covered by a block in the summary, and a reader who has not seen
   the text could say what happens in what order.

## Shape of the report (one per text)

```
# <file or section> - <what it is for, one line>
Read: <date>, <lines read> of <lines>.   Called by: ...   Calls: ...
## What it holds / does, in order
<line range>  <name>  - in: ... / does: ... (formula as written) / out: ...
## Quantities and units
## Findings (marks from the read, each with line, what the text says, why it looks wrong)
## Loose ends
```

Plain language, the user's terms. Formulas in the text's own symbols so he can find them. No verdict on outcomes
here: a summary says what the text does, the check says whether that is right.

## Mistakes this prevents

- Describing the design I remember instead of the code that exists (they drift apart after every patch).
- Checking only the parts I suspect, so the bug in the part I trusted stays.
- Changing a line before knowing who else reads the value it sets.

## Related skills

logic-check (step 2: sanity check the summary against the expected result), solve-once (why this order, and
how to design the few tests that remain), doc-standards (where the report goes and how it is laid out),
manual-first and game-sources (the same rule for games: the source text before guesses), engine4x-economy
(the 4X engine's own logic notes).
