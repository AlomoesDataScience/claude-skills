#!/usr/bin/env python3
"""Pull a whole class of Wikipedia articles gently: Wikidata finds them, the Wikipedia API sends 50 at a time.
First used 2026-11-16 for every battle 1700-1820 (operational sim demo). Everything fetched is untrusted text:
keep OUTDIR away from scripts, run with python3 -I.

  wdpull.py sparql QUERY.rq OUT.json            one Wikidata Query Service request; saves the JSON results
  wdpull.py wikitext OUTDIR TITLE [TITLE...]    up to 50 pages' wikitext in one request -> OUTDIR/<title>.wiki
  wdpull.py pull TITLES.txt OUT.jsonl.gz [--pause 3]
                                                wikitext of every title, 50 a request, serial, maxlag=5; resumable
                                                (titles already in OUT are skipped); stops on 403/429/503
  wdpull.py parse IN.jsonl.gz OUTDIR            local only: OUTDIR/battles.jsonl (infobox raw + clean, coords,
                                                campaignboxes, categories) and OUTDIR/text/<title>.txt

Politeness (wiki-scout rules + Wikimedia Robot policy, wikitech.wikimedia.org/wiki/Robot_policy, read 2026-11-16):
robots.txt is read first and a disallowed URL is never requested (en.wikipedia.org disallows /w/, so api.php
is refused there); one request at a time; a generic honest User-Agent with no personal details; maxlag=5; the
pause between requests is at least 5 s when the last one took over 1 s to serve (Robot policy); a stop (no retry
around it) on 401/403/429/503 or a bot check, quoting Retry-After.
Fails when: a site's robots.txt can't be read (urllib treats that as allow-all; the stop message says so).
"""
import gzip
import json
import os
import re
import sys
import time

import requests

UA = "AI-Development-workspace-wdpull/1.0 (personal offline research; batched, one request at a time)"
WP_API = "https://en.wikipedia.org/w/api.php"
WD_SPARQL = "https://query.wikidata.org/sparql"
STOP = {401, 403, 429, 503}


_robots = {}


def allowed(url):
    """robots.txt verdict for our User-Agent, read once per host (one request)."""
    import urllib.parse, urllib.robotparser
    root = "{0.scheme}://{0.netloc}".format(urllib.parse.urlsplit(url))
    if root not in _robots:
        rp = urllib.robotparser.RobotFileParser()
        r = requests.get(root + "/robots.txt", headers={"User-Agent": UA}, timeout=30)
        rp.parse(r.text.splitlines() if r.status_code == 200 else [])
        if r.status_code != 200:
            print(f"note: {root}/robots.txt answered {r.status_code}; treated as allow-all", file=sys.stderr)
        _robots[root] = rp
    return _robots[root].can_fetch(UA, url)


LAST_SECONDS = [0.0]


def get(url, params, method="GET"):
    if not allowed(url):
        sys.exit(f"STOP: robots.txt disallows {url} for bots; not requesting (wiki-scout rule). Tell the user.")
    s = requests.Session()
    s.headers["User-Agent"] = UA
    for attempt in range(2):
        t0 = time.monotonic()
        r = s.request(method, url, params=params if method == "GET" else None,
                      data=params if method == "POST" else None, timeout=120)
        LAST_SECONDS[0] = time.monotonic() - t0
        if r.status_code in STOP:
            sys.exit(f"STOP: {url} answered {r.status_code} (Retry-After: {r.headers.get('Retry-After', 'none')}); "
                     "not retrying (wiki-scout rule). Tell the user.")
        r.raise_for_status()
        j = r.json()
        if isinstance(j, dict) and j.get("error", {}).get("code") == "maxlag" and attempt == 0:
            time.sleep(int(r.headers.get("Retry-After", "5")) + 1)
            continue
        return j
    sys.exit("STOP: server still lagged after one wait")


def safe_name(title):
    return re.sub(r'[/\\:*?"<>|]', "_", title)[:180]


