# Systems catalogue

Built by borrow.py index from the guides' ## Systems sections; do not edit by hand.

## Time

- **Tabletop Wargames/The US Civil War**: each action phase both players roll a d6; high roller moves first and both get the difference as action points; doubles hand out Special Action Cards and reroll; a difference of 1 gives a point in every theatre (4.1, p3). Shared, swingy tempo.

## Map

- **Roguelikes/Dungeon Crawl Stone Soup**: random levels with hand-made vaults mixed in, written in a text level language (`dat/des`).

## Economy

- **Tabletop Wargames/The US Civil War**: Confederate reinforcements come from resource hexes (build points), the Union's are fixed per theatre; capturing Northern objective hexes gives the South VPs and BPs (2.1.4, 14.3).

## Research

- **Roguelikes/Dungeon Crawl Stone Soup**: experience goes into skills you have used, and you can set which to focus (E): a use-based advancement model with player steering.

## Population

- **AGEOD and Byzantine Games/AGEOD/Field of Glory Kingdoms**: population units by social class assigned to tasks, productivity from a class x job table modified by culture, religion and terrain (`PopJobsProd.csv`, 3.7, 10).

## Characters

- **AGEOD and Byzantine Games/AGEOD/Field of Glory Kingdoms**: Peers of the Realm with traits as governors and commanders; coups and revolts (3.4, 9.5).
- **Roguelikes/Dungeon Crawl Stone Soup**: a species x background pick; aptitudes per species per skill (`aptitudes.txt`).

## Politics

- **AGEOD and Byzantine Games/AGEOD/Field of Glory Kingdoms**: demesne size cap; authority and local authority; loyalty and revolt risk per region; progress and disorder tokens (3.3, 7.2, 9).
- **Roguelikes/Dungeon Crawl Stone Soup**: gods to worship, each with conducts that grant or withdraw powers (J).

## Diplomacy

- **AGEOD and Byzantine Games/AGEOD/Field of Glory Kingdoms**: vassals with their own loyalty; legacy changes the cost of war (3.8, 12).

## Operational war

- **Tabletop Wargames/The US Civil War**: reaction movement lets the defender answer moves (9.0); generals lead stacks (7.0).

## Tactical combat

- **AGEOD and Byzantine Games/AGEOD/Field of Glory Kingdoms**: battles auto-resolve or export to Field of Glory II Medieval and come back (16.5): strategy and tactics from two studios joined by a file.
- **AGEOD and Byzantine Games/Byzantine Games/Field of Glory II Medieval**: Points of Advantage: every factor is a bonus on one scale, 100 POA ~33%, net difference capped at 200; impact then melee; only front ranks count, extra ranks give staying power (13.1-13.2).
- **AGEOD and Byzantine Games/Byzantine Games/Field of Glory II Medieval**: four cohesion states with 2d6 tests and quality as re-rolls instead of modifiers; autobreak by losses; pursuit chances by troop type (14).

## Logistics

- **Tabletop Wargames/The US Civil War**: strategic movement by rail, river, ocean and road with fixed per-side capacities; the Union has far more (3.2, 15.0).

## AI

- **AGEOD and Byzantine Games/AGEOD/Field of Glory Kingdoms**: difficulty as economic bonuses only, never in battle (4.1).
- **AGEOD and Byzantine Games/Byzantine Games/Field of Glory II Medieval**: plays by the player's rules at all levels; difficulty = army balance; auto-deploys by terrain (heavy foot on open ground, cavalry on the open wing) (31.1).

## Victory

- **AGEOD and Byzantine Games/AGEOD/Field of Glory Kingdoms**: Legacy points as the running score and the win condition after turn 100 (7).
- **Roguelikes/Dungeon Crawl Stone Soup**: dive for the Orb of Zot and bring it out; a single death ends the run (manual A).
- **Tabletop Wargames/The US Civil War**: automatic victory checked each end phase (20.3).

## UI

- **AGEOD and Byzantine Games/Byzantine Games/Field of Glory II Medieval**: Win:Draw:Lose odds shown by simulating the combat 1000 times; detailed tooltips list every modifier (13.6). A good answer to "rules too thick to read".
- **Roguelikes/Dungeon Crawl Stone Soup**: designed against tedium and grinding (N, "Philosophy"); full keyboard play, tiles or console.

## Modding

- **AGEOD and Byzantine Games/AGEOD/Field of Glory Kingdoms**: everything in typed CSV tables (type row above the header row) plus BSF scripts: a good model for our engine's data files.
- **AGEOD and Byzantine Games/Byzantine Games/Field of Glory II Medieval**: units in one CSV with a comment row per column; game logic in readable BSF scripts; global mods loaded from Documents without touching the install; 3D unit models with a text animation table (frame ranges per action, sounds, script calls) (25).
- **Roguelikes/Dungeon Crawl Stone Soup**: levels in .des files, game rules partly in Lua, every option in a text init file.
