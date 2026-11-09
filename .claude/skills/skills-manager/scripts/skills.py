"""Manage Claude's skills in this project: what there is, which ones a task needs (and in what
order), checking them, making new ones, importing, and unloading/loading them.

  python3 -I skills.py list [--all]              every skill: name, size, scripts, uses (--all: also
                                                 user-level ~/.claude/skills and disabled ones)
  python3 -I skills.py route "TASK TEXT" [--n 5] which skills fit a task, best first, each with the
                                                 skills it builds on (load those too, first)
  python3 -I skills.py show NAME                 one skill: description, files, scripts, uses, used by
  python3 -I skills.py deps [NAME]               the dependency graph (who builds on whom)
  python3 -I skills.py check [NAME]              lint: frontmatter, name = folder, description length,
                                                 links to missing skills/files, scripts that do not compile
  python3 -I skills.py new NAME "DESCRIPTION" [--uses a,b] [--script FILE.py] [--dir FOLDER]
                                                 make a new skill folder in the house style (--dir: in
                                                 a game or genre folder, e.g. "Games/Wargames/Hex of Steel")
  python3 -I skills.py import PATH [--name NAME] [--force]
                                                 add a skill from a folder, a SKILL.md or a .zip
  python3 -I skills.py disable NAME              unload: move it to .claude/skills-disabled/ (its
                                                 description no longer takes context in new sessions)
  python3 -I skills.py enable NAME               load it again
  python3 -I skills.py split NAME [--budget 140] [--dry]   move big sections to reference/*.md
  python3 -I skills.py index                     rewrite .claude/skills/INDEX.md (the catalogue) and
                                                 each game folder's own .claude/skills/INDEX.md

Skills live in a hierarchy: generic ones in the project root's .claude/skills, genre and game ones
in that folder's own .claude/skills (e.g. "Games/Fantasy Strategy/Dominions 6/.claude/skills/<prefix>-guide").
Claude Code loads the root ones at startup and a folder's ones the first time Claude reads or edits
a file in that folder (or right away with /add-dir FOLDER, or when the session starts there).

Claude Code reads every skill's name and description at the start of a session and loads the
body only when the skill is used; a new or re-enabled skill shows up in the next session (or when
the skills list is refreshed). Pure standard library.
"""
import argparse
import os
import py_compile
import re
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.path.dirname(os.path.dirname(HERE))                      # .claude/skills
CLAUDE = os.path.dirname(SKILLS)                                     # .claude
PROJECT = os.path.dirname(CLAUDE)                                    # the project root
NEST_DEPTH = 5                                                       # genre/game/sub folders searched
DISABLED = os.path.join(CLAUDE, "skills-disabled")
USER = os.path.expanduser("~/.claude/skills")
DESC_MAX = 1024
DESC_WORDS = 40      # budget (doc-standards, 2026-11-09): the listing is re-sent nearly every turn
BODY_LINES = 150     # budget: SKILL.md over this -> split detail into reference/ files
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
STOP = set("""a an the and or of to in on for with by from at as is are be it its this that these those
when whenever use used uses using user users asks ask wants want claude skill skills any all
each every new into out not no only also can how what which who does do make makes made""".split())


# ---------------------------------------------------------------- reading skills

