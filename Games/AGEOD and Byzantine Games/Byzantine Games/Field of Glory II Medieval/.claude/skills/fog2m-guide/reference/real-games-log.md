# fog2m-guide - Real games log

Part of the fog2m-guide skill; SKILL.md links here.

## Real games log
### Battle 1 (2026-11-02): Anglo-Irish (Claude) vs Irish AI, Norman Invasion of Ireland 1170, attacking
- Mine: 3 Knights & Sergeants (0 C-in-C Edmund Marshall, 1 Piers FitzMaurice SG, 2 Thomas le Boteler SG;
  superior, heavily armoured, knightly lancers/swordsmen, AP 14); Sergeants (3, armoured lancers, AP 16);
  Irish Foot 4-7 (medium foot, heavy weapon; Ralf de Cogan SG); Irish Kerns 8-12 (medium foot, light
  spear, swordsmen 50%); Light Javelinmen 13-15 and Light Archers 16 (light foot, unprotected, AP 12,
  5 turns ammo); Spearmen (Defensive) 17-20 (undrilled heavy foot, protected); Welsh Longbowmen 21-22
  (bowmen, unprotected, 5 turns ammo); Ostmen 23 (undrilled heavy foot, heavy weapon).
- Theirs: Irish Kerns (9-18 seen; medium foot, lightly protected) in fenced enclosures and fields with
  woods both flanks; Noble Cavalry (0) behind.
- **Lesson (the user): don't accept the default deployment line.** I only moved the knights and kept the
  game's basic line, so troops started out of position. Next time: look at every unit and the enemy
  and the ground first, then deploy on purpose (shooters where they can reach the enemy's strong
  points, heavy foot for the assault, light troops screening, cavalry where the ground is open).
- Look at all units (Tab + read the card) and identify the enemy (hover) before giving any orders.
- **The camera follows a unit as it moves** (scrolled ~140 px after a move near the screen edge): every
  later coordinate goes stale. Re-identify units (hover) after each order; scripts/fogmove.py does
  this with --expect. A stale click moved the wrong unit once (Irish Foot 7 instead of Longbowmen 22).
- A right-click on a square with several possible orders opens big buttons: ▲ Move Unit on the
  target, blue ▲▲▲ Move Whole Command under it - left-click one. One possible order = moves at once.
- Plan to break them (turn 2): The user's read - the AI defends but will march on my formation as I come
  close and go for light units. So: form two lines (heavy-weapon foot centre, spearmen on the flanks,
  bowmen just behind and between, kerns second line), light screen that falls back before contact,
  knights + sergeants held on the open north flank. Advance to longbow range of the northern
  enclosures, shoot one kern unit at a time; when they come out of the fences, take them on the
  heavy foot and hit their flanks with the knights in the open. Then mass the heavy foot on the north
  end of their line (2 on 1) and roll it up; spearmen watch for the Noble Cavalry. Need 40% routed.
- The user's correction: **the AI only comes out if threatened by the longbows.** So the longbows are the
  trigger: form up fully out of range first (no hurry - they won't move), then step the longbows
  into range with the trap already set. Ranges (manual 12.1): foot bow/longbow short 2, long 4
  squares (half effect at long); javelins 1. Bowmen can't shoot through friends unless from higher
  ground (chequerboard gaps are fine). Average longbowmen = 100% swordsmen but unprotected; only
  light foot can pass through friends, so leave gaps for bowmen to fall back.
