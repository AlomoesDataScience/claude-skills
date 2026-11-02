"""Search and read the local illwiki mirror (raw DokuWiki text) as clean text.

  python3 -I wiki.py search WORD [WORD...] [--ns top|dom5|all] [-n 20]   pages with all the words, ranked
  python3 -I wiki.py show PAGE [--section TEXT] [--raw]                 a page (or one section) as text
  python3 -I wiki.py toc PAGE                                            a page's section headings
  python3 -I wiki.py list [CATEGORY]                                     pages by category (no arg: the categories)
  python3 -I wiki.py grep REGEX [--ns ...]                               matching lines with their page

PAGE is a path under pages/ without .txt (`pythium-ma`, `dom5/pythium-ma`,
`user/loggy/castingai`), or a unique substring of one. Top-level pages are the Dominions 6 wiki; `dom5/`
is the old Dominions 5 wiki. The mirror lives in `Games/Fantasy Strategy/Dominions 6/illwiki/` (`fetch.sh` refreshes it).
"""
import argparse
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "illwiki", "pages"))

ERAS = ("-ea", "-ma", "-la")
CATEGORIES = {
    "nations": "nation pages (Dom6), e.g. pythium-ma, tir-na-n-og-ea",
    "abilities": "unit abilities and special attributes (one page each)",
    "magic": "paths, schools, globals, communion, empowerment, gems, sites, magic access",
    "mechanics": "dice, combat stats, morale, fatigue, provinces, scales, supply, turn order",
    "guides": "guides and strategy articles (Dom6)",
    "research": "community research pages under user/ (Loggy's tables and studies)",
    "dom5": "the old Dominions 5 wiki",
}
MAGIC = {"air", "astral", "blood", "blood-magic", "death", "earth", "fire", "glamour", "nature", "water", "holy",
         "alteration", "conjuration", "construction", "enchantment", "evocation", "thaumaturgy", "divine-magic",
         "combat-magic", "globals", "communion", "empowerment", "gems", "magic-sites", "magic-access", "magic",
         "mage-summons", "lab", "alchemy-spell", "magic-duel", "power", "fearbattleenchantments",
         "generic-blood-magic-guide", "blood-hunting", "bless", "thrones", "thrones-of-ascension", "pretenders",
         "pretender-god", "pretender-titles", "dominion-effects", "scales", "prophet", "disciples", "heretic",
         "forge-bonus", "master-smith", "spell-table-notation", "nexus", "void", "twilight", "lichcraft"}
MECH = {"drn", "attack-skill", "defence-skill", "precision", "protection", "natural-protection", "hit-points", "hp",
        "strength", "size", "encumbrance", "fatigue", "morale", "rout", "retreat", "experience", "afflictions",
        "map-movement", "population", "province-attributes", "province-defense", "provinces", "supplies", "unrest",
        "turn-order-sequence", "weather", "stealth", "assassin", "independents", "random-events", "gold", "levy",
        "old-age", "age", "ages", "starving", "sailing", "underwater", "combat-speed", "stacking-effects-bob",
        "commander", "resistances", "resistance", "harassment", "thugs-and-supercombatants", "patchnotes",
        "new-player-guide", "join-multiplayer-game-guide", "naps", "unit-abilities", "unit-attributes"}


def pages(ns="top"):
    out = []
    for d, _, files in os.walk(ROOT):
        for f in files:
            if not f.endswith(".txt"):
                continue
            rel = os.path.relpath(os.path.join(d, f), ROOT)[:-4]
            top = "/" not in rel
            if ns == "all" or (ns == "top" and top) or (ns == "dom5" and rel.startswith("dom5/")) or \
                    (ns not in ("top", "dom5", "all") and rel.startswith(ns)):
                out.append(rel)
    return sorted(out)


def resolve(q):
    q = q.strip().removesuffix(".txt")
    if os.path.exists(os.path.join(ROOT, q + ".txt")):
        return q
    hits = [p for p in pages("all") if q.lower() in p.lower()]
    top = [p for p in hits if "/" not in p]
    if len(top) == 1:
        return top[0]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        sys.exit(f"no page matches {q!r}")
    sys.exit(f"{q!r} matches {len(hits)} pages: " + ", ".join(hits[:30]))


def read(p):
    with open(os.path.join(ROOT, p + ".txt"), encoding="utf-8", errors="replace") as f:
        return f.read()


