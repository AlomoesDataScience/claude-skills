#!/usr/bin/env python3
"""Turn a Discord data package ("Request my data", Settings > Data & Privacy) into readable logs and a
searchable database. Reads the zip directly (nothing is extracted or run). The package holds YOUR OWN
messages only (servers, DMs, group DMs) - not other people's replies.

  python3 -I discordlogs.py import PACKAGE.zip|FOLDER [--out DIR]
        builds DIR/discord.sqlite (tables channels, messages + full-text search) and DIR/logs/<server>/<channel>.md
        (default DIR: ~/Documents/discord-logs). Re-importing a newer package replaces the old data.
  python3 -I discordlogs.py channels [--out DIR]              every channel: kind, server, name, message count, dates
  python3 -I discordlogs.py search WORDS [--channel X] [--server X] [--from 2025-01-01] [--to 2025-12-31]
                                         [--limit 50] [--out DIR]
        full-text search (FTS5 syntax: "exact phrase", word*, a OR b, a NOT b), newest first, with channel and date
  python3 -I discordlogs.py stats [--out DIR]                  messages per year, per server, top channels
  python3 -I discordlogs.py sql "SELECT ..." [--out DIR]

Package layouts handled: Messages/index.json + Messages/c<id>/ (or <id>/) with channel.json and
messages.json (new) or messages.csv (old); attachments are kept as links.
"""
import csv
import io
import json
import os
import re
import sqlite3
import sys
import zipfile

a = sys.argv[1:]


def opt(name, default=None):
    return a[a.index(name) + 1] if name in a else default


OUT = os.path.expanduser(opt("--out", "~/Documents/discord-logs"))
DB = os.path.join(OUT, "discord.sqlite")


class Package:
    """the same reading interface for a zip and an extracted folder"""

    def __init__(self, src):
        self.zip = zipfile.ZipFile(src) if zipfile.is_zipfile(src) else None
        self.root = None if self.zip else src
        names = self.zip.namelist() if self.zip else [
            os.path.relpath(os.path.join(d, f), src).replace(os.sep, "/") for d, _, fs in os.walk(src) for f in fs]
        self.names = names
        hits = [n for n in names if re.search(r"(^|/)messages/index\.json$", n, re.I)]
        self.base = hits[0][:-len("index.json")] if hits else None

    def read(self, name):
        if self.zip:
            return self.zip.read(name).decode("utf-8", "replace")
        return open(os.path.join(self.root, name), encoding="utf-8", errors="replace").read()


def channel_kind(ch):
    t = str(ch.get("type", ""))
    return {"0": "server", "GUILD_TEXT": "server", "1": "dm", "DM": "dm", "3": "group", "GROUP_DM": "group",
            "11": "thread", "PUBLIC_THREAD": "thread", "12": "thread", "PRIVATE_THREAD": "thread",
            "5": "server", "GUILD_ANNOUNCEMENT": "server", "2": "voice", "GUILD_VOICE": "voice"}.get(t, t or "?")


def load_messages(pkg, folder):
    files = {n.rsplit("/", 1)[-1].lower(): n for n in pkg.names if n.startswith(folder) and n.count("/") == folder.count("/")}
    out = []
    if "messages.json" in files:
        for m in json.loads(pkg.read(files["messages.json"]) or "[]"):
            out.append((str(m.get("ID") or m.get("id")), m.get("Timestamp") or m.get("timestamp") or "",
                        m.get("Contents") or m.get("content") or "", m.get("Attachments") or m.get("attachments") or ""))
    elif "messages.csv" in files:
        for m in csv.DictReader(io.StringIO(pkg.read(files["messages.csv"]))):
            out.append((m.get("ID", ""), m.get("Timestamp", ""), m.get("Contents", ""), m.get("Attachments", "")))
    return out, files


def safe(s):
    return re.sub(r"[^\w .,()&'-]+", "_", s or "unnamed").strip(" .")[:80] or "unnamed"


