#!/usr/bin/env python3
"""Give one FoG II move order safely, in map coordinates (bgplay screen, top view, zoomed out).

  order.py move SC SR DC DR "NAME PART" [--go]    without --go: checks only (select, read name, hover target)
  order.py where C R                               pin the camera, hover square C,R, save the tooltip crop
  order.py cal                                     calibrate the minimap (4 clicks + border measures) - once per map/zoom
  order.py present [--view C R]                    centre the camera for a human (minimap click), mouse on banner
  order.py reach C R "NAME"                        select, photograph its reach (white squares = where it can move)
  order.py turn SC SR TC TR "NAME" [--go]          face an ADJACENT square (hover icon first; Move+Turn -> lower button)
  order.py charge SC SR TC TR "NAME" [--show]      hover the target (charge icon/forecast); --show = 1st click only
                                                   (shows Win:Draw:Lose) - the 2nd click is done by hand after reading
  order.py shoot SC SR TC TR "NAME" [--go]         hover the target (shooting forecast); --go = right-click (Shoot)
  order.py cards C R [C R ...]                     hover squares and OCR the unit cards + tooltip (army-log)
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
from PIL import Image, ImageDraw

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
        for x in range(60, 1300):
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
    North view: west edge x0 in 440-520, north edge 90-160 (rows 0-10 at y 120-782).
    South view: x0 in 440-520, south edge 840-885 (rows 11-16 at y 99-440). Columns 0-16 clear the minimap."""
    south = row > 10
    seq("move 1578 448", "hold a 4000", "hold s 4000" if south else "hold w 4000", "wait 1200")
    lo, hi = (840, 885) if south else (90, 160)
    xlo, xhi = 440, 520              # west edge band: columns up to 16 stay clear of the minimap
    for _ in range(24):
        p = shot("wait 900")
        try:
            x0, e = measure(p, south)
        except SystemExit:
            x0, e = None, None
        steps = []
        if x0 is None:
            steps.append("hold a 1500")          # border off screen = too far east: re-home west
        elif x0 > xhi:
            steps.append("hold d 35" if x0 - xhi > 90 else "hold d 12")
        elif x0 < xlo:
            steps.append("hold a 12")
        if e is None:
            steps.append("hold s 1500" if south else "hold w 1500")   # re-home to the corner
        elif e < lo:
            steps.append("hold w 35" if lo - e > 90 else "hold w 12")
        elif e > hi:
            steps.append("hold s 35" if e - hi > 90 else "hold s 12")
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
    seq(f"move {x} {y}", "wait 300", f"click {x} {y}", "wait 1500", "move 1578 448", "wait 300")


CAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "ui", "minimap_cal.json")


def settle(limit=10.0):
    """Wait until the camera stops gliding: two photos in a row with the same map band."""
    t0 = time.time(); prev = None
    while time.time() - t0 < limit:
        cur = np.asarray(Image.open(shot("wait 400")).convert("L").crop((350, 250, 1330, 700)), dtype=np.int16)
        if prev is not None and np.abs(cur - prev).mean() < 0.8:
            return
        prev = cur
    print("  (camera still moving after", limit, "s)")


def mm_click(mx, my):
    seq("move 1578 448", f"move {mx} {my}", "wait 300", f"click {mx} {my}", "move 1578 448")
    settle()


def calibrate():
    """Click the minimap at 4 pixels near the NW corner, measure the west/north border each time, and fit
    map coordinate at screen centre (800,465) = a*px + b for each axis. Saved to ui/minimap_cal.json."""
    import json
    pts = []
    for (c, r) in ((6, 3), (10, 3), (6, 6), (10, 6)):
        mx, my = int(round(MM_X0 + c * MM_SX)), int(round(MM_Y0 + r * MM_SY))
        mm_click(mx, my)
        p = shot("move 1578 448", "wait 900")
        x0, e = measure(p, False)
        pts.append((mx, my, (800 - x0) / SQ, (465 - e) / SQ))
        print(f"  minimap ({mx},{my}) -> centre at map col {pts[-1][2]:.2f} row {pts[-1][3]:.2f}")
    X = np.array([[q[0], 1] for q in pts]); Y = np.array([[q[1], 1] for q in pts])
    ax, bx = np.linalg.lstsq(X, np.array([q[2] for q in pts]), rcond=None)[0]
    ay, by = np.linalg.lstsq(Y, np.array([q[3] for q in pts]), rcond=None)[0]
    json.dump({"ax": ax, "bx": bx, "ay": ay, "by": by, "points": pts}, open(CAL, "w"), indent=1)
    print(f"col = {ax:.4f}*px + {bx:.2f}   row = {ay:.4f}*py + {by:.2f}   saved {CAL}")


