"""One pass over the English Wikipedia XML dump, one part at a time: catalogue every article, keep full text for
the fields we want, check the extraction, then delete the part (the user 2026-11-16: "delete it directly after
confirming we don't want it").

Usage: python3 -I dumppass.py COMMAND ...
  sums   OUT PARTS                    download the run's sha1sums list once (one request) into PARTS
  run    OUT PARTS --parts 1,36|2-71 [--keep] [--pause 10]
                                      for each part not yet done: check disk, download (one connection, policy UA),
                                      verify sha1, extract, check, then rm the part (--keep leaves it for re-runs)
  extract OUT FILE                    re-run extraction on a part already on disk (rule tuning; no requests)
  report OUT [--samples 12]           keep rate, bytes, projected size, sample kept and dropped titles per field
  OUT    output folder (Theory/Sources/Wikipedia/enwiki-dump/): catalogue/part-NN.tsv.gz, text/part-NN.jsonl.xz
         (articles matching a field), rest/part-NN.jsonl.xz (every other article, with "why"), other/part-NN.jsonl.xz
         (Template, Category and Portal pages: navboxes and campaignboxes),
         done.json (per-part stats; parts listed there are skipped, so run resumes)
  PARTS  download folder, separate from OUT and from scripts (downloads are untrusted)
Rules: ../dump-rules.json (fields, exclusions, people rule). Contact for the User-Agent:
  <workspace>/.claude/private/wikimedia-contact.txt (the user approved his email for Wikimedia only, 2026-11-16).
Catalogue columns: pageid, ns (0 article, 14 category), title, bytes, redirect target, short description,
  infoboxes (;), fields (,), why (first rule that decided), categories (|).
Text rows (jsonl): {"title", "pageid", "revid", "fields": {field: why}, "wikitext"}; rest rows have "why" instead
  of "fields"; other rows have "ns". Nothing is thrown away (the user 2026-11-16: keep the whole thing): the rules only
  sort articles into text/ (read first) and rest/.
Site rules (site-rules skill, dumps.wikimedia.org): WMF User-Agent policy enforced, at most 3 connections per IP;
  we use one. Any HTTP error stops the run (failure protocol: no automatic retry).
Fails when: categories added by templates (navboxes, {{Disambiguation}}, year templates) are not in the wikitext,
  so rules see only explicit categories; keyword rules miss narrowly named categories and pull noise from broad
  words; a part's last page id may be a deleted page (the range check then reports, not fails).
"""
import gzip, hashlib, json, lzma, os, random, re, shutil, subprocess, sys, time
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
RULES = os.path.join(HERE, "..", "dump-rules.json")
CONTACT = os.path.join(ROOT, ".claude", "private", "wikimedia-contact.txt")
BASE = "https://dumps.wikimedia.org/enwiki/"
SUMS = "enwiki-latest-sha1sums.txt"
PART_RX = re.compile(r"^enwiki-(\w+)-pages-articles(?:-multistream)?(\d+)\.xml-p(\d+)p(\d+)\.bz2$")
# The run's sha1sums list (checked 2026-11-16, run 20261101) holds the plain pages-articles parts (71, ids 1-84,714,711,
# no gaps) but not the multistream ones, so we use the plain parts: same pages, sha1 verifiable.
MIN_FREE = 4 * 1024 ** 3
# Namespaces whose pages are kept: 0 article (text/ if a field matches, else rest/), and in other/ the full text of
# 14 Category, 10 Template (navboxes, campaignboxes), 100 Portal. The user 2026-11-16: keep the whole thing, storage is fine.
KEEP_NS = ("0", "10", "14", "100")


def ua():
    if not os.path.exists(CONTACT):
        sys.exit(f"no contact file {CONTACT}: the WMF User-Agent policy needs contact info (ask the user)")
    email = open(CONTACT).read().strip()
    ver = subprocess.run(["curl", "--version"], capture_output=True, text=True).stdout.split()[1]
    return f"AI-Development-workspace-dumpbot/1.0 ({email}; personal offline research, one download at a time) curl/{ver}"


