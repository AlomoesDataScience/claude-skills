#!/usr/bin/env python3
"""Evaluate and log each army, turn by turn, for any wargame (army-log skill).

A battle log is one JSON file (next to the battle plan). Each turn, each side gets a snapshot from a
CSV that Claude fills by reading the screen (unit cards, hovers, banners) - never from game data.

  armylog.py new LOG.json --sides "English,French" [--states "Steady,Disrupted,Fragmented,Broken,Routed"]
             [--routed "Broken,Routed"] [--break 60] [--edge 40] [--margin 25] [--turns 24] [--sectors "N:0-10,C:11-13,S:14-99"]
  armylog.py snap LOG.json TURN SIDE UNITS.csv [--banner PCT] [--note "..."]
        CSV columns (header row; extra columns kept): id,name,type,quality,armour,pts,str,max,cohesion,ap,ammo,col,row,facing,role,task,weight
        str blank = full (max); weight blank = 1 (rout share; set 0.5 etc. where the game weights by size)
  armylog.py show LOG.json [TURN]            both armies' tables and summaries for a turn (default: last)
  armylog.py eval LOG.json [TURN]            the evaluation: losses, cohesion, ammo, rout % vs victory
                                             rules, units still to break, combat power by type and sector
  armylog.py diff LOG.json T1 T2             what changed per unit between two turns (moves, losses, cohesion)
  armylog.py turns LOG.json                  one line per turn and side (history)
"""
import csv, json, os, sys

NUM = ("pts", "str", "max", "ap", "ammo", "col", "row", "weight")


def opt(a, k, d=None):
    return a[a.index(k) + 1] if k in a else d


def load(p):
    return json.load(open(p))


def save(p, d):
    json.dump(d, open(p, "w"), indent=1, ensure_ascii=False)


def num(v):
    try:
        return float(v) if "." in str(v) else int(v)
    except (TypeError, ValueError):
        return None


def read_csv(path):
    out = []
    for r in csv.DictReader(l for l in open(path) if l.strip() and not l.startswith("#")):
        r = {k.strip(): (v or "").strip() for k, v in r.items() if k}
        for k in NUM:
            if k in r:
                r[k] = num(r[k])
        if r.get("str") is None and r.get("max") is not None:
            r["str"] = r["max"]
        if r.get("weight") is None:
            r["weight"] = 1
        out.append(r)
    return out


def snaps(d, turn=None):
    ts = sorted({s["turn"] for s in d["snaps"]})
    t = ts[-1] if turn is None else int(turn)
    return t, {s["side"]: s for s in d["snaps"] if s["turn"] == t}


def first(d, side):
    ss = [s for s in d["snaps"] if s["side"] == side]
    return min(ss, key=lambda s: s["turn"]) if ss else None


def routed(d, u):
    return u.get("cohesion", "") in d["routed"] or (u.get("str") == 0)


def summary(d, s):
    us = s["units"]
    W = sum(u["weight"] for u in us)
    rw = sum(u["weight"] for u in us if routed(d, u))
    st = sum(u["str"] or 0 for u in us); mx = sum(u["max"] or 0 for u in us)
    coh = {}
    for u in us:
        coh[u.get("cohesion", "?")] = coh.get(u.get("cohesion", "?"), 0) + 1
    return {"units": len(us), "W": W, "routed_w": rw, "routed_pct": 100 * rw / W if W else 0,
            "str": st, "max": mx, "coh": coh, "pts": sum(u.get("pts") or 0 for u in us)}


def table(us):
    cols = ["id", "name", "type", "str", "max", "cohesion", "ap", "ammo", "col", "row", "facing", "role", "task"]
    cols = [c for c in cols if any(u.get(c) not in (None, "") for u in us)]
    w = {c: max(len(c), *(len(str(u.get(c, "") if u.get(c) is not None else "")) for u in us)) for c in cols}
    w = {c: min(v, 34) for c, v in w.items()}
    print("  " + " ".join(c.ljust(w[c]) for c in cols))
    for u in us:
        print("  " + " ".join(str(u.get(c, "") if u.get(c) is not None else "")[:34].ljust(w[c]) for c in cols))


def show(d, turn):
    t, ss = snaps(d, turn)
    for side in d["sides"]:
        s = ss.get(side)
        if not s:
            print(f"== turn {t} {side}: no snapshot"); continue
        m = summary(d, s)
        print(f"== turn {t} {side}: {m['units']} units, {m['str']}/{m['max']} men, routed {m['routed_pct']:.0f}%"
              + (f" (banner {s['banner']}%)" if s.get("banner") is not None else "") + f"  cohesion {m['coh']}")
        if s.get("note"):
            print("  note:", s["note"])
        table(s["units"])


def sector(d, row):
    for name, rng in d.get("sectors", {}).items():
        lo, hi = map(int, rng.split("-"))
        if row is not None and lo <= row <= hi:
            return name
    return "-"


