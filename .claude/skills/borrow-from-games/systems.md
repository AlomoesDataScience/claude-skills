# Systems catalogue

Built by borrow.py index from the guides' ## Systems sections; do not edit by hand.

## Time

- **Space Strategy/Aurora 4x**: player picks the increment (5 s to 30 days); sub-pulses inside; automatic interrupts (contact, missile launch, ship under fire, fleet arrival, construction/research done, fuel, breakdowns); C# removed false interrupts (no-target fire controls make a message, not a stop) (manual p1312-1313)
- **Tabletop Wargames/Solar Starfire**: campaign in monthly turns processed by the Space Master (X1 checklist); battles drop to tactical turns (B, X)
- **Tabletop Wargames/The US Civil War**: each action phase both players roll a d6; high roller moves first and both get the difference as action points; doubles hand out Special Action Cards and reroll; a difference of 1 gives a point in every theatre (4.1, p3). Shared, swingy tempo.

## Map

- **Roguelikes/Dungeon Crawl Stone Soup**: random levels with hand-made vaults mixed in, written in a text level language (`dat/des`).

## Economy

- **Historical Strategy/Rule The Waves**: yearly budget from national resources x share given to the navy, paid monthly; a big surplus gets taken by politicians; colony income declines and democracies free their colonies late (p12-13)
- **Tabletop Wargames/Solar Starfire**: everything in MegaCredits; population units give income; Gross Planetary and Empire Value (L, p103)
- **Tabletop Wargames/The US Civil War**: Confederate reinforcements come from resource hexes (build points), the Union's are fixed per theatre; capturing Northern objective hexes gives the South VPs and BPs (2.1.4, 14.3).

## Production

