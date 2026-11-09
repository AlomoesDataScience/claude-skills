---
name: game-sources
description: "Turn a game's manuals and wikis into searchable page-numbered text and list the user's Steam library (steamlib.py). Use when starting a new game, looking up a rule in a manual, or when a manual is dropped."
keywords: "written, something, search, pdfs, chapter, outline, bookmarks, printed, table, contents, headings, font, size, grep, page, lookups, wiki, lore, sites, mediawiki, fetched, html, infobox, facts, through, wayback, machine, site, blocks, downloads, wikifetch, scanned, game-ui's, ocr, read, screen, drops, names, gives, cloudflare, curl, webfetch"
---

# Game sources: manuals and wikis

Every game starts from its written sources. Get them into text once, keep the text next to the
source in the game's folder, then search it instead of re-reading.

## Manuals (`scripts/manual.py`)

```
manual.py info MANUAL.pdf               # pages, bookmarks or not, text layer or scanned
manual.py text MANUAL.pdf [OUT.txt]     # page-numbered text next to the PDF ("=== page N")
manual.py outline MANUAL.pdf [--depth N]  # bookmarks; none -> headings by font size
manual.py toc MANUAL.txt [--pages N]    # the printed table of contents ("title ... page")
manual.py grep MANUAL.txt "supply|morale" [-C 2]   # hits with page numbers
manual.py page MANUAL.txt 37 [40]       # read pages
```

- Order: `info` → `text` → `outline` (or `toc` when there are no bookmarks and the font fallback
  only finds titles, as in Space Empires IV and War in the Pacific) → read the overview and core
  rules chapters → write the game's starter skill → `grep` for details as they come up.
- **Scanned manual** (`info` says little or no text layer; Emperor of the Fading Suns):
  `python3 -I <root>/.claude/skills/game-ui/scripts/ocr.py pdf MANUAL.pdf` (300 dpi, ~5 s a page),
  then use `grep`/`page` on its .txt as usual. OCR text has errors: check numbers that matter
  against the page image (`pdftoppm -f N -l N -r 150 -png`).
- PDF page numbers (what `page` and `grep` use) differ from the printed page numbers in the
  manual's own contents: note the offset in the game's skill.
- Text with `-layout` keeps table rows on one line; columns of two-column manuals can interleave,
  read those pages from the image if a passage looks garbled.

## Wikis and lore sites (`scripts/wikifetch.py`)

```
wikifetch.py fetch BASE_URL TITLES.txt OUTDIR [--year 2025] [--pause 4]
wikifetch.py text PAGE.html [OUT.txt] | textall OUTDIR
wikifetch.py links PAGE.html [SECTION_ID]     # wiki titles a page (or one section) links to
wikifetch.py infobox PAGE.html | infoboxes OUTDIR OUT.json   # the fact boxes
wikifetch.py allpages API_URL OUT.txt            # every page title via the MediaWiki API
wikifetch.py api API_URL TITLES.txt OUTDIR       # each page's wikitext as OUTDIR/<title>.wiki
```

- Try the API first (`https://<site>/api.php`, fandom wikis have it): it often answers when the
  HTML pages give 403, and returns clean wikitext. Example: the Gihren's Greed wiki
  (`Games/Wargames/Gihren's Greed/sources/`). Falls back to Wayback when the API is blocked too.

- For MediaWiki sites (fandom wikis, greyhawkonline). Sites behind Cloudflare (403 "Just a
  moment" for curl and WebFetch) are read from the Wayback Machine (`web.archive.org/web/<year>id_/URL`):
  pages arrive gzip-compressed (handled), the archive rate-limits at about 1 request/s (4 s pause,
  back-off on 429), pages never archived come back 404.
- Build TITLES from an overview page's links (`links`), plus the names you need (map labels,
  units). Underscores for spaces.
- `infoboxes` gives the facts (capital, population, races, resources...) as JSON: the quick way to
  turn lore into game data. Keep the HTML: it is the source.
- Lore and wiki text is the authors' work: keep it as local reference, summarise it in your own
  words in skills, quote only short bits.
- Example: the Greyhawk lore (D&D) in `Games/Tabletop RPGs/Dungeons & Dragons/Worlds/Greyhawk/lore/`
  (Flanaess overview + 143 pages, infoboxes.json).

## Where things go

`<Genre>/<Game>/` holds the manual and its .txt; `<Genre>/<Game>/.claude/skills/<prefix>-guide/`
is the starter skill (what the game is, manual map with page numbers, core rules in Claude's
words, open questions). See learn-to-play for the whole method.

## the user's Steam library (steamlib.py)

`scripts/steamlib.py list [--type game] [--min-hours H] [--sort hours|name|recent]` prints every app
The user has played or owns with hours and last-played date; `steamlib.py installed` lists installed
apps. It reads the local Steam client files only (appcache/appinfo.vdf for names and types,
userdata/<id>/config/localconfig.vdf for playtime): nothing is written, nothing goes online.
2026-11-01: 525 games. SteamDB (web) adds details, tags and the full catalogue when the user gives access.

## Related skills
manual-first (lookup.py builds on manual.py), wiki-scout (wikis and publisher docs), library-intake (where files go), learn-to-play, learn-to-mod
