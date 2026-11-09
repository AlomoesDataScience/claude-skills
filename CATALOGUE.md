# Catalogue

Written by export.py. `generic` skills work anywhere; `tool` = standalone program; the
others were built for one game or one shelf (folder shown) and work as knowledge plus tools.

| Skill | From | What it is |
|---|---|---|
| archive-curator | generic | Turn archived Claude Code sessions into lasting knowledge (skill edits, new skills, memory, BACKLOG, plans) and track which sessions are done with curate.py. |
| army-log | generic | Read and log both armies every wargame turn (one CSV per side), then evaluate losses, cohesion, combat power and force ratios with armylog.py. |
| battle-tactics | generic | How Claude plans and fights tactical battles in any wargame: The user's turn method, the planning questions, general principles, per-game notes. |
| borrow-from-games | generic | Use every learned game as a parts bin for designing ours: a systems taxonomy, borrow.py catalogue and search. |
| chat-review | generic | Review past Claude Code sessions without loading raw transcripts: chatreview.py makes a short digest, then summarise it or mine it for lessons and new skills. |
| check-skills | generic | Check which skills a task needs and load only those, via the hook's hints, checkskills.py and the routing INDEX.md. |
| cleanup | generic | Cleanup pipeline: cleanup.py catalogues a folder's clutter (duplicates, installers, archives, caches, temp, empty, loose files) for the user to tick; ticked items move to a reversible holding folder. |
| combat-models | generic | Combat models for playing and designing games: Hughes' salvo model, Lanchester's laws, Helmbold, with combat.py. |
| context-audit | generic | Measure where Claude Code's context and usage go from the session transcripts (ctxaudit.py): requests, context size, compactions, tokens by source. |
| context-hygiene | generic | Working rules that keep context small: OCR over screenshots, crops, batched calls, capped outputs, sections not whole files, few skills loaded. |
| delegate | generic | Acting as the user's delegate when he hands over control: mission command, self-review checklist, certainty test, decision log, hand-back. |
| dice-math | generic | Exact dice odds for any game with dice.py: sums, keep-highest, exploding and open-ended dice, re-rolls, opposed rolls, chance to hit a target. |
| discord-logs | generic | Read the user's Discord history from Discord's data export zip into per-channel logs and a searchable database (discordlogs.py). |
| doc-standards | generic | Documentation standards for this workspace: progressive disclosure, Diataxis kinds, one fact in one place, dates and sources, lifecycle labels, decision records, size budgets, with the docs.py checker |
| draw-map | generic | Draw a game map as a clean schematic picture (grid, terrain colours, units, arrows) from a text board with drawmap.py. |
| draw-moves | generic | Draw a movement plan on a game board, all turns in one picture or one per turn, from a plan file with turnplan.py. |
| game-database | generic | Build a rank-everything database for any game: every unit, spell or item from the data files, sorted and ranked by purpose. |
| game-setup | generic | Get a game running properly for Claude (bgplay, Steam launch options, windowed mode, GPU, logs) and parse its UI by hovering every element. |
| game-sources | generic | Turn a game's manuals and wikis into searchable page-numbered text and list the user's Steam library (steamlib.py). |
| game-ui | generic | Drive any game or app window on the X11 desktop or the background bgplay screen: shots, clicks, keys, typing, plus Tesseract OCR. |
| generalize-learning | generic | When and how to lift a lesson from a game-specific skill into a generic one, and what stays game-specific. |
| hand-back | generic | Lock the user's input while Claude drives the virtual screen and hand control back the moment it is done, screen left as he had it. |
| idle-view | generic | Where to leave a game's camera and mouse while Claude is idle so the screen looks natural for viewers and recordings. |
| install-windows-games | generic | Install Windows games (GOG offline installers, setup.exe) and GOG Linux .sh installers into Lutris, one Wine prefix each (wininstall.py). |
| learn-from-tutorials | generic | Learn any game through its built-in tutorials, lessons and hint modes: play every lesson, read each prompt as a rule, write it down. |
| learn-to-mod | generic | How Claude learns to mod a game: how mods load, where data lives, the manual's modding chapter, a test mod. |
| learn-to-play | generic | How Claude learns to play a new video game: manual and in-game help first, map the screen, safe exploration, one test at a time, lessons written down. |
| loading-screens | generic | Tell whether a game screen is loading and wait through loads properly (shot before, frames after, one general loading test). |
| manual-first | generic | The reflex when anything new shows in a game: look it up in the manual first (lookup.py), then write it into the guide with the page. |
| map-camera | generic | Drive a game's map camera to see everything: find the camera controls, clear overlays, centre, zoom, pan. |
| map-measure | generic | Get a game map's size and dimensions early so every square can be found in photos. |
| map-usage | generic | Generic method for using any game's map to make decisions: layout, grid, coordinates, zones, sides, fog, terrain. |
| military-doctrine | generic | Real tactics from US Army FM 3-90 for games: operations, forms of maneuver, tactical tasks, security, recon, control measures. |
| military-operations | generic | The operational level of war from FM 3-0 for games: principles of war, operational art, lines of operation, culmination. |
| mod-diff | generic | Find what a mod or patch changed in any game and what got better or worse, by diffing exported tables. |
| mod-docs | generic | Keep modded games apart from vanilla: find the mods and versions first, one folder per mod, check the mod before quoting numbers. |
| move-phases | generic | Give a turn's movement in phases (main body, extension pass, final check), verifying each before the next. |
| obs-record | generic | Record Claude's gameplay with OBS Studio (flatpak) via its UI and WebSocket (obs.py): start, stop, pause while thinking. |
| photo-map | generic | Find out what is going on in any map game: identify UI vs map, zoom out, photograph the whole map, stitch (panorama.py), build the board. |
| planning | generic | Make a detailed plan before non-trivial work, save it as a file (plan.py) and re-read and tick it as work goes. |
| rules-skills | generic | Turn a game's rules into a family of mechanics skills and guides (the method behind the Dominions 6 set). |
| save-scum | generic | Learning-only save and reload around tests to repeat them or undo a bad result. |
| scouting | generic | Generic scouting for any strategy or tactics game: purposes, fog of war, what to look for, reports, counter-scouting. |
| screening | generic | Generic screening for any tactics or strategy game: The user's definition, what screens do, placement, when to pull back. |
| skill-sync | generic | Keep skills current with the skills they learn from, and move files in and out of skills (sync.py). |
| skills-manager | generic | Manage Claude's skills: route a task to skills, list, check budgets, make, import, disable, and generate the routing INDEX.md (skills.py). |
| source-triage | generic | Sort which of a game's documents are worth reading and in what order when a pile is dropped. |
| soviet-doctrine | generic | The Soviet school of operations and tactics for games (FM 100-2-1 and a CIA report): echelons, deep battle, norms. |
| stream-panel | generic | A side window for recordings and streams: tracker on top (game, status, goals) and Claude's live log below. |
| unit-combat-math | generic | Unit-versus-unit combat math for any game: hit chance, damage after armour, rounds to kill, both ways. |
| unload | generic | Unload context: write a hand-off file, then clear or compact; find old context again with recall. |
| video-watch | generic | Read and watch videos (YouTube or local files) with video.py: info, transcript, frames at chosen times. |
| waiting-checklist | generic | Make a checklist document for work parked until something happens (game free, the user's go, a file). |
| war-concepts | generic | Glossary of war concepts for games, triaged from Wikipedia's war index into what matters for play and design. |
| war-language | generic | Translate a game's situation up into military terms (METT-TC, SALUTE, mission, intent), reason there, and back down into orders. |
| wiki-scout | generic | Find and pull wikis, manuals and docs for a game or franchise as safe text (Wayback first) with scout.py. |
| write-skill | generic | How to write or rewrite a skill so it passes the checker and gets used: format, budgets, keywords, layout, where it goes. |
| mapgen | tool | standalone tool in Games/Fantasy Strategy/Dominions 6/Maps/mapgen/ |
| spritestudio | tool | standalone tool in Games/Fantasy Strategy/Dominions 6/spritestudio/ |
| economic-theory | Economic Theory/.claude | The user's economic theory shelf (Smith, Mill, Marx and more) as searchable text with each work's core ideas. |
| fogk-guide | Games/AGEOD and Byzantine Games/AGEOD/Field of Glory Kingdoms/.claude | Guide to Field of Glory Kingdoms (AGEOD/Slitherine), medieval grand strategy of realms, vassals and population: manual map, rules, data. |
| fog2m-guide | Games/AGEOD and Byzantine Games/Byzantine Games/Field of Glory II Medieval/.claude | Guide to Field of Glory II Medieval, a turn-based tactical battle wargame on a square grid: manual page map, rules, UI, lessons. |
| fog2m-map | Games/AGEOD and Byzantine Games/Byzantine Games/Field of Glory II Medieval/.claude | Using the Field of Glory II Medieval battle map: layout, deployment zones, whole-map photos, reading squares and terrain. |
| fog2m-scouting | Games/AGEOD and Byzantine Games/Byzantine Games/Field of Glory II Medieval/.claude | Scouting in Field of Glory II Medieval: the per-turn enemy reading routine (photos, hovers, counts, diffs, hidden units in woods). |
| gearcity-guide | Games/Economic Games/Gear City/.claude | Starter guide to GearCity, the car-industry business sim: component design, factories, markets. |
| coe5-guide | Games/Fantasy Strategy/Conquest of Elysium 5/.claude | Starter guide to Conquest of Elysium 5 (Illwinter): turns, resources, armies, combat, magic, the 24 classes, manual page map. |
| dom6-abilities | Games/Fantasy Strategy/Dominions 6/.claude | Dominions 6 unit stats and special abilities (manual pp. |
| dom6-armor | Games/Fantasy Strategy/Dominions 6/.claude | How armour and protection work in Dominions 6: protection roll, natural plus armour, shields, encumbrance. |
| dom6-army-check | Games/Fantasy Strategy/Dominions 6/.claude | Pre-End-Turn checklist for every Dominions 6 army and commander: mage/priest scripts, gems, positions, orders, items. |
| dom6-battle-ai | Games/Fantasy Strategy/Dominions 6/.claude | How Dominions 6 battles run themselves and what the battle AI does (manual and casting-AI notes): orders, targeting, unscripted mages. |
| dom6-battle-view | Games/Fantasy Strategy/Dominions 6/.claude | Review a Dominions 6 battle replay: battle_review.py reads the summary and combat log so Claude learns from it. |
| dom6-battlefield | Games/Fantasy Strategy/Dominions 6/.claude | Dominions 6 battlefield conditions: clouds, darkness, night, battlefield enchantments and their effects (manual pp. |
| dom6-best-by-purpose | Games/Fantasy Strategy/Dominions 6/.claude | What is good in vanilla Dominions 6 for each purpose: top generic spells for damage, buffs, debuffs, fear, enchantments, rituals. |
| dom6-blood | Games/Fantasy Strategy/Dominions 6/.claude | Blood magic and blood slaves in Dominions 6: slaves as gems, sacrifices, sabbaths, the blood economy. |
| dom6-blood-hunting | Games/Fantasy Strategy/Dominions 6/.claude | Blood hunting in Dominions 6: the three checks, unrest, hunter choice, patrols and income. |
| dom6-buffs | Games/Fantasy Strategy/Dominions 6/.claude | How buffs and debuffs work in Dominions 6: kinds, stacking, scripting order, item buffs. |
| dom6-combat-math | Games/Fantasy Strategy/Dominions 6/.claude | Melee combat math for Dominions 6: hit chances, damage per attack and rounds to kill from unit cards, with a calculator. |
| dom6-communions | Games/Fantasy Strategy/Dominions 6/.claude | Communions in Dominions 6: astral Communion, blood Sabbath, master and slave scripting, path boosts and fatigue. |
| dom6-dominion | Games/Fantasy Strategy/Dominions 6/.claude | Dominion and scales in Dominions 6: belief vs control, max dominion, temples, prophets, preaching, scale effects. |
| dom6-drn | Games/Fantasy Strategy/Dominions 6/.claude | The Dominions 6 dice roll (open-ended 2d6 DRN) with exact probability tables for opposed checks. |
| dom6-economy | Games/Fantasy Strategy/Dominions 6/.claude | The Dominions 6 economy (manual pp. |
| dom6-evocations | Games/Fantasy Strategy/Dominions 6/.claude | How damage spells work in Dominions 6: casting time, landing, area, precision, MR, killing power. |
| dom6-fatigue | Games/Fantasy Strategy/Dominions 6/.claude | Fatigue in Dominions 6 battles: what builds it, spell fatigue, encumbrance, unconsciousness and recovery. |
| dom6-forging | Games/Fantasy Strategy/Dominions 6/.claude | Forging magic items in Dominions 6: the Forge Item order, Construction levels, path levels, gems, forge bonus. |
| dom6-game | Games/Fantasy Strategy/Dominions 6/.claude | Play an ongoing Dominions 6 game in the running client: main-screen hotkeys, what the screen shows, orders, transfers, turn routine. |
| dom6-gem-casting | Games/Fantasy Strategy/Dominions 6/.claude | How magic gems work in Dominions 6: battle gem boosts, fatigue halving, rituals and forging costs. |
| dom6-healing | Games/Fantasy Strategy/Dominions 6/.claude | Hit points, healing, regeneration and afflictions in Dominions 6. |
| dom6-holy | Games/Fantasy Strategy/Dominions 6/.claude | Holy magic, priests and sacred units in Dominions 6: priest levels, blessings, banishment, sermons, preaching. |
| dom6-inspector | Games/Fantasy Strategy/Dominions 6/.claude | Local copy of the Dominions 6 Mod Inspector with every vanilla unit, spell, item, site, nation and event, searchable from scripts. |
| dom6-items | Games/Fantasy Strategy/Dominions 6/.claude | Claude's ranked guide to Dominions 6 magic items: killing, protection, utility and boosters, by worth. |
| dom6-knowledge | Games/Fantasy Strategy/Dominions 6/.claude | Claude's Dominions 6 knowledge base learned from the running game: nation files, screens, icons, magic symbols. |
| dom6-magic-duel | Games/Fantasy Strategy/Dominions 6/.claude | The Magic Duel spell in Dominions 6: who it picks, the 1d6 plus astral skill roll, odds and counters. |
| dom6-magic-resistance | Games/Fantasy Strategy/Dominions 6/.claude | Magic resistance and penetration in Dominions 6: the MR check, penetration, which spells check it, odds. |
| dom6-map | Games/Fantasy Strategy/Dominions 6/.claude | Reading and using the Dominions 6 strategic map from the virtual screen: panels, provinces, armies, scout reports. |
| dom6-maps | Games/Fantasy Strategy/Dominions 6/.claude | Make Dominions 6 maps with MapNuke 2: players, era, layout, nations (mod nations too), install and check. |
| dom6-mechanics | Games/Fantasy Strategy/Dominions 6/.claude | Dominions 6 rules and formulas from the official manual: dice, melee, missiles, armour, morale, magic and more, with page refs. |
| dom6-mod-magic | Games/Fantasy Strategy/Dominions 6/.claude | What a Dominions 6 mod does to magic: modmagic.py sorts every touched spell into new, better, worse or mixed. |
| dom6-modding | Games/Fantasy Strategy/Dominions 6/.claude | Write, change or check Dominions 6 mod files (.dm): nations, units, pretenders, spells, items, sites, events. |
| dom6-modinspector | Games/Fantasy Strategy/Dominions 6/.claude | Load Dominions 6 mods (.dm) into the Mod Inspector and read what they add and change as text. |
| dom6-morale | Games/Fantasy Strategy/Dominions 6/.claude | Morale and rout in Dominions 6: squad morale checks, triggers, leadership, fear, routing armies. |
| dom6-mounts | Games/Fantasy Strategy/Dominions 6/.claude | How mounted units work in Dominions 6: rider and mount, who gets hit, trample, fear, dismounting. |
| dom6-nations | Games/Fantasy Strategy/Dominions 6/.claude | Read Dominions 6 nations from the game's own nation info screens into one markdown and JSON file per nation. |
| dom6-path-air | Games/Fantasy Strategy/Dominions 6/.claude | The Air path of Dominions 6 magic: what air mages get by role, boosters, crosspaths and every generic air spell. |
| dom6-path-astral | Games/Fantasy Strategy/Dominions 6/.claude | The Astral path of Dominions 6 magic: what astral mages get by role, boosters, crosspaths and every generic astral spell. |
| dom6-path-death | Games/Fantasy Strategy/Dominions 6/.claude | The Death path of Dominions 6 magic: what death mages get by role, boosters, crosspaths and every generic death spell. |
| dom6-path-earth | Games/Fantasy Strategy/Dominions 6/.claude | The Earth path of Dominions 6 magic: what earth mages get by role, boosters, crosspaths and every generic earth spell. |
| dom6-path-fire | Games/Fantasy Strategy/Dominions 6/.claude | The Fire path of Dominions 6 magic: what fire mages get by role, boosters, crosspaths and every generic fire spell. |
| dom6-path-glamour | Games/Fantasy Strategy/Dominions 6/.claude | The Glamour path of Dominions 6 magic: what glamour mages get by role, boosters, crosspaths and every generic glamour spell. |
| dom6-path-nature | Games/Fantasy Strategy/Dominions 6/.claude | The Nature path of Dominions 6 magic: what nature mages get by role, boosters, crosspaths and every generic nature spell. |
| dom6-path-water | Games/Fantasy Strategy/Dominions 6/.claude | The Water path of Dominions 6 magic: what water mages get by role, boosters, crosspaths and every generic water spell. |
| dom6-play | Games/Fantasy Strategy/Dominions 6/.claude | How to play Dominions 6 well, from the manual: game setup, pretender, interface, a turn-by-turn checklist, expansion, war. |
| dom6-pretender | Games/Fantasy Strategy/Dominions 6/.claude | Design a Dominions 6 pretender god like the Pretenders Calculator and beyond: chassis, paths, dominion, scales, blesses, costs. |
| dom6-pretender-ingame | Games/Fantasy Strategy/Dominions 6/.claude | Build a designed pretender inside the running Dominions 6 (Game Tools > Create a Pretender God) and save it. |
| dom6-ranged-math | Games/Fantasy Strategy/Dominions 6/.claude | Precision and ranged combat math for Dominions 6: deviation, who gets hit, shields, arrow protection. |
| dom6-research | Games/Fantasy Strategy/Dominions 6/.claude | Magic research in Dominions 6: the seven schools, research points, queue, labs and speed. |
| dom6-rituals | Games/Fantasy Strategy/Dominions 6/.claude | Ritual magic in Dominions 6: lab casting, costs, remote attacks and defences, global enchantments. |
| dom6-scbm | Games/Fantasy Strategy/Dominions 6/.claude | Everything specific to the SCBM balance mod for Dominions 6, kept apart from vanilla: modded units, spells, items, numbers. |
| dom6-scouting | Games/Fantasy Strategy/Dominions 6/.claude | Scouting and intelligence in Dominions 6: what each source reveals, report freshness, scout placement, hiding. |
| dom6-sieges | Games/Fantasy Strategy/Dominions 6/.claude | Forts and sieges in Dominions 6: besieging, storming, relief forces, defence and fort stats. |
| dom6-site-search | Games/Fantasy Strategy/Dominions 6/.claude | Finding magic sites in Dominions 6: the search order, site levels, search rituals and gem income. |
| dom6-spell-db | Games/Fantasy Strategy/Dominions 6/.claude | Spell evaluation database for Dominions 6: every vanilla and SCBM spell sorted by purpose and ranked. |
| dom6-spells | Games/Fantasy Strategy/Dominions 6/.claude | Claude's complete reference to Dominions 6 combat spells: every spell from the inspector with path, school, range, effects and worth. |
| dom6-sprites | Games/Fantasy Strategy/Dominions 6/.claude | Make Dominions 6 unit sprites (TGA, black-transparent, facing left) by modelling 3D figures and rendering them cel-shaded. |
| dom6-stealth | Games/Fantasy Strategy/Dominions 6/.claude | Stealth, patrols and assassins in Dominions 6: sneaking, detection, patrol strength, assassination. |
| dom6-summoning | Games/Fantasy Strategy/Dominions 6/.claude | Summoning in Dominions 6: ritual and battle summons, per-gem value, path access, summon-based armies. |
| dom6-supercombatants | Games/Fantasy Strategy/Dominions 6/.claude | Building and beating Dominions 6 supercombatants and army-wiping cheese units: the five tank archetypes and their counters. |
| dom6-tactics | Games/Fantasy Strategy/Dominions 6/.claude | Laying out a Dominions 6 army for battle and what has worked: positions, formations, squad and commander orders, leadership, lessons. |
| dom6-thugs | Games/Fantasy Strategy/Dominions 6/.claude | Basic thugging in Dominions 6: what a thug is, kitting, buff scripts, raiding, army thugs vs solo. |
| dom6-tooltips | Games/Fantasy Strategy/Dominions 6/.claude | Reading the Dominions 6 interface through tooltips and exact pointing (centre of the text, not the icon). |
| dom6-ui | Games/Fantasy Strategy/Dominions 6/.claude | Drive the running Dominions 6 window through the game-ui guard: menus, game setup, mods, pretenders, hotkeys, font tools. |
| dom6-weapons | Games/Fantasy Strategy/Dominions 6/.claude | How weapons work in Dominions 6 melee: attack and damage rolls, weapon stats, length, multiple attacks, damage types. |
| dom6-wiki | Games/Fantasy Strategy/Dominions 6/.claude | Local mirror of illwiki (the Dominions community wiki, Dom6 and Dom5) with wiki.py to search and read it. |
| rtw3-guide | Games/Historical Strategy/Rule The Waves/.claude | Starter guide to Rule the Waves 3, the naval ship-design and fleet-command game (1890-1970). |
| dcss-guide | Games/Roguelikes/Dungeon Crawl Stone Soup/.claude | Guide to Dungeon Crawl Stone Soup (DCSS 0.34, flatpak): rules, species, gods, level design language. |
| quasimorph-guide | Games/Roguelikes/Quasimorph/.claude | Starter guide to Quasimorph, a dark sci-fi turn-based extraction roguelike (PMC, clones, wounds). |
| aurora-guide | Games/Space Strategy/Aurora 4x/.claude | Starter guide to Aurora 4X (C# 2.x), the deep sandbox space 4X: colonies, industry, ship and missile design, formulas. |
| efs-guide | Games/Space Strategy/Emperor of the Fading Suns/.claude | Starter guide to Emperor of the Fading Suns (1996), hex-based space and planetary strategy of feudal Houses. |
| se4-guide | Games/Space Strategy/Space Empires/Space Empires IV/.claude | Starter guide to Space Empires IV Deluxe, a space 4X: first turns, ship design, research, combat, screens. |
| se4-modding | Games/Space Strategy/Space Empires/Space Empires IV/.claude | Modding Space Empires IV Deluxe (v1.95): how mods load, the data files, checks, the WMD mod. |
| swr-guide | Games/Space Strategy/Star Wars Rebellion/.claude | Starter guide to Star Wars Rebellion (1998), galactic grand strategy of Alliance vs Empire: systems, support, characters, missions. |
| stars-guide | Games/Space Strategy/Stars!/.claude | Starter guide to Stars! |
| vgap-guide | Games/Space Strategy/VGA Planets Nu/.claude | Starter guide to VGA Planets Nu, the browser remake of the classic play-by-email space 4X. |
| coc-guide | Games/Tabletop RPGs/Call of Cthulhu/.claude | Starter guide to Call of Cthulhu 7th Edition (Chaosium): d100 skills, sanity, investigation, keeper advice. |
| greyhawk-lore | Games/Tabletop RPGs/Dungeons & Dragons/.claude | World of Greyhawk lore reference (the original D&D world): the Flanaess, its realms, rulers, peoples, places and wars. |
| faserip-guide | Games/Tabletop RPGs/FASERIP/.claude | Starter guide to Advanced FASERIP (free Marvel Super Heroes retro-clone): ranks, FEAT rolls, Karma, characters. |
| mnm-guide | Games/Tabletop RPGs/Mutants and Masterminds 3E/.claude | Starter guide to Mutants & Masterminds 3E: d20 checks, power level, point-buy powers, conditions. |
| paranoia-guide | Games/Tabletop RPGs/Paranoia/.claude | Starter guide to PARANOIA (Mongoose 2023), the comic RPG of Troubleshooters serving The Computer. |
| fftow-guide | Games/Tabletop Tactics/Fistful of TOWs/.claude | Starter guide to A Fistful of TOWs 3, miniatures rules for mechanized war 1930s-present: sequence, quality, fire, points. |
| eih-guide | Games/Tabletop Wargames/Empires in Harm/.claude | Starter guide to Empires in Harm (Empires in Arms successor), the 7-10 player Napoleonic strategic and diplomatic board wargame. |
| fe-guide | Games/Tabletop Wargames/Federation and Empire/.claude | Starter stub for Federation & Empire (ADB), the Star Fleet Universe strategic board wargame. |
| hellfire-guide | Games/Tabletop Wargames/Hellfire/.claude | Starter guide to Hellfire, a 6mm sci-fi miniatures wargame with a campaign system. |
| ocs-guide | Games/Tabletop Wargames/Operational Combat System/.claude | Starter guide to the Operational Combat Series v4.3: supply, modes, combat, air, the OCS games. |
| pog-guide | Games/Tabletop Wargames/Paths of Glory/.claude | Starter guide to Paths of Glory (GMT), the card-driven WWI board wargame. |
| thirdreich-guide | Games/Tabletop Wargames/Rise and Decline of the Third Reich/.claude | Starter guide to Rise and Decline of the Third Reich (Avalon Hill WWII grand strategy) with the fan 4.5 rules. |
| starfire-guide | Games/Tabletop Wargames/Solar Starfire/.claude | Starter guide to Solar Starfire (2013): tactical ship combat on hexes and the 4X campaign system. |
| sfb-guide | Games/Tabletop Wargames/Starfleet Battles Games/.claude | Starter guide to Star Fleet Battles (Captain's Edition): energy allocation, impulses, weapons, damage. |
| sfgc-guide | Games/Tabletop Wargames/Starfleet Battles Games/Starfleet Galactic Conquest/.claude | Starter guide to Star Fleet Universe Galactic Conquest (5C), a GM-run strategic campaign system. |
| uscw-guide | Games/Tabletop Wargames/The US Civil War/.claude | Guide to GMT's The U.S. |
| toc-guide | Games/Tabletop Wargames/Triumph of Chaos/.claude | Starter guide to Triumph of Chaos v2 Deluxe, the card-driven Russian Civil War board wargame. |
| vbam-guide | Games/Tabletop Wargames/Victory by Any Means/.claude | Starter guide to Victory by Any Means 2E, a generic tabletop space-empire campaign system. |
| ww1dx-guide | Games/Tabletop Wargames/World War 1 Deluxe Edition/.claude | Starter guide to World War I Deluxe (Decision Games 2018), a two-player hex wargame of the Great War. |
| atg-guide | Games/Wargames/Advanced Tactics Gold/.claude | Starter guide to Advanced Tactics Gold, a hex wargame engine and construction set with random 4X-style games. |
| giren-guide | Games/Wargames/Gihren's Greed/.claude | Starter guide to Gihren's Greed (Gundam Giren no Yabou grand strategy), with Japanese screen reading. |
| hos-guide | Games/Wargames/Hex of Steel/.claude | Starter guide to Hex of Steel, a WWII-and-beyond hex wargame in the Panzer General tradition. |
| toaw4-guide | Games/Wargames/The Operational Art of War IV/.claude | Starter guide to The Operational Art of War IV, operational hex wargame and scenario editor. |
| witp-guide | Games/Wargames/War in the Pacific/.claude | Starter guide to War in the Pacific Admiral's Edition, the grand-scale WWII Pacific wargame. |
| military-theory | Military Theory/.claude | The user's military theory shelf as searchable text, with his essay on space warfare and the classics. |
