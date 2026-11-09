# dom6-mechanics - Looking things up

Part of the dom6-mechanics skill; SKILL.md links here.

## Looking things up

- `scripts/game_manual_text.py [PDF] [OUTDIR]` (needs `pdftotext`) writes `OUTDIR/rules.txt`
  (chapters, pages 1-98, columns untangled) and `OUTDIR/tables.txt` (every page in layout form, so
  table rows stay on one line). Default OUTDIR `/tmp/dom6manual/`. Each page starts `=== page N`.
- `scripts/lookup.py NAME [TABLES_TXT]` prints a whole table entry with its page: a unit's
  gold/resources/recruitment points and stats, a spell's row (and summoned creature stats), a
  ritual's description, an item. Example: `lookup.py "wind rider"`. The manual's tables only cover
  part of the game: for any vanilla unit, spell, item, site, nation or event with full stats and
  ids, use the `dom6-inspector` skill (`scripts/inspector.py unit "wind rider"`).
- `scripts/combat_calc.py table` (reproduces the page-13 odds) and
  `combat_calc.py melee --att --def --dmg --prot [...]` (hit chance, shield hits, mean damage per
  attack). Use it to check a mod unit against a vanilla one.
- `community-research.md`: rules the manual doesn't spell out, from illwiki (mostly Loggy's
  Dom5 disassembly): exact morale checks and the hidden "morale problems" counter, scout report
  error (scout ±30%, spy ±10%, scrying 0%), when the enemy AI burns gems, experience gain,
  spell timing ±500 ticks, the full Dom6 turn order, province defence thresholds. More in the
  dom6-wiki skill (`wiki.py`).
- Where things are: rules 13-89; nation lore 89-98; magic items 99-117 (path boosters 116);
  battle spells 118-140 (divine 131-132, unholy 136); summoning rituals 141-207; global
  enchantments 208-216; other rituals 217-240; nation index 241-429 (each nation: summary, then
  commanders and units with Gold, Res, Rec and full stats, then mounts); launch options 430-433.
- Row codes in the tables: `Mag: S1?2` = Astral 1 plus random picks, `Sacr` sacred, `Rec`
  recruitment points, `CS` combat speed, `MM` map move, AN armour negating, AP armour piercing,
  MR / MR- resisted / easily resisted, BE battlefield enchantment, NUW not underwater.
