---
name: ww2-air
description: "WW2 air war as we model it: air armies, Luftflotten, airfields as places, aircraft as counts, the sortie cycle, ground attack, Flak, maintenance, losses per sortie. Use when designing or checking WW2 air units, sorties or air losses."
keywords: "air war, luftwaffe, vvs, luftflotte 4, luftflotte 6, air army, 16th air army, 2nd air army, 17th air army, airfield, dummy airfield, sortie, sortie rate, loss per sortie, il-2, ptab, hs 129, ju 87g, stuka, fw 190, bf 109, yak, la-5, po-2, night harassment, flak, 61-k, ground attack, air recon, serviceability, maintenance, ground crew"
---

# WW2 air - airfields, sorties, losses

**Origin:** the user 2026-11-16: "we need to simulate airfields, and airplane sorties", and "obviously airplanes,
equipment, all that needs to be maintained and such by actual processes". The design is in `Kursk 1943.md` §4,
"Airfields and sorties".

## The method
1. **Airfields are places, aircraft are counts.** Each field has a runway, fuel, bombs, spares, a repair shop
   and Flak, supplied like a depot. Aircraft are counts per regiment or Gruppe (ready, in repair, written off),
   and become bodies only while a sortie is in view.
2. **One event per package:** order, take off, fly out (detection and interception), on target, return and
   turnaround. Air combat is a salvo exchange of counts. Ground attack uses the lab against top armour
   (ww2-armour).
3. **Maintenance is a process.** Being ready costs ground crew hours, spares and a place. Readiness falls by
   itself without them. Never use a flat serviceability rate where the process can run.
4. **Raids aim at beliefs.** Dummy fields drew 29 of 35 June Luftwaffe raids, so targets come from what the
   attacker believes (doc 19).
5. **Check by loss per sortie,** not raw totals. The Citadel bands are in `Kursk pass targets.md` (VVS 4.95%,
   Luftwaffe 0.709%, day 1 losses 176:26).

## Status / open
- To check: the Luftflotte 4 commanders, the 1st, 15th and 5th Air Armies for Kutuzov, and which Flakpanzers
  existed in July 1943. Sortie timelines need Bergström. The wiki gives only daily totals.
- Fails when: maintenance hours or fitter numbers are invented with no sourced serviceability rate to check.

## Related skills
ww2 (hub), ww2-armour (ground-attack kills), combat-models (salvo exchange), ww2-eastern-front (when and where).