def fetch_batch(titles):
    """{requested title: (final title, pageid, revid, wikitext or None)} for up to 50 titles."""
    j = get(WP_API, {"action": "query", "prop": "revisions", "rvprop": "ids|content", "rvslots": "main",
                     "titles": "|".join(titles), "redirects": "1", "format": "json", "formatversion": "2",
                     "maxlag": "5"}, method="POST")
    q = j.get("query", {})
    alias = {t: t for t in titles}
    for k in ("normalized", "redirects"):
        for m in q.get(k, []):
            for t, v in list(alias.items()):
                if v == m["from"]:
                    alias[t] = m["to"]
    pages = {p["title"]: p for p in q.get("pages", [])}
    out = {}
    for t in titles:
        p = pages.get(alias[t])
        if not p or p.get("missing") or "revisions" not in p:
            out[t] = (alias[t], None, None, None)
        else:
            rv = p["revisions"][0]
            out[t] = (p["title"], p["pageid"], rv["revid"], rv["slots"]["main"]["content"])
    return out


# ---------- wikitext to text ----------

def _tpl(body, infobox):
    parts = [p.strip() for p in body.split("|")]
    name = parts[0].lower().replace("_", " ").strip()
    args = [p for p in parts[1:] if "=" not in p.split("[[")[0] or name in ("ubl", "unbulleted list", "plainlist", "flatlist", "hlist", "plain list")]
    named = dict(p.split("=", 1) for p in parts[1:] if "=" in p.split("[[")[0])
    named = {k.strip(): v.strip() for k, v in named.items()}
    if name in ("kia", "k.i.a."): return " (KIA)"
    if name in ("dow", "d.o.w."): return " (DOW)"
    if name in ("pow", "p.o.w."): return " (POW)"
    if name in ("wia",): return " (WIA)"
    if name in ("nbsp", "spaces", "thinsp"): return " "
    if name in ("snd", "spaced ndash", "ndash", "spnd"): return " - "
    if name in ("mdash", "--"): return " - "
    if name in ("circa", "c.", "ca"): return "c. " + (args[0] if args else "")
    if name in ("flagicon", "flagicon image", "flagdeco", "efn", "efn-ua", "efn-lr", "refn", "sfn", "sfnp", "harvnb",
                "cn", "citation needed", "clarify", "when", "who", "which", "dubious", "failed verification",
                "better source needed", "page needed", "rp", "r", "ref", "dash", "-", "clear", "notetag", "ref label"):
        return ""
    if name in ("flag", "flagcountry", "flagu", "flag country", "flagcountry2", "flag2"): return args[0] if args else ""
    if name in ("lang", "transl", "transliteration", "lang-x"): return args[-1] if args else ""
    if name.startswith("lang-"): return args[0] if args else ""
    if name in ("convert", "cvt"): return " ".join(args[:2])
    if name in ("ubl", "unbulleted list", "plainlist", "flatlist", "hlist", "plain list", "collapsible list"):
        items = [a for a in parts[1:] if not re.match(r"^\s*(title|class|style|frame_style|list_style|framestyle|liststyle)\s*=", a)]
        txt = "; ".join(i for i in (x.strip("* \n") for x in "\n".join(items).split("\n")) if i)
        return txt
    if name in ("nowrap", "small", "big", "nobr", "smaller", "larger", "abbr", "tooltip", "nobold", "noitalic",
                "lower", "resize", "center", "centre", "right", "midsize", "sc", "smallcaps", "em", "strong",
                "nowrap begin", "line break", "bold", "italic", "nbsp;"):
        return args[0] if args else ""
    if name in ("coord",): return "{COORD|" + "|".join(parts[1:]) + "}"
    if name in ("date", "start date", "end date", "dts", "birth date", "start and end dates", "start date and age",
                "osdate", "old style date", "o.s.", "os", "ns", "old style date and year", "osdate2",
                "date range", "start-date"):
        return " ".join(a for a in args if a)
    if re.search(r"style|date|calendar|julian|gregorian", name):     # NS/OS and other date wrappers: keep the dates
        return " ".join(a for a in args if a)
    if name.startswith("campaignbox") or name.startswith("infobox"): return ""
    if infobox and args and name in ("aligned table", "army", "navy", "nowrap", "plainlist"): return "; ".join(args)
    return ""


