---
name: ww2-armour
description: "WW2 armour and anti-tank fire: penetration tables and their criteria, armour profiles by angle, the lab hit rule, and our equipment.json. Use when judging whether a WW2 gun kills a tank, or filling or checking equipment data."
keywords: "penetration, armour penetration, armor, rha, slope, compound angle, presented area, hit location, tiger, panther, t-34, kv-1, su-76, t-60, stug, elefant, ferdinand, pak 40, zis-3, 45 mm, 76 mm, 88 mm, apcbc, apcr, heat, de marre, equipment.json, penmm, crit, 50 percent criterion, 75 percent criterion, tank kill, knocked out"
---

# WW2 armour - will this shot kill that tank

**Origin:** the Kursk tactics lab (the user 2026-11-16: kills come from stats, not scripted rules). The design is in
`Kursk 1943.md` §6 (vehicle model, armour profile, how a squad kills a tank). The data is in
`kursk/equipment.json`.

## The method
1. **Check the criterion before comparing numbers.** Penetration figures mix test standards: plate at 30° or
   at 90°, and a 50% (US/UK) or a 75% (Soviet) success rate. equipment.json keeps `penMm` per ammunition and
   range, with a `crit` field for the standard. Never compare two figures with different `crit` values
   without converting them, and note the conversion.
2. **Find the plate hit.** Hit location is chosen by presented area from the shooter's angle and height. The
   effective thickness comes from the compound angle (slope and side angle), the armour profile in §6. The
   top plates matter for air attack and for close-combat charges.
3. **Lab rule:** P(penetrate) = Φ((pen − eff) / (0.08 · pen)), the 8% spread. A penetration is not a kill.
   Roll crew, ammunition, fire and mobility effects from the vehicle model (crew seats, states).
4. **Gate-2 check** (`Kursk pass targets.md`): every kill must trace to a shot the table allows, or to a
   non-penetrating cause. The test case: no 45 mm front kill on a Tiger I at combat range.
5. **Convert to the unified toughness scale** (the user 2026-11-16: "1 unified armor toughness", which our own
   designs then change). Protection = thickness × material toughness, in RHA-equivalent mm, so a historical
   plate and one of our designed plates are compared the same way (`Kursk 1943.md` §10).
6. Ammunition matters: APCR and HEAT were scarce and issued per gun, so they are counted, not unlimited.

## Status / open
- equipment.json has nulls, which Kursk plan step 5 fills (KV-1, SU-76, T-60, RPG-43, Hafthohlladung, mines,
  aircraft, Flak). StuG and Panther armour detail and the formula leads (de Marre and others) are in §10.
- Fails when: one source's figure is used for every range and angle. Mark any figure that was read off one
  chart and stretched to other ranges.

## Related skills
ww2 (hub), ww2-tactics (who carries what), unit-combat-math (hit and damage math), combat-models (salvo at the
force level).
