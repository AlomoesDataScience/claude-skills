"""abccheck.py - check ABC tunes for bar lengths, voice bar counts and pitch range (read only).

Usage:
  python3 -I abccheck.py FILE [FILE...] [--bars] [--max N]

  FILE    a text file holding one or more ABC tunes (X: starts each tune)
  --bars  list every bar's length, not only the wrong ones
  --max N print at most N problem lines per tune (default 40)

What it checks, per tune and per voice:
  - each bar's length against the metre (M:), with L:, tuplets, chords and inline [M:]/[L:] changes;
    a short first bar is reported as a pickup, a short last bar as fine when pickup + last = one bar
  - voices with different bar counts (they drift apart when played)
  - the lowest and highest note (MIDI numbers, key signature ignored) and notes off the 88-key range
  - uppercase notes with ' (C' means c; legal for some programs, unclear for others)
It does not play, render or change anything. Written for our own use (Claude, 2026-11-25), from the
ABC 2.1 rules as Claude knows them; no code from EasyABC or any other program.
"""
import re
import sys
from fractions import Fraction as F

NOTE_BASE = {"C": 60, "D": 62, "E": 64, "F": 65, "G": 67, "A": 69, "B": 71}
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def midi_name(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def parse_meter(v):
    v = v.strip().split()[0] if v.strip() else ""
    if v in ("C", "C|"):
        return F(1)
    if v.lower() == "none" or not v:
        return None
    m = re.match(r"\(?([\d+]+)\)?/(\d+)", v)
    if not m:
        return None
    return F(sum(int(x) for x in m.group(1).split("+")), int(m.group(2)))


def parse_len(v):
    m = re.match(r"\s*(\d+)/(\d+)", v)
    return F(int(m.group(1)), int(m.group(2))) if m else None


def read_dur(s, i):
    """Read a duration suffix at s[i:]; return (multiplier, new i)."""
    m = re.match(r"(\d*)(/*)(\d*)", s[i:])
    d1, sl, d2 = m.groups()
    num = int(d1) if d1 else 1
    if sl:
        den = int(d2) if d2 else 2 ** len(sl)
    else:
        den = 1
    return F(num, den), i + m.end()


class Voice:
    def __init__(self, name):
        self.name = name
        self.bars = []        # (length, metre, line number)
        self.cur = F(0)
        self.notes = []       # midi numbers
        self.upper_tick = 0

    def close(self, meter, line):
        if self.cur > 0:
            self.bars.append((self.cur, meter, line))
        self.cur = F(0)


def check_tune(lines, show_bars, cap):
    head = {}
    out = []
    voices = {}
    meter = F(1)
    unit = None
    vname = "1"
    in_body = False
    tuplet = None   # [left, factor]
    compound = False

    def voice():
        if vname not in voices:
            voices[vname] = Voice(vname)
        return voices[vname]

    def default_unit():
        return F(1, 16) if meter is not None and meter < F(3, 4) else F(1, 8)

    def set_field(k, v):
        nonlocal meter, unit, vname, compound
        if k == "M":
            meter = parse_meter(v)
            compound = meter is not None and meter.numerator % 3 == 0 and meter.numerator > 3
        elif k == "L":
            unit = parse_len(v) or unit
        elif k == "V":
            vname = v.split()[0] if v.split() else "1"

    for ln, raw in lines:
        line = raw.rstrip("\n")
        if line.startswith("%"):
            continue
        fm = re.match(r"^([A-Za-z]):(.*)$", line)
        if fm:
            k, v = fm.group(1), fm.group(2)
            if not in_body:
                head.setdefault(k, v.strip())
            if k in "wWs":
                continue
            set_field(k, v)
            if k == "K" and not in_body:
                in_body = True
                if unit is None:
                    unit = default_unit()
            continue
        if not in_body:
            continue
        if unit is None:
            unit = default_unit()
        s = re.sub(r"(?<!\\)%.*$", "", line)
        i = 0
        n = len(s)
        while i < n:
            c = s[i]
            if c in " \t\\`y-)":
                i += 1
            elif c == '"':
                j = s.find('"', i + 1)
                i = n if j < 0 else j + 1
            elif c in "!+":
                j = s.find(c, i + 1)
                i = n if j < 0 else j + 1
            elif c == "{":
                j = s.find("}", i + 1)
                i = n if j < 0 else j + 1
            elif c == "(":
                m = re.match(r"\((\d)(?::(\d*))?(?::(\d*))?", s[i:])
                if m:
                    p = int(m.group(1))
                    q = int(m.group(2)) if m.group(2) else (3 if p in (2, 4, 8) else 2 if p in (3, 6)
                                                            else (3 if compound else 2))
                    r = int(m.group(3)) if m.group(3) else p
                    tuplet = [r, F(q, p)]
                    i += m.end()
                else:
                    i += 1
            elif c == "[" and re.match(r"\[[A-Za-z]:", s[i:]):
                j = s.find("]", i)
                j = n if j < 0 else j
                body = s[i + 1:j]
                k, v = body[0], body[2:]
                set_field(k, v)
                i = j + 1
            elif c == "[" and i + 1 < n and s[i + 1].isdigit():
                m = re.match(r"\[[\d,\-]+", s[i:])
                i += m.end()
            elif c in "|:[]" :
                if c == "[" and i + 1 < n and s[i + 1] == "|":
                    voice().close(meter, ln)
                    i += 2
                    continue
                if c == "[":                           # a chord
                    j = s.find("]", i)
                    j = n if j < 0 else j
                    inner = s[i + 1:j]
                    first = None
                    for m in re.finditer(r"(\^\^|\^|__|_|=)?([A-Ga-g])([',]*)(\d*/*\d*)", inner):
                        add_note(voice(), m.group(1), m.group(2), m.group(3))
                        if first is None:
                            first = read_dur(m.group(4), 0)[0]
                    mult, i = read_dur(s, j + 1)
                    d = (first if first is not None else F(1)) * mult * unit
                    tuplet = add_dur(voice(), d, tuplet)
                    continue
                if c in "|:":
                    voice().close(meter, ln)
                    i += 1
                    m = re.match(r"\d[\d,\-]*", s[i:])
                    if m:
                        i += m.end()
                else:
                    i += 1
            elif c in "^_=" or c in "ABCDEFGabcdefg":
                m = re.match(r"(\^\^|\^|__|_|=)?([A-Ga-g])([',]*)", s[i:])
                if not m:
                    i += 1
                    continue
                add_note(voice(), m.group(1), m.group(2), m.group(3))
                mult, i = read_dur(s, i + m.end())
                tuplet = add_dur(voice(), mult * unit, tuplet)
            elif c in "zx":
                mult, i = read_dur(s, i + 1)
                tuplet = add_dur(voice(), mult * unit, tuplet)
            elif c in "ZX":
                mult, i = read_dur(s, i + 1)
                v = voice()
                v.close(meter, ln)
                for _ in range(int(mult)):
                    v.bars.append((meter or F(1), meter, ln))
            else:
                i += 1                                 # decorations . ~ H L M O P S T u v, > < etc.
    for v in voices.values():
        v.close(meter, lines[-1][0] if lines else 0)

    title = head.get("T", "") or "(no title)"
    out.append(f"== X:{head.get('X', '?')} {title}  M:{head.get('M', '-')} L:{head.get('L', 'default')} "
               f"K:{head.get('K', '-')}  voices: {len(voices)}")
    problems = 0
    counts = {}
    for v in voices.values():
        bars = v.bars
        counts[v.name] = len(bars)
        bad = []
        for bi, (length, met, ln) in enumerate(bars):
            if met is None:
                continue
            ok = length == met
            note = ""
            if not ok and bi == 0 and length < met:
                note, ok = "pickup", True
            if not ok and bi == len(bars) - 1 and length < met and bars and bars[0][0] < bars[0][1] \
                    and bars[0][0] + length == met:
                note, ok = "closes the pickup", True
            if show_bars or not ok:
                bad.append(f"   V:{v.name} bar {bi + 1} (line {ln}): {fmt(length)} of {fmt(met)}"
                           + ("" if ok else "  WRONG") + (f"  {note}" if note else ""))
            if not ok:
                problems += 1
        rng = ""
        if v.notes:
            lo, hi = min(v.notes), max(v.notes)
            rng = f"range {midi_name(lo)}..{midi_name(hi)} (MIDI {lo}..{hi})"
            off = [x for x in v.notes if x < 21 or x > 108]
            if off:
                rng += f", {len(off)} notes off the 88 keys"
        out.append(f"  V:{v.name}: {len(bars)} bars, {rng}"
                   + (f", {v.upper_tick} uppercase notes with '" if v.upper_tick else ""))
        out.extend(bad[:cap])
        if len(bad) > cap:
            out.append(f"   ... {len(bad) - cap} more")
    if len(set(counts.values())) > 1:
        out.append(f"  voices differ in bar count: {counts}")
        problems += 1
    out.append(f"  {problems} problem(s)")
    return out


def add_note(v, acc, letter, octv):
    m = NOTE_BASE[letter.upper()] + (12 if letter.islower() else 0)
    m += {"^": 1, "^^": 2, "_": -1, "__": -2}.get(acc or "", 0)
    m += 12 * octv.count("'") - 12 * octv.count(",")
    if letter.isupper() and "'" in octv:
        v.upper_tick += 1
    v.notes.append(m)


def add_dur(v, d, tuplet):
    if tuplet:
        d *= tuplet[1]
        tuplet[0] -= 1
        if tuplet[0] <= 0:
            tuplet = None
    v.cur += d
    return tuplet


def fmt(x):
    return str(x) if x.denominator != 1 else str(x.numerator)


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    show = "--bars" in argv
    cap = 40
    if "--max" in argv:
        cap = int(argv[argv.index("--max") + 1])
    files = [a for k, a in enumerate(argv) if not a.startswith("--") and not (k and argv[k - 1] == "--max")]
    for f in files:
        print(f"# {f}")
        try:
            text = open(f, encoding="utf-8", errors="replace").read().splitlines()
        except OSError as e:
            print(f"  cannot read: {e}")
            continue
        tune = []
        for ln, l in enumerate(text, 1):
            if l.startswith("X:") and tune:
                print("\n".join(check_tune(tune, show, cap)))
                tune = []
            if l.startswith("X:") or tune:
                tune.append((ln, l))
        if tune:
            print("\n".join(check_tune(tune, show, cap)))
        elif not any(l.startswith("X:") for l in text):
            print("  no X: line, so no tune found")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
