---
name: balance-of-power-method
description: "Crawford's Balance of Power reasoning as our design method: outline every model, few quantities with named causes, pressures not scripts, judge by the record (import = stake x care). Use when designing a game system or AI commitment logic."
keywords: "balance of power, crawford, chris crawford, design reasoning, reasoning behind the rules, import, stake, care, credibility, record, bluff, finlandization, crisis ladder, coup, insurgency, power projection, contiguity, concessions, what's inside, model outline, diplomacy paradigm, honest mechanics"
---

# Balance of Power method - how we reason about rules

**Origin:** the user 2026-11-16 on Crawford's *Balance of Power* (1990 manual): "it is basically how I want us to
approach things ... Not the rules, I mean the reasoning behind the rules", "The rules are also good", and on the
proposal: "The proposal is good, for the balance of power learning. You can make that a skill." The full notes
with manual pages: `Theory/Derived/Strategy Game Theory/Strategy/Balance of Power Approach.md`. The manual text
is `Theory/Sources/Game Design Theory/Balance of Power The 1990 Edition Manual.txt`.

## The method (check a design against each)
1. **Outline every model for the player.** Say which factors are in and which are out. Leave out the exact
   numbers (honest-mechanics: no answer sheet). Our open data and code are fine (the user).
2. **Few quantities, each with two or three named causes** a player can see and argue with.
3. **Pressures, not scripts.** Behaviour comes from balancing pressures (threat, expectations, growth). The
   system resolves or collapses by itself (`design-you-are-the-universe`).
4. **The AI judges by the record.** Import = stake x care. Care comes from affinity, treaties, sphere and
   troops present. Credibility is built beforehand, and a bluff with no record reads as a bluff. When the
   record is thin, use a stated prior (doctrine, alignment) and say so in the report.
5. **No exploitable reasonableness.** The rules must not reward what would fail in the world being modelled.
6. **Indirect effects count:** deterrence without firing, treaties worth the integrity with which they are
   kept, reputation.
7. **Asymmetries come from data** (money-heavy vs manpower-heavy armies). Help is valued by need, but harm is
   resented in full.
8. **Write the concessions down.** Each system keeps a concessions list.
9. **Leave out theory that doesn't fit,** and say you did.
10. **Show the research,** with every source graded in a line (`failure-clauses-rule`).
11. **Data has a date,** and each country has its own parameters.
12. **Build in levels.** Each level adds one way things change, and the earlier ones keep running (demo first).

## Applying it (the PROPOSAL the user approved, 2026-11-16)
- Every Proposal doc gets a short **"What's inside"** section: factors in, factors out, concessions. The manual
  is written from these.
- AI commitment decisions use **import = stake x care** from the record, not a personality roll. That covers
  pockets (doc 22), diplomatic crises, code breaks (doc 20) and the battle command controller (Kursk doc §4a).
- The Kursk release demo ships each model's outline with its graded sources.
- **It is one paradigm.** the user: "the Crawford stuff is literally a paradigm. If you run the game against
  someone with a different paradigm for how to do diplomacy, then you fail." So in the engine it is one
  diplomacy paradigm among several (`Theory/Derived/the user/Paradigms.md`).

## Status / open
- **When:** the user 2026-11-16: "crawford's work is a good starting point for the agent rework. For now, we're doing
  systems, we'll pass them all to agents after we finish part 3 ... Agents are passed to part 4." So in Part 3,
  use the method on systems and their What's inside sections. Agent decision logic (import = stake x care) is
  Part 4 work, and Part 3 code uses simple stand-in rules where an agent will decide later.
- **Open, with the user:** how we handle diplomacy and power projection in detail (the user 2026-11-16: "We gotta go
  through and state how we want to handle the diplomacy power projection stuff in detail"). Crawford's rules
  to start from are projection by contiguity, Finlandization and the crisis ladder, in the notes file.
- Fails when: the outline is so vague the player can't predict anything, or so exact it is an answer sheet.

## Related skills
engine4x-design (where it is applied), borrow-from-games (the parts bin), own-theories (claims and tests),
war-concepts (deterrence, escalation), combat-models (the numbers behind military power).
