"""Package Sprite Studio for release.

  python3 -I tools/release.py [VERSION]       (default version: 0.1.0-demo)

Rebuilds the app (tools/build.py), then writes into dist/:

SpriteStudio-<version>-linux.zip
  SpriteStudio            the app (unpacks itself on first run; brings the killbot as an example)
  icon.png                launcher icon
  install-menu-entry.sh   adds an applications-menu entry pointing at the unzipped folder
  README.md               user quick start (release/README.md)

SpriteStudio-<version>-windows.zip   (needs nothing installed on the Windows PC)
  Sprite Studio.bat       starts python\\pythonw.exe -X utf8 app\\start.py (no console window)
  app\\                    server, engine, web page, start.py (tools/winstart.py), the killbot
  python\\                 the official embeddable Python for Windows + Pillow, unpacked
  README.md               user quick start (release/README-windows.md)

Both also carry MANUAL.md (this folder's README.md without the developer sections),
THIRD-PARTY-NOTICES.txt and VERSION. Your own models/ and output/ are not included.
The Windows parts are downloaded once into .downloads/ and checked against pinned SHA-256s.
"""
import hashlib
import io
import os
import re
import subprocess
import sys
import urllib.request
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REL = os.path.join(ROOT, "release")
DL = os.path.join(ROOT, ".downloads")
DEV_SECTIONS = {"Files", "Testing hook", "Planned next"}

PY_VER = "3.14.8"
DOWNLOADS = {   # file -> (url, sha256)
    f"python-{PY_VER}-embed-amd64.zip": (
        f"https://www.python.org/ftp/python/{PY_VER}/python-{PY_VER}-embed-amd64.zip",
        "a93abe456ab01bd96d7a085b3cdb6566b3063f4241360d114142fbdb07f0a310"),
    "pillow-13.0.0-cp314-cp314-win_amd64.whl": (
        "https://files.pythonhosted.org/packages/50/e2/7ad17747517e4c813dca78257d6bb593466f8231baf1384bc98d92745edb/pillow-13.0.0-cp314-cp314-win_amd64.whl",
        "f7cbb7a64e7ec664775195e4f81923bc8a93d9451b963f844e59118f63147a7a"),
}
BAT = ("@echo off\r\n"
       "rem Starts Sprite Studio with the Python bundled in this folder (nothing to install).\r\n"
       'start "" "%~dp0python\\pythonw.exe" -X utf8 "%~dp0app\\start.py" %*\r\n')


def manual():
    """README.md for users: drop the developer sections and the run-from-source notes."""
    text = open(os.path.join(ROOT, "README.md")).read()
    out, skip = [], False
    for block in re.split(r"(?m)^(?=#{2,3} )", text):
        head = block.splitlines()[0].lstrip("#").strip() if block.startswith("#") else ""
        if block.startswith("## "):
            skip = head in DEV_SECTIONS
        if skip or head == "The built app":
            continue
        if head == "Start":
            block = ("## Start\n\nSee README.md for how to start Sprite Studio. **Quit** (top right) "
                     "closes it; it also closes by itself about 3 minutes after you close the tab.\n\n")
        out.append(block)
    return "".join(out).rstrip() + "\n"


def fetch(name):
    """A pinned download, from .downloads/ if it is already there."""
    url, sha = DOWNLOADS[name]
    path = os.path.join(DL, name)
    if not os.path.exists(path):
        os.makedirs(DL, exist_ok=True)
        print(f"downloading {url}")
        data = urllib.request.urlopen(url, timeout=120).read()
        with open(path + ".tmp", "wb") as f:
            f.write(data)
        os.replace(path + ".tmp", path)
    data = open(path, "rb").read()
    if hashlib.sha256(data).hexdigest() != sha:
        raise SystemExit(f"{name}: checksum mismatch; delete {path} and try again")
    return data


class Pack:
    """A zip with everything under one top folder, fixed dates, and Unix modes."""

    def __init__(self, path, top):
        self.path, self.top = path, top
        self.z = zipfile.ZipFile(path + ".tmp", "w", zipfile.ZIP_DEFLATED)

    def put(self, name, data, exe=False):
        info = zipfile.ZipInfo(f"{self.top}/{name}", date_time=(2026, 1, 1, 0, 0, 0))
        info.external_attr = (0o100755 if exe else 0o100644) << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        self.z.writestr(info, data)

    def close(self):
        self.z.close()
        os.replace(self.path + ".tmp", self.path)
        print(f"packaged {os.path.relpath(self.path, ROOT)}  ({os.path.getsize(self.path) // 1024} KB)")


def common(p, version, notices_extra=""):
    p.put("MANUAL.md", manual().encode())
    p.put("VERSION", (version + "\n").encode())
    p.put("THIRD-PARTY-NOTICES.txt", (notices_extra + open(os.path.join(REL, "THIRD-PARTY-NOTICES.txt")).read()).encode())


def linux(version):
    p = Pack(os.path.join(ROOT, "dist", f"SpriteStudio-{version}-linux.zip"), f"SpriteStudio-{version}")
    for name, src, exe in [("SpriteStudio", os.path.join(ROOT, "SpriteStudio"), True),
                           ("icon.png", os.path.join(ROOT, "icon.png"), False),
                           ("install-menu-entry.sh", os.path.join(REL, "install-menu-entry.sh"), True),
                           ("README.md", os.path.join(REL, "README.md"), False)]:
        p.put(name, open(src, "rb").read(), exe)
    common(p, version)
    p.close()


def windows(version):
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import build
    files = build.collect()
    build_id = hashlib.sha256(b"".join(n.encode() + b for n, b in files)).hexdigest()[:12]
    p = Pack(os.path.join(ROOT, "dist", f"SpriteStudio-{version}-windows.zip"), f"SpriteStudio-{version}-windows")
    p.put("Sprite Studio.bat", BAT.encode())
    p.put("README.md", open(os.path.join(REL, "README-windows.md"), "rb").read())
    p.put("app/start.py", open(os.path.join(ROOT, "tools", "winstart.py"), "rb").read())
    p.put("app/BUILD", build_id.encode())
    for n, b in files:
        p.put("app/" + n, b)
    with zipfile.ZipFile(io.BytesIO(fetch(f"python-{PY_VER}-embed-amd64.zip"))) as z:
        for n in z.namelist():
            if not n.endswith("/"):
                p.put("python/" + n, z.read(n))
    with zipfile.ZipFile(io.BytesIO(fetch("pillow-13.0.0-cp314-cp314-win_amd64.whl"))) as z:
        for n in z.namelist():                       # PIL\ next to python.exe is on its path (python314._pth: ".")
            if not n.endswith("/"):
                p.put("python/" + n, z.read(n))
    common(p, version, f"The python\\ folder holds the embeddable Python {PY_VER} for Windows (python\\LICENSE.txt)\n"
                       "and Pillow 13.0.0 (python\\pillow-13.0.0.dist-info\\licenses\\LICENSE).\n\n")
    p.close()


def main():
    version = sys.argv[1] if len(sys.argv) > 1 else "0.1.0-demo"
    if not re.match(r"^[0-9A-Za-z.\-]+$", version):
        raise SystemExit("bad version")
    subprocess.run([sys.executable, "-I", os.path.join(ROOT, "tools", "build.py")], check=True)
    os.makedirs(os.path.join(ROOT, "dist"), exist_ok=True)
    linux(version)
    windows(version)


if __name__ == "__main__":
    main()
