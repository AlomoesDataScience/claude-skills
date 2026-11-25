# learn-to-play - Real-time strategy with pause (Paradox: Stellaris, CK, EU, HOI, Victoria)

Part of the learn-to-play skill; SKILL.md links here.

## Real-time strategy with pause (Paradox: Stellaris, CK, EU, HOI, Victoria)

The user's note (2026-11-01): Paradox games run in real time, not turns, so a single screenshot is
not enough. And his PC is weak, so they run slowly (late game worst).
- **Play pause-driven:** pause (Space), read the screen, give every order, unpause at speed 1 or 2
  for a short stretch, pause again. Pause on events too (the games can auto-pause on chosen alerts:
  set that up first). This turns them into short turns that screenshot reading can handle.
- **Watch while it runs:** a loop that captures the window every few seconds and OCRs only the
  bits that matter (date, resources, alert icons, popups), pausing when something changes. Build
  this on game-ui's ocr.py as a `watch` mode when we first play one. Keep it light, since the game
  already struggles on this machine.
- Low settings, small galaxies or maps, fewer AI empires: faster ticks and fewer popups.
