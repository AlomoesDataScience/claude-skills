"""Monte Carlo of one Dominions 6 melee attack, using the rules in the game manual (pages 13, 60-62).

  python3 -I combat_calc.py table
      prints the chance that X + DRN beats Y + DRN for X - Y = -10..10 (manual page 13)
  python3 -I combat_calc.py melee --att 12 --def 10 --dmg 18 --prot 15 [--helm 12] [--parry 4]
          [--shield 6] [--hp 10] [--ap] [--an] [--pierce] [--slash] [--twohanded --str 12]
      --dmg is strength + weapon damage (add --twohanded --str S to get the +25% strength bonus)
      --def is the defender's defence with its shield's defence penalty already included
      --parry/--shield are the shield's parry and protection; --helm is head protection (10% of hits)
      --ap halves protection, --an ignores it, --pierce takes 15% off protection (piercing weapon),
      --slash adds 25% to damage after protection

Not modelled: fatigue, harassment, repel, size/reach limits on hit locations, resistances,
blunt head bonus, afflictions. The DRN is 2d6 where each 6 counts 5 and is rolled again.
"""
import argparse
import random

N = 200000


def drn():
    t = 0
    for _ in range(2):
        d = random.randint(1, 6)
        while d == 6:
            t += 5
            d = random.randint(1, 6)
        t += d
    return t


def melee(a):
    hits = shield_hits = kills = 0
    dmg_total = 0.0
    for _ in range(N):
        roll = a.att + drn()
        d = drn()
        if roll <= a.def_ + d:
            continue                                     # miss
        hits += 1
        shield = roll <= a.def_ + a.parry + d            # beat defence but not defence + parry
        shield_hits += shield
        prot = a.helm if (a.helm is not None and random.random() < 0.10) else a.prot
        if a.an:
            prot = 0
        elif a.ap:
            prot *= 0.5
        if a.pierce and not a.an:
            prot *= 0.85
        damage = a.dmg + (0.25 * a.str if a.twohanded else 0) + drn()
        prot_drn = drn()
        if prot_drn == 2:
            prot *= 0.75                                 # armour defeating hit
        prot_roll = prot + prot_drn + (a.shield if shield else 0)
        dealt = max(0.0, damage - prot_roll)
        if a.slash:
            dealt *= 1.25
        dmg_total += dealt
        kills += dealt >= a.hp
    print(f"hit {hits / N:.1%} (of which shield hits {shield_hits / max(1, hits):.1%}), "
          f"mean damage per attack {dmg_total / N:.2f}, per hit {dmg_total / max(1, hits):.2f}, "
          f"one-blow kill ({a.hp} hp) {kills / N:.1%}")


p = argparse.ArgumentParser()
p.add_argument("mode", choices=["table", "melee"])
p.add_argument("--att", type=float, default=10)
p.add_argument("--def", dest="def_", type=float, default=10)
p.add_argument("--parry", type=float, default=0)
p.add_argument("--shield", type=float, default=0)
p.add_argument("--dmg", type=float, default=16)
p.add_argument("--str", type=float, default=10)
p.add_argument("--prot", type=float, default=10)
p.add_argument("--helm", type=float, default=None)
p.add_argument("--hp", type=float, default=10)
for flag in ("ap", "an", "pierce", "slash", "twohanded"):
    p.add_argument("--" + flag, action="store_true")
args = p.parse_args()
if args.mode == "table":
    for diff in range(-10, 11):
        wins = sum(diff + drn() > drn() for _ in range(N))
        print(f"{diff:+3d}  {wins / N:5.1%}")
else:
    melee(args)
