"""Shared pieces for scripts that drive a running game through the gameui guard: a
session object (Game6) whose every input re-checks that the game is focused, screen-text checks,
and run(), which waits for the user to be idle and gives focus and the pointer back afterwards."""
import os
import sys
import time

from PIL import ImageGrab

import gameui as U


class Stop(Exception):
    pass


# ---------------------------------------------------------------- driving the window

class Game6:
    def __init__(self, prefix="shot"):
        self.wid, self.geo = U.guard()
        self.n, self.prefix = 0, prefix

    def alive(self):
        if U.active_window() != self.wid:
            raise Stop("the game lost focus (the user switched window); stopped")

    def grab(self, name=None):
        self.alive()
        x, y, w, h, _ = self.geo
        im = ImageGrab.grab(bbox=(x, y, x + w, y + h), xdisplay=U.DISPLAY)
        if name:
            os.makedirs(U.OUT, exist_ok=True)
            self.n += 1
            p = os.path.join(U.OUT, f"{self.prefix}_{self.n:02d}_{name}.png")
            im.resize((w // 2, h // 2)).save(p)
            print(f"  shot: {p}")
        return im

    def burst(self, n=16, gap=0.25):
        """N grabs GAP seconds apart (a short video): what moves is the 3D world behind the UI."""
        out = []
        for _ in range(n):
            out.append(self.grab())
            time.sleep(gap)
        return out

    def click(self, x, y, right=False, times=1, wait=0.15, mods=()):
        self.alive()
        U.click(self.geo, x, y, right=right, mods=mods)
        for _ in range(times - 1):
            self.alive()
            U.button(3 if right else 1, True)
            time.sleep(0.017)
            U.button(3 if right else 1, False)
            time.sleep(0.017)
        time.sleep(wait)

    def hover(self, x, y, wait=0.05):
        self.alive()
        U.approach(self.geo, x, y)
        time.sleep(wait)

    def key(self, *keys, wait=0.25):
        for k in keys:
            self.alive()
            U.key(k)
        time.sleep(wait)

    def hold(self, name, seconds, wait=0.1):
        """Hold a key down for SECONDS (camera pans: Left/Right/Up/Down)."""
        self.alive()
        kc, _ = U.keycode(name)
        U.XTST.XTestFakeKeyEvent(U.dpy(), kc, 1, 0); U.X11.XFlush(U.dpy())
        time.sleep(seconds)
        U.XTST.XTestFakeKeyEvent(U.dpy(), kc, 0, 0); U.X11.XFlush(U.dpy())
        time.sleep(wait)

    def type(self, text):
        self.alive()
        U.type_text(text)

    def scroll(self, down, n, at=(960, 500), wait=0.25):
        self.alive()
        U.move(self.geo, *at)
        for _ in range(n):
            U.button(5 if down else 4, True)
            U.button(5 if down else 4, False)
            time.sleep(0.015)
        time.sleep(wait)


def says(im, box, text, light=True, limit=0.3):
    import textmatch as T                       # Dominions font matcher (dom6-ui/scripts on sys.path)
    r = T.match(im, box, [text], light)
    return bool(r) and r[0][0] <= limit


def on_text(im, box, light=True):
    """A point on the text in BOX (the game ignores clicks on a row's blank part)."""
    import textmatch as T
    got = T.ink(im, box, light)
    x = box[0] + got[2] + min(25, max(4, got[1] // 4)) if got else box[0] + 20
    return x, (box[1] + box[3]) // 2


def same(a, b, box):
    from PIL import ImageChops, ImageStat
    d = ImageStat.Stat(ImageChops.difference(a.crop(box).convert("L"), b.crop(box).convert("L"))).mean[0]
    return d < 2


# ---------------------------------------------------------------- screens

def _recorder():
    """obs-record's obs.py when a gameplay recording session is open (its flag file exists) and
    this run drives a game (not OBS itself)."""
    if not os.path.exists(U.FLAG) or U.WM_CLASS == "obs":   # not while driving OBS itself
        return None
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "obs-record", "scripts"))
    try:
        import obs
        return obs
    except Exception:
        return None


def run(work, prefix="shot"):
    """Run WORK(g) on the focused game; hand focus and the pointer back afterwards."""
    U.wait_idle(U.IDLE_S, U.IDLE_MAX)
    prev_win, prev_ptr = U.active_window(), U.pointer()
    g = Game6(prefix)
    rec = _recorder()
    if rec:
        rec.hook(True)                             # OBS gameplay session: record this action
    try:
        work(g)
    except Stop as e:
        if U.active_window() == g.wid:
            g.grab("stopped")
        print(f"STOPPED: {e}")
        sys.exit(2)
    finally:
        if rec:
            rec.hook(False)
        U.hand_back(g.wid, prev_win, prev_ptr)
