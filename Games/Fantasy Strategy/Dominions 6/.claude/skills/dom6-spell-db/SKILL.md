---
name: dom6-spell-db
description: "Spell evaluation database for Dominions 6: every vanilla and SCBM spell sorted by purpose and ranked. Use when ranking or choosing spells for a purpose or comparing vanilla with a mod."
keywords: "combat, ritual, generic, national, army, damage, single-target, group, self, buff, debuff, fear, battlefield, enchantment, battle, summon, units, commanders, site, search, remote, attack, global, province, movement, logistics, healing, economy, utility, inside, tier, s-d, value, cost-efficiency, simulated, kills, cast, melee, trades, summons, weighted, effect, coverage, buffs, debuffs"
---

# Spell evaluation database (dom6-spell-db)

The user (2026-11-03): "just rank all the spells and make a spell evaluation database. There might be spells you
didn't catch, just do it." Also his ask for "lists on what's good in vanilla generally for each purpose".
The method for any game, and a generic builder: game-database.

## Files
- `scripts/spelldb.py` - build and query (docstring has every command).
- `data/<label>/spells.sqlite` and `spells.csv` - the database (table `spells`); labels `vanilla`, `scbm`.
- `<label>/INDEX.md` and one page per purpose (`<label>/army-damage.md`, `group-buff.md`...): generic spells
  first, then national ones, each with rank, tier, value, efficiency, my curated tier and detail.

## Queries
```
python3 -I scripts/spelldb.py purposes [--label scbm]
python3 -I scripts/spelldb.py top "army buff" --paths N2G2H2 [--nation "Tir na"] [--max-level 6] [--label scbm]
python3 -I scripts/spelldb.py spell "Destruction" --label scbm
python3 -I scripts/spelldb.py sql "SELECT name, tier, value FROM spells WHERE purpose='debuff' AND path LIKE 'E%'"
```
`--paths` alone shows generic spells only; add `--nation` for that nation's own spells. Rebuild after a mod
update: `spelldb.py build --data <modinspector folder> --label <mod>` (~5 minutes; `-n` = casts simulated).

## How much to trust a number
- **simulated** (damage, summons): real DRN, shields, MR, AP/AN, at the REQUIRED path level, against packed
  Militia, sword Heavy Infantry and Barbarians (living men). Undead-only or demon-only spells (Banishment,
  Solar Rays) score 0 here - they're anti-undead tools, judge them separately. Summons: enemy heavy infantry
  killed in melee before dying (no ranged, no spells, no morale).
- **weights** (buffs, debuffs, battlefield): keyword weights x men covered x MR landing chance (0.45 for MR
  spells, 0.3 for sacred-only buffs). A ranking within the purpose, not a measurement. Divine spells cost no
  fatigue in the data, so their efficiency is inflated.
- **cost** (most rituals): ranked by level and gems only - read the effect and the curated tier.
- **curated**: my earlier hand tiers (dom6-spells pages, judged for Pythium-era play) - trust them over the
  automatic tier when they disagree, and check with the calculator (spells.py melee/missile) for buffs.
- Tiers are percentiles inside a purpose: an "S" debuff and an "S" summon aren't comparable.

## Related skills
dom6-spells (calculator, curated rankings), dom6-mod-magic (what a mod changed), dom6-scbm, dom6-buffs,
dom6-evocations, dom6-summoning, dom6-rituals, dom6-research.
