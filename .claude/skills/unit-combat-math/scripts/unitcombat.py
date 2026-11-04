#!/usr/bin/env python3
"""Unit-vs-unit combat math for any game: hit -> damage -> kill -> rounds, exact per attack (dice-math) and
simulated for whole fights. Pick the game's rule system, give two units as key=value lists.

Units:  "att=12,def=10,dmg=13,prot=15,hp=15,attacks=1,ap=0,an=0,regen=0"
  att/def  attack and defence (opposed systems) - or att = to-hit bonus, def = target number (target systems)
  dmg      flat damage added to the damage roll (Dominions: strength + weapon damage)
  prot     armour subtracted from damage; ap=1 halves the target's armour, an=1 ignores it
  hp, attacks per round, regen (HP back per round)

Rule systems (--rules, default dom6):
  dom6     hit: att + 2d6!d > def + 2d6!d (attacker must be strictly higher)
           damage: (dmg + 2d6!d) - (prot + 2d6!d), at least 0
  d20      hit: 1d20 + att >= def (def = armour class); damage: --dmgdice (default 1d8) + dmg - prot, min 0
  custom   --hit "2d6" --hitties first|second|none --dmgroll "2d6!d" --protroll "2d6!d"
           (opposed hit with those dice; protroll "0" for flat armour)
  --harass N  defender's defence -N for every earlier attack on it this round (Dominions: -1 per attack)

  python3 -I unitcombat.py expect A B          one attack of A on B: hit %, damage per hit, per attack, per round,
                                               rounds to kill (simulated distribution)
  python3 -I unitcombat.py duel A B [-n 20000] both strike each round: win %, draw %, rounds, HP left
  python3 -I unitcombat.py buff A B "prot+7" [--on a|b]
                                               what a modifier is worth: rounds-to-kill both ways, before/after
  python3 -I unitcombat.py crowd A B --n 3     N copies of A on one B with harassment: rounds to kill B
"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "dice-math", "scripts"))
import dice  # noqa: E402

a = sys.argv[1:]


def opt(name, default):
    return a[a.index(name) + 1] if name in a else default


RULES = opt("--rules", "dom6")
HARASS = float(opt("--harass", 1 if RULES == "dom6" else 0))
if RULES == "dom6":
    HIT, HIT_TIES, DMG, PROT = "2d6!d", "second", "2d6!d", "2d6!d"
elif RULES == "d20":
    HIT, HIT_TIES, DMG, PROT = "1d20", "target", opt("--dmgdice", "1d8"), "0"
else:
    HIT, HIT_TIES = opt("--hit", "2d6"), opt("--hitties", "none")
    DMG, PROT = opt("--dmgroll", "2d6"), opt("--protroll", "0")
D_HIT, D_DMG, D_PROT = dice.parse(HIT), dice.parse(DMG), dice.parse(PROT)


def unit(s):
    u = {"att": 10, "def": 10, "dmg": 10, "prot": 0, "hp": 10, "attacks": 1, "ap": 0, "an": 0, "regen": 0}
    for kv in filter(None, s.split(",")):
        k, _, v = kv.partition("=")
        u[k.strip()] = float(v)
    return u


def modify(u, mods):
    u = dict(u)
    for m in filter(None, mods.split(",")):
        k, op, v = m.partition("+") if "+" in m else m.partition("-")
        u[k] = u.get(k, 0) + (float(v) if op == "+" else -float(v))
    return u


_HIT = {}
_SAMP = {}


def p_hit(A, B, harass=0):
    key = (A["att"], B["def"] - harass)
    if key not in _HIT:
        _HIT[key] = _p_hit(A, B, harass)
    return _HIT[key]


def _p_hit(A, B, harass=0):
    if HIT_TIES == "target":
        return sum(p for k, p in D_HIT.items() if k + A["att"] >= B["def"] - harass)
    gt, eq, _ = dice.compare({k + A["att"]: p for k, p in D_HIT.items()},
                             {k + B["def"] - harass: p for k, p in D_HIT.items()})
    return gt + (eq if HIT_TIES == "first" else 0)


def prot_of(A, B):
    return 0 if A["an"] else B["prot"] / 2 if A["ap"] else B["prot"]


def dmg_dist(A, B):
    """distribution of damage of one landed hit"""
    out = {}
    pr = prot_of(A, B)
    for x, p in D_DMG.items():
        for y, q in D_PROT.items():
            d = max(0, int(x + A["dmg"] - (y + pr)))
            out[d] = out.get(d, 0) + p * q
    return out


def sampler(dist):
    ks, ps = zip(*sorted(dist.items()))
    acc, c = [], 0
    for p in ps:
        c += p
        acc.append(c)

    def draw(r=random.random):
        x = r()
        for k, t in zip(ks, acc):
            if x <= t:
                return k
        return ks[-1]
    return draw


def round_damage(A, B, attackers=1):
    """one round of damage from `attackers` copies of A onto B, with harassment building up"""
    total, n = 0, 0
    key = (A["dmg"], prot_of(A, B))
    if key not in _SAMP:
        _SAMP[key] = sampler(dmg_dist(A, B))
    draw = _SAMP[key]
    for _ in range(attackers):
        for _ in range(int(A["attacks"])):
            if random.random() < p_hit(A, B, HARASS * n):
                total += draw()
            n += 1
    return total


def rounds_to_kill(A, B, n=4000, attackers=1, cap=200):
    out = []
    for _ in range(n):
        hp, r = B["hp"], 0
        while hp > 0 and r < cap:
            r += 1
            hp -= round_damage(A, B, attackers)
            if hp > 0:
                hp = min(B["hp"], hp + B["regen"])
        out.append(r)
    out.sort()
    return sum(out) / n, out[n // 2], out[int(n * 0.9)], sum(1 for x in out if x >= cap) / n


def duel(A, B, n=20000, cap=200):
    wa = wb = draw = 0
    rounds = []
    for _ in range(n):
        ha, hb, r = A["hp"], B["hp"], 0
        while ha > 0 and hb > 0 and r < cap:
            r += 1
            da, db = round_damage(A, B), round_damage(B, A)
            hb, ha = hb - da, ha - db
            if hb > 0:
                hb = min(B["hp"], hb + B["regen"])
            if ha > 0:
                ha = min(A["hp"], ha + A["regen"])
        rounds.append(r)
        if hb <= 0 < ha:
            wa += 1
        elif ha <= 0 < hb:
            wb += 1
        else:
            draw += 1
    return wa / n, wb / n, draw / n, sum(rounds) / n


def show_expect(A, B, label="A on B"):
    ph = p_hit(A, B)
    dd = dmg_dist(A, B)
    eh = sum(k * p for k, p in dd.items())
    mean, med, p90, never = rounds_to_kill(A, B)
    print(f"{label}: hit {100 * ph:.1f}%, damage per hit {eh:.2f} (any damage {100 * (1 - dd.get(0, 0)):.0f}%), "
          f"per attack {ph * eh:.2f}, per round {ph * eh * A['attacks']:.2f}; rounds to kill: mean {mean:.1f}, "
          f"median {med}, 90% by {p90}" + (f", never within 200 rounds {100 * never:.0f}%" if never else ""))
    return mean


def main():
    if len(a) < 3 or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    cmd, A, B = a[0], unit(a[1]), unit(a[2])
    print(f"rules {RULES}: hit {HIT} ({HIT_TIES}), damage {DMG} vs protection {PROT}, harassment {HARASS:g}")
    if cmd == "expect":
        show_expect(A, B)
    elif cmd == "duel":
        wa, wb, dr, r = duel(A, B, int(opt("-n", 20000)))
        print(f"duel: A wins {100 * wa:.1f}%, B wins {100 * wb:.1f}%, neither {100 * dr:.1f}%, mean {r:.1f} rounds")
        show_expect(A, B, "A on B")
        show_expect(B, A, "B on A")
    elif cmd == "buff":
        mods, on = a[3], opt("--on", "a")
        A2, B2 = (modify(A, mods), B) if on == "a" else (A, modify(B, mods))
        print(f"before:")
        x1, y1 = show_expect(A, B, "  A kills B"), show_expect(B, A, "  B kills A")
        print(f"after {mods} on {on.upper()}:")
        x2, y2 = show_expect(A2, B2, "  A kills B"), show_expect(B2, A2, "  B kills A")
        print(f"change in rounds to kill: A kills B {x2 - x1:+.1f}, B kills A {y2 - y1:+.1f}")
    elif cmd == "crowd":
        k = int(opt("--n", 3))
        mean, med, p90, never = rounds_to_kill(A, B, attackers=k)
        print(f"{k} x A on one B (harassment {HARASS:g}/attack): mean {mean:.1f} rounds, median {med}, 90% by {p90}")
        mean1 = rounds_to_kill(A, B)[0]
        print(f"one A alone: {mean1:.1f} rounds - the crowd is {mean1 / max(mean, 1e-9):.1f}x faster")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
