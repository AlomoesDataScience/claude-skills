---
name: dom6-army-check
description: Checklist for making sure every Dominions 6 army and unit is set up properly before ending a turn - for each commander, (1) is it a mage or priest, (2) does it have spells scripted and should it, setting them if wanted, and what its default orders do, (3) which units are in its squads and whether leadership, morale and squad orders are right, (4) where each squad and the commander stand and in which formation. Uses dom6-game (screens and click points), dom6-tooltips (reading numbers), dom6-tactics (layouts and lessons). Use when a turn is about to end, after recruiting, merging, moving or buying mercenaries, before any attack, and when the user asks whether the armies are ready.
---

# Dom6 army check

A checklist, done for **every commander** (every army) before the turn ends. The order is the
user's (turn 6): mage first, then spells, then defaults, then units, then positions and
formations. Screens and click points: **dom6-game** (Army Setup, Battle orders, Position Army).
Reading the numbers: **dom6-tooltips**. Layout rules and the battle log: **dom6-tactics**.

## Files

- `scripts/script_orders.py NAME [--spell S]... [--main ORDER] [--target T] [--keep] [--read]`:
  in an open Army Setup, opens NAME's battle orders, clears the script (each `<del>`), adds
  each spell through Choose spell (refuses greyed spells), sets the main order, reads the result
  back (the selected radio is found by its X mark's pixels, since OCR merges marks into labels)
  and presses Ok. Army Setup rows also show each commander's script, a quick visual check.

## When to rescript (the user)

Check every mage's script **every time research finishes a level** (new spells) and **before a
big battle** or any situation that changes what is worth casting. Scripting costs Claude
nothing, so script every mage; it is a good habit.

## 0. List the armies

- Every province with a commander: the commander list on the main map, or each province's Army
  Setup (`t` in the province; `y` = Army setup at destination when armies will meet).
- Scouts and lone commanders away from home show on the map as movement arrows (grey arrow from
  the province they are in); right-click that province, then `t`.
- Note for each: where it is, where it is ordered to go (move, attack, research, patrol...).
  Commanders staying home on Research or a ritual still get checked: they fight if attacked.

## 1. Is it a mage (or a priest)?

- The token in Army Setup shows path symbols under the name; the unit screen (right-click the
  portrait) shows the magic row: path symbol + level, the candelabra = priest (Holy), the
  yellow ? = random path (right-click it for the odds). Tooltips: "fire mage level 1",
  "priest level 2". dom6-knowledge `ui/magic-symbols.md` has every symbol.
- No paths and no Holy: a plain commander. Skip to step 3 (but still give it a main order).

## 2. Spells: scripted? should they be?

1. Open its `<set battle orders>`. The top bars are the script (up to five steps), the orange
   bar the main order. Read what is there.
2. Decide whether a script is wanted:
   - Leave it to the AI when the AI's choices are fine (Theocratus cast Holy Avenger, Sermon of
     Courage and Word of Stone on his own at Murias). Check the last battle review
     (dom6-battle-view) to see what the mage actually cast.
   - Script when a specific buff or opening spell matters (blesses for sacreds, protection
     spells before melee, a communion), or when the AI wastes casts.
   - Gem spells need the gems in the mage's inventory before the battle; tick **Conservative
     magic gem usage** to keep gems for scripted spells only.
3. To set: Cast a specific spell > Choose spell (greyed = can't cast; right-click for the
   spell card) > click the spell's text. Remove a step with its `<del>`. Copy a good script to
   other mages: hover it, ctrl+number; hover the other `<set battle orders>`, press the number.

## 3. Defaults: know what each unset order does

- **Commander, Main Order None**: the AI assigns orders (manual p. 45); a mage then casts what
  the AI picks. Stay behind troops = casts spells, fires missiles, keeps to the rear; Cast
  spells = AI-chosen spells; Advance and cast spells = moves near the front and casts; Attack =
  melee; Retreat = leaves the field (scouts).
- **Squad, order None** (grey box): the commander decides. Undisciplined squads (red box) take
  no squad orders at all.
