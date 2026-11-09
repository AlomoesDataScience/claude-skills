---
name: greyhawk-lore
description: "World of Greyhawk lore reference (the original D&D world): the Flanaess, its realms, rulers, peoples, places and wars. Use when Greyhawk or Oerth comes up or a D&D campaign or map needs lore."
keywords: "dungeons, dragons, gary, gygax, regions, ruler, capital, towns, population, faiths, allies, enemies, resources, wiki's, fact, boxes, human, big, history, twin, cataclysms, great, migrations, kingdom, iuz, climate, lookup, script, over, local, copy, greyhawkonline, wiki, pages, realm, page, search, list, adventure, set, turned, game, nation, dom6-maps, image"
---

# World of Greyhawk - lore reference

Status 2026-10-29: the wiki's Flanaess page and 143 linked pages (realms, regions, seas, forests,
hills, peoples) are in `Worlds/Greyhawk/lore/` (fetched through the Wayback Machine; 33 linked
pages had no archive copy, listed in `pages.txt`). Maps in `Worlds/Greyhawk/maps/`. The lore text
is the wiki's: summarise it in your own words, never paste it into a game or document.

Other D&D worlds (Forgotten Realms, Eberron, Dark Sun, ...) come later, each as its own
`Worlds/<world>/` folder and `<world>-lore` skill next to this one.

## Look it up

```
scripts/lore.py realm furyondy            fact box: ruler, government, capital, towns, population,
                                          races, languages, religions, allies, enemies, resources
scripts/lore.py page "Shield Lands"       article text (history, geography)
scripts/lore.py search "Rain of Colorless Fire"   lines across all pages, with the page
scripts/lore.py list --region "Sheldomar" realms of one region with capital and population
scripts/lore.py table realms.md           rebuild the realm table (already here: realms.md)
```

Facts are dated (most fact boxes 576-591 CY; the wiki mixes 1983 boxed set, Greyhawk Wars and
Living Greyhawk eras): say which year a fact is from when it matters. A few realms share one page
(Blackmoor's box is Arn's) - check the page if a box looks wrong.

## The setting in brief (Claude's summary)

**Place.** Oerth is the world; Oerik its main continent; the **Flanaess** is Oerik's eastern part,
named after the Flan, its first human people. The calendar counts Common Years (CY); the classic
"now" is 576 CY, the later one 591 CY after the wars.

**Peoples.** Six human stocks: Flan (natives), Oeridians (the main conquering stock, most
kingdoms), Suloise (Suel, fair-haired, survivors of a fallen empire), Baklunish (the west), Olman
(southern jungles), Rhennee (river and lake folk), plus the Touv of Hepmonaland. Elves, dwarves,
gnomes and halflings are strong in the Sheldomar Valley, Celene, the Ulek states and the Lortmils;
orcs and goblinoids hold the Pomarj, the Bone March and much of the north.

**Deep history.** Roughly a thousand years before CY, the Suel Imperium and the Baklunish Empire
destroyed each other with magic (the **Twin Cataclysms**: the Rain of Colorless Fire turned the
Suel lands into the **Sea of Dust**; the Invoked Devastation broke the Baklunish). The **Great
Migrations** pushed Oeridians and Suel east into the Flanaess, over the Flan. The Oeridian Aerdi
founded the **Great Kingdom** (Aerdy), whose calendar, Common tongue and coinage the whole region
still uses; it ruled from Rauxes and shed provinces over the centuries (Ferrond/Furyondy and
Veluna 254 CY, Nyrond later), sinking into decadence under the House of Naelax.

**The Greyhawk Wars (582-584 CY)** reshaped the map: the demigod **Iuz** (the Old One) swallowed
the Horned Society, the Bandit Kingdoms and the Shield Lands; the orc warlord Turrosh Mak took the
Pomarj and the southern Wild Coast; the **Scarlet Brotherhood** (Suel supremacist monks of the
Tilvanot Peninsula) seized Onnwal, Idee and the southern coasts by murder and coup; giants overran
Geoff and Sterich; the Great Kingdom broke apart (Ivid's empire fell 586 CY; North Kingdom,
Ahlissa and others followed). The Pact of Greyhawk ended the war in the **Free City of
Greyhawk**, the trade and adventuring hub on the Nyr Dyv and the Selintan, with Castle Greyhawk's
ruins nearby.

## Regions (the wiki's own grouping)

- **Sheldomar Valley ("Old Keoland")**, south-west, warm and fertile between the Crystalmists and
  the Lortmils: Keoland (oldest continuous realm), the Ulek states, Gran March, Bissel, Geoff,
  Sterich, Yeomanry, Hold of the Sea Princes; demihumans common.
- **Central Flanaess / "Old Ferrond"**, Nyr Dyv to the Yatils, long the heart of good: Domain of
  Greyhawk, Furyondy, Veluna, Shield Lands, Perrenland, Celene (elves), the Wild Coast.
- **Northern Reaches**: Iuz's empire north of Lake Whyestil, the Vesve, Bandit Kingdoms, ruins
  and orc lairs; cool climate.
- **Old Aerdy East**: former Great Kingdom heartland between the Rakers, the Vast Swamp and the
  Solnor: North Kingdom, Ahlissa, Bone March, Sunndi, Almor, Ratik, Sea Barons, Lordship of the Isles.
- **Old Aerdy West / "Old Nyrond"**, temperate and fertile: Nyrond, the Urnst states, Tenh,
  Theocracy of the Pale.
- **Bitter North ("Old Blackmoor")**: cold steppe and pine forest, nomads and goblinoids (Arn,
  Chakyik, Wegwiur, Blackmoor). **Thillonrian Peninsula**: Suel barbarian kingdoms of fjords and
  mountains (Fruztii, Cruski, Schnai).
- **Baklunish West**, cut off by the Yatils, Barrier Peaks and Crystalmists: Ket, Tusmit, Zeif,
  Ekbir, Ull, the Paynim and Tiger and Wolf nomads.
- **Edges**: the Sea of Dust (ash waste, former Suel lands), the Amedio Jungle and Hepmonaland
  (tropical, Olman ruins).

**Climate**: freezing only in midwinter outside the far north; summers long (five months or more);
winter and autumn winds from the north-east, the rest of the year from the south-east.

## Uses here

- Dominions map from the Greyhawk HD picture: `Games/Fantasy Strategy/Dominions 6/Maps/mapgen/from_image.py`
  has a LORE table (realm → climate, terrain flags) and SITE_FEATURES (classic modules mapped to
  Dominions sites) still to fill; take realm facts from `realms.md` and `lore.py realm`.
- D&D play: realm fact boxes give rulers, enemies and resources for adventure hooks.
