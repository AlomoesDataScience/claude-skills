#!/usr/bin/env python3
"""One careful DCSS step on the bgplay screen: auto-explore once, fight what that turns up,
and stop for Claude's judgement on anything that isn't routine.

  crawlstep.py [N] [--hp 0.7] [--known "rat,jackal,..."]

Repeats up to N steps (default 1). Each step: `o`, read the messages; if a monster is in the way,
`Tab` one swing at a time with a read after each, until "No target in view". It STOPS and prints
why when: health under --hp of max, a monster not in the known list, more than two monsters at
once, a gnoll (packs with reach and nets: corridor first), a web or net, an item or feature was found ("Found", "You see here", "Things that are here"), a prompt
(--more--, "?", level-up), "Done exploring", or anything unusual ("malevolent", "LOW HITPOINT").
One `o` per step and a read after every action (the user's rule after the missed cloak).
Run from the Crawl folder so bgplay finds the game-ui.json regions (and the tracker hook).
"""
import os
import re
import subprocess
import sys

BG = os.path.expanduser("~/Desktop/AI Development/.claude/skills/game-ui/scripts/bgplay.py")
KNOWN = {"rat", "jackal", "bat", "goblin", "kobold", "frilled lizard", "ball python", "adder",
         "endoplasm", "quokka", "dart slug", "hobgoblin", "newt", "giant cockroach", "leopard gecko",
         "toad", "hound", "worm", "orc", "ooze", "centipede", "wolf spider"}
STOP_WORDS = ("Found", "You see here", "Things that are here", "--more--", "Done exploring",
              "malevolent", "LOW HITPOINT", "Increase (S)", "level", "?", "There is an entrance",
              "You fall", "trap", "shaft", "altar", "shop", "Trog", "feel")


def bg(*steps):
    return subprocess.run([sys.executable, "-I", BG, "seq", *steps], capture_output=True, text=True).stdout


def hp_of(out):
    m = re.search(r"Health:\s*(-?\d+)/(\d+)", out)
    return (int(m.group(1)), int(m.group(2))) if m else (None, None)


def new_lines(before, after):
    """Message lines in `after` that weren't at the end of `before` (the log scrolls up)."""
    a = [x.strip("_ ").strip() for x in after.split("[hp]")[0].splitlines() if x.strip()][1:]
    b = [x.strip("_ ").strip() for x in before.split("[hp]")[0].splitlines() if x.strip()][1:]
    for k in range(len(b), -1, -1):
        if a[:k] == b[len(b) - k:]:
            return a[k:]
    return a


ROUTINE = ("corpse", "gold piece", "staircase", "escape hatch", "door", "accepts your kill",
           "skill increases", "Trog accepts")


def routine(line):
    """Lines that match a stop word but need no decision (corpses, gold, stairs, doors)."""
    if any(r in line for r in ROUTINE) and not re.search(r"Found (an?|\d+) (?!.*(corpse|gold|staircase|hatch|door))", line):
        return True
    return False


def encountered(lines):
    names = []
    for ln in lines:
        for m in re.finditer(r"You encounter ([^.!]+)", ln):
            for part in re.split(r",| and ", m.group(1)):
                p = re.sub(r"^(an?|the|\d+)\s+", "", part.strip()).split(" It is")[0].strip()
                p = re.sub(r"s$", "", p) if re.match(r"^\d", part.strip()) else p
                if p:
                    names.append(p)
    return names


def main(a):
    n = int(a[0]) if a and a[0].isdigit() else 1
    limit = float(a[a.index("--hp") + 1]) if "--hp" in a else 0.7
    known = KNOWN | ({x.strip() for x in a[a.index("--known") + 1].split(",")} if "--known" in a else set())
    last = bg("read msg hp")
    for step in range(n):
        out = bg("key o", "wait 2200", "read msg hp")
        lines = new_lines(last, out)
        last = out
        print(f"--- step {step + 1}: " + " | ".join(lines))
        foes = encountered(lines)
        stop = [w for w in STOP_WORDS if any(w in ln and not routine(ln) for ln in lines)]
        unknown = [f for f in foes if not any(k in f for k in known)]
        if unknown:
            return print(f"STOP: unknown monster(s) {unknown}")
        if len(foes) > 2:
            return print(f"STOP: {len(foes)} monsters at once {foes}")
        if stop:
            return print(f"STOP: {stop}")
        if foes or any("nearby" in ln or "There are monsters" in ln for ln in lines):
            for _ in range(20):
                out = bg("key Tab", "wait 330", "read msg hp")
                fl = new_lines(last, out)
                last = out
                h, mx = hp_of(out)
                print("    " + " | ".join(fl) + f"   [HP {h}/{mx}]")
                if h is not None and h < limit * mx:
                    return print(f"STOP: HP {h}/{mx}")
                more = encountered(fl)
                if [f for f in more if not any(k in f for k in known)]:
                    return print(f"STOP: new monster {more}")
                if any(w in ln for ln in fl for w in ("--more--", "Increase (S)", "LOW HITPOINT", "too injured",
                                                         "caught in a web", "held in a net", "gnoll")):
                    return print("STOP: prompt or danger")
                if any("No target in view" in ln for ln in fl):
                    break
        h, mx = hp_of(last)
        if h is not None and h < mx:
            last = bg("key 5", "wait 3500", "read msg hp")
    h, mx = hp_of(last)
    print(f"done {n} step(s), HP {h}/{mx}")


if __name__ == "__main__":
    main(sys.argv[1:])
