#!/usr/bin/env python3
"""Which skills fit this task? A fast matcher (< 1 s) for the check-skills skill and its auto-load hook.

  checkskills.py "TASK TEXT" [--n 8] [--cwd DIR]   best-matching skills (name, folder, why), best first
  checkskills.py hook                              UserPromptSubmit / SessionStart hook: reads the hook
                                                   JSON on stdin, prints additionalContext JSON (always
                                                   exits 0; prints nothing it can't work out)

Scores every SKILL.md under the workspace (.claude/skills/*/SKILL.md, game and genre folders included,
skills-disabled left out) by the task's words: name x4, folder path x2, description + keywords: line x1 (words
stemmed), plus a bonus when
the session's working folder is inside the skill's folder. skills-manager `route` is the slower, deeper
version (dependency order) - use it when planning; this one is for every message.
Pure standard library.
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4))   # workspace = folder holding .claude/
STOP = set("""the and for you that this with your are was but not have all can just yeah yah know get got
gonna wanna its it's out about from into what when then them they there here also some more like make
check sure want need probably thing things stuff one two now next turn go look load all other relevant
please okay ok alright also how why should would could did does done let lets i'm im""".split())


ALIAS = {"dominions": "dom6", "dom": "dom6", "fog": "fog2m", "glory": "fog2m", "se4": "se4", "sprites": "sprite"}


def stem(w):
    """crude English stem so 'odds'/'odd', 'rolling'/'roll', 'skills'/'skill' meet."""
    for suf in ("ing", "ies", "es", "ed", "s"):
        if len(w) > len(suf) + 3 and w.endswith(suf):
            return w[: -len(suf)] + ("y" if suf == "ies" else "")
    return w


def words(t):
    ws = [w for w in re.findall(r"[a-z0-9][a-z0-9'-]{2,}", t.lower()) if w not in STOP]
    ws += [ALIAS[w] for w in ws if w in ALIAS]
    ws += ["dice"] if any(re.fullmatch(r"\d*d\d+\S*", w) for w in ws) else []   # 3d6, 1d20+5 -> dice
    return ws + [stem(w) for w in ws if stem(w) != w]


def hits_prefix(tw, nw):
    """task words that equal a name word or are a prefix of one ("fog" -> fog2m, "sprite" -> sprites)."""
    return {t for t in tw for n in nw if n == t or (len(t) >= 3 and n.startswith(t))}


def skills():
    out = []
    for d, ds, fs in os.walk(ROOT):
        ds[:] = [x for x in ds if x not in (".git", "node_modules", "__pycache__", "skills-disabled", "illwiki",
                                            "retired", "Manuals", "data")]
        if os.path.basename(os.path.dirname(d)) == "skills" and "SKILL.md" in fs \
                and os.path.basename(os.path.dirname(os.path.dirname(d))) == ".claude":
            try:
                head = open(os.path.join(d, "SKILL.md"), encoding="utf-8").read(3000)
            except OSError:
                continue
            m = re.search(r"^name:\s*(.+)$", head, re.M)
            dm = re.search(r"^description:\s*(.+)$", head, re.M)
            km = re.search(r"^keywords:\s*(.+)$", head, re.M)      # routing words kept out of the listing
            home = os.path.dirname(os.path.dirname(os.path.dirname(d)))   # folder that owns .claude/
            out.append((m.group(1).strip() if m else os.path.basename(d),
                        (dm.group(1) if dm else "") + " " + (km.group(1) if km else ""), home))
    return out


def rank(task, cwd=None, n=8):
    tw = set(words(task))
    cwd = os.path.abspath(cwd or os.getcwd())
    res = []
    sk = skills()
    df = {}                                         # how many skills use each word: rare words count double
    for _, desc, _ in sk:
        for w in set(words(desc)):
            df[w] = df.get(w, 0) + 1
    for name, desc, home in sk:
        rel = os.path.relpath(home, ROOT)
        nw, pw, dw = set(words(name.replace("-", " "))), set(words(rel)), set(words(desc))
        nh = hits_prefix(tw, nw)
        s = 4 * len(nh) + 2 * len(tw & pw) + sum(2 if df.get(w, 0) <= 3 else 1 for w in tw & dw)
        if rel != "." and (cwd == home or cwd.startswith(home + os.sep)):
            s += 3                                  # we are working in this skill's game/genre folder
        if s >= 3:
            res.append((s, name, rel, sorted(nh | (tw & (pw | dw)))[:5]))
    res.sort(key=lambda r: -r[0])
    return res[:n]


def hook():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    ev = data.get("hook_event_name", "UserPromptSubmit")
    prompt = data.get("prompt", "") or ""
    cwd = data.get("cwd") or os.getcwd()
    rule = ("check-skills (light, 2026-11-09): load only the 1-3 skills THIS step needs (already loaded = don't "
            "reload); prefer reading one section of a SKILL.md over loading it whole. Context rules: context-hygiene.")
    hits = rank(prompt, cwd, n=5) if prompt else []
    if hits:
        rule += " Likely matches: " + ", ".join(f"{h[1]}" + (f" [{h[2]}]" if h[2] != "." else "") for h in hits) + "."
    if ev == "SessionStart" and data.get("source") in ("clear", "compact"):
        h = os.path.join(ROOT, ".claude", "handoff", "HANDOFF.md")
        if os.path.exists(h):
            rule += f" A hand-off exists: read {h} first (unload skill)."
    print(json.dumps({"hookSpecificOutput": {"hookEventName": ev, "additionalContext": rule}}))


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    if a[0] == "hook":
        try:
            hook()
        except Exception:
            pass
        return
    n = int(a[a.index("--n") + 1]) if "--n" in a else 8
    cwd = a[a.index("--cwd") + 1] if "--cwd" in a else None
    for s, name, rel, why in rank(a[0], cwd, n):
        print(f"{s:3}  {name:28} {'' if rel == '.' else rel:45} {', '.join(why)}")


if __name__ == "__main__":
    main()
