"""Example scorer for gamedb.py: units judged by a simulated melee trade against a reference unit, per gold.
Shows the pattern: purpose() says what a row is for; score() returns value, cost, basis and a detail."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "unit-combat-math", "scripts"))
sys.argv = [sys.argv[0]]                      # unitcombat reads options from argv at import
import unitcombat as uc                        # noqa: E402

REF = uc.unit("att=10,def=9,dmg=13,prot=15,hp=11")   # the "Heavy Infantry" everyone is measured against
CURATED = {"Knight": "S"}                     # hand tiers win where they disagree


def purpose(r):
    return {"missile": "ranged troops", "cavalry": "shock troops", "monster": "monsters"}.get(r["role"], "line infantry")


def score(r):
    u = uc.unit(",".join(f"{k}={r[k]}" for k in ("att", "def", "dmg", "prot", "hp", "attacks")))
    kill = uc.rounds_to_kill(u, REF, n=600)[0]          # rounds for this unit to kill one reference man
    die = uc.rounds_to_kill(REF, u, n=600)[0]           # rounds for one reference man to kill it
    value = die / kill                                  # reference men killed before it dies (trade)
    return {"value": value, "cost": float(r["gold"]), "basis": "simulated",
            "detail": f"kills one HI in {kill:.1f} rounds, dies in {die:.1f}"}
