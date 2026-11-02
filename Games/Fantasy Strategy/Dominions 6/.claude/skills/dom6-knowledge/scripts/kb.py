"""Claude's Dominions 6 knowledge base: what was learned by reading the game itself (nation info
screens, the unit screen, icons and magic symbols, how screens behave), kept as markdown topic
files so it can be read, searched and added to.

  python3 -I kb.py topics                       every topic file with its title and size
  python3 -I kb.py show TOPIC                   print a topic (ui/unit-screen, nations/OVERVIEW...)
  python3 -I kb.py search TEXT [TEXT...]        lines in any topic that have all the words
  python3 -I kb.py add TOPIC "SECTION" "FACT" [--source TEXT]
                                                add a fact under a section heading of a topic
                                                (creates both when missing; dated, with its source)
  python3 -I kb.py new TOPIC "TITLE" ["WHAT IT COVERS"]   start a topic file

TOPIC is a path under the knowledge folder without .md: ui/unit-screen, ui/icons, nations/MA/ulm.
"""
import datetime
import os
import re
import sys

KB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # dom6-knowledge/


def path(topic):
    topic = topic[:-3] if topic.endswith(".md") else topic
    p = os.path.normpath(os.path.join(KB, topic + ".md"))
    if not p.startswith(KB + os.sep) or "/scripts/" in p:
        sys.exit(f"bad topic {topic!r}")
    return p


def topics():
    out = []
    for root, dirs, files in os.walk(KB):
        dirs[:] = sorted(d for d in dirs if d not in ("scripts", "__pycache__", "img"))
        for f in sorted(files):
            if f.endswith(".md") and f != "SKILL.md":
                p = os.path.join(root, f)
                with open(p, encoding="utf-8") as fh:
                    first = fh.readline().strip().lstrip("# ")
                out.append((os.path.relpath(p, KB)[:-3], first, os.path.getsize(p)))
    return out


def new(topic, title, about=""):
    p = path(topic)
    if os.path.exists(p):
        sys.exit(f"{topic} exists")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{about + chr(10) + chr(10) if about else ''}")
    return p


def add(topic, section, fact, source=""):
    """Append FACT as a bullet under '## SECTION' of TOPIC (made if missing)."""
    p = path(topic)
    if not os.path.exists(p):
        new(topic, topic.split("/")[-1].replace("-", " ").capitalize())
    with open(p, encoding="utf-8") as f:
        text = f.read()
    stamp = datetime.date.today().isoformat()
    line = f"- {fact}" + (f" *({source}, {stamp})*" if source else f" *({stamp})*") + "\n"
    head = f"## {section}"
    m = re.search(rf"^{re.escape(head)}\s*$", text, re.M)
    if not m:
        text = text.rstrip("\n") + f"\n\n{head}\n\n{line}"
    else:
        nxt = re.search(r"^## ", text[m.end():], re.M)
        end = m.end() + nxt.start() if nxt else len(text)
        body = text[:end].rstrip("\n") + "\n" + line
        text = body + ("\n" + text[end:] if nxt else "")
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    return p


def search(words):
    ws = [w.lower() for w in words]
    for topic, _, _ in topics():
        with open(path(topic), encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                low = line.lower()
                if all(w in low for w in ws):
                    print(f"{topic}:{n}: {line.rstrip()}")


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd, a = argv[0], argv[1:]
    if cmd == "topics":
        for t, title, size in topics():
            print(f"{t:40} {size:>7}  {title}")
    elif cmd == "show":
        with open(path(a[0]), encoding="utf-8") as f:
            print(f.read())
    elif cmd == "search":
        search(a)
    elif cmd == "new":
        print(new(a[0], a[1], a[2] if len(a) > 2 else ""))
    elif cmd == "add":
        src = ""
        if "--source" in a:
            i = a.index("--source")
            src = a[i + 1]
            a = a[:i] + a[i + 2:]
        print(add(a[0], a[1], a[2], src))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
