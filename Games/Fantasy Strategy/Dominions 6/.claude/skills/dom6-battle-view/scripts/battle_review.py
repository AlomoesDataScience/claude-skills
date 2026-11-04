"""Review a Dominions 6 battle from its replay: what each side lost, who hit whom, when, and what
every unit ended with. Part of the dom6-battle-view skill; feeds the dom6-tactics battle log.

  python3 -I battle_review.py record NAME [--fast | --slow] [--no-units] [--units-only]
        --slow: slow-motion replay (z) so the detail-4 log is not skipped (Troban: normal speed lost ~half)
        Start on the Battle Summary of the battle (click the battle message's text in Messages).
        1. reads the summary (units, count, wounded, dead per side);
        2. pass 1: View Battle, log detail 4, round counter on, then captures the log panel and a
           field frame while the replay plays, until it closes by itself at the end;
        3. pass 2 (unless --no-units): View Battle again at turbo, pauses on the last round seen
           in pass 1 and saves the F1 Unit Overview's pages as pictures (read by `report`: type,
        side, HP, fatigue, XP, dead/retreated). --units-only repeats pass 2 alone.
  python3 -I battle_review.py watch NAME [--up N] [--keys "g c"] [--setup-only]
        Watch the units move (the FoG II look, for replays). Start on the Battle Summary. View Battle,
        pause at once, detail 4, the given toggles (default g grid + c team squares), PageUp N times
        (camera height, whole field in view), photo of round 0 = the field reference (resnap); then slow
        motion with one full shot per round as the counter changes -> NAME/rounds/rNN.png + sheet.png.
  python3 -I battle_review.py boards NAME
        Grid-snapped top-down boards per round (gridsnap.py on the backed-off field shot fNN.png that watch
        takes before zooming in) -> NAME/boards/rNN.txt + boards.json; gif then adds a minimap per round
  python3 -I battle_review.py gif NAME [--ms 350]
        Animated GIF of a watched battle (NAME/frames): round, kills, tramples and who killed whom per round,
        a small battle log panel (that round's lines, scrolling), and Claude's COMMENTARY from
        NAME/commentary.txt ("3: text" or "5-7: text" per line, wrapped into a banner on top of those rounds).
        Run `report` first for log.txt -> NAME/battle.gif
  python3 -I battle_review.py units NAME
        With the F1 Unit Overview already open in a paused replay: save its pages and read them. Raw captures go to ~/.cache/game-ui/dom6_amd64/battles/NAME/.
  python3 -I battle_review.py report NAME [--out FILE.md]
        OCRs the captures, stitches the log, parses the events and writes the report (default:
        ../battles/NAME.md in this skill) plus a contact sheet of field frames.

Input goes through dom6-ui's guard (waits for the user to be idle, works only while the game is
focused). The replay closes by itself when the battle ends, so the log can only be read while it
plays. `+`/`-` scroll the battle log (manual p. 58; the user) - an earlier note here said resize: wrong.
"""
import json
import os
import re
import sys
import time
from difflib import SequenceMatcher

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)                          # gridsnap.py (python -I leaves the script's folder off the path)
sys.path.insert(0, os.path.join(HERE, "..", "..", "dom6-ui", "scripts"))
import vision as V                                # noqa: E402  (first: puts game-ui on the path)
import session                                    # noqa: E402
import dom6ui as U                                # noqa: E402
from session import Stop                          # noqa: E402
from PIL import Image, ImageChops, ImageStat     # noqa: E402

BASE = os.path.join(U.OUT, "battles")
LOG_STRIP = (0, 0, 1920, 310)                     # log panel (top left) + round counter (top right)
LOG_LINES = [(10, y, 935, y + 25) for y in range(44, 300, 25)]
ROUND_BOX = (1640, 62, 1820, 88)                  # "Combat round N" after `r` (1920 wide; round_no is relative)
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
    r = _round_shapes(im)
    if r is None:                                  # bright sky behind the white digits: OCR the phrase
        r = _round_ocr(im)
    return r


def counter_sig(im):
    """The round counter's white text as a mask (min channel > 235: the sky stays below ~220). None when hidden."""
    import numpy as np
    a = np.asarray(im.convert("RGB").crop((1770, 60, 1850, 88)))
    m = a.min(axis=2) > 235
    return m.tobytes() if m.sum() >= 12 else None


