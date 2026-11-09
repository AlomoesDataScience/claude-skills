---
name: dom6-communions
description: "Communions in Dominions 6: astral Communion, blood Sabbath, master and slave scripting, path boosts and fatigue. Use when planning a communion mage line or reading a battle where one broke."
keywords: "manual, illwiki, thaumaturgy, man's, chorus, master's, boost, levels, has, slaves, spell, including, encumbrance, split, among, participants, multiplied, weaker, being, helpless, sharing, self-buffs, backlash, masters, die, flee, 3d50, round, stunned, items, crystal, matrix, slave's, heart, athame, damage, grand, globals, around, judging, whether, may, pass, mentions"
---

# Communions (Dominions 6, vanilla)

The user (2026-11-03): "fatigue and communions need their own skills." His fatigue rule: passing out is fine
"unless you're in a communion, then it's iffy". Sources: manual pp.77-79, illwiki `communion.txt` (wiki =
lower truth). Fatigue basics: dom6-fatigue.

## The spells
- **Communion Master** and **Communion Slave**: Thaumaturgy 1, Astral 1, 20 fatigue each (inspector). Both
  must be in effect: no master or no slaves = no communion (p.78). SCBM 1.13: both `ainocast` - the AI never
  casts them on its own; script them (dom6-scbm).
- **Sabbath** (blood): same, costs blood slaves; wiki: masters take 50% less fatigue, slaves 25% more.
  **Chorus**: MA Man's spellsingers only; a chorus slave who passes out leaves it safely (p.79).
- One communion of each type can be active at once, each with its own members (p.79).
- Items join their bearer automatically without casting (bearer must be a mage, any path but Holy):
  Crystal Matrix, Slave Matrix, Slave's Heart, Master's Athame (p.79).
- Wiki: masters' spells take 25% longer to cast in an astral communion.

## Path boost (p.78)
Each master gains +n levels in EVERY path he already has (at least 1) for 2^n slaves: 2 slaves +1, 4 +2,
8 +3, 16 +4. It drops as soon as the slave count falls under the threshold. The boost counts for overcasting
(area, penetration, fatigue cut) - a cheap way to reach a spell one level up without gems.

## Fatigue sharing (p.78; wiki adds encumbrance)
- Participants of one cast = the master casting + all friendly slaves on the field. Each takes the spell's cost
  (wiki: including the master's spellcasting encumbrance) / participants.
- Per slave, by level in the spell's primary path vs the master's (levels from the communion itself are not
  counted for this, wiki): slave higher = /2; equal = x1; lower = x2; lower than half the master = x4.
  So gems on the master cut HIS share but raise the slaves' multiplier (wiki's Time Stop example).
- Wiki: minimum 1 fatigue per slave per cast; a slave pushed past 200 always takes 1 HP (inside the head),
  the normal formula past 250.

## Slaves are helpless (p.78-79)
- Slaves can do nothing else while in the communion; they do get the master's self-buffs (range 0, single
  target): one Reinvigoration or Mistform on the master lands on every slave too.
- The communion ends when all masters or all slaves are gone. If the MASTERS die or flee, every slave is
  stunned about a round and takes 3d50 fatigue (wiki: ~75 on average, 3-150) - many fall unconscious.

## Why passing out is "iffy" here (the user)
- **Unconscious slaves stay in the communion** (the user, 2026-11-03, from play; manual and wiki are silent - only
  Chorus slaves leave when out, p.79): his share keeps landing on him; past 200 it becomes HP damage - long gem-heavy fights can kill
  slaves. An unconscious master still holds the communion together but casts nothing.
- So: few big casts = fine; many casts over a long battle = watch slave fatigue, add slaves, use
  Reinvigoration on the master, or keep the master's gems for his share only.

## Grand Communion (p.78)
Not a battle communion: commanders with the Grand Communion ability use the order of that name in the
province where a global is cast; their skill in the global's path adds to the casting / dispel strength.

## Tir na n'Og (SCBM game)
No native astral mages; a communion needs S1 mages (random paths) or the communion items. Research had
Thaumaturgy 1 queued (2026-11-03). Notes: dom6-scbm `tirnanog.md`.

## Related skills
dom6-fatigue, dom6-gem-casting, dom6-spells, dom6-items (the matrix items), dom6-mechanics, dom6-scbm.
