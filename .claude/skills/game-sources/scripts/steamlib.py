#!/usr/bin/env python3
"""The user's Steam library from the local Steam client files (read only).

  steamlib.py list [--min-hours H] [--type game] [--sort hours|name|recent]   played/owned apps
  steamlib.py installed                                                      installed apps

Names and types come from the client's app cache (appcache/appinfo.vdf, binary VDF v27-29);
playtime and last-played from userdata/<id>/config/localconfig.vdf. Nothing is written.
"""
import os, re, struct, sys, signal, time
signal.signal(signal.SIGPIPE, signal.SIG_DFL)
STEAM = os.path.expanduser("~/.local/share/Steam")


def read_kv(buf, pos, strings):
    """Binary VDF map starting at pos -> (dict, new pos)."""
    out = {}
    while True:
        t = buf[pos]; pos += 1
        if t == 8:
            return out, pos
        if strings is not None:
            key = strings[struct.unpack_from("<I", buf, pos)[0]]; pos += 4
        else:
            e = buf.index(b"\0", pos); key = buf[pos:e].decode("utf-8", "replace"); pos = e + 1
        if t == 0:
            out[key], pos = read_kv(buf, pos, strings)
        elif t == 1:
            e = buf.index(b"\0", pos); out[key] = buf[pos:e].decode("utf-8", "replace"); pos = e + 1
        elif t in (2, 4, 6):
            out[key] = struct.unpack_from("<i", buf, pos)[0]; pos += 4
        elif t == 3:
            out[key] = struct.unpack_from("<f", buf, pos)[0]; pos += 4
        elif t in (7, 10):
            out[key] = struct.unpack_from("<Q", buf, pos)[0]; pos += 8
        else:
            raise ValueError(f"unknown VDF type {t} at {pos}")


def appinfo():
    buf = open(os.path.join(STEAM, "appcache", "appinfo.vdf"), "rb").read()
    magic, _ = struct.unpack_from("<II", buf, 0)
    ver = magic & 0xFF
    pos, strings = 8, None
    if ver >= 0x29:
        off = struct.unpack_from("<q", buf, 8)[0]; pos = 16
        n = struct.unpack_from("<I", buf, off)[0]; p = off + 4; strings = []
        for _ in range(n):
            e = buf.index(b"\0", p); strings.append(buf[p:e].decode("utf-8", "replace")); p = e + 1
    apps = {}
    while True:
        appid = struct.unpack_from("<I", buf, pos)[0]
        if appid == 0:
            break
        size = struct.unpack_from("<I", buf, pos + 4)[0]
        start = pos + 8 + 4 + 4 + 8 + 20 + 4 + (20 if ver >= 0x28 else 0)
        try:
            kv, _ = read_kv(buf, start, strings)
            common = kv.get("appinfo", kv).get("common", {})
            apps[appid] = (common.get("name", "?"), str(common.get("type", "?")).lower())
        except Exception:
            pass
        pos += 8 + size
    return apps


def localconfig():
    """{appid: (minutes, last played epoch)} from every user's localconfig.vdf (text VDF)."""
    res = {}
    for u in os.listdir(os.path.join(STEAM, "userdata")):
        f = os.path.join(STEAM, "userdata", u, "config", "localconfig.vdf")
        if not os.path.isfile(f):
            continue
        text = open(f, encoding="utf-8", errors="replace").read()
        m = re.search(r'"apps"\s*\{', text[text.find('"Steam"'):]) if '"Steam"' in text else None
        for am in re.finditer(r'\n\t*"(\d+)"\s*\n\t*\{([^{}]*)\}', text):
            body = am.group(2)
            if "Playtime" not in body and "LastPlayed" not in body:
                continue
            pt = re.search(r'"Playtime"\s*"(\d+)"', body); lp = re.search(r'"LastPlayed"\s*"(\d+)"', body)
            res[int(am.group(1))] = (int(pt.group(1)) if pt else 0, int(lp.group(1)) if lp else 0)
    return res


def installed():
    out = []
    for f in os.listdir(os.path.join(STEAM, "steamapps")):
        if f.startswith("appmanifest_"):
            t = open(os.path.join(STEAM, "steamapps", f), encoding="utf-8", errors="replace").read()
            out.append((int(re.search(r'"appid"\s*"(\d+)"', t).group(1)), re.search(r'"name"\s*"([^"]*)"', t).group(1)))
    return sorted(out, key=lambda x: x[1].lower())


def main(a):
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    if a[0] == "installed":
        for i, n in installed():
            print(f"{i:>8}  {n}")
        return
    minh = float(a[a.index("--min-hours") + 1]) if "--min-hours" in a else 0
    typ = a[a.index("--type") + 1] if "--type" in a else None
    sort = a[a.index("--sort") + 1] if "--sort" in a else "hours"
    info, lc = appinfo(), localconfig()
    rows = []
    for i, (mins, last) in lc.items():
        name, t = info.get(i, (f"(app {i})", "?"))
        if typ and t != typ:
            continue
        if mins / 60 < minh:
            continue
        rows.append((i, name, t, mins / 60, last))
    key = {"hours": lambda r: -r[3], "name": lambda r: r[1].lower(), "recent": lambda r: -r[4]}[sort]
    for i, n, t, h, last in sorted(rows, key=key):
        print(f"{i:>8}  {h:7.1f}h  {time.strftime('%Y-%m-%d', time.localtime(last)) if last else '----------'}  {t:<6} {n}")
    print(f"{len(rows)} apps")


if __name__ == "__main__":
    main(sys.argv[1:])