def evaluate(d, turn):
    t, ss = snaps(d, turn)
    ms = {side: summary(d, ss[side]) for side in d["sides"] if side in ss}
    print(f"== Evaluation, turn {t}" + (f" of {d['turns']} ({d['turns'] - t} left)" if d.get("turns") else ""))
    for side, m in ms.items():
        known = [u for u in ss[side]["units"] if u.get("str") is not None and u.get("max")]
        full = sum(u["max"] for u in known); lost = sum(u["max"] - u["str"] for u in known)
        ammo = [u["ammo"] for u in ss[side]["units"] if u.get("ammo") is not None]
        print(f"- {side}: {m['units']} units ({m['pts']} pts); men {full - lost}/{full} in {len(known)} read units"
              f" (lost {lost}, {100*lost/max(full,1):.1f}%);"
              f" routed {m['routed_pct']:.1f}% of rout weight; cohesion {m['coh']}"
              + (f"; ammo left {sorted(ammo)}" if ammo else ""))
        weak = [u["id"] for u in ss[side]["units"] if u.get("cohesion") and not u["cohesion"].endswith("?")
                and u["cohesion"] not in (d["states"][0], *d["routed"])]
        unread = [u["id"] for u in ss[side]["units"] if u.get("str") is None or str(u.get("cohesion", "")).endswith("?")]
        if unread:
            print(f"    not read this turn (assumed full, unchanged): {unread}")
        if weak:
            print(f"    shaken (not {d['states'][0]}, not routed): {weak}")
    if len(ms) == 2:
        a, b = d["sides"]
        for me, them in ((a, b), (b, a)):
            r_me, r_them = ms[me]["routed_pct"], ms[them]["routed_pct"]
            need_edge = max(d["edge"], r_me + d["margin"])
            print(f"- {them} breaks at {d['break']}% routed, or at {d['edge']}-{d['break']-1}% if {me} has lost at least "
                  f"{d['margin']} points less -> now {r_them:.1f}% vs {me} {r_me:.1f}%: {me} needs ~{need_edge:.0f}% "
                  f"(~{max(0,(need_edge - r_them)/100*ms[them]['W']):.1f} more rout weight, e.g. that many average units)")
    print("- Combat power = points x men left / men at full (unrouted; unread = full) - by type and sector:")
    for side in ms:
        bytype, bysec = {}, {}
        for u in ss[side]["units"]:
            if routed(d, u):
                continue
            f = (u["str"] / u["max"]) if u.get("str") is not None and u.get("max") else 1.0
            v = round((u.get("pts") or 0) * f)
            bytype[u.get("type", "?")] = bytype.get(u.get("type", "?"), 0) + v
            k = sector(d, u.get("row")); bysec[k] = bysec.get(k, 0) + v
        print(f"    {side}: by type {bytype}")
        if d.get("sectors"):
            print(f"    {side}: by sector {bysec}")


def diff(d, t1, t2):
    _, s1 = snaps(d, t1); _, s2 = snaps(d, t2)
    for side in d["sides"]:
        if side not in s1 or side not in s2:
            continue
        a = {u["id"]: u for u in s1[side]["units"]}; b = {u["id"]: u for u in s2[side]["units"]}
        print(f"== {side}: turn {t1} -> {t2}")
        for k in list(a) + [k for k in b if k not in a]:
            x, y = a.get(k), b.get(k)
            if not y:
                print(f"  {k}: gone"); continue
            if not x:
                print(f"  {k}: new at ({y.get('col')},{y.get('row')})"); continue
            ch = []
            if (x.get("col"), x.get("row")) != (y.get("col"), y.get("row")):
                ch.append(f"moved ({x.get('col')},{x.get('row')})->({y.get('col')},{y.get('row')})")
            if x.get("str") != y.get("str"):
                ch.append(f"men {x.get('str')}->{y.get('str')}")
            for f in ("cohesion", "ammo", "facing", "role", "task"):
                if x.get(f) != y.get(f):
                    ch.append(f"{f} {x.get(f)}->{y.get(f)}")
            print(f"  {k}: " + ("; ".join(ch) if ch else "unchanged"))


def main(a):
    if len(a) < 2:
        sys.exit(__doc__)
    c, p = a[0], a[1]
    if c == "new":
        if os.path.exists(p):
            sys.exit(f"{p} exists")
        st = opt(a, "--states", "Steady,Disrupted,Fragmented,Broken,Routed").split(",")
        sec = {}
        if opt(a, "--sectors"):
            for part in opt(a, "--sectors").split(","):
                k, v = part.split(":"); sec[k] = v
        save(p, {"sides": opt(a, "--sides", "A,B").split(","), "states": st,
                 "routed": opt(a, "--routed", "Broken,Routed").split(","), "break": float(opt(a, "--break", 60)),
                 "edge": float(opt(a, "--edge", 40)), "margin": float(opt(a, "--margin", 25)),
                 "turns": int(opt(a, "--turns", 0)) or None, "sectors": sec, "snaps": []})
        print("new log", p)
        return
    d = load(p)
    if c == "snap":
        t, side, f = int(a[2]), a[3], a[4]
        if side not in d["sides"]:
            sys.exit(f"side must be one of {d['sides']}")
        d["snaps"] = [s for s in d["snaps"] if not (s["turn"] == t and s["side"] == side)]
        b = opt(a, "--banner")
        d["snaps"].append({"turn": t, "side": side, "units": read_csv(f), "banner": float(b) if b else None,
                           "note": opt(a, "--note", "")})
        save(p, d)
        print(f"turn {t} {side}: {len(d['snaps'][-1]['units'])} units logged")
    elif c == "show":
        show(d, a[2] if len(a) > 2 else None)
    elif c == "eval":
        evaluate(d, a[2] if len(a) > 2 else None)
    elif c == "diff":
        diff(d, int(a[2]), int(a[3]))
    elif c == "turns":
        for s in sorted(d["snaps"], key=lambda s: (s["turn"], s["side"])):
            m = summary(d, s)
            print(f"turn {s['turn']:>2} {s['side']:<10} units {m['units']:>2} men {m['str']:>5}/{m['max']:<5} routed {m['routed_pct']:5.1f}%  {m['coh']}")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
