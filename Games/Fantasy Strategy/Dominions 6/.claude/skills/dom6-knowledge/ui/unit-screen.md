# Unit stat screen

Right-click a unit's sprite (nation info screen, recruit lists, armies) to open it. Picture: ui/img/unit_screen_black_knight.png (Ulm's Black Knight). What each popup shows: ui/unit-popups.md.

## How to open

- Right-click on the sprite's own pixels in the nation info screen's Commanders/Units rows; it opens over the info screen. Exit button at the bottom. *(game screen, 2026-10-26)*

## Layout

- Title tab with the unit's name. Under it a tab row: the unit and, for mounted units, its mount (Black Knight | Black Destrier); the selected tab is highlighted. *(game screen, 2026-10-26)*
- Three stat columns with an icon before each label. Left: Gold, Hit points, Size (3(5) = size 3, the mount's 5 used for space), Protection, Magic Resistance, Morale. Middle: Resources, Strength, Attack Skill, Defence Skill, Precision, Combat Speed. Right: Recruitment points, Map Move, Encumbrance, Fatigue, Age, XP. The unit's sprite at the right. *(game screen, 2026-10-26)*
- Below the stats a row of ability icons (not every unit has them). Right-click one to see its name, value and what it does; see unit-popups.md. The Black Knight has one: Skilled Rider. *(game screen, 2026-10-26)*
- Weapon table on parchment: Weapon, Len, Att, Dmg (damage-type icons, then weapon damage + Strength), and Armor table: Armor, Prt, Def, Par, Enc. A '#' before a weapon name (# Lance): right-clicking it opens the Lance popup; meaning not confirmed (guess: the once-per-battle charge weapon). *(game screen, 2026-10-26)*
- Then the unit's description text, then Exit. *(game screen, 2026-10-26)*

## Black Knight (Ulm, MA)

- Gold 60, HP 15, Size 3(5), Prot 23, MR 9, Morale 14, Res 72, Str 13, Att 12, Def 13, Prec 8, Combat Speed 20, Rec points 51, Map Move 16, Enc 6, Fatigue 0, Age 27, XP 0. Lance len 3 att 13 dmg 19; Morningstar len 1 att 13 dmg 19. Full Plate of Ulm 23/-3/-/4, Full Helmet of Ulm 23/-1/-/0, Kite Shield of Ulm 22/-2/6/2. *(game screen, 2026-10-26)*

## Reading it

- vision.py scene reads labels and numbers cleanly (score <0.1); the last table row can merge into one line, and the small icons are not read - crop and right-click them. *(Claude, 2026-10-26)*

## Mounts

- A mounted unit's stat screen has two tabs: the rider (Black Knight) and the mount (Black Destrier); clicking the mount's tab swaps the screen to the horse's own stats. *(user, 2026-10-26)*
- The mount's tab has the same layout: its own stats, weapon (Hoof) and barding; no ability icons for the Black Destrier. The rider screen's Combat Speed (20) and Map Move mounted (16) come from the mount. *(game screen, 2026-10-26)*

## Ability icons

- Rider-on-horse icon below Morale (Black Knight) = Skilled Rider. *(user, 2026-10-26)*

## What can be right-clicked

- Most things in the top box (the stat labels), the ability icons, every weapon and every armour line. The description is not clickable. *(user, 2026-10-26)*

## Weapon table

- The '#' in front of a weapon name (# Lance): meaning unknown, the user does not know either. *(user, 2026-10-26)*

## Items

- Commanders can hold gear (magic items). Promoting a unit to commander technically gives it the same capability; rarely matters, since such units usually have better commander versions or differ only in weapons and armour. *(user, 2026-10-26)*
