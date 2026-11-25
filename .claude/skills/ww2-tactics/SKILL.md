---
name: ww2-tactics
description: "WW2 small-unit and anti-tank tactics as our design reads them: squads, close-combat kit, German Panzerjäger and Panzerabwehr units, Soviet PTOP and Pakfront, mines, the Japanese handbooks. Use when designing or judging WW2 squad, platoon or AT-unit behaviour."
keywords: "squad, gruppe, otdeleniye, platoon, company, panzerjager, panzerabwehrzug, panzervernichtungstrupp, close combat, hafthohlladung, magnetic mine, rpg-40, rpg-43, ptrd, ptrs, anti-tank rifle, molotov, satchel charge, anti-tank dog, panzerfaust, panzerschreck, ptop, pakfront, anti-tank strongpoint, minefield, channelling, hold fire, 14th company, japanese tactics, tm 30-480"
---

# WW2 tactics - squads and anti-tank units

**Origin:** the user 2026-11-16 on dedicated AT units: German Panzerabwehrzug, Soviet PTOP and Pakfront (from Gemini
pastes, so leads only). On close-combat charges: "Effectiveness is uh, well, yah know", meaning low and costly.
The design is in `Kursk 1943.md` §6: the close-combat kit table, "How a regular squad kills a tank" and
"Dedicated anti-tank units".

## The method
1. **Date every item.** Kit and units existed only in a given window (the Panzerfaust and Panzerschreck came
   after Kursk; AT dogs ended in December 1943). The kit table in §6 has the dates. Check the date against the
   scenario before giving a squad anything.
2. **Kit is a role slot, not a unit type.** A charge team is men from a squad carrying an item. Its kill chance
   comes from the item's stats against the plate it reaches (ww2-armour), and the cost is the team's exposure.
3. **Doctrine sets fire rules, not hit rates.** Pakfront means hold fire, then all guns on one target, with
   mines 500 m–1 km out channelling the tanks. PTOP = 4–6 AT guns, 6–9 AT rifles, 5–7 MGs. German Panzerjäger
   use mobile and ambush tactics. In code a doctrine tag changes only fire control (a doc 20 net) and
   placement. The kills still come from the lab.
4. **Tank riders** (Soviet tankodesant) are decided (the user 2026-11-16: "tank riders is correct"). Infantry ride on
   tank decks as riders do on horses (`Kursk 1943.md` §6 Cavalry and riders): two bodies, and a hit on the tank
   can strip the riders off. **Built 2026-11-25** as a prototype (`src/Sim/Tactical/Riders.cs`, TAC_RIDERS, commit
   409836e, Bench not yet run). The user: dismount on "assumed contact" (spotters fed them data), else at the
   staff's dismount line, else on contact "unless they think they shouldn't". Tanks are the only carriers; trucks
   aren't in the battle yet, and half-tracks are dismountables with their own drill (not built).
6. **Spotting** (the user 2026-11-25, documented, not built): high spotting only for recon or elements with recon
   tools; using them is active; spotting can be combined with hiding but means being somewhat exposed. Sources:
   `kursk/sources/spotting/` (pulled, not read yet).
5. **Japan:** read the 1942 and 1944 handbooks (`Theory/Sources/Military Theory/`) as a US view of a foe, and
   tag it so (`sources-by-nation`).

## Status / open
- The Lone Sentry report on German AT tactics: lonesentry.com blocks our scripts (site-rules, 2026-11-23); use
  the archive.org copy or the user's hand download.
- Fails when: charge teams get a cheap kill rate. Check the history: a charge works against a tank that is
  blind, stopped or alone, and fails otherwise.

## Related skills
ww2 (hub), ww2-armour (the plate and the penetration), military-doctrine (task names), soviet-doctrine (norms,
echelons), battle-tactics.
