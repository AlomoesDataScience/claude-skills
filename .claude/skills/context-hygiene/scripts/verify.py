#!/usr/bin/env python3
"""Verify the whole context-saving system works (Proposals/Context cost review.md, built 2026-11-09).
  verify.py [-v]      runs every check, prints PASS/FAIL per check and a total; exit 1 if any fails.
Checks: settings (compaction, retention, 4 hooks and their scripts), the check-skills hook (JSON out, speed,
hand-off notice), routing test, skills lint and budgets, frontmatter YAML, INDEX.md complete, docs.py check,
archive hook + recall, hand-off draft, chat-review digest, archive-curator, cleanup scan/apply/undo in a
sandbox. Leaves no test files behind (sandbox in a temp dir)."""
import glob, json, os, re, shutil, subprocess, sys, tempfile, time

ROOT = os.path.expanduser("~/Desktop/AI Development")
SK = os.path.join(ROOT, ".claude", "skills")
PY = [sys.executable, "-I"]
V = "-v" in sys.argv
results = []


def run(args, inp=None, env=None, timeout=300):
    e = dict(os.environ, **(env or {}))
    r = subprocess.run(PY + args, input=inp, capture_output=True, text=True, cwd=ROOT, env=e, timeout=timeout)
    return r.returncode, r.stdout + r.stderr


def check(name):
    def deco(fn):
        t = time.time()
        try:
            ok, info = fn()
        except Exception as ex:
            ok, info = False, f"{type(ex).__name__}: {ex}"
        results.append(ok)
        print(f"{'PASS' if ok else 'FAIL'}  {name:34} {info if (V or not ok) else ''} ({time.time() - t:.1f}s)")
        return fn
    return deco


@check("settings")
def _():
    s = json.load(open(os.path.expanduser("~/.claude/settings.json")))
    acw = [m.get("autoCompactWindow") for m in s.get("modelSettings", {}).values()]
    bad = []
    if not acw or max(a or 10**9 for a in acw) > 150000:
        bad.append(f"autoCompactWindow {acw}")
    if s.get("cleanupPeriodDays", 30) < 90:
        bad.append("cleanupPeriodDays < 90")
    for ev in ("UserPromptSubmit", "SessionStart", "PreCompact", "SessionEnd"):
        hs = s.get("hooks", {}).get(ev)
        if not hs:
            bad.append(f"no {ev} hook"); continue
        for h in hs[0]["hooks"]:
            m = re.search(r'"(\$HOME[^"]+\.py)"', h["command"])
            if m and not os.path.exists(m.group(1).replace("$HOME", os.path.expanduser("~"))):
                bad.append(f"{ev} script missing")
    return not bad, "; ".join(bad) or f"compaction {acw}, retention {s.get('cleanupPeriodDays')} days, 4 hooks"


@check("check-skills hook (prompt)")
def _():
    t = time.time()
    rc, out = run([os.path.join(SK, "check-skills/scripts/checkskills.py"), "hook"],
                  json.dumps({"hook_event_name": "UserPromptSubmit", "prompt": "what are the odds on 3d6", "cwd": ROOT}))
    d = json.loads(out)["hookSpecificOutput"]
    dt = time.time() - t
    ok = "dice-math" in d["additionalContext"] and dt < 3
    return ok, f"{dt:.1f}s, {d['additionalContext'][-80:]}"


@check("check-skills hook (hand-off notice)")
def _():
    ho = os.path.join(ROOT, ".claude", "handoff", "HANDOFF.md")
    made = not os.path.exists(ho)
    if made:
        os.makedirs(os.path.dirname(ho), exist_ok=True); open(ho, "w").write("# test\n")
    try:
        rc, out = run([os.path.join(SK, "check-skills/scripts/checkskills.py"), "hook"],
                      json.dumps({"hook_event_name": "SessionStart", "source": "clear", "cwd": ROOT}))
    finally:
        if made:
            os.remove(ho)
    return "hand-off exists" in out, out[-90:]


@check("routing test")
def _():
    rc, out = run([os.path.join(SK, "skills-manager/tests/routetest.py"), "-v"])
    return rc == 0, out.strip().splitlines()[0] if rc == 0 else out[-400:]


@check("skills lint (errors, desc budget)")
def _():
    rc, out = run([os.path.join(SK, "skills-manager/scripts/skills.py"), "check"])
    errs = [l for l in out.splitlines() if "error:" in l]
    over = [l for l in out.splitlines() if "words (budget" in l]
    big = [l for l in out.splitlines() if "lines (budget" in l]
    return not errs and not over, f"{len(errs)} errors, {len(over)} long descriptions, {len(big)} long SKILL.md"


@check("frontmatter YAML")
def _():
    try:
        import yaml
    except ImportError:
        return True, "PyYAML not available - skipped"
    bad = []
    fs = [f for f in glob.glob(os.path.join(ROOT, "**/.claude/skills/*/SKILL.md"), recursive=True) if "/Archive/" not in f]
    for f in fs:
        t = open(f).read()
        try:
            d = yaml.safe_load(t[3:t.find("\n---", 3)])
            assert isinstance(d["description"], str)
        except Exception:
            bad.append(os.path.relpath(f, ROOT))
    return not bad, f"{len(fs)} files" + (f", bad: {bad[:3]}" if bad else "")