def do_import(src):
    pkg = Package(src)
    if pkg.base is None:
        sys.exit("no Messages/index.json in this package - is it a Discord data package?")
    index = json.loads(pkg.read(pkg.base + "index.json"))
    folders = sorted({n[:n.index("/", len(pkg.base)) + 1] for n in pkg.names
                      if n.startswith(pkg.base) and "/" in n[len(pkg.base):]})
    os.makedirs(OUT, exist_ok=True)
    if os.path.exists(DB):
        os.remove(DB)
    con = sqlite3.connect(DB)
    con.executescript("""
        CREATE TABLE channels (id TEXT PRIMARY KEY, kind TEXT, server TEXT, name TEXT, recipients TEXT);
        CREATE TABLE messages (id TEXT, channel TEXT, ts TEXT, content TEXT, attachments TEXT);
        CREATE VIRTUAL TABLE fts USING fts5(content, content='messages', content_rowid='rowid');""")
    total = 0
    for folder in folders:
        msgs, files = load_messages(pkg, folder)
        ch = json.loads(pkg.read(files["channel.json"])) if "channel.json" in files else {}
        cid = str(ch.get("id") or re.sub(r"\D", "", folder.rstrip("/").rsplit("/", 1)[-1]))
        kind = channel_kind(ch)
        server = (ch.get("guild") or {}).get("name", "") if isinstance(ch.get("guild"), dict) else ""
        label = index.get(cid) or ch.get("name") or ""
        name = ch.get("name") or label or cid
        if kind == "dm" and label:
            name = re.sub(r"^Direct Message with ", "", label)
        recips = ",".join(map(str, ch.get("recipients", []) or []))
        con.execute("INSERT OR REPLACE INTO channels VALUES (?,?,?,?,?)", (cid, kind, server, name, recips))
        con.executemany("INSERT INTO messages VALUES (?,?,?,?,?)", [(m[0], cid, m[1], m[2], m[3]) for m in msgs])
        total += len(msgs)
        if msgs:
            where = os.path.join(OUT, "logs", safe(server) if server else {"dm": "DMs", "group": "Group DMs"}.get(kind, safe(kind)))
            os.makedirs(where, exist_ok=True)
            with open(os.path.join(where, safe(name) + ".md"), "w", encoding="utf-8") as f:
                f.write(f"# {name}\n{kind}{' - ' + server if server else ''} | {len(msgs)} of my messages | "
                        f"channel {cid}\n\n")
                day = None
                for _, ts, text, att in sorted(msgs, key=lambda m: m[1]):
                    if ts[:10] != day:
                        day = ts[:10]
                        f.write(f"\n## {day}\n")
                    f.write(f"- {ts[11:16]} {text}" + (f" [attachment: {att}]" if att else "") + "\n")
    con.execute("INSERT INTO fts(fts) VALUES('rebuild')")
    con.commit()
    print(f"{len(folders)} channels, {total} messages -> {DB} and {os.path.join(OUT, 'logs')}/")


def db():
    if not os.path.exists(DB):
        sys.exit(f"no database at {DB} - run: discordlogs.py import PACKAGE.zip")
    return sqlite3.connect(DB)


def table(cur):
    names = [c[0] for c in cur.description]
    rows = cur.fetchall()
    print("| " + " | ".join(names) + " |\n|" + "---|" * len(names))
    for r in rows:
        print("| " + " | ".join(str(x if x is not None else "").replace("|", "/").replace("\n", " ")[:160] for x in r) + " |")
    print(f"\n{len(rows)} rows")


def main():
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    cmd = a[0]
    if cmd == "import" and len(a) > 1:
        do_import(a[1])
    elif cmd == "channels":
        table(db().execute("""SELECT c.kind, c.server, c.name, count(m.id) msgs, min(substr(m.ts,1,10)) first,
                              max(substr(m.ts,1,10)) last FROM channels c LEFT JOIN messages m ON m.channel=c.id
                              GROUP BY c.id ORDER BY msgs DESC"""))
    elif cmd == "search" and len(a) > 1:
        words = " ".join(x for i, x in enumerate(a[1:], 1)
                         if not x.startswith("--") and not a[i - 1].startswith("--"))
        sql = ("SELECT substr(m.ts,1,16) time, c.server, c.name channel, m.content FROM fts JOIN messages m "
               "ON m.rowid=fts.rowid JOIN channels c ON c.id=m.channel WHERE fts MATCH ?")
        p = [words]
        for flag, col in (("--channel", "c.name"), ("--server", "c.server")):
            if opt(flag):
                sql += f" AND {col} LIKE ?"
                p.append(f"%{opt(flag)}%")
        if opt("--from"):
            sql += " AND m.ts >= ?"
            p.append(opt("--from"))
        if opt("--to"):
            sql += " AND m.ts <= ?"
            p.append(opt("--to") + "~")
        sql += " ORDER BY m.ts DESC LIMIT ?"
        p.append(int(opt("--limit", 50)))
        table(db().execute(sql, p))
    elif cmd == "stats":
        con = db()
        table(con.execute("SELECT substr(ts,1,4) year, count(*) msgs FROM messages GROUP BY year ORDER BY year"))
        table(con.execute("""SELECT CASE WHEN c.server='' THEN '('||c.kind||')' ELSE c.server END place, count(*) msgs
                             FROM messages m JOIN channels c ON c.id=m.channel GROUP BY place ORDER BY msgs DESC LIMIT 20"""))
    elif cmd == "sql" and len(a) > 1:
        table(db().execute(a[1]))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
