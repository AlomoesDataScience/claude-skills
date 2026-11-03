#!/usr/bin/env python3
"""Play a game in the background: on a virtual X screen (Xephyr) of its own, so Claude's keys,
clicks and screenshots never touch the user's desktop, focus or keyboard.

  bgplay.py start [--size 1600x990]          start the virtual screen (a window titled "Claude game
                                              screen" appears; the user can minimise or ignore it)
  bgplay.py launch CMD [ARGS...]              start a game on it, e.g.  launch flatpak run org.develz.Crawl
  bgplay.py steam APPID [--wait 180] [--env K=V ...]
                                              start a Steam game on it. Steam starts games itself, so the
                                              game's Steam launch option (Properties > General > Launch
                                              Options) must read the env file:
      env $(cat "$HOME/.cache/game-ui/steam-env" 2>/dev/null) %command%
                                              Without the file the game runs on the user's screen as
                                              usual. The file gets DISPLAY=<this screen> and
                                              PROTON_USE_WINED3D=1 (Xephyr has no DRI3: Vulkan/DXVK can't
                                              show here, so Proton draws with OpenGL, in software:
                                              slow but fine for turn-based games), plus any --env; it is
                                              removed once a window shows up here (or after --wait).
                                              With VirtualGL installed (/opt/VirtualGL) the file also gets
                                              LD_PRELOAD=<its 64+32-bit fakers> VGL_DISPLAY=egl: OpenGL is
                                              drawn on the real GPU (--nogpu: software only)
  start --glamor                              Xephyr's glamor drawing (2D only; it does NOT give the
                                              game DRI3 or Vulkan - tested with FoG II, 2026-11-02)
  bgplay.py waitchange [--timeout 180] [--every 3] [--nosettle]
                                              wait for the whole screen to change, then hold still
                                              (loading screens, turn changes); ends with a shot.
                                              Use with mark:  seq "mark" "click X Y" "waitchange"
                                              (mark = the screen before the action, so a fast
                                              change can't happen before the polling starts)
  bgplay.py windows                           windows on the virtual screen (class, size, position)
  bgplay.py shot [--full]                     screenshot of the virtual screen (half size unless --full)
  bgplay.py zoom X Y W H [--scale 2]          crop of the last full shot
  bgplay.py key K [K...] | type "text" | click X Y [--right] | move X Y | scroll up|down N [X Y] | hold KEY MS | drag X1 Y1 X2 Y2 [--right] [--slow]
  bgplay.py seq "key o" "wait 800" "type abc" "click 400 300" "shot"
  bgplay.py read [REGION|X0 Y0 X1 Y1]...      text of screen regions by OCR (cheaper and faster than a
                                              screenshot); named regions come from the game folder's
                                              .claude/game-ui.json "regions" (found from the current folder)
  in seq: "read msg stats" reads after the steps before it; "fast" drops the pauses between keys
  bgplay.py lock | unlock | locked            lock = the user's mouse and keyboard can't reach the game
                                              through the window (Claude's input still works); unlock =
                                              the user can play it too. `start` locks (--unlocked: don't)
  bgplay.py show                              bring the "Claude game screen" window back on the user's
                                              desktop and repaint it (it can come back blank)
  bgplay.py keeper                            (started by `start`) repaints the game whenever the window
                                              reappears and every 4 s: with a compositor Xephyr loses its
                                              picture while hidden and shows what was behind it
  bgplay.py stop                              close the virtual screen (and every game on it)

Options: --display :5 (default; env BG_DISPLAY). Coordinates are virtual-screen pixels (the full
screenshot's). No idle guard is needed: nothing the user does reaches this screen, and nothing
sent here reaches theirs. Screenshots go to ~/.cache/game-ui/bg<display>/.
Needs Xephyr (package xserver-xephyr). A game that needs real 3D acceleration may run slowly or not
at all on Xephyr (software rendering); 2D games and roguelikes are fine.
"""
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))


