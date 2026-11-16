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
  pointer in the window last clicked (a click makes its window the active one, like a window manager's focus;
  the user 2026-11-15), else the biggest viewable one. Hidden windows (a closed GTK file dialog stays listed by
  `windows`) are skipped. To send keys to a dialog window, click inside it first. Coordinates are virtual-screen pixels.
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
- **Minimising (2026-11-15).** Any new X client on the virtual screen (xrefresh, xinput, xprop,
  xdpyinfo, a shot, a click) maps Xephyr's minimised window back onto the user's desktop. Tested one by
  one; commands on `:0` (wmctrl, xwininfo) don't do it. So the keeper does nothing on `:5` while the
  window is minimised (no repaint, no lock check), and it repaints and re-locks once the window is
  back. The user can minimise it while Claude is idle. Any command Claude runs on `:5` brings it back,
  so tell him when Claude is about to work there.
- **It broke again (2026-11-16): "it's also popping in front sometimes".** The lock has failed every time
  since 2026-11-09 (`xinput --disable` returns 0 and changes nothing; cause unknown, open). The keeper
  saw "not locked" every 4 s and ran `lock` again: up to 30 tries of ~6 xinput runs each, every one a
  new client on `:5`, so a minimise was undone within a second and the window came back in front
  (re-mapping raises it; a visible window behind others is not raised, checked by stacking order).
  Fix: the keeper tries the lock once per start, never retries a failed one, never touches `:5`
  while minimised, and `lock` stops when the window is minimised mid-try. Restart the keeper (or
  `stop`/`start`) after editing bgplay.py: a running keeper keeps the old code.
- **Size is remembered (2026-11-16):** `start --size WxH` saves it in `bg5/size`; a plain `start` reuses
  it (1600x990 the first time). The user's desktop is 1920x1080, and the screen is 1920x1080 now.
- Fine for 2D games and roguelikes; 3D games get software rendering there (slow), fine when
  turn-based. Set the game to windowed at a size that fits the virtual screen (FoG II: 1600x900 in a
  1600x990 screen) through the game's own settings.
