---
name: solve-once
description: "Fix problems from the source, once: read all the logic in order, check it, then test only written hypotheses drawn from specific lines, not run-and-patch loops. Use when debugging, when results look odd, or before any test run."
keywords: "debug, bug fixing, solve once, iterate, trial and error, guessing, poking around, hypothesis, test design, root cause, outcome testing, bench run, tokens, cost, sources not guesses, artifacts, odd result, why is it broken"
---

# Solve once - read the source, then test hypotheses, never patch outcomes

**Origin (the user, 2026-11-10, rule):** "The problem here is you have not, and are just fixing the outcome, which
will do nothing to fix bugs except what you find. ... doing it by checking if outcome works is extremely
expensive and inefficient, because you are testing results 1 billion times. I need you to write down a skill
why solving a problem once is better than testing and iterating on it 1000 times, and how to specifically
check everything in logic in order, then design tests around a series of hypothesises based on your
understanding derived from the specific text in the logic." And: "we rely on sources not poking around and
guessing." "The most optimal way you do things is always how we do it."

## Why once beats a thousand times

- **An outcome says something is wrong, not where.** A run of the whole program gives one number that
  thousands of lines feed. Each run narrows the place a little; a read of the lines names it.
- **Outcome testing finds only the bugs that move the number being watched.** Errors that cancel, errors in
  parts the test world does not exercise, and errors that make the number look better all stay.
- **A fix aimed at the outcome is a patch.** It changes the number without removing the cause, adds a line
  that the next reader must also understand, and can hide the real error behind a better score.
- **The cost adds up the wrong way.** A read is paid once and its notes stay. Every run is paid again in
  time and tokens, and its output is thrown away when the code changes.
- **The reading is the understanding.** After it, the user and I both know how the thing works; after a
  thousand runs we know a thousand scores.

## The method, in order

1. **Summarize all of it** (summarize-logic): every text, one at a time, in order of dependence, line by line,
   what it reads. No runs yet.
2. **Check it** (logic-check): expected result from a source, a tiny case by hand, the list. Fix what is
   plainly an error against the text's own stated intent; send design questions to the user.
3. **Write hypotheses only for what reading could not settle.** Each one in this form:
   - *Text:* file and lines, quoted or restated exactly.
   - *Reading:* what I take those lines to do.
   - *If so, then:* one thing that must be seen, with a number or a direction, stated before the run.
   - *Test:* the smallest run or probe that shows it (one place, one month, one printed value), never the
     full bench when a small case will do.
   - *Result:* seen or not seen; if not seen, the reading was wrong: back to the text, not to a second guess.
4. **One hypothesis per test, the prediction written first.** A test with no prediction is poking around.
5. **Run the full outcome check last, once,** to confirm that the fixed logic gives a sane whole, and record
   it. If the outcome is still odd, the next step is more reading at the place the hypotheses point to.
6. **Stop conditions.** A test that surprises twice means the summary is wrong there: reread. Three runs on
   one question without a new written hypothesis means stop running.

## Sources, not guesses

The order of truth holds here too: the text itself (the code as written, the paper's own words) stands above
the comment, the comment above the design note, the design note above my memory of it, and my guess last.
A guess is allowed only as a written hypothesis with its test.

## Evidence (4X engine, 2026-11)

Measured 2026-11-10 from one session's transcript (requests counted once each; input = fresh + cached
context sent; summarising for compactions not counted):

| Phase | Requests | Input tokens | Output | Bench runs | Errors found |
|---|---|---|---|---|---|
| Outcome testing (audit, probes, bench and patch) | 197 | 32.2 M | 250 k | about 85 run commands | 3 maths fixes (a839d9f) |
| File-by-file read (33 files, 8,298 lines) | 93 | 8.2 M | 298 k | none | 2 certain, 26 likely, 16 small |

- About 11 M input tokens a fixed error by outcome testing, about 0.2 M a found error by reading: some 50 times
  cheaper, and the read also produced the logic reports and 7 written hypotheses.
- Fair caveats: the first phase also built features (fixers, layoffs, migration), and the read's errors are not
  fixed or tested yet. The read compacted often (16 times) because whole files fill the context; that cost is
  not in the table.

## Related skills

summarize-logic (step 1), logic-check (step 2), context-audit (measuring what a method costs), manual-first
(the same rule in games: look it up before trying things), planning (plan before work), save-scum (cheap
repeatable tests when a test is truly needed), engine4x-dev (the 4X engine's bench and probes).
