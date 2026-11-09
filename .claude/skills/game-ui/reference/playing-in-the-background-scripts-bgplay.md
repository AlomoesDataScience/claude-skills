# game-ui - Playing in the background (`scripts/bgplay.py`)

Part of the game-ui skill; SKILL.md links here.

## Playing in the background (`scripts/bgplay.py`)

The user's ask (2026-11-01): play without taking over his desktop. `bgplay.py` runs a game on its own
virtual X screen (Xephyr, display :5): Claude's keys, clicks and screenshots go there only, so no
focus stealing, no idle wait, and nothing he types reaches the game.

```
bgplay.py start                      # virtual screen + "Claude game screen" window; locked by default
bgplay.py launch flatpak run org.develz.Crawl
bgplay.py steam 1368870              # a Steam game onto the virtual screen (launch option needed, below)
bgplay.py windows | shot [--full] | zoom X Y W H
bgplay.py seq "key o" "wait 2500" "type abc" "click 400 300" "shot --full"
bgplay.py lock | unlock | locked     # lock: The user's mouse/keyboard can't touch the game (he can watch)
bgplay.py stop
```

- Lock = the Xephyr window's own mouse and keyboard devices disabled (`xinput`); Claude's input
  uses the XTEST devices, so it still works. `unlock` lets the user play along; toggle any time.
  Locked is the default and must hold (the user, 2026-11-02, "I have access"): the first lock right
  after `start` used to fail silently; now `lock` retries until both devices are off, writes
  `~/.cache/game-ui/bg5/locked`, and the keeper re-locks within 4 s if anything re-enables them.
- No window manager on the screen: keys go to the window under the pointer, so bgplay parks the
  pointer on the biggest window before keys. Coordinates are virtual-screen pixels.
- **Steam games** (2026-11-02, FoG II Medieval): Steam starts the game itself, so the game needs this
  Steam launch option (Properties > General > Launch Options; open it with
  `steam steam://gameproperties/APPID`, type it with gameui, then check the box's start and end):
  `env $(cat "$HOME/.cache/game-ui/steam-env" 2>/dev/null) %command%`
  No file = the game runs on the user's screen as always. `bgplay.py steam APPID` writes
  `DISPLAY=:5 PROTON_USE_WINED3D=1` there, starts the game, and removes the file when the first
  window appears (children of the launcher inherit it).
- **Why WineD3D:** Xephyr has no DRI3, so Vulkan can't present ("Could not find both graphics and
  present queues"); DXVK games crash right after loading (FoG II died at "TS: UILoaded"). With
  `PROTON_USE_WINED3D=1` Proton draws through OpenGL on llvmpipe: software, slow, fine for turn-based
  games. `start --glamor` does not help. No gamescope installed.
- Other Proton/umu games launched outside bgplay still open on the real desktop.
- `show` brings the window back; a keeper (started with `start`) repaints it, since with xfwm4's
  compositor Xephyr shows what was behind it after being hidden.
- Fine for 2D games and roguelikes; 3D games get software rendering there (slow), fine when
  turn-based. Set the game to windowed at a size that fits the virtual screen (FoG II: 1600x900 in a
  1600x990 screen) through the game's own settings.
