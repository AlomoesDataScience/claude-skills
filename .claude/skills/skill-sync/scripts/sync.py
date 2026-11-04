"""Keep skills up to date with the skills they learn from, and move single files in and out of skills.

A skill's SOURCES are the generic skills it uses or names (skills.py uses/related, root .claude/skills) and its
COUNTERPARTS in other games (same name after the game prefix: dom6-map <-> fog2m-map), plus any added by hand.
`mark` snapshots the sources ("synced up to here"); `status` then shows what changed in them since - new,
changed or removed SKILL.md sections and files - so the changes can be carried over, and `diff` shows them.

  python3 -I sync.py changed [--since 2026-11-01] [--game DIR]   which skills changed since a date (newest first)
  python3 -I sync.py sources SKILL [--add S..] [--drop S..]      the sources of a skill (and edit the list)
  python3 -I sync.py status [SKILL..]                            per source: what changed since the last mark
                                                                 (no SKILL: every skill with a ledger entry)
  python3 -I sync.py diff SKILL SOURCE [--file REL]              the changes themselves (unified diff since the
                                                                 snapshot; never synced: sections SKILL lacks)
  python3 -I sync.py mark SKILL [SOURCE..] [--note TEXT]         SKILL is now up to date with these sources
  python3 -I sync.py gaps FROM_PREFIX TO_PREFIX                  skills one game has and the other lacks
                                                                 (gaps fog2m dom6: fog2m-scouting, no dom6-scouting)
  python3 -I sync.py load SRC_SKILL REL DEST_SKILL [--as REL2] [--force]
                                                                 copy one file into a skill, provenance recorded
  python3 -I sync.py unload SKILL REL --why TEXT                 move a file to SKILL/retired/ (never deleted)
  python3 -I sync.py provenance [SKILL]                          loaded files: where from, has the original
                                                                 changed since (then re-load or merge by hand)

Ledger and snapshots: <project>/.claude/skill-sync/ (ledger.json, snapshots/). Whole skills are loaded and
unloaded with skills-manager (skills.py enable / disable). Run with no arguments = this text.
"""
import difflib
import hashlib
import json
import os
import re
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "skills-manager", "scripts"))
import skills as SK                     # noqa: E402  (all_skills, PROJECT, SKILLS)

STORE = os.path.join(SK.PROJECT, ".claude", "skill-sync")
LEDGER = os.path.join(STORE, "ledger.json")
SNAP = os.path.join(STORE, "snapshots")
TEXT_EXT = (".md", ".py", ".sh", ".js", ".json", ".txt", ".csv", ".yaml", ".yml", ".toml")
MAX_SNAP = 512 * 1024                   # bigger files are hashed, not snapshotted


def ledger():
    try:
        return json.load(open(LEDGER))
    except (OSError, ValueError):
        return {}


def save(led):
    os.makedirs(STORE, exist_ok=True)
    json.dump(led, open(LEDGER, "w"), indent=1, sort_keys=True)


