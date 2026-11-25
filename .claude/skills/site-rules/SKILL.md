---
name: site-rules
description: "What each website we pull from allows bots: robots.txt and bot policy per host, dated copies, sitecheck.py for User-Agent collisions and path verdicts. Use before the first request to any host, and before any bulk pull."
keywords: "robots.txt, robot policy, bot policy, crawl-delay, rate limit, 429, retry-after, user-agent, user agent policy, wikipedia, wikimedia, wikidata, sparql, query service, api.php, rest api, wayback, archive.org, dumps, allowed paths, disallow, sitecheck, polite scraping, scraping rules, site rules"
---

# Site rules - what each site lets our scripts do

The user (2026-11-16), after the battles pull drew a 429: "I found their standards.
https://wikitech.wikimedia.org/wiki/Robot_policy"; then "Obviously look at and inform me of anything that's
relevant from robots.txt", "As a skill". **Rule:** no script makes its first request to a host until that
host has an entry here and the paths it will use say ALLOW. How to pull is in wiki-scout. This skill covers
what each site permits.

## Method (once per host, then per new path)
1. **Fetch robots.txt once** (one request; `textpull.py check URL` or curl with our generic UA). Save it as
   `robots/<host>-<date>.txt`. A 404 means none: allowed, but still read the site's own policy.
2. **Read it locally:** `python3 -I scripts/sitecheck.py robots/<file> URL...`. It shows the comments addressed
   to bots, Crawl-delay values and which bot each applies to, the bots blocked outright, an ALLOW/DENY verdict
   for each URL for every one of our User-Agents, and **COLLISIONS**.
3. **Collisions:** Python's robotparser matches a listed bot name as a *substring* of our UA's first word.
   On 2026-11-16, `docpull` matched Wikipedia's blocked bot "DOC" and `wikifetch` matched "Fetch". Both were
   renamed (`filepull`, `wikitext`). Name new scripts so they match no listed bot, and rerun sitecheck after
   any rename.
4. **Read the site's bot/API policy** if it has one: rate, concurrency, contact info, preferred bulk route.
   robots.txt doesn't hold those.
5. **Write the host entry below:** allowed paths, denied paths we would want, rate, bulk route, and the date.
   If a path we need is denied, stop and ask the user. Never route around it (wiki-scout rule).

## Hosts

### api.nuget.org (robots.txt 2026-11-16: 404, none)
- NuGet's package API, used only through `dotnet restore` / `dotnet add package` (its own client, the
  intended route). Allowed: no robots.txt (`robots/api.nuget.org-2026-11-16-404.txt`). Packages are
  pulled once into ~/.nuget/packages and then come from the cache. Only packages the user has seen named
  (4X engine renderer test, plan step 18: Silk.NET.OpenGL, Raylib-cs). No scraping of nuget.org pages.

### github.com / api.github.com (robots.txt 2026-11-16; api: 404, none)
- github.com robots.txt (`robots/github.com-2026-11-16.txt`): repo pages and blobs are allowed for `*`.
  It blocks some named bots (Bytespider and others, none ours) and says "If you would like to crawl
  GitHub contact us", so no crawling. api.github.com has no robots.txt (`robots/api.github.com-2026-11-16-404.txt`).
  The REST API is GitHub's intended route for automated reads.
- Use: single API reads of a named repo (licence, file list, one file), as the user asked (sound plan,
  2026-11-16: the Engine-Simulator licence check). Unauthenticated limit: 60 requests an hour. Stop on 403/429.
  No bulk cloning or walking whole orgs without the user's OK. A `git clone` of one repo he named is fine.

### share.google / www.google.com (robots.txt 2026-11-16)
- `share.google/<id>` (Gemini / AI Mode share links) has no robots.txt of its own: it 302-redirects to
  `www.google.com/share.google?q=...`. google.com's robots.txt DENIES `/share.google` and `/search` to all
  our User-Agents. **Do not fetch.** Ask the user to paste the conversation text instead (2026-11-16).

### en.wikipedia.org (robots.txt 2026-11-16, Robot policy read 2026-11-16)
- **Allowed:**
  - article pages `/wiki/Title`. robots.txt: "Friendly, low-speed bots are welcome viewing article pages, but
    not dynamically-generated pages please." These are served from cache, so they cost the site least.
  - `/w/api.php?action=mobileview&...`, the one API exception (untested; it may no longer exist in MediaWiki).
  - `/w/load.php`, `/api/rest_v1/?doc` (documentation only), and the sitemap
    `/w/rest.php/site/v1/sitemap/0`, which lists article URLs.
