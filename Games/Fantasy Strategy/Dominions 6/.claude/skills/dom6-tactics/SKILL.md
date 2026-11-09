---
name: dom6-tactics
description: "Laying out a Dominions 6 army for battle and what has worked: positions, formations, squad and commander orders, leadership, lessons. Use when setting up or changing an army, picking battle orders, or after a battle."
keywords: "lay, position, placement, morale, limits, colour, legend, setup, destination, armies, meet, province, plus, log, fought, result, drawn, dom6-ui, input, dom6-game, click, adding, squads, mercenaries, planning, record, did"
---

# Dom6 tactics

Battles in Dominions 6 are not controlled live: the army fights from its **setup** (where each
squad and commander starts, in what formation) and its **battle orders**. This skill holds the
rules for that setup, the layouts that are known to work, and a log of every battle with what the
setup did, so the layouts get better with each fight. It is a living file: add to the battle log
and the lessons after every battle (the user asked for this, 2026-10-28).

Click positions and the screens themselves are in **dom6-game** (sections "Army Setup",
"Battle orders", "Position Army", "Turn-5 lessons"). Input goes through **dom6-ui**'s guard.
Strategy (what to attack) is in dom6-knowledge `play/strategy.md`; formulas in dom6-mechanics.

## Workflow: every time an army changes

1. **Army Setup** (`t` in the province, or **`y` = Army setup at destination**, which shows
   every army that will be in the target province next turn: use it when two commanders attack
   together). Put units into squads: select (alt+click or double-click = all of that type,
   shift+click = several), then click the **commander's portrait** for a new squad or an
   existing **squad strip** to add to it. Enter deselects.
2. **Orders** for each commander and squad (the order word or `<set battle orders>` bar).
3. **Position Army** (left-click a squad's or a commander's small green box). Lay out *every*
   squad and every commander. New squads and mercenaries land stacked on one default spot
   (the user caught this, turn 6).
4. Check the result on the small green boxes in Army Setup (they are mini-maps), then Exit.
5. After the battle: review it with **dom6-battle-view**, read the report, and **add a row
   to the battle log** with the setup and what happened. Turn a repeated result into a lesson.

## Layout rules

From the user:
- **Commanders centred** on the army's line, behind the troops, not off to one side (turn 6).
- **Scouts**: Retreat order and the far rear (left edge), so they escape at once.
- Every squad positioned after any change (above).

From the manual (pp. 43-46, 57-60) and reasoning, to test:
- The whole army routs when **all its commanders are dead or routed**, or when it has lost 75%
  of its hit points. So commanders stay behind and centred, out of missile lines.
- Units halt in an enemy's **zone of control** when adjacent; routing units ignore it.
- One grid square holds 10 size points (three humans). Box = near-square block.
- Unassigned garrison units (no fort) fight as one big squad in the centre.
- Front to back that has worked so far: expendable or melee screen → heavy line (Alae with tower
  shields) → javelin and missile troops → commanders. Flank squads offset up or down.

## Leadership and squads (manual p. 59)

A commander leads at most 5 squads and no more units than his leadership. Morale effect by base
leadership: 10: −1 for one squad, another −1 to all per extra squad; 50: no penalty for 1-2
squads, −1 per extra; 100: +1 to all for up to 3 squads, −1 per squad above 3; 150: +2 for up
to 4, −1 to all with a fifth; 200: +3 for all five. The Army Setup row shows squads used/allowed
(Theocratus 2/3, Urgek 1/2) and units led (44/125). Mixing undisciplined units into a squad
makes the whole squad undisciplined with −1 morale; undead or demons mixed with living, −1.
Experience raises leadership (units led) but not these morale bonuses.

## War skills (the user 2026-11-02: call the military skills when playing; build on them)
- Level of war: **tactical (battles run from setup)**; domain: **land (fantasy)**. Vocabulary: military-doctrine (FM 3-90 tactics) first; soviet-doctrine for the
  opposing school; war-concepts (glossary, `warwiki.py look TERM`).
- Every turn / battle: **war-language** (UP: the situation in doctrine terms -> THINK: intent,
  form of manoeuvre, a task and purpose per unit -> DOWN: concrete orders -> CHECK) and **army-log**
  (read, log and evaluate both sides; `armylog.py`). Before the first real game write
  **`LEXICON.md`** in this skill folder (`warlang.py lexicon`): units -> roles, terrain -> OAKOC,
  rules -> effects, victory -> end state, task -> game actions.
- combat-models: The user's land salvo system and Lanchester (concentrate; make fights square when stronger, linear when weaker).
- Dominions battles are set up, not steered: the THINK step is the whole battle - formations, positions and orders ARE the plan.

## Trample, formations and support mages (vanilla rules; checked 2026-11-03)
Learned in the user's SCBM game (its notes: dom6-scbm `tirnanog.md`); these rules are vanilla manual/wiki facts.
- Trample is NOT magic (wiki trample): invulnerability counts as protection there (halved), and an
  ethereal trampler halves 7+size first, so trample is minor. Shield parry does not apply to it.