class RoundTracker:
    """Counts rounds without reading digits (the fast reader fails on bright sky, OCR takes ~0.75 s and starves
    the capture loop): the counter's white-text mask changes only when the round does, so a NEW mask seen on two
    grabs in a row = the next round. Tested on two Troban replays: one run of masks per round, camera moves
    included. A background OCR read every few seconds corrects the count (two reads agreeing on the same offset)."""

    def __init__(self, im, start=0):
        from concurrent.futures import ThreadPoolExecutor
        self.r, self.sig, self.cand = start, counter_sig(im), None
        self.pool, self.job, self.t, self.last_diff = ThreadPoolExecutor(1), None, 0, None

    def update(self, im):
        s = counter_sig(im)
        if s is not None and s != self.sig:
            if s == self.cand:
                self.r, self.sig, self.cand = self.r + 1, s, None
            else:
                self.cand = s
        else:
            self.cand = None
        self._ocr_check(im)
        return self.r

    def _ocr_check(self, im):
        if self.job and self.job.done():
            got, at = self.job.result(), self.job.at
            self.job = None
            if got is not None and abs(got - at) <= 3:
                diff = got - at
                if diff and diff == self.last_diff:
                    print(f"  round count corrected {self.r} -> {self.r + diff} (OCR)", flush=True)
                    self.r += diff
                    diff = None
                self.last_diff = diff
        if self.job is None and time.time() - self.t > 3:
            self.t = time.time()
            self.job = self.pool.submit(_round_ocr, im.crop((0, 0, 1912, 100)))
            self.job.at = self.r


def _round_ocr(im):
    from PIL import ImageOps
    c = im.convert("L").crop((1660, 60, 1800, 88))
    c = ImageOps.autocontrast(c).resize((c.width * 3, c.height * 3))
    t = V.ocr(c.convert("RGB"), [(0, 0, c.width, c.height)], [True], psm=7)[0]["text"]
    m = re.search(r"round\s*([0-9GO/&lI]{1,3})", t, re.I)
    if not m:
        return None
    d = m.group(1).translate(str.maketrans("GO/&lI", "007811"))
    return int(d) if d.isdigit() else None


def _round_shapes(im):
    """The replay's "Combat round N" (after `r`), read by matching the white digit shapes to
    templates (OCR confuses this font: G for 0, / for 7, & for 8). The first glyph in the box is
    the "d" of "round"; None when the counter is not shown."""
    c = im.convert("L").crop((1770, 60, 1840, 88))   # same place at 1920 and 1912 wide (checked)
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

def corner(g):
    """A resting spot for the pointer in the window's bottom-right corner, whatever its size
    (was fixed at 1910,1040 for 1920x1044; Claude's virtual screen is 1912x1000)."""
    return g.geo[2] - 10, g.geo[3] - 4


def start_replay(g, wait=3.5):
    if not on_summary(g) and not locate_view(g.grab()):
        raise Stop("not on the Battle Summary (View Battle not found)")
    g.click(*VIEW_BATTLE, wait=wait)
    g.hover(*corner(g), wait=0.2)
    if round_no(g.grab()) is None:                # `r` is a toggle that persists between replays
        g.key("r", wait=0.4)
        g.hover(*corner(g), wait=0.2)


def record(g, name, fast=False, units=True, units_only=False, slow=False):
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
    if slow:
        g.key("z", wait=0.2)
    last, n, t_field, t_check, t0 = None, 0, 0, 0, time.time()
    while time.time() - t0 < (2400 if slow else 900):
        im = g.grab()
        strip = im.crop((0, 0, min(LOG_STRIP[2], im.width), LOG_STRIP[3]))
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


PAN_PX = 103                     # replay camera: px of sideways shift per 100 ms of Left/Right held (camcal, 2026-11-03)


FIELD_TOP, FIELD_BOTTOM = 110, 45
LOG_PANEL = (0, 0, 900, 290)                       # the see-through log panel: units under it are washed out                  # sky/top bar above, the nation-icon bar below (px from the bottom)


def square_masks(im):
    """Team-square pixel masks {kind: mask} (see unit_blobs), grid lines opened away, UI areas cleared."""
    import numpy as np
    import cv2
    a = np.asarray(im.convert("RGB"), dtype=np.int16)
    H = a.shape[0]
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    lo, hi = a.min(axis=2), a.max(axis=2)
    out = {}
    for kind, m in (("dark", (G - R > 55) & (G - B > 75) & (G > 105) & (R < 58)),
                    ("light", (G - R > 55) & (G - B > 75) & (G > 105) & (R >= 58)),
                    ("pale", (lo > 140) & (hi - lo < 45))):
        m = m.astype(np.uint8)
        m[:FIELD_TOP] = 0; m[H - FIELD_BOTTOM:] = 0
        if kind == "pale":
            m[:LOG_PANEL[3], :LOG_PANEL[2]] = 0; m[:, -20:] = 0
        out[kind] = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    return out


