"""Review a Dominions 6 battle from its replay: what each side lost, who hit whom, when, and what
every unit ended with. Part of the dom6-battle-view skill; feeds the dom6-tactics battle log.

  python3 -I battle_review.py record NAME [--fast] [--no-units] [--units-only]
        Start on the Battle Summary of the battle (click the battle message's text in Messages).
        1. reads the summary (units, count, wounded, dead per side);
        2. pass 1: View Battle, log detail 4, round counter on, then captures the log panel and a
           field frame while the replay plays, until it closes by itself at the end;
        3. pass 2 (unless --no-units): View Battle again at turbo, pauses on the last round seen
           in pass 1 and saves the F1 Unit Overview's pages as pictures (read by `report`: type,
        side, HP, fatigue, XP, dead/retreated). --units-only repeats pass 2 alone.
  python3 -I battle_review.py units NAME
        With the F1 Unit Overview already open in a paused replay: save its pages and read them. Raw captures go to ~/.cache/game-ui/dom6_amd64/battles/NAME/.
  python3 -I battle_review.py report NAME [--out FILE.md]
        OCRs the captures, stitches the log, parses the events and writes the report (default:
        ../battles/NAME.md in this skill) plus a contact sheet of field frames.

Input goes through dom6-ui's guard (waits for the user to be idle, works only while the game is
focused). The replay closes by itself when the battle ends, so the log can only be read while it
plays; `-` and `+` resize the log panel, they do not scroll it.
"""
import json
import os
import re
import sys
import time
from difflib import SequenceMatcher

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "dom6-ui", "scripts"))
import vision as V                                # noqa: E402  (first: puts game-ui on the path)
import session                                    # noqa: E402
import dom6ui as U                                # noqa: E402
from session import Stop                          # noqa: E402
from PIL import Image, ImageChops, ImageStat     # noqa: E402

BASE = os.path.join(U.OUT, "battles")
LOG_STRIP = (0, 0, 1920, 310)                     # log panel (top left) + round counter (top right)
LOG_LINES = [(10, y, 935, y + 25) for y in range(44, 300, 25)]
ROUND_BOX = (1640, 62, 1820, 88)                  # "Combat round N" after `r`
VIEW_BATTLE = (959, 726)                          # the words on the Battle Summary
VIEW_BOX = (880, 715, 1040, 740)
F1_ROW0, F1_DY, F1_ROWS = 107, 28.5, 29           # Unit Overview rows (full screen)
F1_COLS = {"type": (660, 870), "hp": (950, 1000), "fp": (1018, 1068), "xp": (1088, 1138), "status": (1160, 1270)}
F1_FLAG_X = (888, 906)


def ocr1(im, box, light=True):
    return V.ocr(im, [box], [light])[0]["text"].strip()


def digits(im, box):
    """A number in a small box, or 0 when the box has no bright (text) pixels: OCR of an empty box
    invents digits."""
    px = im.convert("L").crop(box).getdata()
    if sum(1 for p in px if p > 100) < 6:
        return "0"
    t = V.ocr(im, [box], [True], psm=7)[0]["text"]
    return (re.findall(r"\d+", t) or ["0"])[0]


DIGITS = {d: tuple(rows) for d, rows in json.load(open(os.path.join(HERE, "round_digits.json"))).items()}


def round_no(im):
    """The replay's "Combat round N" (after `r`), read by matching the white digit shapes to
    templates (OCR confuses this font: G for 0, / for 7, & for 8). The first glyph in the box is
    the "d" of "round"; None when the counter is not shown."""
    c = im.convert("L").crop((1770, 60, 1840, 88))
    w, h = c.size
    px = c.load()
    on = lambda x, y: px[x, y] > 225
    cols = [any(on(x, y) for y in range(h)) for x in range(w)]
    gl, x = [], 0
    while x < w:
        if cols[x]:
            a = x
            while x < w and cols[x]:
                x += 1
            gl.append(tuple("".join("1" if on(i, y) else "0" for i in range(a, x)) for y in range(h)))
        else:
            x += 1
    if len(gl) < 2:
        return None
    out = ""
    for g in gl[1:]:
        best, score = None, -1
        for d, t in DIGITS.items():
            if len(t[0]) != len(g[0]):
                continue
            sc = sum(a == b for ra, rb in zip(t, g) for a, b in zip(ra, rb))
            if sc > score:
                best, score = d, sc
        if best is None or score < 0.9 * len(g) * len(g[0]):
            return None
        out += best
    return int(out)


