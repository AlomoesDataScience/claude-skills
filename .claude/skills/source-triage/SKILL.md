---
name: source-triage
description: "Sort which of a game's documents are worth reading and in what order when a pile is dropped. Use when starting on a game, when new documents appear, or when unsure which manual version to trust."
keywords: "drops, files, folder, toaw, literally, took, docs, threw, scans, install, guesses, one's, role, keys, hotkey, lists, update, what's-new, readme, notes, override, core, guide, primers, editor, modding, guides, data, tables, older, previous-version, manuals, duplicate, formats, broken, unreadable, advert, catalogues, finds, newest, often, opens, confirms, writes, sources"
---

# Source triage - which documents are good, in what order

The user (2026-11-03): "build a skill to organize what resources are good, cause I literally just took all the docs I
have and threw them in your folder." Filing (where things go) is library-intake; this is **judging** them.

## Steps
1. `python3 -I .claude/skills/source-triage/scripts/triage.py GAME_FOLDER --install INSTALL_DIR` - every
   document with a guessed role, size or pages. `--md` = a SOURCES.md skeleton.
2. **Find the version actually installed** (readme, whatsnew, the game's title screen). Update notes newer than
   the manual OVERRIDE it - the newest one wins. They often sit only in the install (TOAW IV: Whatsnew 4.1
   and the 4.1.0.40 readme were in the install, the folder had only 4.0): copy them into Manuals/ and make text
   (docx: unzip word/document.xml; pdf: pdftotext; scanned: game-ui ocr.py).
3. **Open every candidate** (first pages, table of contents) and confirm the role - names lie. Look for errata
   sections (TOAW: Whatsnew 4.1 Appendix 7 "Manual errata").
4. **Write `SOURCES.md` in the game's guide skill**: read order for play (KEYS -> UPDATE -> CORE by chapter ->
   GUIDE), the modding set (EDITOR, DATA), use with care (OLDER - always say "this is from the old version"),
   ignore (BROKEN, DUPLICATE, ADVERT). Link it from the guide's SKILL.md.
5. Order of truth stays: game > newest update notes > manual > older manuals > wiki.

## Rules
- Never delete the user's files: duplicates and adverts are only marked. Never touch the install (copy out only).
- Purchased PDFs stay local (not in the skills git).

## Related skills
library-intake (where files go), game-sources (manual.py text and outline), manual-first (lookup.py),
learn-to-play (reads SOURCES.md first), wiki-scout (when documents are missing).
