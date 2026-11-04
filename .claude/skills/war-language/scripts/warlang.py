#!/usr/bin/env python3
"""Templates for the war-language skill: translate a game turn UP into military terms, THINK at
that level, translate DOWN into game orders, and a LEXICON.md skeleton for a new game.

  warlang.py up | think | down | lexicon | all
"""
import sys

UP = """## UP - situation (game coordinates in brackets)
- Mission / end state: (victory conditions, turns left)
- Enemy (SALUTE): size / activity / location / unit types / time seen / equipment
  - their type of operation:
  - most likely COA:
  - most dangerous COA:
- Terrain (OAKOC): observation & fields of fire / avenues of approach / key terrain /
  obstacles / cover & concealment - favours whom:
- Troops: our strength, state (cohesion, ammo, commanders), relative combat power at contact:
- Time: turns left, turns per phase, culmination:
- Read-out (one line):
"""
THINK = """## THINK - plan
- Form of maneuver / defeat mechanism:
- Commander's intent: purpose / key tasks / end state
- Main effort / supporting efforts / reserve (+ commit trigger) / security (who, which flank):
- Tasks (unit: TASK target [square] SO THAT purpose):
  -
- Control measures (phase lines, objective, limit of advance - squares + turns):
- Risk vs most dangerous COA and the counter:
- Engagement / disengagement criteria:
"""
DOWN = """## DOWN - orders
| # | unit (game name) | task | action | to / target [square] | cost (AP, ammo) | check after |
|---|------------------|------|--------|----------------------|-----------------|-------------|
| 1 |                  |      |        |                      |                 |             |
Feasibility: reach / points / facing / ZOC / line of sight / range / terrain cost / command range /
enemy reach next turn / execution order keeps lanes open.
Anything infeasible -> change the plan in THINK, not silently here.

## CHECK - after the turn (and after the enemy's)
- Task purpose achieved? (one line per unit that deviated, and why)
"""
LEX = """# <Game> lexicon (war-language)
Game element <-> doctrine term. Sources: manual pages, play. Extend when new things appear.

## 1. Units -> roles
| game unit/type | arm | natural tasks | never |
|----------------|-----|---------------|-------|

## 2. Map -> terrain (OAKOC)
| terrain | observation/fire | movement (avenue/obstacle) | cover/concealment | favours |
|---------|------------------|----------------------------|-------------------|---------|

## 3. Mechanics -> effects
| game rule | doctrine effect | note |
|-----------|-----------------|------|

## 4. Victory -> end state

## 5. Control measures in this game's coordinates

## 6. Back-translation: task -> game actions
| doctrine task | game actions | cost | check after |
|---------------|--------------|------|-------------|
"""

if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    out = {"up": UP, "think": THINK, "down": DOWN, "lexicon": LEX, "all": UP + "\n" + THINK + "\n" + DOWN}.get(c)
    sys.exit(__doc__) if out is None else print(out)
