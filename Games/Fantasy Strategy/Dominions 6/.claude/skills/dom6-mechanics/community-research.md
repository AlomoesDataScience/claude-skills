# Community research: rules the manual doesn't spell out

Distilled 2026-10-28 from illwiki (the dom6-wiki skill; page names in brackets).
- Loggy's notes were measured by disassembling **Dominions 5** (5.53-5.60). Treat them as
  "very likely still true" for Dom6, not as verified.
- The turn order and province defence pages are Dom6 pages.
- Where the manual (`SKILL.md`) is simpler, these are the details behind it.

## Morale checks in detail [user/loggy/morale]

- **Every unit has a hidden "morale problems" counter.** It rises when:
  - **a squad-mate dies: +100 to everyone in the squad**;
  - **a unit drops below 80% hp: +1**;
  - **a fear effect hits** (spell or fear aura): +1000 to the whole squad, and +1000 more to the
    unit hit; units with morale 50+ ignore it;
  - **a fear-arrow hit** (fear type 2, e.g. howling bows): +1 to the unit and to its squad.
  The counter resets to 0 after each check, so morale damage doesn't carry over between rounds.
- **Commanders are squads of one.** Any morale problem forces a check:
  **5 + morale + DRN vs 14 + DRN**; losing routs (a tie holds). A morale-10 mage who gets
  wounded below 80% hp checks at 15 + DRN vs 14 + DRN and **routs 31% of the time** (simulated).
  A wounded friend nearby doesn't make him check.
- **Squads check when:**
  - their highest counter reaches 10,000 (fear), or
  - a "bad case" row is true. Each row needs, unless marked, the counter to be at least half
    the surviving members:
    - ≤80% alive and average morale ≤8;
    - ≤75% alive and morale ≤10;
    - ≤70% alive and morale ≤11;
    - ≤60% alive (any morale);
    - ≤30% alive (any problem at all);
    - or the survivors are no more than a d4 roll (tiny squads).
  - Because one death adds 100, **any death in a small squad meets the half-squad
    condition**. So what decides a check is mostly the % alive and the average morale.
- **The squad's check:** 4 (0 in a bad case) + average morale (30 counts as 30 max) +
  (original/2 + 5 × alive)/original + DRN vs 14 + DRN.
  - For a full squad the survivor term is ≈5.
  - **Simulated:** a near-full squad that isn't in a bad case routs 7% of the time at
    morale 10 and 14% at morale 8. In a bad case (base 0) at morale 10 it's 31%.
  - **Morale 12+ troops rarely rout early; morale 8-10 troops start breaking once 20-30% are
    dead.**
- **Whole-army rout:**
  - at **75% of field hp lost** (province defence counts ¼, as in the manual) the army routs;
  - an attacker routs all commanders without a check;
  - a defender in a fort makes each commander check vs 10 + DRN instead.
- **Time limits:** attackers rout from round 91 at 25% hp left; defenders from round 111.
- **Fear auras hit one square around the unit** (more only with aura 25+). Stacking more fear
  adds little once a squad is at 10,000.
- **Fear and morale effects are capped at ±5** and halve each round.

## Scout reports [user/loggy/scoutreports]

- **Error by source:**
  - **scout ±30%**;
  - **spy ±10%**;
  - default/dominion ±50%;
  - Arcane Scrying ±40%;
  - **scrying spells (Astral Projection) and Eyes of God 0%**.
- **The error is uniform:** −100% to +99% of the inaccuracy, × the true count. So a scout's
  "about 30" means 21-39 or so, rounded to tens. (Helmshire: "30", really 44, which was even
  outside that; false-army or obfuscate abilities count too.)
- "The army appears to be commanded by X" only shows when the error is under 30%: with a spy
  or scrying, not a scout.
- **The report lists the six most common unit types.**
  - It may "notice" big units (15% per size point from size 4).
  - It may notice strong units (power score = hp, ×2 if ethereal, + 10 × fear + 5 × awe,
    + 15 × paths for commanders; chance score/2 %).
  - It may notice fliers.
  So **mages and monsters can be missing from a scout report.**
- **Fata Morgana:** 50% the whole army is hidden, otherwise the count is ×0-5. "Fool scouts"
  wipes the second unit type.
