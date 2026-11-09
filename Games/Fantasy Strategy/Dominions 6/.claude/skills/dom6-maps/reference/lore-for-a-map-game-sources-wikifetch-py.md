# dom6-maps - Lore for a map (game-sources wikifetch.py and the LORE layer, 2026-10-29)

Part of the dom6-maps skill; SKILL.md links here.

## Lore for a map (game-sources wikifetch.py and the LORE layer, 2026-10-29)

- Lore wikis are read with the generic `game-sources` skill (`wikifetch.py` in the project's root
  `.claude/skills/game-sources/scripts/`): Wayback fetching for Cloudflare sites, page text, links,
  fact boxes (`infoboxes OUTDIR OUT.json`), or the MediaWiki API (`allpages`, `api`).
- Greyhawk lore now lives with D&D: `Games/Tabletop RPGs/Dungeons & Dragons/Worlds/Greyhawk/lore/`
  (Flanaess.html/.txt, `pages/` 143 pages, `infoboxes.json` 89 fact boxes) and the source pictures
  in `.../Worlds/Greyhawk/maps/` (`Greyhawk HD.png`, `Greyhawk.jpeg`). The `greyhawk-lore` skill
  there (`lore.py realm/list/search`, `realms.md`) is the quick way to the realm facts.
- `from_image.py` gives every province a realm (`self.realm`: its own label, or the nearest label
  for fill provinces). Config fields read by `province_lines` (written as `#setland` blocks at the
  end of the .map, after the `#pb` lines; mapgen.py's `province_lines(num)` hook):
  `LORE = {label: {"poptype": n, "people": realm population, "fort": n, "climate": "cold"|"warm"}}`
  (population spread over the realm by area, towns ×1.35 and capitals ×2 weight, `POP_SCALE`
  default 0.02, clamped 500-40000, never on start provinces; forts only where a capital symbol is),
  `SITE_FEATURES = {adventure number: [vanilla site ids]}` → `#feature id`. Climate from LORE
  replaces the picture's warm/cold bits before starts are chosen.
- Status: written and parsing, **not yet run** - the Greyhawk LORE table is still to be filled from
  infoboxes.json. Poptype numbers are in the map manual's table (`#poptype`), site ids from
  dom6-inspector (`records/sites.jsonl`). Picks so far: Temple of Darkness 843 (Temple of Elemental
  Evil), Tomb of the Grand Thaumathurg 822 (Tomb of Horrors), Slave Market 1073 (Slave Pits),
  Jungle Temple 872 (Tamoachan), The Forgotten City 732 (Forbidden City), Abandoned Laboratory 692
  (In Search of the Unknown), Circle of Standing Stones 643 (Shattered Circle), Frost Vale 544
  (Glacial Rift), Castle Arcanum 640 (Castle Greyhawk).
