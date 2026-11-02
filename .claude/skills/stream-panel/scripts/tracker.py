#!/usr/bin/env python3
"""Tracker data for the stream panel: what the right-hand column shows besides the live log.

The data is one JSON file, ~/.cache/game-ui/tracker.json (env TRACKER_FILE), that the panel
watches. Anything can write it: this CLI, the Python API below, or hooks (bgplay.py `read`
fills fields from OCR text through the game folder's .claude/game-ui.json "tracker" block).

  tracker.py show                         print the current data
  tracker.py game "Dungeon Crawl Stone Soup" [--mode "Tutorial 5: Gods"]
  tracker.py field HP 24/24 [Place D:3 ...]   set fields (shown in the order first set)
  tracker.py field --del HP                   remove a field
  tracker.py goal add "Reach the exit"        add a goal
  tracker.py goal done 1 | undo 1 | del 1 | clear
  tracker.py note "Went berserk at full HP"   recent-events list (last 6 shown)
  tracker.py status "fighting 3 gnolls"       one-line status under the title
  tracker.py start                            restart the session timer (also clears notes)
  tracker.py clear                            empty everything

Hook format in .claude/game-ui.json (applied to every bgplay `read` of that region):
  "tracker": {"game": "Dungeon Crawl Stone Soup",
              "fields": {"HP": ["hp", "Health:\\\\s*(\\\\S+)"], "Place": ["stats", "Place:\\\\s*(\\\\S+)"]}}
Each field = [region name, regex with one group]; no match leaves the old value.

Python:  import tracker as T; T.update(fields={"HP": "24/24"}, note="Level 3")
"""
import json
import os
import re
import sys
import time

FILE = os.environ.get("TRACKER_FILE", os.path.expanduser("~/.cache/game-ui/tracker.json"))
EMPTY = {"game": "", "mode": "", "status": "", "fields": {}, "goals": [], "notes": [], "started": 0}


def load():
    try:
        d = json.load(open(FILE))
    except (OSError, ValueError):
        d = {}
    out = dict(EMPTY, **d)
    out["fields"] = dict(out.get("fields") or {})
    if not out["started"]:
        out["started"] = time.time()
    return out


def save(d):
    os.makedirs(os.path.dirname(FILE), exist_ok=True)
    tmp = FILE + ".tmp"
    json.dump(d, open(tmp, "w"), indent=1)
    os.replace(tmp, FILE)           # atomic: the panel never reads half a file


def update(game=None, mode=None, status=None, fields=None, note=None, goal=None):
    d = load()
    if game is not None:
        d["game"] = game
    if mode is not None:
        d["mode"] = mode
    if status is not None:
        d["status"] = status
    if fields:
        for k, v in fields.items():
            if v is None:
                d["fields"].pop(k, None)
            else:
                d["fields"][k] = str(v)
    if note:
        d["notes"] = (d["notes"] + [{"t": time.time(), "text": note}])[-20:]
    if goal:
        d["goals"].append({"text": goal, "done": False})
    save(d)
    return d


def apply_hooks(hooks, region, text):
    """Fill fields from OCR text of one region (bgplay calls this)."""
    if not hooks:
        return
    found = {}
    for name, spec in (hooks.get("fields") or {}).items():
        reg, pat = spec[0], spec[1]
        if reg == region:
            m = re.search(pat, text)
            if m:
                found[name] = m.group(1)
    if found or hooks.get("game"):
        d = load()
        changed = False
        if hooks.get("game") and d["game"] != hooks["game"]:
            d["game"], changed = hooks["game"], True
        for k, v in found.items():
            if d["fields"].get(k) != v:
                d["fields"][k], changed = v, True
        if changed:
            save(d)


def main(a):
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    c, rest = a[0], a[1:]
    if c == "show":
        print(json.dumps(load(), indent=1))
    elif c == "game":
        mode = None
        if "--mode" in rest:
            i = rest.index("--mode")
            mode = rest[i + 1]
            del rest[i:i + 2]
        update(game=" ".join(rest), mode=mode)
    elif c == "mode":
        update(mode=" ".join(rest))
    elif c == "status":
        update(status=" ".join(rest))
    elif c == "field":
        if rest and rest[0] == "--del":
            update(fields={k: None for k in rest[1:]})
        else:
            if len(rest) % 2:
                sys.exit("field takes NAME VALUE pairs")
            update(fields=dict(zip(rest[::2], rest[1::2])))
    elif c == "goal":
        d = load()
        sub = rest[0] if rest else ""
        if sub == "add":
            d["goals"].append({"text": " ".join(rest[1:]), "done": False})
        elif sub in ("done", "undo", "del"):
            i = int(rest[1]) - 1
            if sub == "del":
                d["goals"].pop(i)
            else:
                d["goals"][i]["done"] = sub == "done"
        elif sub == "clear":
            d["goals"] = []
        else:
            sys.exit("goal add TEXT | done N | undo N | del N | clear")
        save(d)
    elif c == "note":
        update(note=" ".join(rest))
    elif c == "start":
        d = load()
        d["started"], d["notes"] = time.time(), []
        save(d)
    elif c == "clear":
        save(dict(EMPTY, started=time.time()))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
