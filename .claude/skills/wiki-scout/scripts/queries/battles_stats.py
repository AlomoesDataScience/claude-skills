"""Battles 1700-1820: table and coverage report from wdpull.py parse output (local only, no requests).

Usage: python3 -I battles_stats.py PARSEDIR INDEXDIR [--years 1700-1820]
Reads PARSEDIR/battles.jsonl and INDEXDIR/battles-sources.json; writes PARSEDIR/battles.csv and prints coverage.
Kept: one row per page (redirects folded) with a conflict-type infobox and a year 1700-1820 in its date.
Numbers: n1/n2 = the first number in strength1/2 (men, or ships for naval), k1/k2 = the first number in
casualties1/2 by losses() (the "total" if given, else killed+wounded+captured+missing summed). Naval = infobox or title or categories say naval/sea, or the naval list names it.
Fails when: the first number is not the headline one ("2 regiments, 4,000 men" gives 2; "c. 10-12,000" gives 10);
a range or several estimates are given (only the first is taken); the casualty cell lists men in a form
losses() misses ("1,200 men", no kind word: the first number); a part counts the same men twice ("500 killed or
wounded; including 200 killed" sums 700); strength counts ships, not men (naval rows: read with care).
"""
import collections, csv, json, os, re, sys

FIELDS = ["title", "year", "date", "place", "lat", "lon", "partof", "result", "combatant1", "combatant2",
          "commander1", "commander2", "strength1", "strength2", "casualties1", "casualties2",
          "n1", "n2", "k1", "k2", "naval", "campaignboxes", "pageid", "revid"]


def first_num(s):
    m = re.search(r"(\d{1,3}(?:,\d{3})+|\d+)", s or "")
    return int(m.group(1).replace(",", "")) if m else None


NUM = r"(\d{1,3}(?:,\d{3})+|\d+)"
KINDS = r"kill|dead|died|wound|captur|prisoner|missing|desert|drown|casualt|loss|lost|surrender"


def losses(s):
    """Men lost: the number after "total" if given, else the sum of killed/wounded/captured/missing parts
    (low end of ranges; parts about ships, guns, colours or generals skipped), else the first number."""
    s = s or ""
    m = re.search(r"total[^0-9;]{0,15}" + NUM, s, re.I)
    if m:
        return int(m.group(1).replace(",", ""))
    tot, hit = 0, False
    for part in re.split(r";|\n", s):
        if re.search(r"ship|frigate|gun|cannon|colou?r|standard|flag|general|vessel|boat|brig|sloop|galley", part, re.I):
            continue
        m = re.match(r"\D{0,12}?" + NUM, part)
        if m and re.search(KINDS, part, re.I):
            tot, hit = tot + int(m.group(1).replace(",", "")), True
    return tot if hit else first_num(s)


def year_of(date):
    for y in re.findall(r"\b(1[3-9]\d\d)\b", date or ""):
        return int(y)
    return None


def main(a):
    if len(a) < 2:
        sys.exit(__doc__)
    pdir, idx = a[:2]
    y0, y1 = map(int, (a[a.index("--years") + 1] if "--years" in a else "1700-1820").split("-"))
    src = json.load(open(os.path.join(idx, "battles-sources.json"), encoding="utf-8"))
    rows, seen, n_all, no_box, out_of_range = [], set(), 0, 0, 0
    for line in open(os.path.join(pdir, "battles.jsonl"), encoding="utf-8"):
        b = json.loads(line)
        n_all += 1
        if b["pageid"] in seen:
            continue
        seen.add(b["pageid"])
        ib, t = b["infobox"], (b.get("infobox_type") or "").lower()
        if not re.search(r"conflict|battle|siege|naval", t):
            no_box += 1
            continue
        y = year_of(ib.get("date"))
        if y is None or not y0 <= y <= y1:
            out_of_range += 1
            continue
        lists = src.get(b["title"], []) + src.get(b.get("requested", ""), [])
        naval = bool(re.search(r"naval|\bsea\b", t + " " + b["title"] + " " + " ".join(b["categories"]), re.I)
                     or "List of naval battles" in lists)
        lat, lon = (b["coords"] or (None, None))[:2]
        r = {k: ib.get(k, "") for k in FIELDS if k in ib}
        r.update(partof=ib.get("part_of") or ib.get("partof", ""), place=ib.get("location") or ib.get("place", ""),
                 date=ib.get("date", ""), result=ib.get("result", ""))
        r.update(title=b["title"], year=y, lat=lat, lon=lon, naval=int(naval), pageid=b["pageid"], revid=b["revid"],
                 campaignboxes="; ".join(b["campaignboxes"]),
                 n1=first_num(ib.get("strength1")), n2=first_num(ib.get("strength2")),
                 k1=losses(ib.get("casualties1")), k2=losses(ib.get("casualties2")))
        rows.append(r)
    rows.sort(key=lambda r: (r["year"], r["title"]))
    with open(os.path.join(pdir, "battles.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    def share(rs, pred):
        return f"{sum(1 for r in rs if pred(r)) * 100 // max(1, len(rs))}%"

    both_n = lambda r: r["n1"] is not None and r["n2"] is not None
    both_k = lambda r: r["k1"] is not None and r["k2"] is not None
    print(f"{n_all} parsed, {len(seen)} pages, {no_box} without a conflict infobox, {out_of_range} dated outside "
          f"{y0}-{y1} or undated -> {len(rows)} engagements in battles.csv")
    print(f"all: strength both sides {share(rows, both_n)}, casualties both sides {share(rows, both_k)}, "
          f"coords {share(rows, lambda r: r['lat'] is not None)}, partof {share(rows, lambda r: r['partof'])}")
    for nv in (0, 1):
        rs = [r for r in rows if r["naval"] == nv]
        print(f"{'naval' if nv else 'land'} {len(rs)}: strength {share(rs, both_n)}, casualties {share(rs, both_k)}")
    print("per decade (count, strength both, casualties both):")
    dec = collections.defaultdict(list)
    for r in rows:
        dec[r["year"] // 10 * 10].append(r)
    print("  " + " | ".join(f"{d}s {len(rs)} {share(rs, both_n)} {share(rs, both_k)}" for d, rs in sorted(dec.items())))
    war = collections.defaultdict(list)
    for r in rows:
        war[re.sub(r"^the\s+|\s*\(.*", "", re.split(r";", r["partof"] or "(none)")[0].strip(), flags=re.I)[:60]].append(r)
    print("top wars (count, strength both, casualties both):")
    for k, rs in sorted(war.items(), key=lambda kv: -len(kv[1]))[:25]:
        print(f"  {len(rs):4} {share(rs, both_n):>4} {share(rs, both_k):>4}  {k}")


if __name__ == "__main__":
    main(sys.argv[1:])
