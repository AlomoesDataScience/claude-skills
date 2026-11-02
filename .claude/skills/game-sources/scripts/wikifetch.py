#!/usr/bin/env python3
"""Fetch MediaWiki pages through the Wayback Machine and turn them into plain text.

For lore wikis that sit behind Cloudflare (curl and WebFetch get 403 "Just a moment").

  wikifetch.py fetch BASE_URL TITLES.txt OUTDIR [--year YEAR (default: this year; falls back up to 2 years per page)] [--pause 4]
      BASE_URL like https://www.greyhawkonline.com/greyhawkwiki/ ; one page title per line
      (underscores for spaces). Saves OUTDIR/<title>.html, skips pages already there, waits
      --pause seconds between pages and backs off on 429 (the archive allows ~1 request/s).
  wikifetch.py allpages API_URL OUT.txt       every page title through the MediaWiki API (api.php),
                                              which often answers when the HTML pages are blocked
  wikifetch.py api API_URL TITLES.txt OUTDIR  each page's wikitext (OUTDIR/<title>.wiki) via the API
  wikifetch.py text PAGE.html [OUT.txt]      article body as text (## headings, - lists, | tables)
  wikifetch.py textall OUTDIR                 PAGE.txt next to every PAGE.html
  wikifetch.py links PAGE.html [SECTION]      wiki titles the page (or one section id) links to
  wikifetch.py infobox PAGE.html              the infobox rows as "key: value" lines
  wikifetch.py infoboxes OUTDIR OUT.json      every page's infobox as {title: {key: value}}
"""
import html, os, re, subprocess, sys, time


def get(url, out):
    """curl with gzip; returns the HTTP code (archive pages arrive gzip-compressed)."""
    r = subprocess.run(["curl", "-sSL", "--compressed", "-A", "AI-Development-workspace-wikifetch/1.0 (personal offline reading; low rate)", "--max-time", "60",
                        "-o", out, "-w", "%{http_code}", url], capture_output=True, text=True)
    return r.stdout.strip() or "000"


def fetch(base, titles, outdir, year=None, pause=4.0):
    year = year or time.strftime("%Y")
    os.makedirs(outdir, exist_ok=True)
    ok = miss = 0
    for t in [l.strip() for l in open(titles) if l.strip()]:
        f = os.path.join(outdir, t.replace("/", "_") + ".html")
        if os.path.exists(f) and os.path.getsize(f):
            continue
        # newest first; fall back a year at a time when the snapshot is not an article (a site's
        # bot-check page got archived instead, as on the Stellaris wiki from 2026)
        for y in range(int(year), int(year) - 3, -1):
            for tries in range(4):
                code = get(f"https://web.archive.org/web/{y}id_/{base.rstrip('/')}/{t}", f)
                if code not in ("429", "000"):
                    break
                time.sleep(30 * (tries + 1))
            body = open(f, encoding="utf-8", errors="replace").read() if os.path.exists(f) else ""
            if code == "200" and "mw-content-text" in body:
                break
            time.sleep(pause)
        if code == "200" and "mw-content-text" in body:
            ok += 1
            print("ok", y, t, flush=True)
        else:
            miss += 1
            print("MISS", code, t, flush=True)
            if os.path.exists(f):
                os.remove(f)
        time.sleep(pause)
    print(f"done: {ok} fetched, {miss} missing")


def api_get(api, params):
    import json
    import urllib.parse
    url = api + "?" + urllib.parse.urlencode(dict(params, format="json"))
    r = subprocess.run(["curl", "-sSL", "--compressed", "-A", "AI-Development-workspace-wikifetch/1.0 (personal offline reading; low rate)", "--max-time", "60", url],
                       capture_output=True, text=True)
    return json.loads(r.stdout or "{}")


def allpages(api, out):
    titles, cont = [], {}
    while True:
        d = api_get(api, dict({"action": "query", "list": "allpages", "aplimit": "500"}, **cont))
        titles += [p["title"] for p in d.get("query", {}).get("allpages", [])]
        if "continue" not in d:
            break
        cont = {"apcontinue": d["continue"]["apcontinue"]}
    open(out, "w").write("\n".join(titles) + "\n")
    print(len(titles), "titles ->", out)


def api_pages(api, titles, outdir, pause=1.0):
    os.makedirs(outdir, exist_ok=True)
    n = 0
    for t in [l.strip() for l in open(titles) if l.strip()]:
        f = os.path.join(outdir, t.replace("/", "_") + ".wiki")
        if os.path.exists(f):
            continue
        d = api_get(api, {"action": "parse", "page": t, "prop": "wikitext", "redirects": "1"})
        w = d.get("parse", {}).get("wikitext", {}).get("*")
        if w is None:
            print("MISS", t, d.get("error", {}).get("code", ""), flush=True)
            continue
        open(f, "w").write(w)
        n += 1
        time.sleep(pause)
    print(n, "pages ->", outdir)


