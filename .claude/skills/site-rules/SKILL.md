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

## Fails when
- **A server matches agents differently from Python** (exact names, regex): sitecheck's collisions and verdicts
  are Python's reading. A site can still block us for rate or behaviour that robots.txt doesn't state.
- **The copy is stale:** robots.txt changes. Refetch it (one request) when an entry is more than about 3 months
  old or a request is refused.
- **robots.txt only binds crawlers in spirit:** an API's own terms may allow more or less. When the two
  disagree, robots.txt holds until the user rules.

## Reference files (read the one the step needs)

| File | Holds |
|---|---|
| `reference/hosts.md` | **Hosts** - api.nuget.org (robots.txt 2026-11-16: 404, none) - NuGet's package API, used only through dotnet restore / dot |

## Related skills
wiki-scout (how to pull: Wayback first, scout/textpull/wdpull/docpull), game-sources (wikifetch.py),
war-concepts (warwiki.py), failure-protocol memory (stop on 429, never resend), license-check (what we may use
once pulled)
