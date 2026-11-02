#!/usr/bin/env python3
"""Install Windows (and GOG Linux .sh) games into Lutris without clicking through its GUI.

  wininstall.py runners                         Wine/Proton builds Lutris has (default GE-Proton8-32)
  wininstall.py install SLUG SETUP.exe [--runner R] [--args "/VERYSILENT ..."]
        silent install into its own prefix ~/Games/SLUG through Lutris's umu-run (as Lutris does);
        default args are Inno Setup's (GOG): /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-
        and the installer's log lands in ~/Games/SLUG/drive_c/inst.log
  wininstall.py gogsh SLUG gog_game.sh          GOG Linux installer (MojoSetup, DOSBox inside) to ~/Games/SLUG
  wininstall.py launch SLUG                     the installed game's primary launch task (goggame-*.info)
  wininstall.py register SLUG "Name" [--year Y] [--runner R]
        write the Lutris config and add or update its row in pga.db (backed up first to
        pga.db.bak-<time>); a Lutris that is open shows it after a restart
  wininstall.py run SLUG                        start the game the way the Lutris entry would (umu-run)

Lutris here is the Flatpak net.lutris.Lutris; its data is in ~/.var/app/net.lutris.Lutris/data/lutris.
Running a Proton build's wine directly fails (wined3d/ddraw not found): always go through umu-run
with PROTONPATH, as Lutris's own installers do.
"""
import glob
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import time

H = os.path.expanduser("~")
L = f"{H}/.var/app/net.lutris.Lutris/data/lutris"
UMU = f"{L}/runtime/umu/umu-run"
RUNNER = "GE-Proton8-32"
INNO = "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP- /LOG=C:\\inst.log"


def opt(a, k, d=None):
    if k in a:
        i = a.index(k)
        v = a[i + 1]
        del a[i:i + 2]
        return v
    return d


def umu(slug, exe, args="", runner=RUNNER, cwd=None, wait=True):
    pre = f"{H}/Games/{slug}"
    os.makedirs(pre, exist_ok=True)
    inner = (f"{'cd ' + repr(cwd) + ' && ' if cwd else ''}export WINEPREFIX={pre} GAMEID=umu-default "
             f"PROTONPATH={L}/runners/wine/{runner} WINEDEBUG=-all; {UMU} {exe!r} {args}")
    cmd = ["flatpak", "run", "--command=bash", "net.lutris.Lutris", "-c", inner]
    if wait:
        return subprocess.run(cmd, capture_output=True, text=True).returncode
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)


def game_dir(slug):
    ds = glob.glob(f"{H}/Games/{slug}/drive_c/GOG Games/*/")
    return ds[0] if ds else None


def launch_task(slug):
    d = game_dir(slug)
    if d:
        for f in glob.glob(d + "goggame-*.info"):
            for t in json.load(open(f)).get("playTasks", []):
                if t.get("isPrimary"):
                    return d, t.get("path", ""), t.get("arguments", ""), t.get("workingDir", "")
    if os.path.exists(f"{H}/Games/{slug}/start.sh"):
        return f"{H}/Games/{slug}/", "start.sh", "", ""
    sys.exit(f"no launch task found for {slug} (look in ~/Games/{slug} and pass the exe by hand)")


def register(slug, name, year=None, runner=RUNNER):
    d, path, args, wd = launch_task(slug)
    base = f"{H}/Games/{slug}"
    if path == "start.sh" and not game_dir(slug):
        r, plat = "linux", "Linux"
        body = f"game:\n  exe: {base}/start.sh\n  working_dir: {base}\n"
    else:
        r, plat = "wine", "Windows"
        rel = os.path.relpath(os.path.join(d, path.replace("\\", "/")), base)
        work = os.path.normpath(os.path.join(d, wd.replace("\\", "/"))) if wd else d.rstrip("/")
        body = (f"game:\n  arch: win64\n  exe: {rel}\n" + (f"  args: {json.dumps(args)}\n" if args else "") +
                f"  prefix: {base}\n  working_dir: {work}\nwine:\n  version: {runner}\n")
    now = int(time.time())
    cfg = f"{slug}-{now}"
    shutil.copy(f"{L}/pga.db", f"{L}/pga.db.bak-{now}")
    open(f"{L}/games/{cfg}.yml", "w").write(body)
    c = sqlite3.connect(f"{L}/pga.db")
    row = c.execute("select id from games where slug=?", (slug,)).fetchone()
    if row:
        c.execute("update games set installed=1, runner=?, platform=?, directory=?, configpath=?, installed_at=?, "
                  "year=coalesce(year,?) where id=?", (r, plat, base, cfg, now, year, row[0]))
    else:
        c.execute("insert into games (name, sortname, slug, platform, runner, directory, installed, installed_at, year, "
                  "configpath, has_custom_banner, has_custom_icon, has_custom_coverart_big, playtime) "
                  "values (?,?,?,?,?,?,1,?,?,?,0,0,0,0.0)", (name, name, slug, plat, r, base, now, year, cfg))
    c.commit()
    print(("updated " if row else "added ") + f"{name} ({r}) -> {cfg}.yml")


def main(a):
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    c = a[0]
    if c == "runners":
        print("\n".join(sorted(os.listdir(f"{L}/runners/wine"))))
    elif c == "install":
        runner, args = opt(a, "--runner", RUNNER), opt(a, "--args", INNO)
        rc = umu(a[1], os.path.abspath(a[2]), args, runner)
        log = f"{H}/Games/{a[1]}/drive_c/inst.log"
        tail = open(log, encoding="utf-8-sig", errors="replace").read().splitlines()[-3:] if os.path.exists(log) else []
        print(f"exit {rc}; installed to {game_dir(a[1])}\n" + "\n".join(tail))
    elif c == "gogsh":
        rc = subprocess.run(["bash", os.path.abspath(a[2]), "--", "--i-agree-to-all-licenses", "--noreadme",
                             "--nooptions", "--noprompt", "--destination", f"{H}/Games/{a[1]}"],
                            capture_output=True).returncode
        print(f"exit {rc}; {H}/Games/{a[1]}")
    elif c == "launch":
        print(launch_task(a[1]))
    elif c == "register":
        year = opt(a, "--year")
        register(a[1], a[2], int(year) if year else None, opt(a, "--runner", RUNNER))
    elif c == "run":
        d, path, args, wd = launch_task(a[1])
        if path == "start.sh":
            subprocess.Popen(["bash", d + "start.sh"], cwd=d, start_new_session=True)
        else:
            umu(a[1], path.replace("\\", "/").split("/")[-1] if not wd else os.path.join(d, path.replace("\\", "/")),
                args, cwd=os.path.normpath(os.path.join(d, wd.replace("\\", "/"))) if wd else d, wait=False)
        print("started")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
