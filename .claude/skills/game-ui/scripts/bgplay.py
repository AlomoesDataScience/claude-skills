#!/usr/bin/env python3
"""Play a game in the background: on a virtual X screen (Xephyr) of its own, so Claude's keys,
clicks and screenshots never touch the user's desktop, focus or keyboard.

  bgplay.py start [--size 1600x990]          start the virtual screen (a window titled "Claude game
                                              screen" appears; the user can minimise or ignore it)
  bgplay.py launch CMD [ARGS...]              start a game on it, e.g.  launch flatpak run org.develz.Crawl
  bgplay.py windows                           windows on the virtual screen (class, size, position)
  bgplay.py shot [--full]                     screenshot of the virtual screen (half size unless --full)
  bgplay.py zoom X Y W H [--scale 2]          crop of the last full shot
  bgplay.py key K [K...] | type "text" | click X Y [--right] | move X Y
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


def start(size):
    if running():
        print(f"virtual screen {DISP} already running")
        return
    log = open(os.path.join(OUT, "xephyr.log"), "w")
    subprocess.Popen(["Xephyr", DISP, "-screen", size, "-ac", "-title", "Claude game screen"],
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
        last, tick = state, tick + 1
        time.sleep(0.5)


USER_DEVICES = ("Xephyr virtual mouse", "Xephyr virtual keyboard")   # the window's input = the user's


def set_lock(on):
    """Disable/enable the Xephyr window's own input devices; Claude's input uses the XTEST devices."""
    need()
    for dev in USER_DEVICES:
        subprocess.run(["xinput", "--disable" if on else "--enable", dev], env=dict(os.environ, DISPLAY=DISP),
                       capture_output=True)
    print("locked: the user's input can't reach the virtual screen" if on else "unlocked: the user can play it too")


def is_locked():
    out = subprocess.run(["xinput", "list-props", USER_DEVICES[1]], env=dict(os.environ, DISPLAY=DISP),
                         capture_output=True, text=True).stdout
    m = re.search(r"Device Enabled \(\d+\):\s+(\d)", out)
    return bool(m and m.group(1) == "0")


def main(a):
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    c = a[0]
    if c == "start":
        unlocked = "--unlocked" in a
        a = [x for x in a if x != "--unlocked"]
        start(opt(a, "--size", "1600x990"))
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
    elif c in ("key", "type", "click", "move"):
        need()
        do(" ".join(a))
    elif c == "stop":
        subprocess.run(["pkill", "-f", f"Xephyr {DISP} "])
        print(f"stopped {DISP}")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(ARGS)