- **Formation**: new squads are Box. **Position**: new squads and mercenaries land stacked on one
  default spot; garrison units with no commander fight as one big squad in the centre.
- Write down any default that was kept on purpose, so a later review can test it.

Scripts in use (turn 6, after the user's review; spell data from dom6-inspector):
- Theurgs (A1 W1 S2 H2): Air Shield, Twist Fate, Slime x3; main **Stay behind troops** (the
  user's habit, over Cast spells). Slime: AoE, -2 att/def and slowed; **AoE beats single-target**
  because it still lands among the enemy when it misses.
- Bartholomeus (A2 W2 S3 H4) is the **communion master**: Communion Master, Divine Blessing
  (once: blesses all sacreds, Theurgs and Communicants), Star Fires x3 (its damage grows with the
  boosted path level). The 5 Theurg Communicants are his squad with **Guard commander**
  ("bodyguards"); they cast Communion Slave by themselves. Other Theurgs are neither slaves nor
  masters for now.
- Theocratus (prophet, H3): Sermon of Courage, Holy Avenger, Word of Stone x3; Stay behind.
- Scouts: Retreat, far rear.
- Worth remembering: Trueshot (A1, +4 precision) on javelin troops; Cold Bolt (W2).

**Copying a script** (manual p. 45, faster than rebuilding it): in Army Setup hover the
commander's script bar, press ctrl+1 (1-9 are slots); hover another commander's bar and press 1.
Tested turn 6: Apuleius's script onto three Theurgs.

## 4. Units in the army

In Army Setup, per commander (the four numbers on its row; hover the number's centre):
- **Squads**: used / led without morale penalty (bodyguards don't count). Past the limit,
  every squad loses morale (dom6-tactics, leadership table).
- **Living units** led / leadership, and **magic beings** led / magic leadership: undead,
  demons and magic beings need the matching leadership.
- Every unit in a squad (none left loose), squads of one type each where possible, a Standard
  per squad if the nation has them, no undisciplined units mixed into a disciplined squad
  (the whole squad turns undisciplined, −1 morale), no undead/demons mixed with living (−1).
- New recruits and mercenaries in this province: joined to the right commander?
- Squad orders set for each squad (Fire closest for javelin troops, Attack for melee, Guard
  commander for a bodyguard of at most 5 under Theocratus, Retreat for scouts).
- Supplies: the header's supplies available vs needed.
- Garrison units with no squad (Army Setup header strip): put them under a local commander
  (alt+click one = all of that type, click the commander's portrait = new squad, Enter), or
  plan a commander for them. If troops pile up at the capital with no field commander, recruit
  one: the user's rule is that the commander beats the Theurg for the capital's 2 commander
  points that month (turn 6: Theurg swapped for Centurion + Scout, commander repeat unticked).
- Squad order window: None, Attack, Hold and attack, Fire, Hold and Fire, Fire and keep
  distance, Retreat, Guard commander, plus targets; click the word's centre, then Ok.
- Mages staying home: no troops needed, but they are the capital's defence if attacked.

## 5. Positions and formations

Open Position Army (a squad's or the commander's green box) for every army that may fight:
- Every squad placed (none on the default spot), all on our light-green half.
- Front to back: expendable screen, main line, missile troops, commanders **centred behind the
  line** (the user), scouts at the far rear on Retreat. Flankers offset up or down.
- A new squad lands on the commander's spot: select it by the top-left corner of its box (the
  header must show "N units", not the commander's name), right-click where it should go.
- Formation per squad: Box (default) unless there is a reason (a Mounted Commander's squads
  only offer Box and Skirmish); Line / Double line need a good
  leader; Sparse line and Skirmish cost −1 morale. Record the choice in the battle log.
- Check the mini-maps (green boxes) in Army Setup afterwards, then Exit.

## 6. Report

For each army, one line: commander, mage paths (or none), script (or AI), main order, squads and
orders, formation, leadership used / limits, problems fixed. Then tell the user, and only end
the turn when the user says so.