def look_at(c, r):
    """Put map point (c, r) at the screen centre by a minimap click (the user 2026-11-02: show the location
    you want, don't steer by key presses). Returns screen(col,row) -> pixel centre of that square,
    computed from the point the click really centres on."""
    import json
    k = json.load(open(CAL))
    mx = int(round((c - k["bx"]) / k["ax"])); my = int(round((r - k["by"]) / k["ay"]))
    mm_click(mx, my)
    cc, rc = k["ax"] * mx + k["bx"], k["ay"] * my + k["by"]
    return lambda col, row: (int(800 + (col + 0.5 - cc) * SQ), int(465 + (row + 0.5 - rc) * SQ))


RESNAP = os.path.expanduser("~/Desktop/AI Development/.claude/skills/map-measure/scripts/resnap.py")
REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "ui", "map_ref_battle2.png")


def snap(path):
    """Exact grid on this screenshot by matching it against the reference map picture (map-measure
    resnap.py). Tries this zoom first, then a zoom search. Returns screen(col,row) or exits."""
    res = []
    for extra in ([], ["--zoom", "0.9", "3"]):
        out = subprocess.run([sys.executable, "-I", RESNAP, "find", REF, path, *extra],
                             capture_output=True, text=True).stdout.split()
        res.append((float(out[7]), float(out[1]), float(out[3]), float(out[5])))
        if not extra and res[0][0] >= 0.6:
            break                          # normal zoom, clear match: done
    m1 = res[0]; best = m1
    if len(res) > 1 and res[1][0] > m1[0] + 0.1:
        best = res[1]                      # zoomed view: only when clearly better
    m, S, x0, y0 = best
    if m >= 0.4:
        print(f"  snapped: square {S:.1f} px, map corner at ({x0:.0f},{y0:.0f}), match {m:.2f}")
        f = lambda c, r: (int(x0 + (c + 0.5) * S), int(y0 + (r + 0.5) * S))
        f.grid = (S, x0, y0)
        return f
    sys.exit(f"could not snap the grid (best match {m:.2f}) - look at {path}")


def snapview(c, r):
    """Show map point (c,r) near the screen centre (minimap click, approximate), then snap the grid exactly."""
    # keep the view inside the 32x24 map: centring past the edge shows the black margin and the snap then
    # latches on squares off (turn 7: reserve at col 28 read as the border, match 0.69)
    c = min(max(c, 8.0), 24.0); r = min(max(r, 7.0), 17.0)
    look_at(c, r)
    return snap(shot("move 1578 448", "wait 300"))


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
    X = min(max(x - 60, 0), 1600 - 460); Y = min(max(y - 40, 0), 990 - 280)
    Image.open(path).crop((X, Y, X + 460, Y + 280)).save(os.path.join(OUT, name))
    return os.path.join(OUT, name)


