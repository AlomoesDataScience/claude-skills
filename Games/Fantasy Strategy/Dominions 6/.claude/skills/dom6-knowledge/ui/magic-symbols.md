# Magic symbols

The path symbols on unit screens, the pretender design screen, spells and gems. Pictures in
`img/` (path_* = pretender screen on parchment, unit_magic_* = unit screen on dark). Templates of
the same names are in dom6-ui (`vision.py find`).

## The paths

The manual (p. 73): nine paths. Elemental: Fire, Air, Water, Earth. Sorcery: Astral, Nature,
Death, Glamour (new in Dom6: illusions, dreams, luck). Blood is outside both. Eight gem types,
one per path except Blood (blood magic uses blood slaves). Priests have the Holy path. *(manual, 2026-10-26)*

| Symbol | Path | Mod letter / #magicskill | Picture |
|---|---|---|---|
| Flame | Fire | F / 0 | img/path_fire.png, img/unit_magic_fire.png |
| White cloud | Air | A / 1 | img/path_air.png |
| Blue drop | Water | W / 2 | img/path_water.png |
| Golden hammer | Earth | E / 3 | img/path_earth.png, img/unit_magic_earth.png |
| Blue-white star | Astral | S / 4 | img/path_astral.png |
| Purple skull | Death | D / 5 | img/path_death.png |
| Green tree | Nature | N / 6 | img/path_nature.png |
| Pink crystal | Glamour | G / 7 | img/path_glamour.png |
| Red bowl dripping blood | Blood | B / 8 | img/path_blood.png |
| Lit candelabra (5 flames) | Holy (priest) | H / 9 | img/unit_magic_holy.png |
| Yellow ? | Random magic skill | U (inspector) / #custommagic | img/unit_magic_random.png |
| Stack of books + number | Research ability | R (inspector) | img/unit_research.png |

*(pretender screen, unit screen, manual, dom6-modding; 2026-10-26)*

## On the unit screen

- Row under the gear slots: each path the unit has, as symbol + level ("1", "2"), then the
  yellow ? + a number, then books + research points, then the ability icons. *(game screen, 2026-10-26)*
- Hover tooltips (bottom of the screen): "fire mage level 1", "earth mage level 2", "priest
  level 2", "random magic skill", "Research ability: 11". Path symbols, the books and the gear
  slots have only a tooltip, no right-click popup. *(game screen, 2026-10-26)*
- **The yellow ? (random magic skill) is the important one.** Right-click opens "Random magic":
  a table with Possible paths (path symbols), Level (+1) and Chance (percent), one row per
  random pick. The number after the ? on the screen is 0 here. Master Smith: Fire/Air/Earth/
  Astral +1 at 20%; Black Priest: the same four at 10%. These are the #custommagic picks: each
  recruited unit may roll an extra level. *(game screen + user, 2026-10-26)*
- The Black Knight (no magic) has no magic row: just the ability icon. *(game screen, 2026-10-26)*

## Reading them

- Hover each icon and read the tooltip (dom6-knowledge `scripts/probe.py --icons`): exact names
  and levels. Templates are a quick first guess: unit_magic_fire/earth/holy/random/research
  match exactly on unit screens; the pretender-screen path_* templates do not match on the dark
  unit screen (different drawing/background; Earth only at 0.05). Add unit_magic_<path> when a
  unit with that path is met. *(Claude, 2026-10-26)*
- Indirect magic effects of each path (leadership, resistances, age): dom6-mechanics.
  Master Smith: Fire 1 gives +10 leadership and −2 max age, Earth 2 + Fire 1 give 30 magic
  leadership (inspector breakdown). *(inspector, 2026-10-26)*

## Random magic rows

- Each row of the Random magic popup is one roll: the path symbols it can pick from, the level and the chance. The Arch Theurg has two rows over Fire/Air/Water/Astral: +1 at 100 percent (always one extra level) and +1 at 10 percent. A 100% row means a guaranteed but random path. *(game screen, 2026-10-27, 2026-10-27)*