def body(s):
    a = s.find('id="mw-content-text"')
    b = s.find('class="printfooter"')
    return s[a:b if b > 0 else len(s)]


def to_text(s):
    s = body(s)
    s = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", s)
    s = re.sub(r'(?is)<span class="mw-editsection".*?</span>\s*</span>', "", s)
    s = re.sub(r'(?is)<div id="toc".*?</ul>\s*</div>', "", s)
    s = re.sub(r'(?is)<sup[^>]*class="reference".*?</sup>', "", s)
    for n in (2, 3, 4):
        s = re.sub(rf"(?is)<h{n}[^>]*>(.*?)</h{n}>", lambda m, n=n: "\n\n" + "#" * n + " " + m.group(1) + "\n", s)
    s = re.sub(r"(?i)<li[^>]*>", "\n- ", s)
    s = re.sub(r"(?i)<(td|th)[^>]*>", " | ", s)
    s = re.sub(r"(?i)</?(p|tr|br|ul|ol|table|div|dd|dt|dl)[^>]*>", "\n", s)
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n[ \t]+", "\n", s)
    return re.sub(r"\n{3,}", "\n\n", s).strip() + "\n"


def infobox(s):
    a = s.find('class="infobox')
    if a < 0:
        return []
    a = s.rfind("<table", 0, a)
    depth, i = 0, a
    for m in re.finditer(r"(?i)<(/?)table\b", s[a:]):        # the infobox may hold nested tables
        depth += -1 if m.group(1) else 1
        if depth == 0:
            i = a + m.end()
            break
    rows = []
    for tr in re.findall(r"(?is)<tr.*?</tr>", s[a:i]):
        cells = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", c))).strip()
                 for c in re.findall(r"(?is)<t[hd][^>]*>(.*?)</t[hd]>", tr)]
        if len(cells) >= 2 and cells[0]:
            rows.append(f"{cells[0].rstrip(':')}: {' '.join(cells[1:])}")
    return rows


def links(s, section=None):
    if section:
        a = s.find(f'id="{section}"')
        nxt = re.search(r'<h2', s[a + 10:])
        s = s[a:a + 10 + nxt.start()] if nxt else s[a:]
    else:
        s = body(s)
    return sorted(set(t for t in re.findall(r'href="[^"]*?/(?:wiki|greyhawkwiki)/([^"#:?]+)"', s)))


def main(a):
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd = a[0]
    if cmd == "fetch":
        opt = {a[i]: a[i + 1] for i in range(4, len(a) - 1, 2)}
        fetch(a[1], a[2], a[3], opt.get("--year"), float(opt.get("--pause", 4)))
    elif cmd == "allpages":
        allpages(a[1], a[2])
    elif cmd == "api":
        api_pages(a[1], a[2], a[3])
    elif cmd == "text":
        t = to_text(open(a[1], encoding="utf-8", errors="replace").read())
        open(a[2], "w").write(t) if len(a) > 2 else sys.stdout.write(t)
    elif cmd == "textall":
        n = 0
        for f in sorted(os.listdir(a[1])):
            if f.endswith(".html"):
                p = os.path.join(a[1], f)
                open(p[:-5] + ".txt", "w").write(to_text(open(p, encoding="utf-8", errors="replace").read()))
                n += 1
        print(n, "pages converted")
    elif cmd == "links":
        print("\n".join(links(open(a[1], encoding="utf-8", errors="replace").read(), a[2] if len(a) > 2 else None)))
    elif cmd == "infobox":
        print("\n".join(infobox(open(a[1], encoding="utf-8", errors="replace").read())))
    elif cmd == "infoboxes":
        import json
        out = {}
        for f in sorted(os.listdir(a[1])):
            if f.endswith(".html"):
                rows = infobox(open(os.path.join(a[1], f), encoding="utf-8", errors="replace").read())
                out[f[:-5]] = dict(r.split(": ", 1) for r in rows if ": " in r)
        json.dump(out, open(a[2], "w"), indent=1, ensure_ascii=False)
        print(len(out), "pages,", sum(1 for v in out.values() if v), "with an infobox ->", a[2])
    else:
        sys.exit(f"unknown command {cmd}\n{__doc__}")


if __name__ == "__main__":
    main(sys.argv[1:])
