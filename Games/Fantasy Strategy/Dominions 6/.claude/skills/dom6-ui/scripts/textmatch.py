"""Read text on the Dominions 6 screen by matching it against known candidate strings rendered in
the game's own font (data/guifont.ttf). Not general OCR: it answers "which of these strings is
written here", which is all the pretender screens need (nation, form and bless names, numbers).
Pure PIL, no numpy; the pixel work runs in PIL's C code.
"""
import functools
import glob
import os

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageStat

FONT_DIRS = [os.environ.get("DOM6_DIR", ""), os.path.expanduser("~/.local/share/Steam/steamapps/common/Dominions6"),
             os.path.expanduser("~/.steam/steam/steamapps/common/Dominions6")]
SIZES = [s / 4 for s in range(60, 129)]         # 15 .. 32 in quarter points; the game scales its UI text
PAD = 3


def font_path(name="guifont.ttf"):
    for d in FONT_DIRS:
        p = os.path.join(d, "data", name) if d else ""
        if p and os.path.exists(p):
            return p
    hits = glob.glob(os.path.expanduser("~/**/Dominions6/data/" + name), recursive=True)
    if hits:
        return hits[0]
    raise SystemExit(f"cannot find the game's {name}; set DOM6_DIR to the Dominions6 install folder")


@functools.lru_cache(maxsize=None)
def _font(size, name):
    return ImageFont.truetype(font_path(name), size)


@functools.lru_cache(maxsize=200000)
def _size_of(text, size, name):
    r = render(text, size, name)
    return (r.width, r.height) if r else (0, 0)


def _sizes(text, w, h, font, prefix, only=None):
    """Font sizes worth trying for TEXT on a screen ink box W x H, best first."""
    out = []
    for s in only or SIZES:
        rw, rh = _size_of(text, s, font)
        dh = abs(rh - h)
        if not rw:
            continue
        if prefix:                                  # the rest of the line may add descenders
            if rw <= w + 3 and rh <= h + 2:
                out.append((0, -s, s))
            continue
        dw = abs(rw - w)
        if dh <= 2 and dw <= max(3, 0.04 * w):
            out.append((dw + 2 * dh, 0, s))
    return [s for *_, s in sorted(out)] if prefix else [s for *_, s in sorted(out)[:4]]


@functools.lru_cache(maxsize=20000)
def render(text, size, name="guifont.ttf"):
    """Antialiased text, white on black, cropped to its ink."""
    f = _font(size, name)
    l, t, r, b = f.getbbox(text)
    im = Image.new("L", (r - l + 6, b - t + 6), 0)
    ImageDraw.Draw(im).text((3 - l, 3 - t), text, font=f, fill=255)
    box = im.point(lambda v: 255 if v > 90 else 0).getbbox()
    return im.crop(box) if box else None


def _otsu(im):
    hist = im.histogram()
    total = sum(hist)
    sum_all = sum(i * h for i, h in enumerate(hist))
    best, thr, wb, sb, means = -1, 128, 0, 0, (0, 255)
    for t in range(256):
        wb += hist[t]
        if wb == 0 or wb == total:
            continue
        sb += t * hist[t]
        mb, mf = sb / wb, (sum_all - sb) / (total - wb)
        var = wb * (total - wb) * (mb - mf) ** 2
        if var > best:
            best, thr, means = var, t, (mb, mf)
    return thr, means


def ink(img, box, light=True):
    """(text intensity image 0-255 cropped to the ink + PAD, ink width) for the text in BOX of a
    screenshot; None if BOX holds no text. LIGHT: the text is lighter than its background."""
    g = img.crop(box).convert("L")
    thr, (dark, bright) = _otsu(g)
    fg, bg = (bright, dark) if light else (dark, bright)
    if abs(fg - bg) < 25:
        return None
    lut = [max(0, min(255, int(255 * (v - bg) / (fg - bg)))) for v in range(256)]
    t = g.point(lut)
    inkbox = t.point(lambda v: 255 if v > 128 else 0).getbbox()
    if not inkbox:
        return None
    x0, y0, x1, y1 = inkbox
    return t.crop((x0 - PAD, y0 - PAD, x1 + PAD, y1 + PAD)), x1 - x0, x0


def _score(scr, cand, part_w=None, right=False):
    """Smallest normalised difference between the screen text and a rendered candidate over a few
    pixel offsets (0 = identical). PART_W: compare only the left (RIGHT: right) PART_W pixels."""
    W, H = scr.size
    if part_w is not None:
        k = min(W, part_w + 2 * PAD)
        scr = scr.crop((W - k, 0, W, H) if right else (0, 0, k, H))
        W = k
    s_sum = ImageStat.Stat(scr).sum[0]
    best = 9.0
    for dy in (-1, 0, 1):
        for dx in (-2, -1, 0, 1, 2):
            c = Image.new("L", (W, H), 0)
            c.paste(cand, (PAD + dx, PAD + dy))
            d = ImageStat.Stat(ImageChops.difference(scr, c)).sum[0]
            tot = s_sum + ImageStat.Stat(c).sum[0]
            if tot:
                best = min(best, d / tot)
    return best


