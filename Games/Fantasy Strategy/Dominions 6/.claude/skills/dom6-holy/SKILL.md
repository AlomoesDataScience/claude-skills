---
name: dom6-holy
description: "Holy magic, priests and sacred units in Dominions 6: priest levels, blessings, banishment, sermons, preaching. Use when scripting priests, planning sacred armies and blesses, or choosing preachers."
keywords: "manual, illwiki, divine-magic, bless, unlocks, blessing, sermon, courage, smite, demon, word, avenger, divine, fanaticism, channeling, spells, cost, fatigue, casting, encumbrance, need, research, replaced, god's, top, path, temples, recruit, half, upkeep, blessable, morale, plus, effects, incarnate, god, map, boosters, thrones, blood, sacrifice, recalling, dead, points, prophets"
---

# Holy magic, priests and blesses (Dominions 6, vanilla)

Plan item 24 (the user approved the extras 2026-11-03). Manual pp.81-85; illwiki `holy`, `divine-magic`,
`bless`. Bless design at god creation: dom6-pretender.

## Divine spells (wiki; manual p.81)
- No research, no gems, **no fatigue** except casting encumbrance (dom6-fatigue) - a priest can chant all
  battle. Works underwater. Pretenders can't cast them.
| Level | Spells |
|---|---|
| H1 | Blessing (sacreds in 5+5/lvl squares), Banishment (undead only, MR) |
| H2 | Sermon of Courage (+1 morale, 10+5/lvl squares), Smite Demon, Holy Word (stuns a sacred/blessed, MR), Holy Avenger (self) |
| H3 | Divine Blessing (all sacreds), Smite (10 AN, MR) |
| H4 | Fanaticism (Sermon for the whole army) |
| H5 | Divine Channeling (+1 holy to friendly priests) |
- God with a path at 4+: Banishment and Smite become path versions (manual p.81 table; wiki: e.g. Earth =
  Pull from the Grave / Word of Stone, Nature = Final Rest / Word of Thorns, Death = Syllable of Death).
- Morale magic bonus caps at +1: Sermon and Fanaticism don't stack with each other (dom6-morale).

## Sacred units and the bless (wiki bless)
- Sacred: recruited only where you have a temple, half upkeep, can be blessed.
- Blessed = +1 morale + the nation's bless effects. Sources: priests' Blessing/Divine Blessing, items, or
  fighting alongside the pretender in friendly dominion. The god always has its bless in its dominion.
- Incarnate blesses (needing 5+ in a path) work only while the god is on the map (not dormant/imprisoned/dead).

## Outside battle
- Preach (dom6-dominion), claim thrones (pretender, prophet or priest 3+), blood sacrifice (some nations),
  **recall a dead god** (priests put ~their level a turn into 50 points), build temples (sacred commanders).
- Holy can't be empowered; boosters are rare (Ring of the False Prophet - cursed - and three artifacts).
- Prophet: one at a time; +1 holy or holy 3; a new one only 6 turns after the last dies (wiki).

## Scripting priests (the user's game)
- The prophet or a priest in the army handles the holy spells (the user, 2026-11-03: "he has the prophet in the
  area"), so mages don't waste rounds on them. Typical: Divine Blessing (if sacreds) -> Sermon -> Smite.
- Eigneach (Tir na n'Og prophet, H3): Divine Blessing + Group Barkskins with nature gems (dom6-scbm tirnanog.md).

## Related skills
dom6-dominion, dom6-morale, dom6-pretender, dom6-fatigue, dom6-magic-resistance, dom6-spell-db, dom6-mechanics.
