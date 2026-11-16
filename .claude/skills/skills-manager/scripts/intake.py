#!/usr/bin/env python3
"""The new-skill pipeline (the user 2026-11-14, "New Skills Documentation"): every new or rewritten skill goes
through the same six steps, so the other skills keep agreeing with it.

  python3 -I intake.py wanted [--n 40]           1. skills to add: skill ideas named in BACKLOG.md, Proposals/,
                                                    plans and checklists that no skill covers yet
  python3 -I intake.py scan NAME | --topic "TEXT" [--n 8] [--all]
                                                 2. what to read first: the skills and documents that share
                                                    the topic, each with the sections to open (--all: also
                                                    Archive/, old summaries, third-party repos/)
     (step 4: write the skill with write-skill and skills.py new)
  python3 -I intake.py run NAME [--n 8] [--all]  3 + 5 + 6. after writing it: the lines in other skills to
                                                    check against it, proposals (links both ways, overlaps,
                                                    routes.md row, routing test case, lint), and a review
                                                    file in .claude/skill-intake/DATE-NAME.md to tick off

Terms are the skill's distinctive word stems (name, description, keywords, headings), weighted by how few
other skills use them. Matching is by words only, so it suggests what to read and check; Claude decides.
Reads files only; `run` writes only its review file. Pure standard library.
"""
import argparse
import datetime
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skills as S  # noqa: E402

PROJECT = S.PROJECT
OUT = os.path.join(S.CLAUDE, "skill-intake")
SKIP = {".git", "__pycache__", "node_modules", "bin", "obj", "skills", "skills-disabled", "skill-intake",
        "skill-sync", "handoff"}
SKIP_OLD = {"Archive", "Archived", "Old Claude Summaries For Review", "repos"}   # repos: third-party checkouts
DOC_MAX = 300_000
RULE = re.compile(r"\b(never|always|must|only|rule|don't|do not|default|max|min|at most|at least)\b|\d", re.I)


# ---------------------------------------------------------------- terms

def stems(text):
    return [S.stem(w) for w in S.words(text)]


def skill_text(s):
    heads = " ".join(l for l in s["body"].splitlines() if l.startswith("#"))
    return " ".join([s["name"].replace("-", " "), s["description"], s["meta"].get("keywords", ""), heads])


def idf(sk):
    df = {}
    for s in sk.values():
        for t in set(stems(skill_text(s))):
            df[t] = df.get(t, 0) + 1
    n = len(sk)
    return {t: math.log((n + 1) / (c + 0.5)) for t, c in df.items()}, n


def key_terms(text, w, n, k=15):
    """The K most distinctive stems of TEXT ((1 + log frequency) x idf, so one common word repeated does not win; stems in over a fifth of all skills dropped)."""
    cnt = {}
    for t in stems(text):
        if len(t) > 2 and not t.isdigit():
            cnt[t] = cnt.get(t, 0) + 1
    floor = math.log((n + 1) / (n / 5 + 0.5))
    sc = {t: (1 + math.log(c)) * w.get(t, math.log(n + 1)) for t, c in cnt.items() if w.get(t, 99) >= floor}
    out = []
    for t, _ in sorted(sc.items(), key=lambda x: -x[1]):
        if not any(t.startswith(o) or o.startswith(t) for o in out):
            out.append(t)
    return out[:k]


def subject_terms(name, text, w, n):
    """Key terms, led by the words of the skill's own name (wiki-scout: wiki, scout), which define it however common."""
    lead = [t for t in stems(name.replace("-", " ")) if len(t) > 2 and not t.isdigit()] if name else []
    rest = [t for t in key_terms(text, w, n) if t not in lead]
    return (lead + rest)[:15] or stems(text)


def hits(terms, text):
    """The terms TEXT contains, a term also matching longer words that start with it (doc: documents)."""
    ws = set(stems(text))
    return {t for t in terms if t in ws or any(x.startswith(t) for x in ws if len(t) >= 4)}


def mentions(text, name):
    return re.search(r"(?<![\w-])" + re.escape(name) + r"(?![\w-])", text) is not None


# ---------------------------------------------------------------- step 1: wanted

def wanted_sources():
    out = [os.path.join(PROJECT, "BACKLOG.md")]
    for top in ("Proposals", "Stuff You Need Me To Do", os.path.join(".claude", "plans"), "plans"):
        for root, dirs, files in os.walk(os.path.join(PROJECT, top)):
            dirs[:] = [d for d in dirs if d not in SKIP and d != "Done"]
            out += [os.path.join(root, f) for f in files if f.endswith((".md", ".txt")) or "." not in f]
    for root, dirs, files in os.walk(PROJECT):
        dirs[:] = [d for d in dirs if d not in SKIP | SKIP_OLD and not d.startswith(".")]
        if os.path.basename(root) == "checklists":
            out += [os.path.join(root, f) for f in files if f.endswith(".md")]
    return [p for p in dict.fromkeys(out) if os.path.isfile(p) and os.path.getsize(p) < DOC_MAX]


