#!/usr/bin/env python3
"""Is the game actually working? The user's rule (2026-11-02): assume a freshly launched game is NOT
working until shown otherwise, and check in periodically; 30 s to 1 min tells.

  UI_WMCLASS=<class> gamecheck.py [--secs 60] [--every 15] [--hover X Y] [--bg]

Checks, every --every seconds for --secs seconds, on the game's window (gameui's guard: waits for
the user to be idle, only shoots when the game is in front; --bg = the bgplay virtual screen
instead, no guard):
  GONE      no window of that class any more (crashed or closed)
  POPUP     more than one window of the class (an error box, a notice, a launcher) - look at it
  BLANK     the picture is one flat colour (black or white screen: not drawing)
  FROZEN    (with --hover) moving the pointer off and onto X Y changes nothing there - the game
            isn't reading input or isn't redrawing
  OK        none of those
Prints one line per check and a verdict; exit code 0 = OK every time, 1 = a problem was seen.
Shots are kept (paths printed) - Read the last one when anything isn't OK.
"""
import os
import subprocess
import sys
import time

from PIL import Image, ImageChops, ImageStat

HERE = os.path.dirname(os.path.abspath(__file__))
CLS = os.environ.get("UI_WMCLASS", "")


def opt(a, name, default):
    if name in a:
        i = a.index(name)
        return a[i + 1:i + 3] if name == "--hover" else a[i + 1]
    return default


def windows():
    out = subprocess.run(["wmctrl", "-lx"], capture_output=True, text=True).stdout
    return [ln for ln in out.splitlines() if len(ln.split()) > 2 and ln.split()[2].split(".")[0] == CLS]


def run(tool, *steps):
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, tool), "seq", *steps],
                       capture_output=True, text=True)
    return [ln for ln in r.stdout.splitlines() if ln.endswith(".png")], r.stdout + r.stderr


def check(bg, hover):
    tool = "bgplay.py" if bg else "gameui.py"
    if not bg:
        wins = windows()
        if not wins:
            return "GONE", None
        if len(wins) > 1:
            return "POPUP", None
    steps = []
    if hover:
        x, y = map(int, hover)
        steps = [f"move {x + 300} {y + 300}", "wait 700", "shot --full", f"move {x} {y}", "wait 700"]
    shots, log = run(tool, *steps, "shot --full")
    if not shots:
        return "NO SHOT (" + log.strip().splitlines()[-1][:80] + ")", None
    img = Image.open(shots[-1]).convert("RGB")
    if max(ImageStat.Stat(img).stddev) < 4:
        return "BLANK", shots[-1]
    if hover and len(shots) == 2:
        a = Image.open(shots[0]).convert("RGB")
        x, y = map(int, hover)
        box = (max(0, x - 150), max(0, y - 40), x + 150, y + 40)
        if max(ImageStat.Stat(ImageChops.difference(a.crop(box), img.crop(box))).mean) < 1.0:
            return "FROZEN", shots[-1]
    return "OK", shots[-1]


def main(a):
    if "-h" in a or "--help" in a or (not CLS and "--bg" not in a):
        sys.exit(__doc__)
    secs, every = int(opt(a, "--secs", 60)), int(opt(a, "--every", 15))
    hover, bg = opt(a, "--hover", None), "--bg" in a
    t0, bad = time.time(), []
    while True:
        st, shot = check(bg, hover)
        print(f"{time.time() - t0:5.0f}s  {st}  {shot or ''}", flush=True)
        if st != "OK":
            bad.append(st)
        if st == "GONE" or time.time() - t0 + every > secs:
            break
        time.sleep(every)
    print("VERDICT:", "working" if not bad else "PROBLEM - " + ", ".join(sorted(set(bad))))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