def opt(a, name, default=None):
    if name in a:
        i = a.index(name)
        v = a[i + 1]
        del a[i:i + 2]
        return v
    return default


ARGS = sys.argv[1:]
DISP = opt(ARGS, "--display", os.environ.get("BG_DISPLAY", ":5"))
NUM = DISP.lstrip(":").split(".")[0]
SOCK = f"/tmp/.X11-unix/X{NUM}"
HOST = os.environ.get("DISPLAY", ":0")             # the user's desktop
os.environ["DISPLAY"] = DISP                      # gameui's X input goes to the virtual screen
os.environ.setdefault("UI_WMCLASS", f"bg{NUM}")   # only names the shot folder here
sys.path.insert(0, HERE)
import gameui as U                                 # noqa: E402  (after DISPLAY is set)
from PIL import ImageGrab                          # noqa: E402

OUT = os.path.join(U.CACHE, f"bg{NUM}")
os.makedirs(OUT, exist_ok=True)


def running():
    return os.path.exists(SOCK)


def need():
    if not running():
        sys.exit(f"no virtual screen on {DISP}: run  bgplay.py start")


def start(size, glamor=False):
    if running():
        print(f"virtual screen {DISP} already running")
        return
    log = open(os.path.join(OUT, "xephyr.log"), "w")
    subprocess.Popen(["Xephyr", DISP, "-screen", size, "-ac", "-title", "Claude game screen"]
                     + (["-glamor"] if glamor else []),
                     stdout=log, stderr=log, start_new_session=True, env=dict(os.environ, DISPLAY=HOST))
    for _ in range(50):
        if running():
            print(f"virtual screen {DISP} started ({size})")
            return
        time.sleep(0.1)
    sys.exit("Xephyr did not start (see " + os.path.join(OUT, "xephyr.log") + ")")


def launch(cmd):
    need()
    log = open(os.path.join(OUT, "game.log"), "w")
    env = dict(os.environ, DISPLAY=DISP)
    p = subprocess.Popen(cmd, stdout=log, stderr=log, env=env, start_new_session=True)
    print(f"started pid {p.pid} on {DISP}: {' '.join(cmd)}")


def windows():
    need()
    out = subprocess.run(["xwininfo", "-display", DISP, "-root", "-tree"], capture_output=True, text=True).stdout
    rows = []
    for m in re.finditer(r'(0x[0-9a-f]+) "([^"]*)": \("([^"]*)" "[^"]*"\)\s+(\d+)x(\d+)\+(-?\d+)\+(-?\d+)', out):
        wid, title, cls, w, h, x, y = m.groups()
        if int(w) > 50 and int(h) > 50:
            rows.append((wid, title, cls, int(w), int(h), int(x), int(y)))
    return rows


