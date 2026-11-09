# dom6-ui - Seeing the screen (`vision.py`)

Part of the dom6-ui skill; SKILL.md links here.

## Seeing the screen (`vision.py`)

**Look before clicking: `vision.py scene` gives every element on the screen, organised.**

```
vision.py scene [IMAGE] [--frames N] [--out PNG] [--json] [--no-text]
vision.py read IMAGE X0 Y0 X1 Y1 [--dark]              # the text in a box (Tesseract)
vision.py find IMAGE NAME [NAME...] [--box X0 Y0 X1 Y1] # where saved templates appear
vision.py add NAME IMAGE X0 Y0 X1 Y1 [--kind sprite|icon|ui|text] [--note TEXT]
vision.py templates                                     # the template library (templates/)
vision.py video OUT.gif [--n 16] [--gap 0.25]           # a short clip of the game
```

- With no IMAGE, `scene` and `video` grab the game under the guard (wait for idle, game in
  front only, focus given back). `--frames 16` grabs a burst first: **what moves is the 3D world**
  (the menu camera flies; the battle replay behind the menu), what stays is UI and text. Use it on
  the main menu: one still frame misses buttons whose edges blend into the backdrop.
- Output tree: `windows` (found by the tan frame round every window, and by the flat dark-grey
  panel), each with `bars` (header and group bars, with their title), `text` (lines with their
  reading, score and word boxes) and `sprites` (sprites and icons); `floating` text and sprites
  outside windows (main-menu buttons, banners, the version line); `background` shares of sky,
  water, land, trees and the biggest tree/object boxes.
- How it tells things apart: UI panels are flat, colourless grey; the frame is a tan strip with
  dark panel 10 px inside; text is grey/white/black (low saturation), sprites are coloured;
  candidates are cut from an edge mask by recursive row/column cuts (so an icon column and a
  name column split apart); a candidate that Tesseract cannot read becomes a sprite or icon.
- **Text reading: Tesseract 5 from the NormCap flatpak** (`com.github.dynobo.normcap`, installed
  by the user; run as `flatpak run --env=TESSDATA_PREFIX=/app/share/tessdata
  --command=tesseract com.github.dynobo.normcap`). `vision.ocr(img, boxes)` reads all boxes of a
  screen in one call (~1 s): each box is turned dark-on-white, enlarged 3x and stacked. It read
  30/30 nation names and 34/34 Mods rows exactly. `vision.closest(text, names, limit, margin)`
  snaps a reading to known names (margin rejects v2.1 vs v2.10 ties). Without NormCap, a pure-PIL
  glyph reader (`vision.read`) is used: about half the lines exact, every nation name snaps.
- Text and sprites change size (text-size preference, map zoom): the reader does not assume a
  size, and `find` tries each template at the scale that fits each element (0.9-1.1x of it, and
  1x), sliding a few pixels, then to the pixel. Score = mean colour difference over the
  template's own pixels (black = transparent): 0 = identical, under ~0.06 = the same picture.
- Templates: `templates/<name>.png` + `index.json` (vision.py's `TEMPLATES`; set `UI_TEMPLATES` to use another folder). Saved: the nine magic path icons of the
  design screen (`path_fire` ... `path_blood`). Add one with `add` from any screenshot.
- Test screens: `tests/shots/*.png` (full size): main menu (hills, underwater), Game Tools,
  era, nation list, nation overview, design, form chooser and tooltip, bless list, Mods.
- The world behind the menus changes per launch (hills, sea floor), so never key on it.
