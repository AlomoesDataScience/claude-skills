---
name: ww2
description: "Hub for Second World War knowledge: where our WW2 sources, data and docs live, pulling more from the local Wikipedia dump, source grades, the nation rule. Use when any WW2 fact, unit, weapon, battle or doctrine is needed."
keywords: "ww2, wwii, world war 2, world war two, second world war, 1939, 1940, 1941, 1942, 1943, 1944, 1945, wehrmacht, red army, heer, waffen-ss, luftwaffe, vvs, axis, allies, eastern front, ostfront, kursk, normandy, pacific, japanese army, imperial japanese, source grade, wiki level, dumpget, enwiki dump, glantz, frieser, zetterling, zamulin, krivosheev, bergstrom"
---

# WW2 - the hub of the WW2 skill group

**Origin:** the user 2026-11-16: "You should also make WW2 understanding a skill group too, ww2 has too much
information to skill." So this hub only says where things are. The topic skills below hold the method, and the
facts stay in the files they name. Don't copy facts into skills.

## The group
| Skill | For |
|---|---|
| ww2-armour | penetration, armour profiles, the lab hit rule, equipment.json |
| ww2-tactics | squads, close-combat kit, AT units (Pakfront, PTOP, Panzerjäger), Japanese handbooks |
| ww2-air | air armies, Luftflotten, airfields, the sortie cycle, losses per sortie |
| ww2-eastern-front | Kursk timeline, OOB, pass targets, Soviet and German operations 1943 |

## Where things are
- **Kursk work** (our deepest WW2 set): `Projects/Our Games/4x Game Engine/Build Proposal/battles/`, which has
  `Kursk 1943.md` (design), `Kursk timeline.md`, `Kursk pass targets.md` and `kursk/` (`equipment.json`,
  `oob.json`, `tactics.json`, `sources/` with about 150 articles plus `SOURCE.md`). The JSON files start
  with `//` comments, so strip those lines before parsing.
- **Wikipedia, offline:** `Theory/Sources/Wikipedia/enwiki-dump/` (the 2026-11-01 dump, all 71 parts).
  Get articles with no web call:
  `python3 -I .claude/skills/wiki-scout/scripts/dumpget.py Theory/Sources/Wikipedia/enwiki-dump --find REGEX`,
  then `... dumpget.py DUMP OUTDIR "Title" "Title"`. One call is about 1 minute, so batch the titles. For battle
  work, put the articles in the battle's `sources/` folder.
- **Manuals shelf:** `Theory/Sources/Military Theory/` (military-theory skill). WW2-era: the Handbook on Japanese
  Military Forces, 1942 and 1944 (US War Department), and Svechin's *Strategy* (1927, the pre-war Soviet
  base). Later works used as background only: FM 100-2-1 (1984 Soviet army), the CIA report, Sustainment.
- **TOAW IV:** `Games/Wargames/The Operational Art of War IV/` holds the manuals, the equipment database guide,
  the panzerworld German organisation and symbol tables, and the manoftin WW2 ranges note (toaw4-guide skill).
  FM 17-12 there is US tank gunnery. It is not used for German or Soviet fire.

## Rules for WW2 sources
1. **Order of truth** holds: game or data files > manual > wiki > word > hypothesis. A wiki fact is
   "wiki level": cite the article, and mark it to check against the books before release (Glantz and House,
   Frieser, Zetterling, Zamulin, Krivosheev, Bergström). Name the author whenever the article does, because
   counts differ by author (e.g. 252 or 323 German tanks lost at Citadel).
2. **Sources by nation:** generic human doctrine is the default, never US doctrine. Tag every source with its
   nation. Japan comes from the US 1942 and 1944 handbooks, read as a foe's view (memory `sources-by-nation`).
3. **Pastes from other AIs** (Gemini and others) are leads only. Find the claim in a source before using it.
   - Update, the user 2026-11-24: "I think all the stuff gemini is posting is generally fine for our use." Gemini
     figures may stand as working numbers, tagged "Gemini (the user 2026-11-24: fine for our use)", ranked under any
     source we hold, and checked against a book before release.
4. **Web:** site-rules first for any new host, one request at a time, and the user sees every call.
   tanks-encyclopedia.com is never fetched. Wayback first. Text only, in our own words.
5. Every claim taken into a design gets a **Fails when** (`failure-clauses-rule`).

## Related skills
ww2-armour, ww2-tactics, ww2-air, ww2-eastern-front (the group); soviet-doctrine (Soviet operations and norms),
military-theory (the manuals shelf), toaw4-guide (an operational WW2 game and its data), wiki-scout (dumpget.py,
dumppass.py), combat-models (salvo and Lanchester for the numbers).
