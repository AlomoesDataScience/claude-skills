#!/usr/bin/env python3
"""Give one FoG II move order safely, in map coordinates (bgplay screen, top view, zoomed out).

  order.py move SC SR DC DR "NAME PART" [--go]    without --go: checks only (select, read name, hover target)
  order.py where C R                               pin the camera, hover square C,R, save the tooltip crop
  order.py present [--view C R]                    centre the camera for a human (minimap click), mouse on banner
EVERY command ends with present(): the corner pins are for measuring only and must never be left on
screen (the user 2026-11-02: "It's popping the camera in the corner, and that's not usable to a human").

1. pins the camera to the NW corner (then 90 ms east, so col 11 clears the minimap) (rows 0-10) or the SW corner (rows 11-23) and measures the inner map
   border (west x, north/south y) from the photo - square = 59.25 px
2. left-clicks the source square, reads the unit card name (OCR 500 758 730 782); wrong name -> deselect, stop
3. hovers the target, saves a tooltip crop (shows "Move Unit used/total" if reachable)
4. --go: right-clicks the target (opens Move Unit / Move Whole Command buttons ON the target; when only one
   order is possible it moves at once), left-clicks the target = Move Unit, reads the card AP after the move; parks the mouse on the score banner
Prints every check. Never touches End Turn. Keep squares between y 90 and 800: near the bottom edge the order buttons open sideways and the
square itself becomes Move Whole Command (2026-11-02, nearly happened). Do NOT press X (hides the whole UI in battle, card OCR then fails)."""
import os, subprocess, sys, time
import numpy as np
from PIL import Image

BG = os.path.expanduser("~/Desktop/AI Development/.claude/skills/game-ui/scripts/bgplay.py")
OUT = os.path.expanduser("~/.cache/game-ui/bg5/orders")
SQ = 59.25


def seq(*steps):
    r = subprocess.run([sys.executable, "-I", BG, "seq", *steps], capture_output=True, text=True)
    return r.stdout


def shot(*pre):
    return [l for l in seq(*pre, "shot --full").splitlines() if l.endswith(".png")][-1]


def measure(path, south):
    im = np.asarray(Image.open(path).convert("HSV")).astype(int)
    s = im[:, :, 1]
    xs = []
    for y in range(300, 700, 25):
        for x in range(400, 1300):
            if s[y, x] < 30 and im[y, x, 2] > 60 and (s[y, x + 1:x + 16] >= 30).all() \
                    and x >= 40 and (s[y, x - 39:x + 1] < 30).all():          # a real stone band, not a track
                xs.append(x + 1); break
    ys = []
    for x in range(900, 1300, 25):
        rng = range(895, 40, -1) if south else range(40, 880)
        for y in rng:
            if south:
                n = min(40, 899 - y)
                if s[y, x] < 30 and im[y, x, 2] > 60 and (s[y - 15:y, x] >= 30).all() \
                        and n >= 12 and (s[y:y + n, x] < 30).all():
                    ys.append(y); break
            elif s[y, x] < 30 and im[y, x, 2] > 60 and (s[y + 1:y + 16, x] >= 30).all() \
                    and y >= 40 and (s[y - 39:y + 1, x] < 30).all():
                ys.append(y + 1); break
    if not xs or not ys:
        sys.exit(f"border not found (west {xs[:3]}, edge {ys[:3]}) - look at {path}")
    x0 = int(np.median(xs)); e = int(np.median(ys))
    return x0, e


def pin(row):
    """Closed loop: corner first, then nudge until the border sits in a safe band (pans vary run to run).
    North view: west edge x0 in 530-640, north edge 100-190 (rows 0-10 at y 130-800).
    South view: x0 in 530-640, south edge 840-885 (rows 11-16 at y 99-440)."""
    south = row > 10
    seq("move 170 75", "hold a 4000", "hold s 4000" if south else "hold w 4000", "wait 1200")
    lo, hi = (840, 885) if south else (100, 190)
    for _ in range(24):
        p = shot("wait 900")
        try:
            x0, e = measure(p, south)
        except SystemExit:
            x0, e = None, None
        steps = []
        if x0 is None:
            steps.append("hold a 1500")          # border off screen = too far east: re-home west
        elif x0 > 640:
            steps.append("hold d 35")
        elif x0 < 530:
            steps.append("hold a 25")
        if e is None:
            steps.append("hold s 1500" if south else "hold w 1500")   # re-home to the corner
        elif e < lo:
            steps.append(("hold w 35" if lo - e > 90 else "hold w 12") if south else "hold w 25")
        elif e > hi:
            steps.append("hold s 25" if south else "hold s 35")
        if not steps:
            return x0, (e - 24 * SQ if south else e), p
        print(f"  camera x0 {x0} edge {e} -> {' '.join(steps)}")
        seq(*steps)
    sys.exit("could not settle the camera - look at " + p)


