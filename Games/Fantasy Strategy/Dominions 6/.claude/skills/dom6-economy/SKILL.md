---
name: dom6-economy
description: "The Dominions 6 economy (manual pp. 22-29): income, scales, forts, unrest, supply, upkeep, labs and temples. Use when planning income, recruitment, forts or PD, or when armies starve."
keywords: "turn, steps, population, fort, admin, divided, without, friendly, line, resources, halved, collect, neighbours, points, band, palisades, upward, order, step, raises, lowers, recruiting, blocked, table, resource, loss, people, growth, death, heat, cold, plus, distance, starvation, disease, gold, cost, sacred, slaves, province, defence, level, bought, patrols, point"
---

# Economy (Dominions 6, vanilla)

Plan item 26 (the user approved the extras 2026-11-03). Manual pp.22-29; turn order: income step 38, upkeep 41
(pp.55-56). Scales: dom6-dominion. Unrest from hunting: dom6-blood-hunting.

## Income (p.22)
- Base = population / 100. Modified = base x scale modifiers x (1 + fort admin / 200) (a fort with admin 30
  = +15%). With unrest: / (1 + 0.02 x unrest).
- **No income** from a province that can't trace friendly provinces back to a friendly fort.
- The top bar shows income before upkeep, upkeep in brackets.

## Resources (p.22)
- Halved in the province itself unless it has a fort; forts collect from neighbours by admin %.
- With unrest: / (1 + 0.01 x unrest).
| Unrest | 10 | 25 | 50 | 75 | 100 | 150 | 200 |
|---|---|---|---|---|---|---|---|
| Income | 83% | 67% | 50% | 40% | 33% | 25% | 20% |
| Resources | 91% | 80% | 67% | 57% | 50% | 40% | 33% |

## Recruitment points (p.22)
Population bands, added up: 20 + first 5000/100 + next 5000/200 + next 10000/300 + next 20000/400 + rest/500.
Then the fort bonus (palisades +50%, up to +150%) and Order +10% per step.

## Unrest (pp.23, 29)
- Raised by: events, spies and bards, blood hunting, sites, spells, globals, ruling a province under another
  god's dominion. Lowered by: patrolling (kills 10 people per point), PD (1 per 10 PD a turn), Order, sites.
- **100+ = no recruiting.** Max 500 or one per 10 people.

## Supply (pp.23-24)
- Population supply: 1 per 30 people for the first 15000, then 1 per 60; x growth/death, then heat/cold.
- Plus the best fort within 4 provinces: admin x 6 / (distance + 1) (400% of admin at 0, 200% at 1, 133%,
  100%, 80%).
- Units use supply by size. Short: some troops starve (-4 morale; 5% disease, 50% if starving again);
  survival skills give 50% to be unaffected. Disease stays (dom6-healing). Siege supply: dom6-sieges.

## Upkeep (pp.24, 55)
Gold cost / 15 a turn; sacred units and slaves / 30. Paid after income (step 41); desertion if short.

## Province defence (pp.24, 29)
- Level n costs n gold (PD 10 = 54 total); level 1 free. Bonus troops at 10, 15, 20; max 100; no upkeep;
  restored after a won battle; can't be lowered; needs 10 people per point; captured = gone.
- -1 unrest per 10 PD; from 15, patrol strength = PD - 14 (dom6-stealth).

## Buildings (pp.25-28)
| Fort | Gold | Months | Admin | Commanders |
|---|---|---|---|---|
| Palisades | 1000 | 5 | 15 | +0 |
| Fortress | +600 | 3 | 30 | +1 |
| Castle | +600 | 3 | 45 | +1 |
| Citadel | +600 | 3 | 60 | +2 |
| Grand Citadel | +1000 | 5 | 70 | +2 |
- Each stage builds on the last; era sets the top (EA fortress, MA castle, LA citadel); masons one higher.
- Temple 600 (Man, Marverni half; Pangaea half in forest; LA Gath double): dominion check, preaching bonus,
  sacred recruiting. Lab 600 (cheaper for some): research, rituals, gem transfers.

## Mercenaries (p.29)
Hired for 3 months; when a contract ends the previous employer's bid counts double that one turn.

## Related skills
dom6-dominion (scales), dom6-stealth (patrol, PD), dom6-sieges, dom6-blood-hunting, dom6-healing, dom6-mechanics.
