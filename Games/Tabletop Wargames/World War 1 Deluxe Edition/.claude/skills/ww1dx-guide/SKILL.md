---
name: ww1dx-guide
description: Starter guide to World War I Deluxe Edition (Decision Games 2018, after Jim Dunnigan's SPI classic; design Joseph Miranda), a two-player hex board wargame of the Great War in Europe and the Middle East at 36 miles a hex and six months a turn - initiative from mobilization points, three impulses with front activation by plan markers, entrenched/mobile unit status, supply and lines of communication, ZOC, loss-point combat, mobilization points to build and absorb losses, campaign markers, neutrals, collapse and surrender, victory points, with a page map of BX-U_WorldWarI-Rules_V6F-ERULES.pdf (32 pages; searchable .txt). Uses game-sources (rulebook lookups), learn-to-play (method). Use when the user wants to play, learn, set up or talk about World War I Deluxe / Decision Games' World War I, or wants a rules question answered or a move planned.
---

# World War I Deluxe Edition - starter guide

Status 2026-10-29: the 2018 rules booklet read in contents, introduction, scale, sequence of play
and victory. Not played yet. Compare with the card-driven WWI games here (pog-guide, toc-guide):
this one is a hex-and-counter game run on mobilization points instead of cards.

Files: `BX-U_WorldWarI-Rules_V6F-ERULES.pdf` and `.txt` (PDF page = booklet page; the contents
on p2 is in three columns, so `manual.py grep ... "^ *10\.[0-9]"` finds the rule itself). Red text
in the PDF marks errata and exceptions, blue marks examples.

## What it is (Claude's summary)

Ten turns cover 1914-1918 (Summer and Winter turns of six months; turn one is August-October
1914), plus short scenarios (the opening, the final battles) and a 1919 option. Units are field
armies (60-120 000 men) and some corps, double-sided: mobile on the front, **entrenched** on the
back. **Mobilization points** (MP) are the economy: they build units, absorb combat losses and buy
campaign markers, and shrink as the war wears on. The map has three fronts (Western, Eastern with
the Balkans, Middle East).

## Turn (3.0, p5; expanded sequence on p32)

- **Initiative** each turn to the side whose major powers have more MP combined (CP wins ties);
  the initiative player goes first.
- Up to **three impulses**: in each, the initiative player moves then attacks, then the other
  player does. Every front is active in the first impulse; in the second and third a **plan
  marker** must be spent per front activated. Units on an inactive front only defend; crossing a
  front boundary needs both fronts active.
- Combat (8.0) is resolved in **loss points** taken by both sides (9.0), paid from units or MP;
  assault tactics, infiltration and no man's land are optional additions.

## Winning (3.4, p5)

Victory points through the game: the Allies 7 per turn the blockade holds, the CP 5 per turn it
doesn't; points for enemy violations of neutrality (Belgium 10, Italy 15, Ottoman Empire 15, ...);
for each enemy power's surrender, much more the earlier it happens (major power 100 in 1914 down to
20 in 1918). At the end: points per occupied enemy mobilization, objective and resource hex,
capital, and collapsed power (a unit must stand in the hex, control is not enough).

## Rule map (sections, booklet pages)

Components 2.0 p3; sequence of play 3.0 p5; unit status 4.0 p6; supply and LOC 5.0; ZOC 6.0;
movement 7.0 (rail, terrain); combat 8.0 p8; combat losses 9.0; mobilization 10.0 p12;
fortifications 11.0; campaign markers 12.0; neutrals 13.0 (diplomacy, invasion, US entry); naval
movement 14.0; transit areas 15.0; special units 16.0; assault tactics 17.0; collapse and
surrender 18.0; optional rules 19.0-27.0 (MP transfer, Russian civil war, depots, infiltration,
no man's land, construction, insurgents); scenarios 28.0.

## To learn next

1. Read 8.0-10.0 (combat, losses, mobilization) in full and summarise the CRT logic here.
2. Set up the short opening scenario with the user (the centre pages hold an 11x17 set-up map).
