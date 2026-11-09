#!/usr/bin/env python3
"""Dependency files for the skills: DEPENDENCIES-linux.md and DEPENDENCIES-windows.md.

  deps.py [TREE] [--out DIR]   scan TREE's scripts (default: the workspace) for each known dependency, fill
                               in which skills use it, write both files to DIR (default TREE). Unknown
                               third-party Python imports are reported so the table can be extended.
export.py runs this on the exported copy, so the files in the shared repository always match the code.
The table below is the hand-kept part: how to install each thing on Linux, and the recommended Windows
equivalent with how far the skills work there. Pure standard library."""
import collections, os, re, sys

# key: (category, how to detect in code (regex), Linux install, Windows equivalent, Windows install, Windows note)
T = {
    "Claude Code": ("core", None, "`curl -fsSL https://claude.ai/install.sh | bash` (docs.claude.com)",
                    "Claude Code for Windows", "PowerShell: `irm https://claude.ai/install.ps1 | iex` (needs Git for Windows)",
                    "native, or inside WSL2"),
    "Python 3.10+": ("core", None, "`sudo apt install python3`", "Python 3.12", "`winget install Python.Python.3.12`",
                     "scripts are run as `python -I script.py` instead of `python3 -I`"),
    "Pillow (PIL)": ("python", r"^\s*(from|import) PIL\b", "`sudo apt install python3-pil` or `pip install pillow`",
                     "Pillow", "`pip install pillow`", "ImageGrab works natively on Windows"),
    "NumPy": ("python", r"^\s*(from|import) numpy\b", "`sudo apt install python3-numpy`", "NumPy", "`pip install numpy`", ""),
    "OpenCV": ("python", r"^\s*(from|import) cv2\b", "`sudo apt install python3-opencv`", "OpenCV",
               "`pip install opencv-python`", ""),
    "faster-whisper": ("python", r"^\s*(from|import) faster_whisper\b", "`pip install faster-whisper` (optional: speech to text)",
                       "faster-whisper", "`pip install faster-whisper`", "optional"),
    "PyYAML": ("python", r"^\s*(from|import) yaml\b|import yaml", "`sudo apt install python3-yaml` (optional: verify.py YAML check)",
               "PyYAML", "`pip install pyyaml`", "optional"),
    "git": ("core", r"[\"']git[\"']", "`sudo apt install git`", "Git for Windows", "`winget install Git.Git`",
            "also brings bash and `file`"),
    "curl": ("documents", r"[\"']curl[\"']", "`sudo apt install curl`", "curl", "built into Windows 10/11 (`curl.exe`)", ""),
    "file": ("documents", r"\[\s*[\"']file[\"']\s*,", "`sudo apt install file`", "file (Git for Windows)",
             "comes with Git for Windows (`usr/bin/file.exe`)", ""),
    "poppler-utils (pdftotext, pdfinfo, pdftoppm, pdftohtml)": (
        "documents", r"pdftotext|pdfinfo|pdftoppm|pdftohtml", "`sudo apt install poppler-utils`",
        "Poppler for Windows", "`scoop install poppler` (or the poppler-windows release zip, bin/ on PATH)", ""),
    "LibreOffice (soffice)": ("documents", r"soffice", "`sudo apt install libreoffice-core libreoffice-writer`",
                              "LibreOffice", "`winget install TheDocumentFoundation.LibreOffice`", "add `program/` to PATH"),
    "7-Zip": ("documents", r"[\"']7z[\"']|\b7z x\b", "`sudo apt install p7zip-full`", "7-Zip", "`winget install 7zip.7zip`", ""),
    "Tesseract OCR 5": ("screen", r"tesseract", "`sudo apt install tesseract-ocr` (+ `tesseract-ocr-jpn tesseract-ocr-jpn-vert`) "
                        "or the NormCap flatpak, which bundles it", "Tesseract (UB Mannheim build)",
                        "`winget install UB-Mannheim.TesseractOCR` (tick extra languages in the installer)", ""),
    "xdotool": ("screen", r"xdotool", "`sudo apt install xdotool`", "AutoHotkey v2 or pywinauto",
                "`winget install AutoHotkey.AutoHotkey` / `pip install pywinauto`", "game-ui's input layer must be ported"),
    "wmctrl, xwininfo, xprop": ("screen", r"wmctrl|xwininfo|xprop", "`sudo apt install wmctrl x11-utils`",
                                "pywinauto / pygetwindow", "`pip install pywinauto pygetwindow`", "window finding must be ported"),
    "xinput": ("screen", r"[\"']xinput[\"']", "`sudo apt install xinput`", "AutoHotkey `BlockInput`",
               "with AutoHotkey (needs admin)", "locking the user's input (hand-back)"),
    "Xephyr (bgplay virtual screen)": ("screen", r"Xephyr", "`sudo apt install xserver-xephyr`",
                                       "Windows Sandbox or a Hyper-V VM", "Windows Pro: `Enable-WindowsOptionalFeature -Online -FeatureName Containers-DisposableClientVM`",
                                       "no direct equivalent; play on the main desktop instead"),
    "VirtualGL (vglrun)": ("screen", r"vglrun", "VirtualGL .deb from virtualgl.org", "not needed", "-",
                           "games draw on the GPU directly"),
    "OBS Studio (WebSocket on)": ("media", r"obsws|:4455|\b4455\b", "`flatpak install flathub com.obsproject.Studio`", "OBS Studio",
                                  "`winget install OBSProject.OBSStudio`", "WebSocket server built in (Tools > WebSocket)"),
    "FFmpeg (ffmpeg, ffprobe)": ("media", r"[\"']ffmpeg[\"']|[\"']ffprobe[\"']", "`sudo apt install ffmpeg`", "FFmpeg",
                                 "`winget install Gyan.FFmpeg`", ""),
    "yt-dlp": ("media", r"yt-dlp|yt_dlp", "`pip install yt-dlp` (or `sudo apt install yt-dlp`)", "yt-dlp",
               "`winget install yt-dlp.yt-dlp`", ""),
    "gifsicle": ("media", r"gifsicle", "`sudo apt install gifsicle`", "gifsicle", "`scoop install gifsicle`", "optional"),
    "Flatpak": ("games", r"[\"']flatpak[\"']", "`sudo apt install flatpak`", "not needed", "-", "use the Windows installers"),
    "Steam": ("games", r"[\"']steam[\"']", "`sudo apt install steam-installer`", "Steam", "`winget install Valve.Steam`", ""),
    "Lutris + umu-run + Wine/Proton": ("games", r"umu-run|lutris|[\"']wine[\"']", "`sudo apt install lutris` (umu and Proton come with it)",
                                       "GOG Galaxy or Playnite", "`winget install GOG.Galaxy` / `winget install Playnite.Playnite`",
                                       "Windows games run natively; install-windows-games is Linux-only"),
    "Firefox": ("games", r"firefox", "`sudo apt install firefox`", "Firefox", "`winget install Mozilla.Firefox`",
                "dom6-inspector / dom6-modinspector headless runs"),
    ".NET SDK 8+": ("games", r"\bdotnet\b", "`sudo apt install dotnet-sdk-8.0`", ".NET SDK 8", "`winget install Microsoft.DotNet.SDK.8`",
                    "C# projects"),
    "zenity, notify-send": ("games", r"zenity|notify-send", "`sudo apt install zenity libnotify-bin` (Sprite Studio launcher, optional)",
                            "not needed", "-", "the Windows build of Sprite Studio has its own launcher"),
}
CATS = [("core", "Core (everything)"), ("python", "Python packages"), ("documents", "Manuals and documents"),
        ("screen", "Seeing and driving the screen (X11)"), ("media", "Recording and video"),
        ("games", "Games, installers, per-game tools")]