KEBAB = r"[a-z][a-z0-9]*(?:-[a-z0-9]+)+"
WANT_RES = [re.compile(r"`(" + KEBAB + r")`"),                                   # `design-review`
            re.compile(r"\b(" + KEBAB + r")\s+skill\b(?!s)", re.I),              # design-review skill
            re.compile(r"\bskill\s+(" + KEBAB + r")\b", re.I),                   # skill design-review
            re.compile(r"((?:[A-Z][\w'-]*\s+){2,5})[Ss]kills?\b")]               # Web App Design Standards Skills


def wanted(sk):
    """{candidate: [(path, line no, text)]} for skill ideas no skill is named after."""
    names = set(sk)
    found = {}
    for p in wanted_sources():
        try:
            lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
        except OSError:
            continue
        rel = os.path.relpath(p, PROJECT)
        if rel.startswith("Proposals" + os.sep) and "." not in os.path.basename(p):   # the user's own proposal notes
            i = next((i for i, l in enumerate(lines, 1) if re.search(r"\bskills?\b", l, re.I)), 0)
            if i:
                found.setdefault("proposal: " + os.path.basename(p), []).append((rel, i, lines[i - 1].strip()))
        for i, line in enumerate(lines, 1):
            if not re.search(r"\bskills?\b", line, re.I) or re.match(r"\s*[-*] \[x\]", line, re.I):
                continue
            for rx in WANT_RES:
                for m in rx.finditer(line):
                    c = m.group(1).strip()
                    low = c.lower()
                    if (low in names or low.split()[0] in ("the", "a", "new", "this", "these", "all", "our", "every")
                            or re.search(r"\d{4}|\.\w+$", low) or len(low) < 5):
                        continue
                    if rx is WANT_RES[0] and not re.search(r"\bskill", line[max(0, m.start() - 60):m.end() + 60], re.I):
                        continue                                      # a backticked name far from "skill"
                    found.setdefault(c, []).append((os.path.relpath(p, PROJECT), i, line.strip()))
    return found


def cmd_wanted(sk, n):
    found = wanted(sk)
    if not found:
        print("no skill ideas found that lack a skill")
        return
    print(f"{len(found)} skill ideas without a skill (most mentioned first; 'near' = closest existing skill)\n")
    for c, hits in sorted(found.items(), key=lambda x: (-len(x[1]), x[0].lower()))[:n]:
        r = S.route(c, sk, 1)
        near = f"  near: {r[0][1]} ({r[0][0]})" if r else ""
        p, i, text = hits[0]
        print(f"{len(hits):2}x {c}{near}\n     {p}:{i}  {text[:110]}")
    if len(found) > n:
        print(f"\n... {len(found) - n} more (--n)")


# ---------------------------------------------------------------- step 2: scan

def doc_files(include_old):
    skip = SKIP | (set() if include_old else SKIP_OLD)
    for root, dirs, files in os.walk(PROJECT):
        dirs[:] = sorted(d for d in dirs if d not in skip and not (d.startswith(".") and d != ".claude"))
        for f in files:
            p = os.path.join(root, f)
            ryan_note = "." not in f and os.path.relpath(root, PROJECT).startswith("Proposals")
            if (f.endswith(".md") and f != "INDEX.md" or ryan_note) and os.path.getsize(p) < DOC_MAX:
                yield p