def expand(s, infobox=False):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<ref[^>/]*/>", "", s)
    s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S | re.I)
    s = re.sub(r"<br\s*/?>", "; " if infobox else "\n", s, flags=re.I)
    for _ in range(40):
        n = re.sub(r"\{\{([^{}]*)\}\}", lambda m: _tpl(m.group(1), infobox), s)
        if n == s:
            break
        s = n
    for _ in range(10):
        n = re.sub(r"\[\[([^\[\]|]*)(?:\|([^\[\]]*))?\]\]",
                   lambda m: "" if re.match(r"\s*(file|image|category|media):", m.group(1), re.I)
                   else (m.group(2) if m.group(2) is not None else m.group(1)), s)
        if n == s:
            break
        s = n
    s = re.sub(r"\[https?://[^\s\]]+\s?([^\]]*)\]", r"\1", s)
    s = re.sub(r"'{2,}", "", s)
    s = re.sub(r"</?[a-zA-Z][^>]*>", "", s)
    s = s.replace("&nbsp;", " ").replace("&ndash;", "-").replace("&mdash;", "-").replace("&amp;", "&")
    return s


def strip_tables(s):
    out, depth = [], 0
    for line in s.split("\n"):
        t = line.strip()
        if t.startswith("{|"):
            depth += 1
            continue
        if depth and t.startswith("|}"):
            depth -= 1
            continue
        if not depth:
            out.append(line)
    return "\n".join(out)


def to_text(wikitext):
    s = strip_tables(expand(wikitext))
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


# ---------- infobox ----------

def find_template(s, start):
    """End index (after '}}') of the template beginning at s[start:start+2] == '{{'."""
    depth, i = 0, start
    while i < len(s) - 1:
        if s[i:i + 2] == "{{":
            depth, i = depth + 1, i + 2
        elif s[i:i + 2] == "}}":
            depth, i = depth - 1, i + 2
            if depth == 0:
                return i
        else:
            i += 1
    return len(s)


def split_top(body):
    parts, cur, d1, d2, i = [], [], 0, 0, 0
    while i < len(body):
        two = body[i:i + 2]
        if two == "{{": d1 += 1; cur.append(two); i += 2; continue
        if two == "}}": d1 -= 1; cur.append(two); i += 2; continue
        if two == "[[": d2 += 1; cur.append(two); i += 2; continue
        if two == "]]": d2 -= 1; cur.append(two); i += 2; continue
        if body[i] == "|" and d1 == 0 and d2 == 0:
            parts.append("".join(cur)); cur = []
        else:
            cur.append(body[i])
        i += 1
    parts.append("".join(cur))
    return parts


def infobox(wikitext):
    best = None
    for m in re.finditer(r"\{\{\s*infobox[ _]([^|}\n]*)", wikitext, re.I):
        name = m.group(1).strip().lower()
        if best is None or any(k in name for k in ("conflict", "battle", "siege", "naval")):
            best = (m.start(), name)
            if any(k in name for k in ("conflict", "battle", "siege", "naval")):
                break
    if not best:
        return None, {}
    end = find_template(wikitext, best[0])
    parts = split_top(wikitext[best[0] + 2:end - 2])
    raw = {}
    for p in parts[1:]:
        if "=" in p:
            k, v = p.split("=", 1)
            if v.strip():
                raw[k.strip().lower()] = v.strip()
    return best[1], raw


def coords(raw):
    m = re.search(r"\{\{\s*coord\s*\|([^{}]*)\}\}", raw or "", re.I)
    if not m:
        return None
    a = [x.strip() for x in m.group(1).split("|") if "=" not in x]
    try:
        if len(a) >= 2 and all(re.match(r"^-?[\d.]+$", x) for x in a[:2]):
            return [float(a[0]), float(a[1])]
        nums, out = [], []
        for x in a:
            if x.upper() in ("N", "S", "E", "W"):
                v = sum(float(n) / 60 ** i for i, n in enumerate(nums))
                out.append(-v if x.upper() in ("S", "W") else v)
                nums = []
                if len(out) == 2:
                    return out
            elif re.match(r"^-?[\d.]+$", x):
                nums.append(x)
    except ValueError:
        return None
    return None


