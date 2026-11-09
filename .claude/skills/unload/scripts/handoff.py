#!/usr/bin/env python3
"""Unload context safely: hand-off file, archive index, recall.

  handoff.py draft [--session JSONL]   print a HANDOFF.md skeleton with what this session loaded and touched
                                       (skills, files edited/written, since the last compaction) - Claude fills
                                       it in and writes it to .claude/handoff/HANDOFF.md
  handoff.py show                      print the current hand-off (short)
  handoff.py done                      move the hand-off to Archive/sessions/handoffs/ (task finished)
  handoff.py precompact | sessionend   PreCompact / SessionEnd hook (JSON on stdin): copy the transcript gzip'd
                                       to Archive/sessions/YYYY-MM/ (Claude Code deletes transcripts after
                                       cleanupPeriodDays) and append one line to Archive/sessions/INDEX.md
  handoff.py archive-all               archive every transcript now (backfill; same as the hooks)
  handoff.py recall WORD [WORD...] [--n 12] [--chars 240]
                                       search every transcript for lines with all the words; print short
                                       snippets (date, session, role) - old context without loading it
Pure standard library."""
import datetime, glob, gzip, json, os, re, shutil, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4))   # workspace = folder holding .claude/
HO = os.path.join(ROOT, ".claude", "handoff", "HANDOFF.md")
ARCH = os.path.join(ROOT, "Archive", "sessions")
PROJ = os.path.expanduser("~/.claude/projects")


def latest_jsonl():
    fs = glob.glob(os.path.join(PROJ, "*", "*.jsonl"))
    return max(fs, key=os.path.getmtime) if fs else None


def since_compaction(path):
    lines = open(path, encoding="utf-8", errors="replace").readlines()
    start = 0
    for i, l in enumerate(lines):
        if '"isCompactSummary": true' in l or '"isCompactSummary":true' in l:
            start = i
    return lines[start:]


def draft(path):
    skills, files = [], []
    for l in since_compaction(path):
        try:
            e = json.loads(l)
        except Exception:
            continue
        for it in (e.get("message") or {}).get("content") or []:
            if isinstance(it, dict) and it.get("type") == "tool_use":
                inp = it.get("input") or {}
                if it.get("name") == "Skill" and inp.get("skill") not in skills:
                    skills.append(inp.get("skill"))
                if it.get("name") in ("Edit", "Write") and inp.get("file_path") not in files:
                    files.append(inp.get("file_path"))
    rel = lambda f: os.path.relpath(f, ROOT) if f and f.startswith(ROOT) else f
    print(f"""# Hand-off - {datetime.date.today()}  (session {os.path.basename(path)[:8]})

## Task (the user's words)
- 

## State - done / in progress / not started
- 

## Next steps (in order)
1. 

## Read first (files, sections - not whole folders)
- 

## Rules in force for this task
- 

## Skills used (reload only what the next step needs)
{chr(10).join('- ' + s for s in skills) or '- (none via the Skill tool)'}

## Files changed this stretch
{chr(10).join('- ' + rel(f) for f in files[-25:]) or '- none'}
""")


def topic(path):
    """first real user prompt of a transcript, short - the INDEX line's 'what was this session about'."""
    try:
        for l in open(path, encoding="utf-8", errors="replace"):
            if '"type":"user"' not in l.replace(" ", ""):
                continue
            e = json.loads(l)
            c = (e.get("message") or {}).get("content")
            t = c if isinstance(c, str) else " ".join(it.get("text", "") for it in c or [] if isinstance(it, dict)
                                                      and it.get("type") == "text")
            t = re.sub(r"<[^>]+>[^<]*</[^>]+>|<[^>]+>", " ", t or "")
            t = re.sub(r"\s+", " ", t).strip()
            if len(t) > 15 and not t.startswith(("Caveat", "[Request interrupted")):
                return t[:110]
    except Exception:
        pass
    return "?"


