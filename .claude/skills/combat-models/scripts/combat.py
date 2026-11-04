#!/usr/bin/env python3
"""Combat models calculator: Lanchester laws, the salvo combat model and Helmbold parameters.

  combat.py law A B ALPHA BETA [--n 2]        who wins an attrition fight to the end, and survivors.
        A, B = numbers on each side; ALPHA, BETA = kills per unit per time (each side's per-unit
        effectiveness). --n 2 square law (aimed fire, everyone can engage everyone), 1 linear law
        (one-on-one duels / unaimed area fire), 1.5 the common in-between. Invariant: ALPHA*A^n - BETA*B^n.
  combat.py sim A B ALPHA BETA [--n 2] [--dt 0.05] [--steps 400] [--every 20]
        step the fight through time (square: dA=-BETA*B; linear: area fire dA=-BETA*A*B; any n keeps the law's invariant) and print it.
  combat.py split A B ALPHA BETA K [--n 2]     B fights A's force split into K equal parts one after
        another (defeat in detail) vs all at once - shows the value of concentration.
  combat.py need A B ALPHA BETA [--n 2]       per-unit quality BETA needed for B to break even with A
        (and numbers B needed at the same quality).
  combat.py salvo A B ALPHA BETA Y Z W X [--rounds 10]   Hughes salvo model, simultaneous salvos:
        ALPHA/BETA offensive missiles per unit per salvo, Y/Z interceptions per unit per salvo,
        W/X hits needed to put one unit out (staying power). dA = -(BETA*B - Y*A)/W, clipped.
        --first red|blue : one side fires first (surprise / out-scouting).
  combat.py land RED.json BLUE.json [--salvos N] [--dice] [--seed S] [--first red|blue]
        the user's Salvo Combat System for Land Battles (Military Theory/, prototype numbers): each salvo,
        engaged strength (frontage) x rate of fire = shots; x accuracy (training, equipment, fatigue,
        range) = hits; minus tactics saves (target's defensive or offensive tactics by its posture);
        x armour penetration chance = losses. Both sides fire together unless --first. Expected values,
        or --dice for random rolls. Element fields: see LAND_FIELDS below.
  combat.py helmbold A0 D0 AL DL              attacker/defender start strengths and losses ->
        defender's advantage mu, bitterness epsilon, P(defender wins) (Helmbold 2021 logistic).
"""
import math
import sys


def opt(a, k, d, cast=float):
    return cast(a[a.index(k) + 1]) if k in a else d


def law(A, B, al, be, n=2.0):
    inv = al * A ** n - be * B ** n
    if abs(inv) < 1e-12:
        return "draw", 0.0, 0.0
    if inv > 0:
        return "A (red)", (inv / al) ** (1 / n), 0.0
    return "B (blue)", 0.0, (-inv / be) ** (1 / n)


LAND_FIELDS = {        # defaults; every multiplier is 1.0 = no effect
    "name": "element", "strength": 100, "frontage": 1.0, "frontage_mod": 1.0, "frontage_var": 0.0,
    "rof": 1.0, "accuracy": 0.05, "training_mod": 1.0, "equipment_mod": 1.0, "range": 0.0,
    "range_scalar": 0.0, "fatigue": 0.0, "fatigue_scalar": 0.0, "posture": "defend",
    "def_tactics": 0.0, "off_tactics": 0.0, "terrain_def": 0.0, "terrain_off": 0.0,
    "penetration": 1.0, "armor": 0.0, "ammo": 1e9, "moving": False, "move_scalar": 0.0}


def land(a):
    import json, random
    red = dict(LAND_FIELDS, **json.load(open(a[1]))); blue = dict(LAND_FIELDS, **json.load(open(a[2])))
    salvos = opt(a, "--salvos", 6, int); dice = "--dice" in a; first = opt(a, "--first", "", str)
    rnd = random.Random(opt(a, "--seed", 1, int))

    def shots(e):
        fr = e["frontage"] * e["frontage_mod"] * (1 + (rnd.uniform(-1, 1) * e["frontage_var"] if dice else 0))
        engaged = max(0.0, min(e["strength"], e["strength"] * fr))
        n = engaged * e["rof"] * (1 - (e["move_scalar"] if e["moving"] else 0))
        n = min(n, e["ammo"])
        return engaged, n

    def acc(e):
        f = 1 - e["fatigue"] * e["fatigue_scalar"]; r = 1 - e["range"] * e["range_scalar"]
        return max(0.0, min(1.0, e["accuracy"] * e["training_mod"] * e["equipment_mod"] * max(0, f) * max(0, r)))

    def save(t):            # target's tactics + terrain by its posture: chance a hit is nullified
        if t["posture"] == "attack":
            return max(0.0, min(1.0, t["off_tactics"] + t["terrain_off"]))
        return max(0.0, min(1.0, t["def_tactics"] + t["terrain_def"]))

    def pen(s, t):
        return max(0.0, min(1.0, s["penetration"] - t["armor"]))

    def fire(s, t):
        engaged, n = shots(s)
        p = acc(s) * (1 - save(t)) * pen(s, t)
        if dice:
            k = sum(1 for _ in range(int(round(n))) if rnd.random() < p)
        else:
            k = n * p
        return n, min(k, t["strength"])

    print(f"{red['name']}: hit chance per shot {acc(red):.3f}, gets through {(1-save(blue))*pen(red,blue):.2f}")
    print(f"{blue['name']}: hit chance per shot {acc(blue):.3f}, gets through {(1-save(red))*pen(blue,red):.2f}")
    for i in range(1, salvos + 1):
        nr, kr = fire(red, blue); nb, kb = fire(blue, red)
        if i == 1 and first == "red":
            kb = 0.0
        if i == 1 and first == "blue":
            kr = 0.0
        red["ammo"] -= nr; blue["ammo"] -= nb
        blue["strength"] -= kr; red["strength"] -= kb
        print(f"salvo {i}: {red['name']} fires {nr:.0f} -> {kr:.1f} lost | {blue['name']} fires {nb:.0f} -> {kb:.1f} lost"
              f" | left {red['strength']:.1f} v {blue['strength']:.1f}")
        if red["strength"] <= 0 or blue["strength"] <= 0:
            break