def clean(t):
    t = re.sub(r"\{\{[^}]*\}\}", "", t)                                  # images and includes
    t = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", t)                   # [[target|label]]
    t = re.sub(r"\[\[([^\]]*)\]\]", lambda m: m.group(1).split(":")[-1], t)
    t = re.sub(r"^(={2,6})\s*(.*?)\s*={2,6}\s*$", lambda m: "#" * max(1, 7 - len(m.group(1))) + " " + m.group(2), t, flags=re.M)
    t = re.sub(r"(?<!:)//(.*?)//", r"\1", t)                             # italics
    t = re.sub(r"</?(?:wrap|WRAP|html|HTML|nowiki|del|sup|sub|color[^>]*|font[^>]*)[^>]*>", "", t)
    t = re.sub(r"^\s*[\^|]", "|", t, flags=re.M)                           # table rows start with | or ^
    t = re.sub(r"\s*\^\s*", " | ", t)
    t = re.sub(r"[ \t]{2,}", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def sections(t):
    """[(level, title, body)] from cleaned text."""
    out, cur = [], [0, "(top)", []]
    for line in t.split("\n"):
        m = re.match(r"^(#{1,6}) (.*)$", line)
        if m:
            out.append(tuple(cur[:2]) + ("\n".join(cur[2]),))
            cur = [len(m.group(1)), m.group(2), []]
        else:
            cur[2].append(line)
    out.append(tuple(cur[:2]) + ("\n".join(cur[2]),))
    return out


def cmd_search(a):
    words = [w.lower() for w in a.words]
    res = []
    for p in pages(a.ns):
        raw = read(p)
        t = raw.lower()
        if all(w in t for w in words):
            score = sum(t.count(w) for w in words) + 50 * sum(w in p.lower() for w in words)
            res.append((score, p, raw))
    for score, p, raw in sorted(res, reverse=True)[:a.n]:
        i = raw.lower().find(words[0])
        snip = re.sub(r"\s+", " ", clean(raw[max(0, i - 80):i + 160]))
        print(f"{p}  ({score})\n    …{snip}…")
    print(f"{len(res)} pages")


def cmd_show(a):
    p = resolve(a.page)
    t = read(p) if a.raw else clean(read(p))
    if a.section:
        secs = sections(t)
        hit = [i for i, s in enumerate(secs) if a.section.lower() in s[1].lower()]
        if not hit:
            sys.exit("sections: " + " | ".join(s[1] for s in secs))
        i = hit[0]
        lvl = secs[i][0]
        body = [f"{'#' * lvl} {secs[i][1]}", secs[i][2]]
        for s in secs[i + 1:]:
            if s[0] <= lvl:
                break
            body += [f"{'#' * s[0]} {s[1]}", s[2]]
        t = "\n".join(body)
    print(f"[{p}]\n{t}")


def cmd_toc(a):
    p = resolve(a.page)
    for lvl, title, body in sections(clean(read(p))):
        print(f"{'  ' * max(0, lvl - 1)}{title}  ({len(body)} chars)")


def category(p):
    if p.startswith("dom5/"):
        return "dom5"
    if p.startswith("user/"):
        return "research"
    if p.startswith("guides") or p.startswith("wiki/common") or p.startswith("game-mechanics"):
        return "guides"
    if "/" in p:
        return None
    if p.endswith(ERAS) or p in ("mictlan",):
        return "nations"
    if p in MAGIC:
        return "magic"
    if p in MECH:
        return "mechanics"
    return "abilities"


def cmd_list(a):
    if not a.category:
        for c, d in CATEGORIES.items():
            n = sum(category(p) == c for p in pages("all"))
            print(f"{c:10} {n:4}  {d}")
        return
    for p in pages("all"):
        if category(p) == a.category:
            print(f"{p}  ({os.path.getsize(os.path.join(ROOT, p + '.txt')) // 1000} kB)")


def cmd_grep(a):
    rx = re.compile(a.regex, re.I)
    n = 0
    for p in pages(a.ns):
        for line in read(p).split("\n"):
            if rx.search(line):
                print(f"{p}: {clean(line)[:220]}")
                n += 1
                if n >= a.n:
                    return


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search"); s.add_argument("words", nargs="+"); s.add_argument("--ns", default="top"); s.add_argument("-n", type=int, default=20)
    s = sub.add_parser("show"); s.add_argument("page"); s.add_argument("--section"); s.add_argument("--raw", action="store_true")
    s = sub.add_parser("toc"); s.add_argument("page")
    s = sub.add_parser("list"); s.add_argument("category", nargs="?")
    s = sub.add_parser("grep"); s.add_argument("regex"); s.add_argument("--ns", default="top"); s.add_argument("-n", type=int, default=60)
    a = ap.parse_args()
    {"search": cmd_search, "show": cmd_show, "toc": cmd_toc, "list": cmd_list, "grep": cmd_grep}[a.cmd](a)


if __name__ == "__main__":
    main()
