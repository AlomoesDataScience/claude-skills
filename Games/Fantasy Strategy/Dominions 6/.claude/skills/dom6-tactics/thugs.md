# Thugs and supercombatants (from the illwiki thug guide)

Distilled 2026-10-28 from the Dom6 thug guide on illwiki
(`wiki.py show strategy_articles/thugs/part1_mechanics`; part 2 has worked examples, part 3 the
item and spell tables). It's written from tournament play, so it describes what works against
humans; the AI is softer.

## Terms

- **Light thug:** 0-15 gems of gear. Kills small province defence (PD) alone or with a fluffer
  or two. Fails against big PD.
- **Heavy thug:** self-sustaining. Kills any amount of PD or unbuffed infantry. Still vulnerable
  to strong infantry (barbarians, giants, lizardmen).
- **Supercombatant (SC):** built to beat a real army, sometimes with mages.
- **Fluffer:** a mage that buffs the thug, then retreats.
- **Counterthug:** a cheap unit with one strong weapon, built to kill an enemy thug. The guide's
  example is a Greatsword of Sharpness (15 armour-piercing) on a strong chassis. Bring a scout
  to pick up the loot.
- **Army thug:** embedded in our own line, to hold off a blob, snipe elites, or add damage.

## The guide's verdict: thugs are overrated

- **Troops and sacreds win wars; thugs are a side benefit.** In the tournament finals they
  studied, almost no thugs appeared before turn 23.
- **Every thug costs:**
  - gems (and gives them to the enemy when it dies: a "loot piñata");
  - commander points;
  - mage turns spent forging instead of researching or site-searching.
- **Cost guide:** 10-15 gems for a cheap thug. Don't overinvest in one that only clears PD; two
  5-gem items usually beat one 10-gem item.
- **Thugs can't take forts**, and land they raid is retaken. They work best:
  - as a decisive raid right before a big army fight;
  - against undefendable border provinces;
  - against small, separate forces (reinforcements, raiders).

## The defensive onion

- **Layers multiply:** each layer that stops ¾ of attacks leaves ¼, so four layers leave 1/256.
  Mixing *different* checks beats pushing one stat higher.
- **Protection is the weakest layer** because of armour-defeating hits.
- **Good combinations:**
  - Mistform + Body Ethereal;
  - protection buffs + regeneration (watch the fatigue);
  - high defence + Mirror Image + Shroud of Bewilderment;
  - fear + awe.
- **Early layer spells:**
  - Body Ethereal (S1, cast on another unit);
  - Mistform / Mossbody;
  - the skin spells;
  - Summon Earth Power (the only early reinvigoration);
  - Personal Regeneration;
  - Shroud of Bewilderment;
  - Awe.
- **Pythium:** Theurgs have S1 for Body Ethereal and A1 for Personal Mistform (Mistform on
  others needs A2). That gives an Emerald Lord two strong layers, on top of his tower shield.

## Armour-defeating hits and fatigue (the usual cause of thug death)

- **The rule:** when the defender's protection roll is a 2 (1 in 36), the hit ignores 25% of
  protection.
  - At **fatigue 50-99** it's a 2-3 (1 in 12).
  - At **fatigue 100+ or immobilised** (entangled, webbed) it's a 2-4 (1 in 6).
  - Each 10 fatigue also costs 1 defence (max −10).
- **Don't end a buff script with a big spell that fatigues the thug out.**
- **Don't tank giants with protection:** at protection 32 against 28 damage, a fatigued thug takes
  about twice the damage of a fresh one.
- **Fatigue sources:**
  - melee: encumbrance each round of attacks, and each flight;
  - casting: encumbrance + 2 × (armour + shield encumbrance) a spell, ×1 for combat casters;
  - heat/cold scales: +0.5 at 2, +1.5 at 3.
- Undead start at 0 encumbrance.
- **Reinvigoration items come at Construction 5:** Boots of the Messenger, Girdle of Might,
  Amulet of Resilience; also the Amulet/Ring of Regeneration. Construction 3 thugs struggle to stay
  fatigue-neutral; Construction 3 and 5 are the core thug techs.

## Protection, invulnerability, wading

- **Combining armour and natural protection, quickly:** larger + half the smaller (+1 under 30).
  Armour 20 + natural 10 ≈ 25. The exact formula is in dom6-spells.
- **Invulnerability:** replaces natural protection against **non-magic** weapons only, when it's
  higher. It doesn't stack with natural protection.
- **Wading (new in Dom6):** a unit 3+ sizes bigger can walk through smaller units (not a
  trampler; it can even wade onto fort walls).
  - A big thug can start behind the line, take buffs, then wade in.
  - Flying army thugs can be scripted to attack the rear after round 5, when the enemy mages are
    off-script.

## Scripting notes from the guide

- **Self buffs spread to the mount:** Personal Barkskin, Shroud and Personal Regeneration buff
  rider and horse. Matters for Serpent Lords and cataphract commanders.
- **Buffs target differently.** Some go to the most valuable target nearby (Body Ethereal),
  others prefer the caster (Gift of Cheated Fate). The card doesn't say which. Check in replays.
- **Unscripted spells are drawn from about 50 random castable spells, then weighted.** Spells
  in the script get no priority once the script runs out. (Matches `ai-casting.md`.)
- **A gem or two on a thug changes everything:**
  - E1 casting Summon Earth Power (reinvigoration + E2);
  - N1 casting Personal Regeneration;
  - G1 casting Shroud;
  - A1 casting Personal Mistform.
- **Hide the gear:** a scout can carry gems or a stealth helmet (Construction 5 G3 / Construction 7
  G2) and swap it onto the thug after the fight so it can sneak away.
- **Magic-phase moves** (Teleport, Cloud Trapeze) land together with stealthed units attacking
  the same province.

## Choosing targets

- **Edge-of-territory provinces:** safest; out of reinforcement range, unpredictable.
- **Next to a fort:** risky (mages inside) and retaken next turn; only to open a path.
- **Forts and capitals:** pin the defender for a turn; needs stealth or magic phase.
- **PD type matters:** protection thugs die to barbarian or lizard PD; tribe and cave PD is
  weak and a good target.
- **Defending against thugs:** dump PD in provinces with good independents. Script mage
  armies to retreat if a supercombatant may drop on them.

## Counters (for us, and against us)

- **Curse** (G/N early, D with gems): every chip of damage risks an affliction. The top
  anti-thug spell.
- **Magic Duel:** kills astral-mage thugs. That's why we keep the god away from astral.
- **Web / Earth Meld** and other immobilising spells: low research, area. They pin low-strength
  thugs and raise armour-defeating hits to 1 in 6.
- **Mind Hunt / Soul Slay:** snipe thugs remotely (`dom6-spells/rituals.md`).
- **Armour-negating damage:**
  - Lightning Bolt (Pythium, Evocation 2);
  - Frozen Heart (W1, Alteration 6: any Theurg);
  - Life for a Life (Blood 8).
- Evocation 5 area spells hurt army thugs.
- **Chaff** (Horde of Skeletons, illusions) swamps thugs with no area damage.
- **Returning thugs** (Ring/Ritual of Returning) must die in one weapon's attacks:
  - multi-hit weapons count: Sword of Swiftness ×2, Gloves of the Gladiator ×4, Wave Breaker ×3;
  - or Magic Duel, Gifts from Heaven, Disintegrate, Stream of Life, Bane Fire, Control.
