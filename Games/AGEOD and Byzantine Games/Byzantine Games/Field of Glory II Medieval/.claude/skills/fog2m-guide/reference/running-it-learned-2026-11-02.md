# fog2m-guide - Running it (learned 2026-11-02)

Part of the fog2m-guide skill; SKILL.md links here.

## Running it (learned 2026-11-02)
- Steam app **1368870**, Proton Experimental; window class `steam_app_1368870`.
- **Background play (normal way):** `bgplay.py start` then `bgplay.py steam 1368870` (the Steam launch
  option for it is set; see game-ui). The **Launcher** window (1000x537 at +300+226 on the 1600x990
  screen) comes first: **Play** at screen (1204, 370). Then the game window "FieldOfGloryMedieval"
  (1594x871 at +3+29). Runs with WineD3D in software; check with
  `gamecheck.py --bg --hover 812 402` (Battles button) for 30-60 s after launch.
- On the user's desktop (no flag file) it runs as normal with the GPU.
- **Popups:** the first launch showed "Field of Glory 2 will now attempt to connect to the internet"
  (OK) as its own small window before the game; later launches didn't. Expect others.
- Settings and logs: `~/.local/share/Steam/steamapps/compatdata/1368870/pfx/drive_c/users/steamuser/
  Documents/My Games/FieldOfGloryMedieval/` - `OPTIONS.TXT` (RezX/RezY, Fullscreen 0, WindowFrame 1),
  `error.log` (a startup trace even when nothing is wrong: a healthy start ends "TS: Ended").
