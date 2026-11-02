"""Seeing the Dominions 6 screen: read text in the game's own fonts, find and label every element
(windows, header bars, parchment panels, text lines, buttons, sprites and icons, tooltips, and the
3D world behind them: sky, distant hills, water, land, trees and other objects), and find saved
templates ("regex for images").

  python3 -I vision.py scene [IMAGE] [--out PNG] [--json]  the organised element tree of a screenshot
                                                           (no IMAGE: grab the game, which must be
                                                           in front); --out draws the boxes
  python3 -I vision.py read IMAGE X0 Y0 X1 Y1 [--dark] [--glyphs [--fancy] [--size S]]  text in a box
  python3 -I vision.py find IMAGE NAME [NAME...] [--box X0 Y0 X1 Y1]   where saved templates appear
  python3 -I vision.py add NAME IMAGE X0 Y0 X1 Y1 [--kind sprite|icon|ui|text] [--note TEXT]
  python3 -I vision.py templates                                       list saved templates
  python3 -I vision.py video OUT.gif [--n 16] [--gap 0.25]   a short clip of the game (half size)
  scene --frames N   grabs N frames first: what moves is the 3D world, what stays is UI and text

Text is read by Tesseract 5 from the NormCap flatpak (com.github.dynobo.normcap; all text boxes of
a screen in one call, ~1 s). Without it, a pure-PIL glyph reader (read()) matches each glyph blob
against the game's own font rendered at the line's size and sub-pixel position; slower (~0.3 s a
line) and rougher. closest() snaps a read string to a list of known names.
"""
import functools
import json
import os
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageStat

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

def _skill_scripts(name):
    """scripts/ of a skill in this or any parent folder's .claude/skills (generic skills sit at the root)."""
    d = os.path.dirname(os.path.abspath(__file__))
    while True:
        p = os.path.join(d, ".claude", "skills", name, "scripts")
        if os.path.isdir(p) or os.path.dirname(d) == d:
            return p
        d = os.path.dirname(d)
sys.path.insert(1, _skill_scripts("game-ui"))
import textmatch as T  # noqa: E402

TEMPLATES = os.environ.get("UI_TEMPLATES") or os.path.join(os.path.dirname(HERE), "templates")
GLYPHS = ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
          ".,:;'!?-+()/&%\"" "àáâäåèéêëíïñ"
          "óôöúüÄÉÖÜ")
INK = 110                       # 0-255 text intensity that counts as ink
FEE = 0.025                     # cost of one more glyph, per point of size, when cutting merged letters


# ---------------------------------------------------------------- glyphs

@functools.lru_cache(maxsize=None)
def _metrics(size, font):
    f = ImageFont.truetype(T.font_path(font), size)
    asc = max(-f.getbbox(c, anchor="ls")[1] for c in "Hdlbk")
    return f, asc, int(size * 1.15) + 1, int(size * 0.35) + 1     # font, ascender, canvas above/below


PHASES = (0, 1, 2, 3)            # sub-pixel positions, in quarter pixels


@functools.lru_cache(maxsize=None)
def _big(size, font):
    return ImageFont.truetype(T.font_path(font), size * 4)


