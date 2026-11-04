---
name: aurora-guide
description: Starter guide to Aurora 4X (C# version 2.x, Steve Walmsley), the deep sandbox space 4X simulation - race and system generation, colonies, population, environment and terraforming, eleven Trans-Newtonian minerals and mining, construction, wealth and the civilian economy, research with scientists, ship design (hulls, armor, engines, sensors, weapons), shipyards and task groups, jump points and survey, thermal/EM signatures and stealth, fire controls, beams, missiles, point defense, EW, ground forces, fuel and maintenance, aliens and diplomacy, officers, xenoarchaeology, time increments, SpaceMaster mode - with a page map of the 1716-page community manual (aurora-manual-2026.03.01.01.pdf, bookmarked; searchable .txt) and the game database (AuroraDB.db, SQLite). Uses game-sources (lookups), learn-to-play (method). Use when the user wants to play, learn or talk about Aurora 4X, design a ship or missile, check a formula, or study Aurora as a model for the user's own 4X engine.
---

# Aurora 4X - starter guide

Status 2026-11-01: manual outline, preface and AI-play chapter read. Game not installed here
(Windows game; free download from the Aurora forums). Community wiki:
https://www.aurora4x.net/wiki/index.php/Main_Page (the user's `Resources` file).

## The manual: use with care

`aurora-manual-2026.03.01.01.pdf` (1716 pages, v2026.02) is an **unofficial, AI-assisted**
community manual (github.com/ErikEvenson/aurora-manual). It cites the game database (AuroraDB.db
v2.7.1, game 2.8.0) for its numbers and marks unverified claims, but Aurora's author has warned
that it contains errors. Rule: the game database and the game beat the manual; the forums and
wiki beat the manual for strategy. Say "per the community manual" when quoting it.

Search: `manual.py grep aurora-manual-2026.03.01.01.txt "Sorium" -C 2`. PDF page numbers below.

## What it is (Claude's summary)

A single-player sandbox that simulates an interstellar civilisation in great detail: you set up
the start (race, system, conditions), the game generates the galaxy as you explore jump points,
and you run economy, research, fleet design and war with no fixed goal. Time advances in chosen
increments (5 seconds to months); interrupts stop it when something happens. Eleven
Trans-Newtonian minerals (Duranium, Neutronium, Corbomite, Tritanium, Boronide, Mercassium,
Vendarite, Sorium, Uridium, Corundium, Gallicite) gate everything you build. Ships are designed
from components you research and size yourself (engines, sensors, missiles are designed too).
Detection is physics-like: thermal and EM signatures against passive and active sensors.
SpaceMaster mode lets a player edit anything (a GM mode).

## Manual map (PDF pages)

Setup: new game options 103, race creation 122, system generation 142, racial traits 151, start
conditions 163. Interface 178-236. Astronomy: systems 237, planets 250, asteroids/comets 265, jump
points 273. Colonies 294, population 315, environment 338, infrastructure 356, terraforming 374.
Economy: minerals 389, mining 399, construction 412, wealth and trade 427, civilian economy 439.
Research: tree 457, scientists 474, facilities 482, categories 494. Ship design: philosophy 515,
hull/armor 533, engines 543, sensors 560, weapons 573, other 593, examples 629. Fleet: shipyards
643, build/refit/repair 656, task groups 665, organisation 676, orders 692. Movement 738, jump
transit 760, survey 780. Sensors and stealth 796-852. Combat 853: fire controls 859, beams 877,
missiles 902, PD 921, EW 935, damage 945, PDCs 961. Ground forces 974-1050. Logistics: fuel 1051,
maintenance 1063, supply ships 1083, habitats 1101. Aliens 1110, communications 1133, treaties
1148, diplomacy 1160, intelligence 1179. Officers 1188-1243. Surveys and xenoarchaeology 1244-1294.
Mechanics 1295, time increments 1312, spoiler races 1318, late game 1336, SpaceMaster 1352.
**Formulas 1360**, glossary 1392, tips 1399, reference tables 1408; worked examples 1443-1622
(economic bootstrap, exploration, mining network, beam cruiser, missile destroyer, fleet battle,
jump point defence, ground invasion); window layouts 1623+. AI-assisted play 87 (how to use an
assistant with the manual).

## For our 4X engine (the user's design docs name Aurora as a model)

- Data lives in one SQLite database (tables like DIM_PlanetaryInstallation): easy to mod, query
  and verify. A good pattern for "everything exportable to plain text" plus speed.
- Semi-turn-based time with variable increments and interrupts: The user's "real time pausable with
  sub pulses". Physics-based detection fits his space-warfare essay (everyone tracks everything;
  EW and stealth degrade targeting).
- Designable components (engines, missiles) at chosen sizes; civilian economy running beside
  the state's; SpaceMaster mode = his "Universe Control Tools".

## War skills (the user 2026-11-02: call the military skills when playing; build on them)
- Level of war: **strategic + tactical (4X)**; domain: **space**. Vocabulary: military-doctrine (FM 3-90 tactics) first; military-operations (strategic/operational levels, principles of war) + war-concepts' strategy section (total/limited war, escalation, war economy, war termination); soviet-doctrine for the
  opposing school; war-concepts (glossary, `warwiki.py look TERM`).
- Every turn / battle: **war-language** (UP: the situation in doctrine terms -> THINK: intent,
  form of manoeuvre, a task and purpose per unit -> DOWN: concrete orders -> CHECK) and **army-log**
  (read, log and evaluate both sides; `armylog.py`). Before the first real game write
  **`LEXICON.md`** in this skill folder (`warlang.py lexicon`): units -> roles, terrain -> OAKOC,
  rules -> effects, victory -> end state, task -> game actions.
- combat-models: the salvo model plus the user's space-warfare essay (military-theory shelf) - tracking, point defence, low staying power, who launches first; war-concepts: space weapon, kill chain, A2/AD.