def unit_blobs(im, min_px=25):
    """Every squad on screen, from the team squares (`c`): filled quads in the side's colour - in Troban our side
    dark green ~(41,123,24) / (54,142,35), Pangaea lighter green ~(70,154,53), independents pale grey. A 3x3
    opening removes the 1-2 px grid lines. Returns [{box, c (centre), px, rgb, kind green|pale}], biggest first."""
    import numpy as np
    import cv2
    a = np.asarray(im.convert("RGB"), dtype=np.int16)
    H = a.shape[0]
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    green = (G - R > 55) & (G - B > 75) & (G > 105)
    lo, hi = a.min(axis=2), a.max(axis=2)
    pale = (lo > 140) & (hi - lo < 45)
    out = []
    for kind, m in (("green", green), ("pale", pale)):
        m = m.astype(np.uint8)
        m[:FIELD_TOP] = 0; m[H - FIELD_BOTTOM:] = 0
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        if kind == "pale":                         # the log panel (top left, see-through) and the right edge are pale
            m[:LOG_PANEL[3], :LOG_PANEL[2]] = 0; m[:, -20:] = 0
        n, lab, st, cen = cv2.connectedComponentsWithStats(cv2.dilate(m, np.ones((7, 7), np.uint8)))
        for i in range(1, n):
            x, y, w, h, _ = st[i]
            sel = (lab == i) & (m > 0)
            px = int(sel.sum())
            if px < min_px or (kind == "pale" and (w > 400 or h > 200)):
                continue
            ys, xs = np.nonzero(sel)
            out.append({"box": (int(x), int(y), int(x + w), int(y + h)), "c": (int(xs.mean()), int(ys.mean())),
                        "px": px, "rgb": [int(v) for v in a[sel].mean(axis=0)], "kind": kind})
    return sorted(out, key=lambda b: -b["px"])


def unit_mask_box(im):
    """Bounding box and centre of all squads in view (unit_blobs, weighted by size); None when none is seen."""
    bl = unit_blobs(im)
    if not bl or sum(b["px"] for b in bl) < 40:
        return None
    x0 = min(b["box"][0] for b in bl); y0 = min(b["box"][1] for b in bl)
    x1 = max(b["box"][2] for b in bl); y1 = max(b["box"][3] for b in bl)
    t = sum(b["px"] for b in bl)
    return (x0, y0, x1, y1, int(sum(b["c"][0] * b["px"] for b in bl) / t), int(sum(b["c"][1] * b["px"] for b in bl) / t))


def grid_on(im):
    """The battlefield grid (`g`) shows as thin near-white lines over the ground."""
    import numpy as np
    a = np.asarray(im.convert("RGB"), dtype=np.int16)[400:900, 100:1800]
    light = a.min(axis=2) > 100                      # grid lines ~(130,144,108); bare grass min <= ~45
    return light.mean() > 0.008                      # tested: grid 0.028, no grid 0.001


def unit_mask(im):
    import numpy as np
    m = np.zeros((im.height, im.width), np.float32)
    for b in unit_blobs(im):
        x0, y0, x1, y1 = b["box"]
        m[y0:y1, x0:x1] = 1
    return m


def calibrate_pan(g, secs=0.4):
    """Replay pan speed at the CURRENT camera height (it changes with height: 103 px/100 ms low, ~44 at the top).
    Hold Right, compare the squads' masks before/after (phase correlation; squads don't repeat like the grid),
    hold Left back. Sets PAN_PX; returns it, or None (kept) when no squads are in view."""
    global PAN_PX
    import cv2
    a = unit_mask(g.grab())
    if a.sum() < 50:
        return None
    g.hold("Right", secs, wait=0.5)
    b = unit_mask(g.grab())
    g.hold("Left", secs, wait=0.5)
    (dx, dy), resp = cv2.phaseCorrelate(a, b)
    if resp < 0.1 or abs(dx) < 10:
        return None
    PAN_PX = abs(dx) / (secs * 10)
    return PAN_PX


def pan_x(g, px):
    if abs(px) > 20:
        g.hold("Right" if px > 0 else "Left", abs(px) / PAN_PX * 0.1, wait=0.35)


def ensure_paused(g, tries=3):
    """Press pause and CHECK it: two grabs 0.4 s apart must show the same field (units stand still)."""
    from PIL import ImageChops, ImageStat
    for _ in range(tries):
        g.key("space", wait=0.4)
        a = g.grab().crop((0, 320, g.geo[2], g.geo[3] - 60)).convert("L")
        time.sleep(0.4)
        b = g.grab().crop((0, 320, g.geo[2], g.geo[3] - 60)).convert("L")
        if ImageStat.Stat(ImageChops.difference(a, b)).mean[0] < 0.5:
            return True
    print("  warning: could not confirm the pause", flush=True)
    return False


