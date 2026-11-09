# dom6-tactics - Battle orders (manual pp. 44-46, 58-60; read in full 2026-11-03 at the user's request)

Part of the dom6-tactics skill; SKILL.md links here.

## Battle orders (manual pp. 44-46, 58-60; read in full 2026-11-03 at the user's request)
See also **dom6-battle-ai** (the same orders plus how the AI picks spells and targets).

Nobody steers a battle: units deploy where Position Army puts them and then follow these orders.
Each squad has its own order, even under one commander. Orders marked * also need a TARGET.

**Squad orders** (p. 44-45)
| Order | What the squad does | Use it for |
|---|---|---|
| None | the computer decides | rarely: write down why if kept |
| Attack* | moves on the target and melees it | melee squads vs a divided enemy (the expansion guide: Attack picks them apart) |
| Fire* | shoots the target until **out of missiles** | javelin/missile squads. The manual stops there; **game-tested (T6 Murias): Alae on Fire closest went on to melee with spears once the javelins were gone** |
| Guard commander | centres on its commander and protects him; may join him in an assassination fight; missile units fire only when an enemy gets too close | bodyguards (Bartholomeus' Communicants) |
| Hold and attack* | holds **2 rounds** (shoots if it has missiles), then melee | vs heavy cavalry (they arrive alone and get surrounded) and fliers; NOT vs many archers (2 extra volleys taken) |
| Hold and fire* | holds 2 rounds, then fires or moves into range | archers who should let the enemy close first |
| Fire and keep distance* | fires until the target is close, then withdraws to a safe range and keeps firing | fast skirmishers, archers that must not be caught |
| Retreat | leaves the field - treated exactly like a rout, may scatter to neighbouring provinces | scouts, units that must not fight |
No order makes a squad hold forever ("Can't my soldiers just sit back and defend?" - "No"). Any order can
fail if the squad is caught in an enemy's zone of control on the way.

**Targets** (p. 45): None = a random enemy and its squad; Archers; Cavalry (also fast units); Fliers;
Large monsters (size 7+, or 6 if there are none); Closest = the closest enemy squad; Rearmost = a random
enemy at the back. The expansion guide: Fire Closest is the default (routs the infantry, then the
archers); Fire at Archers splits our damage; Fire at Large Monsters is anti-cavalry.

**Commander orders** (p. 45-46): up to **five specific orders** (one round each), then **one general
order** for the rest of the battle. No orders = the AI assigns them.
- Specific: Hold one turn; Hold or fire missile weapon; Hold or cast a spell (AI picks the spell, casters
  only); **Cast a specific spell** (if the gems are carried and a target is in range - otherwise the AI
  picks a spell instead); Attack one turn (a random enemy); Fly attack one turn (fliers).
- General: **Stay behind troops** (casts spells, fires missiles, keeps to the rearmost part of the army);
  Attack (melee); Cast spells (AI-chosen); Advance and cast spells (moves near the front, casts on the way);
  Retreat (routs off the map).
- **Conservative gem use**: gems only for scripted spells. `[x]` repeats the last order given.
- Copy a script: hover it, Ctrl+digit; hover another `<set battle orders>`, press the digit (0-9 slots).

**What breaks an army** (p. 58): a squad tests morale when it takes enough casualties and routs if it
fails; **all commanders dead or routed = the whole army routs**, however big; 75% of the side's hit points
lost = rout. There is no "attack commanders" order - getting at theirs is a setup question.
Battle limits (dom6-play): enchantments end at round 100, attackers rout at 150, defenders at 170.

**Formations** (p. 59; chosen per squad in Position Army, top right)
| Formation | Layout | Notes |
|---|---|---|
| Box | as near a square as possible (36 size-3 men = 4 squares wide x 3 deep) | default; a big arrow target; back ranks backfill slowly |
| Line | one straight rank facing the enemy | good commanders only; the guide's usual best |
| Double line | half the men in a rank right behind the first | good commanders only; rarely useful |
| Sparse line | a line with an empty square between squares (twice as long) | -1 morale; good commanders only |
| Skirmish | checkerboard, empty square on all four sides | -1 morale; undisciplined squads always use it |
Skirmisher ability removes the -1 in Skirmish / Sparse line; Formation Fighter fits more men per square.
**One square holds 10 size points** (three size-3 humans). A unit 3+ sizes bigger can push into a
square by displacing smaller units (1 extra combat speed); tramplers never do this unless routing (p. 60).

**Movement and contact** (p. 58-60): one square costs ~1 combat speed (diagonal 1.5); units halt in an
enemy's zone of control (adjacent) and stay locked while it lives; routing units ignore it. After a step
a unit waits a short cooldown (shorter for faster units), after a strike a long one (about a round).
Missiles: the hit chance depends on how many units are in the square hit and the target's shield;
**missiles can hit our own men** (dom6-play) - shooters behind a line in contact are a risk.

**Mixing and leadership** (p. 59): see "Leadership and squads" above. Unassigned units: one big squad in
the centre (no fort) or inside the walls (fort).

**In use (Pythium, T7)**: Alae and Velites Fire closest; Jaguar slingers + warriors Fire closest;
commanders Stay behind troops with scripts; bodyguards Guard commander; scouts Retreat at the far rear.
Checked against the manual 2026-11-03: all consistent. Against Bear Tribe (no shields, leather prot 9,
bare heads, morale 10) Fire closest is right - javelins are for unshielded enemies (expansion guide).