def archive(t, event, sid=None, cwd=None, trigger=""):
    """copy transcript T (gzip) into Archive/sessions/YYYY-MM/<date>-<session8>.jsonl.gz - one file per session,
    refreshed at every compaction and at session end, screenshots stripped - and append an INDEX.md line."""
    if not t or not os.path.exists(t):
        return None
    sid = (sid or os.path.basename(t).split(".")[0])[:8]
    old = glob.glob(os.path.join(ARCH, "*", f"*-{sid}.jsonl.gz"))
    if old:
        dst = old[0]
    else:
        day = datetime.datetime.fromtimestamp(os.path.getmtime(t))
        try:                                       # date of the session's first timestamped line
            for l in open(t, encoding="utf-8", errors="replace"):
                m = re.search(r'"timestamp":\s*"(\d{4}-\d\d-\d\d)', l)
                if m:
                    day = datetime.datetime.strptime(m.group(1), "%Y-%m-%d")
                    break
        except Exception:
            pass
        dst = os.path.join(ARCH, f"{day:%Y-%m}", f"{day:%Y-%m-%d}-{sid}.jsonl.gz")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    tmp = dst + ".part"
    img = re.compile(rb'"data":\s*"[A-Za-z0-9+/=]{500,}"')   # screenshots (base64) - useless for recall
    with open(t, "rb") as fi, gzip.open(tmp, "wb", compresslevel=6) as fo:
        for l in fi:
            fo.write(img.sub(b'"data":"<image stripped by archive>"', l) if b'"data"' in l else l)
    os.replace(tmp, dst)
    n = sum(1 for _ in open(t, errors="replace"))
    proj = os.path.basename(os.path.dirname(t)).replace(re.sub(r"[^A-Za-z0-9]", "-", os.path.dirname(ROOT) + "/"), "")
    with open(os.path.join(ARCH, "INDEX.md"), "a") as f:
        f.write(f"- {datetime.datetime.now():%Y-%m-%d %H:%M} {event}{(' ' + trigger) if trigger else ''} | {sid} | "
                f"{proj} | {n} lines | {os.path.relpath(dst, ARCH)} | {topic(t)}\n")
    return dst


def hook(event):
    try:
        d = json.load(sys.stdin)
    except Exception:
        d = {}
    archive(d.get("transcript_path", ""), event, d.get("session_id"), d.get("cwd"), d.get("trigger", "") or d.get("reason", ""))


def archive_all():
    for t in sorted(glob.glob(os.path.join(PROJ, "*", "*.jsonl")), key=os.path.getmtime):
        print(archive(t, "backfill"))


def archived_only():
    """archived transcripts whose original Claude Code has already deleted."""
    live = {os.path.basename(f)[:8] for f in glob.glob(os.path.join(PROJ, "*", "*.jsonl"))}
    return [f for f in glob.glob(os.path.join(ARCH, "*", "*.jsonl.gz")) if f[-17:-9] not in live]


def recall(words, n, chars):
    words = [w.lower() for w in words]
    hits, seen = [], set()
    files = sorted(glob.glob(os.path.join(PROJ, "*", "*.jsonl")), key=os.path.getmtime, reverse=True)
    for f in files + sorted(archived_only(), reverse=True):
        opener = gzip.open if f.endswith(".gz") else open
        for l in opener(f, "rt", encoding="utf-8", errors="replace"):
            low = l.lower()
            if not all(w in low for w in words):
                continue
            try:
                e = json.loads(l)
            except Exception:
                continue
            if e.get("type") not in ("user", "assistant"):
                continue                               # skip internal copies (api-request-blob, snapshots)
            c = (e.get("message") or {}).get("content")
            texts = [c] if isinstance(c, str) else [it.get("text") or it.get("thinking") or json.dumps(it.get("input", ""))
                                                     for it in c or [] if isinstance(it, dict)]
            for t in texts:
                if t and all(w in t.lower() for w in words):
                    i = t.lower().index(words[0])
                    snip = re.sub(r"\s+", " ", t[max(0, i - chars // 3): i + chars])
                    if snip in seen:
                        break
                    seen.add(snip)
                    hits.append(f"{(e.get('timestamp') or '')[:16]} {os.path.basename(f)[:8]} {e.get('type', '?'):9} {snip}")
                    break
            if len(hits) >= n:
                break
        if len(hits) >= n:
            break
    print("\n".join(hits) or "no matches")


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    if a[0] == "draft":
        p = a[a.index("--session") + 1] if "--session" in a else latest_jsonl()
        draft(p)
    elif a[0] == "show":
        print(open(HO).read() if os.path.exists(HO) else "no hand-off")
    elif a[0] == "done":
        if os.path.exists(HO):
            d = os.path.join(ARCH, "handoffs"); os.makedirs(d, exist_ok=True)
            shutil.move(HO, os.path.join(d, f"{datetime.datetime.now():%Y-%m-%d-%H%M}-HANDOFF.md")); print("archived")
    elif a[0] in ("precompact", "sessionend"):
        try:
            hook(a[0])
        except Exception:
            pass                                   # a hook must never break the session
    elif a[0] == "archive-all":
        archive_all()
    elif a[0] == "recall":
        n = int(a[a.index("--n") + 1]) if "--n" in a else 12
        ch = int(a[a.index("--chars") + 1]) if "--chars" in a else 240
        ws = [w for i, w in enumerate(a[1:], 1) if not w.startswith("--") and a[i - 1] not in ("--n", "--chars")]
        recall(ws, n, ch)


if __name__ == "__main__":
    main()