def main(a):
    if not a:
        sys.exit(__doc__)
    c = a[0]
    n = opt(a, "--n", 2.0)
    if c == "law":
        A, B, al, be = map(float, a[1:5])
        w, sa, sb = law(A, B, al, be, n)
        print(f"n={n:g}: strength A {al*A**n:.4g} vs B {be*B**n:.4g} -> winner {w}; survivors A {sa:.2f}  B {sb:.2f}")
        print(f"  losses A {A-sa:.2f} ({(A-sa)/A:.0%})  B {B-sb:.2f} ({(B-sb)/B:.0%})")
    elif c == "sim":
        A, B, al, be = map(float, a[1:5])
        dt, steps, every = opt(a, "--dt", 0.05), opt(a, "--steps", 400, int), opt(a, "--every", 20, int)
        t = 0.0
        for i in range(steps + 1):
            if i % every == 0 or A <= 0 or B <= 0:
                print(f"t {t:6.2f}  A {max(A,0):8.2f}  B {max(B,0):8.2f}")
            if A <= 0 or B <= 0:
                break
            # dA = -BETA*B^(n-1)*k, dB = -ALPHA*A^(n-1)*k with the SAME k = (A*B)^(2-n): keeps the invariant
            # ALPHA*A^n - BETA*B^n for any n (n=2: aimed fire dA=-BETA*B; n=1: area fire dA=-BETA*A*B)
            k = (A * B) ** (2 - n)
            dA = -be * B ** (n - 1) * k * dt
            dB = -al * A ** (n - 1) * k * dt
            A, B, t = A + dA, B + dB, t + dt
    elif c == "split":
        A, B, al, be, K = float(a[1]), float(a[2]), float(a[3]), float(a[4]), int(a[5])
        w, sa, sb = law(A, B, al, be, n)
        print(f"all at once: winner {w}, survivors A {sa:.2f} B {sb:.2f}")
        b = B
        for k in range(K):
            w2, sa2, sb2 = law(A / K, b, al, be, n)
            print(f"  part {k+1}/{K} ({A/K:.1f}) vs B {b:.2f}: winner {w2}, A part left {sa2:.2f}, B left {sb2:.2f}")
            b = sb2
            if b <= 0:
                print("  B destroyed"); break
        else:
            print(f"B survives defeat in detail with {b:.2f}")
    elif c == "need":
        A, B, al, be = map(float, a[1:5])
        print(f"n={n:g}: B breaks even with quality beta = {al*A**n/B**n:.4g} (x{al*A**n/B**n/be:.2f} now), "
              f"or with numbers B = {(al*A**n/be)**(1/n):.2f} at the current quality")
    elif c == "salvo":
        A, B, al, be, y, z, w, x = map(float, a[1:9])
        rounds = opt(a, "--rounds", 10, int); first = opt(a, "--first", "", str)
        for r in range(1, rounds + 1):
            hitA = max(0.0, be * B - y * A) / w   # damage to red
            hitB = max(0.0, al * A - z * B) / x   # damage to blue
            if r == 1 and first == "red":
                hitA = 0.0
            if r == 1 and first == "blue":
                hitB = 0.0
            A2, B2 = max(0.0, A - hitA), max(0.0, B - hitB)
            print(f"salvo {r}: red fires {al*A:.1f} (blue stops {z*B:.1f}) -> blue loses {B-B2:.2f};"
                  f" blue fires {be*B:.1f} (red stops {y*A:.1f}) -> red loses {A-A2:.2f}  | left A {A2:.2f} B {B2:.2f}")
            A, B = A2, B2
            if A <= 0 or B <= 0 or (hitA == 0 and hitB == 0 and r > 1):
                break
    elif c == "land":
        land(a)
    elif c == "helmbold":
        A0, D0, AL, DL = map(float, a[1:5])
        FA, FD = AL / A0, DL / D0
        mu, eps = math.sqrt(FA / FD), math.sqrt(FA * FD)
        z = -0.1794 + 5.8694 * math.log(mu)
        print(f"casualty fractions A {FA:.4f} D {FD:.4f}; defender's advantage mu {mu:.4f} (log {math.log(mu):+.4f}),"
              f" bitterness eps {eps:.4f}; P(defender wins) {1/(1+math.exp(-z)):.2f}")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
