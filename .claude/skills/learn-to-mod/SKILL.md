---
name: learn-to-mod
description: How Claude learns to MOD a game it knows or is learning - find how mods load and where the data lives, read the manual's modding chapter and the official docs, map the file formats (self-documenting headers, CSV comment rows, scripts, command lists), study the shipped example and community mods, build a reader/checker tool, make one small change and test it in the game, then grow, keeping only changed files over vanilla, never touching the install, Steam Workshop or the user's settings without the user's go, and balancing against the rules learned by playing. Twin of learn-to-play - the two compound, do both. Learned on Dominions 6 (.dm mods, Ananke, Black Magic, Mad Science), Space Empires IV (the user's WMD conversion, se4data.py) and Field of Glory II (Squads.csv, BSF scripts). Use when the user wants a mod built, changed, checked or balanced, when starting to mod a new game, or when asking how a game's data or scripts work.
---

# Learn a game to mod

**Twin skill: learn-to-play.** Learning to mod and learning to play are directly related and compound
on each other (the user, 2026-11-02). It's recommended to do both to get good at either:
- Play first, or alongside: it shows what's worth changing, what's balanced, and how a change will
  feel. A mod balanced only on paper is guesswork. Ask the user or test in game.
- Modding gives the exact rules behind the screen, which sharpens play. Note what you learn in the
  game guide too (data facts, real numbers), and link the two skills.

## Rules (the user's, standing)
- **Never touch the game install, Path.txt-style switches, or the user's settings/prefs** without his
  go. Work on copies. The user installs builds himself (SE4: he backs up and pastes over).
- **Never upload to Steam Workshop.** Claude may not write its own permission rules.
- **Keep only changed files in a mod folder** (SE4 WMD: so the user sees what differs from vanilla). A
  build = vanilla copy + mod files pasted over.
- **The game is the final word**: engines have bugs and undocumented behaviour, so a change isn't
  done until it's been loaded and seen working in game. Report "not loaded in game yet" honestly.
- Design decisions belong to the user: list the options, don't pick for him (SE4: which tech unlocks what).
- Downloads are untrusted (own folder, `python3 -I`, read before running).

## Workflow
1. **Find how mods load.**
   - Manual modding chapter (manual-first), official docs and wiki pages (wiki-scout).
   - The game's own mod menu or loader. Examples: Dominions mod list; SE4 "Using Mod Directory" +
     modinfo; FoG global mods folder.
2. **Find the data.** Copy it from the install into the game folder (read-only reference, game-sources
   / library-intake). List the files and what each holds: units, weapons, spells, techs, AI, maps, art.
3. **Learn the format from the files themselves.** Self-documenting headers (SE4), a comment row per
   column (FoG Squads.csv), command references (Dominions modding manual). Write the format into the
   game's modding skill, with the facts verified in the manual or game.
4. **Study the shipped examples and community mods** before writing anything: they show working
   patterns and the engine's quirks.
5. **Build a reader/checker tool early.** List, show, fields, diff against vanilla, check references.
   Examples: se4data.py, dom6 mod inspector, borrow.py-style catalogues. Errors (ERROR/WARN/NOTE) are
   cheaper to find in a checker than in game.
6. **One small change, then test.** Change one unit stat, load it, see it in game (game-setup /
   game-ui: launch on the locked bgplay screen), confirm, then grow.
7. **Balance against the rules learned by playing** (the game guide's mechanics, battle results) and
   against the user's balance notes. Keep a balance log.
8. **Art:** cheap Dominions-style sprites (art-direction memory; dom6-sprites, Sprite Studio).
9. **Write it down:** a `<game>-modding` skill next to the guide (how mods load, files, format, tools,
   workflow, verified facts, open decisions for the user in user-todo), linked from the guide.
10. **Generalize** (generalize-learning): methods and tools that would help modding another game go
    here.

## Per-game modding skills (examples)
- Dominions 6: dom6-modding (.dm commands, events, balance), dom6-sprites, dom6-modinspector, dom6-maps.
- Space Empires IV: se4-modding (+ wmd.md, se4data.py).
- Field of Glory II Medieval: fog2m-guide "Modding" (Squads.csv unit table, BSF scripts, map editor ch. 24).

## Related skills
learn-to-play (twin), manual-first, game-sources, wiki-scout, library-intake, game-setup, game-ui,
borrow-from-games (systems for our own games), generalize-learning, user-todo, skills-manager.