def _seg_score(scr, cand, part_w=None, right=False, seg=36):
    """Like _score, but every SEG-pixel slice is aligned on its own and the worst slice counts:
    a wrong word cannot hide behind a long shared tail ("Raven/Statue of the Underworld"). The
    score is half the worst slice plus half the mean, so slices that differ break ties."""
    W, H = scr.size
    if part_w is not None:
        k = min(W, part_w + 2 * PAD)
        scr = scr.crop((W - k, 0, W, H) if right else (0, 0, k, H))
        W = k
    full = Image.new("L", (W + 8, H + 4), 0)
    full.paste(cand, (PAD + 2, PAD + 1))
    worst, scores = 0.0, []
    for x0 in range(0, W, seg):
        x1 = min(W, x0 + seg)
        a = scr.crop((x0, 0, x1, H))
        a_sum = ImageStat.Stat(a).sum[0]
        best = 9.0
        for dy in (-1, 0, 1):
            for dx in (-3, -2, -1, 0, 1, 2, 3):
                b = full.crop((x0 + 2 - dx, 1 - dy, x1 + 2 - dx, H + 1 - dy))
                tot = a_sum + ImageStat.Stat(b).sum[0]
                if tot < 255 * 6:
                    best = 0.0
                    continue
                best = min(best, ImageStat.Stat(ImageChops.difference(a, b)).sum[0] / tot)
        worst = max(worst, best)
        scores.append(best)
    return (worst + sum(scores) / len(scores)) / 2 if scores else 1.0


def match(img, box, candidates, light=True, prefix=False, font="guifont.ttf", sizes=None, suffix=False):
    """Rank CANDIDATES by how well they match the text in BOX: [(score, text, size)], best first.
    Below ~0.25 is a match; the gap to the runner-up says how sure it is. PREFIX: the screen text
    may continue after the candidate ("Name - 190 points" when only the name is known)."""
    got = ink(img, box, light)
    if not got:
        return []
    scr, w, _ = got
    out = []
    h = scr.height - 2 * PAD
    only = sizes
    for c in dict.fromkeys(candidates):
        sizes = _sizes(c, w, h, font, prefix or suffix, only)
        best = None
        for s in sizes:
            r = render(c, s, font)
            if r is None or r.height > scr.height:
                continue
            sc = _score(scr, r, r.width if (prefix or suffix) else None, right=suffix)
            if best is None or sc < best[0]:
                best = (round(sc, 3), c, s)
        if best:
            out.append(best)
    out.sort()
    top = []                                    # re-rank the leaders slice by slice
    for sc, c, sz in out[:6]:
        r = render(c, sz, font)
        top.append((round(_seg_score(scr, r, r.width if (prefix or suffix) else None, right=suffix), 3), c, sz))
    return sorted(top) + out[6:]


def best(img, box, candidates, light=True, prefix=False, limit=0.3, margin=0.03, sizes=None, font="guifont.ttf"):
    """The candidate written in BOX, or None when nothing matches clearly."""
    r = match(img, box, candidates, light, prefix, font=font, sizes=sizes)
    if not r or r[0][0] > limit:
        return None
    if len(r) > 1 and r[1][0] - r[0][0] < margin and r[1][1] != r[0][1]:
        return None
    return r[0][1]


def _first_word(img, box, light, gap=4):
    """BOX narrowed to its first word (cut at the first run of GAP blank columns after ink)."""
    got = ink(img, box, light)
    if not got:
        return box
    t, w, x0 = got
    m = t.point(lambda v: 255 if v > 100 else 0)
    cols = [any(m.crop((x, 0, x + 1, m.height)).getdata()) for x in range(m.width)]
    seen, blank = False, 0
    for x, c in enumerate(cols):
        if c:
            seen, blank = True, 0
        elif seen:
            blank += 1
            if blank >= gap:
                return (box[0], box[1], box[0] + x0 - PAD + x, box[3])
    return box


def number(img, box, lo, hi, light=True, prefix=None, font="guifont.ttf", after=""):
    """The integer in BOX (lo..hi). PREFIX: text written before the number ("Design points:"),
    AFTER: text written after it (" points"); both are found on the screen and cut off, so only
    the digits are compared."""
    sizes = None
    got = ink(img, box, light)
    if not got:
        return None
    x_ink = box[0] + got[2]
    if prefix:
        r = match(img, box, [prefix], light, prefix=True, font=font)
        if not r:
            return None
        s0 = r[0][2]
        box = (x_ink + render(prefix, s0, font).width + 2, box[1], box[2], box[3])
        sizes = (s0 - 0.5, s0 - 0.25, s0, s0 + 0.25, s0 + 0.5)
    if after.strip():
        got = ink(img, box, light)
        r = match(img, box, [after.strip()], light, suffix=True, font=font, sizes=sizes)
        if not got or not r:
            return None
        right = box[0] + got[2] + got[1]
        box = (box[0], box[1], right - render(after.strip(), r[0][2], font).width - 3, box[3])
    got = best(img, box, [str(n) for n in range(lo, hi + 1)], light, limit=0.35, margin=0.02,
               sizes=sizes, font=font)
    return None if got is None else int(got)


def lines(img, x0, x1, y0, y1, light=True, min_h=8):
    """Centre y of each text line in a column strip."""
    g = img.crop((x0, y0, x1, y1)).convert("L")
    thr, _ = _otsu(g)
    m = g.point(lambda v: 255 if (v > thr) == light else 0)
    w = m.width
    out, start = [], None
    for y in range(m.height + 1):
        n = 0 if y == m.height else sum(1 for v in m.crop((0, y, w, y + 1)).getdata() if v)
        if n >= 2 and start is None:
            start = y
        elif n < 2 and start is not None:
            if y - start >= min_h:
                out.append(y0 + (start + y) // 2)
            start = None
    return out
