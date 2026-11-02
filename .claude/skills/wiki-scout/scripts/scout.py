#!/usr/bin/env python3
"""Find and pull game and franchise (IP) wikis as plain text, gently: Wayback Machine first.

  scout.py find "Game or IP name" [more names...]   where its wiki lives (Fandom, wiki.gg, Paradox,
                    StrategyWiki, PCGamingWiki...), checked through the Wayback availability API:
                    zero requests to the wikis themselves
  scout.py titles BASE OUT.txt [--prefix X] [--limit N]   every archived article title under BASE
                    (e.g. https://gundam.fandom.com/wiki/) from the Wayback CDX index
  scout.py pull BASE TITLES.txt OUTDIR [--pause 4] [--max N] [--keep-html]
                    newest good Wayback snapshot of each page (falls back up to 3 years) -> OUTDIR/<title>.txt
                    and <title>.infobox.json; raw HTML deleted unless --keep-html; resumable
  scout.py live API_URL TITLES.txt OUTDIR [--pause 4]   pages Wayback lacks, from the live MediaWiki API
                    (api.php): honest User-Agent, robots.txt respected, maxlag, slow; plain-text extracts
  scout.py check OUTDIR    safety check: every file is plain UTF-8 text with no script or iframe left
  scout.py record OUTDIR BASE    write OUTDIR/SOURCE.md (what, where from, when, how many)

Nothing fetched is ever executed or opened in a browser. Only text is kept.
"""
import os, sys, re, json, time, html, subprocess, urllib.parse, urllib.robotparser, signal
signal.signal(signal.SIGPIPE, signal.SIG_DFL)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "game-sources", "scripts"))
import wikifetch  # to_text, infobox

UA = "AI-Development-workspace-wiki-scout/1.0 (personal offline reading; ~1 request per few seconds)"


def curl(url, out=None, timeout=60):
    cmd = ["curl", "-sS", "-L", "--compressed", "-A", UA, "--max-time", str(timeout), "-w", "%{http_code}"]
    cmd += ["-o", out] if out else ["-o", "-"]
    r = subprocess.run(cmd + [url], capture_output=True)
    if out:
        return r.stdout.decode()[-3:], None
    body, code = r.stdout[:-3], r.stdout[-3:].decode(errors="replace")
    return code, body.decode("utf-8", errors="replace")


def patient(url, tries=5, **kw):
    """Retry on 429/5xx/000 and on the archive's 'Temporarily Offline' page, backing off."""
    for t in range(tries):
        code, body = curl(url, **kw)
        busy = code in ("000", "429", "502", "503", "504") or (body and "Temporarily Offline" in body[:400])
        if not busy:
            return code, body
        time.sleep(20 * (t + 1))
    return code, body


def slugs(name):
    n = re.sub(r"[™®:']", "", name).strip()
    words = re.findall(r"[A-Za-z0-9]+", n)
    s = {"".join(words).lower(), "-".join(words).lower(), words[0].lower() if words else ""}
    if len(words) > 1:
        s.add("".join(w[0] for w in words).lower())
        s.add("".join(words[:2]).lower())
    return [x for x in s if len(x) > 2]


def candidates(name):
    t = urllib.parse.quote(name.replace(" ", "_"))
    out = []
    for s in slugs(name):
        out += [f"{s}.fandom.com", f"{s}.wiki.gg", f"{s}.paradoxwikis.com", f"{s}.gamepedia.com"]
    out += [f"https://strategywiki.org/wiki/{t}", f"https://www.pcgamingwiki.com/wiki/{t}",
            f"https://en.wikipedia.org/wiki/{t}"]
    return out