def parse_article(title, wikitext):
    name, raw = infobox(wikitext)
    clean = {k: re.sub(r"\s+", " ", expand(v, infobox=True)).strip(" ;") for k, v in raw.items()}
    camp = sorted({m.strip() for m in re.findall(r"\{\{\s*(Campaignbox[^|}\n]*)", wikitext, re.I)})
    cats = re.findall(r"\[\[\s*Category:([^\]|]+)", wikitext)
    coord = coords(raw.get("coordinates") or raw.get("coords") or "") or coords(wikitext)
    return {"title": title, "infobox_type": name, "infobox": clean, "infobox_raw": raw, "coords": coord,
            "campaignboxes": camp, "categories": [c.strip() for c in cats], "chars": len(wikitext)}


# ---------- commands ----------

def cmd_sparql(qfile, out):
    q = open(qfile, encoding="utf-8").read()
    j = get(WD_SPARQL, {"query": q, "format": "json"}, method="POST")
    json.dump(j, open(out, "w", encoding="utf-8"))
    print(f"{len(j['results']['bindings'])} rows -> {out}")


def cmd_wikitext(outdir, titles):
    os.makedirs(outdir, exist_ok=True)
    for t, (final, pid, rev, txt) in fetch_batch(titles[:50]).items():
        if txt is None:
            print(f"missing: {t}")
            continue
        open(os.path.join(outdir, safe_name(final) + ".wiki"), "w", encoding="utf-8").write(txt)
        print(f"{final}: {len(txt)} chars (rev {rev})")


def cmd_pull(tfile, out, pause):
    titles = [t.strip() for t in open(tfile, encoding="utf-8") if t.strip()]
    done = set()
    if os.path.exists(out):
        with gzip.open(out, "rt", encoding="utf-8") as f:
            for line in f:
                done.add(json.loads(line)["requested"])
    todo = [t for t in titles if t not in done]
    print(f"{len(titles)} titles, {len(done)} already pulled, {len(todo)} to go, {(len(todo) + 49) // 50} requests")
    missing = 0
    for i in range(0, len(todo), 50):
        batch = fetch_batch(todo[i:i + 50])
        with gzip.open(out, "at", encoding="utf-8") as f:
            for t, (final, pid, rev, txt) in batch.items():
                missing += txt is None
                f.write(json.dumps({"requested": t, "title": final, "pageid": pid, "revid": rev, "wikitext": txt},
                                   ensure_ascii=False) + "\n")
        print(f"  {min(i + 50, len(todo))}/{len(todo)}", flush=True)
        time.sleep(max(pause, 5 if LAST_SECONDS[0] > 1 else 0))   # Robot policy: >1 s to serve -> wait 5 s
    print(f"done; {missing} missing pages")


def cmd_parse(inp, outdir):
    os.makedirs(os.path.join(outdir, "text"), exist_ok=True)
    seen, n = set(), 0
    with gzip.open(inp, "rt", encoding="utf-8") as f, open(os.path.join(outdir, "battles.jsonl"), "w", encoding="utf-8") as o:
        for line in f:
            r = json.loads(line)
            if not r["wikitext"] or r["title"] in seen:
                continue
            seen.add(r["title"])
            a = parse_article(r["title"], r["wikitext"])
            a.update(pageid=r["pageid"], revid=r["revid"], requested=r["requested"])
            o.write(json.dumps(a, ensure_ascii=False) + "\n")
            open(os.path.join(outdir, "text", safe_name(r["title"]) + ".txt"), "w", encoding="utf-8").write(to_text(r["wikitext"]))
            n += 1
    print(f"{n} articles parsed -> {outdir}/battles.jsonl, text/")


def main(a):
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    if a[0] == "sparql" and len(a) == 3:
        cmd_sparql(a[1], a[2])
    elif a[0] == "wikitext" and len(a) >= 3:
        cmd_wikitext(a[1], a[2:])
    elif a[0] == "pull" and len(a) >= 3:
        pause = float(a[a.index("--pause") + 1]) if "--pause" in a else 3.0
        cmd_pull(a[1], a[2], pause)
    elif a[0] == "parse" and len(a) == 3:
        cmd_parse(a[1], a[2])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
