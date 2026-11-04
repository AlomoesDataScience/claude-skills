---
name: dom6-morale
description: Morale and rout in Dominions 6, from the manual (pp. 59, 69-71) and illwiki - squad morale (average of the squad), the morale check (squad morale + DRN + survivor bonus 0-5 vs 14 + DRN), what triggers checks (heavy losses, four or fewer left, fear, army below 50% HP every round), army rout at 75% HP lost (mounts, PD and slaves count less), morale modifiers (leadership stars +1/+2/+3, inspirational, standards, home province, dominion, blessing, sparse/skirmish -1, undead/demon squadmates -1), the magic morale bonus (-10 to +1; Sermon of Courage and Fanaticism +1, fear and frighten), fear auras and dread, awe, repel and morale, mindless and magic-being leadership, berserkers, rout effects and where routers end up, turn-routs at rounds 150/170. Use when planning squads and commanders, judging whether an army will hold, choosing morale spells or fear, reading a rout in a battle log, or when the user asks about morale or routing.
---

# Morale and rout (Dominions 6, vanilla)

The user's list (2026-11-03). Manual pp.69-71; illwiki `morale`, `rout`, `fear`, `awe`, `inspirational`,
`berserker`. Troban (2026-11-03) was lost to an ARMY rout in round 11 - morale decides most battles.

## Squad morale
- Checked per SQUAD: the average morale of its members, with modifiers (p.69):
  - Leadership (wiki): commander leadership 200+ = +3, 150-199 = +2, 100-149 = +1, 50-99 = 0, under 50 = -1;
    modified by formation and squads led (dom6-tactics: past the squad allowance squads lose morale).
  - Inspirational +/-N (commander); Standard in the squad +x (highest only).
  - +1 home province (where recruited), +1 in friendly dominion, +1 blessed (sacreds).
  - -1 sparse line / skirmish; -1 with undead or demons in the squad (for the living).
- **Magic morale bonus** (p.69): -10 to +1. Sermon of Courage and Fanaticism: +1 (cap +1); fear lowers it;
  a negative bonus recovers ~1 per 2 rounds; a positive one lasts the battle. Sermon is +1 morale for the
  army (or one point of fear undone) - useful, not decisive.

## The check (p.70)
Morale roll: squad morale + DRN + survivor bonus (0-5: 5 near intact, 0 nearly wiped out; wiki: 5 x share alive)
vs fear roll 14 + DRN. Morale wins ties (wiki). Squad morale 10 intact (15 effective) holds ~85%; at half
strength (12.5) ~38%... use the dom6-drn table on (morale + bonus - 14).

## What triggers a check (p.69-70; max once a round per squad)
- Heavy losses: since the last check, wounds >= half the squad's members (a "wound" = damage while at or
  under 80% HP), and the squad has lost >= 20%.
- Four or fewer members left and one was hurt this round.
- Near a Fear monster; hit by a Fear spell (Frighten doesn't force checks).
- **Army below 50% of its total HP: every squad checks every round.**
- **Army at 75% HP lost: the whole army routs** (p.70). Mounts and province defence count 25%, slaves 50%,
  battle summons don't count if the army is one commander + retinue (wiki).

## Fear, dread, awe
- Fear (aura or spell): lowers morale (up to its value, max 10 under base) and forces a check; units flashed may
  rout individually (easy check ~6, wiki). Fear aura +0 = fear roll base 10, +5 = 11, +10 = 12 (wiki).
- Frighten: up to -5, no forced check. Dread (Glamour): fear that True Sight/Spirit Sight ignore.
- Awe +N: each attacker rolls morale + DRN vs 10 + N + DRN or loses that attack (individual) - stops trample
  too. Mindless and blind ignore it. (dom6-weapons for repel, which also uses morale.)

## Who doesn't rout
Mindless (morale 50): dissolve without a commander that can lead them (33% a round) (p.70). Berserk units
(morale 99, can't cast spells, once per battle). Magic beings need magic leadership, undead and demons undead
leadership - without it they rout (p.70).

## Rout effects (p.70; wiki)
Routers run for their edge at -4 defence; off the map they end up next door (dom6 retreat rules p.72; to an
enemy province = destroyed); bleeding/poison finish off-screen. Units of a winning army can rout too.
Round 100 twilight (enchantments end), 150 attackers with morale <= 50 rout, 170 defenders, 200 everyone dies.

## Using it
- Big squads hold longer (survivor bonus, heavy-loss threshold); keep squads under one good leader within
  his squad allowance; a Standard in key squads; fight at home and in your dominion.
- High-morale anchors (Tuatha) where the shock lands; low-morale chaff where it doesn't.
- Break THEM: concentrate damage on one squad per round (heavy-loss checks), fear, kill 25% of army HP fast
  to reach the 50% rolling-check zone. A high-HP pretender counts for a lot of army HP (Ghost Moose 145).
- Troban lesson: our army hit the 50% line and rolled checks every round until it broke - more HP in the army
  (bigger army, healthier start) and armour/skins to slow the HP loss are the real fixes; Sermon helps +1.

## Related skills
dom6-drn, dom6-tactics (leadership and squads, formations), dom6-mounts, dom6-weapons (repel), dom6-fatigue,
dom6-battle-view (rout in logs), dom6-mechanics.
