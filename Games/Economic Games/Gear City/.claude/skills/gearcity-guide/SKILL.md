---
name: gearcity-guide
description: Starter guide to GearCity (Visual Entertainment and Technologies), the automobile-industry business simulation from 1900 onward - designing chassis, engines, gearboxes and vehicles from dated sub-components, factories, branches and districts, sales, pricing, marketing, contracts, racing, stocks and financing, unions, taxes, lobbying, war, popularity - plus its modding (Components.xml and other XML scripts in media/Scripts, maps, the Qt ModTools suite with editors for AI, cities, components, events). Points to the official DokuWiki manual (wiki.gearcity.info) and the local install. Uses learn-a-game (method), game-ui (the game window). Use when the user wants to play, learn, mod or talk about GearCity, or study its component-design and market systems for our own 4X engine (the user's Component Design doc names GearCity).
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
