#!/usr/bin/env python3
"""What a mod (or a patch) changed in a game's data, and what got better or worse - for any game.

  python3 -I moddiff.py diff OLD NEW --key id [--rules RULES.json] [--top 40] [--only better|worse|new|removed|mixed|other]
  python3 -I moddiff.py summary OLD NEW --key id [--rules RULES.json] [--by school]
  python3 -I moddiff.py row OLD NEW --key id NAME        one row's changes, scored line by line

OLD / NEW  .csv or .json (list of objects) - the same kind of table before and after (vanilla vs mod, patch
           1.0 vs 1.1). Rows are matched by --key (default "id"); --name-col names them in output (default "name").
RULES.json says how to judge a changed field (anything not listed counts as "other"):
  {"lower_better":  {"cost": 2, "fatigue": 1, "research": 2},
   "higher_better": {"damage": 2, "area": 2, "range": 1, "hp": 1},
   "flags_good":    {"ignores_shields": 2},          flag appearing = better by the weight
   "flags_bad":     {"mr_negates": 2},               flag appearing = worse
   "ai_only":       ["ai_weight", "ai_nocast"],     changes that only move the AI's choices
   "ignore":        ["rank", "score"],               derived columns, not real changes
   "group":         "school"}                        default column for --by
Numbers are read from the start of the value ("30+", "5E" -> 30, 5; "6+ [2/lvl]" -> 8). Encoded fields
(ids, effect codes) belong in no list - they show up as "other" for a human to read. A change is "better" if every scored
field moved the good way, "worse" if every one moved the bad way, else "mixed"; only AI fields = "AI only".
Dominions has a fuller version over modinspector output: dom6-mod-magic (modmagic.py).
"""
import csv
import json
import re
import sys
from collections import Counter

a = sys.argv[1:]


def opt(name, default=None):
    return a[a.index(name) + 1] if name in a else default


def load(path):
    if path.endswith(".json"):
        return json.load(open(path, encoding="utf-8"))
    return list(csv.DictReader(open(path, encoding="utf-8")))


def num(v):
    """leading number; a per-level part like "6+ [2/lvl]" adds its step once (so 6 -> 6+[2/lvl] is better)"""
    m = re.match(r"\s*(-?\d+(?:\.\d+)?)", str(v)) or re.search(r"(-?\d+(?:\.\d+)?)\s*$", str(v))
    if not m:                                   # (or a trailing number: "Enchantment 4" -> 4)
        return None
    x = float(m.group(1))
    step = re.search(r"\[(\d+(?:\.\d+)?)/lvl\]", str(v))
    return x + (float(step.group(1)) if step else 0)


def truthy(v):
    return str(v).strip().lower() not in ("", "0", "-", "false", "no", "none")


def score(old, new, R):
    s, why, ai, other = 0, [], [], []
    for k in sorted(set(old) | set(new)):
        o, n = old.get(k, ""), new.get(k, "")
        if str(o) == str(n) or k in R.get("ignore", []):
            continue
        if k in R.get("ai_only", []):
            ai.append(f"{k} {o}->{n}")
            continue
        if k in R.get("lower_better", {}) or k in R.get("higher_better", {}):
            x, y = num(o), num(n)
            if x is None or y is None or x == y:
                other.append(f"{k} {o}->{n}")
                continue
            w = R.get("lower_better", {}).get(k) or R.get("higher_better", {}).get(k)
            good = (y < x) if k in R.get("lower_better", {}) else (y > x)
            s += w if good else -w
            why.append(("+" if good else "-") + f"{k} {o}->{n}")
        elif k in R.get("flags_good", {}) or k in R.get("flags_bad", {}):
            added, was = truthy(n), truthy(o)
            if added == was:
                continue
            w = R.get("flags_good", {}).get(k) or -R.get("flags_bad", {}).get(k)
            d = w if added else -w
            s += d
            why.append(("+" if d > 0 else "-") + f"{k} {'added' if added else 'removed'}")
        else:
            other.append(f"{k} {str(o)[:30]}->{str(n)[:30]}")
    return s, why, ai, other


def kind(s, why, ai, other):
    if not why:
        return "AI only" if ai and not other else "other" if other else "same"
    pos, neg = any(w[0] == "+" for w in why), any(w[0] == "-" for w in why)
    return "better" if pos and not neg else "worse" if neg and not pos else "mixed"


def main():
    if len(a) < 3 or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    cmd, old, new = a[0], load(a[1]), load(a[2])
    key, name = opt("--key", "id"), opt("--name-col", "name")
    R = json.load(open(opt("--rules"))) if opt("--rules") else {}
    O = {str(r.get(key)): r for r in old}
    N = {str(r.get(key)): r for r in new}
    res = []
    for k, r in N.items():
        if k not in O:
            res.append(("new", 0, [], [], [], r))
        else:
            s, why, ai, other = score(O[k], r, R)
            kd = kind(s, why, ai, other)
            if kd != "same":
                res.append((kd, s, why, ai, other, r))
    for k, r in O.items():
        if k not in N:
            res.append(("removed", 0, [], [], [], r))
    if cmd == "summary":
        c = Counter(x[0] for x in res)
        print(f"{len(res)} rows changed of {len(N)}: " + ", ".join(f"{k} {v}" for k, v in c.most_common()))
        g = opt("--by", R.get("group"))
        if g:
            by = {}
            for x in res:
                by.setdefault(str(x[5].get(g, "?")), Counter())[x[0]] += 1
            print(f"\nby {g}: (new / better / worse / mixed / AI only / other / removed)")
            for k, v in sorted(by.items(), key=lambda kv: -sum(kv[1].values())):
                print(f"  {k[:20]:20} " + " ".join(f"{v[t]:4}" for t in
                                                   ("new", "better", "worse", "mixed", "AI only", "other", "removed")))
    elif cmd == "diff":
        only = opt("--only")
        rows = [x for x in res if not only or x[0] == only]
        rows.sort(key=lambda x: (["better", "new", "mixed", "worse", "AI only", "other", "removed"].index(x[0]), -x[1]))
        print("| Change | Score | Name | Why |\n|---|---|---|---|")
        for kd, s, why, ai, other, r in rows[:int(opt("--top", 40))]:
            txt = "; ".join(why + [f"(AI) {x}" for x in ai] + [f"(?) {x}" for x in other])
            print(f"| {kd} | {s:+d} | {r.get(name, '?')} | {txt.replace('|', '/')[:200]} |")
        print(f"\n{len(rows)} rows" + (f" ({only})" if only else ""))
    elif cmd == "row":
        q = " ".join(x for x in a[3:] if not x.startswith("--") and x not in (key, name, opt("--rules", ""))).lower()
        for kd, s, why, ai, other, r in res:
            if q and q in str(r.get(name, "")).lower():
                print(f"{r.get(name)}: {kd}, score {s:+d}")
                for x in why:
                    print("  scored:", x)
                for x in ai:
                    print("  AI only:", x)
                for x in other:
                    print("  not scored:", x)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