def centre_on_units(g, back=0.6):
    """FoG II `present` for the replay: every squad in view and as big as fits, without offset arithmetic (pan
    speed changes with height and hold length). Back the camera off first (`back` s of Down: from further back
    the whole field is in view, so nothing hides off-screen), then: pan toward any edge the squads touch, back
    off more if they touch both, centre on the middle of ALL squads, step forward (Up) until they fill the
    frame, backing off once if they spill. Camera height: set by watch (PageUp HELD, taps do nothing)."""
    W, H = g.geo[2], g.geo[3]
    m = 0.03 * W
    if back:
        g.hold("Down", back, wait=0.5)
    backed = False
    for _ in range(14):
        b = unit_mask_box(g.grab())
        if not b:
            g.hold("Down", 0.3, wait=0.4)          # lost them: further back shows more
            continue
        left, right = b[0] < m, b[2] > W - m
        if left and right:
            g.hold("Down", 0.2, wait=0.4); backed = True
            continue
        if left or right:
            pan_x(g, (-1 if left else 1) * W / 4)
            continue
        mid = (b[0] + b[2]) / 2
        if abs(mid - W / 2) > 120:
            pan_x(g, mid - W / 2)
            continue
        if b[3] > 0.93 * H:
            if backed:
                break
            g.hold("Down", 0.15, wait=0.35); backed = True
            continue
        if not backed and (b[2] - b[0]) < 0.75 * W and b[3] < 0.85 * H:   # forward = lower on screen AND bigger
            g.hold("Up", 0.15, wait=0.35)
            continue
        break
    return unit_mask_box(g.grab()) is not None


def field_shot(g, path, back=0.6):
    """Backed-off view with the units centred sideways (the whole field in view): the shot gridsnap boards are
    made from. Leaves the camera backed off for centre_on_units(back=0)."""
    g.hold("Down", back, wait=0.5)
    for _ in range(3):
        b = unit_mask_box(g.grab())
        if not b or abs((b[0] + b[2]) / 2 - g.geo[2] / 2) < 150:
            break
        pan_x(g, (b[0] + b[2]) / 2 - g.geo[2] / 2)
    g.hover(*corner(g), wait=0.3)
    g.grab().save(path)


