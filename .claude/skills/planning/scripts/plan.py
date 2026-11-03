#!/usr/bin/env python3
"""Plans as files: plan.py new "Title" [--dir FOLDER] | list [--all] | show PATH|SLUG
Plans live in <folder of the work>/plans/<slug>.md (default folder: the current directory)."""
import datetime
import os
import re
import sys

ROOT = os.path.expanduser("~/Desktop/AI Development")
TEMPLATE = """# Plan: {title}
Status: open    Created: {date}    Owner: Claude (the user reviews)

## Goal
(what done looks like - checkable)

## Context
(facts, rules, constraints, the user's instructions)

## Steps
- [ ] 1. ... -> check: ...
- [ ] 2. ... -> check: ...

## Decisions
- ...

## Risks / watch for
- ...

## References - re-read this plan when
- starting a session or after a context summary
- before each step / before decisions this plan covers
- something goes off-plan
- The user asks what's next

## Status / changes log
- {date}: plan made.
"""


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:60]


def plans():
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if not x.startswith(".") or x == ".claude"]
        dirs[:] = [x for x in dirs if x not in ("node_modules", "repos", "illwiki", "sources")]
        if os.path.basename(d) == "plans":
            for f in files:
                if f.endswith(".md"):
                    yield os.path.join(d, f)


def status(p):
    m = re.search(r"^Status:\s*(\S+)", open(p, errors="replace").read(), re.M)
    return m.group(1) if m else "?"


def main(a):
    if not a or a[0] not in ("new", "list", "show"):
        print(__doc__)
        return
    if a[0] == "new":
        title = a[1]
        d = a[a.index("--dir") + 1] if "--dir" in a else os.getcwd()
        os.makedirs(os.path.join(d, "plans"), exist_ok=True)
        p = os.path.join(d, "plans", slug(title) + ".md")
        if os.path.exists(p):
            sys.exit(f"exists: {p}")
        open(p, "w").write(TEMPLATE.format(title=title, date=datetime.date.today()))
        print(p)
    elif a[0] == "list":
        ps = sorted(plans(), key=os.path.getmtime, reverse=True)
        for p in ps:
            s = status(p)
            if "--all" in a or s.lower() != "done":
                print(f"{s:8s} {datetime.date.fromtimestamp(os.path.getmtime(p))}  {os.path.relpath(p, ROOT)}")
    else:
        t = a[1]
        p = t if os.path.exists(t) else next((x for x in plans() if os.path.basename(x) == slug(t) + ".md"), None)
        print(open(p).read() if p else f"no plan {t}")


if __name__ == "__main__":
    main(sys.argv[1:])
