#!/usr/bin/env python3
"""Checklist documents for work that is PARKED until something happens (the game is free, the user gives the
go, a file arrives) - the waiting-checklist skill. Files only: nothing here touches a game or a screen.

  checklist.py new "Title" --dir FOLDER --waits-on "what must happen first" [--go "who says go"] [--plan PATH]
        writes FOLDER/checklists/<slug>.md from the template (gate, safety, items, after, log) - fill it in
  checklist.py list [--all]       every checklist in the workspace: status, open items, what it waits on
                                  (default: not done ones) - run at session start next to BACKLOG.md
  checklist.py show PATH|SLUG     print one
  checklist.py status PATH|SLUG waiting|ready|in-progress|done     set the Status line (and log it, dated)

A checklist's header lines are read by `list`: "Status:", "Waits on:", "Go from:". Items are "- [ ]".
"""
import datetime
import os
import re
import sys

a = sys.argv[1:]
TODAY = datetime.date.today().isoformat()
STATES = ("waiting", "ready", "in-progress", "done")


def opt(name, default=None):
    return a[a.index(name) + 1] if name in a else default


def root():
    d = os.path.abspath(os.getcwd())
    while d != "/":
        if os.path.exists(os.path.join(d, "BACKLOG.md")):
            return d
        d = os.path.dirname(d)
    return os.path.expanduser("~/Desktop/AI Development")


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


TEMPLATE = """# {title} - waiting checklist

Status: waiting
Waits on: {waits}
Go from: {go}
Created: {today}{plan}

## Gate - all true before starting (check each, don't assume)
- [ ] {waits}
- [ ] Go given for THIS session ({go}), in words, not inferred
- [ ] The tools named below still exist and their docstrings were re-read (never run game scripts bare)

## Safety for this session
- (the rules that apply: what must not be changed, what needs a separate go, what to never press)

## Items (each: steps -> done when -> results go to)
- [ ] 1. ...
      Steps:
      Done when:
      Results go to:

## After
- [ ] Hand back (unlock / screen readable / say so)
- [ ] Results written where each item says; skills updated; the source plan ticked
- [ ] Status: done (`checklist.py status ... done`), BACKLOG.md line ticked, memory updated if it changed

## Log
- {today}: created.
"""


def find(q):
    if os.path.isfile(q):
        return q
    for p in all_lists():
        if os.path.basename(p)[:-3] == q:
            return p
    sys.exit(f"no checklist {q!r} - checklist.py list --all")


def all_lists():
    out = []
    for d, ds, fs in os.walk(root()):
        ds[:] = [x for x in ds if x not in (".git", "node_modules", "__pycache__", "retired")]
        if os.path.basename(d) == "checklists":
            out += [os.path.join(d, f) for f in fs if f.endswith(".md")]
    return sorted(out)


def header(p):
    t = open(p, encoding="utf-8").read()
    g = lambda k: (re.search(rf"^{k}:\s*(.*)$", t, re.M) or [None, "?"])[1].strip()
    return g("Status"), g("Waits on"), g("Go from"), len(re.findall(r"^\s*- \[ \]", t, re.M)), t


def main():
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    c = a[0]
    if c == "new" and len(a) > 1 and opt("--dir") and opt("--waits-on"):
        d = os.path.join(opt("--dir"), "checklists")
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, slug(a[1]) + ".md")
        if os.path.exists(p):
            sys.exit(f"{p} exists - edit it instead")
        plan = f"\nSource plan: {opt('--plan')}" if opt("--plan") else ""
        open(p, "w", encoding="utf-8").write(TEMPLATE.format(title=a[1], waits=opt("--waits-on"),
                                                              go=opt("--go", "the user"), today=TODAY, plan=plan))
        print(p)
    elif c == "list":
        r = root()
        rows = [(p,) + header(p)[:4] for p in all_lists()]
        rows = [x for x in rows if "--all" in a or x[1] != "done"]
        for p, st, waits, go, n in rows:
            print(f"{st:12} {n:3} open  {os.path.relpath(p, r)}\n{'':18}waits on: {waits} (go: {go})")
        print(f"{len(rows)} checklists" + ("" if "--all" in a else " not done"))
    elif c == "show" and len(a) > 1:
        print(open(find(a[1]), encoding="utf-8").read())
    elif c == "status" and len(a) > 2 and a[2] in STATES:
        p = find(a[1])
        t = open(p, encoding="utf-8").read()
        t = re.sub(r"^Status:.*$", f"Status: {a[2]}", t, count=1, flags=re.M)
        t = t.rstrip("\n") + f"\n- {TODAY}: status -> {a[2]}.\n"
        open(p, "w", encoding="utf-8").write(t)
        print(p, "->", a[2])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
