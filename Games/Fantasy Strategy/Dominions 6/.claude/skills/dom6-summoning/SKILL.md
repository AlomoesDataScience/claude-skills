---
name: dom6-summoning
description: Summoning in Dominions 6, from the manual (pp. 73-74, 82 alchemy, turn steps 10 and 36) and illwiki (conjuration, construction, mage-summons) - ritual summons (cast in a lab, gems, arrive in the province), battle summons (combat spells; gone after the battle), constructs from Construction, mage summons that bring new paths, overcasting for more units (+N per level), leadership needs (magic, undead leadership; mindless), upkeep-free monsters, judging value per gem (dom6-spells summons), and alchemy to fund them. Use when choosing summons, comparing summons per gem, planning a summon-based army or path access, or when the user asks about summoning.
---

# Summoning (Dominions 6, vanilla)

The user's list (2026-11-03). Manual pp.73-74 (Conjuration and Construction make units), 82 (alchemy);
illwiki `conjuration`, `construction`, `mage-summons`. Value tables: dom6-spells (`spells.py summons`).

## Kinds
- **Ritual summons**: cast at a lab (dom6-rituals); units appear in that province. Many scale with extra
  levels ("x5 (+0.5 per level)", wiki tables). Mostly Conjuration, also Construction (constructs: Clockwork
  Soldiers, Mandragora, Golem), Blood (bind demons), Enchantment (Hidden in Snow).
- **Battle summons**: combat spells; the units vanish after the battle. Count for little in army HP (rout,
  dom6-morale). Good for screening and soaking.
- **Mage summons**: units with paths your nation lacks (wiki mage-summons table) - the main way to get new
  paths besides empowerment, indies and sites.

## Keeping them
- Leadership: magic beings need magic leadership, undead and demons undead leadership, or they rout
  (dom6-morale). Mindless dissolve without a commander that can lead them.
- Most summons cost no gold upkeep - gems instead of gold.
- Commanders summoned (Golem, Shadow Imp, Unfrozen Mage) give you more casters/thugs.

## Choosing
- Units per gem and what they kill before dying: `spells.py summons` (per gem).
- Fit the job: chaff for screens and patrol (cheap and many), elite fighters, fliers for raids, mages.
- Turn order: ritual summons arrive at step 10 in the lab province, before movement and battles - they can
  defend that province this turn but had no orders to move. Special-order summons (Summon Allies, Reanimate)
  come at step 36, after the battles (p.56).

## Funding
Alchemy (p.82): any mage in a lab converts gems 2:1 to astral pearls or pearls to any gem (4:1 the long way);
Earth/Fire alteration rituals turn gems into gold.

## Related skills
dom6-rituals, dom6-spells, dom6-gem-casting, dom6-research, dom6-morale, dom6-blood, dom6-mechanics.