- **Denied to all bots:**
  - `/w/`, which covers api.php (query, parse, revisions, extracts), index.php?action=raw, and history.
  - `/api/`, the REST page and HTML API.
  - `/wiki/Special:` (Export, AllPages, Search, Random).
  - `/trap/`.
  - deletion, arbitration, adminship and similar discussion pages.
- **Blocked outright by name (30 bots):** among them **wget**, **libwww**, **Fetch**, **DOC**, **fast**,
  HTTrack, WebCopier, Offline Explorer and Teleport. Don't use those tool names in any UA. The `curl` and
  `python-requests` defaults aren't listed, but always send our own UA.
- **Crawl-delay:** none for `*`. SemrushBot gets 5 s, which they describe as staying within about 20 requests
  a second to the backend across the whole site. The header warns: "If you're irresponsible, your access to
  the site may be blocked."
- **Robot policy (wikitech.wikimedia.org/wiki/Robot_policy):**
  - one request at a time, under 5 a second;
  - wait 5 s after any request that took more than 1 s;
  - honour Retry-After on a 429;
  - send Accept-Encoding gzip;
  - batch requests;
  - prefer the dumps for bulk.
  - Logged-in (OAuth) clients may use 3 at once and 10 a second. Toolforge bots aren't rate limited.
    Contact: bot-traffic@wikimedia.org.
- **User-Agent policy:** read 2026-11-16; see the foundation.wikimedia.org entry below.
- **Bulk route:** dumps.wikimedia.org (entry below).
- **Our history (be honest about it):**
  - The battles pull (wdpull, 19 api.php requests, 3 s apart) and earlier api.php use broke this robots.txt:
    `scout.py index` intros, `warwiki.py` (the war index), and `wikifetch.py api` if pointed at Wikipedia.
  - Since 2026-11-16 all four check robots.txt first and refuse a denied URL. `scout.py index` now skips the
    intros on Wikipedia.