# Minimap (top view, game 1600x900 on bgplay): the map rectangle and px per square, measured 2026-11-02.
# A left-click there centres the camera on that map point (it lands at screen ~800,465).
MM_X0, MM_Y0, MM_SX, MM_SY = 1379.3, 776.7, 2.68, 2.64
VIEW = (19, 11.5)   # where the user looks: between the two armies (battle 2); override with --view C R


def present(c=None, r=None):
    """Leave the camera where a HUMAN can read it (idle-view): centred on the armies, mouse on the banner.
    Every command ends with this - corner pins are for measuring only."""
    c = VIEW[0] if c is None else c; r = VIEW[1] if r is None else r
    x, y = int(MM_X0 + c * MM_SX), int(MM_Y0 + r * MM_SY)
    seq(f"move {x} {y}", "wait 300", f"click {x} {y}", "wait 1500", "move 170 75", "wait 300")


def centre(x0, y0, c, r):
    return int(x0 + (c + 0.5) * SQ), int(y0 + (r + 0.5) * SQ)


def card_name():
    out = seq("read 500 758 730 782").splitlines()
    return " ".join(l for l in out if l and not l.startswith("[box]")).strip()


def card_ap():
    out = seq("read 440 835 580 880").splitlines()
    return " ".join(l for l in out if l and not l.startswith("[box]")).strip()


def crop(path, x, y, name):
    os.makedirs(OUT, exist_ok=True)
    X = min(max(x - 60, 0), 1600 - 460); Y = min(max(y - 40, 0), 990 - 160)
    Image.open(path).crop((X, Y, X + 460, Y + 160)).save(os.path.join(OUT, name))
    return os.path.join(OUT, name)


def main(a):
    if not a:
        sys.exit(__doc__)
    view = (float(a[a.index("--view") + 1]), float(a[a.index("--view") + 2])) if "--view" in a else (None, None)
    if a[0] == "present":
        present(*view); print("camera centred for review"); return
    if a[0] == "where":
        c, r = int(a[1]), int(a[2])
        x0, y0, _ = pin(r); x, y = centre(x0, y0, c, r)
        p = shot(f"move {x} {y}", "wait 1100")
        print("grid x0", x0, "y0", round(y0), "square", (x, y), "tooltip:", crop(p, x, y, f"where_{c}_{r}.png"))
        present(*view); return
    sc, sr, dc, dr, want = int(a[1]), int(a[2]), int(a[3]), int(a[4]), a[5]
    go = "--go" in a
    if max(sr, dr) <= 10:
        x0, y0, _ = pin(0)
    elif min(sr, dr) >= 11:
        x0, y0, _ = pin(23)
    else:
        sys.exit("move crosses rows 10/11 - split it or add a view")
    sx, sy = centre(x0, y0, sc, sr); tx, ty = centre(x0, y0, dc, dr)
    if not (30 < sy < 880 and 30 < ty < 880):
        sys.exit(f"squares off screen (src y {sy}, dst y {ty}) - rows too far apart for one view")
    for (x, y) in ((sx, sy), (tx, ty)):
        if y > 800 or y < 90:
            sys.exit(f"square at {x},{y} too near the screen edge - the order buttons open sideways there (Move Whole Command lands on the square)")
        if (1330 < x < 1515 and 715 < y < 900) or (310 < x < 795 and 740 < y < 900) or (1370 < x and y < 120):
            sys.exit(f"square at {x},{y} is under the minimap / unit card / End Turn - change the view")
    print(f"grid x0 {x0} y0 {round(y0)}  src ({sc},{sr})->{sx},{sy}  dst ({dc},{dr})->{tx},{ty}")
    seq(f"move {sx} {sy}", "wait 500", f"click {sx} {sy}", "wait 1000")
    name = card_name(); print("selected:", name)
    if want.lower() not in name.lower():
        present(*view); print("WRONG UNIT - stopped (still selected; left-click empty ground)"); sys.exit(1)
    p = shot(f"move {tx} {ty}", "wait 1100")
    print("target tooltip:", crop(p, tx, ty, f"t_{sc}_{sr}_{dc}_{dr}.png"))
    if not go:
        present(*view); return
    p = shot(f"click {tx} {ty} --right", "wait 1300", f"click {tx} {ty}", "wait 2500", "move 170 75", "wait 400")
    print("after move AP:", card_ap(), " shot:", p)
    present(*view)


if __name__ == "__main__":
    main(sys.argv[1:])
