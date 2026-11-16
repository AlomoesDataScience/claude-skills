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

### query.wikidata.org (robots.txt 2026-11-16)
- **Denied to all bots:** `/sparql` and `/bigdata`, which is the whole query service. The one SPARQL request
  for the battles index broke this. wdpull's robots check now refuses it.
- The query service's own usage docs aren't read yet. They may welcome API clients that send a UA, but
  robots.txt says no, and robots.txt wins until the user rules.

### web.archive.org (2026-11-16)
- **No robots.txt** (404). Python treats that as allow-all. Default source for wikis (wiki-scout). Their
  rate limit is about 1 request a second, so we use a 4 s pause. Their written bot policy isn't read yet.

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
war-concepts (warwiki.py), failure-protocol memory (stop on 429, never resend)
