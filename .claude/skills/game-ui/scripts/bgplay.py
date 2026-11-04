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
  start --cursor                              draw the mouse pointer in the window (Xephyr software
                                              cursor) when a game hides it, e.g. for the user to play there
  start --glamor                              Xephyr's glamor drawing (2D only; it does NOT give the
                                              game DRI3 or Vulkan - tested with FoG II, 2026-11-02)
  bgplay.py act NAME "STEP" [--timeout 180] [--took 3] [--tol 12]
                                              THE way to start a load or screen change (the user's method): shot
                                              before, STEP (e.g. "click 955 589"), grab every ~33 ms until it
                                              TOOK (exit 2 if not), then the GENERAL loading test: no loading
                                              screen = done; loading = poll it out. NAME keeps load times only
  bgplay.py isloading [--window 1] [--nowords]  is the screen NOW a loading screen? LOADING (exit 10, evidence:
                                              blank, fade, spinner-only motion, loading words) / NOT LOADING
  bgplay.py waitload [--timeout 600] [--name N]  if LOADING, poll every second until it's gone
  bgplay.py waitchange [--timeout 180] [--every 3] [--nosettle] [--until TEXT [--box X0 Y0 X1 Y1]]
                                              --until = READY when TEXT is on screen (checked at once: a screen
                                              already up counts) - use it whenever the target has known text;
                                              settles on a still OR steadily animated screen
                                              wait for the whole screen to change, then hold still
                                              (loading screens, turn changes); ends with a shot.
                                              Use with mark:  seq "mark" "click X Y" "waitchange"
                                              (mark = the screen before the action, so a fast
                                              change can't happen before the polling starts)
  bgplay.py windows                           windows on the virtual screen (class, size, position)
  bgplay.py shot [--full] [--box X0 Y0 X1 Y1] screenshot of the virtual screen (half size unless --full;
                                              --box: only that part, fast, as crop_*.png - for sweeps in seq)
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


def start(size, glamor=False, cursor=False):
    if running():
        print(f"virtual screen {DISP} already running")
        return
    log = open(os.path.join(OUT, "xephyr.log"), "w")
    subprocess.Popen(["Xephyr", DISP, "-screen", size, "-ac", "-title", "Claude game screen"]
                     + (["-glamor"] if glamor else []) + (["-sw-cursor"] if cursor else []),
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


def shot(full=False, box=None):
    need()
    im = ImageGrab.grab(xdisplay=DISP)
    if box:                                    # fast: only this part, light compression, no last_full
        p = os.path.join(OUT, f"crop_{time.strftime('%H%M%S')}_{int(time.time() * 1000) % 1000:03d}.png")
        im.crop(tuple(box)).save(p, compress_level=1)
        print(p)
        return
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


def _screen_has(text, box=None):
    """OCR the screen (or a box) for TEXT, case-insensitive, spaces ignored; light and dark text both tried."""
    import ocr as O
    im = ImageGrab.grab(xdisplay=DISP)
    b = tuple(box) if box else (0, 0, im.width, im.height)
    want = re.sub(r"\s+", "", text.lower())
    for dark in (False, True):
        got = re.sub(r"\s+", "", O.ocr(O.prepare(im, b, scale=2, dark=dark), psm=11).lower())
        if want in got:
            return True
    return False


def waitchange(timeout=180, every=3.0, settle=True, until=None, box=None):
    """Wait for a screen to be READY. Fixed 2026-11-03 after the user: "the checking for if stuff loading is broken"
    (Dominions: the game had loaded while the wait still ran to its timeout). Ends on the first of:
      READY     --until TEXT is on the screen (or in --box) - checked at once, so a screen that is ALREADY
                there counts; this is the reliable test, use it whenever the target screen has known text;
      CHANGED   the screen differs from the mark (or from the start) - with --nosettle;
      SETTLED   after a change, the screen holds still (frame difference < 1.5), or keeps moving at a STEADY
                low rate (animated backgrounds: Dominions' sea floor never holds still) - the last two
                frame differences under 6 and within 1 of each other;
      TIMEOUT   says which of the above never happened.
    A heartbeat every ~30 s shows the poll is alive. Ends with a half-size shot."""
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
        print("no mark: comparing with the screen as it is now" + ("" if until else
              " (if the target screen may already be up, use --until TEXT)"), flush=True)
    prev, changed, beat, first, steps = base, False, t0, True, []
    result = None
    while time.time() - t0 < timeout:
        if not first:
            time.sleep(every)
        first = False
        if until and _screen_has(until, box):
            result = f"READY: '{until}' on screen after {time.time() - t0:.0f} s"
            break
        cur = thumb()
        if time.time() - beat > 30:
            beat = time.time()
            print(f"  ...polling, {time.time() - t0:.0f} s, difference {diff(cur, base):.1f} (change = 6)", flush=True)
        if not changed and diff(cur, base) > 6:
            changed = True
            print(f"changed after {time.time() - t0:.0f} s", flush=True)
            if not settle and not until:
                result = f"CHANGED after {time.time() - t0:.0f} s"
                break
        elif changed and not until:
            d = diff(cur, prev)
            steps.append(d)
            if d < 1.5:
                result = f"SETTLED (still) after {time.time() - t0:.0f} s"
                break
            if len(steps) >= 2 and max(steps[-2:]) < 6 and abs(steps[-1] - steps[-2]) < 1:
                result = f"SETTLED (steady animation, frame difference ~{d:.1f}) after {time.time() - t0:.0f} s"
                break
        prev = cur
    if result is None:
        result = (f"TIMEOUT after {timeout} s: " + (f"'{until}' never appeared" if until else
                  "still changing" if changed else "NO CHANGE"))
    print(result, flush=True)
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


def _profile_dir():
    d = os.getcwd()
    while True:
        if os.path.isfile(os.path.join(d, ".claude", "game-ui.json")):
            return os.path.join(d, ".claude")
        if os.path.dirname(d) == d:
            return None
        d = os.path.dirname(d)


def changed(a, b, tol=12.0):
    """Did the screen really change between thumbs A and B? Whole-screen mean difference > TOL (big changes),
    OR >= 0.2% of pixels changed by more than 40 grey levels (a small dialog replacing another one in place -
    Dominions' End Turn Yes -> "AI thinking" box read only 11.8 on the mean). Measured 2026-11-03: Dominions'
    animated background moves no pixel more than 15 in 3 s, so 40 is safe. Returns (bool, why)."""
    from PIL import ImageChops, ImageStat
    d = ImageChops.difference(a, b)
    m = ImageStat.Stat(d).mean[0]
    if m > tol:
        return True, f"mean {m:.1f}"
    h = d.histogram()
    frac = sum(h[41:]) / (d.width * d.height)
    if frac >= 0.002:
        return True, f"{frac * 100:.1f}% of pixels changed sharply"
    return False, f"mean {m:.1f}, sharp {frac * 100:.2f}%"


def loading_signs(window=1.0, words=True, pre=None):
    """GENERAL test: does the screen look like a loading screen right now? (the user 2026-11-03: "the necessary part
    is generalizing how you check if it's a loading screen ... then you can apply the same logic across other
    things"). Watches WINDOW seconds of frames (~33 ms each, 160x99 grey) and reads the screen once:
      blank     dark or near-uniform frame (black screen, a fade's bottom, a plain colour)
      fade      brightness ramps steadily up or down over the window (fade in/out)
      local     only a small patch moves (spinner, progress bar) while the rest holds still - an animated game
                screen drifts all over instead (Dominions' sea: changes spread over the whole frame)
      words     "loading", "please wait", "AI thinking", "reticulating"... (a hint: joke texts exist)
    Returns (loading?, [evidence], last thumb). PRE (the shot before an action) adds "dark vs before"."""
    from PIL import ImageChops, ImageStat
    frames, t0 = [], time.time()
    while time.time() - t0 < window or len(frames) < 3:
        frames.append(thumb())
    st = ImageStat.Stat(frames[-1])
    mean, sd = st.mean[0], st.stddev[0]
    ev = []
    if mean < 25 or sd < 10:
        ev.append(f"blank (mean {mean:.0f}, spread {sd:.0f})")
    if pre is not None and mean < 0.5 * ImageStat.Stat(pre).mean[0]:
        ev.append(f"dark vs before ({mean:.0f} vs {ImageStat.Stat(pre).mean[0]:.0f})")
    ms_ = [ImageStat.Stat(f).mean[0] for f in frames]
    steps = [y - x for x, y in zip(ms_, ms_[1:])]
    if abs(ms_[-1] - ms_[0]) > 6 and (all(d >= -0.5 for d in steps) or all(d <= 0.5 for d in steps)):
        ev.append(f"fade (brightness {ms_[0]:.0f} -> {ms_[-1]:.0f})")
    weak = None
    d = ImageChops.difference(frames[0], frames[-1]).point(lambda v: 255 if v > 25 else 0)
    box = d.getbbox()
    if box:
        moving = sum(d.histogram()[255:]) / (d.width * d.height)
        area = (box[2] - box[0]) * (box[3] - box[1]) / (d.width * d.height)
        if area < 0.12 and 0.001 < moving < 0.03:
            weak = f"local motion only ({area * 100:.1f}% of the screen: spinner / progress bar?)"
    # local motion is a WEAK sign alone: a still game screen with one animated flag looks the same (Dominions
    # map, 2026-11-03: false LOADING). It counts only with a loading word on the screen.
    if words and not ev:
        import ocr as O
        im = ImageGrab.grab(xdisplay=DISP)
        t = re.sub(r"\s+", "", O.ocr(O.prepare(im, (0, 0, im.width, im.height), scale=1, dark=False), psm=11).lower())
        hit = next((w for w in LOADING_WORDS if w in t), None)
        if hit:
            ev.append(f"says '{hit}'")
            if weak:
                ev.append(weak)
    return bool(ev), ev, frames[-1]


def _history(name, load_ms=None):
    """Load-time record per transition NAME (.claude/transitions/NAME.json): optional, for "slower than usual"."""
    import json
    if not name:
        return []
    tdir = os.path.join(_profile_dir() or OUT, "transitions")
    os.makedirs(tdir, exist_ok=True)
    jf = os.path.join(tdir, name + ".json")
    hist = json.load(open(jf)).get("loads_ms", []) if os.path.exists(jf) else []
    if load_ms is not None:
        hist = (hist + [load_ms])[-10:]
        json.dump({"loads_ms": hist, "updated": time.strftime("%Y-%m-%d %H:%M")}, open(jf, "w"), indent=1)
    return hist


def wait_out(t0, tol=12.0, timeout=600, name=None, pre=None):
    """While loading_signs says loading, poll (fast for 5 s, then every second - cheap) until the screen has
    left that loading screen and no longer looks like one. Returns how long the loading screen lasted (ms)."""
    from PIL import ImageChops, ImageStat
    md = lambda a, b: ImageStat.Stat(ImageChops.difference(a, b)).mean[0]
    longest, warned, beat = max(_history(name) or [0]), False, time.time()
    start = time.time()
    loading, ev, L = loading_signs(0.3, words=True, pre=pre)
    if not loading:
        return None, ev
    print(f"LOADING: {'; '.join(ev)}", flush=True)
    while time.time() - t0 < timeout:
        time.sleep(0.1 if time.time() - start < 5 else 1.0)
        cur = thumb()
        if changed(cur, L, tol)[0]:
            loading, ev2, L2 = loading_signs(0.3, words=True)
            if not loading:
                ms_ = int((time.time() - start) * 1000)
                _history(name, ms_)
                return ms_, ev
            L = L2                                   # a second loading screen (progress stages): follow it
        el = int((time.time() - start) * 1000)
        if longest and not warned and el > 2 * longest:
            warned = True
            print(f"  ...slower than ever before ({el} ms, longest seen {longest} ms) - maybe stuck", flush=True)
        if time.time() - beat > 30:
            beat = time.time()
            print(f"  ...still loading, {el // 1000} s", flush=True)
    return -1, ev


def act(name, step, timeout=180.0, took_s=3.0, tol=12.0):
    """Do STEP and see it through (the user's method): shot just BEFORE (same process, no gap); grab every ~33 ms
    until the screen differs from it by TOL (else DID NOT TAKE, exit 2); then the GENERAL loading test
    (loading_signs) on what came up: not loading = done (a button click), loading = wait it out polling
    (wait_out). NAME only keeps a load-time history for "slower than usual". Exit 3 = timeout."""
    from PIL import ImageChops, ImageStat
    need()
    md = lambda a, b: ImageStat.Stat(ImageChops.difference(a, b)).mean[0]
    pre = thumb()
    t0 = time.time()
    do(step)
    took = None
    while time.time() - t0 < took_s:
        if changed(thumb(), pre, tol)[0]:
            took = int((time.time() - t0) * 1000)
            break
    if took is None:
        print(f"DID NOT TAKE: '{step}' - the screen stayed within {tol} of the shot before it for {took_s:.0f} s")
        shot()
        sys.exit(2)
    print(f"TOOK in {took} ms", flush=True)
    load_ms, ev = wait_out(t0, tol, timeout, name, pre)
    if load_ms is None:
        print(f"READY at {int((time.time() - t0) * 1000)} ms: no loading screen (a button click)")
    elif load_ms < 0:
        print(f"TIMEOUT after {timeout:.0f} s: still loading ({'; '.join(ev)})")
        shot()
        sys.exit(3)
    else:
        print(f"READY at {int((time.time() - t0) * 1000)} ms: the loading screen lasted {load_ms} ms")
    shot()


LOADING_WORDS = ("loading", "pleasewait", "thinking", "generating", "saving", "connecting", "initializing",
                 "preparing", "reticulating")   # The Sims: "Reticulating Splines" - joke texts exist; words are only a hint


def isloading(window=1.0, words=True):
    """Is the screen a loading screen NOW? LOADING (exit 10, with the evidence) or NOT LOADING (exit 0)."""
    need()
    loading, ev, _ = loading_signs(window, words)
    print(("LOADING: " + "; ".join(ev)) if loading else "NOT LOADING: no blank/fade, no spinner-only motion, no loading words")
    shot()
    sys.exit(10 if loading else 0)


def waitload(timeout=600, tol=12.0, name=None):
    """isloading; if loading, poll every second until it's gone (wait_out)."""
    need()
    t0 = time.time()
    load_ms, ev = wait_out(t0, tol, timeout, name)
    print("NOT LOADING" if load_ms is None else f"TIMEOUT after {timeout} s: still loading" if load_ms < 0
          else f"READY: the loading screen lasted {load_ms} ms")
    shot()
    if load_ms is not None and load_ms < 0:
        sys.exit(3)


def wait_args(p):
    """waitchange's flags, from the command line or a seq step: [N] [--timeout N] [--every S] [--nosettle]
    [--until TEXT (quote it in seq: "waitchange --until 'Combat round'")] [--box X0 Y0 X1 Y1]"""
    import shlex
    p = list(p) if isinstance(p, list) else shlex.split(p)     # the shell already split command-line args
    if len(p) == 1 and " " in p[0]:
        p = shlex.split(p[0])
    t = opt(p, "--timeout", p[1] if len(p) > 1 and p[1].isdigit() else "180")
    b = p.index("--box") if "--box" in p else -1
    waitchange(int(t), float(opt(p, "--every", "3")), "--nosettle" not in p, opt(p, "--until"),
               [int(v) for v in p[b + 1:b + 5]] if b >= 0 else None)


KEY_GAP = [0.03]


def do(step):
    p = step.split()
    c = p[0]
    if c == "mark":
        mark()
        return
    if c == "waitchange":                      # same flags as the command (they were ignored in seq before)
        wait_args(step)
        return
    if c == "wait":
        time.sleep(int(p[1]) / 1000)
    elif c == "shot":
        b = p.index("--box") if "--box" in p else -1
        shot("--full" in p, [int(v) for v in p[b + 1:b + 5]] if b >= 0 else None)
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
        start(opt(a, "--size", "1600x990"), glamor="--glamor" in a, cursor="--cursor" in a)
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
        wait_args(a)
    elif c == "waitload":
        waitload(float(opt(a, "--timeout", "600")), float(opt(a, "--tol", "12")), opt(a, "--name"))
    elif c == "isloading":
        isloading(float(opt(a, "--window", "1")), "--nowords" not in a)
    elif c == "act":
        act(a[1], a[2], float(opt(a, "--timeout", "180")), float(opt(a, "--took", "3")), float(opt(a, "--tol", "12")))
    elif c == "windows":
        for r in windows():
            print(f"{r[0]}  {r[2]:<16} {r[3]}x{r[4]}+{r[5]}+{r[6]}  {r[1]}")
    elif c == "shot":
        b = a.index("--box") if "--box" in a else -1
        shot("--full" in a, [int(v) for v in a[b + 1:b + 5]] if b >= 0 else None)
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