def main(a):
    if not a:
        sys.exit(__doc__)
    view = (float(a[a.index("--view") + 1]), float(a[a.index("--view") + 2])) if "--view" in a else (None, None)
    if a[0] == "cal":
        calibrate(); present(*view); return
    if a[0] == "grid":                   # order.py grid [C R]: snapped, labelled photo of the view for checks
        if len(a) > 2 and a[1] != "--view":
            look_at(float(a[1]), float(a[2]))
        p = shot("move 1578 448", "wait 300"); S, x0, y0 = snap(p).grid
        im = Image.open(p).convert("RGB"); d = ImageDraw.Draw(im)
        for c in range(0, 33):
            X = x0 + c * S; d.line([X, 30, X, 900], fill=(255, 255, 0)); d.text((X + 3, 252), str(c), fill="yellow")
        for r in range(0, 25):
            Y = y0 + r * S; d.line([0, Y, 1600, Y], fill=(255, 255, 0)); d.text((335, Y + 3), str(r), fill="yellow")
        out = os.path.join(OUT, "grid.png"); im.crop((0, 30, 1600, 900)).save(out); print("gridded photo:", out)
        present(*view); return
    if a[0] == "present":
        present(*view); print("camera centred for review"); return
    if a[0] == "cards":                  # order.py cards C R [C R ...]: hover each square, OCR the unit card (army-log)
        sq = [(int(a[i]), int(a[i + 1])) for i in range(1, len(a) - 1, 2) if a[i] != "--view" and a[i - 1] != "--view"]
        mc = sum(c for c, _ in sq) / len(sq) + 0.5; mr = sum(r for _, r in sq) / len(sq) + 0.5
        scr = snapview(mc, mr)
        for c, r in sq:
            x, y = scr(c, r)
            if not (90 < y < 740) or (1330 < x and y > 700) or (x < 330 and y < 250):
                print(f"({c},{r}): off the readable area (y {y}) - call again centred nearer"); continue
            # our card: bottom-middle (440-790); enemy card: bottom-right (815-1160); cursor tooltip: name, general, terrain
            out = seq(f"move {x} {y}", "wait 1100", f"read {x + 45} {y + 35} {x + 265} {y + 140}",
                      "read 815 755 1160 895", "read 440 755 790 895").splitlines()
            txt = " | ".join(l.strip() for l in out if l.strip() and not l.startswith("[box]"))
            print(f"({c},{r}): {txt}")
        present(*view); return
    if a[0] in ("turn", "charge", "reach"):
        sc, sr = int(a[1]), int(a[2])
        tc, tr = (int(a[3]), int(a[4])) if a[0] != "reach" else (sc, sr)
        want = a[5] if a[0] != "reach" else a[3]
        if a[0] == "turn" and max(abs(tc - sc), abs(tr - sr)) != 1:
            sys.exit("turn target must be an ADJACENT square (the user) - one of the 8 around the unit")
        scr = snapview((sc + tc + 1) / 2, (sr + tr + 1) / 2); sx, sy = scr(sc, sr); tx, ty = scr(tc, tr)
        seq(f"move {sx} {sy}", "wait 500", f"click {sx} {sy}", "wait 1000")
        name = card_name(); print("selected:", name, "|", card_ap())
        if want.lower() not in name.lower():
            present(*view); print("WRONG UNIT - stopped"); sys.exit(1)
        # the white squares around a selected unit = where it can move this turn (the user) - always photograph them
        p = shot("move 1578 448", "wait 400"); X0, Y0 = max(sx - 300, 0), max(sy - 300, 30)
        Image.open(p).crop((X0, Y0, min(X0 + 600, 1600), min(Y0 + 600, 900))).save(os.path.join(OUT, f"reach_{sc}_{sr}.png"))
        print("reach (white squares):", os.path.join(OUT, f"reach_{sc}_{sr}.png"))
        if a[0] == "reach":
            present(*view); return
        # hover until the order icon / forecast shows (a right-click without the hover did nothing, turn 7)
        p = shot(f"move {tx} {ty}", "wait 1500")
        print("hover:", crop(p, tx, ty, f"{a[0]}_{sc}_{sr}_{tc}_{tr}.png"), " full:", p)
        if a[0] == "turn" and "--go" in a:
            before = card_ap(); seq(f"click {tx} {ty} --right", "wait 1800")
            if card_ap() == before:      # Move AND Turn possible: two stacked buttons, Turn is the LOWER one
                p = shot("wait 200"); print("buttons:", crop(p, tx, ty, f"turnbtn_{sc}_{sr}_{tc}_{tr}.png"))
                seq(f"move {tx} {ty + int(SQ)}", "wait 900", f"click {tx} {ty + int(SQ)}", "wait 1800")
            seq("move 1578 448", "wait 400"); print("after:", card_ap())
        if a[0] == "charge" and "--show" in a:
            # FIRST click only: shows Win:Draw:Lose (manual 13; click TWICE to charge). Nothing is committed here.
            p = shot(f"click {tx} {ty} --right", "wait 1800")
            print("after 1st click (read Win:Draw:Lose; the 2nd click is a separate, deliberate step):",
                  crop(p, tx, ty, f"charge1_{sc}_{sr}_{tc}_{tr}.png"), " full:", p)
            return                       # leave the screen as it is - no present(), no mouse move
        present(*view); return
    if a[0] == "shoot":                  # order.py shoot SC SR TC TR "NAME" [--go]: select, name check, hover target (+Ctrl detail)
        sc, sr, tc, tr, want = int(a[1]), int(a[2]), int(a[3]), int(a[4]), a[5]
        scr = snapview((sc + tc + 1) / 2, (sr + tr + 1) / 2); sx, sy = scr(sc, sr); tx, ty = scr(tc, tr)
        seq(f"move {sx} {sy}", "wait 500", f"click {sx} {sy}", "wait 1000")
        name = card_name(); print("selected:", name)
        if want.lower() not in name.lower():
            present(*view); print("WRONG UNIT - stopped"); sys.exit(1)
        p = shot(f"move {tx} {ty}", "wait 1300")
        print("target hover:", crop(p, tx, ty, f"s_{sc}_{sr}_{tc}_{tr}.png"), " full:", p)
        if "--go" in a:                  # right-click = Shoot (photo after; nothing else clicked)
            p = shot(f"click {tx} {ty} --right", "wait 3500", "move 1578 448", "wait 500")
            print("after shoot:", p, " card:", card_ap())
        present(*view); return
    if a[0] == "where":
        c, r = int(a[1]), int(a[2])
        scr = snapview(c + 0.5, r + 0.5); x, y = scr(c, r)
        p = shot(f"move {x} {y}", "wait 1100")
        print("square", (x, y), "tooltip:", crop(p, x, y, f"where_{c}_{r}.png"))
        present(*view); return
    sc, sr, dc, dr, want = int(a[1]), int(a[2]), int(a[3]), int(a[4]), a[5]
    go = "--go" in a
    scr = snapview((sc + dc + 1) / 2, (sr + dr + 1) / 2)        # both squares near the centre, grid snapped
    sx, sy = scr(sc, sr); tx, ty = scr(dc, dr)
    if not (30 < sy < 880 and 30 < ty < 880):
        sys.exit(f"squares off screen (src y {sy}, dst y {ty}) - rows too far apart for one view")
    for (x, y) in ((sx, sy), (tx, ty)):
        if y > 800 or y < 90:
            sys.exit(f"square at {x},{y} too near the screen edge - the order buttons open sideways there (Move Whole Command lands on the square)")
        if (1330 < x < 1515 and 715 < y < 900) or (310 < x < 795 and 740 < y < 900) or (1370 < x and y < 120):
            sys.exit(f"square at {x},{y} is under the minimap / unit card / End Turn - change the view")
    print(f"view centred  src ({sc},{sr})->{sx},{sy}  dst ({dc},{dr})->{tx},{ty}")
    seq(f"move {sx} {sy}", "wait 500", f"click {sx} {sy}", "wait 1000")
    name = card_name(); print("selected:", name)
    if want.lower() not in name.lower():
        present(*view); print("WRONG UNIT - stopped (still selected; left-click empty ground)"); sys.exit(1)
    p = shot(f"move {tx} {ty}", "wait 1100")
    print("target tooltip:", crop(p, tx, ty, f"t_{sc}_{sr}_{dc}_{dr}.png"))
    if not go:
        present(*view); return
    p = shot(f"click {tx} {ty} --right", "wait 1300", f"click {tx} {ty}", "wait 2500", "move 1578 448", "wait 400")
    print("after move AP:", card_ap(), " shot:", p)
    present(*view)


if __name__ == "__main__":
    main(sys.argv[1:])
