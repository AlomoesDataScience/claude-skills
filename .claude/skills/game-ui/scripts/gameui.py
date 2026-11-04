"""Drive a running game window on X11 (any app: UI_WMCLASS / UI_WMTITLE, required): screenshots of the game window only, mouse clicks
and key presses through XTest (libXtst via ctypes, no xdotool or pip needed).

  python3 -I gameui.py find                      window id, position, size, focused or not
  python3 -I gameui.py focus                     raise and focus the game window
  python3 -I gameui.py shot [--grid] [--full]    screenshot of the game window -> prints the PNG path
                                                 (half size unless --full; --grid draws labelled lines
                                                 every 100 game pixels to read coordinates off)
  python3 -I gameui.py zoom X Y W H [--scale 2]  crop of the last full-size shot, for small text
  python3 -I gameui.py click X Y [--right] [--double] [--hold MS]
  python3 -I gameui.py move X Y
  python3 -I gameui.py drag X1 Y1 X2 Y2 [--right] [--slow]   (--slow: one step per frame, for Unity apps)
  python3 -I gameui.py scroll up|down [N] [--at X Y]
  python3 -I gameui.py key KEY [KEY ...]         e.g. key question | key Escape | key ctrl+s | key Return
                                                 | key shift+F1 | key a b c   (X keysym names)
  python3 -I gameui.py type "some text"          types text into the focused field
  python3 -I gameui.py wait MS
  python3 -I gameui.py seq "key c" "wait 1200" "key question" "wait 800" "shot --full"
                                                 several steps in one go (preferred): focuses the game
                                                 once, then gives focus and the mouse pointer back to
                                                 the user's window when done

Coordinates are GAME-WINDOW pixels at full size (0,0 = top-left of the game's drawing area, not
the title bar). A half-size shot shows them halved: multiply what you read by 2, or use --grid,
whose labels are already in game pixels. Every input first checks that the game window is the
focused window and stops otherwise, so keys never land in another program (chat, terminal). In a
seq, if the user clicks another window midway, the rest is dropped (the user takes over). Shots
are only taken while the game is the active window, so other windows are never captured.
Input commands take a screenshot afterwards (--wait MS before it, default 700; --no-shot to skip).
Before taking focus, input waits until the keyboard and mouse have been idle 4 s (--idle S; gives
up after 3 minutes), so the user's own key presses do not land in the game. Shots go to ~/.cache/game-ui/<class>/.
"""
import ctypes
import os
import re
import subprocess
import sys
import tempfile
import time

from PIL import Image, ImageDraw, ImageGrab

# Which window: UI_WMCLASS (wmctrl -lx, the class before its first dot). No built-in default any more
# (it used to be Dominions', and other games' input went there); a game's own skill may set
# UI_DEFAULT_WMCLASS before importing this (dom6ui.py sets dom6_amd64), or the game folder can name it in
# .claude/game-ui.json (see _folder_class).
def _folder_class():
    """A game folder can name its window in .claude/game-ui.json ({"wmclass": "crawl"}): found by walking
    up from the script being run, then from the current folder."""
    import json
    starts = [os.path.dirname(os.path.abspath(sys.argv[0] or ".")), os.getcwd()]
    for d in starts:
        while True:
            f = os.path.join(d, ".claude", "game-ui.json")
            if os.path.isfile(f):
                try:
                    return json.load(open(f)).get("wmclass", "")
                except (OSError, ValueError):
                    return ""
            if os.path.dirname(d) == d:
                break
            d = os.path.dirname(d)
    return ""


WM_CLASS = os.environ.get("UI_WMCLASS") or os.environ.get("UI_DEFAULT_WMCLASS") or _folder_class()
CACHE = os.path.expanduser("~/.cache/game-ui")       # permanent (a /tmp folder is wiped on reboot)
OUT = os.path.join(CACHE, WM_CLASS or "unset")       # one folder of shots per game
FLAG = os.path.join(CACHE, "recording")              # obs-record's gameplay-session flag
os.makedirs(OUT, exist_ok=True)
DISPLAY = os.environ.get("DISPLAY", ":0")