### www.napoleon-series.org (robots.txt 2026-11-16)
- Allowed: Yoast default robots.txt, nothing blocked, no Crawl-delay (`robots/www.napoleon-series.org-2026-11-16.txt`).
  First use: the French 1791 infantry regulation (the user's drop, 2026-11-16). textpull.py, one page at a time,
  --pause 4. The articles and translations are the site's or its authors': numbers and facts in our own words, cite the page.

### manoftinblog.wordpress.com (robots.txt 2026-11-16)
- Allowed: WordPress.com default (`robots/manoftinblog.wordpress.com-2026-11-16.txt`). One post pulled
  (WW2 ranges, the user's link). Hobby blog, ranges from Wikipedia: weak secondary. Facts in our own words, cite the post.

### panzerworld.com (robots.txt 2026-11-16)
- Allowed: 3-line robots.txt, sitemap only (`robots/panzerworld.com-2026-11-16.txt`). The user: "GOOD".
  Pulled the tactical-symbols and organizational-tables pages (text; symbols are images, not pulled).
  textpull one page at a time, --pause 4. Facts in our own words, cite the page.

### www.tankarchives.com (robots.txt 2026-11-16)
- Allowed: Blogger default (`robots/www.tankarchives.com-2026-11-16.txt`). Denied: `/search`, `/share-widget`.
  Sitemap `/sitemap.xml` lists posts. The user's link (Peter Samsonov's blog, Soviet archive documents and trials).
  Not pulled yet. Use textpull one post at a time, --pause 4, and never fetch the search pages. State facts in our
  own words and cite the post.

### dupuyinstitute.org (robots.txt 2026-11-24)
- Allowed: WordPress default, denies only `/wp-admin/` and `/stats/` (`robots/dupuyinstitute.org-2026-11-24.txt`);
  no Crawl-delay, no bots named, no collisions. The user's go 2026-11-24 ("You're good to fetch them"). The Dupuy
  Institute's Kursk Data Base pages. Use textpull one page at a time, --pause 4. The KDB itself is a paid product,
  so read only what the site shows freely; never try to get past a paywall or a login.

### digicoll.lib.berkeley.edu (robots.txt 2026-11-24)
- Allowed: `/record/<id>` pages (`robots/digicoll.lib.berkeley.edu-2026-11-24.txt`). Denied: `/rss`, `/search`,
  record exports. **Crawl-Delay 5 s** for `*`; no bots named, no collisions. UC Berkeley Library digital
  collections: Kursk map sheet leads (records 104859, 265613, 269551; the user's go 2026-11-24 "getting the sheets").
  One record at a time, --pause 5 or more. Map scans: check each record's rights line before saving an image.

### eddie.lunaimaging.com (robots.txt 2026-11-24: 404, none)
- David Rumsey Map Collection's LUNA viewer. No robots.txt (`robots/eddie.lunaimaging.com-2026-11-24-404.txt`):
  allowed, but its terms are not read yet. Lead: the "Kursk" record RUMSEY~8~1~247778~5515573. One page at a time,
  --pause 5. **2026-11-24: the record page is a LUNA login wall. Do not fetch again**; the public Rumsey site
  (www.davidrumsey.com) is a separate host, not checked yet.

### apps.dtic.mil (2026-11-24) - BLOCKED, DO NOT FETCH
- robots.txt itself came back 403 "Service unavailable. The request is blocked." (CDN bot block;
  `robots/apps.dtic.mil-2026-11-24-403.txt`). Stop rule: no retries, no other UA. For a DTIC report (KDB:
  ADA384597), the user downloads it by hand and drops it in the review inbox.

### www.youtube.com (robots.txt 2026-11-16)
- **Denied to all bots:** `/api/`, `/youtubei/`, `/get_video_info`, `/timedtext_video`, `/results`, `/comment`
  and more (`robots/www.youtube.com-2026-11-16.txt`). Watch pages are not denied.
- **Ruled 2026-11-16: no scripts on YouTube.** the user: "make sure our scraper is within rules, if it's not then
  stop". yt-dlp uses the denied `/youtubei/` and `/api/timedtext`, and the Terms of Service (from memory; the
  terms page is denied to bots) forbid scraping and downloading. `video.py` now refuses remote URLs. Use local
  files, or a transcript the user pastes in.

### tanks-encyclopedia.com (robots.txt 2026-11-16) - DO NOT FETCH
- robots.txt (`robots/tanks-encyclopedia.com-2026-11-16.txt`) allows `*`, but it blocks **ClaudeBot,
  anthropic-ai and Claude-Web** by name, along with about 30 other AI bots. Its content signal is
  `search=yes, ai-train=no, use=reference`.
- We are Claude. Fetching with our generic UA would get around a block aimed at us, and the user's rule is "if
  something checks for AI, don't try to bypass it". **No requests.** the user's link was the Panther Ausf F page
  (2026-11-16). If he reads it himself and gives us numbers, cite them as "the user, from tanks-encyclopedia.com".
- **General rule:** a site that names Claude's or Anthropic's bots in a Disallow is closed to all our scripts,
  whatever UA they send.

### query.wikidata.org (robots.txt 2026-11-16)
- **Denied to all bots:** `/sparql` and `/bigdata`, which is the whole query service. The one SPARQL request
  for the battles index broke this. wdpull's robots check now refuses it.
- The query service's own usage docs aren't read yet. They may welcome API clients that send a UA, but
  robots.txt says no, and robots.txt wins until the user rules.

### web.archive.org and archive.org (robots.txt rechecked 2026-11-16)
- **web.archive.org: no robots.txt** (404 again, `robots/web.archive.org-2026-11-16-404.txt`). Python treats
  that as allow-all. Default source for wikis (wiki-scout). Their rate limit is about 1 request a second (not
  read from a policy page), so we use a 4 s pause. Their written bot policy isn't read yet.
- **archive.org** (the parent site: item pages, downloads): `User-agent: *` denies only `/control/` and
  `/report/` (`robots/archive.org-2026-11-16.txt`). No bots named, no Crawl-delay; sitecheck: all six of our
  UAs ALLOW `/details/` and `/download/`, no collisions.
- **Fixed 2026-11-16 (the user: "we need to fix it"):** `wiki-scout/scripts/scout.py` used to retry on 429/5xx
  with back-off. It now makes one request and stops the run on 401/403/429/5xx, no answer, or the archive's
  'Temporarily Offline' page. All our pullers now follow the stop rule.

- **Used 2026-11-23:** `advancedsearch.php` (one search), `/metadata/<item>` (one file list) and two
  `/download/` files (TME-30-4511945, 1945 German handbook), 4 s apart. All 200.

### www.lonesentry.com (2026-11-23) - DO NOT FETCH
- The robots.txt request came back with HTTP **465 and an "Access Denied" page** (saved as
  `robots/www.lonesentry.com-2026-11-23.txt`). That means our script is blocked before robots.txt. No resend,
  no other UA (the rule against bypassing). The user's link was the 1945 handbook's recon section
  (`/manuals/tme30/ch4sec2.html`). The same book came from archive.org instead.

### dumps.wikimedia.org (2026-11-16)
- **No robots.txt** (404). `enwiki/latest/dumpstatus.json` is 404 too (status lives in the dated run folders).
- **What's there** (directory listing `enwiki/latest/`, one request): run 20261101. The listing shows 73
  multistream parts (27.3 GB), but the run's `enwiki-latest-sha1sums.txt` (one request) lists **no multistream
  files**, only the **71 plain `pages-articles<N>.xml-p<first>p<last>.bz2` parts** (ids 1 to 84,714,711, no
  gaps, ~26 GB). Same pages, and the sha1 can be checked, so we use those, from the dated folder
  `enwiki/20261101/`. `latest/` also keeps two stale part-27 files from older runs (2 and 8 Oct); ignore them.
- **Usage rules (front page, read 2026-11-16):**
  - The **WMF User-Agent Policy is enforced** for dump downloads (read 2026-11-16, foundation.wikimedia.org
    entry below). Our dump client: `wiki-scout/scripts/dumppass.py`, UA
    `AI-Development-workspace-dumpbot/1.0 (<contact>; personal offline research, one download at a time) curl/<ver>`.
    The contact is read from `.claude/private/wikimedia-contact.txt` (the user approved his email for Wikimedia only;
    it never goes in a skill file).
  - Downloads are rate limited and capped at **3 connections per IP**. "Clients that do not respect the
    user-agent policy or who try to evade these limits may be blocked."
  - We use one download at a time and no download accelerators.
  - **XML dumps are deprecated and end January 2027.** The replacement is "MediaWiki Content File Exports"
    (other/mediawiki_content_history/readme.html).
  - Mirrors are listed on the front page. Each mirror is a new host and needs its own entry.
- **Our rule for parts (the user 2026-11-16):** "you'd need to delete it directly after confirming we don't want
  it". Download a part, extract our titles, check the extraction, then **delete it outright** (rm, not
  `gio trash`, since the Trash sits on the same disk and frees nothing).

