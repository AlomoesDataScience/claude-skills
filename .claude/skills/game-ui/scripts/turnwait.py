#!/usr/bin/env python3
"""Know when it is my turn again in a turn-based game (bgplay screen).
Compares a box of the screen (e.g. the End Turn button) with a reference picture taken on MY turn;
a --mask box inside it (e.g. the turn number text, which changes) is ignored.

  turnwait.py make REF.png SHOT.png --box X0 Y0 X1 Y1            cut the reference from a screenshot
  turnwait.py check REF.png [SHOT.png] --box ... [--mask ...]     prints MINE / NOT score
  turnwait.py wait REF.png --box ... [--mask ...] [--min 8] [--max 90]
      after End Turn: sleep --min s (the user: assume the AI turn takes 5-10 s), then poll every 1 s until
      the box matches twice in a row, then 1.5 s settle; prints MINE after N s, or TIMEOUT.
  turnwait.py test REF.png SHOTS... --box ... [--mask ...]        score saved frames (calibration)
Match = mean abs grey difference < --thr (default 4; FoG II: mine 0.0-0.4, Enemy Turn banner 48, End Turn confirm open 11.6)."""
import os, subprocess, sys, time
import numpy as np
from PIL import Image

BG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bgplay.py")


def arg(a, k, n=4):
    if k not in a:
        return None
    i = a.index(k)
    return [int(x) for x in a[i + 1:i + 1 + n]]


def shot():
    out = subprocess.run([sys.executable, "-I", BG, "seq", "shot --full"], capture_output=True, text=True).stdout
    return [l for l in out.splitlines() if l.endswith(".png")][-1]


def score(ref, path, box, mask):
    a = np.asarray(Image.open(path).convert("L").crop(box), dtype=np.float32)
    r = np.asarray(Image.open(ref).convert("L"), dtype=np.float32)
    keep = np.ones_like(r, bool)
    if mask:
        keep[mask[1] - box[1]:mask[3] - box[1], mask[0] - box[0]:mask[2] - box[0]] = False
    return float(np.abs(a - r)[keep].mean())


def main(a):
    if len(a) < 2:
        sys.exit(__doc__)
    cmd, ref = a[0], a[1]
    box, mask = arg(a, "--box"), arg(a, "--mask")
    thr = float(a[a.index("--thr") + 1]) if "--thr" in a else 4.0
    if cmd == "make":
        Image.open(a[2]).convert("L").crop(box).save(ref); print("ref", ref); return
    if cmd == "check":
        p = a[2] if len(a) > 2 and a[2].endswith(".png") else shot()
        s = score(ref, p, box, mask); print(("MINE" if s < thr else "NOT"), f"{s:.1f}", p); return
    if cmd == "test":
        for p in [x for x in a[2:] if x.endswith(".png")]:
            s = score(ref, p, box, mask); print(f"{os.path.basename(p)} {s:5.1f} {'MINE' if s < thr else 'not'}")
        return
    if cmd == "wait":
        mn = float(a[a.index("--min") + 1]) if "--min" in a else 8
        mx = float(a[a.index("--max") + 1]) if "--max" in a else 90
        t0 = time.time(); time.sleep(mn); hits = 0
        while time.time() - t0 < mx:
            s = score(ref, shot(), box, mask)
            hits = hits + 1 if s < thr else 0
            if hits >= 2:
                time.sleep(1.5); print(f"MINE after {time.time() - t0:.0f} s (score {s:.1f})"); return
            time.sleep(1)
        print("TIMEOUT - look at the screen"); sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