- **Space Strategy/Space Empires/Space Empires IV**: ship design from components (the user's WMD mod reworks every component, see se4-modding/wmd.md)
- **Space Strategy/Stars!**: per-planet production queue; three minerals (Ironium, Boranium, Germanium) gate everything
- **Tabletop Wargames/Solar Starfire**: ships designed as rows of system boxes on a control sheet (H)

## Research

- **Roguelikes/Dungeon Crawl Stone Soup**: experience goes into skills you have used, and you can set which to focus (E): a use-based advancement model with player steering.

## Population

- **AGEOD and Byzantine Games/AGEOD/Field of Glory Kingdoms**: population units by social class assigned to tasks, productivity from a class x job table modified by culture, religion and terrain (`PopJobsProd.csv`, 3.7, 10).
- **Historical Strategy/Rule The Waves**: unrest (workers) rises with military spending, long wars, blockade, defeats; falls with victories, social programmes, lower spending; acts as a brake on the budget and can bring revolution (p62); fleet morale follows it
- **Space Strategy/Aurora 4x**: unrest points cut ALL output by the same percent (25 unrest = -25%); sources with yearly rates (radiation, overcrowding, too few occupation troops, too little local protection, forced labour); police strength above the requirement reduces it; natural fall depends on Determination (formulas p1387, p330-331)

## Characters

- **AGEOD and Byzantine Games/AGEOD/Field of Glory Kingdoms**: Peers of the Realm with traits as governors and commanders; coups and revolts (3.4, 9.5).
- **Roguelikes/Dungeon Crawl Stone Soup**: a species x background pick; aptitudes per species per skill (`aptitudes.txt`).
- **Tabletop Wargames/Solar Starfire**: graded leaders (Average, Crack, Elite, Legendary); a chain of command where a higher rank overrides, same rank follows diplomats > admirals > generals > governors; good leaders keep units loyal in rebellions (S, p152)

## Politics

- **AGEOD and Byzantine Games/AGEOD/Field of Glory Kingdoms**: demesne size cap; authority and local authority; loyalty and revolt risk per region; progress and disorder tokens (3.3, 7.2, 9).
- **Historical Strategy/Rule The Waves**: national characteristics (efficient yards, cautious, surprise attack, hidden faults...); government types change by revolution; tension per nation rises toward war - the player influences but does not decide (p59-60)
- **Roguelikes/Dungeon Crawl Stone Soup**: gods to worship, each with conducts that grant or withdraw powers (J).
- **Space Strategy/Aurora 4x**: political status per colony (slave, conquered, occupied, subjugated) multiplies the troops needed; colonies expect armed ships in the system (protection value) (p330, p1387)

## Diplomacy

- **AGEOD and Byzantine Games/AGEOD/Field of Glory Kingdoms**: vassals with their own loyalty; legacy changes the cost of war (3.8, 12).
- **Space Strategy/Aurora 4x**: communication rating 0-100% with each alien race before any treaty (p1133)
- **Tabletop Wargames/Solar Starfire**: first contact needs sustained communication first; a cut-off contact ship may sign treaties up to restricted trade only; NPRs negotiate in fixed stylised states like "dummy hands"; suspicious behaviour (hiding, splitting up near their star) triggers a war check (T, p158-160)

## Operational war

- **Historical Strategy/Rule The Waves**: surprise attacks at war start change with the era (destroyers, submarines, carriers); blockade (p67-68)
- **Tabletop Wargames/Solar Starfire**: in a system under attack, governors and leaders order arriving units to fight, pass or retreat; outside orders can't arrive in time (V1.01.5, p182)
- **Tabletop Wargames/The US Civil War**: reaction movement lets the defender answer moves (9.0); generals lead stacks (7.0).

## Tactical combat

- **AGEOD and Byzantine Games/AGEOD/Field of Glory Kingdoms**: battles auto-resolve or export to Field of Glory II Medieval and come back (16.5): strategy and tactics from two studios joined by a file.
- **AGEOD and Byzantine Games/Byzantine Games/Field of Glory II Medieval**: Points of Advantage: every factor is a bonus on one scale, 100 POA ~33%, net difference capped at 200; impact then melee; only front ranks count, extra ranks give staying power (13.1-13.2).
- **AGEOD and Byzantine Games/Byzantine Games/Field of Glory II Medieval**: four cohesion states with 2d6 tests and quality as re-rolls instead of modifiers; autobreak by losses; pursuit chances by troop type (14).
- **Historical Strategy/Rule The Waves**: battles on a tactical map where you command divisions; AI-controlled divisions follow national traits (Cautious) (p77+); look: ship silhouettes, health bars, division flags (shot `Proposal/UI References/images.jpeg` in the 4x project)
- **Space Strategy/Aurora 4x**: fixed phase order each increment: movement + defensive fire, beams + area PD, missile launch, missile movement, CIWS, damage (p853); no separate battle screen - it happens on the system map
- **Space Strategy/Space Empires/Space Empires IV**: each battle strategic (auto, a second or two) or tactical (hand-played); ships fight by **strategies** stored with the design: primary and fallback movement (don't get hurt, max/optimal/short range, point blank, board, ram), targeting priority, type priority, don't fire on, fighter launch group size, who breaks formation (manual p47-48, p65)
- **Space Strategy/Stars!**: auto-resolved; per-fleet **battle plans** (primary and secondary target type, tactic, who to attack) set before; up to 16 rounds; tokens (same-design groups) move and fire in phases; **Battle VCR** replays any battle on demand from the message's View button (user guide 15-11, "Reviewing a Space Battle")

## Logistics

- **Tabletop Wargames/The US Civil War**: strategic movement by rail, river, ocean and road with fixed per-side capacities; the Union has far more (3.2, 15.0).

## Intelligence

- **Tabletop Wargames/Solar Starfire**: communications are a technology ladder: starships and civilian freight network first, then courier drones and buoys at warp points, then comm modules; messages cross warp points only aboard a ship or drone; tightbeam needs a contact point, broadbeam is less secret; data takes hours to turn into information; ships keep **sensor records** of battles that must be carried home (P1-P5, p141-143)

## AI

- **AGEOD and Byzantine Games/AGEOD/Field of Glory Kingdoms**: difficulty as economic bonuses only, never in battle (4.1).
- **AGEOD and Byzantine Games/Byzantine Games/Field of Glory II Medieval**: plays by the player's rules at all levels; difficulty = army balance; auto-deploys by terrain (heavy foot on open ground, cavalry on the open wing) (31.1).
- **Tabletop Wargames/Solar Starfire**: NPRs generated from tables with their own tendencies; most systems have no civilisation (Y, p220)

## Victory

- **AGEOD and Byzantine Games/AGEOD/Field of Glory Kingdoms**: Legacy points as the running score and the win condition after turn 100 (7).
- **Historical Strategy/Rule The Waves**: prestige = your standing (victories, tough answers to events); spent as a currency to sway events; too low and you are sacked (game over); end score for the Hall of Fame (manual p12)
- **Roguelikes/Dungeon Crawl Stone Soup**: dive for the Orb of Zot and bring it out; a single death ends the run (manual A).
- **Tabletop Wargames/The US Civil War**: automatic victory checked each end phase (20.3).

## UI

- **AGEOD and Byzantine Games/Byzantine Games/Field of Glory II Medieval**: Win:Draw:Lose odds shown by simulating the combat 1000 times; detailed tooltips list every modifier (13.6). A good answer to "rules too thick to read".
- **Roguelikes/Dungeon Crawl Stone Soup**: designed against tedium and grinding (N, "Philosophy"); full keyboard play, tiles or console.
- **Space Strategy/Aurora 4x**: one window per subject behind a row of 30 icon buttons; system map with display checkboxes per layer; dense, powerful, hard to learn (the user's reference shot `Projects/Our Games/4x Game Engine/Proposal/UI References/innersol1.png`)
- **Space Strategy/Stars!**: one main screen: star map, left column of stacked tiles for the selected planet or fleet (minerals, status, production, starbase), message pane with Prev/Goto/Next, summary pane for the object under the cursor, distance readout (the user's reference shot `Proposal/UI References/stars_1.png` in the 4x project)

## Modding

- **AGEOD and Byzantine Games/AGEOD/Field of Glory Kingdoms**: everything in typed CSV tables (type row above the header row) plus BSF scripts: a good model for our engine's data files.
- **AGEOD and Byzantine Games/Byzantine Games/Field of Glory II Medieval**: units in one CSV with a comment row per column; game logic in readable BSF scripts; global mods loaded from Documents without touching the install; 3D unit models with a text animation table (frame ranges per action, sounds, script calls) (25).
- **Roguelikes/Dungeon Crawl Stone Soup**: levels in .des files, game rules partly in Lua, every option in a text init file.
- **Space Strategy/Aurora 4x**: all data in one SQLite database (DIM_ tables)
- **Space Strategy/Space Empires/Space Empires IV**: plain text data files (`Name := value`), mods load as a folder over Data/ (se4-modding)
