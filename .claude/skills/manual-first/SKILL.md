---
name: manual-first
description: The default reflex whenever something new pops up in a game - a new screen, option, setting, map type, term, unit line, order or icon - look it up in the game's manual FIRST, before guessing, clicking or reading game files, then write what it says into the game's guide with the page. lookup.py finds the game's manuals, searches every one for the term, shows each hit with its page and chapter heading and says which pages to read as pictures (the colour/ebook version has labelled screenshots). Order of truth - the game wins over the manual, the manual over a hypothesis. The user's rule (2026-11-02, FoG II). Use whenever a game shows something not yet in its guide, when the user names something to check, before acting on any belief about a rule, and before opening game data or scripts.
---

# Manual first

The user (2026-11-02): "Again you need to check the manual by default when something new pops up."
It came up when I picked a map type (North European Agricultural) and went digging in the game's script
files for terrain rules instead of reading the manual's terrain chapter.

## The reflex - every time something new shows up
1. **Name it.** The exact words on screen: "North European Agricultural", "Enclosure", "Swordsmen 50%".
2. **Look it up:** `python3 -I lookup.py "TERM" [--game GAME_FOLDER]`. Read every hit, then read the
   whole section around it - conditions sit in the next sentence or a table footnote.
3. **UI and terrain: read the pages as pictures.** Use the colour/ebook PDF. Its screenshots have
   labels pointing at each element, and some sections are missing from the printer-friendly text.
   (FoG II: Pitch/Tilt and "F1 = all keys" were only in the ebook.)
4. **Write it down** in the game's guide (COMMANDS / PLAY / UNITS or similar) with the page, in my own
   words. Copy conditions exactly; never write a rule from memory.
5. **When the manual is silent or vague** (e.g. FoG "other terrain may cost more AP", no numbers):
   - check the game's own help (tooltips, F1 lists, in-game encyclopedia);
   - otherwise write a hypothesis with its test into the guide's "Hypotheses to test" list.
6. **When the game disagrees with the manual,** the game wins. Note it in the guide's "Game vs manual"
   list.
7. **Not the default:** game data and script files. They're a last resort, and only to read, never to
   change. Tell the user before relying on them.

## Order of truth
1. The game: what it shows and does.
2. The manual.
3. A hypothesis, tested later. In single-player games, play on until it can be tested.

## lookup.py
- `lookup.py TERM [TERM2 ...] [--game DIR] [-C 2]`
  - Finds PDFs under DIR (default: walks up from the current folder to the game folder that has a
    Manuals/ folder).
  - Makes or reuses the page-numbered text (game-sources manual.py).
  - Prints each hit as `[manual] p.N  §heading  line`.
  - Ends with a line of pages to read as pictures, for the ebook/colour PDF if one exists.
- `lookup.py --list [--game DIR]`: the manuals found, and whether each has text.

## Related skills
save-scum (DARK ARTS, learning only: save before a test, reload after; never in real games), game-sources (manual.py), learn-to-play and learn-to-mod (where it's used), wiki-scout (when the manual is missing), generalize-learning
