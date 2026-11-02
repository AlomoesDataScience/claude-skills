# Magic items, ranked: killing, protection, utility (first pass, 2026-10-28, for the user's review)

Every forgeable item (Construction 1-9, not another nation's), sorted into the user's three
categories. Numbers come from `scripts/items.py`, built on the dom6-spells combat model with the
manual's shield rule. The full tables are in `killing-table.md`, `protection-table.md` and
`utility-table.md`.

**Forger** is the cheapest Pythium mage whose own paths reach the item (no boosters):
- **Th** = any Theurg (A1 W1 S2);
- **AT** = Arch Theurg (A2 W1 S3 + random);
- **Barth** = Bartholomeus (A2 W2 S3). W2 items need him or a Water-rolled Arch Theurg;
- **God** = Hortus once awake (E5 N5);
- **—** = nobody of ours.

**C** is the Construction level. We have Construction 0 now (1-3 queued).

## 1. Killing items

The test wielder is the Emerald Lord (att 15, str 13, broad sword, tower shield). The item takes
the sword's place. A two-handed item also takes the shield, so it costs him defence and
protection; this list counts only the kills. A misc-slot weapon (dancing weapons) fights
*beside* his sword and keeps the shield.

**Number:** sword-and-shield heavy infantry killed a round. His own broad sword kills **0.28**.

| Tier | Item | Slot | C | Gems | Forger | HI / round | Why |
|---|---|---|---|---|---|---|---|
| S | The Death Globes | misc | 9 | 10D | — | 4.4 | Six armour-negating 30-damage strikes a round. Death magic; not ours. |
| S | Flailing Hands, Tartarian Chains, Wave Breaker | 2-h / 1-h | 7-9 | 10-35 | — | 1.3-1.5 | Many attacks a round. Not our paths. |
| **S (ours)** | **Dancing Trident** | misc | 5 | 5A | **Th** | **1.0** | **Pythium's best killing item: 3.6× his sword.** Misc slot, so he keeps sword and shield. Any Theurg forges it for 5 air gems. |
| A (God) | Smasher, Hammer of the Mountains, The Stone Sword | 1-h / 2-h | 3-9 | 5-40E | God | 0.77-0.88 | Smasher (C3, 10E) adds Shatter and keeps the shield. Hammer stuns an area. Stone Sword petrifies one. |
| A (ours) | **Sword of Swiftness** | 1-h | 5 | 10W | Barth | 0.81 | Two attacks a round, keeps the shield. Second-best Pythium weapon. |
| A | Twilight Glaive, Unquenched Sword, Ember, Astral Serpent, Sun Slayer, Shadow Brand, Fire Brand | | 5-9 | | — | 0.75-0.91 | Area effects on hit. Not our paths. |
| B (God) | The Summit, Gloves of the Gladiator, Greatsword / Axe / Sword of Sharpness, Axe of Hate, Star of Heroes, Halberd of Might | | 3-9 | 5-25 | God | 0.55-0.71 | Earth gear for the god himself and his thugs. Sword of Sharpness (C3, 5E) is the cheap one-handed pick. |
| B (ours) | Rime Hammer, Shock Trident, Demon Bane, Moon Blade | 2-h | 5-7 | 5-15 | Th / Barth | 0.53-0.64 | Good damage, but they cost the shield. Moon Blade (S1, 5S) suits a Theurg's own hand. |
| B (ours) | **Coral Blade** | 1-h | 3 | 5W | Th | 0.49 | Armour-negating. The best **early** Pythium weapon that keeps the shield: 1.8× his sword at Construction 3. |
| C (ours) | Enchanted Pike, Frost Brand, Enchanted Sword / Spear, Ice Mist Scimitar, Ice Sword, Thunder Whip, Lightning Spear, Herald Lance | | 1-5 | 5-10 | Th | 0.25-0.42 | Barely better than his sword. Use them for the magic damage against ethereal foes, not for the kills. |
| D | Missile items: Bow of War (Th, C7), Thunder Bow (AT), Golden Arbalest | missile | 5-7 | | | ≤0.15 | Shields stop most arrows (manual rule). Only worth it against unshielded targets. |

**Not counted:** Quickness doubles a thug's attacks. Boots of Quickness (Barth, C7, 10W) would
roughly double any row above.

## 2. Protection items

**Thug test.** The Emerald Lord in his own kit (plate, full helmet, tower shield, def 18) takes
**160** heavy-infantry attacks to kill. The item replaces the piece in its slot; misc items add
their abilities. His tower shield already makes him nearly arrow-proof (0 hp per 100 short-bow
shots), so arrows don't separate the thug items.

**Mage test.** A Theurg (def 10, no armour) dies to **3** attacks and loses **79 hp per 100
arrows**. For him the arrow column is the one that matters: missiles are the mage killer.

### Thug protection (×own kit, attacks to kill)

| Tier | Item | Slot | C | Gems | Forger | × kit | Why |
|---|---|---|---|---|---|---|---|
| S | Monolith Armor | body | 9 | 25E | God | 6.0 | Body 34 + regeneration + 20 hp. The god's own armour once awake. Enc 10, so not for casters. |
| S | Bloodstone Armor, Wyrmskin Boots | | 7-9 | | — | 3.5-4.9 | Regeneration. Not ours. |
| A (God) | **Ring of Regeneration** (C5, 10N), Boots of Antaeus, Crown of the Ivy King, Iron Face, Marble Armor, **Boots of Stone** (C5, 10E), **Blacksteel Full Plate** (C1, 10E), Krupp's Bracers | | 1-9 | 10-30 | God | 2.1-2.5 | Regeneration and skin spells stack with armour. Blacksteel Full Plate is the cheapest upgrade at Construction 1. |
| **A (ours)** | **Armor of Virtue** (unique) | body | 9 | 15S | AT | 2.4 | Awe 4 + body 16 + 10 hp. Pythium's best armour, but Construction 9. |
| **A (ours)** | **Weightless Tower Shield** | shield | 3 | 10A | AT | 1.8 | Parry 8, enc 0. The best early Pythium protection item. |
| B (ours) | Ice Aegis (Barth, 10W), Weightless Kite Shield (AT, 10A) | shield | 3 | 10 | AT / Barth | 1.6 | Bigger shields. |
| B (ours) | **Enchanted Shield** | shield | 1 | 5S | Th | 1.3 | Construction 1, 5 astral gems. |
| C (ours) | Dragon Scale Mails, Rime Hauberk, helmets, scale mails, robes, missile amulets, Rabbit Foot | | 1-7 | | Th / AT | 0.2-1.1 | No better than his plate. Lighter body armour is *worse* for him. |

**Cursed (can't be removed):** Lycanthropos' Amulet, Aseftik's Armor, Amon Hotep, Gift of Kurgi.

### Mage protection (Theurg)

| Tier | Item | Slot | C | Gems | Forger | × kit | Arrows / 100 | Why |
|---|---|---|---|---|---|---|---|---|
| S | **Armor of Virtue** (unique) | body | 9 | 15S | AT | 17.6 | 18 | Forged once per game. Awe 4 keeps most attackers off. Enc 1, so a mage can cast in it. Late. |
| **A** | **Weightless Kite Shield** | shield | 3 | 10A | AT | 3.8 | **5** | Arrows drop 79 → 5 and it adds no casting fatigue (enc 0). A Theurg can hold it with his mace. **The mage-saver to forge first.** |
| A | Ice Aegis | shield | 3 | 10W | Barth | 3.5 | 2 | The same, enc 1 (+2 fatigue a spell). |
| A | **Enchanted Shield** | shield | 1 | 5S | **Th** | 2.2 | 5 | **Construction 1, 5 astral gems, any Theurg forges it.** Arrows 79 → 5, at enc 1. The cheapest big gain on the whole page. |
| A | Weightless Tower Shield | shield | 3 | 10A | AT | 2.5 | 2 | |
| B | Robe of Shadows | body | 5 | 10S | Th | 4.1 | 18 | Ethereal: mundane weapons mostly miss. Stealth too. |
| B | Robe / Amulet of Missile Protection | body / misc | 3 | 5-10A | Th / AT | 1.0 | 16-17 | Air shield 80: arrows 79 → 16. The amulet keeps the body slot free. Less than a shield, but stacks with one. |
| B | Dragon Scale Mails, Rime Hauberk, Enchanted Ring Mail, scale mails, Copper Plate | body | 1-7 | 5-10 | Th / AT | 1.8-3.2 | 16-30 | Body armour. Encumbrance adds casting fatigue (+2 per enc a spell). |
| C | Rabbit Foot Charm, Amulet of Antimagic, helmets, Crown of Command | | 1-5 | 5-10 | Th | 1.0-1.5 | 74-81 | Not body protection. Antimagic (MR +4) protects against Soul Slay and Mind Burn, which this test doesn't model. |

**Targeting (the user):** the enemy can't aim at commanders. Arrows reach a mage by luck (stray shots into his square) or when he's the only target left. So mage shields guard against strays, not aimed fire: still cheap and worth it, but less urgent than the arrow column suggests.

**Finding:** under the manual's shield rule a **shield is the mage's best missile protection**,
better than the air-shield items. Theurgs carry a one-handed mace, so the hand is free. To check
in game: does the Theurg's Air Shield spell stack with a shield? Which hits does the AI aim at
mages?

## 3. Utility items

Utility isn't measured in kills. It's ranked by what it does for the plan (research, gems,
communion power, mobility).

**Gem items:** the inspector's "temporary gems" (Water Lens, Bag of Winds, Cornucopia, Fire in a Jar)
are battle-only. They pay a combat spell's gem cost in each battle and can't be used for rituals
or kept (Cornucopia's text). Only "generates gems per month" items are income (Fever Fetish,
the Elemental Orbs), and none of those is ours to forge.

| Tier | Item | C | Gems | Forger | Effect | Why |
|---|---|---|---|---|---|---|
| **S** | **Owl Quill** | 3 | 5A | Th | research +6 | A Theurg makes 19 RP instead of 13 (+46%). The best research item we can forge; one per research mage as air gems allow. |
| **A** | **Bag of Winds** | 5 | 10A | AT | a free Lesser Air Elemental at the start of every battle; 1 battle air gem | A flying ethereal trampler (about 2 HI kills, `summons.md`) for every battle, forever. Good on a front-line commander. |
| B | Water Lens | 5 | 5W | Th | 1 battle water gem, water ritual range +1 | Pays Niefel Flames' gem later. |
| B (God) | Cornucopia | 5 | 15N | God | 2 battle nature gems | For the god's gem-cost nature spells. |
| **A** | **Spell Focus** | 5 | 5S | Th | penetration +1 | For the communion master's Soul Slay, Paralyze and Mind Burn. |
| A | **Crown of Command** | 5 | 10S | Th | leadership +100, magic leadership +50, inspirational | Lets a Theurg lead the summons (Air Elementals, Angels) and a bigger army. |
| A | **Winged Shoes** | 5 | 10A | AT | flying | A thug or Angel-style mage-hunter over the line; the god's mobility. |
| A | **Sky Metal Matrix** | 5 | 5E 5S | empowered forger (E1 S1) | the god masters a communion | From the plan (the user's teaching). Not in the battery, which has no communion item category. |
| A | **Ring of Returning** | 7 | 15S | AT | the wearer teleports home when badly hurt | Saves a communion master or Bartholomeus from dying in a lost battle. Not in the battery. |
| A | **Starfire Staff** | 5 | 10S | Th | astral range +1, casts Star Fires | Range for Soul Slay and Mind Burn. |
| B | **Boosters**: Starshine Skullcap (+S, C7, 10S, Th), Water Bracelet (+W, C7, 5W, Th), Tome of High Power (+A +S, C9, AT), Earth Boots (+E, God), Orb of Elemental Earth (+E, God) | 5-9 | | | +1 path | Communion does this job better (user). Exception: **one +A** lets an Arch Theurg cast Contact Draconians (A3), Pythium's best ritual summon. **Winged Helmet** (+A, C5, 25A) needs an Air-rolled Arch Theurg (A3) to forge. |
| B | Arcane Lens (+1 range in every path, C7, 15S, AT) | 7 | 15S | AT | | Range for the whole communion master's list. |
| B | Ring of Water Breathing (Th), Amulet of Breathing (AT), Pills of Water Breathing (AT) | 3-5 | | | water breathing | For the ocean plan (see the research plan). |
| B | Boots of Quickness | 7 | 10W | Barth | quickness | Doubles a thug's attacks (see killing). |
| B | Sandals of the Crane (blink, C9, Th), Bell of Cleansing (Barth) | 9 | 10 | | battle spells | Late. |
| C | Research items outside our paths: Skull Mentor (D), Dreamstone (G), **Lightless Lantern** (+12, F1, needs a Fire-rolled Arch Theurg), Homunculus (God, cursed) | 3-7 | | | | |
| C | Eye of the Void | 5 | 5S | Th | penetration +2, MR −2 | **Cursed**: never put it on a valuable mage. |

## What to forge, in order

1. **Construction 1:** Enchanted Shields for every Theurg in battle (5S each: arrows 79 → 5).
2. **Construction 3:**
   - Owl Quills on the research Theurgs (5A each);
   - a Weightless Kite Shield for Bartholomeus (communion master);
   - a Coral Blade or Weightless Tower Shield for the best thug.
3. **Construction 5:**
   - Dancing Trident on the thugs (5A, 3.6× kills);
   - a Bag of Winds on each army's lead commander (a free air elemental every battle);
   - Spell Focus and Crown of Command for the communion master;
   - the god's Sky Metal Matrix, Ring of Regeneration and Boots of Stone.
4. **Construction 7-9:** Boots of Quickness and Armor of Virtue for the thug or master; the god's
   Monolith Armor.

## Model limits

- One wearer and one foe type. Only melee and short-bow arrows count; enemy spells, magic weapons
  and morale don't.
- Two-handed items show their kills but not the defence lost with the shield.
- Regeneration counts heal per round of being hit, which flatters it against single attackers.
- Cursed items are marked but their curse (random afflictions) isn't counted.
- The numbers are untested in play. The model ran 1-2× high against the Murias battle.