CODE = (".py", ".sh", ".js")


def owner(path):
    m = re.search(r"/skills/([^/]+)/", path) or re.search(r"/(spritestudio|mapgen)/", path)
    return m.group(1) if m else None


def scan(tree):
    used, texts, unknown = collections.defaultdict(set), [], collections.defaultdict(set)
    local = set()
    for d, ds, fs in os.walk(tree):
        ds[:] = [x for x in ds if x not in (".git", "__pycache__", "node_modules", "vendor", "Archive")]
        for f in fs:
            if f.endswith(CODE) and owner(os.path.join(d, f)):
                local.add(f.rsplit(".", 1)[0])
                texts.append((owner(os.path.join(d, f)), open(os.path.join(d, f), encoding="utf-8", errors="replace").read(), f))
    std = set(sys.stdlib_module_names)
    for sk, t, f in texts:
        for k, v in T.items():
            if v[1] and re.search(v[1], t, re.M):
                used[k].add(sk)
        if f.endswith(".py"):
            for m in re.finditer(r"^\s*(?:import\s+([A-Za-z_]\w*)\s*(?:$|,|\s+as\b)|from\s+([A-Za-z_]\w*)(?:\.\w+)*\s+import\b)", t, re.M):
                mod = m.group(1) or m.group(2)
                if mod not in std and mod not in local and mod not in ("PIL", "numpy", "cv2", "faster_whisper", "yaml", "__future__"):
                    unknown[mod].add(sk)
    return used, unknown