def cmd_find(names):
    for name in names:
        print(f"## {name}")
        for c in candidates(name):
            code, body = patient("https://archive.org/wayback/available?url=" + urllib.parse.quote(c, safe=""))
            try:
                snap = json.loads(body or "{}").get("archived_snapshots", {}).get("closest")
            except ValueError:
                snap = None
            if snap and snap.get("available"):
                where = snap["url"].split("/", 5)[-1]
                wiki = (f"https://{c}/" if "paradoxwikis" in c else f"https://{c}/wiki/") if "/" not in c else c
                print(f"  {snap['timestamp'][:8]}  {wiki}   (snapshot of {where})")
            time.sleep(1.5)


def cmd_titles(base, out, prefix="", limit=0):
    host_path = re.sub(r"^https?://", "", base)
    titles, key, pages = set(), None, 0
    while True:
        q = {"url": host_path + prefix, "matchType": "prefix", "filter": ["statuscode:200", "mimetype:text/html"],
             "collapse": "urlkey", "fl": "original", "limit": "5000", "showResumeKey": "true"}
        if key:
            q["resumeKey"] = key
        url = "https://web.archive.org/cdx/search/cdx?" + urllib.parse.urlencode(q, doseq=True)
        code, body = patient(url, timeout=180)
        if code != "200":
            sys.exit(f"CDX answered {code}; try again later")
        lines = body.splitlines()
        key = None
        if len(lines) >= 2 and lines[-2] == "":
            key = lines[-1]; lines = lines[:-2]
        for l in lines:
            m = re.match(r"https?://[^/]+" + re.escape("/" + host_path.split("/", 1)[1] if "/" in host_path else "/") + r"([^?#]+)$", l)
            if not m:
                continue
            t = urllib.parse.unquote(m.group(1))
            if ":" in t or not t or t.startswith("Special"):
                continue                          # namespaces (File:, Category:, User:...) and odd URLs
            titles.add(t.replace(" ", "_"))
        pages += 1
        print(f"  index page {pages}: {len(titles)} titles", flush=True)
        if not key or (limit and len(titles) >= limit):
            break
        time.sleep(3)
    titles = sorted(titles)[:limit] if limit else sorted(titles)
    open(out, "w").write("\n".join(titles) + "\n")
    print(f"{len(titles)} titles -> {out}")


def is_article(s):
    return "mw-content-text" in s and "Just a moment" not in s[:3000] and "cf-challenge" not in s[:5000]


def save_text(raw, outdir, t, keep):
    base = os.path.join(outdir, t.replace("/", "_"))
    txt = wikifetch.to_text(raw)
    open(base + ".txt", "w", encoding="utf-8").write(txt)
    try:
        box = wikifetch.infobox(raw)
        if box:
            json.dump(box, open(base + ".infobox.json", "w"), ensure_ascii=False, indent=1)
    except Exception:
        pass
    if keep:
        clean = re.sub(r"(?is)<(script|iframe|object|embed|style)\b.*?</\1\s*>", "", raw)
        clean = re.sub(r"(?i)\son\w+\s*=\s*(\"[^\"]*\"|'[^']*')", "", clean)
        open(base + ".html.txt", "w", encoding="utf-8").write(clean)   # .txt so nothing opens it as a page


def cmd_pull(base, titles, outdir, pause=4.0, maxn=0, keep=False):
    os.makedirs(outdir, exist_ok=True)
    year = int(time.strftime("%Y"))
    ok = miss = done = 0
    missed = []
    for t in [l.strip() for l in open(titles) if l.strip()]:
        if maxn and ok + miss >= maxn:
            break
        if os.path.exists(os.path.join(outdir, t.replace("/", "_") + ".txt")):
            done += 1; continue
        got = False
        for y in range(year, year - 4, -1):
            code, body = patient(f"https://web.archive.org/web/{y}id_/{base.rstrip('/')}/{urllib.parse.quote(t)}")
            if code == "200" and body and is_article(body):
                save_text(body, outdir, t, keep); got = True; break
            time.sleep(pause / 2)
        if got:
            ok += 1; print("ok", t, flush=True)
        else:
            miss += 1; missed.append(t); print("MISS", t, flush=True)
        time.sleep(pause)
    if missed:
        open(os.path.join(outdir, "missing.txt"), "a").write("\n".join(missed) + "\n")
    print(f"done: {ok} new, {done} already there, {miss} missing (missing.txt)")


