---
name: wiki-scout
description: Find and pull the wikis, manuals and documentation for a game or a franchise (IP), gently and as safe text. scout.py finds where a wiki lives (Fandom, wiki.gg, Paradox wikis, StrategyWiki, PCGamingWiki, Wikipedia) through the Wayback Machine with no requests to the wiki, lists its archived pages, pulls the newest good snapshot of each as plain text (scripts and ads dropped, resumable), falls back to the live MediaWiki API only for missing pages (honest User-Agent, robots.txt, maxlag, slow), checks the output is plain text and records the source. docpull.py pulls every rules PDF, errata, play aid and module linked from a publisher page (GMT and the like), checks file types, unpacks archives safely and makes text of each PDF. Use when a game or IP needs its wiki or documentation fetched, when the user names a wiki, franchise or publisher page to pull, when a folder is empty but the user owns the game, or when a site blocks scripts or is full of ads.
---

# Wiki scout

The user (2026-11-01): build a tool to find and pull every game's wiki and documentation; "pull from
wayback machine first or trying to make your fetch requests easier on the dev side of things,
because supposedly all the wikis are seeing a lot of fetch level traffic." Also pull **IP-level**
wikis (franchises such as Gundam) for genre and setting knowledge. Fandom is "littered with the
most cursed ads, and what you get needs to be checked for viruses."

## Commands (`scripts/scout.py`)

```
scout.py find "Gundam" "Stellaris"                   # which wikis exist (archived), no wiki traffic
scout.py titles https://gundam.fandom.com/wiki/ all-titles.txt [--prefix Zaku] [--limit N]
scout.py pull https://gundam.fandom.com/wiki/ titles.txt wiki [--pause 4] [--max 200]
scout.py live https://gundam.fandom.com/api.php wiki/missing.txt wiki    # only for what Wayback lacks
scout.py check wiki                                   # all plain text, no script/iframe left
scout.py record wiki https://gundam.fandom.com/wiki/  # wiki/SOURCE.md
```
Run long pulls in the background; the archive allows about one request a second, so the default
pause is 4 s (about 900 pages an hour). `pull` skips pages already saved, so it resumes.

## Publisher pages: `scripts/docpull.py`

The user (2026-11-01): "GMT games has all the resources for all their games online... make a program
to pull manuals from websites like this."
```
docpull.py links "https://www.gmtgames.com/p-1165-the-us-civil-war-3rd-printing.aspx"   # files + sizes
docpull.py pull  "<page>" "<game folder>/gmt" [--only RULES] [--skip _JP|_Ko] [--wayback]
```
It finds every pdf/zip/doc/rtf/vmod/ztb link on the page, downloads each once (one request per
file, pause between), checks the real type with `file` (a mismatch is quarantined as
`.unexpected`), unpacks zips into their own folder keeping only documents, images and game
modules (no programs, no `..` paths), makes a `.txt` of every PDF with manual.py (scans need
ocr.py), and appends to `SOURCE.md`. GMT keeps its files at `gmtwebsiteassets` on Amazon S3.
Put the page link in the game's `Resources` file too.

## Order of sources (gentlest first)

1. **Wayback Machine** snapshots (`id_` raw pages): the wiki itself gets no traffic. Newest
   snapshot first, falling back a year at a time when a snapshot is a bot-check page (the Stellaris
   wiki's 2026 snapshots are).
2. Published dumps or downloads if the wiki offers them (Fandom's Special:Statistics dumps, a
   game's own manual PDF in the install): one request instead of thousands.
3. **Live MediaWiki API** (`live`): parsed text through api.php, honest User-Agent naming this
   workspace, robots.txt obeyed, `maxlag=5`, a pause between pages. Never disguise the client or
   get around a bot check; if a site refuses, use Wayback, WebFetch for single pages, or ask the user.
4. Finding a wiki `find` doesn't know: the WebSearch tool in the session (not scraping Google),
   then `find`'s checks on the URL found.

## Safety (the user: check for viruses)

- Only text is kept: `pull` converts each page to `.txt` (+ `.infobox.json`) and deletes the HTML;
  with `--keep-html` the HTML is stripped of scripts, iframes, embeds and event handlers and saved
  as `.html.txt` so nothing opens it as a page. No images, PDFs or executables are downloaded by
  default. Nothing fetched is run or opened in a browser.
- `check` confirms every file is UTF-8 text with no script or embed left. No virus scanner is
  installed (ClamAV absent); plain text cannot run, which is why the rule is text only.
- A PDF or archive from a wiki is fetched only when needed, into its own folder, and opened with
  the manual tools (`manual.py`, `pdftotext`), never executed.

## Where it goes

- A game's wiki: `<game folder>/wiki/` (text) + `SOURCE.md`; note it in the game's guide skill.
- An IP or franchise wiki: `Games/IP Wikis/<IP>/wiki/` (Gundam first).
- Community wiki text is for Claude's reading: summarise in Claude's own words, don't republish.
