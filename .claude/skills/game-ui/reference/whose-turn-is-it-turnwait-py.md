# game-ui - Whose turn is it? (turnwait.py)

Part of the game-ui skill; SKILL.md links here.

## Whose turn is it? (turnwait.py)
**Unreliable (the user, 2026-11-03: it "works funky" in FoG II; not yet diagnosed).** Don't trust it alone: confirm
the turn by reading the screen (a named OCR region / the game's own turn text). To do: find out why.
Turn-based games: never guess from timing alone. Find the on-screen sign of "my turn" (an End Turn
button that is replaced by an enemy-turn banner, a turn counter, a side colour) by photographing the
screen every ~1.5 s through one whole enemy turn after End Turn - then cut a reference of it.
- `turnwait.py make REF.png SHOT.png --box ...` (from a screenshot on my turn)
- `turnwait.py wait REF.png --box ... --mask ... --min 8` right after confirming End Turn (the user: assume the
  AI turn takes 5-10 s); prints MINE, then take the turn's photos. `check` = one look; `test` = score frames.
- Mask anything inside the box that changes on my turn too (turn number).
- The AI turn may move the camera: park the mouse on a fixed UI panel with no tooltip (idle-view). Not
  outside the game window: the game keeps the last hover position.
FoG II: box 1385 30 1590 115, mask 1435 42 1540 92, ref in the game folder ui/turn_mine.png.