def scan_docs(terms, n, include_old):
    """[(score, path, [(line no, heading)])]: documents sharing the terms (each term weighted by how few
    documents have it), with their matching headings."""
    tset, docs = set(terms), []
    for p in doc_files(include_old):
        try:
            text = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        hit = hits(tset, text)
        if len(hit) >= max(2, len(tset) // 4):
            docs.append((p, text, hit))
    df = {t: sum(t in h for _, _, h in docs) for t in tset}
    w = {t: math.log((len(docs) + 1) / (df[t] + 0.5)) for t in tset}
    out = []
    for p, text, hit in docs:
        heads = []
        for i, line in enumerate(text.splitlines(), 1):
            if line.startswith("#"):
                h = hits(tset, line)
                if h:
                    heads.append((sum(w[t] for t in h), i, line.strip()))
        heads.sort(key=lambda x: (-x[0], x[1]))
        score = (sum(w[t] for t in hit) + sum(h for h, _, _ in heads[:3])) / (1 + max(0, math.log2(len(text) / 20000)))
        out.append((round(score), os.path.relpath(p, PROJECT), [(i, l) for _, i, l in heads[:3]]))
    out.sort(key=lambda x: -x[0])
    return out[:n]


def related_skills(name, text, sk, n):
    """[(score, skill, matched)] for the skills nearest TEXT, the skill itself left out."""
    return [r for r in S.route(text, sk, n + 1) if r[1] != name][:n]


def subject(o, sk):
    if o.name:
        if o.name not in sk:
            sys.exit(f"no skill {o.name} (before it exists, use --topic \"TEXT\")")
        return o.name, skill_text(sk[o.name])
    if not o.topic:
        sys.exit("give a skill NAME or --topic \"TEXT\"")
    return None, o.topic


def cmd_scan(o, sk):
    name, text = subject(o, sk)
    w, total = idf(sk)
    terms = subject_terms(name, text, w, total)
    print(f"terms: {', '.join(terms)}\n\nskills to read (load the sections that match, not whole skills):")
    for score, nm, hit in related_skills(name, " ".join(terms), sk, o.n):
        print(f"  {score:3}  {nm:24} {', '.join(hit[:8])}")
    print("\ndocuments (path, then the matching sections by line):")
    for score, p, heads in scan_docs(terms, o.n, o.all):
        print(f"  {score:3}  {p}")
        for i, h in heads:
            print(f"         {i:5}  {h[:90]}")
    return name, terms


# ---------------------------------------------------------------- steps 3 + 5 + 6: run

def claims(name, sk, terms, w, k=15, per=3):
    """Rule-like lines (never/always/must/numbers...) in every other skill's SKILL.md and reference files
    that use at least two of the terms, rarest terms first: where a skill could disagree with the new one."""
    tset, out = set(terms), []
    for s in sk.values():
        if s["name"] == name:
            continue
        mine = []
        for rel in ["SKILL.md"] + [f for f in s["files"] if f.endswith(".md") and f != "SKILL.md"]:
            try:
                lines = open(os.path.join(s["folder"], rel), encoding="utf-8", errors="replace").read().splitlines()
            except OSError:
                continue
            for i, line in enumerate(lines, 1):
                if line.startswith(("---", "name:", "description:", "keywords:", "#", "|---")) or not RULE.search(line):
                    continue
                h = hits(tset, line)
                if len(h) >= 2:
                    mine.append((sum(w.get(t, 1) for t in h), s["name"], rel, i, line.strip()))
        out += sorted(mine, reverse=True)[:per]
    out.sort(key=lambda x: -x[0])
    return out[:k]


def term_set(s):
    return set(stems(s["description"] + " " + s["meta"].get("keywords", "")))


def related_section(s, sk):
    m = re.search(r"^## Related skills\s*\n(.*?)(?=^#|\Z)", s["body"], re.S | re.M)
    return {o for o in sk if o != s["name"] and m and mentions(m.group(1), o)}


def proposals(name, sk, rel):
    s = sk[name]
    mine, out = term_set(s), []
    top = max([r[0] for r in rel] + [1])
    strong = [nm for score, nm, h in sorted(rel, key=lambda r: -r[0]) if score >= top / 2 and len(h) >= 2][:5]
    listed = related_section(s, sk)
    for nm in sorted(set(strong) | listed, key=lambda x: (x not in strong, x)):
        o = sk[nm]
        if nm not in listed:
            out.append(f"add {nm} to the Related skills of {name} (strong match)")
        if not mentions(o["text"], name):
            out.append(f"add {name} to the Related skills of {nm} ({os.path.relpath(o['folder'], PROJECT)}/SKILL.md)")
        theirs = term_set(o)
        j = len(mine & theirs) / max(1, len(mine | theirs))
        if j >= 0.3:
            out.append(f"overlap with {nm} ({j:.0%} of description and keyword words shared): merge them, or say in "
                       f"each which one owns what")
    crowded = []
    for t in sorted(set(stems(s["meta"].get("keywords", "")))):
        others = [o for o in sk.values() if o["name"] != name and t in set(stems(o["meta"].get("keywords", "")))]
        if len(others) >= 8:
            crowded.append(f"{t} ({len(others)})")
    if crowded:
        out.append("keywords shared with 8+ other skills (weak for routing; keep only if needed): " + ", ".join(crowded[:10]))
    routes = os.path.join(S.HERE, "..", "routes.md")
    rows = [l for l in open(routes, encoding="utf-8").read().splitlines() if l.startswith("| ")][2:]
    if not any(mentions(l, name) for l in rows):
        near = [l.split("|")[1].strip() for l in rows if any(mentions(l, nm) for _, nm, _ in rel[:3])]
        out.append(f"routes.md: {name} is in no task row" + (f"; candidates: {', '.join(near[:3])}" if near else
                                                            "; add a row if it belongs to a common task"))
    cases = json.load(open(os.path.join(S.HERE, "..", "tests", "routing.json"), encoding="utf-8"))
    if not any(name in exp for _, exp in cases):
        m = re.search(r"Use (?:when|whenever|at|for|before|after)\s+(.*)", s["description"])
        sample = (m.group(1) if m else s["description"]).rstrip(".")
        top = [r[1] for r in S.route(sample, sk, 3)]
        out.append(f"tests/routing.json: no case for {name}; e.g. [\"{sample}\", [\"{name}\"]] "
                   f"(today it routes to {', '.join(top) or 'nothing'}{'' if name in top else ': fix the keywords'})")
    for lv, msg in S.check(s, sk):
        out.append(f"skills.py check: {lv}: {msg}")
    return out


def cmd_run(o, sk):
    name = o.name
    if name not in sk:
        sys.exit(f"no skill {name}: write it first (skills.py new, write-skill), then run this")
    s = sk[name]
    text = skill_text(s)
    w, total = idf(sk)
    terms = subject_terms(name, text, w, total)
    rel = related_skills(name, " ".join(terms), sk, o.n)
    docs = scan_docs(terms, o.n, o.all)
    found = wanted(sk)
    ideas = sorted(((len(set(stems(c)) & set(terms)), c, h[0]) for c, h in found.items()), reverse=True)
    ideas = [x for x in ideas if x[0]][:5]
    linked = " ".join(x["text"] for x in sk.values())
    today = datetime.date.today().isoformat()

    L = [f"# Skill intake: {name}", "", f"Status: active ({today})", "",
         f"Made by `intake.py run {name}`. Tick each line once it is done or judged fine; an unticked line is "
         "open work. Steps follow the user's \"New Skills Documentation\" proposal.", "",
         f"Terms: {', '.join(terms)}", "", "## Step 3: do the other skills agree with it?", "",
         "Rule-like lines in other skills that use the same terms (rarest first). Read each next to the new skill; change "
         "whichever is wrong (order of truth: game > files > manual > ... > hypothesis).", ""]
    n_claim = 0
    for _, nm, f, i, line in claims(name, sk, terms, w):
        n_claim += 1
        L.append(f"- [ ] {nm} `{os.path.relpath(os.path.join(sk[nm]['folder'], f), PROJECT)}:{i}`: {line[:160]}")
    if not n_claim:
        L.append("- [x] no rule-like lines in other skills share two or more terms")
    props = proposals(name, sk, rel)
    L += ["", "## Step 5: proposals", ""] + [f"- [ ] {p}" for p in props]
    L += ["", "## Step 6: for manual review", "", "Documents on the same topic (read the sections named; link "
          "or fold in what the skill should carry):", ""]
    for score, p, heads in docs:
        tag = "" if os.path.basename(p) in linked else " (no skill names this file)"
        hs = "; ".join(f"{i}: {h[:60]}" for i, h in heads)
        L.append(f"- [ ] `{p}`{tag}" + (f" ({hs})" if hs else ""))
    if ideas:
        L += ["", "Skill ideas on the backlog that share its terms (fold in, or write next):", ""]
        L += [f"- [ ] {c} (`{p}:{i}`)" for _, c, (p, i, _) in ideas]
    L += ["", "## Finish", "", f"- [ ] `skills.py check {name}` and `skills.py index`",
          "- [ ] `tests/routetest.py` passes", "- [ ] tell the user the skill's name, its gist and what changed elsewhere", ""]
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"{today}-{name}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"{os.path.relpath(path, PROJECT)}: {n_claim} lines to compare, {len(props)} proposals, "
          f"{len(docs)} documents, {len(ideas)} backlog ideas")


def main(argv):
    if not argv:
        print(__doc__)
        return
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("wanted")
    a.add_argument("--n", type=int, default=40)
    for c in ("scan", "run"):
        a = sub.add_parser(c)
        a.add_argument("name", nargs="?" if c == "scan" else None)
        if c == "scan":
            a.add_argument("--topic")
        a.add_argument("--n", type=int, default=8)
        a.add_argument("--all", action="store_true", help="also Archive/, old summaries and repos/")
    o = ap.parse_args(argv)
    sk = S.all_skills()
    if o.cmd == "wanted":
        cmd_wanted(sk, o.n)
    elif o.cmd == "scan":
        cmd_scan(o, sk)
    else:
        cmd_run(o, sk)


if __name__ == "__main__":
    main(sys.argv[1:])
