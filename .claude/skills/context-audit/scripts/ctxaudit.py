#!/usr/bin/env python3
"""Where does the context go? Reads Claude Code transcripts (~/.claude/projects/*/*.jsonl) and reports:
  - per session: requests, average and peak context size, compactions, total tokens processed (from usage)
  - what ENTERED the context, by source: tool results by tool, images, skill bodies, hook text, system
    reminders, user text, assistant text/thinking (estimated tokens = chars/4; images = w*h/750, capped 1600)
  ctxaudit.py [JSONL ...] [--top 12]        (default: every transcript, biggest sessions first)
Pure standard library (PIL optional, for image sizes)."""
import base64, glob, io, json, os, re, sys
from collections import Counter, defaultdict

def img_tokens(b64):
    try:
        from PIL import Image
        w, h = Image.open(io.BytesIO(base64.b64decode(b64[:200000] + "=" * (-len(b64[:200000]) % 4)))).size
        if w * h > 1_150_000:                      # the API scales big images down to ~1.15 MP
            f = (1_150_000 / (w * h)) ** 0.5; w, h = w * f, h * f
        return int(w * h / 750)
    except Exception:
        return 1600

def tok(s):
    return len(s) // 4

def classify_text(t):
    if t.startswith("Base directory for this skill"):
        return "skill body (Skill tool)"
    if "hook additional context" in t or "hookSpecificOutput" in t:
        return "hook text"
    if t.lstrip().startswith("<system-reminder>") or "<system-reminder>" in t[:200]:
        return "system reminders"
    if "This session is being continued from a previous conversation" in t:
        return "compaction summary"
    return "user text"

def audit(path):
    S = dict(path=path, req=0, ctx=[], out=0, cache_read=0, cache_write=0, inp=0, compact=0)
    src = Counter(); tools = Counter(); calls = Counter(); names = {}; skills = Counter(); imgs = 0
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            e = json.loads(line)
        except Exception:
            continue
        if e.get("isCompactSummary") or e.get("type") == "summary":
            S["compact"] += 1
        m = e.get("message") or {}
        u = m.get("usage")
        if e.get("type") == "assistant" and u:
            c = u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
            if c:
                S["req"] += 1; S["ctx"].append(c)
                S["inp"] += u.get("input_tokens", 0); S["cache_read"] += u.get("cache_read_input_tokens", 0)
                S["cache_write"] += u.get("cache_creation_input_tokens", 0); S["out"] += u.get("output_tokens", 0)
        content = m.get("content")
        if isinstance(content, str):
            src[classify_text(content)] += tok(content); continue
        for it in content or []:
            if not isinstance(it, dict):
                continue
            t = it.get("type")
            if t == "text":
                k = "assistant text" if e.get("type") == "assistant" else classify_text(it.get("text", ""))
                src[k] += tok(it.get("text", ""))
            elif t == "thinking":
                src["assistant thinking"] += tok(it.get("thinking", ""))
            elif t == "tool_use":
                names[it.get("id")] = it.get("name"); calls[it.get("name")] += 1
                src["tool calls (inputs)"] += tok(json.dumps(it.get("input", {})))
                if it.get("name") == "Skill":
                    skills[(it.get("input") or {}).get("skill", "?")] += 1
            elif t == "tool_result":
                n = names.get(it.get("tool_use_id"), "?")
                c = it.get("content")
                parts = c if isinstance(c, list) else [{"type": "text", "text": c or ""}]
                for p in parts:
                    if p.get("type") == "image":
                        k = img_tokens((p.get("source") or {}).get("data", "")); imgs += 1
                        src["images (screenshots)"] += k; tools[n + " [image]"] += k
                    else:
                        k = tok(p.get("text", "") if isinstance(p.get("text"), str) else json.dumps(p))
                        src["tool results (text)"] += k; tools[n] += k
            elif t == "image":
                k = img_tokens((it.get("source") or {}).get("data", "")); imgs += 1; src["images (screenshots)"] += k
    S.update(src=src, tools=tools, calls=calls, skills=skills, imgs=imgs)
    return S

def main():
    a = sys.argv[1:]
    top = int(a[a.index("--top") + 1]) if "--top" in a else 12
    files = [x for x in a if x.endswith(".jsonl")] or glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl"))
    res = sorted((audit(f) for f in files), key=lambda s: -sum(s["ctx"]))
    T = Counter(); TT = Counter(); TC = Counter(); TS = Counter(); tot = dict(req=0, proc=0, cr=0, cw=0, out=0, imgs=0)
    print(f"{'session':44} {'req':>5} {'avg ctx':>8} {'peak':>8} {'compact':>7} {'processed':>11}")
    for s in res:
        if not s["req"]:
            continue
        proc = sum(s["ctx"])
        print(f"{os.path.basename(os.path.dirname(s['path']))[-24:] + '/' + os.path.basename(s['path'])[:18]:44} {s['req']:5} "
              f"{proc // s['req']:8} {max(s['ctx']):8} {s['compact']:7} {proc:11,}")
        T.update(s["src"]); TT.update(s["tools"]); TC.update(s["calls"]); TS.update(s["skills"])
        tot["req"] += s["req"]; tot["proc"] += proc; tot["cr"] += s["cache_read"]; tot["cw"] += s["cache_write"]
        tot["out"] += s["out"]; tot["imgs"] += s["imgs"]
    print(f"\nALL: {tot['req']} requests, {tot['proc']:,} input tokens processed (cache read {tot['cr']:,}, cache write "
          f"{tot['cw']:,}), output {tot['out']:,}; {tot['imgs']} images")
    s = sum(T.values()) or 1
    print("\nWhat entered the context (each item is then RE-SENT on every later request until compaction):")
    for k, v in T.most_common():
        print(f"  {k:28} {v:>10,} tok  {100 * v / s:5.1f}%")
    print("\nTool results by tool (tokens):")
    for k, v in TT.most_common(top):
        print(f"  {k:28} {v:>10,}   calls {TC.get(k.replace(' [image]', ''), 0)}")
    print("\nSkills loaded with the Skill tool (times):", ", ".join(f"{k} {v}" for k, v in TS.most_common(top)))

if __name__ == "__main__":
    main()
