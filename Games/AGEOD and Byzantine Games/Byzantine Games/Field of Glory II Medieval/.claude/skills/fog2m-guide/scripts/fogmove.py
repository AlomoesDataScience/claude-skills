#!/usr/bin/env python3
"""One FoG II Medieval order on the bgplay screen, checked.

  fogmove.py X Y TX TY [--expect TEXT] [--whole]     move the unit at X,Y to square TX,TY
  fogmove.py --undo X Y                              undo the last move of the unit at X,Y

Move: hover X,Y and read the tooltip - with --expect, stop unless TEXT is in it (the camera follows
moving units, so coordinates go stale after every order). Then left-click the unit, hover the target,
right-click it. With several possible orders the game opens big buttons: ▲ Move Unit on the target
and a blue ▲▲▲ Move Whole Command under it; the helper sees the blue one and left-clicks ▲ (▲▲▲ with
--whole). One possible order = the unit moves at once. Prints the unit hovered and what happened.
Undo: select, right-click its own square (green ↶ appears there), left-click it.
One order per call, then Space (deselect). Re-check positions before the next call.
"""
import os
import subprocess
import sys

from PIL import Image

BG = os.path.expanduser("~/Desktop/AI Development/.claude/skills/game-ui/scripts/bgplay.py")


def seq(*steps):
    r = subprocess.run([sys.executable, "-I", BG, "seq", *steps], capture_output=True, text=True)
    return r.stdout


def shots(out):
    return [ln for ln in out.splitlines() if ln.endswith(".png")]


def tooltip(x, y):
    out = seq(f"move {x} {y}", "wait 1100", f"read {x - 10} {y - 10} {x + 540} {y + 150}")
    return " ".join(ln.strip() for ln in out.splitlines()
                    if ln.strip() and not ln.startswith("[") and not ln.endswith(".png"))


def blue_at(img, x, y):
    px = list(img.crop((x - 20, y - 20, x + 20, y + 20)).convert("RGB").getdata())
    r, g, b = (sum(p[i] for p in px) / len(px) for i in range(3))
    return b > 90 and b > r + 35 and b > g + 12        # Move Whole Command blue measured (53, 92, 113)


def main(a):
    if "--undo" in a:
        x, y = map(int, a[a.index("--undo") + 1:a.index("--undo") + 3])
        print("unit:", tooltip(x, y)[:90])
        seq(f"click {x} {y}", "wait 1000", f"click {x} {y} --right", "wait 1400", f"click {x} {y}",
            "wait 2200", "key space", "wait 400")
        return print("undo clicked - check the screen")
    expect = a[a.index("--expect") + 1] if "--expect" in a else None
    whole = "--whole" in a
    nums = [int(v) for v in a if v.isdigit()]
    if len(nums) != 4:
        sys.exit(__doc__)
    x, y, tx, ty = nums
    tip = tooltip(x, y)
    print("unit:", tip[:90])
    if expect and expect.lower() not in tip.lower():
        sys.exit(f"STOP: expected '{expect}' at {x},{y} - camera moved? re-locate the unit")
    out = seq(f"click {x} {y}", "wait 900", f"move {tx} {ty}", "wait 900",
              f"click {tx} {ty} --right", "wait 1300", "shot --full")
    s = shots(out)
    if s and blue_at(Image.open(s[-1]), tx, ty + 60):
        bx, by = (tx, ty + 60) if whole else (tx, ty)
        seq(f"click {bx} {by}", "wait 2200")
        print("menu -> clicked", "Move Whole Command" if whole else "Move Unit")
    else:
        print("single order given (or nothing allowed there) - check the screen")
    seq("key space", "wait 400")


if __name__ == "__main__":
    main(sys.argv[1:])