def cmd_live(api, titles, outdir, pause=4.0):
    root = re.match(r"(https?://[^/]+)", api).group(1)
    rp = urllib.robotparser.RobotFileParser(); rp.set_url(root + "/robots.txt")
    try:
        rp.read()
    except Exception:
        pass
    if not rp.can_fetch(UA, api):
        sys.exit(f"robots.txt disallows {api} for scripts: not fetching (ask the user, or use Wayback)")
    os.makedirs(outdir, exist_ok=True)
    for t in [l.strip() for l in open(titles) if l.strip()]:
        f = os.path.join(outdir, t.replace("/", "_") + ".txt")
        if os.path.exists(f):
            continue
        q = {"action": "parse", "page": t.replace("_", " "), "prop": "text", "format": "json",
             "formatversion": "2", "maxlag": "5", "redirects": "1"}
        code, body = patient(api + "?" + urllib.parse.urlencode(q))
        try:
            data = json.loads(body)
            raw = '<div id="mw-content-text">' + data["parse"]["text"] + "</div>"
            save_text(raw, outdir, t, False); print("ok", t, flush=True)
        except Exception:
            print("MISS", code, t, flush=True)
            if body and "maxlag" in body:
                time.sleep(60)
        time.sleep(pause)


def cmd_check(outdir):
    bad = 0; n = 0
    for dp, dn, fn in os.walk(outdir):
        for f in fn:
            p = os.path.join(dp, f); n += 1
            b = open(p, "rb").read()
            try:
                s = b.decode("utf-8")
            except UnicodeDecodeError:
                print("NOT TEXT", p); bad += 1; continue
            if b"\x00" in b or re.search(r"(?i)<script|<iframe|javascript:|<object|<embed", s):
                print("ACTIVE CONTENT", p); bad += 1
    print(f"{n} files checked, {bad} flagged" + ("" if bad else ": all plain text"))
    return bad


def cmd_record(outdir, base):
    n = len([f for f in os.listdir(outdir) if f.endswith(".txt") and not f.endswith(".html.txt") and f not in ("missing.txt",)])
    miss = len(open(os.path.join(outdir, "missing.txt")).read().split()) if os.path.isfile(os.path.join(outdir, "missing.txt")) else 0
    open(os.path.join(outdir, "SOURCE.md"), "w").write(
        f"# Source\n\n- Wiki: {base}\n- Pulled: {time.strftime('%Y-%m-%d')} by wiki-scout (Wayback Machine snapshots"
        f" first, newest good one per page; plain text only)\n- Pages: {n} text files; {miss} not found (missing.txt)\n"
        "- Community wiki text: summarise in Claude's own words; don't republish it.\n")
    print(f"recorded {n} pages")


def main(a):
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    opt = {}
    pos = []
    i = 1
    while i < len(a):
        if a[i].startswith("--"):
            if a[i] == "--keep-html":
                opt["keep"] = True; i += 1
            else:
                opt[a[i][2:]] = a[i + 1]; i += 2
        else:
            pos.append(a[i]); i += 1
    c = a[0]
    if c == "find": cmd_find(pos)
    elif c == "titles": cmd_titles(pos[0], pos[1], opt.get("prefix", ""), int(opt.get("limit", 0)))
    elif c == "pull": cmd_pull(pos[0], pos[1], pos[2], float(opt.get("pause", 4)), int(opt.get("max", 0)), opt.get("keep", False))
    elif c == "live": cmd_live(pos[0], pos[1], pos[2], float(opt.get("pause", 4)))
    elif c == "check": sys.exit(1 if cmd_check(pos[0]) else 0)
    elif c == "record": cmd_record(pos[0], pos[1])
    else: sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