def frontmatter(text):
    """({key: value}, body) of a SKILL.md (simple YAML: one `key: value` per line)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    meta = {}
    for line in text[3:end].strip().splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, text[end + 4:].lstrip("\n")


def load(folder, where="project"):
    p = os.path.join(folder, "SKILL.md")
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as f:
        text = f.read()
    meta, body = frontmatter(text)
    files, scripts, size = [], [], 0
    for root, dirs, names in os.walk(folder):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for n in names:
            fp = os.path.join(root, n)
            rel = os.path.relpath(fp, folder)
            size += os.path.getsize(fp)
            files.append(rel)
            if rel.startswith("scripts" + os.sep) and n.endswith((".py", ".sh", ".js")):
                scripts.append(rel)
    return {"name": meta.get("name", os.path.basename(folder)), "folder": folder, "where": where,
            "meta": meta, "description": meta.get("description", ""), "body": body, "text": text,
            "files": sorted(files), "scripts": sorted(scripts), "size": size,
            "lines": text.count("\n") + 1}


def nested_bases():
    """(skills dir, folder) for every .claude/skills below the project root (game and genre folders)."""
    out = []
    for root, dirs, _ in os.walk(PROJECT):
        depth = os.path.relpath(root, PROJECT).count(os.sep) + (root != PROJECT)
        if root != PROJECT and os.path.isdir(os.path.join(root, ".claude", "skills")):
            out.append((os.path.join(root, ".claude", "skills"), os.path.relpath(root, PROJECT)))
        dirs[:] = [] if depth >= NEST_DEPTH else sorted(d for d in dirs if not d.startswith(".") and d != "__pycache__")
    return out


def all_skills(include_user=False, include_disabled=False):
    out = {}
    places = [(SKILLS, "project")] + nested_bases()
    if include_disabled:
        places.append((DISABLED, "disabled"))
        places += [(os.path.join(os.path.dirname(b), "skills-disabled"), f"disabled, {w}") for b, w in nested_bases()]
    if include_user and os.path.abspath(USER) != os.path.abspath(SKILLS):
        places.append((USER, "user"))
    for base, where in places:
        if not os.path.isdir(base):
            continue
        for d in sorted(os.listdir(base)):
            s = load(os.path.join(base, d), where)
            if s and s["name"] not in out:
                out[s["name"]] = s
    for s in out.values():
        s["uses"] = uses(s, out)
    for s in out.values():
        s["used_by"] = sorted(o["name"] for o in out.values() if s["name"] in o["uses"])
        s["related"] = related(s, out)
    return out


def uses(s, skills):
    """Skills this one needs loaded first: its scripts reach into their folders (a quoted
    skill name: sys.path entries, data paths), or its description says it uses them."""
    code = ""
    for sc in s["scripts"]:
        try:
            with open(os.path.join(s["folder"], sc), encoding="utf-8", errors="replace") as f:
                code += "\n" + f.read()
        except OSError:
            pass
    desc_uses = " ".join(re.findall(r"\b(?:Uses|Builds on|Needs)\b[^.]*", s["description"])
                         + re.findall(r"\bBuilds on\b[^.\n]*", s["body"]))
    out = set()
    for other in skills:
        if other == s["name"]:
            continue
        pat = re.escape(other) + r"(?![\w-])"
        if re.search(r"[\"'/]" + pat + r"[\"'/]", code) or re.search(r"(?<![\w-])" + pat, desc_uses):
            out.add(other)
    return sorted(out)


def related(s, skills):
    """Other skills its SKILL.md mentions (see-also links; not needed to use it)."""
    return sorted(o for o in skills if o != s["name"] and o not in s["uses"]
                  and re.search(r"(?<![\w-])" + re.escape(o) + r"(?![\w-])", s["text"]))


# ---------------------------------------------------------------- routing a task to skills

def words(text):
    return [w for w in re.findall(r"[a-z0-9][a-z0-9'+-]*", text.lower()) if w not in STOP and len(w) > 1]


def stem(w):
    for suf in ("ing", "ers", "ies", "es", "ed", "er", "s"):
        if len(w) > len(suf) + 3 and w.endswith(suf):
            return w[: -len(suf)]
    return w


def route(task, skills, n=5):
    """Skills ranked for TASK: words of the task found in the description (weight 3), in the
    name (4) and in the body's headings (1), summed over distinct stems."""
    tw = {stem(w) for w in words(task)}
    scored = []
    for s in skills.values():
        desc = {stem(w) for w in words(s["description"] + " " + s["meta"].get("keywords", ""))}
        name = {stem(w) for w in words(s["name"].replace("-", " "))}
        heads = {stem(w) for line in s["body"].splitlines() if line.startswith("#") for w in words(line)}
        hits = {w: 3 * (w in desc) + 4 * (w in name) + 1 * (w in heads) for w in tw}
        score = sum(hits.values())
        if score:
            scored.append((score, s["name"], sorted(w for w, v in hits.items() if v)))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return scored[:n]


