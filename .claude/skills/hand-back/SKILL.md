---
name: hand-back
description: Sharing the game screen with the user - lock his input while Claude drives the virtual screen, and hand mouse and keyboard control back to him the moment Claude is done (bgplay.py unlock + show), with the screen left exactly as he had it (dialogs Claude opened closed, his own screen and orders untouched, mouse parked, camera on the subject) and one line telling him it's his. The user's praise (2026-11-03) - "I really like that you give me mouse control after you're done". Use whenever Claude starts or finishes acting on a shared game screen, when the user asks to look at or click something himself, when he says "go look", and at the end of every look, test, battle replay or turn sequence on bgplay.
---

# Hand control back when done

The user (2026-11-03): "I really like that you give me mouse control after you're done, that's a really good
idea, add a skill." It came from a look at his Dominions MP turn: he asked "can you give me click access?",
later "go look, right click em"; I locked, read the unit cards, closed them, unlocked and said so.

Tools: game-ui `bgplay.py lock | unlock | locked | show` (lock = his mouse and keyboard can't reach the
virtual screen; Claude's input still works).

## While Claude works
1. `locked` first: know the state you found. If he has it unlocked he may be mid-click: only take it when he
   has said "go" (or the task is clearly mine), then `lock` so our inputs never mix.
2. Note what is on screen before the first click (his open dialog, the selected province): that is what he gets
   back. The user's open Army Setup stayed open; I only opened and closed unit cards on top of it.
3. Look-only rules of the game still apply (Dominions MP: right-click = view; no orders, no End Turn).

## When done - every time, without being asked
1. Close every window Claude opened (Exit buttons by OCR/position, never Esc where Esc opens Options).
2. Leave his own screen as found; mouse parked on a neutral spot (idle-view), camera on the subject.
3. `bgplay.py unlock` (and `show` if the window was hidden), then check `locked` says unlocked.
4. Tell him in one line: "the screen is yours" + where it is left (e.g. "back on Army Setup, nothing changed").
5. Don't touch the screen again until he hands it back ("go look", a new task) - take a fresh shot first then,
   since he may have changed things.

## When he asks for control
`unlock` + `show` at once, stop all scripts that send input (battle watchers, sweeps), say so, and wait.

## Related skills
game-ui (bgplay lock/unlock/show), idle-view (where mouse and camera rest), delegate (handing back after acting
alone), dom6-game / fog2m-guide (per-game look-only rules).
