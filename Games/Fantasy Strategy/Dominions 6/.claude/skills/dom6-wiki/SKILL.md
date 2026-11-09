---
name: dom6-wiki
description: "Local mirror of illwiki (the Dominions community wiki, Dom6 and Dom5) with wiki.py to search and read it. Use when the community wiki might answer it: a nation's strategy, an ability, a mechanic."
keywords: "com, pages, top, level, old, under, show, page, section, clean, text, list, page's, sections, category, nations, unit, abilities, mechanics, magic, schools, guides, research, loggy, plus, catalogue, covers, skill, part, feeds, dom6-knowledge, distilled, lessons, dom6-inspector, check, claims, against, game, data, question, answered, works, morale, stealth, scout"
---

# Dom6 wiki

**What it holds:** the whole of illwiki, the Dominions community wiki, mirrored as raw DokuWiki
text, and `wiki.py` to search it and read pages as clean text. The user asked for the mirror
on 2026-10-28 ("Feel free to download the entire wiki").

**What it doesn't do:** it isn't game data. Numbers come from the dom6-inspector skill, and
rules from the manual (dom6-mechanics). The wiki adds player experience and
reverse-engineered mechanics.

## Files

- `scripts/wiki.py`:
  - `search WORDS [--ns top|dom5|all|PREFIX] [-n N]`: pages containing all the words, ranked,
    with a snippet;
  - `show PAGE [--section TEXT] [--raw]`: a page or one section;
  - `toc PAGE`: sections with their sizes, so you can read the big pages in pieces;
  - `list [CATEGORY]`: nations, abilities, magic, mechanics, guides, research, dom5;
  - `grep REGEX [--ns ...] [-n N]`: matching lines with their page.
  PAGE is a path without `.txt`, or a unique substring of one.
- **The mirror:** `Games/Fantasy Strategy/Dominions 6/illwiki/`:
  - `pages/` (1,347 pages, 21 MB);
  - `pages.txt` (the page list);
  - `fetch.sh` refreshes everything from `?do=export_raw`.
- Builds on the **dom6-knowledge** skill (nation files get the distilled notes).
- Builds on the **dom6-inspector** skill (to check what the wiki claims).

Run Python with `python3 -I` (system Python with PIL only; no pip).

## Workflow

1. **Check the distilled notes first** (below): the important pages are already summarised in
   the other skills.
2. **Otherwise search:** `wiki.py search WORDS`, then `toc PAGE`, then
   `show PAGE --section ...` for big pages. Add `--ns all` to include Dom5 pages.
3. **Check every number** that matters against dom6-inspector or the manual, and say whether a
   claim is Dom5 or Dom6.
4. **Write anything worth keeping** into the skill that uses it (table below), with the page
   name as the source.

## Where the wiki has been distilled (2026-10-28)

| Wiki pages | Distilled into |
|---|---|
| `user/loggy/castingai`, `castingaiexample` | dom6-tactics `ai-casting.md` (how the AI picks spells, what to script) |
| thug guide parts 1-3 (`strategy_articles/thugs/...`) | dom6-tactics `thugs.md` |
| Cybertron2 expansion guide parts 1-3 | dom6-tactics `expansion.md` (every independent type rated, party size, formations, orders) |
| `user/loggy/morale`, `scoutreports`, `gemusage`, `experience`, `casttime`; `turn-order-sequence`; `game-mechanics/province-defence` | dom6-mechanics `community-research.md` |
| `early_and_midgame_magic`, `fearbattleenchantments`, `globals` | dom6-spells `community-notes.md`, `rituals.md` (globals section) |
| `basics_of_higher_level_pretender_design` | dom6-pretender `SKILL.md` ("What strong players do") |
| `pythium-ma`, `dom5/pythium-ma` | dom6-knowledge `nations/MA/pythium.md` (and Contact Lar into the research plan) |
| `tir-na-n-og-ea`, `dom5/tir-na-n-og-ea` | dom6-knowledge `nations/EA/tir_na_nog.md` (the user's MP nation) |
| `magic-sites`, `user/loggy/sitegeneration` | dom6-knowledge `play/site-searching.md`, `scripts/siteodds.py` |
| `wiki/common_beginner_mistakes` | below, under "Beginner mistakes" |

**Not yet distilled; read on demand:**
- the school pages (`alteration`, `evocation`, `enchantment`, `conjuration`, `thaumaturgy`,
  `construction`, 60-90 kB each, with community commentary on every spell);
- `magic-access` (how each nation reaches each path);
- `unit-abilities` and the 176 ability pages;
- `stacking-effects-bob`, `pretender-titles`, `thrones`, `patchnotes`;
- Loggy's `indies-ea/ma/la` (every independent province type with its troops; ~380 kB each:
  use `grep`), `freespawn`, `horrors`, `horrormark`, `afflictions`, `age-decay`, `auras`,
  `longdead`, `combatsim`, `indepspells`, `misc`;
- the other 114 nation pages.

## Beginner mistakes (the wiki's list, condensed)

- **Expansion:**
  - test expansion against the AI first (aim for about 20 provinces in the first year);
  - split armies to take several provinces a turn.
- **Mages:**
  - don't bring mages to fights they can't swing early; research and site-search with them;
  - **bring dozens with gems to big midgame battles**, with scouts carrying gems.
- **Script** armies and mages; give commanders bodyguards against fliers.
- **First fort around turn 7** (not for every nation). Build temples in forts or far from the
  front.
- **Don't lose a war with gems in the bank.** Spend them; site-search early.
- **Never leave a province at 0 province defence** (a scout can take it); big dumps rarely
  help.
- **Make enough scouts.** They also carry gems, build forts and ping armies.
- **Be decisive:** pull mages into a war if it ends it faster. **Avoid sunk-cost wars**:
  make peace if a third player is growing.

## Facts and gotchas

- **Top-level pages are Dom6. `dom5/` is the old wiki**, often with more player commentary
  (most Dom6 nation pages have empty strategy sections). Costs and stats changed between
  versions.
- **Loggy's `user/loggy/*` pages are Dom5 disassembly** (5.53-5.60). Very useful, but label
  them as Dom5.
- **`clean()` drops DokuWiki path icons** (`{{...}}`), so path letters in tables often vanish
  ("Theurg A1" can show as "Theurg"). Use `--raw` to see the icon names, or check the
  inspector.
- **Tabboxes** (`<tabbox ...>`) are kept as tags in the text; pipe through
  `sed 's/<\/\?tabbox[^>]*>//g'` to strip them.
- Python's broken pipe on `| head` is harmless.

## Standards (audit 2026-11-03)
- **Modded games:** numbers here are vanilla - check the mod first (dom6-scbm for SCBM; mod-docs).

## Related skills
dom6-mechanics, dom6-inspector, wiki-scout.
Also (2026-11-03): video-watch, wiki-scout, rules-skills (order of truth: manual > videos > wiki).
