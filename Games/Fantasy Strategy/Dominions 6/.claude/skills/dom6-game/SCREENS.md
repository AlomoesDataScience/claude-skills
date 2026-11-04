# Dominions 6 screens - reference (moved out of dom6-game SKILL.md, 2026-11-03)
Measured on the 1920x1044 desktop: on the 1912x1000 virtual screen find positions by OCR (dom6-ui).

## The province panel (right side), item by item (Pythium, 2026-10-27)

Left-click each line (middle of its text). Hovering gives a tooltip at the bottom (it follows the
mouse sideways on the map). Popups close with their Exit.

| Line | Click | Tooltip / what it says |
|---|---|---|
| Name (number) | nothing | none |
| Terrain | nothing | terrain effects, e.g. "Plains, Mountains (low income, excellent resources, more magic sites)" |
| Population | popup: growth breakdown | capital "ideal size for about 25000"; base growth 0.2%, density −0.2%, terrain −0.1% → −0.1% |
| Income | nothing | gold per month for this province |
| Resources | nothing | needed for metal armaments of units and commanders; local, not saved between months |
| Recruitment points `519 / 2` | nothing | units / commanders recruitable per month here |
| Supplies, Supply usage | nothing | one human-sized unit eats one supply; starvation if usage exceeds supplies |
| Defence `25+/-` | the **d** screen: gold left, defence level, unrest reduction/month, patrol strength, a picture of the Defence Units | (don't buy defence casually: it costs gold) |
| Unrest | nothing | unrest cuts tax; 100+ blocks recruiting |
| Dominion candle / scale icons | popup: dominion strength here and every scale's effect (Order 3: income +9%, resources +9%, events −6%, unrest −3, recruitment +30%; Productivity 2: income +6%, resources +30%; Magic 1: research +1 RP) | each scale icon's tooltip names it ("Order: 3") |
| Fortification | the **f** screen (fort stats) | "(f) Fort statistics" |
| Laboratory | nothing | none |
| Temple | the **o** screen (dominion stats, bless effect) | |
| A magic site (e.g. Cathedral of the Spheres) | popup "Magic Site Effects": recruits it enables, gems it produces | Cathedral: Arch Theurg, Battle Vestal; 5 astral, 2 air, 1 water a month. Swamps of Pythia: Hydra Hatchling, Hydra, Hydra Tamer |

- **Other provinces** (right-click, turn 1). An unseen province (Azimar, Fucan, Nom, Ashenton,
  Copper Woods, Saetica, Duvan, Clon) shows only its name (number), terrain and empty Dominion
  and Buildings & Sites headers. Helmshire (287), which has my dominion candle (one of the two
  converted provinces), also shows population, income, resources, recruitment points and supply
  usage, with Supplies "?". No defence, unrest, sites or armies. The commander column is empty
  unless my commanders are there. The yellow dotted lines go from the viewed province to its
  neighbours. Pythium shows only a red-and-yellow line toward Nom: probably the snowed-in pass
  (not checked).
- Province labels sit near the borders: right-clicking open land can hit the province behind it
  (a click north of Helmshire got Duvan). Check the panel title after each click.
- `probe.tooltip` finds the tooltip's frame, but the map shows through it and can hide the frame.
  If it returns "", OCR the band `(0, 940, 1590, 1044)` and drop the junk before the sentence.

## Recruit screen (`r`, or the second top-bar icon) — per province

Armies and recruiting are province-dependent: the screen recruits in the viewed province
("Recruitment in Pythium"). Two portrait grids: Commanders, then Units, each with an empty queue
strip under it and a "repeat recruitment" checkbox. Bottom: Gold, Resources, Commander Points,
Recruitment Points, Holy Points (sacred units), Reset recruitment, Exit. Hover a portrait for
"Name (gold, resources, commander/recruitment points[, max 1/month])"; a left-click would queue it.
Left-click a portrait = queue one (it appears in the strip below); **click a queued unit to
remove it**. "repeat recruitment" (click the words) keeps that list's queue for following
turns. Sacred recruits use Holy Points (the Theurg took 1). Check the bottom counters after.
Pythium turn 1 (full-screen hover points, commanders y 160/238, units y 475/556):
commanders Scout 35g, Assassin 80, Centurion 95, Legatus Legionis 150 (2 CP), Emerald Lord 125,
Serpent Lord 100, Battle Deacon 90, Theurg Acolyte 100 (2 CP), Theurg 300 (2 CP), Hydra Tamer 35,
Arch Theurg 565 (4 CP); units Slinger 7g/2r/3rp, Velite 10/10/9, Alae Legionnaire 10/20/9,
Hastatus 11/21/12, Principe 14/21/20, Triarius 15/29/25, Emerald Guard 20/30/31, Standard
20/21/21, Serpent Cataphract 45/41/41, Retiarius 10/1/9, Gladiator 10/1/9, Theurg Communicant
50/1/31 (1/month), Battle Vestal 15/4/14, Hydra Hatchling 35/1/15, Hydra 200/1/50 (1/month).

## Research (F5)

"Magic Research": Magic Schools (level, progress bar, RP left per school), Research speed, then
the Research Queue. **Click a school's name to queue its next level**; clicking again queues the
level after. **Click a queue entry to remove it** (remove from the bottom up, then click the
schools in the new order; the queue's entries are ~32 px apart from y≈484). The queue holds
**at most 9 entries** (the user). Research only happens with mages
on the Research order (space menu); turn 1 Pythium has none, so speed 0. School name points
(full screen): Conjuration (651, 168), Alteration (641, 204), Evocation (646, 234), Construction
(658, 264), Enchantment (661, 296), Thaumaturgy (659, 327); Blood Magic below.

## Mercenaries (`b`, third top-bar icon)

"Hire Mercenaries": Company name, Price (minimum), Employer, Bid, Land. Click `<bid>` (the word):
a dialog "X demands at least N gold", `- N +` (+ at about (1025, 440), steps of 1), Hire, Cancel.
After Hire the row shows your bid and the landing province. The bid is **charged once** (the
user), for a 3-month contract; highest bidder wins; when it runs out the old employer's bid
counts double that one turn (manual p. 29). Turn 1: bid 66 for Dagan, the Renegade Sage (Sage,
S1, adept researcher 8), landing in Pythium.

## Other top-bar screens (turn 1)

- Send Messages (`s`): a "Send Message" list: text message, gold, magic gems, blood slaves, magic
  item, diplomatic missive. Exit.
- F1 Nation Overview: one row per province (Inc., Unr., Res., Sup., S.U., Def., Sites icons,
  Searches) with its commanders and their orders underneath ("Theocratus Defend, commanding
  45 units"; "Latinus Sneak to Azimar (263)"), then "Sneaking commanders".
- F2 Score graphs: a row of nation banners to toggle, tabs Provinces, Forts, Income, Gem inc.,
  Blood inc., Research, Dominion, Army Size, Ascension Points; empty on turn 1.
- F3 Hall of Fame: Name, Nation, Kills, Exp.; empty on turn 1.
- F4 Pretenders of the World: Name (with nation banner), Relation, Controller (AI/Human),
  Blessing ("known" for my own). Scrolls (wheel). **Hover the name word** (not right of it)
  for "Nation info for X" at the bottom (low rows' tips can hide under the Exit); click the name
  for the nation info screen (description, National Features, recruits, sites, and "X worships
  the pretender NAME, TITLES": the titles hint at the god's build). Long info screens put Ok
  below the fold: scroll the wheel to reach it. Game 1 map: dom6-knowledge play/game1-pretenders.

## Menus seen (open by hotkey; close with the menu's Exit - Esc on the map opens Options)

- F1 Nation Overview: provinces table (income, unrest, resources, supply, defence, sites,
  searches) and commanders with their orders.
- F2 Score Graphs: army size, provinces, ascension points, income, gem income, research...
- F4 Pretenders: every god, relation, controller (AI/Human), blessing.
- F5 Research: per school level and RP left, research speed, research queue.
- F9 Thrones: required ascension points and every throne with its points (the list scrolls).
  **Left-click a throne's name** for its effects: the unclaimed site effect, then "The throne must
  be claimed to gain the following effects" (ascension points, dominion spread, gems, gold,
  recruits, blesses). Exit closes it; closing it can shift the list, so re-read row positions
  after each popup. Game 1's list: dom6-knowledge play/game1-thrones.md.
- r Recruit: commanders and units lists, commander points, gold, holy points, recruitment
  points, resources, repeat recruitment, reset.
- d Recruit Defence: gold left, unrest reduction, patrol strength.
- f Fort info: administration, commander point bonus, recruitment point bonus, guards.
- o Temple and dominion: temples, converted provinces, dominion strength, spread chance, bless
  effects.
- i Province chronicle: description and events (e.g. a snowed-in mountain pass).
- b Mercenaries: companies, employer, price, bid.