@functools.lru_cache(maxsize=200000)
def glyph(text, size, font="guifont.ttf", phase=0):
    """TEXT (one glyph or a few) rendered white on black with the baseline at a fixed row, at a
    sub-pixel PHASE (quarter pixels: drawn 4x larger, shifted, shrunk with a box filter, the way
    antialiasing places a glyph between pixels), cropped to its ink horizontally: (image, width)."""
    _, _, up, down = _metrics(size, font)
    f = _big(size, font)
    l, t, r, b = f.getbbox(text, anchor="ls")
    if r <= l:
        return None
    W = ((r - l + 16 + phase) // 4 + 2) * 4
    im = Image.new("L", (W, (up + down) * 4), 0)
    ImageDraw.Draw(im).text((8 - l + phase, up * 4), text, font=f, fill=255, anchor="ls")
    im = im.resize((W // 4, up + down), Image.Resampling.BOX)
    box = im.point(lambda v: 255 if v > INK else 0).getbbox()
    if not box:
        return None
    im = im.crop((box[0], 0, box[2], up + down))
    return im, box[2] - box[0]


@functools.lru_cache(maxsize=None)
def _by_width(size, font):
    """{ink width: [glyphs]} at this size (phase 0)."""
    out = {}
    for c in GLYPHS:
        g = glyph(c, size, font)
        if g:
            out.setdefault(g[1], []).append(c)
    return out


def _cands(w, size, font):
    """Glyphs that fit a blob W wide (the game's text runs up to 2 px wider than a render)."""
    table = _by_width(size, font)
    return tuple(c for ww in range(w - 2, w + 2) for c in table.get(ww, ()))


@functools.lru_cache(maxsize=4000)
def _stack(cands, W, H, size, font, shifts, dys):
    """Every variant (glyph, phase, dx, dy) of CANDS drawn on a W x H canvas, stacked into one
    tall image: (image, [(glyph, ink sum)])."""
    variants = []
    for c in cands:
        for ph in PHASES:
            g = glyph(c, size, font, ph)
            if not g or g[1] > W + 1 or g[1] < W - 4:
                continue
            gi, gw = g
            for dy in dys:
                for dx in shifts:
                    variants.append((c, gi, dx + (W - gw) // 2, dy))
    if not variants:
        return None, []
    tall = Image.new("L", (W, H * len(variants)), 0)
    labels = []
    for k, (c, gi, x, dy) in enumerate(variants):
        tall.paste(gi, (x, k * H + dy))
        labels.append(c)
    sums = [v * W * H for v in tall.convert("F").resize((1, len(variants)), Image.Resampling.BOX).getdata()]
    return tall, list(zip(labels, sums))


def _tile(img, n):
    W, H = img.size
    out = Image.new("L", (W, H * n), 0)
    out.paste(img, (0, 0))
    k = 1
    while k < n:                                              # double the filled part each time
        c = min(k, n - k)
        out.paste(out.crop((0, 0, W, H * c)), (0, H * k))
        k += c
    return out


def _best(blob, cands, size, font, shifts=(-1, 0, 1), dys=(-1, 0, 1)):
    """Best (score, glyph, absolute difference) for a screen blob (L image, baseline at the canvas
    row) among CANDS, over sub-pixel phases and small shifts, compared in one batched PIL call.
    Ranked by the absolute pixel difference (a normalised score would favour glyphs with more ink:
    "l" over "i" and "t"); the score (difference / ink of both, 0 = same) says how sure."""
    W, H = blob.size
    tall, meta = _stack(tuple(cands), W, H, size, font, tuple(shifts), tuple(dys))
    if not meta:
        return 9.0, "", 9e9
    n = len(meta)
    diff = ImageChops.difference(tall, _tile(blob, n)).convert("F").resize((1, n), Image.Resampling.BOX)
    bsum = ImageStat.Stat(blob).sum[0]
    best = None
    for d, (c, gsum) in zip(diff.getdata(), meta):
        dabs = d * W * H / (255.0 * H)                        # in "fully wrong columns"
        if ord(c[0]) > 127:
            dabs += 0.1                                       # plain letters win ties
        if best is None or dabs < best[2]:
            tot = gsum + bsum
            best = (d * W * H / tot if tot else 1.0, c, dabs)
    return best


# ---------------------------------------------------------------- reading a line

def _line(img, box, light):
    """(text intensity 0-255, stroke mask) for BOX: the intensity is normalised so the text is
    white, and the mask keeps thin strokes only (a blurred copy is subtracted), so smooth
    backgrounds, gradients and button edges do not count as ink."""
    g = img.crop(box).convert("L")
    thr, (dark, bright) = T._otsu(g)
    fg, bg = (bright, dark) if light else (dark, bright)
    if abs(fg - bg) < 25:
        return None
    lut = [max(0, min(255, int(255 * (v - bg) / (fg - bg)))) for v in range(256)]
    t = g.point(lut)
    hp = ImageChops.subtract(t, t.filter(ImageFilter.BoxBlur(4)))
    m = ImageChops.multiply(hp.point(lambda v: 255 if v > 40 else 0), t.point(lambda v: 255 if v > 70 else 0))
    m = m.filter(ImageFilter.MaxFilter(3))
    return ImageChops.multiply(t, m), m.point(lambda v: 255 if v else 0)


def _band(t):
    """(top, baseline, bottom, ink mask) of the strongest text line in T."""
    m = t.point(lambda v: 255 if v > INK else 0)
    W, H = m.size
    col = m.resize((1, H), Image.Resampling.BOX).load()
    rows = [col[0, y] * W / 255 for y in range(H)]
    if max(rows, default=0) < 1:
        return None
    floor = max(1.0, 0.06 * max(rows))                        # runs of rows with real ink
    bands, start = [], None
    for y in range(H + 1):
        on = y < H and rows[y] >= floor
        if on and start is None:
            start = y
        elif not on and start is not None:
            bands.append((sum(rows[start:y]), start, y))
            start = None
    _, a, b = max(bands)
    peak = max(rows[a:b])
    base = max(y for y in range(a, b) if rows[y] >= 0.35 * peak)
    return a, base, b, m


def _blobs(m, y0, y1):
    """[(x0, x1)] runs of columns holding ink between rows y0..y1."""
    W = m.width
    band = m.crop((0, max(0, y0), W, y1))
    cols = band.resize((W, 1), Image.Resampling.BOX).load()
    out, start = [], None
    for x in range(W + 1):
        on = x < W and cols[x, 0] > 3
        if on and start is None:
            start = x
        elif not on and start is not None:
            out.append((start, x))
            start = None
    return out


_SIZE_HINT = {}


def read(img, box, light=True, font="guifont.ttf", size=None, detail=False, pad=7):
    """The text of the line in BOX (the box is widened by PAD up and down, so it need not be
    tight). Returns the string, or with DETAIL a dict: text, size, score (mean glyph difference;
    under ~0.2 is a clean read), scores per character and the text's box on screen."""
    x0, y0, x1, y1 = box
    box = (x0, max(0, y0 - pad), x1, min(img.height, y1 + pad))
    got = _line(img, box, light)
    empty = {"text": "", "score": 1.0, "box": None}
    if got is None:
        return empty if detail else ""
    t, _ = got
    band = _band(t)
    if not band:
        return empty if detail else ""
    top, base, bottom, m = band
    if size:
        sizes = [size]
    else:
        cap = base - top + 1
        _, a19, _, _ = _metrics(19, font)
        s0 = max(8.0, round(cap * 19 / a19 * 2) / 2)
        hint = _SIZE_HINT.get((font, light))
        if hint and abs(hint - s0) <= 1.5 and _read_at(t, m, base, bottom, hint, font, quick=True)["score"] < 0.2:
            sizes = [hint]                                    # same size as the last line read
        else:
            sizes = sorted({s0 + d for d in (-1.5, -1, -0.5, 0, 0.5, 1)} | ({hint} if hint else set()))
            scored = sorted((_read_at(t, m, base, bottom, s, font, quick=True)["score"], s) for s in sizes)
            s1 = scored[0][1]
            sizes = [s1 - 0.25, s1, s1 + 0.25]
    s_mid = sizes[len(sizes) // 2]                              # the baseline row, to the pixel
    base = min((base + d for d in (-1, 0, 1)),
               key=lambda bb: _read_at(t, m, bb, bottom, s_mid, font, quick=True, dys=(0,))["score"])
    best = None
    for s in sizes:
        r = _read_at(t, m, base, bottom, s, font, quick=len(sizes) > 1)
        if best is None or r["score"] < best["score"]:
            best = r
    if len(sizes) > 1:
        best = _read_at(t, m, base, bottom, best["size"], font, quick=False)
    _SIZE_HINT[(font, light)] = best["size"]
    ink = m.getbbox()
    best["box"] = (box[0] + ink[0], box[1] + ink[1], box[0] + ink[2], box[1] + ink[3]) if ink else None
    return best if detail else best["text"]


def _read_at(t, m, base, bottom, size, font, quick, dys=(-1, 0, 1)):
    f, asc, up, down = _metrics(size, font)
    space = f.getlength(" ")
    y0, y1 = base + 1 - up, base + 1 + down
    blobs = _blobs(m, base - asc - 2, min(base + down, bottom + 1))
    if quick:
        blobs = [b for b in blobs if b[1] - b[0] >= 4][:10]
    text, scores, prev = "", [], None
    for x0, x1 in blobs:
        if prev is not None and x0 - prev >= max(3.5, 0.85 * space):
            text += " "
        prev = x1
        blob = Image.new("L", (x1 - x0, up + down), 0)
        blob.paste(t.crop((x0, max(0, y0), x1, y1)), (0, max(0, -y0)))
        w = x1 - x0
        s, c, dabs = _best(blob, _cands(w, size, font), size, font, dys=dys)
        if not quick and (w >= 0.55 * size or s > 0.2):         # may be letters touching
            seg = _segment(blob, size, font)
            if seg and seg[2] < dabs + FEE * size - 0.05:
                s, c = seg[0], seg[1]
        if s > 1:                                            # nothing of that width
            s, c = 1.0, "?"
        text += c
        scores.append(s)
    if not quick:                                            # specks of panel texture at the ends
        parts = text.split(" ")
        while len(parts) > 1 and len(parts[0]) == 1 and scores and scores[0] >= 0.3:
            parts.pop(0); scores.pop(0)
        if len(parts) == 1 and len(parts[0]) > 2 and scores and scores[0] >= 0.3 and not parts[0][0].isalnum():
            parts[0] = parts[0][1:]; scores.pop(0)
        if len(parts[0]) > 2 and scores and scores[0] >= 0.3 and parts[0][0] in "ijl;,.!'f" and parts[0][1].isupper():
            parts[0] = parts[0][1:]; scores.pop(0)
        while len(parts) > 1 and len(parts[-1]) == 1 and scores and scores[-1] >= 0.3:
            parts.pop(); scores.pop()
        text = " ".join(parts)
    return {"text": _context(text), "size": size, "baseline": base, "scores": scores,
            "score": sum(scores) / len(scores) if scores else 1.0}


def _segment(blob, size, font):
    """Read a blob of touching letters: the cheapest chain of glyphs covering it, each glyph
    compared with the slice under it (neighbours may overlap by a pixel). (score, text, total
    cost in the units of _best's absolute difference plus a fee per glyph) or None."""
    W, H = blob.size
    table = _by_width(size, font)
    widths = sorted(w for w in table if w <= W + 1)
    INF = float("inf")
    cost = [INF] * (W + 2)
    back = [None] * (W + 2)
    cost[0] = 0.0
    for x in range(W):
        if cost[x] == INF:
            continue
        for w in widths:
            if x + w > W + 1:
                break
            for pw in (w, w + 1):                             # the game draws glyphs a bit wider
                if x + pw > W:
                    break
                piece = blob.crop((x, 0, x + pw, H))
                s, c, dabs = _best(piece, table[w], size, font, shifts=(0,), dys=(0,))
                if s > 0.6 or (w <= 3 and s > 0.12):          # thin glyphs only when clear
                    continue
                step = dabs + FEE * size                      # each extra glyph must earn its place
                for nx in (x + pw - 1, x + pw, x + pw + 1):
                    if x < nx <= W + 1 and cost[x] + step < cost[nx]:
                        cost[nx], back[nx] = cost[x] + step, (x, c)
    end = min((e for e in (W, W + 1, W - 1) if 0 < e <= W + 1 and cost[e] < INF), key=lambda e: cost[e], default=None)
    if end is None:
        return None
    text, x = "", end
    while x > 0:
        x, c = back[x]
        text = c + text
    n = len(text)
    return (cost[end] - FEE * size * n) / max(W, 4 * n) * 2.5, text, cost[end]


def _context(text):
    """Fix what the glyphs cannot tell apart: l / I (identical in guifont), 0 / O."""
    out = list(text)
    for i, c in enumerate(out):
        prev = out[i - 1] if i else " "
        nxt = out[i + 1] if i + 1 < len(out) else " "
        if c == "I" and (prev.islower() or nxt.islower() and prev not in " -(\"'"):
            out[i] = "l"
        elif c == "l" and prev in " -(" and nxt.isupper():
            out[i] = "I"
        elif c == "0" and (prev.isalpha() or nxt.isalpha()):
            out[i] = "O"
        elif c == "O" and prev.isdigit() and nxt.isdigit():
            out[i] = "0"
    return "".join(out)


def _trim(im):
    box = im.point(lambda v: 255 if v > INK else 0).getbbox()
    return im.crop((box[0], 0, box[2], im.height)) if box else im


def _norm_name(t):
    import re
    t = re.sub(r"\s*([_.])\s*", r"\1", t.lower())         # OCR puts spaces round "_" and "."
    return " ".join(t.replace("’", "'").replace("‘", "'").split())


def closest(text, names, limit=0.75, margin=0.0):
    """The name in NAMES nearest to a read TEXT (difflib ratio), or None below LIMIT or when the
    runner-up is within MARGIN of it (v2.1 / v2.10)."""
    import difflib
    t = _norm_name(text)
    scored = sorted(((difflib.SequenceMatcher(None, t, _norm_name(n)).ratio(), n) for n in names), reverse=True)
    if not scored or scored[0][0] < limit:
        return None
    if scored[0][0] == 1.0:
        return scored[0][1]
    if len(scored) > 1 and scored[0][0] - scored[1][0] < margin:
        return None
    return scored[0][1]


# ---------------------------------------------------------------- Tesseract (NormCap's copy)

TESS = ["flatpak", "run", "--env=TESSDATA_PREFIX=/app/share/tessdata", "--command=tesseract",
        "com.github.dynobo.normcap"]
UP = 3                           # Tesseract reads the game's small text best enlarged 3x


@functools.lru_cache(maxsize=1)
def tesseract_ok():
    """Is NormCap's Tesseract there (the flatpak com.github.dynobo.normcap)?"""
    import subprocess
    try:
        r = subprocess.run(TESS + ["--version"], capture_output=True, timeout=30)
        return r.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def is_light(img, box):
    """Is the text in BOX lighter than what is behind it?"""
    L = img.convert("L").crop(box)
    hist = L.histogram()
    n, acc, bg = sum(hist), 0, 0
    for v, c in enumerate(hist):                            # median = the background
        acc += c
        if acc >= n / 2:
            bg = v
            break
    hi = sum(c for v, c in enumerate(hist) if v > bg + 50)
    lo = sum(c for v, c in enumerate(hist) if v < bg - 50)
    return hi > lo


def _normalise(img, box, light, G=None):
    """[the box ready for Tesseract] plus, for dark text on parchment next to a dark panel, a
    second version with the parchment's border ridge painted out (Tesseract reads the better)."""
    from PIL import ImageOps
    G = G or img.convert("L")
    L = G.crop(box)
    out = [L]
    if not light and box[0] >= 3:
        Lw = _whiten_border(G, L, box)
        if Lw is not L:
            out.append(Lw)
    res = []
    for L in out:
        if light:
            L = ImageOps.invert(L)
        L = ImageOps.autocontrast(L, cutoff=1)
        res.append(L.resize((L.width * UP, L.height * UP), Image.Resampling.LANCZOS))
    return res


def _whiten_border(G, L, box, most=6):
    """Dark text on parchment with the window's dark panel just left of the box: the parchment's
    border ridge sits against the first letter ("[ihe" for "The"); paint it parchment colour, up
    to the first blank column."""
    if ImageStat.Stat(G.crop((box[0] - 3, box[1], box[0], box[3]))).mean[0] >= 90:
        return L
    bg = ImageStat.Stat(L).median[0]
    if bg < 110:
        return L
    px = L.load()
    W, H = L.size
    blank = None
    for x in range(1, min(most, W)):                        # the gap between ridge and letter
        col = [px[x, y] for y in range(H)]
        if min(col) > bg - 50 and max(col) < bg + 50:
            blank = x
            break
    if blank is None:                                       # no gap: the box starts on a letter
        return L
    L = L.copy()
    px = L.load()
    for x in range(blank):
        for y in range(H):
            px[x, y] = int(bg)
    return L


def ocr(img, boxes, lights=None, psm=6):
    """Read many text boxes with one Tesseract call: each box is cut out, turned dark-on-white,
    enlarged and stacked on a strip; the words are put back by height. Returns per box a dict:
    text, score (1 - Tesseract's confidence; under ~0.25 is a clean read), box, words
    [(text, conf, (x0, y0, x1, y1) on screen)]."""
    import subprocess
    boxes = [tuple(b) for b in boxes]
    if not boxes:
        return []
    if lights is None:
        lights = [is_light(img, b) for b in boxes]
    G = img.convert("L")
    pieces, owner = [], []                                  # owner: which box a piece reads
    for i, (b, l) in enumerate(zip(boxes, lights)):
        for p in _normalise(img, b, l, G):
            pieces.append(p)
            owner.append(i)
    GAP = 24
    W = max(p.width for p in pieces) + 2 * GAP
    H = sum(p.height + GAP for p in pieces) + GAP
    strip = Image.new("L", (W, H), 255)
    rows, y = [], GAP
    for p in pieces:
        strip.paste(p, (GAP, y))
        rows.append((y, y + p.height))
        y += p.height + GAP
    import io
    buf = io.BytesIO()
    strip.save(buf, "PNG")
    r = subprocess.run(TESS + ["stdin", "stdout", "--psm", str(psm), "tsv"], input=buf.getvalue(),
                       capture_output=True, timeout=120)
    words = [[] for _ in pieces]
    for line in r.stdout.decode("utf-8", "replace").splitlines()[1:]:
        f = line.split("\t")
        if len(f) < 12 or f[0] != "5" or not f[11].strip():
            continue
        x, yy, w, h, conf = int(f[6]), int(f[7]), int(f[8]), int(f[9]), float(f[10])
        cy = yy + h / 2
        for i, (a, b) in enumerate(rows):
            if a - GAP / 2 <= cy <= b + GAP / 2:
                bx = boxes[owner[i]]
                sx0 = bx[0] + (x - GAP) / UP
                sy0 = bx[1] + (yy - a) / UP
                words[i].append((f[11], conf, (round(sx0), round(sy0), round(sx0 + w / UP), round(sy0 + h / UP)),
                                 int(f[2]), int(f[4])))
                break
    out = [None] * len(boxes)
    for i, ws in enumerate(words):
        ws.sort(key=lambda w: (w[3], w[4], w[2][0]))
        text = " ".join(w[0] for w in ws)
        conf = sum(w[1] for w in ws) / len(ws) if ws else 0
        res = {"text": text, "score": round(1 - conf / 100, 3), "box": boxes[owner[i]],
               "words": [(w[0], w[1], w[2]) for w in ws], "engine": "tesseract"}
        k = owner[i]
        if out[k] is None or res["score"] < out[k]["score"] - 0.01:
            out[k] = res
    return out


def read_any(img, box, light=None, font="guifont.ttf"):
    """Read one box: Tesseract when NormCap is installed, else the glyph reader."""
    if light is None:
        light = is_light(img, box)
    if tesseract_ok():
        return ocr(img, [box], [light])[0]
    r = read(img, box, light=light, font=font, detail=True)
    r["engine"] = "glyphs"
    return r


# ---------------------------------------------------------------- the scene

B = 8                            # block size of the classification grid


def _grid(img):
    """Per 8x8 block: (r, g, b, luminance, std of luminance), as row lists."""
    rgb = img.convert("RGB")
    W, H = rgb.size[0] // B, rgb.size[1] // B
    small = rgb.resize((W, H), Image.Resampling.BOX).load()
    L = rgb.convert("L")
    m1 = L.convert("F").resize((W, H), Image.Resampling.BOX).load()
    sq = ImageChops.multiply(L, L).convert("F").resize((W, H), Image.Resampling.BOX).load()
    out = []
    for y in range(H):
        row = []
        for x in range(W):
            r, g, b = small[x, y]
            mean = m1[x, y]
            var = max(0.0, sq[x, y] * 255 - mean * mean)
            row.append((r, g, b, mean, var ** 0.5))
        out.append(row)
    return out


def _kind(r, g, b, lum, std):
    """What one block looks like on its own."""
    sat = max(r, g, b) - min(r, g, b)
    if sat <= 10 and 3 <= lum <= 85 and std <= 6:
        return "panel"                                   # the dark UI panels
    if 120 <= lum <= 215 and r > g > b and 20 <= r - b <= 70 and std <= 22:
        return "parchment"
    if 75 <= r <= 135 and 28 <= r - g <= 55 and 3 <= g - b <= 25 and std <= 12:
        return "bar"                                     # red-brown group bars
    if std > 18:
        return "busy"                                    # text, sprites, trees, edges
    if b >= r - 4 and lum >= 140 and std <= 8:
        return "sky"
    if b > r + 10 and b >= g and 60 <= lum < 170:
        return "water"
    if b > r + 20 and b >= g:
        return "water" if lum < 170 else "sky"           # sea, lakes, the underwater menu world
    if lum < 60 and g >= r - 5:
        return "tree"
    return "land"


def _components(cells, W, H):
    """4-connected components of a set of (x, y) cells: [set]."""
    cells, out = set(cells), []
    while cells:
        seed = cells.pop()
        comp, stack = {seed}, [seed]
        while stack:
            x, y = stack.pop()
            for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if n in cells:
                    cells.remove(n)
                    comp.add(n)
                    stack.append(n)
        out.append(comp)
    return out


def _bbox(comp):
    xs = [c[0] for c in comp]
    ys = [c[1] for c in comp]
    return (min(xs) * B, min(ys) * B, (max(xs) + 1) * B, (max(ys) + 1) * B)


def _inside(a, b, slack=0):
    return a[0] >= b[0] - slack and a[1] >= b[1] - slack and a[2] <= b[2] + slack and a[3] <= b[3] + slack


def _overlap(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def edges(img, thr=38):
    """Mask (L, 255 = edge) of sharp local contrast: text strokes, sprite outlines, UI lines."""
    L = img.convert("L")
    hp = ImageChops.difference(L, L.filter(ImageFilter.BoxBlur(2)))
    return hp.point(lambda v: 255 if v > thr // 2 else 0)


def still(frames, thr=10):
    """(static mask, motion mask) from a burst of frames: the 3D world behind the menus moves
    (the camera flies), UI, text and sprites do not."""
    Ls = [f.convert("L") for f in frames]
    hi, lo = Ls[0], Ls[0]
    for f in Ls[1:]:
        hi, lo = ImageChops.lighter(hi, f), ImageChops.darker(lo, f)
    moving = ImageChops.difference(hi, lo).point(lambda v: 255 if v > thr else 0)
    return ImageChops.invert(moving), moving


def text_bands(mask, box, min_h=7, max_h=48, max_sprite=260):
    """Things in BOX of an edge mask, by recursive XY cuts: split on empty rows, then on column
    gaps wider than the piece is tall, then again on rows inside each piece (a list of icons next
    to names: the icon column and the name column cut apart first). [(x0, y0, x1, y1)]: pieces
    min_h..max_h tall are text candidates, taller ones (up to max_sprite) sprites."""
    out = []
    _cut(mask, box, out, min_h, max_sprite, 0)
    return out


def _profile(mask, box, axis):
    sub = mask.crop(box)
    W, H = sub.size
    if axis == "rows":
        p = sub.resize((1, H), Image.Resampling.BOX).load()
        return [p[0, y] * W / 255 for y in range(H)]
    p = sub.resize((W, 1), Image.Resampling.BOX).load()
    return [p[x, 0] * H / 255 for x in range(W)]


def _spans(prof, need, gap):
    """Runs of entries >= NEED, joined over holes up to GAP long: [(start, end)]."""
    out, start, last = [], None, None
    for i, v in enumerate(prof):
        if v >= need:
            if start is None:
                start = i
            elif i - last - 1 > gap:
                out.append((start, last + 1))
                start = i
            last = i
    if start is not None:
        out.append((start, last + 1))
    return out


def _cut(mask, box, out, min_h, max_sprite, depth):
    x0, y0, x1, y1 = box
    if x1 - x0 < 4 or y1 - y0 < 4:
        return
    prof = _profile(mask, box, "rows")
    rows = []
    for a, b in _spans(prof, 2, 1):
        rows.extend(_valleys(prof, a, b) if b - a > 30 else [(a, b)])
    if len(rows) == 1 and rows[0][1] - rows[0][0] > 40 and depth < 8:
        # nothing splits the rows (a scroll bar, an icon column): cut into columns first
        a, b = rows[0]
        cols = _spans(_profile(mask, (x0, y0 + a, x1, y0 + b), "cols"), 1, 6)
        if len(cols) > 1:
            for c, d in cols:
                if d - c >= 5:
                    _cut(mask, (x0 + c, y0 + a, x0 + d, y0 + b), out, min_h, max_sprite, depth + 1)
            return
    for a, b in rows:
        h = b - a
        if h < min_h - 2:
            continue
        rowbox = (x0, y0 + a, x1, y0 + b)
        cols = _spans(_profile(mask, rowbox, "cols"), 1, max(8, int(0.9 * min(h, 30))))
        for c, d in cols:
            if d - c < max(5, 0.4 * min(h, 30)):
                continue
            piece = (x0 + c, y0 + a, x0 + d, y0 + b)
            if depth < 8 and h > 40 and (len(cols) > 1 or len(rows) > 1):
                _cut(mask, piece, out, min_h, max_sprite, depth + 1)
            elif h <= max_sprite and (h <= 48 or d - c <= 4 * max_sprite):   # lines may be long
                out.append(_tight(mask, piece))


def _valleys(prof, a, b, frac=0.1, gap=2, least=8):
    """Split rows a..b at thin bands (GAP+ rows under FRAC of the block's busy rows): the specks
    of a textured panel join a paragraph's lines into one block. Keeps parts of LEAST rows."""
    seg = sorted(prof[a:b])
    thr = frac * seg[int(0.9 * (len(seg) - 1))]
    out, start, low = [], a, 0
    for y in range(a, b):
        if prof[y] < thr:
            low += 1
            continue
        if low >= gap and y - low - start >= least:
            out.append((start, y - low))
            start = y
        elif low >= gap and y - low - start < 4:
            start = y                                       # a panel's border line, specks
        low = 0
    end = b - low if low >= gap else b
    if end - start >= least or not out:
        out.append((start, end))
    elif out:
        out[-1] = (out[-1][0], end)
    return out


def _tight(mask, box):
    b = mask.crop(box).getbbox()
    return (box[0] + b[0], box[1] + b[1], box[0] + b[2], box[1] + b[3]) if b else box


def scene(img, frames=None, read_text=True):
    """Every element on the screen, organised:
    {"size", "windows": [{"box", "bars", "parchment", "text", "sprites"}], "floating": {"text",
    "sprites"}, "background": {"sky", "water", "land", "trees", "objects", "moving"}}.
    FRAMES (a burst from grab_frames) separates the moving 3D world from the still UI."""
    W, H = img.size
    grid = _grid(img)
    gw, gh = len(grid[0]), len(grid)
    kinds = [[_kind(*grid[y][x]) for x in range(gw)] for y in range(gh)]
    static = moving = None
    if frames:
        static, moving = still(frames)
        mv = moving.resize((gw, gh), Image.Resampling.BOX).load()
    # -- windows: rectangles of panel / parchment / bar blocks
    # windows grow from the flat dark-grey panel only: sand looks like parchment, but no part of
    # the 3D world is a flat, colourless grey
    ui = [(x, y) for y in range(gh) for x in range(gw) if kinds[y][x] == "panel"
          and not (frames and mv[x, y] > 60)]
    wins = []
    for comp in _components(ui, gw, gh):
        bx = _bbox(comp)
        area = (bx[2] - bx[0]) * (bx[3] - bx[1]) / B / B
        if bx[2] - bx[0] >= 64 and bx[3] - bx[1] >= 32 and len(comp) >= 0.15 * area and len(comp) >= 20:
            wins.append(bx)
    framed = window_frames(img)
    wins = [w for w in wins if not any(_overlap(w, f) for f in framed)] + framed
    wins = _merge(wins)
    E = edges(img)
    if static is not None:
        E_ui = ImageChops.multiply(E, static)               # edges that stay put = UI
    else:
        E_ui = E
    out = {"size": [W, H], "windows": [], "floating": {"text": [], "sprites": []},
           "background": {}}
    for wb in sorted(wins, key=lambda b: (b[1], b[0])):
        out["windows"].append(_window(img, wb, kinds, E, read_text))
    # -- floating UI outside the windows (main-menu buttons, labels, tooltips, banners)
    free = Image.new("L", (W, H), 255)
    for wb in wins:
        free.paste(0, wb)
    fe = ImageChops.multiply(E_ui, free)
    for tb in text_bands(fe, (0, 0, W, H)):
        h, wd = tb[3] - tb[1], tb[2] - tb[0]
        if static is None and not (8 <= h <= 48 and wd >= 2 * h):
            continue                                        # no frames: only text-shaped things
        out["floating"]["text"].append(_text(img, tb, read_text and not tesseract_ok()))
    if static is not None:
        out["floating"]["sprites"] = _blobs_of(ImageChops.multiply(static, free), img, wins, out["floating"]["text"])
    else:                                                   # text-shaped but not text: drop
        out["floating"]["text"] = [t for t in out["floating"]["text"] if t["kind"] == "text"]
    if frames:
        out["frames"] = len(frames)
    if read_text and tesseract_ok():
        _read_all(img, out)
    # -- background
    out["background"] = _background(kinds, wins, gw, gh, moving)
    return out


def _trim_specks(E, box, most=6):
    """Cut a panel's border line off the ends of a text box: a column within MOST pixels of an
    end whose edge runs on well above and below the line (a letter stops with the line), and the
    empty columns after it."""
    x0, y0, x1, y1 = box
    h = y1 - y0
    if x1 - x0 < 4 * most:
        return box
    def rule(x):                                            # over a few lines and their gaps a
        c = E.crop((x, max(0, y0 - 60), x + 1, min(E.height, y1 + 60)))   # border covers ~0.8,
        return ImageStat.Stat(c).mean[0] / 255 >= 0.7       # aligned capitals at most ~0.5

    p = E.crop(box).resize((x1 - x0, 1), Image.Resampling.BOX).load()
    cov = [p[x, 0] for x in range(x1 - x0)]
    a = 0                                                   # just past the line: the letter's
    for k in range(most):                                   # faint antialiased edge counts as blank
        if rule(x0 + k):
            a = k + 2
    b = 0
    for k in range(most):
        if rule(x1 - 1 - k):
            b = k + 2
    x0, x1 = x0 + a, x1 - b
    rp = E.crop((x0, y0, x1, y1)).resize((1, y1 - y0), Image.Resampling.BOX).load()
    rows = [rp[0, y] / 255 for y in range(y1 - y0)]
    on = [r >= 0.06 for r in rows]
    runs, k = [], 0                                         # runs of busy rows
    while k < len(on):
        if on[k]:
            e = k
            while e < len(on) and on[e]:
                e += 1
            runs.append((k, e))
            k = e
        else:
            k += 1
    top, bot = 0, len(rows)
    if len(runs) > 1:                                       # a thin strip apart from the text is
        if runs[-1][1] - runs[-1][0] <= 4 and runs[-1][0] - runs[-2][1] >= 3:   # a panel's edge
            bot = runs[-2][1]
        if runs[0][1] - runs[0][0] <= 4 and runs[1][0] - runs[0][1] >= 3:
            top = runs[1][0]
    if bot - top < 6:
        top, bot = 0, len(rows)
    return (x0, y0 + top, x1, y0 + bot)


def _clean(r):
    """Drop the stray marks Tesseract makes of a panel's border at either end of a line:
    a first or last 'word' of one or two non-letters, or a low-confidence single letter."""
    ws = list(r["words"])
    if len(ws) > 1 and 2 <= len(ws[0][0]) <= 3 and ws[0][0][0] in "[|({" and ws[0][0][-1].isupper() \
            and ws[1][0][:1].islower():                       # "[A dd" -> "Add": a border split it
        ws[0:2] = [(ws[0][0][-1] + ws[1][0], min(ws[0][1], ws[1][1]),
                    (ws[0][2][0], ws[1][2][1], ws[1][2][2], ws[1][2][3]))]
    junk = lambda w: (len(w[0]) <= 2 and not any(c.isalnum() for c in w[0])) or \
        (len(w[0]) <= 2 and w[1] < 60 and len(ws) > 1)
    while ws and junk(ws[0]):
        ws.pop(0)
    while ws and junk(ws[-1]):
        ws.pop()
    if ws:
        first = ws[0][0]
        if len(first) > 2 and first[0] in "[|({/\\'‘“\"" and first[1].isalpha():
            ws[0] = (first[1:],) + tuple(ws[0][1:])
    text = " ".join(w[0] for w in ws)
    conf = sum(w[1] for w in ws) / len(ws) if ws else 0
    return dict(r, text=text, words=ws, score=round(1 - conf / 100, 3))


def _read_all(img, sc):
    """Read every text box and bar title of a scene in one Tesseract call; boxes it cannot
    read are moved to the sprites/icons."""
    items = []
    for w in sc["windows"]:
        items += [("text", w, t) for t in w["text"]]
        items += [("bar", w, b) for b in w["bars"]]
    items += [("float", None, t) for t in sc["floating"]["text"]]
    wide = lambda t: t["box"][2] - t["box"][0] >= 3 * (t["box"][3] - t["box"][1]) and t["box"][3] - t["box"][1] <= 48
    items += [("wsprite", w, t) for w in sc["windows"] for t in w["sprites"] if wide(t)]
    items += [("fsprite", None, t) for t in sc["floating"]["sprites"] if wide(t)]
    boxes = []
    E = edges(img)
    for kind, _, t in items:
        bx = t["box"]
        if kind == "bar":                                   # the title, inside the bar's end caps
            inner = (bx[0] + 24, bx[1] + 3, bx[2] - 24, bx[3] - 3)
            ink = E.crop(inner).getbbox()
            bx = (inner[0] + ink[0], inner[1], inner[0] + ink[2], inner[3]) if ink else inner
            boxes.append((bx[0] - 2, bx[1], bx[2] + 2, bx[3]))
        else:
            tb = _trim_specks(E, bx)
            pad = 1
            boxes.append((max(0, tb[0] - pad), max(0, tb[1] - 3), tb[2] + 1, tb[3] + 3))
    reads = ocr(img, boxes)
    retry = [i for i, r in enumerate(reads) if items[i][0] in ("text", "float")
             and sum(c.isalnum() for c in r["text"]) >= 4 and r["score"] >= 0.5][:10]
    for i in retry:                                         # Tesseract sometimes gives up on a line
        again = ocr(img, [boxes[i]])[0]                     # inside the strip; alone it reads it
        if again["score"] < reads[i]["score"]:
            reads[i] = again
    for (kind, w, t), r in zip(items, reads):
        r = _clean(r)
        alnum = sum(c.isalnum() for c in r["text"])
        sure = max((w[1] for w in r["words"]), default=0)    # one word read with confidence
        good = bool(r["text"]) and alnum > 0 and (r["score"] < (0.2 if len(r["text"]) <= 2 else 0.5)
                                                  or (alnum >= 4 and sure >= 85))
        if kind == "bar":
            if good:
                t["text"] = r["text"]
            continue
        if kind in ("wsprite", "fsprite"):                 # a highlighted button, a coloured label
            if good and r["score"] < 0.25:
                t.update(kind="text", text=r["text"], score=r["score"], words=r["words"])
                src, dst = (w["sprites"], w["text"]) if w is not None else \
                    (sc["floating"]["sprites"], sc["floating"]["text"])
                src.remove(t)
                dst.append(t)
            continue
        if good:
            t.update(text=r["text"], score=r["score"], words=r["words"])
            continue
        h, wd = t["box"][3] - t["box"][1], t["box"][2] - t["box"][0]
        if kind == "float" and "frames" not in sc:
            sc["floating"]["text"].remove(t)                # background texture, not text
            continue
        t.clear()
        t.update(kind="sprite" if max(h, wd) > 44 else "icon", box=r["box"])
        if w is not None:
            w["text"].remove(t)
            w["sprites"].append(t)
        else:
            sc["floating"]["text"].remove(t)
            sc["floating"]["sprites"].append(t)


def window_frames(img, min_len=100):
    """Window boxes from the tan frame the game draws round every window: a vertical strip of
    frame colour with dark panel 10 px inside it, on the left and on the right, at the same
    height. Finds translucent windows (the nation list) that the panel colour misses."""
    W, H = img.size
    h, sat, v = img.convert("RGB").convert("HSV").split()
    tan = ImageChops.multiply(ImageChops.multiply(
        h.point(lambda x: 255 if 18 <= x <= 36 else 0),            # hue 25-50 degrees
        sat.point(lambda x: 255 if 45 <= x <= 120 else 0)),
        v.point(lambda x: 255 if 110 <= x <= 200 else 0))
    dark = img.convert("L").point(lambda x: 255 if x < 95 else 0)

    def shifted(m, dx):
        out = Image.new("L", m.size, 0)
        out.paste(m, (dx, 0))
        return out

    sides = {}
    for side, dx in (("left", -10), ("right", 10)):          # dark panel 10 px inside the frame
        edge = ImageChops.multiply(tan, shifted(dark, dx))
        cols = edge.resize((W, 1), Image.Resampling.BOX).load()
        px = edge.load()
        found = []
        for x in range(W):
            if cols[x, 0] * H / 255 < min_len:
                continue
            best, start, gap = (0, 0, 0), None, 0
            for y in range(H + 1):
                if y < H and px[x, y]:
                    start = y if start is None else start
                    gap = 0
                elif start is not None:
                    gap += 1
                    if gap > 12 or y == H:                      # bars and text may break the strip
                        if y - gap - start > best[0]:
                            best = (y - gap - start, start, y - gap)
                        start, gap = None, 0
            if best[0] >= min_len:
                found.append((x, best[1], best[2]))
        sides[side] = _thin(found)
    out = []
    for xl, a0, a1 in sides["left"]:
        for xr, b0, b1 in sides["right"]:
            if xr - xl >= 120 and abs(a0 - b0) <= 16 and abs(a1 - b1) <= 16:
                out.append((xl - 4, min(a0, b0), xr + 5, max(a1, b1)))
                break
    return out


def _thin(cols):
    """Keep one column per group of neighbouring columns (the longest)."""
    out = []
    for c in sorted(cols):
        if out and c[0] - out[-1][0] <= 6:
            if c[2] - c[1] > out[-1][2] - out[-1][1]:
                out[-1] = c
        else:
            out.append(c)
    return out


def _merge(boxes):
    boxes = list(boxes)
    changed = True
    while changed:
        changed = False
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                if _overlap(a, b):
                    boxes[i] = (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))
                    del boxes[j]
                    changed = True
                    break
            if changed:
                break
    return boxes


def _window(img, wb, kinds, E, read_text):
    x0, y0, x1, y1 = wb
    w = {"box": wb, "bars": [], "parchment": [], "text": [], "sprites": []}
    # header / group bars: rows where most of the width is bar-coloured
    px = img.convert("RGB").load()
    run = None
    for y in range(y0, y1):
        n = 0
        for x in range(x0, x1, 6):
            r, g, b = px[x, y]
            if (abs(r - 50) <= 6 and abs(g - 49) <= 6 and abs(b - 49) <= 6) or \
               (75 <= r <= 135 and 28 <= r - g <= 55 and 3 <= g - b <= 25):
                n += 1
        on = n >= 0.6 * ((x1 - x0) // 6)
        if on and run is None:
            run = y
        elif not on and run is not None:
            if 12 <= y - run <= 40:
                w["bars"].append({"box": (x0, run, x1, y)})
            run = None
    if len(w["bars"]) > 6:                                   # striped list rows, not header bars
        w["bars"] = []
    # parchment sub-panels
    cells = [(x, y) for y in range(y0 // B, y1 // B) for x in range(x0 // B, x1 // B)
             if y < len(kinds) and x < len(kinds[0]) and kinds[y][x] == "parchment"]
    for comp in _components(cells, 0, 0):
        bx = _bbox(comp)
        if len(comp) >= 6:
            w["parchment"].append(bx)
    # text lines and sprites from the edge mask inside the window
    inner = (x0 + 14, y0 + 14, x1 - 14, y1 - 14)          # inside the frame
    if w["bars"]:                                          # bars are read on their own
        E = E.copy()
        for bar in w["bars"]:
            E.paste(0, bar["box"])
    for tb in text_bands(E, inner):
        if tb[2] - tb[0] < 6 or tb[3] - tb[1] < 6:          # panel edges, specks
            continue
        t = _text(img, tb, read_text and not tesseract_ok())
        (w["text"] if t["kind"] == "text" else w["sprites"]).append(t)
    for bar in w["bars"]:
        inside = [t for t in w["text"] if _inside(t["box"], bar["box"], 3)]
        w["text"] = [t for t in w["text"] if t not in inside]
        if read_text and not tesseract_ok():                # panel titles use the fancy font
            bx = bar["box"]
            r = min((read(img, (bx[0] + 14, bx[1], bx[2] - 14, bx[3]), light=True, font=f, detail=True, pad=2)
                     for f in ("guifont.ttf", "guifont_fancy.ttf")), key=lambda r: r["score"])
            if r["text"] and r["score"] < 0.3:
                bar["text"] = r["text"]
            elif inside:
                bar["text"] = inside[0].get("text")
    return w


def _text(img, tb, read_text):
    """Classify a band of edges as text (with its reading) or as a sprite/icon."""
    x0, y0, x1, y1 = tb
    h, wd = y1 - y0, x1 - x0
    # the game's text is grey, white or black; sprites are coloured: saturation on the edges
    S = img.crop(tb).convert("RGB").convert("HSV").split()[1]
    em = edges(img.crop(tb))
    sat = ImageStat.Stat(S, em) if em.getbbox() else ImageStat.Stat(S)
    colourful = sat.mean[0] > 80 or sat.stddev[0] > 48
    if h > 34 or h < 7 or (colourful and wd < 2.5 * h):
        return {"kind": "sprite" if max(h, wd) > 44 else "icon", "box": tb}
    tb = _strip_rule(img, tb)
    t = {"kind": "text", "box": tb}
    if read_text:
        best = None
        for light in (True, False):
            r = read(img, tb, light=light, detail=True, pad=3)
            if r["text"] and (best is None or r["score"] < best["score"]):
                best = dict(r, light=light)
        if best is None or best["score"] > 0.33:
            return {"kind": "sprite" if max(h, wd) > 44 else "icon", "box": tb}
        t.update(text=best["text"], score=round(best["score"], 3), size=best["size"], light=best["light"])
    return t


def _strip_rule(img, tb):
    """Drop a panel border line caught at the start or end of a text box: a run of at most
    3 columns that covers nearly the whole height, with a gap after it."""
    m = edges(img.crop(tb))
    W, H = m.size
    p = m.resize((W, 1), Image.Resampling.BOX).load()
    cov = [p[x, 0] * H / 255 for x in range(W)]
    x0, x1 = tb[0], tb[2]
    run = 0
    while run < W and cov[run] > 0:
        run += 1
    if 0 < run <= 3 and max(cov[:run]) >= 0.85 * H and run + 2 < W and cov[run] == 0:
        k = run
        while k < W and cov[k] == 0:
            k += 1
        x0 = tb[0] + k
    run = 0
    while run < W and cov[W - 1 - run] > 0:
        run += 1
    if 0 < run <= 3 and max(cov[W - run:]) >= 0.85 * H and run + 2 < W and cov[W - 1 - run] == 0:
        k = run
        while k < W and cov[W - 1 - k] == 0:
            k += 1
        x1 = tb[2] - k
    return (x0, tb[1], x1, tb[3]) if x1 - x0 >= 4 else tb


def _blobs_of(mask, img, wins, texts):
    """Still, colourful things outside windows and text: banners, sprites on the map."""
    W, H = img.size
    gw, gh = W // B, H // B
    m = mask.resize((gw, gh), Image.Resampling.BOX).load()
    g = _grid(img)
    cells = [(x, y) for y in range(gh) for x in range(gw) if m[x, y] > 200 and g[y][x][4] > 12]
    out = []
    for comp in _components(cells, gw, gh):
        bx = _bbox(comp)
        if len(comp) < 4 or any(_overlap(bx, t["box"]) for t in texts):
            continue
        out.append({"kind": "sprite", "box": bx})
    return out


def _background(kinds, wins, gw, gh, moving):
    counts, objects = {}, []
    free = [(x, y) for y in range(gh) for x in range(gw)
            if not any(_inside((x * B, y * B, x * B + B, y * B + B), wb) for wb in wins)]
    for x, y in free:
        k = kinds[y][x]
        if k in ("panel", "parchment", "bar"):
            k = "land" if y > gh // 3 else "sky"
        counts[k] = counts.get(k, 0) + 1
    trees = [(x, y) for x, y in free if kinds[y][x] == "tree"]
    for comp in _components(trees, gw, gh):
        if len(comp) >= 3:
            objects.append({"kind": "tree/object", "box": _bbox(comp)})
    total = max(1, len(free))
    bg = {k: round(v / total, 3) for k, v in sorted(counts.items(), key=lambda kv: -kv[1])}
    bg["objects"] = sorted(objects, key=lambda o: -(o["box"][2] - o["box"][0]) * (o["box"][3] - o["box"][1]))[:40]
    if moving is not None:
        bg["moving"] = round(ImageStat.Stat(moving).mean[0] / 255, 3)
    return bg


def draw(img, sc, path):
    """Write IMG with the scene's boxes drawn on it."""
    out = img.convert("RGB").copy()
    d = ImageDraw.Draw(out)
    col = {"window": (255, 255, 0), "bar": (255, 128, 0), "parchment": (200, 150, 255), "text": (0, 255, 0),
           "sprite": (255, 0, 255), "icon": (0, 200, 255), "object": (255, 60, 60)}
    for w in sc["windows"]:
        d.rectangle(w["box"], outline=col["window"], width=3)
        for b in w["bars"]:
            d.rectangle(b["box"], outline=col["bar"], width=2)
        for p in w["parchment"]:
            d.rectangle(p, outline=col["parchment"], width=1)
        for t in w["text"]:
            d.rectangle(t["box"], outline=col["text"], width=1)
        for t in w["sprites"]:
            d.rectangle(t["box"], outline=col[t["kind"]], width=2)
    for t in sc["floating"]["text"]:
        d.rectangle(t["box"], outline=col["text"], width=2)
    for t in sc["floating"]["sprites"]:
        d.rectangle(t["box"], outline=col["sprite"], width=2)
    for o in sc["background"].get("objects", []):
        d.rectangle(o["box"], outline=col["object"], width=1)
    out.save(path)


# ---------------------------------------------------------------- templates ("regex for images")

def _index():
    try:
        with open(os.path.join(TEMPLATES, "index.json")) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def add(name, img, box, kind="sprite", note=""):
    """Save the part of IMG in BOX as template NAME (kind: sprite, icon, ui or text)."""
    os.makedirs(TEMPLATES, exist_ok=True)
    img.convert("RGB").crop(box).save(os.path.join(TEMPLATES, name + ".png"))
    idx = _index()
    idx[name] = {"kind": kind, "note": note, "size": [box[2] - box[0], box[3] - box[1]], "screen": list(img.size)}
    with open(os.path.join(TEMPLATES, "index.json"), "w") as f:
        json.dump(idx, f, indent=1, sort_keys=True)
    return idx[name]


def _mask(t):
    """Pixels of a template that belong to it: not the black (transparent) or panel-dark
    background a sprite sits on."""
    return t.convert("L").point(lambda v: 255 if v > 24 else 0)


def _score(region, t, m):
    d = ImageChops.difference(region.convert("RGB"), t).convert("L")
    st = ImageStat.Stat(d, m)
    return st.mean[0] / 255 if st.count[0] else 1.0


def find(img, names, box=None, scales=None, limit=0.1, places=None):
    """Where templates NAMES appear in IMG: [(score, name, (x0, y0, x1, y1))], best first, score
    = mean colour difference over the template's own pixels (0 = identical, under ~0.1 = found).
    Sprites and map text change size with zoom, so each template is tried at SCALES (default
    0.5-2x) at the places the scene parser found (sprites, icons, text), or at PLACES given,
    sliding a little in each; BOX limits the search."""
    if places is None:
        sc = scene(img, read_text=False)
        places = [e["box"] for w in sc["windows"] for e in w["text"] + w["sprites"]]
        places += [e["box"] for e in sc["floating"]["text"] + sc["floating"]["sprites"]]
        places += [o["box"] for o in sc["background"].get("objects", [])]
    if box:
        places = [p for p in places if _overlap(p, box)]
    rgb = img.convert("RGB")
    out = []
    for name in names:
        t0 = Image.open(os.path.join(TEMPLATES, name + ".png")).convert("RGB")
        found = []
        for p in places:
            pw, ph = p[2] - p[0], p[3] - p[1]
            k = min(pw / t0.width, ph / t0.height)          # the scale that fits the element
            ks = scales or sorted({round(k * f, 3) for f in (0.9, 1.0, 1.1)} | ({1.0} if k >= 1 else set()))
            for s in ks:
                if not 0.3 <= s <= 3.5:
                    continue
                tw, th = max(2, round(t0.width * s)), max(2, round(t0.height * s))
                t = t0.resize((tw, th), Image.Resampling.LANCZOS) if s != 1 else t0
                m = _mask(t)
                best = None
                for dy in range(-4, max(0, ph - th) + 5, 2):
                    for dx in range(-4, max(0, pw - tw) + 5, 2):
                        x, y = p[0] + dx, p[1] + dy
                        if x < 0 or y < 0 or x + tw > img.width or y + th > img.height:
                            continue
                        sc_ = _score(rgb.crop((x, y, x + tw, y + th)), t, m)
                        if best is None or sc_ < best[0]:
                            best = (sc_, (x, y, x + tw, y + th))
                if best:                                     # then to the pixel
                    bx0, by0 = best[1][0], best[1][1]
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            x, y = bx0 + dx, by0 + dy
                            if 0 <= x and 0 <= y and x + tw <= img.width and y + th <= img.height:
                                sc_ = _score(rgb.crop((x, y, x + tw, y + th)), t, m)
                                if sc_ < best[0]:
                                    best = (sc_, (x, y, x + tw, y + th))
                if best and best[0] <= limit:
                    found.append((round(best[0], 3), name, best[1]))
        found.sort()
        kept = []
        for f in found:                                      # one hit per place
            if not any(_overlap(f[2], k[2]) for k in kept):
                kept.append(f)
        out.extend(kept)
    return sorted(out)


# ---------------------------------------------------------------- command line

def _grab_game(n=1, gap=0.25):
    """Grab the game (N frames GAP s apart) under the dom6ui guard: waits until the user is
    idle, grabs only while the game is in front, gives focus back afterwards."""
    import session
    got = []
    session.run(lambda g: got.append(g.grab() if n == 1 else g.burst(n, gap)), "vision")
    return got[0]


def _summary(sc):
    lines = [f"screen {sc['size'][0]}x{sc['size'][1]}"]
    for i, w in enumerate(sc["windows"]):
        lines.append(f"window {i} {w['box']}")
        for b in w["bars"]:
            lines.append(f"  bar   {b['box']} {b.get('text') or ''}")
        for t in sorted(w["text"] + w["sprites"], key=lambda e: (e["box"][1], e["box"][0])):
            label = repr(t.get("text")) + f" ({t.get('score')})" if t["kind"] == "text" and "text" in t else ""
            lines.append(f"  {t['kind']:6} {t['box']} {label}")
    for t in sc["floating"]["text"] + sc["floating"]["sprites"]:
        lines.append(f"floating {t['kind']:6} {t['box']} {repr(t.get('text', ''))}")
    bg = dict(sc["background"])
    objs = bg.pop("objects", [])
    lines.append(f"background {bg}, {len(objs)} trees/objects")
    return "\n".join(lines)


def main(argv):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("scene")
    a.add_argument("image", nargs="?")
    a.add_argument("--out")
    a.add_argument("--json", action="store_true")
    a.add_argument("--frames", type=int, default=0, help="grab a burst of N frames to tell the moving world from the UI")
    a.add_argument("--no-text", action="store_true")
    a = sub.add_parser("read")
    a.add_argument("image")
    a.add_argument("box", type=int, nargs=4)
    a.add_argument("--dark", action="store_true")
    a.add_argument("--fancy", action="store_true")
    a.add_argument("--size", type=float)
    a.add_argument("--glyphs", action="store_true", help="the font-glyph reader, not Tesseract")
    a = sub.add_parser("find")
    a.add_argument("image")
    a.add_argument("names", nargs="+")
    a.add_argument("--box", type=int, nargs=4)
    a = sub.add_parser("add")
    a.add_argument("name")
    a.add_argument("image")
    a.add_argument("box", type=int, nargs=4)
    a.add_argument("--kind", default="sprite", choices=("sprite", "icon", "ui", "text"))
    a.add_argument("--note", default="")
    sub.add_parser("templates")
    a = sub.add_parser("video")
    a.add_argument("out")
    a.add_argument("--n", type=int, default=16)
    a.add_argument("--gap", type=float, default=0.25)
    o = ap.parse_args(argv)

    if o.cmd == "scene":
        frames = None
        if o.image:
            img = Image.open(o.image)
        elif o.frames > 1:
            frames = _grab_game(o.frames)
            img = frames[-1]
        else:
            img = _grab_game()
        sc = scene(img, frames=frames, read_text=not o.no_text)
        if o.out:
            draw(img, sc, o.out)
        print(json.dumps(sc, indent=1) if o.json else _summary(sc))
    elif o.cmd == "read":
        img, light = Image.open(o.image), (False if o.dark else None)
        if o.glyphs or not tesseract_ok():
            r = read(img, tuple(o.box), light=light is None or light,
                     font="guifont_fancy.ttf" if o.fancy else "guifont.ttf", size=o.size, detail=True)
        else:
            r = _clean(ocr(img, [tuple(o.box)], None if light is None else [light])[0])
        print(f"{r['text']!r}  score {r['score']:.3f}  box {r['box']}  ({r.get('engine', 'glyphs')})")
    elif o.cmd == "find":
        for sc_, name, bx in find(Image.open(o.image), o.names, box=tuple(o.box) if o.box else None):
            print(f"{name:24} {sc_:.3f} {bx}")
    elif o.cmd == "add":
        print(add(o.name, Image.open(o.image), tuple(o.box), o.kind, o.note))
    elif o.cmd == "templates":
        for k, v in sorted(_index().items()):
            print(f"{k:24} {v['kind']:6} {v['size'][0]}x{v['size'][1]}  {v.get('note', '')}")
    elif o.cmd == "video":
        fr = _grab_game(o.n, o.gap)
        half = [f.convert("RGB").resize((f.width // 2, f.height // 2)) for f in fr]
        half[0].save(o.out, save_all=True, append_images=half[1:], duration=int(o.gap * 1000), loop=0)
        st, mv = still(fr)
        print(f"{len(fr)} frames -> {o.out}; moving part of the screen {ImageStat.Stat(mv).mean[0] / 255:.1%}")


if __name__ == "__main__":
    main(sys.argv[1:])
