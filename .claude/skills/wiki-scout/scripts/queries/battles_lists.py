"""Titles of every engagement 1700-1820 from the saved index pages + Wikidata results (local only, no requests).

Usage: python3 -I battles_lists.py INDEXDIR OUT_PREFIX [--years 1700-1820] [--lists "List A;List B"]
Year per line: a table cell that is a bare year (rowspan carries it to the next rows), a list-page section
heading (1701-1720 ...), or "(YYYY" on a bullet line (List of sieges). Links on lines whose year is 1700-1820.
Writes OUT_PREFIX-titles.txt (to pull), OUT_PREFIX-sources.json (title -> which lists / wikidata).
Fails when: the engagement cell is unlinked (the row's next non-war link, often a commander, is taken; the
parse step drops it for lack of a conflict infobox); a table row's year cell is missing and the rowspan count is off (the previous year is kept, so a
row can be dated a year early).
"""
import collections, json, os, re, sys

LISTS = ["List of battles 1601–1800", "List of battles 1801–1900", "List of naval battles", "List of sieges"]
NOT = re.compile(r"^(file|image|category|wikt|wiktionary|list of|portal|template|help|wikipedia):", re.I)


def year_lines(text):
    year = None
    for line in text.split("\n"):
        h = re.match(r"^=+\s*(\d{4})\s*[-–]\s*(\d{4})\s*=+", line)
        if h:
            year = int(h.group(1))
            continue
        h = re.match(r"^=+\s*(.*?)\s*=+\s*$", line)
        if h:                                   # other headings ("18th century") reset until a year shows
            year = None
            continue
        cells = [c.strip() for c in re.split(r"\|\||^\|", line) if c.strip()]
        for c in cells[:2]:
            m = re.match(r'^(?:rowspan\s*=\s*"?\d+"?\s*\|\s*)?(\d{4})$', c)
            if m:
                year = int(m.group(1))
        m = re.search(r"\((?:c\.\s*)?(\d{4})", line) if line.startswith("*") else None
        y = int(m.group(1)) if m else year
        yield y, line


def main(a):
    global LISTS
    if len(a) < 2:
        sys.exit(__doc__)
    idx, pre = a[:2]
    y0, y1 = map(int, (a[a.index("--years") + 1] if "--years" in a else "1700-1820").split("-"))
    if "--lists" in a:
        LISTS = a[a.index("--lists") + 1].split(";")
    src = collections.defaultdict(set)
    war = re.compile(r"\b(War|Wars|war|Rebellion|Revolution|Uprising|Revolt|Campaign|Expedition of|Conflict|Crisis)\b")
    for name in LISTS:
        text = open(os.path.join(idx, name + ".wiki"), encoding="utf-8").read()
        for y, line in year_lines(text):
            if y is None or not y0 <= y <= y1:
                continue
            for t in re.findall(r"\[\[([^\[\]|#]+)", line):    # the first link that is not a war = the engagement
                t = t.strip()
                if not t or NOT.match(t) or t.startswith(":") or war.search(t) and not re.match(r"^(Battle|Siege|Action)", t):
                    continue
                src[t[0].upper() + t[1:]].add(name)
                break
    wd = json.load(open(os.path.join(idx, "wikidata.json"), encoding="utf-8"))
    for b in wd["results"]["bindings"]:
        src[b["title"]["value"]].add("wikidata")
    eng = re.compile(r"^(Battle|Battles|Siege|Sieges|Action|Capture|Raid|Bombardment|Storming|Combat|Sack|Relief|Assault|"
                     r"Attack|Blockade|Invasion|Naval|First|Second|Third|Fourth|Fall|Defence|Defense|Engagement|Affair|"
                     r"Massacre|Ambush|Landing|Cutting|Recapture|Burning|Destruction|Crossing|Passage|Cannonade|Glorious)\b")
    keep = set(src)
    open(pre + "-titles.txt", "w", encoding="utf-8").write("\n".join(sorted(keep)) + "\n")
    json.dump({t: sorted(s) for t, s in sorted(src.items())}, open(pre + "-sources.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=0)
    by = collections.Counter(frozenset(src[t]) for t in keep)
    print(f"{len(src)} linked titles, {len(keep)} kept to pull; wikidata only "
          f"{sum(1 for t in keep if src[t] == {'wikidata'})}, lists only {sum(1 for t in keep if 'wikidata' not in src[t])}, "
          f"engagement-named {sum(1 for t in keep if eng.match(t))}")


if __name__ == "__main__":
    main(sys.argv[1:])
