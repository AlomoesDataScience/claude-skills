---
name: logic-check
description: "Sanity check code or a paper against the result it should give: units, signs, both sides of a transfer, bounds, indices, order, copied lines, limit cases. Use after summarize-logic, when bug checking or reviewing an argument."
keywords: "check, logic check, sanity check, bug check, math typo, broken math, review a paper, check the logic, proof check, audit, units, sign error, off by one, double counting, expected result, code review, math bug"
---

# Logic check - does each step give the result it is meant to give

**Origin (the user, 2026-11-10, rule):** "Second, you need to go through and sanity check it. Sanity checking is a
tool to make sure it gets the expected result." And: "Check for math typos ... broken math logic." "If there's
any artifacts, it's likely a math bug. Or code bug."

Step 2 of three. Step 1 is the line-by-line summary (summarize-logic); without it there is nothing to check
against. Step 3 is the few tests the check could not settle (solve-once).

## The method

1. **State the expected result first, from a source.** For each block of the summary, write what it is meant
   to do: from the comment above it, the design document, the user's words, or the paper's own claim. If no
   source says what is meant, that is a finding ("intent not stated"), not a guess to fill in.
2. **Work a tiny case by hand.** Pick the smallest numbers that exercise the block (one place, two goods,
   round figures), run the formula as written on paper, and compare with the expected result. Most math typos
   show here.
3. **Go down the list below for every formula and every transfer.** In order, each line, no skipping.
4. **Write each finding** with: line, what the text does, what was expected and from which source, the
   hand-worked case that shows the gap, and how sure (certain typo / likely error / question for the user).
5. **Sort findings into three piles:** plain errors (the text contradicts its own stated intent: fix),
   design questions (the text does what it says but the result is doubtful: to the user), and things only a run
   can settle (to solve-once as a written hypothesis).

## The list (code and maths)

- **Units.** Both sides of every `=`, `+`, comparison and `min/max` in the same unit. Typical breaks: a
  monthly flow added to a yearly one, a stock compared with a flow, a share multiplied where a count is
  wanted, money per unit against money in total, people against crews.
- **Sign and direction.** Who pays and who receives; `+=` against `-=`; a cost entered as a gain; a
  comparison turned round (`<` for `>`); `min` where `max` is meant (a floor written as a ceiling).
- **Both sides of a transfer.** Everything taken from one place is given to another, same amount, same
  month. One-sided lines create or destroy money, goods or people.
- **Counted once.** Not applied twice (in two functions, or inside and outside a loop), not left out of one
  of two totals that should match, not divided among a different set than it is summed over.
- **Bounds.** Division by a value that can be zero; a clamp whose ends are wrong or swapped; a value that can
  go negative and is then multiplied or rooted; a share that can pass 1.
- **Indices.** The right array with the right index (good, recipe, place, owner are all plain integers and
  swap silently); loop ends; first and last element; an index kept after the list was changed.
- **Order and freshness.** A value read before it is updated this turn or after; an average mixed with
  today's figure; a total computed, then the parts changed, then the total used.
- **Copied lines.** Neighbouring lines that should differ in one symbol and differ in none or two.
- **Comment against code.** The comment states the intent; when the two differ, one of them is wrong.
- **Constants.** The same figure written in two places with different values; a figure with no stated source;
  a rate applied per month that was given per year.
- **Limit cases.** Zero, one, and very large: nothing owned, no workers, empty stock, the only place in a
  system, the first month.
- **Reach.** Who else reads the value this block sets, and does it still mean the same thing to them.

## The list (a paper or argument)

- Terms defined before use, and used with one meaning throughout.
- Each premise stated; hidden ones written out.
- Each step follows from the ones before it and not from the conclusion.
- Every number recomputed from the paper's own figures; tables add up; percentages have a stated base.
- Cited sources say what the paper says they say (check the source, order of truth).
- The conclusion claims no more than the steps showed; cases and counter-examples it leaves out are named.

## What this is not

Running the whole program and looking at the outcome is not a logic check. An outcome can be right with two
errors that cancel and wrong with none (the design itself may give that result). See solve-once.

## Related skills

summarize-logic (step 1), solve-once (step 3 and the reason for the order), dice-math and unit-combat-math
(hand-worked odds for game formulas), doc-standards (report layout), engine4x-dev (the 4X engine's build and
checks).