- **Province defence by report text:**
  - "one officer and a few loyal henchmen" = 1-5;
  - "quite well organized" = 6-19;
  - "very strong" = 20-34;
  - "exceptionally powerful" = 35+.
  The report is from last turn; defence can be raised the same turn we attack.

## When the enemy AI burns gems [user/loggy/gemusage]

- **Unscripted enemy mages save their gems unless the fight looks dangerous to them.** Gem use
  triggers when any of these is true:
  - (our army's value + 2) × 5 ≥ their army's value (we're at least about ⅕ of their strength);
  - our commanders have 10+ non-holy paths in total and carry any gems;
  - our gems + 3 × items + paths ≥ 16;
  - per mage with 4+ paths and gems: (paths + gems − 4) × 33% chance;
  - per commander with 4+ items: (items − 3) × 50% chance.
- **From round 8 they spend gems normally anyway.** After an army routs, no more gems.
- **"Retreating" commanders count less:**
  - commanders scripted to Retreat, or with Returning in the first script slot, or with any
    returning-on-damage effect;
  - their items don't count, and their paths count 2 less.
- **For us:** a pinging scout carries no paths or items, so it won't make the enemy burn gems.
  A big mage army will, from round 1.

## Experience [user/loggy/experience]

- **Ways to gain experience:**
  - +1 a turn alive (not mindless);
  - +1 per melee attack;
  - +1 per trampled square;
  - battles: **+4 if the unit didn't retreat, +1 if it did**;
  - adventure sites +20 a turn;
  - arena win +100;
  - experience items work, but not on animals.

## Spell timing [user/loggy/casttime]

- **A spell lands at its expected cast time ±500 ticks (uniform).** All mages on a side doing the
  same thing start together. Two mages casting the same spell don't land at the same moment.

## Turn order (Dom6 page) [turn-order-sequence; manual pp. 55-57]

In order:

1. Stealth switch, messages, **research**, recruitment, empowerment, **forging**, preaching,
   thrones, quick orders (site entering).
2. **Rituals**, in random order.
3. **Magic-phase battles:** Teleport, Wind Ride, Cloud Trapeze. Stealthed attackers on the same
   province join them.
4. Site searching (non-spell), prophets, Call God, **gods (re)awaken**, blood hunting.
5. Horrors, **assassinations**, raids.
6. **Movement:**
   - friendly moves first, so defenders can group up;
   - then moves into enemy provinces;
   - an army whose middle province was taken in the magic phase doesn't move.
7. **Main battles** (random order), then fort storming, then retreats.
8. Global enchantment effects, **events**, event battles (barbarian raids...).
9. Patrols find hidden units; then sieges damage walls, buildings, reanimation.
10. **Income, then unrest, then starvation, upkeep, dominion spread**, site effects, aging.
11. Healing and disease, **mercenary bids, heroes**, leaderless units deleted, unbesieged forts
    retaken.
12. **Province defence raised to at least 1**, **scout reports**, victory check.
13. Province defence trimmed to population/10.

Consequences:
- **Rituals happen before movement:** a remote spell hits the army where it stood.
- **Teleporting thugs fight before normal moves.**
- **Research and forging happen before battles:** a booster forged this turn is worn in this
  turn's battle.
- Temperature changes happen after the battles: what we see is what we'll fight in.

## Province defence (Dom6 page) [game-mechanics/province-defence]

- **Cost:** level N costs N gold, so 0→10 costs 55 gold. The maximum is 100 or population/10.
  Friendly civilisations pay 2 less a level.
- **Thresholds:**
  - **4, 10 and 20 block many bad events**;
  - **15+ patrols** (patrol strength 1, +1 per level);
  - **20+ adds a second commander and national troops**;
  - each 10 levels cuts unrest by 1 a turn.
- **Troops:**
  - without a fort, province defence is the province's old independent population type;
  - **with a fort it's the owner's national troops**.
  - It's temporary (no afflictions, back every fight) and counts ¼ for the army's hp rout.
- **The guide's verdict:** 0 province defence invites a scout to take the province. Big dumps
  rarely help, since an army that kills 15 kills 30. They're useful backed by mages, or where
  the independents are strong (barbarians, lizards, heavy cavalry).
