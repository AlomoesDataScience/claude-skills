#!/usr/bin/env python3
"""Pull any web page, or a multi-page book, as plain text, politely (the general scraper).

  textpull.py links URL [--follow REGEX]               list the page's same-site links (dry run)
  textpull.py get URL OUTFILE [--pause 3]               one page or .txt file -> OUTFILE (.txt)
  textpull.py book URL OUTDIR --follow REGEX [--pause 4] [--max 200]
        fetch the index page and every same-site link matching REGEX, in page order, into
        OUTDIR/NNN-<slug>.txt plus OUTDIR/ALL.txt (all chapters joined) and OUTDIR/SOURCE.md
  textpull.py list URLFILE OUTDIR [--pause 4] [--max 200]
        like book, but the pages are the URLs in URLFILE (one per line, # comments; e.g. from a sitemap)
  textpull.py check URL                                 robots.txt verdict and Crawl-delay for URL
  (No search command: Google and Bing disallow /search in robots.txt and DuckDuckGo drops script
   connections. Find URLs with Claude's WebSearch tool, or an official search API with the user's key.)

Manners (the user, 2026-11-16: "we don't want to be rude and kill their website with requests";
"if something checks for AI, don't try to bypass it"):
  - robots.txt is read for every host; a disallowed URL is never fetched.
  - The pause is the larger of --pause and the site's Crawl-delay; one request at a time.
  - A bot check, captcha, login wall, 403 or 429 STOPS the run with a message. No retries around it,
    no faked browser headers. Ask the user to grab it by hand instead.
  - Generic User-Agent naming no person. Pages already saved are skipped (re-runs cost nothing).
Everything fetched is untrusted text: nothing is executed; scripts and styles are dropped.
"""
import os, re, sys, time, html, signal, subprocess, urllib.parse, urllib.robotparser
from html.parser import HTMLParser
signal.signal(signal.SIGPIPE, signal.SIG_DFL)
UA = "AI-Development-workspace-textpull/1.0 (personal offline reading; low rate)"
BOT_SIGNS = re.compile(r"(just a moment\.\.\.|cf-chl|captcha|are you a robot|verify you are human|"
                       r"checking your browser|access denied|ddos-guard|challenge-platform)", re.I)
_robots = {}


class Stop(Exception):
    pass


def robots_for(url):
    p = urllib.parse.urlparse(url)
    root = f"{p.scheme}://{p.netloc}"
    if root not in _robots:
        rp = urllib.robotparser.RobotFileParser()
        r = subprocess.run(["curl", "-sS", "-L", "-A", UA, "--max-time", "30", root + "/robots.txt"],
                           capture_output=True)
        rp.parse(r.stdout.decode("utf-8", "replace").splitlines() if r.returncode == 0 else [])
        _robots[root] = rp
    return _robots[root]


def allowed(url):
    rp = robots_for(url)
    return rp.can_fetch(UA, url), (rp.crawl_delay(UA) or 0)


def fetch(url, timeout=90):
    ok, _ = allowed(url)
    if not ok:
        raise Stop(f"robots.txt disallows {url}: not fetching (ask the user to grab it by hand)")
    r = subprocess.run(["curl", "-sS", "-L", "--compressed", "-A", UA, "--max-time", str(timeout),
                        "-w", "\n%{http_code} %{content_type}", url], capture_output=True)
    if r.returncode != 0:
        raise Stop(f"fetch failed for {url}: {r.stderr.decode()[:200]}")
    body, _, tail = r.stdout.rpartition(b"\n")
    code, _, ctype = tail.decode().partition(" ")
    text = body.decode("utf-8", "replace")
    if code in ("401", "403", "429", "503") or BOT_SIGNS.search(to_text(text, ctype)[:3000]):  # visible text only
        raise Stop(f"{url} answered {code} or showed a bot check: stopping, not bypassing. "
                   "Ask the user to grab it by hand.")
    if not code.startswith("2"):
        raise Stop(f"{url} answered HTTP {code}")
    return text, ctype