X11 = ctypes.CDLL("libX11.so.6")
XTST = ctypes.CDLL("libXtst.so.6")
X11.XOpenDisplay.restype = ctypes.c_void_p
X11.XOpenDisplay.argtypes = [ctypes.c_char_p]
X11.XGetInputFocus.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
X11.XSetInputFocus.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong]
X11.XStringToKeysym.restype = ctypes.c_ulong
X11.XStringToKeysym.argtypes = [ctypes.c_char_p]
X11.XKeysymToKeycode.restype = ctypes.c_ubyte
X11.XKeysymToKeycode.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
X11.XkbKeycodeToKeysym.restype = ctypes.c_ulong
X11.XkbKeycodeToKeysym.argtypes = [ctypes.c_void_p, ctypes.c_ubyte, ctypes.c_int, ctypes.c_int]
X11.XFlush.argtypes = [ctypes.c_void_p]
for f, args in (("XTestFakeKeyEvent", [ctypes.c_void_p, ctypes.c_uint, ctypes.c_int, ctypes.c_ulong]),
                ("XTestFakeButtonEvent", [ctypes.c_void_p, ctypes.c_uint, ctypes.c_int, ctypes.c_ulong]),
                ("XTestFakeMotionEvent", [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_ulong])):
    getattr(XTST, f).argtypes = args
_dpy = None


def dpy():
    global _dpy
    if _dpy is None:
        _dpy = X11.XOpenDisplay(DISPLAY.encode())
        if not _dpy:
            sys.exit(f"cannot open X display {DISPLAY}")
    return _dpy