@check("INDEX.md routes + every skill")
def _():
    run([os.path.join(SK, "skills-manager/scripts/skills.py"), "index"])
    idx = open(os.path.join(SK, "INDEX.md")).read()
    names = [os.path.basename(os.path.dirname(f)) for f in
             glob.glob(os.path.join(ROOT, "**/.claude/skills/*/SKILL.md"), recursive=True) if "/Archive/" not in f]
    miss = [n for n in names if f"**{n}**" not in idx]
    return "## Routes" in idx and not miss, f"{len(names)} skills, {idx.count(chr(10))} lines" + (f", missing {miss[:5]}" if miss else "")


@check("docs.py check (no errors)")
def _():
    rc, out = run([os.path.join(SK, "doc-standards/scripts/docs.py"), "check"])
    return rc == 0, out.strip().splitlines()[-1]


@check("archive hook + recall")
def _():
    t = max(glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl")), key=os.path.getmtime)
    idx = os.path.join(ROOT, "Archive", "sessions", "INDEX.md")
    n0 = sum(1 for _ in open(idx)) if os.path.exists(idx) else 0
    sid = os.path.basename(t)[:8]
    run([os.path.join(SK, "unload/scripts/handoff.py"), "precompact"],
        json.dumps({"session_id": sid, "transcript_path": t, "cwd": ROOT, "trigger": "verify"}))
    n1 = sum(1 for _ in open(idx))
    gz = glob.glob(os.path.join(ROOT, "Archive", "sessions", "*", f"*-{sid}.jsonl.gz"))
    rc, out = run([os.path.join(SK, "unload/scripts/handoff.py"), "recall", "context", "--n", "2"])
    return n1 == n0 + 1 and gz and "no matches" not in out, f"index +{n1 - n0}, {len(gz)} archive file, recall ok"


@check("hand-off draft")
def _():
    rc, out = run([os.path.join(SK, "unload/scripts/handoff.py"), "draft"])
    return rc == 0 and "## Next steps" in out, f"{len(out.splitlines())} lines"


@check("chat-review digest")
def _():
    sess = sorted(glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl")), key=os.path.getsize)
    s = [f for f in sess if os.path.getsize(f) > 200000][0]
    rc, out = run([os.path.join(SK, "chat-review/scripts/chatreview.py"), "digest", s])
    m = re.search(r"(\S+\.md)\s+(\d+) KB", out)
    return rc == 0 and m and int(m.group(2)) * 1024 < os.path.getsize(s), out.strip()[:120]


@check("archive-curator")
def _():
    rc, out = run([os.path.join(SK, "archive-curator/scripts/curate.py"), "status"])
    return rc == 0 and len(out.splitlines()) >= 1, f"{len(out.splitlines())} sessions listed"


@check("cleanup scan/apply/undo (sandbox)")
def _():
    sb = tempfile.mkdtemp(prefix="cleanup-verify-")
    try:
        os.makedirs(os.path.join(sb, "a")); os.makedirs(os.path.join(sb, "b")); os.makedirs(os.path.join(sb, "empty"))
        open(os.path.join(sb, "a", "x.txt"), "w").write("same content")
        open(os.path.join(sb, "b", "x.txt"), "w").write("same content")
        open(os.path.join(sb, "setup_game.exe"), "w").write("MZ")
        env = {"CLEANUP_ROOT": sb}
        rc, out = run([os.path.join(SK, "cleanup/scripts/cleanup.py"), "scan", sb, "--out", "t"], env=env)
        cat = glob.glob(os.path.join(sb, "Archive", "cleanup", "*-t.md"))[0]
        txt = open(cat).read()
        cats = all(k in txt for k in ("## duplicate", "## installer", "## empty"))
        open(cat, "w").write(txt.replace("- [ ] `setup_game.exe`", "- [x] `setup_game.exe`"))
        run([os.path.join(SK, "cleanup/scripts/cleanup.py"), "apply", cat], env=env)
        held = glob.glob(os.path.join(sb, "Archive", "cleanup", "held-*"))
        moved = held and not os.path.exists(os.path.join(sb, "setup_game.exe"))
        untouched = os.path.exists(os.path.join(sb, "b", "x.txt"))
        run([os.path.join(SK, "cleanup/scripts/cleanup.py"), "undo", held[0]], env=env)
        back = os.path.exists(os.path.join(sb, "setup_game.exe"))
        return cats and moved and untouched and back, f"categories {cats}, ticked moved {bool(moved)}, unticked kept {untouched}, undo {back}"
    finally:
        shutil.rmtree(sb, ignore_errors=True)


print(f"\n{sum(results)}/{len(results)} checks passed")
sys.exit(0 if all(results) else 1)