- Trample REPLACES the weapon attack (wiki trample, "the free attack"): each action a trampler first looks
  for a square to walk over in the 3x3 around it (random enemy), and only swings if none can be trampled
  (largest occupant >= its size). After each trample, 25% chance of one free full attack (antlers + hoof).
  So keep the tank and everyone near it SMALLER than 9: the moose spends its actions on weak halved
  tramples (2-4 squares a round) instead of 27-damage magic gores. Do NOT enlarge the tank to size 9.
  Each trample costs it encumbrance in fatigue - it tires itself.
- TRAMPLE (manual p.~74, illwiki trample): the trampler picks a random enemy in its 3x3 and tramples that whole
  square; everyone in it rolls Defence (no shield parry, armour def mods apply, -1 per 10 fatigue) vs open-ended
  3d6; fail = 7 + trampler size vs HALF protection, pass = 1 damage. 2-4 squares a round. It can only enter a
  square whose LARGEST occupant is smaller (size-1 reach): one big unit in a square shields the small ones.
  Stopped only by the Awe family; mirror images (glamour) take the hit and are lost; Twist Fate negates; Ethereal
  victims 75%. TRUE SIGHT (the moose has it) cuts Blur, Displacement, Invisibility, Dread and Twilight but NOT
  mirror images, and trample uses neither attack skill nor blur - so True Sight changes nothing for its tramples.
- LINE vs DOUBLE LINE vs BOX against a trampler: squares fill the same in every formation (up to 10 size points,
  3 humans), so men lost per trample is the same. Formation changes exposure: a Box has the fewest men on its
  edges (harder to envelop, inner ranks still throw); a Line puts everyone in front (most melee and missiles at
  once, easiest to wrap); Double Line is between. Sparse Line/Skirmish (gaps, -1 morale) leave squares half
  empty only if the squad is small; they don't thin the squares. Verdict: formation is not the answer to
  trample - high defence (Tuatha evaded most), a big unit in the square, Awe, or killing it with magic are.
- PURE BUFF SUPPORT (the user): most Dominions mages are best as buffers/debuffers (Blessing, Gaia's Due, Twist
  Fate, Curse, Horror Mark), unless casting big AoE that doesn't miss. TV Tropes' trinity (damager / healer /
  tank) is mostly subverted: no aggro, no reliable healing in battle; the roles that do exist are blockers,
  damage (missiles, thugs, evocations) and buffer/debuffer mages.
- Mod games: notes that depend on a mod's numbers live in that mod's folder (SCBM: dom6-scbm skill), not here.


## Standards (the user, 2026-11-03 - apply in every Dominions session)
- **Manual first** (manual-first): look a rule up in dom6-mechanics / the manual, then dom6-wiki, before acting
  on a belief. Order of truth: the game > mod files > the manual > videos > the wiki > what the user says (test it if he insists) > a hypothesis. Mod games: mod-docs rules; SCBM = dom6-scbm skill (its data and notes). Check the
  mod's .dm for changes before trusting vanilla numbers.
- **Commit only when absolutely certain.** End Turn only on the user's go for that turn (end-turn rule). Orders and
  battle setups are the commit in Dominions (no live control): every army through dom6-army-check first,
  failure case known (what if the battle goes wrong, who is exposed), never batch-script orders blind.
- **Acting alone** (delegate skill): write intent, bounds and report points in the plan file; self-review with
  the user's questions; hand back with a clear report.
- **Plan in doctrine** (battle-tactics, military-doctrine): roles for every army, the decisive point, concentrate,
  screen, protect commanders and mages; log lessons after every battle (dom6-battle-view -> dom6-tactics).

## Standards (audit 2026-11-03)
- **Where it runs:** prefer Claude's virtual screen (dom6-ui bgplay, dom6bg.py); lock while working, hand back after (hand-back).

## Reference files (read the one the step needs)

| File | Holds |
|---|---|
| `reference/files.md` | **Files** - Builds on the dom6-ui skill (guarded input, vision.py) |
| `reference/the-field-position-army.md` | **The field (Position Army)** - Left is the back, right is the front (we face right) |
| `reference/battle-orders-manual-pp-44-46-58-60-read.md` | **Battle orders (manual pp. 44-46, 58-60; read in full 2026-11-03 at the user's request)** - See also dom6-battle-ai (the same orders plus how the AI picks spells and targets) |
| `reference/battle-log.md` | **Battle log** - Reported | Province | Our setup | Enemy | Result | Notes | |---|---|---|---|---|---| | T3 | Helmshire | Theo |
| `reference/lessons-from-the-reviews.md` | **Lessons (from the reviews)** - Alae Legionnaires (tower shield, armour) shrug off independent infantry: in Murias 7 Heavy   Infantry hits d |
| `reference/open-questions-test-and-record.md` | **Open questions (test and record)** - T8: both battles' only dead were Velites (3 + 3), though they stood behind the line |

## Related skills
dom6-army-check, dom6-battle-view, dom6-spells, dom6-items, dom6-mechanics, battle-tactics, military-doctrine, combat-models, delegate.
Also (2026-11-03): dom6-battle-ai, dom6-supercombatants, dom6-thugs, unit-combat-math, dom6-scouting.