def load_order(name, skills, seen=None):
    """NAME's dependencies first (depth first), then NAME."""
    seen = [] if seen is None else seen
    for d in skills[name]["uses"]:
        if d not in seen and d in skills:
            seen.append(d)                                  # cycles: mark before descending
            load_order(d, skills, seen)
            seen.remove(d)
            seen.append(d)
    if name not in seen:
        seen.append(name)
    return seen


# ---------------------------------------------------------------- checking

def check(s, skills):
    """[(level, message)] problems with a skill."""
    out = []
    m = s["meta"]
    folder = os.path.basename(s["folder"])
    if not s["text"].startswith("---"):
        out.append(("error", "SKILL.md has no frontmatter (--- name/description ---)"))
    if "name" not in m:
        out.append(("error", "no name in the frontmatter"))
    elif m["name"] != folder:
        out.append(("error", f"name {m['name']!r} differs from the folder {folder!r}"))
    elif not NAME_RE.match(m["name"]):
        out.append(("error", f"name {m['name']!r}: use lowercase letters, digits and hyphens, max 64"))
    d = m.get("description", "")
    if not d:
        out.append(("error", "no description (Claude cannot tell when to use the skill)"))
    elif len(d) > DESC_MAX:
        out.append(("error", f"description is {len(d)} characters (max {DESC_MAX})"))
    elif not re.search(r"\bUse (when|whenever|at|for|in|before|after|to)\b", d, re.I):
        out.append(("warn", "description does not say when to use it ('Use when ...')"))
    if d and len(d.split()) > DESC_WORDS:
        out.append(("warn", f"description is {len(d.split())} words (budget {DESC_WORDS}); move trigger words to keywords:"))
    if not m.get("keywords"):
        out.append(("warn", "no keywords: line (routing words for check-skills and INDEX.md)"))
    if s["lines"] > BODY_LINES:
        out.append(("warn", f"SKILL.md is {s['lines']} lines (budget {BODY_LINES}); move detail into reference/ files it links"))
    for ref in sorted(set(re.findall(r"`((?:scripts|examples|templates|tests|reference)/[\w./-]+)`", s["body"]))):
        if "*" in ref or "<" in ref:
            continue
        if not os.path.exists(os.path.join(s["folder"], ref)) and \
                not any(os.path.exists(os.path.join(o["folder"], ref)) for o in skills.values()):
            out.append(("warn", f"refers to {ref}, which is in no skill folder"))
    for ref in sorted(set(re.findall(r"\b(dom6-[a-z-]+|[a-z]+-[a-z]+-?[a-z]*)\b skill", s["body"]))):
        if ref not in skills and ref.startswith("dom6-"):
            out.append(("warn", f"mentions the {ref} skill, which does not exist"))
    for sc in s["scripts"]:
        if sc.endswith(".py"):
            with tempfile.TemporaryDirectory() as tmp:
                try:
                    py_compile.compile(os.path.join(s["folder"], sc), cfile=os.path.join(tmp, "x.pyc"),
                                       doraise=True)
                except py_compile.PyCompileError as e:
                    out.append(("error", f"{sc} does not compile: {e.msg.strip().splitlines()[-1]}"))
    return out


# ---------------------------------------------------------------- making, importing, (un)loading

TEMPLATE = """---
name: {name}
description: {description}
keywords: {keywords}
---

# {title}

What this skill does in two or three sentences, and what it does not do.

## Files

{files}
Run Python with `python3 -I` (system Python with PIL only; no pip).

## Workflow

1. ...
2. ...
3. Report what was done, where it is, and what is untested.

## Facts and gotchas

- ...
"""


