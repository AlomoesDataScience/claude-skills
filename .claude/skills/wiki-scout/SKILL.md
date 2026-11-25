---
name: wiki-scout
description: "Find and pull wikis, manuals and docs for a game or franchise as safe text (Wayback first) with scout.py. Use when a game or IP needs its wiki or documentation fetched."
keywords: "wiki, wikis, wikipedia dump, dumppass, xml dump, multistream, scrape, scraping, fandom, wiki.gg, paradox wiki, strategywiki, pcgamingwiki, wikipedia, wayback machine, archive, snapshot, mediawiki api, ip wiki, franchise, index, portal, topic index, tier, docpull, publisher pages, errata, play aids, virus check, plain text, textpull, any web page, gutenberg, wikisource, online book, chapters, robots.txt, crawl-delay, bot check, polite scraper, google scraper"
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
scout.py index https://en.wikipedia.org/wiki/Category:Capitalism wiki/capitalism   # index first (below)
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

## Any page or online book: `scripts/textpull.py`

The user (2026-11-16): "don't be rude and kill their website"; "if something checks for AI, don't try to
bypass it. That's rude, we're good people here."
```
textpull.py check URL                                  # robots.txt verdict + Crawl-delay
textpull.py links URL [--follow REGEX]                 # dry run: the same-site links a book pull would take
textpull.py get URL OUTFILE                            # one page or .txt (Gutenberg, Wikisource) -> text
textpull.py book URL OUTDIR --follow REGEX [--pause 4] [--max 200]   # index + chapters, ALL.txt, SOURCE.md
```
It reads robots.txt per host, waits the larger of --pause and Crawl-delay, sends one request at a time
with a generic User-Agent, and **stops** on 401/403/429/503 or a visible bot check. Used 2026-11-16 for
Sirlin's Playing to Win and Keynes' General Theory. **No search command:** Google and Bing disallow
`/search` and DuckDuckGo drops scripts, so find URLs with WebSearch (or an official search API with
The user's key), then pull them.

## Whole-Wikipedia dump pass: `scripts/dumppass.py`

The user (2026-11-16) chose the dump in parts for the battles pull, then widened it: "we'll grab everything we
think we want now". It downloads the enwiki pages-articles parts (71, plain: the sha1 list has no multistream) one at a time with the WMF policy User-Agent,
checks the sha1, catalogues every article and keeps the whole text (the user, after the trial: keep everything). It sorts:
field matches from `dump-rules.json` -> `text/`, every other article -> `rest/` (with the reason), Template/Category/
Portal pages -> `other/` (campaignboxes, navboxes); `catalogue/` lists all. It checks the row counts, then deletes
the part (rm: The user's rule for dump parts). Plan: `plans/wikipedia-dump-pull.md`.
```
dumppass.py sums OUT PARTS ; dumppass.py run OUT PARTS --parts 1,36 --keep ; dumppass.py report OUT
dumppass.py extract OUT PARTFILE      # retune dump-rules.json on a kept part, no requests
```
Reading the dump: `scripts/dumpget.py DUMP --find REGEX` lists titles. `dumpget.py DUMP OUTDIR "Title" ...` writes
whole articles as `.wiki`, following redirects, with no requests (about 1 minute per call, so batch titles).

## Order of sources (gentlest first)

1. **Wayback Machine** snapshots (`id_` raw pages): the wiki itself gets no traffic. Newest
   snapshot first, falling back a year at a time when a snapshot is a bot-check page (the Stellaris
   wiki's 2026 snapshots are).
2. Published dumps or downloads if the wiki offers them (Fandom's Special:Statistics dumps, a
   game's own manual PDF in the install): one request instead of thousands.
3. **Live MediaWiki API** (`live`): parsed text through api.php, honest User-Agent naming this
   workspace, robots.txt obeyed, `maxlag=5`, a pause between pages. Never disguise the client or
   get around a bot check. If a site actively refuses scripts (403, Cloudflare, captcha), don't fetch
   its archive copy either (2026-11-16, TV Tropes: that counts as routing around the block); ask the user
   to save the page by hand into `Needs Review and Cataloguing/`.
   **Wikimedia sites (Wikipedia, Wikidata; the user sent the policy 2026-11-16):** en.wikipedia.org's robots.txt
   disallows `/w/` (so `api.php`, except action=mobileview) and `/api/` for all bots, and welcomes "friendly,
   low-speed bots ... viewing article pages". The Robot policy (wikitech.wikimedia.org/wiki/Robot_policy)
   adds: one request at a time, under 5 per second; wait 5 s after any request that took over 1 s; respect
   Retry-After on 429; prefer dumps for bulk. So: no live api.php on Wikipedia without the user's ruling;
   wdpull.py now refuses it (robots check). Lesson: the battles pull (19 api.php requests, 3 s pause) broke
   both and drew a 429; check robots.txt for every script and host before the first request, not after.
   Per-host digests, saved robots.txt copies and the User-Agent collision check: **site-rules** skill.
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

## Topic scrapes: drop the index first (the standard)

The user (2026-11-15), on the economics and capitalism scrape: "we're going to scrape the index ... make
standards for wiki scraping in the wiki project, like just drop the wiki index." The war index is the
worked example (war-concepts, `warwiki.py`); `scout.py index URL OUTDIR` does steps 1 and 2 for any index, portal or
category page (Category:Capitalism, 2026-11-15: 114 articles, 7 subcategories listed and not followed).
1. **Drop the index page.** Save the topic's index or portal page as it is (`Index_of_..._articles.wiki`,
   `Portal:Capitalism`) into the topic's `wiki/` folder. This is the source of truth for what the topic covers.
2. **Build the index file.** Write `<topic>-index.json` with one entry per linked article: title, short
   description, first two sentences, and `missing` if the article doesn't exist. Short extracts only, so it stays cheap.
3. **Tier it.** A = concepts we use for playing or designing games (pull the full text), B = specific
   examples (fetch on demand), C = not useful. Claude triages and the user can re-tier.
4. **Pull the A tier only**, as text, into `wiki/<topic>/`. Then `check` and `record` (SOURCE.md).
5. Go one level deeper (links of links) only when the user asks. The index decides the scope.

## Where it goes

- A game's wiki: `<game folder>/wiki/` (text) + `SOURCE.md`; note it in the game's guide skill.
- An IP or franchise wiki: `IPs/<IP>/wiki/` (top level, with the user's own settings; Gundam first).
- Community wiki text is for Claude's reading: summarise in Claude's own words, don't republish.

## Related skills
site-rules (what each host's robots.txt and bot policy allow; check before the first request),
game-sources (manuals and wikis as text), manual-first (manual before wiki), library-intake, learn-to-play, learn-to-mod,
war-concepts (the war index: the worked index-first example), economic-theory (Portal:Economics pull), dom6-wiki (the illwiki mirror),
ww2 (the WW2 group reads the dump with dumpget.py)
