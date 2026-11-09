# game-ui - Reading text (`scripts/ocr.py`)

Part of the game-ui skill; SKILL.md links here.

## Reading text (`scripts/ocr.py`)

```
ocr.py image SHOT.png [--box X0 Y0 X1 Y1] [--lang eng|jpn|jpn_vert|eng+jpn] [--psm 6|7] [--scale 3] [--dark] [--tsv]
ocr.py pdf MANUAL.pdf [OUT.txt] [--lang eng] [--dpi 300] [--first N --last M]   # scanned manuals
ocr.py langs | ocr.py getlang LANG [--fast]
```

- Tesseract 5 from the NormCap flatpak (`com.github.dynobo.normcap`, the user's install), with its
  data in `~/.var/app/com.github.dynobo.normcap/data/tessdata` (eng copied from the app, jpn,
  jpn_vert and osd from tessdata_best, added 2026-10-29). Other languages: `getlang`.
- Game text: crop to the text (`--box`), `--scale 3`, `--dark` for light-on-dark, `--psm 7` for a
  single line, `--psm 6` for a block. Japanese output has Tesseract's spaces between CJK
  characters removed.
- **Japanese games** (the user's Gihren's Greed has no English): read the screen with
  `--lang jpn` and translate it yourself; keep a glossary of the game's menu words in the game's
  skill so later screens are read faster. Test: rendered menu words (生産 開発 作戦 外交 ターン終了)
  came back exact.
- Dominions has a richer reader (dom6-ui's `vision.py`: element tree, its own font) - use that one
  for Dominions screens.