### upload.wikimedia.org (robots.txt 2026-11-23)
- Commons and Wikipedia media files. robots.txt (`robots/upload.wikimedia.org-2026-11-23.txt`) denies only
  `/wikipedia/commons/archive/` (old file versions) to `*`. No bots named; sitecheck: no collisions.
- WMF User-Agent policy applies: use the dumpbot UA with the contact from `.claude/private/wikimedia-contact.txt`.
  the user 2026-11-23: "Yes, all Wikimedia hosts". One file at a time, files the user named.
- Used 2026-11-23: the Truppenführung translation PDF (one request, 200). The file's description page lives on
  commons.wikimedia.org, which has no entry yet.

### foundation.wikimedia.org (robots.txt 2026-11-16, User-Agent policy read 2026-11-16)
- robots.txt: the same 30 blocked bots as Wikipedia; our UAs have no collisions; the policy page is ALLOW.
- **WMF User-Agent policy** (Policy:Wikimedia_Foundation_User-Agent_Policy), for every Wikimedia site:
  - Send a UA of the form `<client name>/<version> (<contact information>) <library>/<version>`.
  - Contact: an email, a website, or `<project>; User:<name>`. Put "bot" in the name of an automated client.
  - Name the task or script; never copy a browser's UA or send a generic one (curl, python-urllib).
  - A missing or generic UA can get a 403, and clients that ignore the policy may be blocked.

## Fails when
- **A server matches agents differently from Python** (exact names, regex): sitecheck's collisions and verdicts
  are Python's reading. A site can still block us for rate or behaviour that robots.txt doesn't state.
- **The copy is stale:** robots.txt changes. Refetch it (one request) when an entry is more than about 3 months
  old or a request is refused.
- **robots.txt only binds crawlers in spirit:** an API's own terms may allow more or less. When the two
  disagree, robots.txt holds until the user rules.

## Related skills
wiki-scout (how to pull: Wayback first, scout/textpull/wdpull/docpull), game-sources (wikifetch.py),
war-concepts (warwiki.py), failure-protocol memory (stop on 429, never resend), license-check (what we may use
once pulled)
