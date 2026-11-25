---
name: ww2-eastern-front
description: "Eastern Front 1941-45 as our sources hold it, Kursk 1943 above all: timeline, order of battle, pass targets, the operations (Citadel, Kutuzov, Rumyantsev, Roland), command decisions. Use when setting up, running or judging an Eastern Front scenario."
keywords: "eastern front, ostfront, great patriotic war, kursk, citadel, zitadelle, prokhorovka, kutuzov, rumyantsev, roland, oryol, belgorod, kharkov, ponyri, central front, voronezh front, steppe front, army group centre, army group south, 9th army, 4th panzer army, kempf, ii ss panzer corps, 5th guards tank army, manstein, model, zhukov, vatutin, rokossovsky, stavka, order 227, oob, order of battle"
---

# WW2 Eastern Front - scenarios and checks

**Origin:** the Kursk stress test, the user's engine demo and planned release (`Kursk 1943.md`, plan
`Projects/Our Games/4x Game Engine/plans/kursk-finish.md`). Only Kursk is deep so far. Other battles start from the dump (ww2 hub).

## The method
1. **Set up from data:** `kursk/oob.json` (fronts and armies down to corps, with commanders),
   `kursk/equipment.json`, and reinforcements as R rows in `Kursk timeline.md`.
2. **Inject only what doesn't depend on the battle.** Timeline kinds are W (world), O (order), R
   (reinforcement) and B (battle). Inject W rows, R rows, and O rows that don't depend on the battle. B rows are
   for comparison only. Calling off Citadel, Roland and abandoning Kharkov must come from the command layer
   (`Kursk 1943.md` §4a).
3. **Judge with the gates** in `Kursk pass targets.md`. Gate 1: it works. Gate 2: the books balance and there
   are no impossible kills. Gate 3: over 20 seeds, history sits inside the 10th–90th percentile. Then run the
   counterfactuals: no warning, no Sicily, no Steppe reserve, no repair.
4. **Read Soviet operations as Soviet:** echelons, norms and deep battle (soviet-doctrine). The German side
   uses German doctrine sources, not US ones (`sources-by-nation`).
5. **Stalls come from causes.** the user's static-war rule: an offensive stops when the push falls below the
   defence (doc 22), not when a date arrives.

## Status / open
- Dates to confirm: the Donets/Mius diversion, Oryol's fall, the 5th Guards Tank Army march distance. The
  Sicily, Donbas and Roland articles are now in `kursk/sources/` (plan step 6).
- Tactical demo v0.3.9 (2026-11-25) has every system as a prototype, plus the OOB additions (653/654 Ferdinand,
  Pz-Brigade 10, s.PzAbt 503, and the 4th Gds, 27th, 47th and 53rd Armies; commit 03112ba). Next is v0.4.0: the
  proper Kursk scenario with scenario deployment (the user 2026-11-24). Command (K4/K9) comes last.
- Everything is wiki level until it is checked against Glantz and House, Frieser, Zetterling and Zamulin.

## Related skills
ww2 (hub), soviet-doctrine, military-operations (culmination, lines of operation), toaw4-guide (an operational
wargame to compare with; no Kursk scenario found in our copy yet), ww2-air, ww2-tactics.