def watch(g, name, up=12, keys=("g", "c"), setup_only=False):
    """Watch the units move: per round, pause, centre the camera on the units, photograph, resume; the
    detail-4 log is captured the whole time (as `record`), so `report` works on the same folder."""
    base = os.path.join(BASE, name)
    d = os.path.join(base, "rounds")
    os.makedirs(d, exist_ok=True); os.makedirs(os.path.join(base, "log"), exist_ok=True)
    im = g.grab()
    if on_summary(g) or locate_view(im):
        json.dump(read_summary(im), open(os.path.join(base, "summary.json"), "w"), indent=1)
    start_replay(g, wait=1.0)
    g.key("space", wait=0.4)                       # pause on the deployment
    g.key("4", wait=0.2)
    for k in keys:                                 # toggles persist between replays: set, don't flip
        im = g.grab()
        on = grid_on(im) if k == "g" else (unit_mask_box(im) is not None) if k == "c" else False
        if not on:
            g.key(k, wait=0.4)
            im = g.grab()
            if k == "g" and not grid_on(im):
                print("  warning: grid still not seen after g", flush=True)
    g.hold("Prior", up / 4, wait=0.6)              # PageUp HELD (taps do nothing): 3 s = top height, whole field
    print("pan speed", calibrate_pan(g), "px per 100 ms", flush=True)
    field_shot(g, os.path.join(d, "f00.png"))
    centre_on_units(g, back=0)
    g.hover(*corner(g), wait=0.4)
    g.grab().save(os.path.join(d, "r00.png"))
    print("round 0 photo saved", unit_mask_box(g.grab()), flush=True)
    if setup_only:
        return                                     # left paused on round 0 for a look
    g.key("space", wait=0.2)
    g.key("z", wait=0.2)
    fd = os.path.join(base, "frames"); os.makedirs(fd, exist_ok=True)
    seen, last, n, t0, tf, nf, cur = {0}, None, 0, time.time(), 0, 0, 0
    tr, ts, log_rounds = RoundTracker(g.grab()), time.time(), {}
    while time.time() - t0 < 2400:
        im = g.grab()
        cur = tr.update(im)
        if time.time() - tf > 0.7:                 # animation frames (half size), tagged with the round
            im.convert("RGB").save(os.path.join(fd, f"{nf:05d}_r{cur:02d}.jpg"), quality=88)   # full size: gif crops
            nf, tf = nf + 1, time.time()
        strip = im.crop((0, 0, min(LOG_STRIP[2], im.width), LOG_STRIP[3]))
        b = strip.convert("L").tobytes()
        if b != last:
            strip.save(os.path.join(base, "log", f"{n:05d}.png")); log_rounds[f"{n:05d}.png"] = cur
            last, n = b, n + 1
        r = cur
        if r > max(seen):                          # a new round (RoundTracker)
            ensure_paused(g)                       # pause, field shot (board), centre, photo, resume
            field_shot(g, os.path.join(d, f"f{r:02d}.png"))
            centre_on_units(g, back=0)
            g.hover(*corner(g), wait=0.3)
            g.grab().save(os.path.join(d, f"r{r:02d}.png"))
            seen.add(r)
            print(f"  round {r}", flush=True)
            tr.update(g.grab())                    # paused: re-base on the counter as it is now
            g.key("space", wait=0.2)
            g.key("z", wait=0.1)                   # resume keeps slow motion
        if time.time() - t0 > 5 and time.time() - ts > 2:      # the summary check is OCR: every 2 s only
            ts = time.time()
            if on_summary(g):
                break
        time.sleep(0.05)
    json.dump({"last_round": max(seen), "log_frames": n}, open(os.path.join(base, "meta.json"), "w"))
    json.dump(log_rounds, open(os.path.join(base, "log_rounds.json"), "w"))
    fs = sorted(f for f in os.listdir(d) if f.startswith("r") and f.endswith(".png"))
    ims = [Image.open(os.path.join(d, f)).resize((640, 335)) for f in fs]
    sheet = Image.new("RGB", (640 * 3, 335 * ((len(ims) + 2) // 3)))
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 3) * 640, (i // 3) * 335))
    sheet.save(os.path.join(d, "sheet.png"))
    print(f"{len(fs)} round photos, {n} log frames, {nf} animation frames -> {base}", flush=True)


def make_boards(name):
    """Grid-snapped boards (gridsnap) from each round's field shot (fNN.png; rNN.png if none) -> NAME/boards/
    rNN.txt and boards.json {round: {"col,row": letter}}."""
    import gridsnap
    base = os.path.join(BASE, name)
    d = os.path.join(base, "rounds")
    out = os.path.join(base, "boards"); os.makedirs(out, exist_ok=True)
    allb = {}
    for f in sorted(os.listdir(d)):
        m = re.match(r"([fr])(\d+)\.png$", f)
        if not m or (m.group(1) == "r" and os.path.exists(os.path.join(d, f"f{m.group(2)}.png"))):
            continue
        r = int(m.group(2))
        im = Image.open(os.path.join(d, f))
        txt, cells = gridsnap.board(im)
        open(os.path.join(out, f"r{r:02d}.txt"), "w").write(txt + "\n")
        allb[r] = {f"{c},{rr}": L for (c, rr), L in cells.items()}
        print(f"round {r}: {txt.splitlines()[0][:150]}")
    json.dump(allb, open(os.path.join(out, "boards.json"), "w"))
    return allb


GIF_FIELD = (960, 500)                             # the field part of a GIF frame


def round_crops(fd, fs):
    """Per round, the window the GIF shows: around where the squads were during that round (median of the
    frames' unit boxes), 2:1 like GIF_FIELD, at least 900 px wide at full size - the replay camera cannot zoom
    (wheel = forward), so cropping is the zoom. Frames saved at half size are scaled up first."""
    import numpy as np
    per = {}
    for f in fs:
        r = int(re.search(r"_r(\d+)", f).group(1))
        im = Image.open(os.path.join(fd, f))
        if im.width < 1500:
            im = im.resize((im.width * 2, im.height * 2))
        b = unit_mask_box(im)
        if b:
            per.setdefault(r, []).append(b[:4])
    out = {}
    for r, bs in per.items():
        x0, y0, x1, y1 = np.median(np.asarray(bs), axis=0)
        w = max(900, (x1 - x0) * 1.35, (y1 - y0) * 1.35 * 2)
        w = min(w, 1912); h = w / 2
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        out[r] = (cx, cy, w, h)
    return out


def melee_inset(src, size=(440, 250), zoom=2.0):
    """The biggest cluster of squads (largest squad + every squad within 260 px), magnified - drawn into the
    field's empty sky so the fight is readable while the whole field stays in view."""
    from PIL import ImageDraw
    if src.width < 1500:
        src = src.resize((src.width * 2, src.height * 2))
    bl = unit_blobs(src)
    if not bl:
        return None
    big = bl[0]["c"]
    near = [b for b in bl if abs(b["c"][0] - big[0]) < 260 and abs(b["c"][1] - big[1]) < 160]
    x0 = min(b["box"][0] for b in near); x1 = max(b["box"][2] for b in near)
    y0 = min(b["box"][1] for b in near); y1 = max(b["box"][3] for b in near)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 - 15     # units stand above their squares
    w = max(size[0] / zoom, (x1 - x0) * 1.3); h = w * size[1] / size[0]
    if h < (y1 - y0) * 1.5:
        h = (y1 - y0) * 1.5; w = h * size[0] / size[1]
    box = (int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2))
    ins = src.crop(box).resize(size)
    ImageDraw.Draw(ins).rectangle((0, 0, size[0] - 1, size[1] - 1), outline=(255, 255, 0), width=2)
    ImageDraw.Draw(ins).text((6, 4), f"melee, x{(size[0] / w) / (GIF_FIELD[0] / src.width):.1f}", fill=(255, 255, 0))
    return ins


def crop_units(im, crops, r):
    if im.width < 1500:
        im = im.resize((im.width * 2, im.height * 2))
    keys = [k for k in crops if k <= r] or list(crops)
    if not keys:
        return im.resize(GIF_FIELD)
    cx, cy, w, h = crops[max(keys) if any(k <= r for k in crops) else min(keys)]
    x0 = min(max(0, cx - w / 2), im.width - w); y0 = min(max(110, cy - h * 0.55), im.height - 45 - h)
    y0 = max(0, y0)
    return im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize(GIF_FIELD)


def make_gif(name, ms=350):
    from PIL import ImageDraw
    base = os.path.join(BASE, name)
    fd = os.path.join(base, "frames")
    fs = sorted(f for f in os.listdir(fd) if f.endswith((".png", ".jpg")))
    notes = {}
    lp = os.path.join(base, "log.txt")
    if os.path.exists(lp):
        for line in open(lp):
            r, _, l = line.partition("\t")
            if not r.strip().isdigit():
                continue
            l = tidy(l.strip())
            n = notes.setdefault(int(r), {"kills": 0, "tr": 0, "moose": 0, "who": {}, "lines": []})
            if l and l != "[gap]" and not DETAIL.match(l) and (TRAMPLE.match(l) or RANGED.match(l) or HIT.match(l)
                                                             or MISS.match(l) or CAST.match(l) or "rout" in l.lower()):
                n["lines"].append(l)
            if "killed" in l:
                n["kills"] += 1
                m = TRAMPLE.match(l) or RANGED.match(l) or HIT.match(l)
                if m:
                    k = f"{unit_name(m['a'])} > {unit_name(m['d'])}" + (" (trample)" if TRAMPLE.match(l) else "")
                    n["who"][k] = n["who"].get(k, 0) + 1
            if re.search(r"t\w?ampl", l, re.I):
                n["tr"] += 1
                n["moose"] += "moose" in l.lower()
    comments = {}
    cp = os.path.join(base, "commentary.txt")
    if os.path.exists(cp):
        for line in open(cp, encoding="utf-8"):
            m = re.match(r"\s*(\d+)(?:\s*-\s*(\d+))?\s*:\s*(.+)", line)
            if m:
                for rr in range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1):
                    comments.setdefault(rr, []).append(m.group(3).strip())
    import textwrap
    boards = {}
    bp = os.path.join(base, "boards", "boards.json")
    if os.path.exists(bp):
        import gridsnap
        allc = {int(r): {tuple(map(int, k.split(","))): v for k, v in cells.items()}
                for r, cells in json.load(open(bp)).items()}
        ks = [k for c in allc.values() for k in c]
        if ks:                                     # one view for the whole battle: where the squads ever were
            view = (min(k[0] for k in ks) - 2, min(k[1] for k in ks) - 2,
                    max(k[0] for k in ks) + 3, max(k[1] for k in ks) + 3)
            for r, cells in allc.items():
                boards[r] = gridsnap.draw_board(cells, view=view)
    crops = round_crops(fd, fs)
    per_round = {}
    for f in fs:
        per_round.setdefault(int(re.search(r"_r(\d+)", f).group(1)), []).append(f)
    frames = []
    PW = 420                                       # the small battle log panel, right of the field
    for f in fs:
        r = int(re.search(r"_r(\d+)", f).group(1))
        field = crop_units(Image.open(os.path.join(fd, f)).convert("RGB"), crops, r)
        TOP, CAP = 64, 90                          # commentary strip above the field, caption strip below
        im = Image.new("RGB", (field.width + PW, TOP + field.height + CAP), (20, 20, 20))
        im.paste(field, (0, TOP))
        ins = melee_inset(Image.open(os.path.join(fd, f)).convert("RGB"))
        if ins:
            im.paste(ins, (field.width - ins.width - 6, TOP + 6))
        d = ImageDraw.Draw(im)
        lines = notes.get(r, {}).get("lines", [])
        k, nfr = per_round[r].index(f), len(per_round[r])
        bk = max([k for k in boards if k <= r], default=None)
        show = 36 if bk is None else 24
        if bk is not None:
            im.paste(boards[bk], (field.width, im.height - boards[bk].height))
        start = int(max(0, len(lines) - show) * k / max(1, nfr - 1)) if lines else 0
        d.text((field.width + 8, 6), f"Battle log - round {r}", fill=(255, 255, 0))
        for i, t in enumerate(lines[start:start + show]):
            col = (255, 120, 120) if "killed" in t else (255, 200, 90) if re.search(r"t\w?ampl", t, re.I) else (220, 220, 220)
            d.text((field.width + 8, 24 + 16 * i), t[:62], fill=col)
        n = notes.get(r, {})
        txt = f"Round {r}   kills {n.get('kills', 0)}   tramples {n.get('tr', 0)} (moose {n.get('moose', 0)})"
        cm = textwrap.wrap("  ".join(comments.get(r, [])), 120)[:3]
        d.rectangle((0, 0, field.width, TOP - 1), fill=(10, 30, 60))
        for i, t in enumerate(cm):
            d.text((10, 6 + 18 * i), t, fill=(255, 255, 255))
        who = sorted(n.get("who", {}).items(), key=lambda kv: -kv[1])[:4]
        lines = [txt] + [f"  {k} x{v}" for k, v in who]
        d.rectangle((0, TOP + field.height, field.width, im.height), fill=(0, 0, 0))
        for i, t in enumerate(lines[:5]):
            d.text((8, TOP + field.height + 5 + 16 * i), t, fill=(255, 255, 0) if i == 0 else (255, 255, 255))
        frames.append((r, im))
    # the video: every frame, H.264 through OpenCV's ffmpeg backend (plays anywhere, a fraction of the GIF)
    import cv2
    import numpy as np
    vp = os.path.join(base, "battle.mp4")
    vw = cv2.VideoWriter(vp, cv2.VideoWriter_fourcc(*"avc1"), 1000 / ms, frames[0][1].size)
    for _, f_ in frames:
        vw.write(cv2.cvtColor(np.asarray(f_), cv2.COLOR_RGB2BGR))
    vw.release()
    print(f"video -> {vp} ({os.path.getsize(vp) // 1024} KB)")
    # the GIF: at most 6 frames per round, 80% size (GIFs are big)
    keep, cnt = [], {}
    per_n = {}
    for r, _ in frames:
        per_n[r] = per_n.get(r, 0) + 1
    for r, f_ in frames:
        i = cnt.get(r, 0); cnt[r] = i + 1
        step = max(1, -(-per_n[r] // 6))
        if i % step == 0:
            keep.append(f_.resize((int(f_.width * 0.8), int(f_.height * 0.8))))
    frames = keep
    ms = int(ms * 1.6)
    # one palette for all frames, built from a sample of them: per-frame 128-colour palettes dropped the rare
    # bright team-square greens (squads vanished into the grass)
    samp = frames[:: max(1, len(frames) // 12)]
    mos = Image.new("RGB", (samp[0].width, samp[0].height * len(samp)))
    for i, f_ in enumerate(samp):
        mos.paste(f_, (0, i * f_.height))
    import gridsnap
    fixed = [(255, 255, 0), (255, 255, 255), (255, 120, 120), (255, 200, 90), (10, 30, 60), (0, 0, 0),
             (20, 20, 20), (28, 34, 28), (90, 110, 90), (220, 220, 220), (160, 170, 160),
             (41, 123, 24), (54, 142, 35), (70, 154, 53), (88, 173, 70), (170, 172, 160)] + list(gridsnap.COLOURS.values())
    q = mos.quantize(colors=256 - len(fixed), method=Image.Quantize.MEDIANCUT)
    p = q.getpalette()[: 3 * (256 - len(fixed))]
    for c in fixed:
        p += list(c)
    pal = Image.new("P", (1, 1)); pal.putpalette(p)
    frames = [f_.quantize(palette=pal, dither=Image.Dither.NONE) for f_ in frames]
    out = os.path.join(base, "battle.gif")
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=ms, loop=0, optimize=False)
    import shutil
    import subprocess
    if shutil.which("gifsicle"):                   # the user installed it 2026-11-03: frame deltas + light lossy
        subprocess.run(["gifsicle", "-b", "-O3", "--lossy=30", out], check=False)
    print(f"{len(frames)} frames -> {out} ({os.path.getsize(out) // 1024} KB)")


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
    g.hover(*corner(g), wait=0.4)
    last = None
    for page in range(120):
        im = g.grab()
        b = im.convert("L").crop((660, 110, 1270, 900)).tobytes()
        if b == last:                             # the list did not move: the end
            break
        im.save(os.path.join(out, f"{page:03d}.png"))
        last = b
        g.scroll(True, 3, at=(960, 520))
        g.hover(*corner(g), wait=0.4)
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
TRAMPLE = re.compile(r"^(?P<a>.+?) (?:tried to )?t\w?ampl\w* (?P<d>.+?) (?:for|who evaded)\D*(?P<n>\d+)\s*points? of dama\w*(?P<k>.*killed)?", re.I)
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
    lr_f = os.path.join(d, "log_rounds.json")
    log_rounds = json.load(open(lr_f)) if os.path.exists(lr_f) else {}   # watch's RoundTracker, if recorded
    frames, cur = [], None
    for f in files:
        if f not in cache:
            im = Image.open(os.path.join(d, "log", f))
            cache[f] = [round_no(im), [x["text"] for x in V.ocr(im, LOG_LINES, [False] * len(LOG_LINES))]]
        raw = cache[f][1]
        r = log_rounds[f] if f in log_rounds else round_no(Image.open(os.path.join(d, "log", f)))
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
        return stats.setdefault(u, {"attacks": 0, "hits": 0, "dmg": 0, "kills": 0, "tramples": 0, "tr_dmg": 0, "hit_taken": 0, "dmg_taken": 0, "killed": 0})
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
        m = TRAMPLE.match(l)                     # tramples REPLACE weapon attacks (wiki): count them apart
        if m:
            a, dd, n = nm(m["a"]), nm(m["d"]), int(m["n"])
            k = bool(m["k"])
            st(a)["tramples"] += 1; st(a)["tr_dmg"] += n; st(a)["kills"] += k; st(a)["dmg"] += n
            st(dd)["hit_taken"] += 1; st(dd)["dmg_taken"] += n; st(dd)["killed"] += k
            p = pairs.setdefault((a, dd), [0, 0, 0]); p[0] += 1; p[1] += n; p[2] += k
            if k:
                kills_by_round.setdefault(r, []).append(f"{a} > {dd} (trample)")
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
          "| Unit | Side | Attacks | Hits | Hit % | Tramples | Trample dmg | Damage | Kills | Hits taken | Damage taken | Killed |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for u, s in sorted(stats.items(), key=lambda kv: -kv[1]["dmg"] - kv[1]["dmg_taken"]):
        if s["attacks"] + s["tramples"] + s["hit_taken"] < 2:
            continue
        pct = f"{100 * s['hits'] // s['attacks']}%" if s["attacks"] else "-"
        L.append(f"| {u} | {side_of.get(u, '?')} | {s['attacks']} | {s['hits']} | {pct} | {s['tramples']} | {s['tr_dmg']} | {s['dmg']} | {s['kills']} | {s['hit_taken']} | {s['dmg_taken']} | {s['killed']} |")
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
    ff = sorted(os.listdir(os.path.join(d, "field"))) if os.path.isdir(os.path.join(d, "field")) else []
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
    if len(a) < 2 or a[0] not in ("record", "report", "units", "watch", "gif", "boards"):
        print(__doc__)
        return
    name = re.sub(r"[^A-Za-z0-9_-]+", "_", a[1])
    if a[0] == "record":
        session.run(lambda g: record(g, name, fast="--fast" in a, units="--no-units" not in a,
                                     units_only="--units-only" in a, slow="--slow" in a), "battle")
    elif a[0] == "boards":
        make_boards(name)
    elif a[0] == "gif":
        make_gif(name, int(a[a.index("--ms") + 1]) if "--ms" in a else 350)
    elif a[0] == "watch":
        up = int(a[a.index("--up") + 1]) if "--up" in a else 12
        keys = tuple(a[a.index("--keys") + 1].split()) if "--keys" in a else ("g", "c")
        session.run(lambda g: watch(g, name, up, keys, "--setup-only" in a), "battle")
    elif a[0] == "units":
        d = os.path.join(BASE, name)
        session.run(lambda g: print(capture_units(g, d, open_f1=False), "pages saved"), "battle")
        rows = parse_units(d, debug=True)
        print(len(rows), "units read")
    else:
        report(name, a[a.index("--out") + 1] if "--out" in a else None)


if __name__ == "__main__":
    main(sys.argv[1:])
