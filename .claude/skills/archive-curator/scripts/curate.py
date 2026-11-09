#!/usr/bin/env python3
"""Archive curator: track which archived sessions have been turned into lasting knowledge, and prepare a
proposals file for each - candidate lessons with a suggested home (an existing skill via check-skills'
matcher, memory, BACKLOG) and a checkbox. Claude judges and applies; nothing is changed automatically.

  curate.py status                   every session: digest?, proposals?, curated? (ledger: Archive/sessions/CURATED.md)
  curate.py next                     the oldest session not curated yet
  curate.py propose SESSION [--n 30] write Archive/sessions/proposals/<id>.md (makes the digest if missing)
  curate.py mark SESSION "NOTE"      record SESSION as curated in the ledger, with a one-line note
Pure standard library."""
import datetime, glob, io, os, re, sys
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(SK, "chat-review", "scripts"))
sys.path.insert(0, os.path.join(SK, "check-skills", "scripts"))
import chatreview, checkskills  # noqa: E402

ARCH = chatreview.ARCH
LEDGER = os.path.join(ARCH, "CURATED.md")
PROP = os.path.join(ARCH, "proposals")
MEM_RE = re.compile(r"\b(i am|i'm a|my |i like|i prefer|i hate|i always|i never|call me)\b", re.I)
TODO_RE = re.compile(r"\b(later|todo|to do|next time|eventually|someday|backlog|remind)\b", re.I)


def curated():
    if not os.path.exists(LEDGER):
        return {}
    return {m.group(1): m.group(2) for m in re.finditer(r"^- (\w{8}) (.*)$", open(LEDGER).read(), re.M)}


def propose(sid, n):
    path = chatreview.find(sid)
    sid = sid[:8]
    if not glob.glob(os.path.join(chatreview.DIG, f"*-{sid}.md")):
        with redirect_stdout(io.StringIO()):
            chatreview.digest(path, 600)
    buf = io.StringIO()
    with redirect_stdout(buf):
        chatreview.lessons(path, n)
    rows = []
    for line in buf.getvalue().splitlines():
        ts, _, text = line.partition("  ")
        if MEM_RE.search(text):
            home = "memory (about the user)"
        elif TODO_RE.search(text):
            home = "BACKLOG.md / plan"
        else:
            hits = checkskills.rank(text, checkskills.ROOT, 2)
            home = ("skill: " + " or ".join(h[1] for h in hits)) if hits else "new skill? / memory rule"
        rows.append(f"- [ ] {ts} - \"{text.strip()[:220]}\" -> {home}")
    os.makedirs(PROP, exist_ok=True)
    dst = os.path.join(PROP, f"{sid}.md")
    dig = glob.glob(os.path.join(chatreview.DIG, f"*-{sid}.md"))
    open(dst, "w", encoding="utf-8").write(
        f"# Curation proposals - session {sid}\n\nStatus: draft ({datetime.date.today()})\n\n"
        f"Digest: {os.path.relpath(dig[0], chatreview.ROOT) if dig else '-'}\n\n"
        "Tick what was applied, strike what was rejected (~~text~~), then `curate.py mark`.\n"
        "Suggested homes come from the skill matcher - check each against the digest before acting.\n\n"
        + ("\n".join(rows) or "- no rule-like lines found; read the digest's summary") + "\n")
    print(f"{os.path.relpath(dst, chatreview.ROOT)}  {len(rows)} candidates")


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    ss, cur = chatreview.sessions(), curated()
    if a[0] == "status":
        for sid, p in sorted(ss.items(), key=lambda kv: os.path.getmtime(kv[1])):
            d = "digest" if glob.glob(os.path.join(chatreview.DIG, f"*-{sid}.md")) else "-"
            pr = "proposals" if os.path.exists(os.path.join(PROP, f"{sid}.md")) else "-"
            print(f"{sid}  {d:6}  {pr:9}  {('curated: ' + cur[sid][:60]) if sid in cur else 'open'}")
    elif a[0] == "next":
        left = [s for s, p in sorted(ss.items(), key=lambda kv: os.path.getmtime(kv[1])) if s not in cur]
        print(left[0] if left else "all curated")
    elif a[0] == "propose":
        propose(a[1], int(a[a.index("--n") + 1]) if "--n" in a else 30)
    elif a[0] == "mark":
        with open(LEDGER, "a") as f:
            if os.path.getsize(LEDGER) == 0 if os.path.exists(LEDGER) else True:
                f.write("# Curated sessions\n\nOne line per session turned into skills/memory/backlog.\n\n")
            f.write(f"- {a[1][:8]} {datetime.date.today()} {a[2] if len(a) > 2 else ''}\n")
        print("marked", a[1][:8])


if __name__ == "__main__":
    main()
