---
name: gearcity-guide
description: "Starter guide to GearCity, the car-industry business sim: component design, factories, markets. Use when playing, learning or modding GearCity, or borrowing its design and market systems for our 4X engine."
keywords: "visual, entertainment, technologies, automobile-industry, simulation, onward, designing, chassis, engines, gearboxes, vehicles, dated, sub-components, branches, districts, sales, pricing, marketing, contracts, racing, stocks, financing, unions, taxes, lobbying, war, popularity, plus, components, xml, scripts, media, maps, modtools, suite, editors, cities, events, points, official, dokuwiki, manual, wiki, info, local"
---

# GearCity - starter guide

Status 2026-11-01: installed (Steam, Linux native: `~/.local/share/Steam/steamapps/common/GearCity/`,
4.9 GB). Wiki contents read; component data read. Not played. Read only: don't edit the install.

## Sources

- Official wiki manual: https://wiki.gearcity.info/doku.php?id=start (the user's link). Read pages
  with WebFetch, e.g. `...doku.php?id=gamemanual:gm_engines_design`. Main parts: Game Manual
  (GUI, tutorials: body designer, designing a successful vehicle, pricing, supply and demand,
  marques, trims, new generations, design skills, outsourcing and platform sharing, stocks,
  contracts, districting, auto production, financing, benefits), **Game Mechanics** (chassis,
  engines, gearboxes, vehicles, factories, branches, sales, marketing, contracts, racing,
  stocks, pensions, unions, war, skills and image, taxes, lobbying, penalties, popularity, city
  variables), Troubleshooting, **Modding** (`modtools:overview`, file locations, editors).
- Install: `media/Scripts/Components.xml` (all sub-components), `ComponentStartingPopularity.xml`,
  `EngineContracts.xml`, newspaper/news XML per language, `media/Maps/<map>/MapFileForGame.xml`,
  `media/PredesignedCars`, `ModTools/` (Qt mod tool suite: `launchMT.sh`), `media/Mods`.

## How components work (from Components.xml)

Each sub-component (frame types, suspension, drivetrain, engine layout, cylinders, fuel, valves,
induction, gearbox gears and add-ons, 643 car body types, 179 accessories) has an **introduction
year and a death year**, multipliers for strength, performance, safety, durability, weight, design
cost, manufacturing cost and cost, a **skill** requirement, and a popularity index. A vehicle
design picks a chassis (frame + suspension + drivetrain), an engine and a gearbox, then sliders
for how effort is spent; quality depends on the company's design skills, and buyers in each city
weigh the ratings by vehicle type.

## For our 4X engine

This is the model the user points to for "Component Design": dated technologies that appear and fade,
components designed from sub-components with multipliers, design skill as accumulated human
capital, a market of buyers with preferences per region, plus stocks, financing, unions and
lobbying (his Finance and Economics docs). Plain XML data + an editor suite fits his
"png + text" modding goal.