def sha(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()[:12]


def tracked(s):
    """The files of a skill that carry its knowledge: SKILL.md, side .md files, scripts (not data, not retired)."""
    out = []
    for rel in s["files"]:
        parts = rel.split(os.sep)
        if parts[0] in ("retired", "data", "__pycache__") or not rel.endswith(TEXT_EXT):
            continue
        if rel == "SKILL.md" or rel.endswith(".md") and len(parts) == 1 or parts[0] == "scripts":
            out.append(rel)
    return out


def prefix_split(name):
    return name.split("-", 1) if "-" in name else (name, "")


def default_sources(s, skills):
    srcs = set()
    for o in s.get("uses", []) + s.get("related", []):
        if o in skills and skills[o]["where"] == "project":     # generic (root) skills
            srcs.add(o)
    if s["where"] != "project":                                 # a game skill: counterparts in other games
        _, suf = prefix_split(s["name"])
        for o, os_ in skills.items():
            if o != s["name"] and os_["where"] != "project" and os_["where"] != s["where"] and suf \
                    and prefix_split(o)[1] == suf:
                srcs.add(o)
    return sorted(srcs)


def sources_of(name, skills, led):
    e = led.get(name, {})
    srcs = set(default_sources(skills[name], skills)) | set(e.get("add", []))
    return sorted(srcs - set(e.get("drop", [])))


def snapshot(src):
    """Store the source's tracked files under snapshots/<src>/<file hash>; return {rel: hash}."""
    files = {}
    for rel in tracked(src):
        p = os.path.join(src["folder"], rel)
        h = sha(p)
        files[rel] = h
        if os.path.getsize(p) <= MAX_SNAP:
            dst = os.path.join(SNAP, src["name"], h)
            if not os.path.exists(dst):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(p, dst)
    return files


def sections(text):
    out, head, buf = {}, "(top)", []
    for line in text.splitlines():
        if line.startswith("## "):
            out[head] = "\n".join(buf)
            head, buf = line[3:].strip(), []
        else:
            buf.append(line)
    out[head] = "\n".join(buf)
    return out


def section_changes(old, new):
    a, b = sections(old), sections(new)
    res = []
    for h in b:
        if h not in a:
            res.append(f"+ section '{h}'")
        elif a[h] != b[h]:
            ratio = difflib.SequenceMatcher(None, a[h], b[h]).ratio()
            res.append(f"~ section '{h}' ({100 - ratio * 100:.0f}% changed)")
    res += [f"- section '{h}'" for h in a if h not in b]
    return res


def read_snap(src_name, h):
    p = os.path.join(SNAP, src_name, h)
    return open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else None


def cmd_changed(since, game=None):
    t = time.mktime(time.strptime(since, "%Y-%m-%d"))
    rows = []
    for s in SK.all_skills().values():
        if game and game not in s["folder"]:
            continue
        m = max(os.path.getmtime(os.path.join(s["folder"], r)) for r in s["files"])
        if m >= t:
            newest = max(s["files"], key=lambda r: os.path.getmtime(os.path.join(s["folder"], r)))
            rows.append((m, s["name"], s["where"], newest))
    for m, n, w, f in sorted(rows, reverse=True):
        print(f"{time.strftime('%m-%d %H:%M', time.localtime(m))}  {n:28s} {('generic' if w == 'project' else w)[:40]:40s} {f}")
    print(f"{len(rows)} skills changed since {since}")


def cmd_sources(name, add, drop):
    skills, led = SK.all_skills(), ledger()
    e = led.setdefault(name, {})
    e["add"] = sorted(set(e.get("add", [])) | set(add) - set(drop))
    e["drop"] = sorted(set(e.get("drop", [])) | set(drop) - set(add))
    if add or drop:
        save(led)
    for o in sources_of(name, skills, led):
        kind = "generic" if skills[o]["where"] == "project" else f"counterpart ({skills[o]['where']})"
        print(f"  {o:28s} {kind}")


def cmd_status(names):
    skills, led = SK.all_skills(), ledger()
    names = names or sorted(n for n in led if led[n].get("synced"))
    if not names:
        print("no skill marked yet: sync.py mark SKILL after bringing it up to date")
    for name in names:
        e = led.get(name, {})
        print(f"== {name}  (last mark {e.get('time', 'never')})")
        for src in sources_of(name, skills, led):
            s = skills[src]
            before = e.get("synced", {}).get(src)
            if before is None:
                print(f"  {src}: never synced ({len(tracked(s))} files) - sync.py diff {name} {src}")
                continue
            now = {rel: sha(os.path.join(s["folder"], rel)) for rel in tracked(s)}
            lines = []
            for rel in sorted(set(now) | set(before)):
                if rel not in before:
                    lines.append(f"    + {rel}")
                elif rel not in now:
                    lines.append(f"    - {rel}")
                elif now[rel] != before[rel]:
                    old = read_snap(src, before[rel])
                    if rel.endswith(".md") and old is not None:
                        new = open(os.path.join(s["folder"], rel), encoding="utf-8", errors="replace").read()
                        lines.append(f"    ~ {rel}: " + "; ".join(section_changes(old, new)[:8]))
                    else:
                        lines.append(f"    ~ {rel}")
            print(f"  {src}: " + ("up to date" if not lines else f"{len(lines)} changes"))
            for l in lines:
                print(l)


def cmd_diff(name, src, only=None):
    skills, led = SK.all_skills(), ledger()
    s = skills[src]
    before = led.get(name, {}).get("synced", {}).get(src)
    if before is None:
        mine = sections(skills[name]["text"])
        theirs = sections(s["text"])
        print(f"{name} never synced with {src}. Sections of {src} (* = no section of that name in {name}):")
        for h, body in theirs.items():
            print(f"  {'*' if h not in mine else ' '} {h} ({body.count(chr(10))} lines)")
        extra = [r for r in tracked(s) if r != "SKILL.md"]
        if extra:
            print(f"files: {', '.join(extra)}")
        return
    for rel in sorted(set(tracked(s)) | set(before)):
        if only and rel != only:
            continue
        p = os.path.join(s["folder"], rel)
        new = open(p, encoding="utf-8", errors="replace").read().splitlines() if os.path.exists(p) else []
        old = (read_snap(src, before[rel]) or "").splitlines() if rel in before else []
        if old != new:
            sys.stdout.writelines(l + "\n" for l in difflib.unified_diff(old, new, f"{src}/{rel} (at mark)",
                                                                         f"{src}/{rel} (now)", lineterm="", n=1))


def cmd_mark(name, srcs, note):
    skills, led = SK.all_skills(), ledger()
    e = led.setdefault(name, {})
    srcs = srcs or sources_of(name, skills, led)
    e.setdefault("synced", {})
    for src in srcs:
        e["synced"][src] = snapshot(skills[src])
    e["time"] = time.strftime("%Y-%m-%d %H:%M")
    if note:
        e.setdefault("notes", []).append(f"{e['time']}: {note}")
    save(led)
    print(f"{name} marked up to date with {', '.join(srcs)}")


def cmd_gaps(a, b):
    names = set(SK.all_skills())
    have_b = {prefix_split(n)[1] for n in names if prefix_split(n)[0] == b}
    for n in sorted(names):
        p, suf = prefix_split(n)
        if p == a and suf not in have_b:
            print(f"  {n:24s} -> no {b}-{suf}")


def cmd_load(src_name, rel, dest_name, as_rel=None, force=False):
    skills, led = SK.all_skills(), ledger()
    src, dest = skills[src_name], skills[dest_name]
    sp = os.path.join(src["folder"], rel)
    dp = os.path.join(dest["folder"], as_rel or rel)
    if not os.path.isfile(sp):
        sys.exit(f"no file {rel} in {src_name}")
    if os.path.exists(dp) and not force:
        sys.exit(f"{dest_name}/{as_rel or rel} exists - compare it first (diff), then --force to replace")
    os.makedirs(os.path.dirname(dp), exist_ok=True)
    shutil.copyfile(sp, dp)
    if dp.endswith(".py"):
        import py_compile
        py_compile.compile(dp, doraise=True)
    led.setdefault(dest_name, {}).setdefault("files", {})[as_rel or rel] = {
        "from": f"{src_name}/{rel}", "hash": sha(sp), "time": time.strftime("%Y-%m-%d %H:%M")}
    snapshot(src)
    save(led)
    print(f"loaded {src_name}/{rel} -> {dest_name}/{as_rel or rel}. Now adapt it (paths, game numbers) and "
          f"mention it in {dest_name}/SKILL.md.")


def cmd_unload(name, rel, why):
    skills, led = SK.all_skills(), ledger()
    s = skills[name]
    sp = os.path.join(s["folder"], rel)
    if not os.path.exists(sp):
        sys.exit(f"no file {rel} in {name}")
    dp = os.path.join(s["folder"], "retired", rel)
    os.makedirs(os.path.dirname(dp), exist_ok=True)
    shutil.move(sp, dp)
    led.setdefault(name, {}).setdefault("retired", {})[rel] = {"why": why, "time": time.strftime("%Y-%m-%d %H:%M")}
    led[name].get("files", {}).pop(rel, None)
    save(led)
    left = [l for l in s["text"].splitlines() if os.path.basename(rel) in l]
    print(f"moved {name}/{rel} -> retired/{rel} ({why})")
    if left:
        print("SKILL.md still mentions it - update these lines:")
        for l in left[:10]:
            print("   ", l.strip()[:140])


def cmd_provenance(names):
    skills, led = SK.all_skills(), ledger()
    for name in names or sorted(led):
        files = led.get(name, {}).get("files", {})
        if not files:
            continue
        print(f"== {name}")
        for rel, f in sorted(files.items()):
            sname, srel = f["from"].split("/", 1)
            sp = os.path.join(skills[sname]["folder"], srel) if sname in skills else ""
            state = "source gone" if not os.path.exists(sp) else (
                "source unchanged" if sha(sp) == f["hash"] else "SOURCE CHANGED since load")
            print(f"  {rel:34s} from {f['from']} ({f['time']}): {state}")


def opt(a, flag, n=1, default=None):
    if flag not in a:
        return default
    i = a.index(flag)
    vals = a[i + 1:i + 1 + n]
    del a[i:i + 1 + n]
    return vals[0] if n == 1 else vals


def multi(a, flag):
    if flag not in a:
        return []
    i = a.index(flag)
    j = i + 1
    while j < len(a) and not a[j].startswith("--"):
        j += 1
    vals = a[i + 1:j]
    del a[i:j]
    return vals


def main(a):
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    c, a = a[0], a[1:]
    if c == "changed":
        since = opt(a, "--since", default=time.strftime("%Y-%m-%d", time.localtime(time.time() - 3 * 86400)))
        cmd_changed(since, opt(a, "--game"))
    elif c == "sources":
        add, drop = multi(a, "--add"), multi(a, "--drop")
        cmd_sources(a[0], add, drop)
    elif c == "status":
        cmd_status(a)
    elif c == "diff":
        f = opt(a, "--file")
        cmd_diff(a[0], a[1], f)
    elif c == "mark":
        note = opt(a, "--note")
        cmd_mark(a[0], a[1:], note)
    elif c == "gaps":
        cmd_gaps(a[0], a[1])
    elif c == "load":
        as_rel, force = opt(a, "--as"), "--force" in a
        a = [x for x in a if x != "--force"]
        cmd_load(a[0], a[1], a[2], as_rel, force)
    elif c == "unload":
        why = opt(a, "--why")
        if not why:
            sys.exit("unload needs --why TEXT (the reason is kept with the file)")
        cmd_unload(a[0], a[1], why)
    elif c == "provenance":
        cmd_provenance(a)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
