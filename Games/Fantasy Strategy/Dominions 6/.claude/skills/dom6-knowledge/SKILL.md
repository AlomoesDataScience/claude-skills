---
name: dom6-knowledge
description: "Claude's Dominions 6 knowledge base learned from the running game: nation files, screens, icons, magic symbols. Use when looking up something learned in game, when the user teaches a screen or icon, or after reading a new screen."
keywords: "itself, nations, overview, written, dom6-nations, work, info, unit, stat, mean, right-clicking, shows, facts, markdown, topic, list, show, search, add, dated, source, before, symbol, works, asked, knows, has"
---

# Dominions 6 knowledge base

What Claude learned **from the game and from the user**, kept so it is not re-learned. Vanilla
numbers belong to dom6-inspector, rules and formulas to dom6-mechanics; this holds what those do
not: what the game's screens show and mean, nation texts as the game shows them, and the user's
explanations.

```
scripts/kb.py topics                          # every topic file
scripts/kb.py show ui/unit-screen             # one topic
scripts/kb.py search magic icon               # lines with all the words
scripts/kb.py add ui/unit-screen "Icons" "FACT" --source "user"   # a dated fact under a section
scripts/kb.py new ui/magic-symbols "Magic symbols" "What each path symbol means"
scripts/probe.py --icons [--gear]             # on an open unit screen: sweep the icon rows, probe each icon
scripts/probe.py "Maul=542,505" ... [--no-click] [--json OUT]   # chosen points
scripts/siteodds.py --freq 40                 # Dom6 expected sites per province by path, terrain, searcher level
```

`probe.py` drives the game (dom6-ui guard): it hovers each point and reads the tooltip at the
bottom of the screen, then right-clicks it, reads the popup and closes it with the popup's Exit.
`--icons` finds the icons by sweeping the mouse along each icon row (`sweep()`, every 5 px):
each change of tooltip is a new icon. Icons touch and overlap (Sacred and Grand Communicant on
the Acolyte), so splitting at blank columns (`icon_points`) misses some; use the sweep.

## Layout

- `nations/OVERVIEW.md` - table of every nation read, by era (dom6-nations writes it).
- `nations/<ERA>/<slug>.md|.json|img/` - one nation: description, features, sprite counts,
  inspector lists.
- `plans/` - plans for games (research and items), e.g. `ma-pythium-research.md`.
- `play/strategy.md` - strategy lessons the user teaches.
- `play/site-searching.md` - expected site finds by terrain and searcher level: Dom6 tables from
  `siteodds.py` and the Dom5 illwiki chart (images in `play/img/`).
- The illwiki (Dom5 community wiki) mirror is at `Games/Fantasy Strategy/Dominions 6/illwiki/pages/` as raw DokuWiki
  text (`fetch.sh` refreshes it). Dom5 facts: check against Dom6 data before use.
- `ui/` - screens and symbols: `nation-info-screen.md`, `unit-screen.md`, `unit-popups.md` (every right-click popup), `unit-icons.md` (gear slots, ability and damage icons,
  tooltips), `magic-symbols.md` (paths, holy, random ?, research). Templates in dom6-ui.

## Rules

- Write facts as plain statements with their source: `--source "user"`, `"game screen"`,
  `"inspector"`. Add the date (kb.py does). Say when something is a guess.
- When the user explains something, add it here right away, in the user's terms, and check it on
  the screen when possible.
- Before reading or clicking through a screen, `kb.py search` it: the answer may be known.
- Keep one topic per screen or subject; add pictures (`img/`) for icons, cropped from shots.

## Standards (audit 2026-11-03)
- **Modded games:** numbers here are vanilla - check the mod first (dom6-scbm for SCBM; mod-docs).

## Related skills
dom6-nations, dom6-wiki, dom6-mechanics, dom6-tooltips, generalize-learning.
Also (2026-11-03): rules-skills, dom6-mechanics, order of truth (manual-first).