def new(name, description, uses_=(), script=None, where=None):
    if not NAME_RE.match(name):
        sys.exit(f"bad name {name!r}: lowercase letters, digits and hyphens")
    base = os.path.join(PROJECT, where, ".claude", "skills") if where else SKILLS
    if where and not os.path.isdir(os.path.join(PROJECT, where)):
        sys.exit(f"no folder {where!r} in the project")
    folder = os.path.join(base, name)
    if name in all_skills(include_disabled=True) or os.path.exists(folder):
        sys.exit(f"{name} exists already")
    if len(description) > DESC_MAX:
        sys.exit(f"description is {len(description)} characters (max {DESC_MAX})")
    files = ""
    if script:
        files += f"- `scripts/{script}` - ...\n"
    for u in uses_:
        files += f"- Builds on the **{u}** skill.\n"
    os.makedirs(folder)
    with open(os.path.join(folder, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(TEMPLATE.format(name=name, description=description, keywords="",
                                title=name.replace("-", " ").capitalize(), files=files or "- ...\n"))
    if script:
        os.makedirs(os.path.join(folder, "scripts"))
        with open(os.path.join(folder, "scripts", script), "w", encoding="utf-8") as f:
            f.write(f'"""{description.split(". ")[0]}."""\nimport sys\n\n\ndef main(argv):\n'
                    f'    pass\n\n\nif __name__ == "__main__":\n    main(sys.argv[1:])\n')
    return folder


def import_skill(path, name=None, force=False):
    """Copy a skill in from a folder (with SKILL.md), a lone SKILL.md, or a .zip of either.
    The files are copied, not run; read the SKILL.md and scripts before using the skill."""
    tmp = None
    try:
        if path.endswith(".zip"):
            tmp = tempfile.mkdtemp()
            with zipfile.ZipFile(path) as z:
                for info in z.infolist():                    # no paths out of the folder
                    target = os.path.realpath(os.path.join(tmp, info.filename))
                    if not target.startswith(os.path.realpath(tmp) + os.sep):
                        sys.exit(f"refusing {info.filename!r}: it points outside the archive")
                z.extractall(tmp)
            found = [r for r, _, fs in os.walk(tmp) if "SKILL.md" in fs]
            if len(found) != 1:
                sys.exit(f"the archive holds {len(found)} SKILL.md files; expected 1")
            src = found[0]
        elif os.path.isdir(path):
            src = path
        elif os.path.basename(path) == "SKILL.md" or path.endswith(".md"):
            tmp = tempfile.mkdtemp()
            src = os.path.join(tmp, "skill")
            os.makedirs(src)
            shutil.copy(path, os.path.join(src, "SKILL.md"))
        else:
            sys.exit("give a skill folder, a SKILL.md or a .zip")
        if not os.path.isfile(os.path.join(src, "SKILL.md")):
            sys.exit(f"no SKILL.md in {src}")
        with open(os.path.join(src, "SKILL.md"), encoding="utf-8") as f:
            meta, _ = frontmatter(f.read())
        name = name or meta.get("name") or os.path.basename(os.path.normpath(src))
        if not NAME_RE.match(name):
            sys.exit(f"bad name {name!r}; pass --name")
        dest = os.path.join(SKILLS, name)
        if os.path.exists(dest):
            if not force:
                sys.exit(f"{name} exists already (--force replaces it)")
            shutil.rmtree(dest)
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"))
        if meta.get("name") != name:                         # make the frontmatter name match
            p = os.path.join(dest, "SKILL.md")
            with open(p, encoding="utf-8") as f:
                text = f.read()
            if text.startswith("---") and re.search(r"^name:.*$", text, re.M):
                text = re.sub(r"^name:.*$", f"name: {name}", text, count=1, flags=re.M)
            elif text.startswith("---"):
                text = "---\nname: " + name + "\n" + text[4:]
            else:
                text = f"---\nname: {name}\ndescription: \n---\n\n" + text
            with open(p, "w", encoding="utf-8") as f:
                f.write(text)
        return dest
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


def move(name, to_disabled):
    src_base, dst_base = (SKILLS, DISABLED) if to_disabled else (DISABLED, SKILLS)
    for b, _ in nested_bases():                      # a game folder's skill moves inside that folder
        d = os.path.join(os.path.dirname(b), "skills-disabled")
        if os.path.isdir(os.path.join(b if to_disabled else d, name)):
            src_base, dst_base = (b, d) if to_disabled else (d, b)
    src, dst = os.path.join(src_base, name), os.path.join(dst_base, name)
    if not os.path.isdir(src):
        sys.exit(f"{name} is not in {src_base}")
    if os.path.exists(dst):
        sys.exit(f"{dst} exists already")
    if name == "skills-manager" and to_disabled:
        sys.exit("the skills manager stays loaded (it is how skills are loaded again)")
    os.makedirs(dst_base, exist_ok=True)
    shutil.move(src, dst)
    return dst


def _lines(rows):
    """one line per skill: name - short description (first sentence) - keywords."""
    out = []
    for s in sorted(rows, key=lambda s: s["name"]):
        d = s["description"].split(". Use when")[0].split(". Use whenever")[0].rstrip(".")
        d = d if len(d) <= 160 else d[:157].rsplit(" ", 1)[0] + "..."
        k = s["meta"].get("keywords", "")
        k = k if len(k) <= 120 else k[:117].rsplit(",", 1)[0] + ", ..."
        out.append(f"- **{s['name']}** - {d}" + (f" _[{k}]_" if k else ""))
    return out


def write_index(skills):
    """INDEX.md = the routing index (the user, 2026-11-09: "an index file to call the proper skills after the
    skills refactor"). Routes table (hand-edited in skills-manager/routes.md) on top, then one line per skill
    by folder. Each game folder also gets its own short INDEX.md. Returns the root index path."""
    places = {}
    for s in skills.values():
        places.setdefault(s["where"], []).append(s)
    head = ["Generated by `skills-manager/scripts/skills.py index` from each SKILL.md (description + keywords:)",
            "and `skills-manager/routes.md`; edit those, not this file.", ""]
    routes = open(os.path.join(HERE, "..", "routes.md"), encoding="utf-8").read().strip()
    lines = ["# Skill index", ""] + head + [
        "How to use: find the task in Routes, load only what the current step needs (Skill tool; game skills",
        "outside the session list: Read their SKILL.md), read one section rather than a whole skill.",
        "Fast matcher: `python3 -I .claude/skills/check-skills/scripts/checkskills.py \"TASK\"`.", "",
        "## Routes", "", routes, "", "## Generic skills (project root)", ""] + _lines(places.get("project", []))
    for where in sorted(w for w in places if w not in ("project", "user") and not w.startswith("disabled")):
        lines += ["", f"## {where}", ""] + _lines(places[where])
        with open(os.path.join(PROJECT, where, ".claude", "skills", "INDEX.md"), "w", encoding="utf-8") as f:
            f.write("\n".join([f"# Skills for {where}", ""] + head + _lines(places[where])
                              + ["", "Generic skills and routes: `.claude/skills/INDEX.md` at the workspace root."]) + "\n")
    dis = sorted(os.listdir(DISABLED)) if os.path.isdir(DISABLED) else []
    if dis:
        lines += ["", "Disabled (in `.claude/skills-disabled/`, `skills.py enable NAME` loads one): "
                  + ", ".join(dis)]
    p = os.path.join(SKILLS, "INDEX.md")
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return p



KEEP_RE = re.compile(r"rule|hard|never|always|quick|start|routine|checklist|related|safety|first|method|workflow|steps|procedure|turn method", re.I)


def split(name, skills, budget=140, dry=False):
    """Move the biggest '## ' sections of a SKILL.md into reference/<slug>.md until the SKILL.md is at most
    BUDGET lines. Sections whose heading says rule/hard/never/always/quick/start/routine/checklist/related/
    safety/first stay. Leaves a 'Reference files' table (file - what it holds). No text is dropped:
    returns (words before, words after across SKILL.md + new files, moved [(file, heading)])."""
    s = skills[name]
    p = os.path.join(s["folder"], "SKILL.md")
    text = s["text"]
    end = text.find("\n---", 3) + 4
    fm, body = text[:end], text[end:]
    parts = re.split(r"(?m)^(?=## )", body)
    intro, secs = parts[0], parts[1:]
    in_code = False                      # '## ' inside a code fence is not a heading: re-join such pieces
    merged = []
    for sec in secs:
        if merged and in_code:
            merged[-1] += sec
        else:
            merged.append(sec)
        in_code = (merged[-1].count("```") % 2) == 1
    secs = merged
    n = lambda t: t.count("\n")
    total = n(fm) + n(intro) + sum(n(x) for x in secs)
    order = sorted(range(len(secs)), key=lambda i: -n(secs[i]))
    move, table_cost = set(), 6
    for i in order:
        if total + table_cost + len(move) <= budget:
            break
        head = secs[i].splitlines()[0]
        if KEEP_RE.search(head):
            continue
        move.add(i)
        total -= n(secs[i])
    if not move:
        return None
    os.makedirs(os.path.join(s["folder"], "reference"), exist_ok=True)
    kept, moved, files = [], [], {}
    for i, sec in enumerate(secs):
        if i not in move:
            kept.append(sec)
            continue
        head = sec.splitlines()[0][3:].strip()
        slug = re.sub(r"\b(" + "ry" + "an'?s?|the user'?s?)\b", "", head.lower())   # no names in file names (pieces: export check)
        slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")[:40].strip("-") or f"part{i}"
        f = f"reference/{slug}.md"
        while f in files:
            f = f.replace(".md", "-2.md")
        files[f] = f"# {name} - {head}\n\nPart of the {name} skill; SKILL.md links here.\n\n" + sec.rstrip() + "\n"
        first = re.sub(r"[`*_]", "", " ".join(sec.splitlines()[1:]).strip()).lstrip("-|# ").split(". ")[0][:110]
        moved.append((f, head, first))
    table = ["## Reference files (read the one the step needs)", "", "| File | Holds |", "|---|---|"]
    table += [f"| `{f}` | **{h}** - {d} |" for f, h, d in moved]
    rel = [k for k in kept if k.startswith("## Related")]
    kept = [k for k in kept if not k.startswith("## Related")]
    new = fm + intro + "".join(kept).rstrip() + "\n\n" + "\n".join(table) + "\n\n" + "".join(rel)
    wc = lambda t: len(t.split())
    before = wc(body)
    after = wc(intro) + sum(wc(k) for k in kept) + sum(wc(k) for k in rel) + sum(wc(secs[i]) for i in move)
    if not dry:
        for f, c in files.items():
            with open(os.path.join(s["folder"], f), "w", encoding="utf-8") as fh:
                fh.write(c)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(new.rstrip() + "\n")
    return before, after, [(f, h) for f, h, _ in moved], new.count("\n") + 1


# ---------------------------------------------------------------- command line

def kb(n):
    return f"{n / 1024:.0f} KB" if n < 1024 * 1024 else f"{n / 1024 / 1024:.1f} MB"


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("list")
    a.add_argument("--all", action="store_true")
    a = sub.add_parser("route")
    a.add_argument("task", nargs="+")
    a.add_argument("--n", type=int, default=5)
    a = sub.add_parser("show")
    a.add_argument("name")
    a = sub.add_parser("deps")
    a.add_argument("name", nargs="?")
    a = sub.add_parser("check")
    a.add_argument("name", nargs="?")
    a = sub.add_parser("new")
    a.add_argument("name")
    a.add_argument("description")
    a.add_argument("--uses", default="")
    a.add_argument("--script")
    a.add_argument("--dir", help="game or genre folder (relative to the project root)")
    a = sub.add_parser("import")
    a.add_argument("path")
    a.add_argument("--name")
    a.add_argument("--force", action="store_true")
    a = sub.add_parser("disable")
    a.add_argument("name")
    a = sub.add_parser("enable")
    a.add_argument("name")
    sub.add_parser("index")
    a = sub.add_parser("split")
    a.add_argument("name")
    a.add_argument("--budget", type=int, default=140)
    a.add_argument("--dry", action="store_true")
    o = ap.parse_args(argv)

    if o.cmd in ("disable", "enable"):
        dst = move(o.name, o.cmd == "disable")
        write_index(all_skills())
        print(f"{o.name} -> {dst}\n{'unloaded' if o.cmd == 'disable' else 'loaded'} from the next session on")
        return
    if o.cmd == "new":
        u = [x for x in o.uses.split(",") if x]
        sk = all_skills()
        for x in u:
            if x not in sk:
                sys.exit(f"--uses {x}: no such skill")
        folder = new(o.name, o.description, u, o.script, o.dir)
        write_index(all_skills())
        print(f"made {folder}\nfill in SKILL.md (workflow, facts, gotchas), then: skills.py check {o.name}")
        return
    if o.cmd == "import":
        dest = import_skill(o.path, o.name, o.force)
        sk = all_skills()
        name = os.path.basename(dest)
        write_index(sk)
        print(f"imported {dest}")
        for lv, msg in check(sk[name], sk):
            print(f"  {lv}: {msg}")
        print("read its SKILL.md and scripts before using it: imported files are not trusted")
        return

    sk = all_skills(include_user=getattr(o, "all", False), include_disabled=getattr(o, "all", False))
    if o.cmd == "list":
        for s in sorted(sk.values(), key=lambda s: (s["where"], s["name"])):
            tag = "" if s["where"] == "project" else f" [{s['where']}]"
            print(f"{s['name']:24}{tag} {kb(s['size']):>8}  {len(s['scripts']):2} scripts  "
                  f"desc {len(s['description']):4}  uses: {', '.join(s['uses']) or '-'}")
    elif o.cmd == "route":
        r = route(" ".join(o.task), sk, o.n)
        if not r:
            print("no skill matches; work without one (or make one: skills.py new)")
        for score, name, hit in r:
            order = load_order(name, sk)
            print(f"{score:3}  {name:24} matched: {', '.join(hit)}")
            if len(order) > 1:
                print(f"     load order: {' -> '.join(order)}")
    elif o.cmd == "show":
        s = sk.get(o.name) or all_skills(True, True).get(o.name)
        if not s:
            sys.exit(f"no skill {o.name}")
        print(f"{s['name']} ({s['where']}, {s['folder']})\n\n{s['description']}\n")
        print(f"SKILL.md {s['lines']} lines; {len(s['files'])} files, {kb(s['size'])}")
        print("scripts: " + (", ".join(s["scripts"]) or "-"))
        print("builds on: " + (", ".join(s["uses"]) or "-"))
        print("used by: " + (", ".join(s["used_by"]) or "-"))
        print("see also: " + (", ".join(s["related"]) or "-"))
        print("load order: " + " -> ".join(load_order(s["name"], sk)))
    elif o.cmd == "deps":
        names = [o.name] if o.name else sorted(sk)
        for n in names:
            print(f"{n}: builds on {', '.join(sk[n]['uses']) or '-'}; used by {', '.join(sk[n]['used_by']) or '-'}")
    elif o.cmd == "check":
        names = [o.name] if o.name else sorted(sk)
        bad = 0
        for n in names:
            probs = check(sk[n], sk)
            bad += any(lv == "error" for lv, _ in probs)
            print(f"{n}: {'ok' if not probs else ''}")
            for lv, msg in probs:
                print(f"  {lv}: {msg}")
        sys.exit(1 if bad else 0)
    elif o.cmd == "split":
        r = split(o.name, all_skills(), o.budget, o.dry)
        if not r:
            print(f"{o.name}: nothing to move")
        else:
            b, a_, mv, ln = r
            print(f"{o.name}: {'would move' if o.dry else 'moved'} {len(mv)} sections, SKILL.md -> {ln} lines, "
                  f"words {b} -> {a_} {'OK' if b == a_ else 'MISMATCH'}")
            for f, h in mv:
                print(f"  {f}  ({h})")
    elif o.cmd == "index":
        print(write_index(sk))


if __name__ == "__main__":
    main(sys.argv[1:])
