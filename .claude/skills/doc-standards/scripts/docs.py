#!/usr/bin/env python3
"""Documentation standards checker and helpers (doc-standards skill).

  docs.py check [PATH...] [--all]    check budgets, lifecycle labels and dates; default set = memory, every
                                     SKILL.md, Proposals/, plans/, checklists/, BACKLOG.md. Prints problems
                                     (capped at 40; --all for every one) and a summary; exit 1 on errors
  docs.py label FILE STATUS          set the 'Status: ...' line under the title (draft active done
                                     superseded archived reviewed)
  docs.py adr "TITLE"                new decision record Decisions/NNNN-slug.md (context, decision, consequences)
Pure standard library."""
import datetime, glob, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4))   # workspace = folder holding .claude/
MEM = os.path.join(os.path.expanduser("~/.claude/projects"), re.sub(r"[^A-Za-z0-9]", "-", ROOT), "memory")
STATUSES = "draft active open waiting done superseded archived reviewed accepted digest".split()
LABEL_RE = re.compile(r"^(\*\*)?Status(\*\*)?:\s*\**\s*(\w+)", re.I | re.M)
B = {"skill_lines": 150, "desc_words": 40, "mem_lines": 40, "mem_line_chars": 150, "doc_lines": 400}


def default_set():
    fs = glob.glob(os.path.join(MEM, "*.md"))
    fs += [f for f in glob.glob(os.path.join(ROOT, "**", ".claude", "skills", "*", "SKILL.md"), recursive=True)
           if "/Archive/" not in f]
    fs += glob.glob(os.path.join(ROOT, "Proposals", "*.md"))
    fs += [f for f in glob.glob(os.path.join(ROOT, "**", "plans", "*.md"), recursive=True) if "/Archive/" not in f]
    fs += [f for f in glob.glob(os.path.join(ROOT, "**", "checklists", "*.md"), recursive=True) if "/Archive/" not in f]
    fs += [os.path.join(ROOT, "BACKLOG.md")]
    return [f for f in fs if os.path.isfile(f)]


def front(t):
    if not t.startswith("---"):
        return {}
    e = t.find("\n---", 3)
    return {k.strip(): v.strip().strip('"') for k, _, v in (l.partition(":") for l in t[3:e].splitlines())
            if v and not k.startswith(" ")}


def check(f):
    out = []
    t = open(f, encoding="utf-8", errors="replace").read()
    lines = t.count("\n") + 1
    name = os.path.basename(f)
    if name == "SKILL.md":
        m = front(t)
        if len(m.get("description", "").split()) > B["desc_words"]:
            out.append(("error", f"description {len(m['description'].split())} words > {B['desc_words']}"))
        if not m.get("keywords"):
            out.append(("warn", "no keywords: line"))
        if lines > B["skill_lines"]:
            out.append(("warn", f"{lines} lines > {B['skill_lines']} (skills.py split)"))
    elif f.startswith(MEM):
        if name == "MEMORY.md":
            ls = [l for l in t.splitlines() if l.strip()]
            if len(ls) > B["mem_lines"]:
                out.append(("error", f"{len(ls)} lines > {B['mem_lines']}"))
            for l in ls:
                if len(l) > B["mem_line_chars"]:
                    out.append(("warn", f"line over {B['mem_line_chars']} chars: {l[:50]}..."))
            for ref in re.findall(r"\]\(([^)]+\.md)\)", t):
                if not os.path.exists(os.path.join(MEM, ref)):
                    out.append(("error", f"points to missing {ref}"))
        else:
            m = front(t)
            for k in ("name", "description"):
                if k not in m:
                    out.append(("error", f"frontmatter has no {k}"))
            if "type:" not in t[:400]:
                out.append(("warn", "frontmatter has no type"))
            if f"({name})" not in open(os.path.join(MEM, "MEMORY.md")).read():
                out.append(("warn", "not listed in MEMORY.md"))
    else:
        if name != "BACKLOG.md":
            m = LABEL_RE.search("\n".join(t.splitlines()[:12]))
            if not m:
                out.append(("warn", "no 'Status:' lifecycle label near the top (docs.py label)"))
            elif m.group(3).lower() not in STATUSES:
                out.append(("warn", f"unknown status {m.group(3)!r}"))
        if not re.search(r"20\d\d-\d\d-\d\d", t):
            out.append(("warn", "no date anywhere (facts carry dates)"))
        if lines > B["doc_lines"]:
            out.append(("warn", f"{lines} lines > {B['doc_lines']} - split or archive old parts"))
    return out


def label(f, status):
    if status not in STATUSES:
        sys.exit(f"status must be one of {STATUSES}")
    t = open(f, encoding="utf-8").read()
    head = "\n".join(t.splitlines()[:12])
    if LABEL_RE.search(head):
        t = LABEL_RE.sub(f"Status: {status} ({datetime.date.today()})", t, count=1)
    else:
        ls = t.splitlines()
        i = next((k for k, l in enumerate(ls) if l.startswith("# ")), -1)
        ls.insert(i + 1, f"\nStatus: {status} ({datetime.date.today()})")
        t = "\n".join(ls) + "\n"
    open(f, "w", encoding="utf-8").write(t)
    print(f"{f}: {status}")


def adr(title):
    d = os.path.join(ROOT, "Decisions")
    os.makedirs(d, exist_ok=True)
    n = len(glob.glob(os.path.join(d, "[0-9][0-9][0-9][0-9]-*.md"))) + 1
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:50]
    p = os.path.join(d, f"{n:04d}-{slug}.md")
    open(p, "w").write(f"# {n:04d} {title}\n\nStatus: accepted ({datetime.date.today()})\n\n## Context\n- \n\n"
                       "## Decision\n- \n\n## Consequences\n- \n\n## Sources\n- (the user's words, files, dates)\n")
    print(p)


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    if a[0] == "check":
        paths = [p for p in a[1:] if not p.startswith("--")] or default_set()
        errs = warns = shown = 0
        for f in sorted(paths):
            for lvl, msg in check(os.path.abspath(f)):
                errs += lvl == "error"
                warns += lvl == "warn"
                if shown < 40 or "--all" in a:
                    shown += 1
                    print(f"{lvl:5}  {os.path.relpath(f, ROOT) if f.startswith(ROOT) else f.replace(MEM, 'memory')}: {msg}")
        print(f"checked {len(paths)} files: {errs} errors, {warns} warnings")
        sys.exit(1 if errs else 0)
    elif a[0] == "label":
        label(a[1], a[2])
    elif a[0] == "adr":
        adr(a[1])


if __name__ == "__main__":
    main()
