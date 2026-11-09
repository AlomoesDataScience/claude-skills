#!/usr/bin/env python3
"""Turn a Claude Code session transcript into a short readable digest, so a past chat can be reviewed without
loading its raw .jsonl (which re-sends screenshots, tool dumps and thinking).

  chatreview.py list [--n 20]                 sessions (live + archived): id, date, lines, digest?, first prompt
  chatreview.py digest SESSION [--chars 600]  write Archive/sessions/digests/<date>-<id>.md and print its path
                                              and size. SESSION = 8-char id, a .jsonl or a .jsonl.gz path
  chatreview.py lessons SESSION [--n 40]      skill-mining view: The user's rule-like lines, corrections, requests
                                              for skills, with timestamps (printed, short)
Digest layout: header (dates, counts, skills used, files written), then one block per user turn - the user's words
in full (capped), Claude's replies capped, tool calls one line each - and every compaction summary in full.
Pure standard library."""
import collections, glob, gzip, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4))   # workspace = folder holding .claude/
ARCH = os.path.join(ROOT, "Archive", "sessions")
DIG = os.path.join(ARCH, "digests")
PROJ = os.path.expanduser("~/.claude/projects")
RULE = re.compile(r"\b(always|never|don't|do not|make sure|remember|rule|from now on|i want|i'd like|should|stop|"
                  r"make a skill|save (it|that) as|wrong|no,|not what|instead)\b", re.I)


def sessions():
    """{id8: path} - live transcript wins over its archived copy."""
    out = {}
    for f in glob.glob(os.path.join(ARCH, "*", "*.jsonl.gz")):
        out[os.path.basename(f)[-17:-9]] = f
    for f in glob.glob(os.path.join(PROJ, "*", "*.jsonl")):
        out[os.path.basename(f)[:8]] = f
    return out


def find(s):
    if os.path.exists(s):
        return s
    p = sessions().get(s[:8])
    if not p:
        sys.exit(f"no session {s}")
    return p


def entries(path):
    op = gzip.open if path.endswith(".gz") else open
    for l in op(path, "rt", encoding="utf-8", errors="replace"):
        try:
            e = json.loads(l)
        except Exception:
            continue
        if e.get("type") in ("user", "assistant"):
            yield e


def clean(t):
    t = re.sub(r"<system-reminder>.*?</system-reminder>", " ", t or "", flags=re.S)
    t = re.sub(r"<(command-[a-z]+|local-command-[a-z]+)>.*?</\1>", " ", t, flags=re.S)
    return re.sub(r"[ \t]+", " ", t).strip()


def short_tool(it):
    i = it.get("input") or {}
    arg = i.get("description") or i.get("file_path") or i.get("skill") or i.get("pattern") or i.get("prompt") or \
        i.get("command") or i.get("query") or ""
    return f"`{it.get('name')}` {re.sub(chr(10), ' ', str(arg))[:110]}"


