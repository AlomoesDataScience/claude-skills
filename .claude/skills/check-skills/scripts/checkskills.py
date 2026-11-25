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
    # 2026-11-09 "light" rule ("load only the 1-3 skills ... prefer one section") made Claude stop loading skills.
    # the user 2026-11-17: "If you're not loading them, they are switched off ... put them back on, please."
    rule = ("check-skills (ON, 2026-11-17): before acting, load every skill that fits this step (Skill tool, or Read "
            "SKILL.md for [folder] skills) and follow it. Skills already loaded in this context need no reload; after "
            "a compaction they count as not loaded. Context rules: context-hygiene.")
    hits = rank(prompt, cwd, n=5) if prompt else []
    if hits:
        rule += " Likely matches: " + ", ".join(f"{h[1]}" + (f" [{h[2]}]" if h[2] != "." else "") for h in hits) + "."
        # 2026-11-16: folder skills are often not in the Skill tool's list ("Unknown skill", tried 6 times);
        # say up front to Read them, so no call is wasted
        if any(h[2] != "." for h in hits):
            rule += " [folder] skills: Read <folder>/.claude/skills/<name>/SKILL.md, not the Skill tool."
    if ev == "SessionStart" and data.get("source") in ("clear", "compact"):
        # the user 2026-11-17: "You also need a skill to say ah compaction, let's review."
        rule += " Compaction/clear: run the compaction-review skill FIRST, before any change."
        h = os.path.join(ROOT, ".claude", "handoff", "HANDOFF.md")
        if os.path.exists(h):
            rule += f" A hand-off exists: read {h} first (unload skill)."
    if ev == "SessionStart" and data.get("source") == "compact":
        rule += after_compact(data)
    print(json.dumps({"hookSpecificOutput": {"hookEventName": ev, "additionalContext": rule}}))


def after_compact(data, words_budget=6000, working_budget=2500):
    """Re-inject what a compaction summary loses: The user's own words (verbatim) and the working set.
    the user 2026-11-24, after I doubted settled answers post-compaction: "Chill, you're hallucinating or forgetting
    things. We need to fix it" / "No we gotta do it now, we're doing this cause we're literally building all this
    next!" The summary is in my words; his words and the documents in play must come back as they were."""
    out = ""
    wf = os.path.join(ROOT, ".claude", "handoff", "WORKING.md")
    if os.path.exists(wf):
        w = open(wf, encoding="utf-8", errors="replace").read().strip()
        if len(w) > working_budget:
            w = w[:working_budget] + f" ... (cut; read {wf})"
        out += f"\n\nWORKING SET ({wf}; the task and the documents it depends on, re-read them before acting):\n{w}"
    tp = data.get("transcript_path") or ""
    if tp and os.path.exists(tp):
        try:
            sys.path.insert(0, os.path.join(ROOT, ".claude", "skills", "compaction-review", "scripts"))
            import userwords
            rows, seen = [], set()
            for ts, queued, txt in userwords.words(tp):
                key = " ".join(txt.split())
                if not key or txt.startswith(userwords.SKIP) or key in seen:
                    continue
                seen.add(key)
                rows.append(f"{ts[11:16]} {'[q] ' if queued else ''}{key}")
            keep, size = [], 0
            for r in reversed(rows):             # the most recent words first, whole messages only
                if size + len(r) > words_budget:
                    break
                keep.append(r); size += len(r) + 1
            keep.reverse()
            if keep:
                cut = len(rows) - len(keep)
                out += ("\n\nTHE USER'S OWN WORDS THIS SESSION, verbatim (they win over the summary; "
                        + (f"{cut} older messages left out, run userwords.py for them" if cut else "complete")
                        + "):\n" + "\n".join(keep))
        except Exception as e:
            out += f"\n\n(the user's words could not be re-injected: {e}; run userwords.py.)"
    return out


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
