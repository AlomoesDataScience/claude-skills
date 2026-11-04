#!/usr/bin/env python3
"""Rank-everything database for any game: rows (units, spells, items, techs...) + a small scorer file ->
SQLite + CSV + one markdown page per purpose, with percentile tiers inside each purpose.

  python3 -I gamedb.py build ROWS SCORER --out DIR [--label NAME] [--name-col name]
        ROWS   a .csv or .json (list of objects) with one row per thing
        SCORER a .py file defining
                 purpose(row) -> str            what the thing is FOR ("army damage", "anti-armour", ...)
                 score(row)   -> dict           {"value": float or None, "cost": float or None,
                                                 "basis": "simulated" | "weights" | "cost" | "stat",
                                                 "detail": "why, in a few words"}
               optional: exclude(row) -> bool (tier "-", listed last), CURATED = {"Name": "S", ...}
  python3 -I gamedb.py top DIR PURPOSE [--top 25] [--where "cost<=20"]
  python3 -I gamedb.py purposes DIR
  python3 -I gamedb.py sql DIR "SELECT name, tier FROM things WHERE ..."

Scoring rule used by build: eff = value / cost (cost 0 or missing -> value), score = sqrt(value x eff)
(rewards both raw power and efficiency); rows without a value are ordered by cost (cheapest first) and get
basis "cost". Tiers by percentile of score inside a purpose: S 10%, A 20%, B 30%, C 25%, D 15%.
Example scorer: ../examples/score_example.py. Full worked case: Dominions 6 dom6-spell-db (spelldb.py).
"""
import csv
import importlib.util
import json
import math
import os
import re
import sqlite3
import sys

TIERS = [("S", 0.10), ("A", 0.30), ("B", 0.60), ("C", 0.85), ("D", 1.01)]


def arg(a, name, default=None):
    return a[a.index(name) + 1] if name in a else default


def load_rows(path):
    if path.endswith(".json"):
        return json.load(open(path, encoding="utf-8"))
    return list(csv.DictReader(open(path, encoding="utf-8")))


def load_scorer(path):
    spec = importlib.util.spec_from_file_location("scorer", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "other"


def build(a):
    rows, sc = load_rows(a[1]), load_scorer(a[2])
    out, label, name_col = arg(a, "--out"), arg(a, "--label", "db"), arg(a, "--name-col", "name")
    if not out:
        sys.exit("--out DIR needed")
    cur = getattr(sc, "CURATED", {})
    recs = []
    for r in rows:
        s = sc.score(r) or {}
        v, c = s.get("value"), s.get("cost")
        eff = None if v is None else (v / c if c else v)
        rec = {"name": str(r.get(name_col, "?")), "purpose": sc.purpose(r), "value": v, "cost": c, "eff": eff,
               "score": None if v is None else math.sqrt(max(v, 0) * max(eff, 0)),
               "basis": s.get("basis") or ("cost" if v is None else "stat"), "detail": s.get("detail", ""),
               "excluded": bool(getattr(sc, "exclude", lambda r: False)(r)),
               "curated": cur.get(str(r.get(name_col, "")), ""), "raw": json.dumps(r, ensure_ascii=False)}
        recs.append(rec)
    by = {}
    for r in recs:
        by.setdefault(r["purpose"], []).append(r)
    for p, lst in by.items():
        live = [r for r in lst if not r["excluded"]]
        valued = sorted((r for r in live if r["score"] is not None), key=lambda r: -r["score"])
        costed = sorted((r for r in live if r["score"] is None), key=lambda r: (r["cost"] is None, r["cost"] or 0))
        ordered = valued + costed
        for i, r in enumerate(ordered):
            q = i / max(len(ordered), 1)
            r["rank"], r["tier"] = i + 1, next(t for t, cut in TIERS if q < cut)
        for r in lst:
            if r["excluded"]:
                r["rank"], r["tier"] = 9999, "-"
    os.makedirs(out, exist_ok=True)
    cols = ["name", "purpose", "tier", "rank", "score", "value", "cost", "eff", "basis", "curated", "detail",
            "excluded", "raw"]
    dbp = os.path.join(out, f"{label}.sqlite")
    if os.path.exists(dbp):
        os.remove(dbp)
    con = sqlite3.connect(dbp)
    con.execute(f"CREATE TABLE things ({', '.join(cols)})")
    con.executemany(f"INSERT INTO things VALUES ({','.join('?' * len(cols))})", [[r[c] for c in cols] for r in recs])
    con.commit()
    with open(os.path.join(out, f"{label}.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols[:-1], extrasaction="ignore")
        w.writeheader()
        w.writerows(recs)
    idx = [f"# {label}: {len(recs)} rows, {len(by)} purposes\n", "| Purpose | Rows | Top 3 |", "|---|---|---|"]
    for p, lst in sorted(by.items()):
        lst = sorted(lst, key=lambda r: r["rank"])
        page = [f"# {p} ({label})\n", "| # | Tier | Name | Value | Cost | Eff | Basis | Hand | Detail |",
                "|---|---|---|---|---|---|---|---|---|"]
        for r in lst:
            f3 = lambda x: "" if x is None else f"{x:.3g}"
            page.append(f"| {r['rank'] if r['rank'] < 9999 else '-'} | {r['tier']} | {r['name']} | {f3(r['value'])} | "
                        f"{f3(r['cost'])} | {f3(r['eff'])} | {r['basis']} | {r['curated']} | "
                        f"{str(r['detail']).replace('|', '/')[:100]} |")
        open(os.path.join(out, slug(p) + ".md"), "w", encoding="utf-8").write("\n".join(page) + "\n")
        idx.append(f"| [{p}]({slug(p)}.md) | {len(lst)} | {', '.join(r['name'] for r in lst[:3])} |")
    open(os.path.join(out, "INDEX.md"), "w", encoding="utf-8").write("\n".join(idx) + "\n")
    print(f"{len(recs)} rows, {len(by)} purposes -> {dbp}, {label}.csv, INDEX.md + one page per purpose in {out}")


def query(a, sql, params=()):
    d = a[1]
    dbs = [f for f in os.listdir(d) if f.endswith(".sqlite")]
    if not dbs:
        sys.exit(f"no .sqlite in {d} - run build first")
    con = sqlite3.connect(os.path.join(d, dbs[0]))
    cur = con.execute(sql, params)
    names = [c[0] for c in cur.description]
    rows = cur.fetchall()
    print("| " + " | ".join(names) + " |\n|" + "---|" * len(names))
    for r in rows:
        print("| " + " | ".join("" if x is None else (f"{x:.3g}" if isinstance(x, float) else str(x)) for x in r) + " |")
    print(f"\n{len(rows)} rows")


def main(a):
    if len(a) < 2 or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    if a[0] == "build" and len(a) >= 3:
        build(a)
    elif a[0] == "top" and len(a) >= 3:
        where = arg(a, "--where")
        sql = ("SELECT rank, tier, name, value, cost, eff, basis, curated, detail FROM things WHERE purpose=?"
               + (f" AND ({where})" if where else "") + " ORDER BY rank LIMIT ?")
        query(a, sql, (a[2], int(arg(a, "--top", 25))))
    elif a[0] == "purposes":
        query(a, "SELECT purpose, count(*) n FROM things GROUP BY purpose ORDER BY n DESC")
    elif a[0] == "sql" and len(a) >= 3:
        query(a, a[2])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
