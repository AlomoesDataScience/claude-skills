"""the user's own words from a Claude Code session, including messages he typed mid-turn.

  ryanwords.py SESSION [--since TIME] [--grep REGEX] [--chars N]

SESSION  8-char session id, or a .jsonl / .jsonl.gz path (live sessions in ~/.claude/projects/*/, archived in
         Archive/sessions/**). TIME = ISO prefix ("2026-11-17T10:50") or "HH:MM" (same day as the session's last
         line). --chars caps each message (default 600, 0 = no cap).

Why: messages the user sends while Claude is working are stored as "queue-operation" lines, not "user" lines, so a
filter on type == "user" misses them (found 2026-11-17: "You also need a skill to say ah compaction, let's
review" existed only as a queued line). This reads both, drops tool results, skill bodies, permission grants,
hook and system text, and prints one line per message: time, [q] when queued, the text. Read only.
Pure standard library.
"""
import glob, gzip, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
SKIP = ("<", "This session is being continued", "Base directory for this skill", "Permission granted",
        "(Re-invocation", "Caveat:", "[Request interrupted")


def find(sess):
    if os.path.exists(sess):
        return sess
    pats = [os.path.expanduser(f"~/.claude/projects/*/{sess}*.jsonl"),
            os.path.join(ROOT, "Archive", "sessions", "**", f"*{sess}*.jsonl.gz")]
    for p in pats:
        hits = sorted(glob.glob(p, recursive=True))
        if hits:
            return hits[-1]
    sys.exit(f"no session found for {sess!r}")


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):   # tool_result blocks are not the user's words
        return "\n".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    return ""


def words(path):
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt", encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            t, ts = d.get("type"), d.get("timestamp", "")
            if t == "user" and isinstance(d.get("message"), dict):
                yield ts, False, text_of(d["message"].get("content")).strip()
            elif t == "queue-operation" and d.get("operation") == "enqueue" and isinstance(d.get("content"), str):
                yield ts, True, d["content"].strip()


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    since, rx, cap = "", None, 600
    sess = a[0]
    i = 1
    while i < len(a):
        if a[i] == "--since" and i + 1 < len(a):
            since = a[i + 1]; i += 2
        elif a[i] == "--grep" and i + 1 < len(a):
            rx = re.compile(a[i + 1], re.I); i += 2
        elif a[i] == "--chars" and i + 1 < len(a):
            cap = int(a[i + 1]); i += 2
        else:
            sys.exit(f"unknown argument {a[i]!r}\n\n{__doc__}")
    path = find(sess)
    rows = list(words(path))
    if re.fullmatch(r"\d\d:\d\d", since) and rows:
        since = max(r[0] for r in rows)[:11] + since
    seen = set()
    print(f"# {path}")
    for ts, queued, txt in rows:
        if not txt or txt.startswith(SKIP) or ts < since:
            continue
        key = " ".join(txt.split())
        if key in seen:              # a queued message can come back later as a user line
            continue
        seen.add(key)
        if rx and not rx.search(txt):
            continue
        out = key if not cap or len(key) <= cap else key[:cap] + " ..."
        print(f"{ts[:16].replace('T', ' ')} {'[q] ' if queued else ''}{out}")


if __name__ == "__main__":
    main()
