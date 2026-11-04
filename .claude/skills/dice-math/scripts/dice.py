#!/usr/bin/env python3
"""Exact dice odds for any game - no simulation, every outcome enumerated.

Dice expressions (terms joined by + or -):
  12            a flat number
  2d6           two six-sided dice summed
  4d6kh3        roll 4, keep the highest 3 (kl = keep lowest)
  2d6!          exploding: a die showing its maximum counts in full and rolls again (most tabletop games)
  2d6!d         Dominions DRN style: a 6 counts as 5 and that die rolls again (open-ended 2d6, mean 8)
  2d6r<=2       re-roll each die showing 2 or less, once (keep the new roll); 2d6r>=6 re-rolls 6s
                (FoG II quality: Superior r<=1, Elite r<=2, Untrained r>=6)
  1d20, d100    any die size; "d6" = "1d6"
Explosions are followed to --depth rerolls (default 7: the rest is below 1e-6 for d6).

  python3 -I dice.py dist "2d6!d"                 the distribution: P(=k), P(>=k), P(<=k), mean
  python3 -I dice.py vs "10+2d6!d" "12+2d6!d"      P(first > second), P(tie), P(first < second)
  python3 -I dice.py table "2d6!d" [--from -10 --to 10 --step 1] [--ties first|second|none]
        chance that X + roll beats Y + roll, by X - Y (the "difference table" of an opposed system)
  python3 -I dice.py need "2d6" 8                 P(roll >= 8)   (add --under for P(roll <= 8))
  python3 -I dice.py damage "2d6!d" [--from -10 --to 10]
        expected max(0, (D + roll) - (P + roll)) by D - P: damage left after armour, both rolled
  python3 -I dice.py chain 40 50 75               chance of passing every check in turn (percent each)
  python3 -I dice.py binom 10 0.3 [--atleast 3]   n tries at chance p: P(exactly k) and P(at least k)
"""
import re
import sys
from collections import defaultdict
from math import comb

DEPTH = 7


def die(sides, explode=None):
    """distribution of one die; explode None | 'max' (counts full, rerolls) | 'drn' (counts max-1, rerolls)"""
    if not explode:
        return {v: 1 / sides for v in range(1, sides + 1)}
    dist = defaultdict(float)

    def walk(total, p, depth):
        for v in range(1, sides + 1):
            q = p / sides
            if v == sides and depth < DEPTH:
                walk(total + (sides if explode == "max" else sides - 1), q, depth + 1)
            else:
                dist[total + v] += q
    walk(0, 1.0, 0)
    return dict(dist)


def reroll(sides, op, n):
    """one die, re-rolled once if it shows <= n (op '<=') or >= n (op '>=')"""
    bad = [v for v in range(1, sides + 1) if (v <= n if op == "<=" else v >= n)]
    d = defaultdict(float)
    for v in range(1, sides + 1):
        if v in bad:
            for w in range(1, sides + 1):
                d[w] += 1 / sides / sides
        else:
            d[v] += 1 / sides
    return dict(d)


def add(a, b, sign=1):
    out = defaultdict(float)
    for x, p in a.items():
        for y, q in b.items():
            out[x + sign * y] += p * q
    return dict(out)


def keep(n, sides, k, high=True):
    """NdM keep highest/lowest k, exact by enumerating sorted outcomes (fine for small n)"""
    from itertools import product
    out = defaultdict(float)
    p = 1 / sides ** n
    for roll in product(range(1, sides + 1), repeat=n):
        s = sorted(roll, reverse=high)[:k]
        out[sum(s)] += p
    return dict(out)


def parse(expr):
    expr = expr.replace(" ", "").lower()
    if not expr:
        sys.exit("empty dice expression")
    total = {0: 1.0}
    for sign, term in re.findall(r"([+-]?)((?:[^+-]|r[<>]=)+)", expr):
        s = -1 if sign == "-" else 1
        r = re.fullmatch(r"(\d*)d(\d+)r(<=|>=)(\d+)", term)
        if r:
            one = reroll(int(r.group(2)), r.group(3), int(r.group(4)))
            d = {0: 1.0}
            for _ in range(int(r.group(1) or 1)):
                d = add(d, one)
            total = add(total, d, s)
            continue
        m = re.fullmatch(r"(\d*)d(\d+)(?:(kh|kl)(\d+))?(!d|!)?", term)
        if m:
            n, sides = int(m.group(1) or 1), int(m.group(2))
            if m.group(3):
                d = keep(n, sides, int(m.group(4)), m.group(3) == "kh")
            else:
                one = die(sides, {"!": "max", "!d": "drn"}.get(m.group(5)))
                d = {0: 1.0}
                for _ in range(n):
                    d = add(d, one)
            total = add(total, d, s)
        elif term.isdigit():
            total = {k + s * int(term): p for k, p in total.items()}
        else:
            sys.exit(f"can't read dice term '{term}' (try 2d6, 2d6!, 2d6!d, 4d6kh3, 12)")
    return total


