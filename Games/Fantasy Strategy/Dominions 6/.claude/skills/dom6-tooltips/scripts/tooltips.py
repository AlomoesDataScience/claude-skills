"""Read Dominions 6 tooltips: hover each target at its centre, wait, and OCR the tooltip.

  python3 -I tooltips.py [--wait S] [--box X0,Y0,X1,Y1] [--shot] TARGET...

TARGET is "X,Y" (a point you measured: the centre of the word or number) or a piece of on-screen
text, which is found by OCR and hovered at the centre of its box. OCR often merges neighbouring
labels ("0/1  0/10") into one box; then measure the points from a screenshot and pass X,Y.
--box is where the tooltip shows (default: the bottom bar, y = height-69 .. height-12, which is
where Army Setup, the map and most screens put it). --shot also saves a full screenshot per
target to ~/.cache/dom6ui/tip_N.png, to find where a new screen puts its tooltips.
Between targets the mouse rests inside the window's bottom-right corner so the old tip clears.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "dom6-ui", "scripts"))
import vision as V                                # noqa: E402  (first: puts game-ui on the path)
import session                                    # noqa: E402
import dom6ui as U                                # noqa: E402


def centre(box):
    x0, y0, x1, y1 = box
    return (x0 + x1) // 2, (y0 + y1) // 2


def find(im, text):
    """Centre of the on-screen text that best matches `text`, or None."""
    T = [t for w in V.scene(im)["windows"] for t in w["text"] + w["bars"] if t.get("text")]
    best = V.closest(text, [t["text"].strip() for t in T], 0.6)
    for t in T:
        if best and t["text"].strip() == best:
            return centre(t["box"])
    return None


def read(g, targets, wait=2.0, box=None, shot=False):
    im = g.grab()
    w, h = im.size
    rest = (w - 20, h - 14)
    box = box or (300, h - 69, w - 300, h - 12)
    out = []
    for i, t in enumerate(targets):
        if "," in t and t.replace(",", "").strip().isdigit():
            pt = tuple(int(v) for v in t.split(","))
        else:
            pt = find(g.grab(), t)
            if pt is None:
                out.append((t, None, "(text not found on screen)"))
                continue
        g.hover(*pt, wait=wait)
        im = g.grab()
        if shot:
            im.save(os.path.join(U.OUT, f"tip_{i}.png"))
        tip = V.ocr(im, [box], [True], psm=6)[0]["text"].strip().strip("|}{ ").replace("\n", " ")
        out.append((t, pt, tip))
        g.hover(*rest, wait=0.5)
    return out


def main(a):
    wait, box, shot = 2.0, None, False
    if "--wait" in a:
        i = a.index("--wait"); wait = float(a[i + 1]); del a[i:i + 2]
    if "--box" in a:
        i = a.index("--box"); box = tuple(int(v) for v in a[i + 1].split(",")); del a[i:i + 2]
    if "--shot" in a:
        a.remove("--shot"); shot = True
    if not a:
        print(__doc__)
        return
    session.run(lambda g: [print(f"{t} @ {pt}: {tip}") for t, pt, tip in read(g, a, wait, box, shot)], "tips")


if __name__ == "__main__":
    main(sys.argv[1:])
