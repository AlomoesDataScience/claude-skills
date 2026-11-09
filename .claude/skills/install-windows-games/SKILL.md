---
name: install-windows-games
description: "Install Windows games (GOG offline installers, setup.exe) and GOG Linux .sh installers into Lutris, one Wine prefix each (wininstall.py). Use when the user drops installers or a Windows game must run."
keywords: "show, silent, installs, under, through, lutris's, umu-run, proton, builds, launch, command, read, gog's, goggame, info, config, database, entry, written, msi, something, says, has, launcher, needs"
---

# Install Windows games (Lutris)

Built 2026-11-01 when the user dropped GOG installers (Imperialism, Star Wars Rebellion, Daggerfall,
Master of Orion 1 and 2) and asked for them "installed with Lutris". GOG Galaxy has no Linux
client; the offline installers are enough.

```
wininstall.py runners
wininstall.py install imperialism "<workspace>/setup_imperialism_2.1.0.11.exe"
wininstall.py gogsh master-of-orion "<workspace>/gog_master_of_orion_2.0.0.2.sh"
wininstall.py launch imperialism          # primary play task from goggame-*.info
wininstall.py register imperialism "Imperialism" --year 1997
```

## How it works
- Lutris is the Flatpak `net.lutris.Lutris` (data `~/.var/app/net.lutris.Lutris/data/lutris`:
  `pga.db`, `games/*.yml`, `runners/wine/<build>`, `runtime/umu/umu-run`). It can read the home folder.
- **Go through umu-run** with `PROTONPATH=<runner>`, `GAMEID=umu-default`, `WINEPREFIX=~/Games/<slug>`,
  inside `flatpak run --command=bash net.lutris.Lutris`. Running a Proton build's `files/bin/wine`
  directly breaks installers (wined3d/ddraw missing).
- GOG Windows installers are Inno Setup: `/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP- /LOG=C:\inst.log`
  (they go to `C:\GOG Games\<Game>`). Read `drive_c/inst.log` when nothing appears.
- GOG Linux `.sh` (MojoSetup, DOSBox games): `-- --i-agree-to-all-licenses --noreadme --nooptions
  --noprompt --destination DIR`; Lutris runner `linux`, exe `start.sh`.
- `register` backs up pga.db, writes `games/<slug>-<time>.yml` (format copied from Lutris's own
  entries) and updates the row if Lutris already lists the game (Steam/imported entries exist).
  An open Lutris shows new entries after a restart.
- One prefix per game keeps a bad install from breaking another.

## Rules
- Only install what the user asked for; installers are his files - don't move or delete them without
  telling him (library-intake decides where they go).
- Check disk space first (`df -h ~`); old GOG games are 25 MB - 1.2 GB installed.
- Test launches: Proton under umu **ignores a bgplay virtual screen** - with DISPLAY=:6 the game's
  window still opened on the user's desktop. So a test launch is always on his screen: tell him first.
  Don't kill a "silent" test: it may be showing a window he can see.
- First run of GOG Imperialism shows "Imperialism Setup" (210x115, class `steam_app_default`):
  "Switch to game resolution" left unticked (resolution switches under Wine can break the desktop),
  OK -> the game runs full screen 1920x1080, intro movie centred. Verified 2026-11-01.
- .NET or VC runtimes (e.g. `windowsdesktop-runtime-*.exe`): install into the prefix of the game
  that needs them, not globally - ask which game. Method (verified 2026-11-01): match the Proton
  that made the prefix (its `version` file; may be a Steam compat tool in
  `~/.local/share/Steam/compatibilitytools.d/`) as PROTONPATH, run the Microsoft installer with
  `/install /quiet /norestart`, check `drive_c/Program Files/dotnet/shared/*/`. Pick x64 or x86 by
  the game exe (`file`: PE32+ = 64-bit, PE32 = 32-bit -> x86 runtime, `Program Files (x86)`).
  "Proton: Error: unable to use parent for game drive" is harmless.

## Installed so far (2026-11-01)
imperialism, star-wars-rebellion, the-elder-scrolls-ii-daggerfall (DOSBox for Windows, args from
the .info), master-of-orion, master-of-orion-2 (Linux .sh). Imperialism launched and runs; the others not yet tried.

## Related skills
game-setup (first launch and graphics), library-intake, game-sources (copy the manual out)