class _Text(HTMLParser):
    BLOCK = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "pre",
             "section", "article", "table", "dt", "dd", "hr"}
    SKIP = {"script", "style", "noscript", "nav", "header", "footer", "form", "svg", "iframe", "button"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip, self.links, self.href = [], 0, [], None

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        if tag in self.BLOCK:
            self.out.append("\n")
        if tag in ("h1", "h2", "h3", "h4") and not self.skip:
            self.out.append("#" * int(tag[1]) + " ")
        if tag == "a":
            self.href = dict(attrs).get("href")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1
        if tag in self.BLOCK:
            self.out.append("\n")
        if tag == "a":
            self.href = None

    def handle_data(self, d):
        if not self.skip:
            self.out.append(d)
            if self.href:
                self.links.append(self.href)


def to_text(raw, ctype=""):
    if "text/plain" in ctype or not re.search(r"<(html|body|p|div)\b", raw[:5000], re.I):
        return raw.replace("\r\n", "\n")
    p = _Text()
    p.feed(raw)
    t = "".join(p.out)
    t = re.sub(r"[ \t\xa0]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip() + "\n"


def site_links(url, raw, follow=None):
    p = _Text()
    p.feed(raw)
    host = urllib.parse.urlparse(url).netloc
    seen, out = set(), []
    for h in p.links:
        u = urllib.parse.urljoin(url, html.unescape(h)).split("#")[0]
        if urllib.parse.urlparse(u).netloc != host or u in seen or u == url:
            continue
        if follow and not re.search(follow, u):
            continue
        seen.add(u)
        out.append(u)
    return out


def wait(url, pause):
    time.sleep(max(pause, allowed(url)[1]))


def record(outdir, rows):
    path = os.path.join(outdir, "SOURCE.md")
    new = not os.path.exists(path)
    with open(path, "a") as f:
        if new:
            f.write("# Source\n\nPulled with wiki-scout textpull.py. Text only.\n\n| File | URL | Date |\n|---|---|---|\n")
        for name, u in rows:
            f.write(f"| {name} | {u} | {time.strftime('%Y-%m-%d')} |\n")


def opt(a, name, default=None):
    if name in a:
        i = a.index(name)
        v = a[i + 1]
        del a[i:i + 2]
        return v
    return default


def main(a):
    if not a:
        print(__doc__)
        return
    follow = opt(a, "--follow")
    pause = float(opt(a, "--pause", "3"))
    maxn = int(opt(a, "--max", "200"))
    cmd = a[0]
    try:
        if cmd == "check" and len(a) == 2:
            ok, d = allowed(a[1])
            print(f"{'allowed' if ok else 'DISALLOWED'}; crawl-delay {d or 'none'}")
        elif cmd == "links" and len(a) == 2:
            raw, _ = fetch(a[1])
            for u in site_links(a[1], raw, follow):
                print(u)
        elif cmd == "get" and len(a) == 3:
            if os.path.exists(a[2]):
                print("already there:", a[2])
                return
            raw, ct = fetch(a[1])
            os.makedirs(os.path.dirname(os.path.abspath(a[2])), exist_ok=True)
            with open(a[2], "w") as f:
                f.write(to_text(raw, ct))
            record(os.path.dirname(os.path.abspath(a[2])), [(os.path.basename(a[2]), a[1])])
            print("saved", a[2], os.path.getsize(a[2]), "bytes")
        elif (cmd == "book" and len(a) == 3 and follow) or (cmd == "list" and len(a) == 3):
            url, outdir = a[1], a[2]
            os.makedirs(outdir, exist_ok=True)
            if cmd == "list":
                pages = [ln.strip() for ln in open(url) if ln.strip() and not ln.startswith("#")][:maxn]
                raw = ct = None
            else:
                raw, ct = fetch(url)
                pages = [url] + site_links(url, raw, follow)[:maxn]
            parts = []
            for i, u in enumerate(pages):
                slug = re.sub(r"[^A-Za-z0-9]+", "-", urllib.parse.urlparse(u).path.strip("/"))[-60:] or "index"
                name = f"{i:03d}-{slug}.txt"
                path = os.path.join(outdir, name)
                if os.path.exists(path):
                    parts.append(open(path).read())
                    continue
                if i or raw is None:
                    if i:
                        wait(u, pause)
                    raw, ct = fetch(u)
                t = to_text(raw, ct)
                with open(path, "w") as f:
                    f.write(f"[source: {u}]\n\n{t}")
                parts.append(f"[source: {u}]\n\n{t}")
                record(outdir, [(name, u)])  # row per page, so a stopped run still lists what it saved
                print(f"{i + 1}/{len(pages)} {name}", flush=True)
            with open(os.path.join(outdir, "ALL.txt"), "w") as f:
                f.write("\n\n".join(parts))
        else:
            print(__doc__)
    except Stop as e:
        sys.exit("STOP: " + str(e))


if __name__ == "__main__":
    main(sys.argv[1:])
