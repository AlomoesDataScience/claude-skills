# game-ui - Interface lessons from Field of Glory II (battle 2, 2026-11-02/03) - apply in every game

Part of the game-ui skill; SKILL.md links here.

## Interface lessons from Field of Glory II (battle 2, 2026-11-02/03) - apply in every game
- **Hover before acting.** Many games only arm an order after the pointer rests on the target (FoG II: ~1.3 s;
  the icon under the pointer - lance, red X, Move N/M - is the game's own forecast). Read that tooltip first.
- **Forecast click and commit click are separate steps.** When a game shows odds/costs on a first click and
  commits on the second, NEVER put both in one script: forecast -> report -> wait for the go -> commit
  (commit only when certain; a late "don't" can't stop a running script).
- **Don't move the camera or re-calibrate between linked clicks** (a re-snap between FoG's two charge clicks
  cancelled the order). Calibrate once, then click.
- **Read the game's own highlights** (reach area, valid squares, buttons that appear on a square) instead of
  computing reach yourself; buttons can stack (FoG: Move on top, Turn one square lower) or open sideways near
  screen edges.
- **Verify every action on the screen** (AP left, unit card, a fresh shot); an unexpected number is a problem
  to explain before the next order.
- **Popups: find their real bounds** (beige/frame rows) and the button from those; a loop must stop when the
  screen stops changing - never click a fixed point repeatedly (FoG: one combat report re-read 84 times).
- **Know the undo and cancel keys before you need them** (FoG: right-click own square -> Undo Move, only the
  last move; Space cancels a pending order; **Esc opens the game menu, not cancel**).
- **Leave the screen readable for the user**: camera on the action, mouse parked on a neutral panel (idle-view).
