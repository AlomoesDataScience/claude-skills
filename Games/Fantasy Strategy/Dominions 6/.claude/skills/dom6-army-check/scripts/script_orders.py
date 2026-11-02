"""Set a commander's battle script in an open Army Setup screen.

  python3 -I script_orders.py NAME [--spell "Spell"]... [--main "Cast spells"] [--target "closest enemy"]
                              [--keep] [--read]

NAME is the name on the commander's token (e.g. Apuleius). The script is cleared first (every
<del>) unless --keep; each --spell adds a "Cast a specific spell" step (up to five), picked by
clicking the centre of its text in Choose spell; greyed (uncastable) spells are refused. --main
sets the main order (None, Stay behind troops, Attack, Cast spells, Advance and cast spells,
Retreat), --target its target. --read only prints the current script and main order. Ok closes.
Uses dom6-ui's guard; aim rules from dom6-tooltips (centre of the text).
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "dom6-ui", "scripts"))
import session                                    # noqa: E402
import vision as V                                # noqa: E402


MAIN = ("None", "Stay behind troops", "Attack", "Cast spells", "Advance and cast spells", "Retreat")


class Fail(Exception):
    pass


def texts(im):
    return [t for w in V.scene(im)["windows"] for t in w["text"] + w["bars"] if t.get("text")]


def clean(t):
    """Drop radio marks ("X ", "O ", "KO. ") and script brackets OCR leaves around a label."""
    t = re.sub(r"^[\[(|]?\s*[OX0xK]{1,2}\.?\s+(?=[A-Za-z])", "", t.strip())
    return t.strip("()[] ")


def mid(b):
    return (b[0] + b[2]) // 2, (b[1] + b[3]) // 2


def find(T, name, cut=0.8, region=None):
    best, score = None, 0
    for t in T:
        b = t["box"]
        if region and not (region[0] <= mid(b)[0] <= region[2] and region[1] <= mid(b)[1] <= region[3]):
            continue
        s = V.closest(name, [clean(t["text"])], cut) or clean(t["text"]).lower().startswith(name.lower())
        if s:
            r = len(set(name.lower()) & set(t["text"].lower())) / max(len(set(name.lower())), 1)
            if r > score:
                best, score = t, r
    return best


def rest(g):
    w, h = g.grab().size
    g.hover(w - 20, h - 14, wait=0.4)


def open_orders(g, name):
    T = texts(g.grab())
    tok = find(T, name)
    if not tok:
        raise Fail(f"commander {name} not on screen")
    ty = mid(tok["box"])[1]
    bars = [t for t in T if "set battle orders" in t["text"] or t["box"][0] in range(560, 600)]
    bars = [t for t in bars if abs(mid(t["box"])[1] - ty) < 25 and t["box"][0] > tok["box"][2]]
    if not bars:
        raise Fail(f"no order bar on {name}'s row")
    g.click(*mid(bars[0]["box"]), wait=1.2)
    T = texts(g.grab())
    if not find(T, "Single Round Orders", 0.7):
        raise Fail("the battle orders window did not open")


def read_window(g):
    T = texts(g.grab())
    script = [clean(t["text"]) for t in sorted(T, key=lambda t: t["box"][1])
              if t["box"][1] < 222 and t["box"][0] < 1000 and t["text"].strip().endswith(")")]
    # the selected main order: its radio mark is an X (ink in the middle), the others are O rings
    im = g.grab().convert("L")
    main = []
    for t in T:
        x0, y0, x1, y1 = t["box"]
        name = clean(t["text"])
        if not (500 < y0 < 680 and x0 < 900 and name in MAIN):
            continue
        cy = (y0 + y1) // 2
        mx = 707                                  # centre of the radio marks' column
        core = [im.getpixel((mx + dx, cy + dy)) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
        if min(core) < 90:
            main.append(name)
    return script, main


def clear(g):
    for _ in range(6):
        T = texts(g.grab())
        d = [t for t in T if "del" in t["text"] and t["box"][1] < 250]
        if not d:
            return
        g.click(*mid(d[0]["box"]), wait=0.8)


def pick_spell(g, spell):
    T = texts(g.grab())
    c = find(T, "Cast a specific spell", 0.8)
    if not c:
        raise Fail("no 'Cast a specific spell' (not a spellcaster?)")
    g.click(*mid(c["box"]), wait=1.2)
    g.scroll(False, 40, at=(960, 500))
    rest(g)
    for page in range(6):
        im = g.grab()
        T = texts(im)
        t = find(T, spell, 0.85, region=(700, 40, 1220, 990))
        if t:
            x0, y0, x1, y1 = t["box"]
            lum = sorted(im.convert("L").crop((x0, y0, x1, y1)).getdata())[-10:]
            if sum(lum) / len(lum) < 170:          # greyed: the mage lacks the path level
                ex = find(T, "Exit", 0.9)
                g.click(*mid(ex["box"]), wait=1.0)
                raise Fail(f"{spell} is greyed out for this mage")
            g.click(*mid(t["box"]), wait=1.2)
            return
        g.scroll(True, 10, at=(960, 500))
        rest(g)
    ex = find(texts(g.grab()), "Exit", 0.9)
    if ex:
        g.click(*mid(ex["box"]), wait=1.0)
    raise Fail(f"{spell} not in the spell list")


def set_radio(g, label, xmax):
    T = texts(g.grab())
    t = find(T, label, 0.8, region=(640, 500, xmax, 720))
    if not t:
        raise Fail(f"no '{label}' in the order window")
    g.click(*mid(t["box"]), wait=0.8)


def work(g, a):
    name = a[0]
    spells = [a[i + 1] for i, v in enumerate(a) if v == "--spell"]
    main = a[a.index("--main") + 1] if "--main" in a else None
    target = a[a.index("--target") + 1] if "--target" in a else None
    open_orders(g, name)
    if "--read" not in a:
        if "--keep" not in a:
            clear(g)
        for s in spells:
            pick_spell(g, s)
        if main:
            set_radio(g, main, 940)
        if target:
            set_radio(g, target, 1220)
    script, mo = read_window(g)
    print(f"{name}: script {script or '(none)'}; main {mo}")
    ok = find(texts(g.grab()), "Ok", 0.9, region=(900, 760, 1020, 840))
    if not ok:
        raise Fail("no Ok button found; the order window is still open")
    for _ in range(3):                            # a click right after the read is sometimes lost
        g.hover(*mid(ok["box"]), wait=0.4)
        g.click(*mid(ok["box"]), wait=1.0)
        if not find(texts(g.grab()), "Single Round Orders", 0.7):
            return
    raise Fail("Ok did not close the order window")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit()
    def run(g):
        try:
            work(g, sys.argv[1:])
        except Fail as e:
            print("FAILED:", e)
    session.run(run, "orders")
