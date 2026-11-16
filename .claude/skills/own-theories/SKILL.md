---
name: own-theories
description: "Build our own theories from everything we pull: claims notes while reading, theory files with evidence for and against, a test, and the user's ruling. Use when reading theory, manuals, wikis or game data and a claim is worth keeping."
keywords: "theory, theories, own theories, derived theory, claims, claims notes, hypothesis, evidence, Theory/Derived, Theory/Sources, scrub, synthesis, make our own theories, agents and markets, eras of space war, collapse of empires"
---

# Own theories - turn what we pull into tested theories of our own

**Origin:** the user (2026-11-15): "Part of the idea is to scrub through all the stuff we pull and make our own
theories. That should be a proposal/project." And: "sort sources from derived theory." The folder layout is
in `Theory/README.md`: sources live in `Theory/Sources/`, our work in `Theory/Derived/`.

## 1. Claims notes (while reading anything)
Use this for theory texts, manuals, wikis, game data, Star Wars Combine and Code Sources. When a claim is
worth keeping, add a line to `Theory/Derived/notes/<topic>.md`:
```
- <the claim, in my own words> | <source, with page or file:line> | <shown in: game/engine/none> | <date>
```
Keep it to one line per claim, with no pasted text. Note a clash with another claim next to that claim.

## 2. Theory files
When three or more claims from different sources agree or clash, write `Theory/Derived/<theory>.md` with these parts:
- **Claim**: one sentence.
- **For**: the claims that support it, each with its source.
- **Against**: the claims that cut against it, and the cases where it fails.
- **Fails when** (required, the user's rule 2026-11-16): the conditions under which the theory gives the wrong
  answer, and what observation would show it. A theory with no failure clause is not finished. "If a formula
  or theory is good enough it has failure cases": a theory that claims none hasn't been tested, it isn't perfect.
- **Test**: where the theory is tested. That can be a game, the 4X engine Bench, combat.py or dice.py.
- **Status**: hypothesis, tested (with the result and date), or rejected. **Adopted** only with the user's yes.
Use the order of truth: what a game shows beats a manual, and a manual beats a hypothesis.
How much to trust a source or a witness: `Theory/Derived/How We Know.md` (grades, testimony by default, scrutiny scales with stakes).

## 2b. Critique every source, ours included
The user (2026-11-16): "There's a lot of bad sources... we have to critique everything, including our own theory."
- Grade each source when it is first cited: who wrote it, when, for what purpose, what it can't see (a 1917
  training pamphlet, a JSTOR theory paper, a book summary and a fan wiki are not equal).
- Note a source's known failures next to its claims (a prediction it got wrong, a war it misread).
- Our own theories get the same treatment: World Flow and the layer claims are hypotheses with failure clauses.
- **Wrong is usually a mistake** (the user, 2026-11-16): "90% of the time, nobody is lying, however they can be
  wrong just because of a mistake. Even if they're wrong intentionally, it will look like a mistake most of the
  time, and can be handled as such." So a wrong claim is handled as an error: check it against the order of
  truth and other sources, record the correction, keep the rest of the source. Don't grade on guessed motives.

## 3. Tests
Each theory names a test the engine or a game can run. The worked example is the user's land salvo system
(`Theory/Derived/the user/Salvo Combat System for Land Battles`, prototyped as `combat.py land`; combat-models).

## 4. The user rules
Claude drafts and the user judges. List each theory in the Theories section of `Theory/README.md` with its status.

## Related skills
economic-theory, military-doctrine, war-concepts (the source shelves), combat-models (worked test),
engine4x-economy (the agents and markets test bed), wiki-scout and game-sources (where claims come from),
logic-check (check a theory's argument).