def digest(path, chars):
    sid = os.path.basename(path)[:8] if path.endswith(".jsonl") else os.path.basename(path)[-17:-9]
    blocks, skills, files, tools = [], [], [], collections.Counter()
    first = last = ""
    cur = None
    for e in entries(path):
        ts = (e.get("timestamp") or "")[:16].replace("T", " ")
        first = first or ts
        last = ts or last
        m = e.get("message") or {}
        c = m.get("content")
        if e["type"] == "user":
            if e.get("isCompactSummary"):
                blocks.append(f"\n### {ts} - compaction summary\n\n{clean(c if isinstance(c, str) else json.dumps(c))}\n")
                continue
            text = c if isinstance(c, str) else " ".join(x.get("text", "") for x in c or []
                                                          if isinstance(x, dict) and x.get("type") == "text")
            text = clean(text)
            if not text:
                continue                                # tool results: left out (that's the point)
            cur = {"ts": ts, "user": text[:1500], "out": []}
            blocks.append(cur)
        else:
            for it in c or []:
                if not isinstance(it, dict):
                    continue
                if it.get("type") == "text" and it.get("text", "").strip() and cur is not None:
                    cur["out"].append("> " + clean(it["text"])[:chars].replace("\n", "\n> "))
                elif it.get("type") == "tool_use":
                    tools[it.get("name")] += 1
                    i = it.get("input") or {}
                    if it.get("name") == "Skill" and i.get("skill") not in skills:
                        skills.append(i.get("skill"))
                    if it.get("name") in ("Write", "Edit") and i.get("file_path") not in files:
                        files.append(i.get("file_path"))
                    if cur is not None:
                        cur["out"].append("- " + short_tool(it))
    rel = lambda f: os.path.relpath(f, ROOT) if f and f.startswith(ROOT) else f
    out = [f"# Session {sid} - {first[:10]}", "", "Status: digest (raw transcript: " + rel(path) + ")", "",
           f"- Time: {first} -> {last}", f"- Tool calls: " + ", ".join(f"{k} {v}" for k, v in tools.most_common(8)),
           f"- Skills loaded: {', '.join(skills) or '-'}", f"- Files written/edited ({len(files)}): " +
           ", ".join(rel(f) for f in files[:30]), "", "## Summary (write it here when reviewing)", "", "-", "",
           "## Turns"]
    for b in blocks:
        if isinstance(b, str):
            out.append(b)
            continue
        out += ["", f"### {b['ts']} the user", "", b["user"], ""]
        tl = [x for x in b["out"] if x.startswith("- ")]
        tx = [x for x in b["out"] if x.startswith("> ")]
        if len(tl) > 12:
            tl = tl[:6] + [f"- ... {len(tl) - 12} more tool calls ..."] + tl[-6:]
        out += tl + ([""] if tl else []) + tx[-2:]
    os.makedirs(DIG, exist_ok=True)
    dst = os.path.join(DIG, f"{first[:10]}-{sid}.md")
    open(dst, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"{rel(dst)}  {os.path.getsize(dst) // 1024} KB (~{os.path.getsize(dst) // 4000}k tokens; "
          f"raw {os.path.getsize(path) // 1048576} MB)")


def lessons(path, n):
    k = 0
    for e in entries(path):
        if e["type"] != "user" or e.get("isCompactSummary"):
            continue
        c = (e.get("message") or {}).get("content")
        t = clean(c if isinstance(c, str) else " ".join(x.get("text", "") for x in c or []
                                                        if isinstance(x, dict) and x.get("type") == "text"))
        for sent in re.split(r"(?<=[.!?])\s+|\n", t):
            if 12 < len(sent) < 400 and RULE.search(sent):
                print(f"{(e.get('timestamp') or '')[:16]}  {sent.strip()}")
                k += 1
                break
        if k >= n:
            break


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    opt = lambda k, d: int(a[a.index(k) + 1]) if k in a else d
    if a[0] == "list":
        idx = {}
        if os.path.exists(os.path.join(ARCH, "INDEX.md")):
            for l in open(os.path.join(ARCH, "INDEX.md")):
                p = [x.strip() for x in l.split("|")]
                if len(p) >= 6:
                    idx[p[1]] = p[5]
        rows = sorted(sessions().items(), key=lambda kv: os.path.getmtime(kv[1]), reverse=True)[:opt("--n", 20)]
        for sid, p in rows:
            dg = glob.glob(os.path.join(DIG, f"*-{sid}.md"))
            print(f"{sid}  {'digest' if dg else '      '}  {os.path.getsize(p) // 1048576:4} MB  {idx.get(sid, '?')[:80]}")
    elif a[0] == "digest":
        digest(find(a[1]), opt("--chars", 600))
    elif a[0] == "lessons":
        lessons(find(a[1]), opt("--n", 40))


if __name__ == "__main__":
    main()
