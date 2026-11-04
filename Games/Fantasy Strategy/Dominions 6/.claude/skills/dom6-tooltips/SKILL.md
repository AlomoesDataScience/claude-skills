---
name: dom6-tooltips
description: How to read the Dominions 6 user interface through tooltips and exact pointing - hover or click the centre of the word or number (not the icon beside it, not the space around it), find where a screen shows its tooltip, wait for it, and OCR it. tooltips.py hovers a list of points or on-screen texts and prints each tooltip. Uses dom6-ui (guarded input, vision.py OCR). Use whenever a screen element's meaning is unknown, a tooltip has to be read, a hover or click keeps missing, or a number or icon on a game screen needs explaining.
---

# Dom6 tooltips and exact pointing

Most of what a Dominions 6 screen means is in its tooltips. They only show when the mouse is
**on the element itself**, so every hover and click has to be aimed. The rules come from the
user, who watched misses happen (turn 6).

## Pointing rules (the user)

- **Aim at the centre of the text, vertically and horizontally.** A hover 12 px below the
  middle of a row ("too low, has to be centered") shows nothing.
- **Hover the text, not the icon.** In Army Setup the numbers (0/1, 0/10, 0/60, 1) give the
  tooltips; their icons give none.
- **Click the word, not the space between, not left or right of it** (earlier rule, for every
  button, message and menu entry).
- Take the centre from an OCR box: ((x0+x1)/2, (y0+y1)/2). **OCR merges neighbouring labels**
  ("0/1  0/10" came back as one box), so when a box holds two items, measure each item's centre
  from a screenshot instead (crop, look, compute).
- Keep every point inside the game window: the window is 1920 x 1044 here (not 1080); the guard
  refuses points outside it and stops the run.

## Reading a tooltip

1. Hover the centre and wait about **2 s** (1.5 s works most of the time).
2. Look in the right place. **Army Setup, the map and most screens put the tooltip in a bar at
   the bottom: y = height-69 .. height-12 (975-1032 in a 1044-high window).** If a new screen
   shows nothing there, take a full screenshot while hovering and look for it.
3. OCR that box (light text on dark: `V.ocr(im, [box], [True], psm=6)`).
4. Move the mouse to a resting spot inside the window (bottom-right corner) before the next
   target, so the old tooltip clears.
5. Write what the tooltip says into the screen's notes (dom6-game or dom6-knowledge `ui/`).

`scripts/tooltips.py` does steps 1-4:

    python3 -I scripts/tooltips.py "Bartholomeu" 1228,212 1296,212   # texts or X,Y centres
    python3 -I scripts/tooltips.py --shot 1234,80                     # also save full screenshots
    python3 -I scripts/tooltips.py --box 0,40,1920,90 900,500         # tooltip elsewhere

It prints `target @ (x, y): tooltip text`. A garbled result usually means the tooltip sits over
a busy background or elsewhere on screen: rerun with `--shot` and look.

## Known tooltips

Army Setup (`t`), per commander row (Apuleius the Theurg, Pythium, turn 6):
- name/portrait: the full name ("Bartholomeus the Patriarch").
- **0/1**: "can lead up to 1 squads without getting morale penalties. Bodyguard squads do not
  count against this limit."
- **0/10**: "can lead up to 10 living units".
- **0/60** (0/100 for Bartholomeus): "can lead up to 60 magic beings".
- **1** (far right): "and his units requires 1 supplies".
Army Setup header: "There are 25 units owned by Pythium in the province"; supplies available
(1227; the tip read garbled); "Units in Pythium requires 25 supplies"; "Units in Pythium have a
total siege strength of 25".

Elsewhere (from dom6-game and dom6-knowledge): unit-screen path symbols ("fire mage level 1"),
top-bar resources, recruitment portraits. Add new screens here as they are read.

## Standards (audit 2026-11-03)
- **Screen:** coordinates here were measured on the 1920x1044 desktop. On Claude's 1912x1000 virtual screen (dom6bg.py / bgplay) find positions by OCR or re-measure - never reuse a stale coordinate (memory: apply tools universally).
- **Where it runs:** prefer Claude's virtual screen (dom6-ui bgplay, dom6bg.py); lock while working, hand back after (hand-back).
- **MP games (the user's):** look only - right-click views, hovers; no orders, recruits, research, transfers or End Turn.

## Related skills
dom6-ui, dom6-game, dom6-knowledge, game-ui.
Also (2026-11-03): dom6-abilities, dom6-game.