def shot(full=False):
    need()
    im = ImageGrab.grab(xdisplay=DISP)
    im.save(os.path.join(OUT, "last_full.png"))
    if not full:
        im = im.resize((im.width // 2, im.height // 2))
    p = os.path.join(OUT, f"shot_{time.strftime('%H%M%S')}_{int(time.time() * 1000) % 1000:03d}.png")
    im.save(p)
    print(p)


MARK = os.path.join(OUT, "mark.png")


def thumb():
    return ImageGrab.grab(xdisplay=DISP).convert("L").resize((160, 99))


def mark():
    """Remember the screen BEFORE an action, so waitchange can't miss a change that happens before
    it starts polling (the user: "make sure it didn't just load faster than you set up your polling")."""
    need()
    thumb().save(MARK)


def waitchange(timeout=180, every=3.0, settle=True):
    """Wait until the whole screen differs from the mark (or from now, without a mark), then until
    it holds still for one interval. The first check is immediate, so a change that already
    happened counts. A heartbeat every ~30 s shows the poll is alive and the difference so far.
    Ends with a half-size shot. Small-thumbnail comparison: a moving pointer doesn't count."""
    from PIL import Image, ImageChops, ImageStat
    need()

    def diff(a, b):
        """Whole-screen mean difference, raised when a small patch changes a lot (one unit moving,
        a small popup): the mean alone missed a single FoG II unit's move (2026-11-02). 40+ grey
        levels on 0.25% of the thumbnail pixels (~40 px) counts as a change on its own."""
        d = ImageChops.difference(a, b)
        big = sum(d.histogram()[40:]) / (d.width * d.height)
        return max(ImageStat.Stat(d).mean[0], 7.0 if big > 0.0025 else 0.0)

    t0 = time.time()
    if os.path.exists(MARK):
        base = Image.open(MARK).convert("L")
        os.remove(MARK)             # one mark per wait
        print("comparing with the mark taken before the action", flush=True)
    else:
        base = thumb()
        print("no mark: comparing with the screen as it is now", flush=True)
    prev, changed, beat, first = base, False, t0, True
    while time.time() - t0 < timeout:
        if not first:
            time.sleep(every)
        first = False
        cur = thumb()
        if time.time() - beat > 30:
            beat = time.time()
            print(f"  ...polling, {time.time() - t0:.0f} s, difference {diff(cur, base):.1f} (change = 6)", flush=True)
        if not changed and diff(cur, base) > 6:
            changed = True
            print(f"changed after {time.time() - t0:.0f} s", flush=True)
            if not settle:
                break
        elif changed and diff(cur, prev) < 1.5:
            print(f"settled after {time.time() - t0:.0f} s", flush=True)
            break
        prev = cur
    else:
        print(f"{'still changing' if changed else 'NO CHANGE'} after {timeout} s", flush=True)
    shot()


def zoom(x, y, w, h, scale=2):
    from PIL import Image
    im = Image.open(os.path.join(OUT, "last_full.png")).crop((x, y, x + w, y + h))
    im = im.resize((w * scale, h * scale))
    p = os.path.join(OUT, f"zoom_{time.strftime('%H%M%S')}.png")
    im.save(p)
    print(p)


def root_geo():
    im = ImageGrab.grab(xdisplay=DISP)
    return (0, 0, im.width, im.height, True)


def point_at_game():
    """Without a window manager, keys go to the window under the pointer: park it in the biggest window's top-right corner."""
    ws = windows()
    if ws:
        wid, title, cls, w, h, x, y = max(ws, key=lambda r: r[3] * r[4])
        U.move(root_geo(), x + w - 3, y + 3)     # top-right corner: no hover tooltips over map or messages


def _profile():
    import json
    d = os.getcwd()
    while True:
        f = os.path.join(d, ".claude", "game-ui.json")
        if os.path.isfile(f):
            try:
                return json.load(open(f))
            except ValueError:
                return {}
        if os.path.dirname(d) == d:
            return {}
        d = os.path.dirname(d)


def read(names):
    """OCR named regions (game-ui.json "regions": {"msg": [x0, y0, x1, y1, "dark"?]}) or raw boxes."""
    need()
    import ocr as O
    prof = _profile()
    regions = prof.get("regions", {})
    im = ImageGrab.grab(xdisplay=DISP)
    im.save(os.path.join(OUT, "last_full.png"))
    i = 0
    while i < len(names):
        n = names[i]
        if n in regions:
            box, dark = regions[n][:4], "dark" in regions[n][4:]
            i += 1
        elif n.lstrip("-").isdigit():
            box, dark, n = [int(v) for v in names[i:i + 4]], True, "box"
            i += 4
        else:
            sys.exit(f"unknown region {n!r} (known: {', '.join(regions) or 'none - add them to .claude/game-ui.json'})")
        txt = O.ocr(O.prepare(im, tuple(box), scale=2, dark=dark), psm=6).strip()
        print(f"[{n}]\n{txt}")
        if prof.get("tracker"):
            feed_tracker(prof["tracker"], n, txt)


def feed_tracker(hooks, region, text):
    """Stream-panel hook: fill tracker fields from this read (game-ui.json "tracker" block)."""
    try:
        sys.path.insert(0, os.path.join(HERE, "..", "..", "stream-panel", "scripts"))
        import tracker
        tracker.apply_hooks(hooks, region, text)
    except Exception as e:                     # the panel is optional; never break a read
        print(f"(tracker hook skipped: {e})", file=sys.stderr)


KEY_GAP = [0.03]


def do(step):
    p = step.split()
    c = p[0]
    if c == "mark":
        mark()
        return
    if c == "waitchange":
        waitchange(int(p[1]) if len(p) > 1 and p[1].isdigit() else 180)
        return
    if c == "wait":
        time.sleep(int(p[1]) / 1000)
    elif c == "shot":
        shot("--full" in p)
    elif c == "read":
        read(p[1:])
    elif c == "fast":
        KEY_GAP[0] = 0.005
    elif c == "key":
        point_at_game()
        for k in p[1:]:
            U.key(k)
            time.sleep(KEY_GAP[0])
    elif c == "type":
        point_at_game()
        U.type_text(step.split(" ", 1)[1].strip('"'))
    elif c == "hold":             # hold KEY[+KEY..] MS: keys down for MS ms (camera keys that act while held;
        point_at_game()           # combos like Shift_L+Up press left to right, release in reverse)
        kcs = [U.keycode(k)[0] for k in p[1].split("+")]
        for kc in kcs:
            U.XTST.XTestFakeKeyEvent(U.dpy(), kc, 1, 0)
            U.X11.XFlush(U.dpy())
            time.sleep(0.03)
        time.sleep(int(p[2]) / 1000 if len(p) > 2 else 0.5)
        for kc in reversed(kcs):
            U.XTST.XTestFakeKeyEvent(U.dpy(), kc, 0, 0)
            U.X11.XFlush(U.dpy())
    elif c == "scroll":           # scroll up|down N [X Y]: wheel clicks, at X Y if given
        geo = root_geo()
        if len(p) >= 5:
            U.move(geo, int(p[3]), int(p[4]))
        for _ in range(int(p[2]) if len(p) > 2 else 1):
            U.button(4 if p[1] == "up" else 5, True)
            U.button(4 if p[1] == "up" else 5, False)
            time.sleep(0.05)
    elif c == "drag":             # drag X1 Y1 X2 Y2 [--right] [--slow]: press, glide, release (deployment drags)
        geo = root_geo()
        U.drag(geo, int(p[1]), int(p[2]), int(p[3]), int(p[4]), right="--right" in p, slow="--slow" in p)
    elif c in ("click", "move"):
        geo = root_geo()
        x, y = int(p[1]), int(p[2])
        if c == "move":
            U.move(geo, x, y)
        else:
            U.click(geo, x, y, right="--right" in p)
    else:
        sys.exit(f"unknown step {step!r}")


TITLE = "Claude game screen"


def host_window():
    out = subprocess.run(["wmctrl", "-l"], env=dict(os.environ, DISPLAY=HOST), capture_output=True, text=True).stdout
    for line in out.splitlines():
        if line.endswith(TITLE):
            return line.split()[0]
    return None


def repaint():
    subprocess.run(["xrefresh", "-display", DISP, "-none"], capture_output=True)


def show():
    need()
    wid = host_window()
    if wid:
        env = dict(os.environ, DISPLAY=HOST)
        subprocess.run(["wmctrl", "-i", "-R", wid], env=env)
        subprocess.run(["wmctrl", "-i", "-r", wid, "-e", "0,160,45,-1,-1"], env=env)
        time.sleep(0.5)
    repaint()
    print("shown and repainted" if wid else "no game screen window found; repainted anyway")


def keeper():
    """Repaint on hidden->visible and every 4 s while the virtual screen lives."""
    last, tick = None, 0
    while running():
        wid = host_window()
        state = None
        if wid:
            info = subprocess.run(["xwininfo", "-display", HOST, "-id", wid], capture_output=True, text=True).stdout
            state = "IsViewable" in info
        if (state and last is False) or tick % 8 == 0:
            repaint()
        if tick % 8 == 4 and os.path.exists(LOCK_FILE) and not is_locked():
            set_lock(True, quiet=True)          # something re-enabled the user's devices: lock again
        last, tick = state, tick + 1
        time.sleep(0.5)


USER_DEVICES = ("Xephyr virtual mouse", "Xephyr virtual keyboard")   # the window's input = the user's


LOCK_FILE = os.path.join(OUT, "locked")   # the wish to be locked; the keeper re-applies it


def set_lock(on, quiet=False):
    """Disable/enable the Xephyr window's own input devices; Claude's input uses the XTEST devices.
    Retries until it holds (right after `start` the devices may not exist yet: the first lock used
    to fail silently and leave the screen open to the user)."""
    need()
    if on:
        open(LOCK_FILE, "w").close()
    elif os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
    for _ in range(30):
        for dev in USER_DEVICES:
            subprocess.run(["xinput", "--disable" if on else "--enable", dev], env=dict(os.environ, DISPLAY=DISP),
                           capture_output=True)
        if is_locked() == on:
            break
        time.sleep(0.2)
    else:
        print(f"WARNING: could not {'lock' if on else 'unlock'} the virtual screen")
        return
    if not quiet:
        print("locked: the user's input can't reach the virtual screen" if on else "unlocked: the user can play it too")


def is_locked():
    """True only when BOTH the window's mouse and keyboard are disabled."""
    for dev in USER_DEVICES:
        out = subprocess.run(["xinput", "list-props", dev], env=dict(os.environ, DISPLAY=DISP),
                             capture_output=True, text=True).stdout
        m = re.search(r"Device Enabled \(\d+\):\s+(\d)", out)
        if not (m and m.group(1) == "0"):
            return False
    return True


STEAM_FLAG = os.path.expanduser("~/.cache/game-ui/steam-env")


# libXv first: the fakers need it and Steam's runtime container (sniper) doesn't ship it - without it
# every process in the launch dies "libXv.so.1: cannot open shared object file" (2026-11-02)
VGL_LIBS = ["/usr/lib/x86_64-linux-gnu/libXv.so.1", "/usr/lib/i386-linux-gnu/libXv.so.1",
            "/usr/lib/libdlfaker.so", "/usr/lib/libvglfaker.so",          # 64-bit processes
            "/usr/lib32/libdlfaker.so", "/usr/lib32/libvglfaker.so"]      # 32-bit ones (virtualgl32)


def vgl_env():
    """VirtualGL (the user installed it 2026-11-02): GL drawn on the real GPU through EGL, the picture
    copied to this screen. What `vglrun -d egl` sets, as env vars, because Steam games run inside
    Steam's runtime container where a wrapper can't go; absolute LD_PRELOAD paths are mapped in by
    the container (as for the Steam overlay), and each process skips the library of the other
    bitness. Empty if VirtualGL isn't installed."""
    have = [p for p in VGL_LIBS if os.path.exists(p)]
    if not have:
        return []
    if len(have) < len(VGL_LIBS):
        print("note: VirtualGL is missing " + ", ".join(sorted(set(VGL_LIBS) - set(have)))
              + " (32-bit games need the virtualgl32 package)")
    # GLX back end on the real display by default: FoG II's battle view under the EGL back end drew
    # only text (no textures) and crashed with shadows on; GLX mode (off-screen buffers on the user's
    # X server, nothing shown there) is VirtualGL's mature path. The container passes X auth only for
    # DISPLAY, so this relies on the real server allowing the user (xhost SI:localuser:<user>).
    # BGPLAY_VGL=egl to use EGL instead.
    real = os.environ.get("BGPLAY_REAL_DISPLAY") or os.environ.get("DISPLAY", ":0")
    if real.split(".")[0] == DISP:
        real = ":0"
    back = os.environ.get("BGPLAY_VGL", real.split(".")[0])
    return ["LD_PRELOAD=" + ":".join(have), f"VGL_DISPLAY={back}"]


def steam(appid, wait, extra=(), gpu=True):
    """Start a Steam game on the virtual screen via the launch-option flag file (see the docstring)."""
    need()
    before = {r[0] for r in windows()}
    os.makedirs(os.path.dirname(STEAM_FLAG), exist_ok=True)
    # VideoMemorySize: WineD3D guesses video memory from the card it names (here an old "Radeon HD 5600")
    # and FoG II's battle ran out: 6783 "Out of adapter memory" in the Proton log, black battle screen,
    # crash with shadows on (2026-11-02). An env var, so the Wine prefix stays untouched.
    env = [f"DISPLAY={DISP}", "PROTON_USE_WINED3D=1", "WINE_D3D_CONFIG=VideoMemorySize=2048",
           *(vgl_env() if gpu else []), *extra]
    print("env: " + " ".join(env))
    open(STEAM_FLAG, "w").write(" ".join(env) + "\n")
    try:
        subprocess.Popen(["steam", f"steam://rungameid/{appid}"], stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, start_new_session=True)
        t0 = time.time()
        while time.time() - t0 < wait:
            new = [r for r in windows() if r[0] not in before]
            if new:
                for r in new:
                    print(f"window here: {r[2]} {r[3]}x{r[4]}  {r[1]}")
                return
            time.sleep(2)
        print(f"no window on {DISP} after {wait} s: is the launch option set? (bgplay.py --help)")
    finally:
        try:
            os.remove(STEAM_FLAG)
        except OSError:
            pass


def main(a):
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    c = a[0]
    if c == "start":
        unlocked = "--unlocked" in a
        a = [x for x in a if x != "--unlocked"]
        start(opt(a, "--size", "1600x990"), glamor="--glamor" in a)
        if not unlocked:
            set_lock(True)
        subprocess.Popen([sys.executable, "-I", os.path.abspath(__file__), "--display", DISP, "keeper"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    elif c == "show":
        show()
    elif c == "keeper":
        keeper()
    elif c in ("lock", "unlock"):
        set_lock(c == "lock")
    elif c == "locked":
        need()
        print("locked" if is_locked() else "unlocked")
    elif c == "launch":
        launch(a[1:])
    elif c == "steam":
        extra = [a[i + 1] for i, x in enumerate(a) if x == "--env" and i + 1 < len(a)]
        steam(a[1], int(opt(a, "--wait", "180")), extra, gpu="--nogpu" not in a)
    elif c == "mark":
        mark()
    elif c == "waitchange":
        waitchange(int(opt(a, "--timeout", "180")), float(opt(a, "--every", "3")), "--nosettle" not in a)
    elif c == "windows":
        for r in windows():
            print(f"{r[0]}  {r[2]:<16} {r[3]}x{r[4]}+{r[5]}+{r[6]}  {r[1]}")
    elif c == "shot":
        shot("--full" in a)
    elif c == "zoom":
        sc = int(opt(a, "--scale", "2"))
        zoom(*map(int, a[1:5]), scale=sc)
    elif c == "seq":
        need()
        for s in a[1:]:
            do(s)
    elif c == "read":
        read(a[1:])
    elif c in ("key", "type", "click", "move", "scroll", "hold", "drag"):
        need()
        do(" ".join(a))
    elif c == "stop":
        subprocess.run(["pkill", "-f", f"Xephyr {DISP} "])
        print(f"stopped {DISP}")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(ARGS)