def on_summary(g):
    return "View" in ocr1(g.grab(), VIEW_BOX)


def locate_view(im):
    """Move VIEW_BATTLE / VIEW_BOX to where this summary shows "View Battle": the summary's
    height grows with the number of unit rows (Murias 726, Copper Woods 758)."""
    global VIEW_BATTLE, VIEW_BOX
    for w in V.scene(im)["windows"]:
        for t in w["text"] + w["bars"]:
            if "View Battle" in (t.get("text") or ""):
                x0, y0, x1, y1 = t["box"]
                ym = (y0 + y1) // 2
                VIEW_BATTLE, VIEW_BOX = ((x0 + x1) // 2, ym), (880, ym - 11, 1040, ym + 14)
                return True
    return False


# ------------------------------------------------------------------ the Battle Summary

def read_summary(im):
    """Rows of the Battle Summary: side headers 'Forces of X', then unit rows with count, wounded
    (slash icon) and dead (figure icon) columns, read in fixed boxes."""
    T = sorted([t for w in V.scene(im)["windows"] for t in w["text"] + w["bars"] if t.get("text")],
               key=lambda t: (t["box"][1], t["box"][0]))
    out, side = {"title": "", "result": "", "sides": []}, None
    for t in T:
        x0, y0, x1, y1 = t["box"]
        s = t["text"].strip()
        if "battle in" in s:
            out["title"] = s
        elif "conquered" in s or "defended" in s or "repelled" in s or "failed" in s:
            out["result"] += s + " "
        elif "Forces of" in s:
            side = {"side": s[s.index("Forces of") + 10:].strip(), "units": []}
            out["sides"].append(side)
        elif side is not None and 670 <= x0 <= 700 and s not in ("View Battle", "Exit"):
            ym = (y0 + y1) // 2
            row = {"unit": s, "count": int(digits(im, (1062, ym - 11, 1125, ym + 11))),
                   "wounded": int(digits(im, (1169, ym - 11, 1216, ym + 11))),   # after the sword icon
                   "dead": int(digits(im, (1239, ym - 11, 1295, ym + 11)))}      # after the grave icon
            (side.setdefault("total", row) if s == "Total" else side["units"].append(row))
    return out


# ------------------------------------------------------------------ recording

def start_replay(g, wait=3.5):
    if not on_summary(g) and not locate_view(g.grab()):
        raise Stop("not on the Battle Summary (View Battle not found)")
    g.click(*VIEW_BATTLE, wait=wait)
    g.hover(1910, 1040, wait=0.2)
    if round_no(g.grab()) is None:                # `r` is a toggle that persists between replays
        g.key("r", wait=0.4)
        g.hover(1910, 1040, wait=0.2)


def record(g, name, fast=False, units=True, units_only=False):
    d = os.path.join(BASE, name)
    if units_only:                                # pass 2 again, with the round count from pass 1
        last_round = json.load(open(os.path.join(d, "meta.json")))["last_round"]
        return units_pass(g, d, last_round)
    os.makedirs(os.path.join(d, "log"), exist_ok=True)
    os.makedirs(os.path.join(d, "field"), exist_ok=True)
    im = g.grab()
    im.save(os.path.join(d, "summary.png"))
    summ = read_summary(im)
    json.dump(summ, open(os.path.join(d, "summary.json"), "w"), indent=1)
    print("summary:", summ["title"], "|", summ["result"].strip(), flush=True)

    # pass 1: the log
    start_replay(g)
    g.key("4", wait=0.2)
    if fast:
        g.key("f", wait=0.2)
    last, n, t_field, t_check, t0 = None, 0, 0, 0, time.time()
    while time.time() - t0 < 900:
        im = g.grab()
        strip = im.crop(LOG_STRIP)
        b = strip.convert("L").tobytes()
        if b != last:
            strip.save(os.path.join(d, "log", f"{n:05d}.png"))
            last, n = b, n + 1
        now = time.time()
        if now - t_field > 3:
            im.resize((960, 522)).save(os.path.join(d, "field", f"{int(now - t0):04d}.png"))
            t_field = now
        if now - t_check > 1.5:
            t_check = now
            if on_summary(g):                     # the replay closed: the battle is over
                break
        time.sleep(0.12 if fast else 0.2)
    rounds = [r for r in (round_no(Image.open(os.path.join(d, "log", f))) for f in sorted(os.listdir(os.path.join(d, "log")))) if r is not None]
    last_round = max(rounds) if rounds else None
    print(f"pass 1: {n} log frames, last round seen {last_round}", flush=True)

    json.dump({"last_round": last_round, "log_frames": n}, open(os.path.join(d, "meta.json"), "w"))
    if units and last_round:
        units_pass(g, d, last_round)


def units_pass(g, d, last_round):
    """Pass 2: replay at turbo, slow down near the end, pause on the second-to-last round and
    read the F1 Unit Overview."""
    start_replay(g)
    g.key("t", wait=0.2)
    paused, slowed, t0 = False, False, time.time()
    while time.time() - t0 < 300:
        r = round_no(g.grab())
        if r is not None and r >= last_round - 3 and not slowed:
            g.key("s", wait=0.05)             # normal speed for the last rounds
            slowed = True
        if r is not None and r >= last_round - 1:
            g.key("space", wait=0.5)          # the replay closes when the last round ends
            paused = True
            break
        if not slowed and time.time() - t0 > 5 and on_summary(g):
            break
        time.sleep(0.05)
    if paused:
        n = capture_units(g, d)
        print(f"pass 2: {n} unit list pages saved", flush=True)
        g.key("F1", wait=0.5)
        g.key("q", wait=1.5)
    else:
        print("pass 2: the battle ended before the pause; no unit list", flush=True)


def capture_units(g, d, open_f1=True):
    """Save the F1 Unit Overview as pictures, top to bottom, into d/units/ (the list itself is
    read from them by parse_units, offline). With open_f1=False the overview is already open."""
    out = os.path.join(d, "units")
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        os.remove(os.path.join(out, f))
    if open_f1:
        g.key("F1", wait=1.0)
    g.scroll(False, 80, at=(960, 520))
    g.hover(1910, 1040, wait=0.4)
    last = None
    for page in range(120):
        im = g.grab()
        b = im.convert("L").crop((660, 110, 1270, 900)).tobytes()
        if b == last:                             # the list did not move: the end
            break
        im.save(os.path.join(out, f"{page:03d}.png"))
        last = b
        g.scroll(True, 3, at=(960, 520))
        g.hover(1910, 1040, wait=0.4)
    return len(os.listdir(out))


LIST_BOX = (650, 95, 1280, 978)                    # the F1 list, cut out of each page


def row_ys(im):
    """Centre y of every row on an F1 page: the bands of bright text in the Type column (the
    brightest channel, so blue commander names count too)."""
    col = im.convert("RGB").crop((660, LIST_BOX[1], 870, LIST_BOX[3]))
    w, h = col.size
    px = col.load()
    lit = [sum(1 for x in range(w) if max(px[x, y]) > 150) >= 3 for y in range(h)]
    out, y = [], 0
    while y < h:
        if lit[y]:
            a = y
            while y < h and lit[y]:
                y += 1
            if y - a >= 6:                        # a line of text, not a speck
                out.append((a + y) // 2 + LIST_BOX[1])
        else:
            y += 1
    return out


def read_row(im, ym):
    box = lambda k: (F1_COLS[k][0], ym - 11, F1_COLS[k][1], ym + 11)
    px = list(im.convert("RGB").crop((F1_FLAG_X[0] - 6, ym - 11, F1_FLAG_X[1] + 6, ym + 11)).getdata())
    purple = sum(1 for p in px if p[0] > 100 and p[2] > 120 and p[1] < 95)
    st_box = box("status")
    return {"type": ocr1(im, box("type")), "side": "ours" if purple >= 4 else "other",
            "hp": digits(im, box("hp")), "fp": digits(im, box("fp")), "xp": digits(im, box("xp")),
            "status": ocr1(im, st_box) if _bright(im, st_box) else ""}


def parse_units(d, debug=False):
    """Read the saved F1 pages as one list. Consecutive pages overlap; the overlap shows how far
    the list scrolled, and the running total gives every row a fixed place in the whole list.
    A row is read once, from the first page it is fully on (so two identical rows, like two
    fresh Velites, stay two)."""
    pages = sorted(os.listdir(os.path.join(d, "units")))
    by_pos, offset, prev, pitch, y0 = {}, 0, None, None, None
    for f in pages:
        im = Image.open(os.path.join(d, "units", f))
        if prev is not None:
            dy = scrolled(prev, im)
            if dy is None:
                print(f"{f}: no overlap with the page before; rows may be missing", flush=True)
                dy = 0
            offset += dy
        ys = [y for y in row_ys(im) if LIST_BOX[1] + 14 <= y <= LIST_BOX[3] - 14]
        if pitch is None and len(ys) > 2:
            pitch, y0 = (ys[-1] - ys[0]) / (len(ys) - 1), ys[0]
        new = 0
        for y in ys:
            pos = round((y + offset - y0) / pitch)
            if pos not in by_pos:
                by_pos[pos] = read_row(im, y)
                new += 1
        if debug:
            print(f"{f}: scrolled {offset}px, {len(ys)} rows, {new} new", flush=True)
        prev = im
    rows = [by_pos[k] for k in sorted(by_pos)]
    json.dump(rows, open(os.path.join(d, "units.json"), "w"), indent=1)
    return rows


def scrolled(a, b):
    """How many pixels the F1 list moved up between screenshots a and b, found by sliding the
    rows' text columns over each other; None when nothing lines up."""
    A = a.convert("L").crop((660, 110, 1270, 900)).resize((305, 790))   # cropped to the list
    B = b.convert("L").crop((660, 110, 1270, 900)).resize((305, 790))
    best = None
    for dy in range(1, 700):
        h = 790 - dy
        if h < 80:
            break
        d = ImageStat.Stat(ImageChops.difference(A.crop((0, dy, 305, 790)), B.crop((0, 0, 305, h)))).mean[0]
        if best is None or d < best[1]:
            best = (dy, d)
    return best[0] if best and best[1] < 6 else None


def _bright(im, box, level=100, need=6):
    return sum(1 for p in im.convert("L").crop(box).getdata() if p > level) >= need


# ------------------------------------------------------------------ report

def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def same(a, b):
    a, b = norm(a), norm(b)
    return bool(a) and bool(b) and SequenceMatcher(None, a, b).ratio() >= 0.8


def clean(s):
    s = s.strip(" |;:'\".,`~_-—‘’“”")
    s = re.sub(r"^[^A-Za-z(]{0,3}\s+", "", s)     # stray marks OCR reads from the terrain
    s = re.sub(r"^[A-Za-z]{1,2}\s+(?=[A-Z])", "", s)
    s = re.sub(r"(\s+[^\s)]{1,2})+$", "", s)      # and at the end ("... Holy Avenger j")
    return s.strip()


def stitch(frames):
    """frames: list of (round, [lines]). The panel shows the last ~10 lines, so each frame is
    aligned with the end of what is already there: try every offset into the last 12 lines and
    keep the one where most of the overlapping lines match (one garbled line does not break it).
    Returns [(round, line)], with "[gap]" where a frame does not overlap (lines were missed)."""
    out = []
    for rnd, lines in frames:
        lines = [l for l in lines if len(norm(l)) >= 6]
        if not lines:
            continue
        best_new, best_score = None, 0
        n = len(out)
        for j in range(max(0, n - 12), n):        # lines[0] sits at out[j]
            k = min(n - j, len(lines))
            hits = sum(same(out[j + i][1], lines[i]) for i in range(k))
            if hits >= max(1, (k + 1) // 2) and hits / k > best_score - 1e-9:
                best_score, best_new = hits / k, k
        if best_new is None:
            if out:
                out.append((rnd, "[gap]"))
            best_new = 0
        out += [(rnd, l) for l in lines[best_new:]]
    return out


def canon(name, vocab):
    """The vocabulary name closest to an OCR'd unit name, dropping stray leading tokens."""
    words = name.split()
    best, score = name, 0.0
    for i in range(min(3, len(words))):
        cand = " ".join(words[i:])
        for v in vocab:
            r = SequenceMatcher(None, cand.lower(), v.lower()).ratio()
            if r > score:
                best, score = v, r
    return best if score >= 0.75 else name


def singular(s):
    for a, b in (("ies", "y"), ("ites", "ite"), ("es", "e"), ("s", "")):
        if s.endswith(a) and not s.endswith("ss"):
            return s[: -len(a)] + b
    return s


RANGED = re.compile(r"^(?P<a>.+?) hit (?P<d>.+?) with a ranged attack \((?P<w>[^)]*)\)? ?(?:in|on) (?:the )?(?P<part>.+?) for (?P<n>\d+) points? of dama\w*(?P<k>.*killed)?", re.I)
HIT = re.compile(r"^(?P<a>.+?) hit (?P<d>.+?) (?:in|on) (?P<part>.+?) with (?P<w>.+?) for (?P<n>\d+) points? of dama\w*(?P<k>.*killed)?", re.I)
MISS = re.compile(r"^(?P<a>.+?) missed (?P<d>.+)$", re.I)
REPEL = re.compile(r"^(?P<d>.+?)'s attack with (?P<w>.+?) was repelled by (?P<a>.+)$", re.I)
CAST = re.compile(r"^(?P<a>.+?) casts (?P<s>.+)$", re.I)
DETAIL = re.compile(r"^(attack roll|damage roll|repel value|penetration roll|defence|morale|damage exceeded|armou?r defeating|.*\broll\b)", re.I)
ROUT = re.compile(r"^The (?P<s>.+?) arm\w* (?:are|is) routed", re.I)
PREP = re.compile(r"^(?P<a>.+?) prepares to cast (?P<s>.+)$", re.I)


def tidy(l):
    """Undo OCR punctuation noise inside a log line: "hit:Militia.in.arm" and "1 0 points"."""
    l = l.replace("’", "'").replace("‘", "'")
    l = re.sub(r"(?<=[A-Za-z])[.:;,](?=[A-Za-z])", " ", l)
    l = re.sub(r"\bra\w{2}ed attack ?\(", "ranged attack (", l)
    l = re.sub(r"\s*\b\w{0,2}iss\w?d\b", " missed", l)          # "niissed", "Velitemissed"
    l = re.sub(r"(?<=[a-z])missed\b", " missed", l)
    l = re.sub(r"(\d) (\d)(?= points)", r"\1\2", l)
    return re.sub(r"\s+", " ", l)


def unit_name(s):
    s = re.sub(r"[^A-Za-z' -]", "", s).strip()
    return re.sub(r"\s+", " ", s)


def report(name, out=None):
    d = os.path.join(BASE, name)
    summ = json.load(open(os.path.join(d, "summary.json")))
    meta = json.load(open(os.path.join(d, "meta.json"))) if os.path.exists(os.path.join(d, "meta.json")) else {}
    if os.path.isdir(os.path.join(d, "units")) and os.listdir(os.path.join(d, "units")):
        units = parse_units(d)
    else:
        units = json.load(open(os.path.join(d, "units.json"))) if os.path.exists(os.path.join(d, "units.json")) else []
    files = sorted(os.listdir(os.path.join(d, "log")))
    cache_f = os.path.join(d, "ocr_cache.json")
    cache = json.load(open(cache_f)) if os.path.exists(cache_f) else {}
    frames, cur = [], None
    for f in files:
        if f not in cache:
            im = Image.open(os.path.join(d, "log", f))
            cache[f] = [round_no(im), [x["text"] for x in V.ocr(im, LOG_LINES, [False] * len(LOG_LINES))]]
        raw = cache[f][1]
        r = round_no(Image.open(os.path.join(d, "log", f)))   # templates: exact and fast
        cur = r if r is not None else cur
        frames.append((cur, [l for l in (clean(x) for x in raw) if l]))
    json.dump(cache, open(cache_f, "w"))
    log = stitch(frames)
    vocab = set()
    for side in summ.get("sides", []):
        vocab |= {singular(u["unit"]) for u in side["units"]}
    for u in units:
        t = unit_name(u["type"])
        vocab |= {t, t.split(" the ")[0]}
    vocab |= {unit_name(m["a"]).split()[-1] for _, l in log for m in [CAST.match(l)] if m}
    nm = lambda x: canon(unit_name(x), vocab)
    with open(os.path.join(d, "log.txt"), "w") as fh:
        fh.write("\n".join(f"{r if r is not None else '-'}\t{l}" for r, l in log))

    # events
    stats, pairs, casts, other, gaps = {}, {}, [], [], 0
    first_hit, kills_by_round, routs = None, {}, {}
    def st(u):
        return stats.setdefault(u, {"attacks": 0, "hits": 0, "dmg": 0, "kills": 0, "hit_taken": 0, "dmg_taken": 0, "killed": 0})
    for r, l in log:
        if l == "[gap]":
            gaps += 1
            continue
        l = tidy(l)
        m = ROUT.match(l)
        if m:
            if m["s"] not in routs:
                routs[m["s"]] = r
            continue
        if DETAIL.match(l) or PREP.match(l):
            continue
        m = RANGED.match(l) or HIT.match(l)
        if m:
            a, dd, n = nm(m["a"]), nm(m["d"]), int(m["n"])
            k = bool(m["k"])
            st(a)["attacks"] += 1; st(a)["hits"] += 1; st(a)["dmg"] += n; st(a)["kills"] += k
            st(dd)["hit_taken"] += 1; st(dd)["dmg_taken"] += n; st(dd)["killed"] += k
            p = pairs.setdefault((a, dd), [0, 0, 0]); p[0] += 1; p[1] += n; p[2] += k
            if first_hit is None:
                first_hit = r
            if k:
                kills_by_round.setdefault(r, []).append(f"{a} > {dd}")
            continue
        m = MISS.match(l)
        if m:
            st(nm(m["a"]))["attacks"] += 1
            continue
        m = REPEL.match(l)
        if m:
            st(nm(m["d"]))["attacks"] += 1
            continue
        m = CAST.match(l)
        if m:
            if not casts or casts[-1][1:] != (nm(m["a"]), m["s"].strip()):
                casts.append((r, nm(m["a"]), m["s"].strip()))
            continue
        if any(v.lower() in l.lower() for v in vocab) or "rout" in l.lower() or "flee" in l.lower():
            other.append((r, l))               # skip lines that are only terrain noise

    # sides from the unit overview flags (ours = the first flag seen, our units are listed first)
    side_of = {}
    ours_name = summ["sides"][0]["side"] if summ.get("sides") else "ours"
    for side in summ.get("sides", []):                 # from the Battle Summary's names
        for u in side["units"]:
            side_of[canon(singular(u["unit"]), vocab)] = side["side"]
    for u in units:
        if u.get("side") == "ours":
            side_of[nm(u["type"])] = ours_name

    L = [f"# Battle review: {name}", "",
         f"{summ.get('title', '')} {summ.get('result', '').strip()}",
         f"Last round seen: {meta.get('last_round')}. Log frames: {meta.get('log_frames')}, "
         f"stitched lines: {len(log)}, gaps (lines missed): {gaps}.", ""]
    for s in summ.get("sides", []):
        L += [f"## {s['side']}", "", "| Unit | Count | Wounded | Dead |", "|---|---|---|---|"]
        for u in s["units"]:
            L.append(f"| {u['unit']} | {u['count']} | {u['wounded']} | {u['dead']} |")
        tot = [sum(int(u[k]) for u in s["units"]) for k in ("count", "wounded", "dead")]
        L.append(f"| **Total** | {tot[0]} | {tot[1]} | {tot[2]} |")   # the game's totals are too dim to read
        L.append("")
    L += ["## Who did what (from the log)", "",
          "| Unit | Side | Attacks | Hits | Hit % | Damage | Kills | Hits taken | Damage taken | Killed |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for u, s in sorted(stats.items(), key=lambda kv: -kv[1]["dmg"] - kv[1]["dmg_taken"]):
        if s["attacks"] + s["hit_taken"] < 2:
            continue
        pct = f"{100 * s['hits'] // s['attacks']}%" if s["attacks"] else "-"
        L.append(f"| {u} | {side_of.get(u, '?')} | {s['attacks']} | {s['hits']} | {pct} | {s['dmg']} | {s['kills']} | {s['hit_taken']} | {s['dmg_taken']} | {s['killed']} |")
    L += ["", "## Matchups (attacker > defender: hits, damage, kills)", ""]
    for (a, dd), (h, n, k) in sorted(pairs.items(), key=lambda kv: -kv[1][1])[:25]:
        L.append(f"- {a} > {dd}: {h} hits, {n} damage, {k} kills ({n / h:.1f} per hit)")
    L += ["", "## Timeline", "", f"- First hit in round {first_hit}."]
    L += [f"- **Round {r}: the {who} armies routed.**" for who, r in routs.items()]
    for r in sorted(k for k in kills_by_round if k is not None):
        L.append(f"- Round {r}: {len(kills_by_round[r])} killed ({'; '.join(sorted(set(kills_by_round[r])))[:200]})")
    if casts:
        L += ["", "## Spells", ""] + [f"- Round {r}: {a} casts {s}" for r, a, s in casts]
    if units:
        seen = {}
        for u in units:
            seen[canon(singular(nm(u["type"])), vocab)] = seen.get(canon(singular(nm(u["type"])), vocab), 0) + 1
        bad = []
        for side in summ.get("sides", []):
            for u in side["units"]:
                k = canon(singular(u["unit"]), vocab)
                if k in seen and seen[k] != u["count"]:
                    bad.append(f"{k}: {seen[k]} read, {u['count']} in the summary")
        L += ["", "## Units at the end (F1 overview, last round)", ""]
        if bad:
            L += ["Unit list check against the summary (rows may be doubled or missed): " + "; ".join(bad) + ".", ""]
        L += [
              "| Type | Side | HP | Fatigue | XP | Status |", "|---|---|---|---|---|---|"]
        for u in units:
            L.append(f"| {u['type']} | {ours_name if u.get('side') == 'ours' else 'enemy'} | {u['hp']} | {u['fp']} | {u['xp']} | {u['status']} |")
    if other:
        L += ["", "## Other log lines (unparsed; check for routs and special events)", ""]
        L += [f"- {r}: {l}" for r, l in other[:60]]
    L += ["", f"Raw captures: `{d}` (log/, field/, log.txt, summary.png).", ""]

    # contact sheet of field frames
    ff = sorted(os.listdir(os.path.join(d, "field")))
    if ff:
        pick = ff[:: max(1, len(ff) // 12)][:12]
        sheet = Image.new("RGB", (4 * 480, 3 * 261))
        for i, f in enumerate(pick):
            sheet.paste(Image.open(os.path.join(d, "field", f)).resize((480, 261)), ((i % 4) * 480, (i // 4) * 261))
        sheet.save(os.path.join(d, "field_sheet.png"))
        L.insert(5, f"Field frames: `{os.path.join(d, 'field_sheet.png')}` (every ~3 s, left to right).\n")
    out = out or os.path.join(HERE, "..", "battles", f"{name}.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write("\n".join(L))
    print("wrote", os.path.abspath(out))


def main(a):
    if len(a) < 2 or a[0] not in ("record", "report", "units"):
        print(__doc__)
        return
    name = re.sub(r"[^A-Za-z0-9_-]+", "_", a[1])
    if a[0] == "record":
        session.run(lambda g: record(g, name, fast="--fast" in a, units="--no-units" not in a,
                                     units_only="--units-only" in a), "battle")
    elif a[0] == "units":
        d = os.path.join(BASE, name)
        session.run(lambda g: print(capture_units(g, d, open_f1=False), "pages saved"), "battle")
        rows = parse_units(d, debug=True)
        print(len(rows), "units read")
    else:
        report(name, a[a.index("--out") + 1] if "--out" in a else None)


if __name__ == "__main__":
    main(sys.argv[1:])
