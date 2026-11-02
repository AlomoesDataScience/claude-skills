# Tools these skills need

Everything here is free. Install what the skills you use need; the "Used by" column says which.
Commands are for Debian/Ubuntu/Mint (apt) and flatpak; other systems have the same packages.

## Required for most skills

| Tool | Install | Used by |
|---|---|---|
| Python 3.10+ | `sudo apt install python3` | every script (run them with `python3 -I`) |
| Pillow (PIL) | `sudo apt install python3-pil` or `pip install pillow` | game-ui, dom6-* screen tools, Sprite Studio, mapgen |
| curl | `sudo apt install curl` | game-sources, wiki-scout, game-ui |
| file | `sudo apt install file` | wiki-scout (docpull type checks) |
| git | `sudo apt install git` | skills-manager, dom6-inspector |

## Reading manuals and documents (game-sources, wiki-scout)

| Tool | Install | For |
|---|---|---|
| poppler-utils (`pdftotext`, `pdfinfo`, `pdftoppm`) | `sudo apt install poppler-utils` | manual.py text, outlines, page images for OCR |
| LibreOffice (`soffice`) | `sudo apt install libreoffice-core libreoffice-writer` | manual.py doc: Word/RTF/ODT rulebooks (headless, own throwaway profile) |
| 7-Zip | `sudo apt install p7zip-full` | unpacking .7z/.rar archives from intake |

## Seeing and driving the screen (game-ui, dom6-ui, learn-a-game, obs-record)

X11 desktop only (not Wayland).

| Tool | Install | For |
|---|---|---|
| xdotool | `sudo apt install xdotool` | clicks, keys, typing into one window |
| wmctrl, xwininfo, xprop | `sudo apt install wmctrl x11-utils` | finding and focusing the game window (`UI_WMCLASS` / `UI_WMTITLE`) |
| ImageMagick (`import`, `convert`) | `sudo apt install imagemagick` | window screenshots, crops |
| Tesseract OCR 5 | `sudo apt install tesseract-ocr` (+ `tesseract-ocr-jpn tesseract-ocr-jpn-vert` for Japanese) **or** the NormCap flatpak `flatpak install flathub com.github.dynobo.normcap`, which bundles it (set `TESSDATA_PREFIX` as game-ui's SKILL.md explains) | ocr.py: reading screens and scanned manuals |
| OBS Studio | `flatpak install flathub com.obsproject.Studio` with its WebSocket server on (port 4455) | obs-record (obs.py is pure Python, no pip) |

## Per game

| Tool | For |
|---|---|
| The game itself (Steam, GOG, ...) | each `<prefix>-guide`; the skills read your own install and manuals, nothing is included |
| Dominions 6 | dom6-*; **dom6-inspector's data is not included**: `python3 -I scripts/build.py` in that skill rebuilds it by cloning the community dom6inspector site (needs git and Firefox) |
| .NET SDK 8+ | C# projects (`dotnet`) |
| A browser | Sprite Studio's editor page |

## Standalone tools

- `Games/Fantasy Strategy/Dominions 6/spritestudio/`: 3D-to-sprite editor for Dominions 6. `python3 server.py` (needs Pillow);
  `python3 tools/build.py` makes the one-file app. Bundles three.js r160 (MIT, see `release/THIRD-PARTY-NOTICES.txt`).
- `Games/Fantasy Strategy/Dominions 6/Maps/mapgen/`: Dominions 6 map generator and map-from-picture tools (`python3 mapgen.py --help`; Pillow).