def curl(url, dest):
    """One request, one connection. Resumes a partial file. Returns the HTTP code; never retries."""
    tmp = dest + ".partial"
    cmd = ["curl", "-sS", "--proto", "=https", "-A", ua(), "-H", "Accept-Encoding: identity",
           "-o", tmp, "-w", "%{http_code}", url]
    if os.path.exists(tmp):
        cmd[1:1] = ["-C", "-"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    code = r.stdout.strip()[-3:]
    if r.returncode != 0 or code not in ("200", "206"):
        sys.exit(f"STOP: {url} -> curl rc {r.returncode}, HTTP {code} {r.stderr.strip()[:200]} (not retried)")
    os.replace(tmp, dest)
    return code


def parts_list(partsdir):
    p = os.path.join(partsdir, SUMS)
    if not os.path.exists(p):
        sys.exit(f"no {p}: run 'sums' first")
    out = []
    for line in open(p, encoding="ascii", errors="replace"):
        m = re.match(r"^([0-9a-f]{40})\s+(\S+)$", line.strip())
        if m and PART_RX.match(m.group(2)):
            g = PART_RX.match(m.group(2))
            out.append({"sha1": m.group(1), "name": m.group(2), "run": g.group(1),
                        "first": int(g.group(3)), "last": int(g.group(4))})
    out.sort(key=lambda d: d["first"])
    for i, d in enumerate(out, 1):
        d["n"] = i
    return out


# ---------- rules ----------
def load_rules():
    R = json.load(open(RULES, encoding="utf-8"))
    c = lambda s: re.compile(s, re.I)
    rules = {
        "fields": {k: c(v) for k, v in R["fields"].items()},
        "strong": {k: c(v) for k, v in R["strong_words"].items()},
        "infobox": {k: c(v) for k, v in R["infobox"].items()},
        "ib_people": c(R["infobox_people_ok"]),
        "titles": {k: re.compile(v) for k, v in R["title_patterns"].items()},
        "exclude": c(R["exclude"]), "ex_sd": c(R["exclude_shortdesc"]),
        "person": re.compile(R["person"], re.I | re.M), "people": c(R["people"]),
        "skip": c(R["skip_templates"]), "lists": {},
    }
    for tl in R.get("title_lists", []):
        f = os.path.join(ROOT, tl["file"])
        for t in open(f, encoding="utf-8"):
            if t.strip():
                rules["lists"][t.strip()] = tl["field"]
    return rules


CAT = re.compile(r"\[\[\s*category\s*:\s*([^\]|\n]+)", re.I)
SD = re.compile(r"\{\{\s*short description\s*\|\s*([^}|\n]*)", re.I)
IB = re.compile(r"\{\{\s*infobox[ _]+([^|}\n<]+)", re.I)


def classify(R, title, cats, sd, ibs, text):
    """-> (fields {field: why}, why) ; empty fields = not kept."""
    hay = "\n".join(cats) + "\n" + sd
    f, strong = {}, False
    for ib in ibs:
        for k, rx in R["infobox"].items():
            if rx.search(ib):
                f.setdefault(k, "infobox:" + ib); strong = True
    for k, rx in R["titles"].items():
        if rx.search(title):
            f.setdefault(k, "title"); strong = True
    if title in R["lists"]:
        f.setdefault(R["lists"][title], "list"); strong = True
    for k, rx in R["strong"].items():
        m = rx.search(hay)
        if m:
            f.setdefault(k, "strong:" + m.group(0)); strong = True
    if f and R["skip"].search(text):
        return {}, "dab"
    person = R["person"].search("\n".join(cats))
    if person and strong and not any(R["ib_people"].search(i) for i in ibs) and not R["people"].search(hay):
        strong = False; f = {}           # a person kept only by a weak strong-word: apply the people rule below
    if not strong:
        m = R["exclude"].search(hay) or (R["ex_sd"].search(sd) if sd else None)
        if m:
            return {}, "excl:" + m.group(0).lower()
        if person:
            m = R["people"].search(hay)
            if not m:
                return {}, "person"
            f["people"] = "people:" + m.group(0).lower()
        for k, rx in R["fields"].items():
            m = rx.search(hay)
            if m:
                f.setdefault(k, "cat:" + m.group(0).lower())
        if person and len(f) == 1:
            return {}, "person-nofield"
        if f and R["skip"].search(text):
            return {}, "dab"
    else:
        for k, rx in R["fields"].items():          # kept by a strong rule: label its other fields too
            m = rx.search(hay)
            if m:
                f.setdefault(k, "cat:" + m.group(0).lower())
    why = next(iter(f.values())) if f else "nomatch"
    return f, why


# ---------- extraction ----------
def clean(s):
    return s.replace("\t", " ").replace("\n", " ").replace("\r", " ")


def extract(out, path, part):
    """Stream one .bz2 part. Writes catalogue and text to .tmp files, renames after the check. -> stats dict."""
    R = load_rules()
    n = part["n"]
    os.makedirs(os.path.join(out, "catalogue"), exist_ok=True)
    for d in ("text", "rest", "other"):
        os.makedirs(os.path.join(out, d), exist_ok=True)
    cat_p = os.path.join(out, "catalogue", f"part-{n:02d}.tsv.gz")
    txt_p = os.path.join(out, "text", f"part-{n:02d}.jsonl.xz")
    rest_p = os.path.join(out, "rest", f"part-{n:02d}.jsonl.xz")
    oth_p = os.path.join(out, "other", f"part-{n:02d}.jsonl.xz")
    cat_t, txt_t, rest_t, oth_t = cat_p + ".tmp", txt_p + ".tmp", rest_p + ".tmp", oth_p + ".tmp"
    st = {"part": n, "name": part["name"], "pages": 0, "ns": {}, "articles": 0, "redirects": 0, "categories": 0,
          "article_bytes": 0, "kept": 0, "kept_bytes": 0, "by_field": {}, "field_bytes": {}, "why": {},
          "min_id": None, "max_id": None, "out_of_range": 0, "rest": 0, "other": 0, "t0": time.time()}
    bz = subprocess.Popen(["bzip2", "-dc", path], stdout=subprocess.PIPE)
    with open(txt_t, "wb") as tf, open(rest_t, "wb") as rf, open(oth_t, "wb") as of:
        xz = subprocess.Popen(["xz", "-6", "-T2", "-c"], stdin=subprocess.PIPE, stdout=tf)
        xr = subprocess.Popen(["xz", "-6", "-T4", "-c"], stdin=subprocess.PIPE, stdout=rf)
        xo = subprocess.Popen(["xz", "-6", "-T2", "-c"], stdin=subprocess.PIPE, stdout=of)
        cf = gzip.open(cat_t, "wt", encoding="utf-8", compresslevel=6)
        root = None
        for ev, el in ET.iterparse(bz.stdout, events=("start", "end")):
            if root is None:
                root = el
            if ev != "end" or not el.tag.endswith("}page"):
                continue
            d = {}
            for ch in el:
                tag = ch.tag.rsplit("}", 1)[-1]
                if tag in ("title", "ns", "id"):
                    d[tag] = ch.text or ""
                elif tag == "redirect":
                    d["redirect"] = ch.get("title", "")
                elif tag == "revision":
                    for rc in ch:
                        rt = rc.tag.rsplit("}", 1)[-1]
                        if rt == "id":
                            d["revid"] = rc.text
                        elif rt == "text":
                            d["text"] = rc.text or ""
            root.clear()
            st["pages"] += 1
            ns, pid = d.get("ns", ""), int(d.get("id", "0"))
            st["ns"][ns] = st["ns"].get(ns, 0) + 1
            st["min_id"] = pid if st["min_id"] is None else min(st["min_id"], pid)
            st["max_id"] = pid if st["max_id"] is None else max(st["max_id"], pid)
            if not part["first"] <= pid <= part["last"]:
                st["out_of_range"] += 1
            if ns not in KEEP_NS:
                continue
            text, title = d.get("text", ""), d.get("title", "")
            red = d.get("redirect", "")
            if red:
                st["redirects"] += 1
                cf.write(f"{pid}\t{ns}\t{clean(title)}\t{len(text)}\t{clean(red)}\t\t\t\t\t\n")
                continue
            cats = [c.strip() for c in CAT.findall(text)]
            m = SD.search(text)
            sd = m.group(1).strip() if m else ""
            ibs = [i.strip().lower() for i in IB.findall(text)]
            fields, why = {}, ""
            if ns != "0":
                if ns == "14":
                    st["categories"] += 1
                st["other"] += 1
                row = {"title": d.get("title", ""), "pageid": pid, "revid": int(d.get("revid") or 0), "ns": int(ns), "wikitext": text}
                xo.stdin.write((json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8"))
                if ns != "14":
                    continue
            else:
                st["articles"] += 1
                st["article_bytes"] += len(text)
                fields, why = classify(R, title, cats, sd, ibs, text)
                key = why.split(":")[0] if not fields else "kept"
                st["why"][key] = st["why"].get(key, 0) + 1
            cf.write("\t".join([str(pid), ns, clean(title), str(len(text)), "", clean(sd), clean(";".join(ibs)),
                                ",".join(fields), clean(why), clean("|".join(cats))]) + "\n")
            if fields:
                st["kept"] += 1
                st["kept_bytes"] += len(text)
                for k in fields:
                    st["by_field"][k] = st["by_field"].get(k, 0) + 1
                    st["field_bytes"][k] = st["field_bytes"].get(k, 0) + len(text)
                row = {"title": title, "pageid": pid, "revid": int(d.get("revid") or 0), "fields": fields, "wikitext": text}
                xz.stdin.write((json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8"))
            elif ns == "0":
                st["rest"] += 1
                row = {"title": title, "pageid": pid, "revid": int(d.get("revid") or 0), "why": why, "wikitext": text}
                xr.stdin.write((json.dumps(row, ensure_ascii=False) + "\n").encode("utf-8"))
        cf.close()
        for x in (xz, xr, xo):
            x.stdin.close()
        xz_rc = max(abs(x.wait()) for x in (xz, xr, xo))
    bz_rc = bz.wait()
    st["seconds"] = round(time.time() - st.pop("t0"))
    # ---- check ----
    probs = []
    if bz_rc != 0:
        probs.append(f"bzip2 rc {bz_rc}")
    if xz_rc != 0:
        probs.append(f"xz rc {xz_rc}")
    if st["out_of_range"]:
        probs.append(f"{st['out_of_range']} page ids outside p{part['first']}p{part['last']}")
    with gzip.open(cat_t, "rt", encoding="utf-8") as g:
        cat_rows = sum(1 for _ in g)
    with lzma.open(txt_t, "rt", encoding="utf-8") as x:
        txt_rows = sum(1 for _ in x)
    want = st["articles"] + st["redirects"] + st["categories"]
    if cat_rows != want:
        probs.append(f"catalogue rows {cat_rows} != pages {want}")
    if txt_rows != st["kept"]:
        probs.append(f"text rows {txt_rows} != kept {st['kept']}")
    with lzma.open(rest_t, "rt", encoding="utf-8") as x:
        rest_rows = sum(1 for _ in x)
    with lzma.open(oth_t, "rt", encoding="utf-8") as x:
        oth_rows = sum(1 for _ in x)
    if rest_rows != st["articles"] - st["kept"]:
        probs.append(f"rest rows {rest_rows} != articles - kept {st['articles'] - st['kept']}")
    if oth_rows != st["other"]:
        probs.append(f"other rows {oth_rows} != {st['other']}")
    st["last_id_reached"] = st["max_id"] == part["last"]
    st["catalogue_bytes"], st["text_bytes"] = os.path.getsize(cat_t), os.path.getsize(txt_t)
    st["rest_bytes"], st["other_bytes"] = os.path.getsize(rest_t), os.path.getsize(oth_t)
    st["problems"] = probs
    if probs:
        print("CHECK FAILED: " + "; ".join(probs) + f" (part kept: {path})")
        return st
    os.replace(cat_t, cat_p)
    os.replace(txt_t, txt_p)
    os.replace(rest_t, rest_p)
    os.replace(oth_t, oth_p)
    return st


def save_done(out, st):
    p = os.path.join(out, "done.json")
    done = json.load(open(p)) if os.path.exists(p) else {}
    done[str(st["part"])] = st
    json.dump(done, open(p + ".tmp", "w"), indent=1)
    os.replace(p + ".tmp", p)


def show(st):
    a = max(st["articles"], 1)
    print(f"part {st['part']}: {st['pages']:,} pages, {st['articles']:,} articles, {st['redirects']:,} redirects, "
          f"{st['categories']:,} categories, {st['seconds']} s")
    print(f"  kept {st['kept']:,} articles ({100 * st['kept'] / a:.1f}%), {st['kept_bytes'] / 1e6:,.0f} MB of "
          f"{st['article_bytes'] / 1e6:,.0f} MB text; written: text {st['text_bytes'] / 1e6:,.0f} MB xz, "
          f"catalogue {st['catalogue_bytes'] / 1e6:,.0f} MB gz, rest {st.get('rest_bytes', 0) / 1e6:,.0f} MB xz "
          f"({st.get('rest', 0):,} articles), other {st.get('other_bytes', 0) / 1e6:,.0f} MB xz ({st.get('other', 0):,} pages)")
    print(f"  ids {st['min_id']}-{st['max_id']} (last id reached: {st['last_id_reached']}); "
          f"problems: {st['problems'] or 'none'}")


def parse_parts(spec, total):
    s = set()
    for bit in spec.split(","):
        a, _, b = bit.partition("-")
        s.update(range(int(a), int(b or a) + 1))
    return sorted(x for x in s if 1 <= x <= total)


# ---------- commands ----------
def cmd_sums(out, partsdir):
    os.makedirs(partsdir, exist_ok=True)
    dest = os.path.join(partsdir, SUMS)
    if os.path.exists(dest):
        sys.exit(f"{dest} exists; not fetched again")
    curl(BASE + "latest/" + SUMS, dest)
    ps = parts_list(partsdir)
    print(f"{len(ps)} parts, run {ps[0]['run'] if ps else '?'} -> {dest}")


def cmd_run(out, partsdir, spec, keep, pause):
    ps = parts_list(partsdir)
    done = json.load(open(os.path.join(out, "done.json"))) if os.path.exists(os.path.join(out, "done.json")) else {}
    todo = [p for p in ps if p["n"] in parse_parts(spec, len(ps))]
    first = True
    for p in todo:
        if str(p["n"]) in done and not done[str(p["n"])]["problems"]:
            print(f"part {p['n']} done already, skipped"); continue
        free = shutil.disk_usage(out).free
        if free < MIN_FREE:
            sys.exit(f"STOP: {free / 1e9:.1f} GB free, need {MIN_FREE / 1e9:.0f} GB before a download")
        path = os.path.join(partsdir, p["name"])
        if not os.path.exists(path):
            if not first:
                time.sleep(pause)
            run = p["run"] if re.fullmatch(r"\d{8}", p["run"]) else "latest"
            t = time.time()
            curl(BASE + run + "/" + p["name"], path)
            print(f"part {p['n']}: downloaded {os.path.getsize(path) / 1e6:,.0f} MB in {time.time() - t:.0f} s")
            first = False
        h = hashlib.sha1()
        with open(path, "rb") as f:
            for b in iter(lambda: f.read(1 << 20), b""):
                h.update(b)
        if h.hexdigest() != p["sha1"]:
            sys.exit(f"STOP: sha1 mismatch for {path} (kept for inspection)")
        st = extract(out, path, p)
        save_done(out, st)
        show(st)
        if st["problems"]:
            sys.exit("STOP: check failed, part kept")
        if keep:
            print(f"  kept on disk (--keep): {path}")
        else:
            os.remove(path)
            print(f"  checked, deleted {p['name']}")


def cmd_extract(out, path):
    name = os.path.basename(path)
    g = PART_RX.match(name)
    if not g:
        sys.exit(f"not a part file name: {name}")
    ps = {p["name"]: p for p in parts_list(os.path.dirname(os.path.abspath(path)))}
    st = extract(out, path, ps[name])
    save_done(out, st)
    show(st)


def cmd_report(out, samples):
    done = json.load(open(os.path.join(out, "done.json")))
    n_all = 71
    tot = {k: sum(d.get(k, 0) for d in done.values()) for k in ("articles", "kept", "article_bytes", "kept_bytes", "text_bytes", "catalogue_bytes", "rest_bytes", "other_bytes")}
    print(f"{len(done)} parts done: {tot['kept']:,} of {tot['articles']:,} articles kept "
          f"({100 * tot['kept'] / max(tot['articles'], 1):.1f}%), text {tot['kept_bytes'] / 1e6:,.0f} of "
          f"{tot['article_bytes'] / 1e6:,.0f} MB ({100 * tot['kept_bytes'] / max(tot['article_bytes'], 1):.1f}%)")
    w = tot['text_bytes'] + tot['catalogue_bytes'] + tot['rest_bytes'] + tot['other_bytes']
    print(f"written {tot['text_bytes'] / 1e6:,.0f} MB text + {tot['rest_bytes'] / 1e6:,.0f} MB rest + "
          f"{tot['other_bytes'] / 1e6:,.0f} MB other + {tot['catalogue_bytes'] / 1e6:,.0f} MB catalogue; "
          f"naive x{n_all}/{len(done)} projection {w * n_all / len(done) / 1e9:.1f} GB "
          f"(part 1 holds the oldest, longest articles: it overstates)")
    bf, fb, why = {}, {}, {}
    for d in done.values():
        for k, v in d["by_field"].items(): bf[k] = bf.get(k, 0) + v
        for k, v in d["field_bytes"].items(): fb[k] = fb.get(k, 0) + v
        for k, v in d["why"].items(): why[k] = why.get(k, 0) + v
    print("by field (an article can be in several): " + ", ".join(f"{k} {v:,} ({fb[k] / 1e6:,.0f} MB)" for k, v in sorted(bf.items(), key=lambda x: -x[1])))
    print("decided by: " + ", ".join(f"{k} {v:,}" for k, v in sorted(why.items(), key=lambda x: -x[1])))
    rnd = random.Random(7)
    kept, dropped, excl = {}, {}, {}
    for d in done.values():
        with gzip.open(os.path.join(out, "catalogue", f"part-{d['part']:02d}.tsv.gz"), "rt", encoding="utf-8") as g:
            for line in g:
                c = line.rstrip("\n").split("\t")
                if c[1] != "0" or c[4]:
                    continue
                if c[7]:
                    for k in c[7].split(","):
                        kept.setdefault(k, []).append(f"{c[2]}  [{c[8]}]")
                elif int(c[3]) > 8000:
                    key = c[8].split(":")[0]
                    (excl.setdefault(c[8], []) if key == "excl" else dropped.setdefault(key, [])).append(
                        f"{c[2]}  [{c[8]}] {c[5][:50]}")
    for k, v in sorted(kept.items()):
        print(f"\nKEPT {k} ({len(v):,}): " + " | ".join(rnd.sample(v, min(samples, len(v)))))
    for k, v in sorted(dropped.items()):
        print(f"\nDROPPED {k}, over 8 KB ({len(v):,}): " + " | ".join(rnd.sample(v, min(samples, len(v)))))
    top = sorted(excl.items(), key=lambda x: -len(x[1]))[:15]
    print("\nEXCLUDED over 8 KB, top words: " + ", ".join(f"{k[5:]} {len(v):,}" for k, v in top))
    allx = [t for v in excl.values() for t in v]
    print("  sample: " + " | ".join(rnd.sample(allx, min(samples, len(allx)))))


def main(a):
    if len(a) < 2:
        sys.exit(__doc__)
    cmd, out = a[0], os.path.abspath(a[1])
    if cmd == "sums" and len(a) >= 3:
        cmd_sums(out, os.path.abspath(a[2]))
    elif cmd == "run" and len(a) >= 3 and "--parts" in a:
        cmd_run(out, os.path.abspath(a[2]), a[a.index("--parts") + 1], "--keep" in a,
                int(a[a.index("--pause") + 1]) if "--pause" in a else 10)
    elif cmd == "extract" and len(a) >= 3:
        cmd_extract(out, os.path.abspath(a[2]))
    elif cmd == "report":
        cmd_report(out, int(a[a.index("--samples") + 1]) if "--samples" in a else 12)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