def mean(d):
    return sum(k * p for k, p in d.items())


def compare(a, b):
    """P(a > b), P(a == b), P(a < b)"""
    diff = add(a, b, -1)
    gt = sum(p for k, p in diff.items() if k > 0)
    eq = diff.get(0, 0.0)
    return gt, eq, 1 - gt - eq


def pct(x):
    return f"{100 * x:.1f}"


def arg(a, name, default):
    return a[a.index(name) + 1] if name in a else default


def main(a):
    global DEPTH
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    DEPTH = int(arg(a, "--depth", DEPTH))
    cmd = a[0]
    if cmd == "dist":
        d = parse(a[1])
        ks = sorted(k for k, p in d.items() if p > 1e-5)
        print(f"{a[1]}: mean {mean(d):.2f}, min {ks[0]}, shown to {ks[-1]}")
        print("| k | P(=k) % | P(>=k) % | P(<=k) % |\n|---|---|---|---|")
        for k in ks:
            ge = sum(p for x, p in d.items() if x >= k)
            le = sum(p for x, p in d.items() if x <= k)
            print(f"| {k} | {pct(d[k])} | {pct(ge)} | {pct(le)} |")
    elif cmd == "vs":
        gt, eq, lt = compare(parse(a[1]), parse(a[2]))
        print(f"{a[1]} vs {a[2]}: first higher {pct(gt)}%, tie {pct(eq)}%, second higher {pct(lt)}%")
    elif cmd == "table":
        r = parse(a[1])
        lo, hi, st = int(arg(a, "--from", -10)), int(arg(a, "--to", 10)), int(arg(a, "--step", 1))
        ties = arg(a, "--ties", "none")
        print(f"X + {a[1]} vs Y + {a[1]}, by X - Y (ties: {ties})")
        print("| X-Y | strictly higher % | tie % | higher or tie % | counted % |\n|---|---|---|---|---|")
        for dx in range(lo, hi + 1, st):
            gt, eq, lt = compare({k + dx: p for k, p in r.items()}, r)
            counted = gt + (eq if ties == "first" else 0)
            print(f"| {dx:+d} | {pct(gt)} | {pct(eq)} | {pct(gt + eq)} | {pct(counted)} |")
    elif cmd == "need":
        d, t = parse(a[1]), int(a[2])
        if "--under" in a:
            print(f"P({a[1]} <= {t}) = {pct(sum(p for k, p in d.items() if k <= t))}%")
        else:
            print(f"P({a[1]} >= {t}) = {pct(sum(p for k, p in d.items() if k >= t))}%")
    elif cmd == "damage":
        r = parse(a[1])
        lo, hi = int(arg(a, "--from", -10)), int(arg(a, "--to", 10))
        diff = add(r, r, -1)
        print(f"(D + {a[1]}) - (P + {a[1]}), by D - P\n| D-P | expected damage | any damage % |\n|---|---|---|")
        for dx in range(lo, hi + 1):
            e = sum(max(0, k + dx) * p for k, p in diff.items())
            anyd = sum(p for k, p in diff.items() if k + dx > 0)
            print(f"| {dx:+d} | {e:.2f} | {pct(anyd)} |")
    elif cmd == "chain":
        p = 1.0
        for x in a[1:]:
            if x.startswith("--"):
                break
            p *= float(x) / 100
        print(f"all {len([x for x in a[1:] if not x.startswith('--')])} checks pass: {pct(p)}%")
    elif cmd == "binom":
        n, p = int(a[1]), float(a[2])
        k0 = int(arg(a, "--atleast", 1))
        print("| k | exactly % | at least % |\n|---|---|---|")
        for k in range(n + 1):
            ex = comb(n, k) * p ** k * (1 - p) ** (n - k)
            al = sum(comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))
            if ex > 1e-4 or k == k0:
                print(f"| {k}{' <-' if k == k0 else ''} | {pct(ex)} | {pct(al)} |")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