def run(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout


# ---------------------------------------------------------------- the game window

_NOWM = None


def no_wm():
    """True on a screen with no window manager (bgplay's Xephyr): wmctrl can't list or focus there."""
    global _NOWM
    if _NOWM is None:
        _NOWM = not run("wmctrl", "-m").strip()
    return _NOWM


def find_window():
    title = os.environ.get("UI_WMTITLE")              # optional: one window of the app (a dialog)
    if no_wm():                                       # e.g. DISPLAY=:5 (bgplay): read the window tree
        for line in run("xwininfo", "-root", "-tree").splitlines():
            m = re.match(r'\s*(0x[0-9a-f]+) "([^"]*)": \("([^"]*)" "([^"]*)"\)', line)
            if m and WM_CLASS in (m.group(3), m.group(4)) and (not title or title in m.group(2)):
                return int(m.group(1), 16)
    for line in run("wmctrl", "-lx").splitlines():
        parts = line.split(None, 4)
        if len(parts) >= 3 and parts[2].split(".")[0] == WM_CLASS:
            if title and (len(parts) < 5 or title not in parts[4]):
                continue
            return int(parts[0], 16)
    if not WM_CLASS:
        sys.exit("say which window: UI_WMCLASS=<class> (wmctrl -lx lists them; the class is the part before its first dot)")
    sys.exit(f"no {WM_CLASS} window is open (wmctrl -lx; UI_WMCLASS is the class before its first dot)")


def geometry(wid):
    info = run("xwininfo", "-id", hex(wid))
    g = {k: int(re.search(rf"{k}:\s+(-?\d+)", info).group(1)) for k in
         ("Absolute upper-left X", "Absolute upper-left Y", "Width", "Height")}
    mapped = "IsViewable" in info
    return g["Absolute upper-left X"], g["Absolute upper-left Y"], g["Width"], g["Height"], mapped


def active_window():
    if no_wm():
        w = ctypes.c_ulong(); r = ctypes.c_int()
        X11.XGetInputFocus(dpy(), ctypes.byref(w), ctypes.byref(r))
        return w.value
    m = re.search(r"window id # (0x[0-9a-f]+)", run("xprop", "-root", "_NET_ACTIVE_WINDOW"))
    return int(m.group(1), 16) if m else None


def focus(wid, tries=3):
    for _ in range(tries):
        if active_window() == wid and geometry(wid)[4]:
            return True
        if no_wm():
            X11.XSetInputFocus(dpy(), ctypes.c_ulong(wid), 2, 0); X11.XFlush(dpy())
        else:
            subprocess.run(["wmctrl", "-i", "-R", hex(wid)])       # bring to this desktop, raise, focus
        time.sleep(0.8)
    return active_window() == wid


def guard():
    """The game window, focused; exits rather than send input anywhere else."""
    wid = find_window()
    if not focus(wid):
        sys.exit(f"STOPPED: could not focus the {WM_CLASS} window; no input was sent")
    return wid, geometry(wid)


# ---------------------------------------------------------------- screenshots

def shot(full=False, grid=False, quiet=False):
    wid = find_window()
    x, y, w, h, mapped = geometry(wid)
    if not mapped or active_window() != wid:
        print("no shot: the game window is not in front (another window would be captured)")
        return None
    os.makedirs(OUT, exist_ok=True)
    im = ImageGrab.grab(bbox=(x, y, x + w, y + h), xdisplay=DISPLAY)
    im.save(os.path.join(OUT, "last_full.png"))
    if grid:
        d = ImageDraw.Draw(im)
        for gx in range(0, w, 100):
            d.line([(gx, 0), (gx, h)], fill=(255, 255, 0) if gx % 500 else (255, 0, 0), width=1)
            d.text((gx + 2, 2), str(gx), fill=(255, 255, 0))
        for gy in range(0, h, 100):
            d.line([(0, gy), (w, gy)], fill=(255, 255, 0) if gy % 500 else (255, 0, 0), width=1)
            d.text((2, gy + 2), str(gy), fill=(255, 255, 0))
    if not full:
        im = im.resize((w // 2, h // 2), Image.LANCZOS)
    path = os.path.join(OUT, f"shot_{time.strftime('%H%M%S')}_{int(time.time() * 1000) % 1000:03d}.png")
    im.save(path)
    if not quiet:
        print(f"{path}  ({'full' if full else 'half'} size of {w}x{h}{', grid in game pixels' if grid else ''})")
    return path


def zoom(x, y, w, h, scale=2):
    im = Image.open(os.path.join(OUT, "last_full.png")).crop((x, y, x + w, y + h))
    im = im.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    path = os.path.join(OUT, f"zoom_{time.strftime('%H%M%S')}.png")
    im.save(path)
    print(path)


# ---------------------------------------------------------------- input

class XScreenSaverInfo(ctypes.Structure):
    _fields_ = [("window", ctypes.c_ulong), ("state", ctypes.c_int), ("kind", ctypes.c_int),
                ("til_or_since", ctypes.c_ulong), ("idle", ctypes.c_ulong), ("eventMask", ctypes.c_ulong)]


def idle_ms():
    """Milliseconds since the user last touched the keyboard or mouse (XScreenSaver extension)."""
    xss = ctypes.CDLL("libXss.so.1")
    xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(XScreenSaverInfo)
    xss.XScreenSaverQueryInfo.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(XScreenSaverInfo)]
    X11.XDefaultRootWindow.restype = ctypes.c_ulong
    X11.XDefaultRootWindow.argtypes = [ctypes.c_void_p]
    info = xss.XScreenSaverAllocInfo()
    xss.XScreenSaverQueryInfo(dpy(), X11.XDefaultRootWindow(dpy()), info)
    return info.contents.idle


def wait_idle(seconds, max_wait):
    """Wait until the user has been idle SECONDS, so their typing cannot land in the game."""
    t0 = time.time()
    told = False
    while idle_ms() < seconds * 1000:
        if time.time() - t0 > max_wait:
            sys.exit(f"STOPPED: the user was busy for {max_wait} s; no input was sent (try again later)")
        if not told:
            print(f"waiting until the keyboard and mouse have been idle {seconds} s...", flush=True)
            told = True
        time.sleep(0.5)


def pointer():
    root, child = ctypes.c_ulong(), ctypes.c_ulong()
    rx, ry, wx, wy = ctypes.c_int(), ctypes.c_int(), ctypes.c_int(), ctypes.c_int()
    mask = ctypes.c_uint()
    X11.XDefaultRootWindow.restype = ctypes.c_ulong
    X11.XDefaultRootWindow.argtypes = [ctypes.c_void_p]
    X11.XQueryPointer.argtypes = [ctypes.c_void_p, ctypes.c_ulong] + [ctypes.c_void_p] * 7
    X11.XQueryPointer(dpy(), X11.XDefaultRootWindow(dpy()), ctypes.byref(root), ctypes.byref(child),
                      ctypes.byref(rx), ctypes.byref(ry), ctypes.byref(wx), ctypes.byref(wy), ctypes.byref(mask))
    return rx.value, ry.value


def to_screen(geo, x, y):
    gx, gy, w, h, _ = geo
    if not (0 <= x < w and 0 <= y < h):
        sys.exit(f"STOPPED: ({x}, {y}) is outside the game window ({w}x{h}); no input was sent")
    return gx + x, gy + y


def move(geo, x, y):
    sx, sy = to_screen(geo, x, y)
    XTST.XTestFakeMotionEvent(dpy(), -1, sx, sy, 0)
    X11.XFlush(dpy())


def button(b, down):
    XTST.XTestFakeButtonEvent(dpy(), b, 1 if down else 0, 0)
    X11.XFlush(dpy())


def approach(geo, x, y):
    """Glide onto (x, y) in small steps: the game misses a hover (and then the click) when the
    pointer jumps straight onto some list rows. One frame apart is enough: no visible glide
    (the user wants no delays, 2026-10-27)."""
    move(geo, max(0, x - 4), max(0, y - 3))
    time.sleep(0.017)
    move(geo, x, y)


def click(geo, x, y, right=False, double=False, hold=20, mods=()):
    """mods: modifier names held during the click, e.g. ("alt",) for the game's alt-click."""
    approach(geo, x, y)
    time.sleep(0.017)
    b = 3 if right else 1
    held = [keycode(MODS[m.lower()])[0] for m in mods]
    for m in held:
        XTST.XTestFakeKeyEvent(dpy(), m, 1, 0)
    X11.XFlush(dpy())
    try:
        for _ in range(2 if double else 1):
            button(b, True)
            time.sleep(hold / 1000)
            button(b, False)
            time.sleep(0.017)
    finally:
        for m in reversed(held):
            XTST.XTestFakeKeyEvent(dpy(), m, 0, 0)
        X11.XFlush(dpy())


def drag(geo, x1, y1, x2, y2, right=False, slow=False):
    """slow: Unity apps (MapNuke) miss a drag whose moves all land in one frame, so pause a frame
    after the press, between steps and before the release."""
    b = 3 if right else 1
    pause = 0.03 if slow else 0
    move(geo, x1, y1)
    time.sleep(pause)
    button(b, True)
    for i in range(1, 11):
        time.sleep(pause)
        move(geo, x1 + (x2 - x1) * i // 10, y1 + (y2 - y1) * i // 10)
    time.sleep(pause * 3)
    button(b, False)


def keycode(name):
    ks = X11.XStringToKeysym(name.encode())
    if not ks:
        sys.exit(f"unknown key name {name!r} (use X keysym names: a, A, question, Escape, Return, F1, Left...)")
    kc = X11.XKeysymToKeycode(dpy(), ks)
    if not kc:
        sys.exit(f"key {name!r} is not on this keyboard layout")
    shift = X11.XkbKeycodeToKeysym(dpy(), kc, 0, 0) != ks and X11.XkbKeycodeToKeysym(dpy(), kc, 0, 1) == ks
    return kc, shift


MODS = {"ctrl": "Control_L", "control": "Control_L", "shift": "Shift_L", "alt": "Alt_L"}


def key(combo):
    parts = combo.split("+") if combo != "+" else ["plus"]
    mods = [MODS[p.lower()] for p in parts[:-1]]
    kc, shift = keycode(parts[-1])
    if shift and "Shift_L" not in mods:
        mods.append("Shift_L")
    down = [keycode(m)[0] for m in mods]
    for m in down:
        XTST.XTestFakeKeyEvent(dpy(), m, 1, 0)
    XTST.XTestFakeKeyEvent(dpy(), kc, 1, 0)
    X11.XFlush(dpy())
    time.sleep(0.017)
    XTST.XTestFakeKeyEvent(dpy(), kc, 0, 0)
    for m in reversed(down):
        XTST.XTestFakeKeyEvent(dpy(), m, 0, 0)
    X11.XFlush(dpy())


CHARS = {" ": "space", ".": "period", ",": "comma", "-": "minus", "_": "underscore", ":": "colon", "/": "slash",
         "'": "apostrophe", '"': "quotedbl", "!": "exclam", "?": "question", "(": "parenleft", ")": "parenright",
         "@": "at", "#": "numbersign", "+": "plus", "=": "equal", ";": "semicolon", "&": "ampersand",
         "*": "asterisk", "%": "percent", "$": "dollar", "\n": "Return", ">": "greater", "<": "less",
         "|": "bar", "~": "asciitilde", "^": "asciicircum", "{": "braceleft", "}": "braceright",
         "[": "bracketleft", "]": "bracketright", "\\": "backslash", "`": "grave"}


def type_text(text):
    for c in text:
        key(CHARS.get(c, c))


# ---------------------------------------------------------------- command line

def flag(a, name, default=None, n=1):
    if name in a:
        i = a.index(name)
        vals = a[i + 1:i + 1 + n]
        del a[i:i + 1 + n]
        return vals[0] if n == 1 else vals
    return default


def step(cmd, a, wid, geo, shots):
    """One input step; returns False if the game lost focus (the user took over)."""
    if cmd in ("shot",):
        p = shot(full="--full" in a, grid="--grid" in a, quiet=True)
        if p:
            shots.append(p)
        return True
    if cmd == "wait":
        time.sleep(int(a[0]) / 1000)
        return True
    if active_window() != wid:
        return False
    if cmd == "click":
        hold = int(flag(a, "--hold", 150))
        nums = [int(v) for v in a if re.fullmatch(r"-?\d+", v)]
        click(geo, nums[0], nums[1], "--right" in a, "--double" in a, hold)
    elif cmd == "move":
        move(geo, int(a[0]), int(a[1]))
    elif cmd == "drag":
        nums = [int(v) for v in a if re.fullmatch(r"-?\d+", v)]
        drag(geo, *nums[:4], right="--right" in a, slow="--slow" in a)
    elif cmd == "scroll":
        at = flag(a, "--at", None, 2)
        if at:
            move(geo, int(at[0]), int(at[1]))
        b = 4 if a[0] == "up" else 5
        for _ in range(int(a[1]) if len(a) > 1 else 1):
            button(b, True)
            button(b, False)
            time.sleep(0.05)
    elif cmd == "key":
        for k in a:
            if active_window() != wid:
                return False
            key(k)
    elif cmd == "type":
        type_text(" ".join(a))
    else:
        sys.exit(f"unknown step {cmd!r}")
    return True


IDLE_S, IDLE_MAX = 4, 180


def _recorder():
    """obs-record's obs.py while a gameplay recording session is open (its flag file exists) and
    this run drives a game (not OBS itself); same as session.py."""
    if not os.path.exists(FLAG) or WM_CLASS == "obs":     # not while driving OBS itself
        return None
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "obs-record", "scripts"))
    try:
        import obs
        return obs
    except Exception:
        return None


def hand_back(wid, prev_win, prev_ptr):
    """Give the pointer and focus back after acting. If the app itself was already in front (it
    took focus when it opened, or an earlier hand-back missed), focus goes to the terminal Claude
    runs in ($WINDOWID, set by the terminal), so focus never stays stuck in the app."""
    if no_wm():                                       # Claude's own screen: nothing to hand back
        return
    home = prev_win if prev_win and prev_win != wid else int(os.environ.get("WINDOWID") or 0)
    if home and home != wid:
        XTST.XTestFakeMotionEvent(dpy(), -1, prev_ptr[0], prev_ptr[1], 0)
        X11.XFlush(dpy())
        subprocess.run(["wmctrl", "-i", "-a", hex(home)])


def session(steps, final_shot=True, wait=700):
    """Wait for the user to be idle, focus the game, run the steps, take a shot, then hand focus
    and the pointer back."""
    wait_idle(IDLE_S, IDLE_MAX)
    prev_win, prev_ptr = active_window(), pointer()
    wid, geo = guard()
    shots, done = [], 0
    rec = _recorder()
    if rec:
        rec.hook(True)                             # OBS gameplay session: record this action
    try:
        for cmd, a in steps:
            if not step(cmd, list(a), wid, geo, shots):
                print(f"STOPPED after {done} of {len(steps)} steps: the game lost focus (the user switched window)")
                break
            done += 1
        else:
            if final_shot and (not steps or steps[-1][0] != "shot"):
                time.sleep(wait / 1000)
                p = shot(quiet=True)
                if p:
                    shots.append(p)
    finally:
        if rec:
            rec.hook(False)
        hand_back(wid, prev_win, prev_ptr)
    for p in shots:
        print(p)


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd, a = a[0], a[1:]
    global IDLE_S
    wait = int(flag(a, "--wait", 700))
    IDLE_S = float(flag(a, "--idle", IDLE_S))
    no_shot = "--no-shot" in a
    if no_shot:
        a.remove("--no-shot")
    if cmd == "find":
        wid = find_window()
        x, y, w, h, mapped = geometry(wid)
        print(f"window {hex(wid)} at {x},{y} size {w}x{h}, {'mapped' if mapped else 'minimised/unmapped'}, "
              f"{'focused' if active_window() == wid else 'not focused'}")
        return
    if cmd == "shot":
        shot(full="--full" in a, grid="--grid" in a)
        return
    if cmd == "zoom":
        scale = float(flag(a, "--scale", 2))
        zoom(*map(int, a[:4]), scale=scale)
        return
    if cmd == "wait":
        time.sleep(int(a[0]) / 1000)
        if not no_shot:
            shot()
        return
    if cmd == "seq":
        steps = []
        for item in a:
            parts = item.split()
            steps.append((parts[0], parts[1:] if parts[0] != "type" else [item.split(None, 1)[1]]))
        session(steps, final_shot=not no_shot, wait=wait)
        return
    if cmd in ("click", "move", "drag", "scroll", "key", "type"):
        session([(cmd, a if cmd != "type" else [" ".join(a)])], final_shot=not no_shot, wait=wait)
        return
    if cmd == "focus":
        guard()
        print("focused")
        return
    sys.exit(f"unknown command {cmd!r}; see --help")

if __name__ == "__main__":
    main()