def fmt(names):
    s = sorted(names)
    return ", ".join(s[:8]) + (f" +{len(s) - 8} more" if len(s) > 8 else "") if s else "-"


def write(tree, out=None):
    out = out or tree
    used, unknown = scan(tree)
    lin = ["# Dependencies - Linux", "", "Generated by `skills-manager/scripts/deps.py` from the scripts themselves (the Used by column is",
           "what the code calls). Everything is free. Commands are Debian/Ubuntu/Mint (apt) and Flathub; other",
           "distributions have the same packages. Install the core, then what the skills you use need.",
           "Windows: see [DEPENDENCIES-windows.md](DEPENDENCIES-windows.md).", ""]
    win = ["# Dependencies - Windows (recommended equivalents)", "", "Generated by `skills-manager/scripts/deps.py`. The skills were built and tested on Linux (X11).",
           "On Windows:", "",
           "- **Should work as is** (pure Python + Python packages; not yet tested on Windows): the knowledge skills, game guides, dice/combat math,",
           "  manuals as text, wiki-scout, the context system (check-skills hook, unload, chat-review, archive-curator,",
           "  doc-standards, cleanup), skills-manager, Dominions modding and data tools. Run scripts with `python -I`",
           "  (also in the hook commands: `python3` is usually not on PATH on Windows).",
           "- **Needs porting**: game-ui and everything that drives a game window (dom6-ui, bgplay, hand-back,",
           "  photo-map shooting) call X11 tools; the equivalents below are what a port would use.",
           "- **Linux-only**: install-windows-games (Lutris/Wine) - on Windows the games just install natively.",
           "- **Alternative**: WSL2 runs the Linux side unchanged, but it cannot drive native Windows game windows.",
           "", "`winget` ships with Windows 10/11; `scoop` is at scoop.sh. Check an id with `winget search NAME`.", ""]
    for cat, title in CATS:
        rows = [(k, v) for k, v in T.items() if v[0] == cat and (used.get(k) or cat == "core")]
        if not rows:
            continue
        lin += [f"## {title}", "", "| Dependency | Install | Used by |", "|---|---|---|"]
        win += [f"## {title}", "", "| Linux | Windows equivalent | Install | Notes | Used by |", "|---|---|---|---|---|"]
        for k, v in rows:
            u = fmt(used.get(k, ())) if v[1] else "everything"
            e = lambda x: x.replace("|", "\\|")             # a pipe inside a cell would split the table
            lin.append(f"| {e(k)} | {e(v[2])} | {u} |")
            win.append(f"| {e(k)} | {e(v[3])} | {e(v[4])} | {e(v[5]) or '-'} | {u} |")
        lin.append("")
        win.append("")
    extra = ["## Per game", "", "The games themselves (Steam, GOG, ...) and their manuals are not included: each `<prefix>-guide`",
             "reads your own install and documents. dom6-inspector's data is rebuilt from your own Dominions 6 with",
             "its `scripts/build.py` (git + Firefox).", ""]
    if unknown:
        extra += ["## Not yet classified", "", "Third-party imports found in the code that this table does not list yet:", ""]
        extra += [f"- `{m}` ({fmt(s)})" for m, s in sorted(unknown.items())] + [""]
    for name, lines in (("DEPENDENCIES-linux.md", lin + extra), ("DEPENDENCIES-windows.md", win + extra)):
        with open(os.path.join(out, name), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    return used, unknown


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    tree = os.path.abspath(a[0]) if a and not a[0].startswith("--") else \
        os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4))
    out = a[a.index("--out") + 1] if "--out" in a else tree
    used, unknown = write(tree, out)
    print(f"{len([k for k in T if used.get(k)])} dependencies in use, {len(unknown)} unclassified imports "
          f"{sorted(unknown) if unknown else ''} -> {out}/DEPENDENCIES-*.md")
