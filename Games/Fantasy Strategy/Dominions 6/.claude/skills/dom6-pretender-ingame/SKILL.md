---
name: dom6-pretender-ingame
description: Build a pretender god inside the running Dominions 6 through Tools & Manuals (Game Tools) > Create a Pretender God and save it to the user's created pretenders, from a design checked with the dom6-pretender calculator. Picks the era and nation, the physical form (telling same-name forms like the Dragons apart), sleep state, magic paths, dominion, scales and blesses, reads the game's points back and names and saves the god. Uses the dom6-ui guard (waits for the user to be idle, works only while the game is focused). Use when the user asks Claude to make, enter, save or check a pretender in the game itself, to put a designed god into the game's pretender list, or to see what the game charges for a design.
---

# Building a pretender in the game

`scripts/build_god.py` enters a design in the running game (it does not start the game) and saves
it. The design comes from the **dom6-pretender** skill: same NATION, GOD and design options as its
`pretender.py build`. Run from this skill's `scripts/` folder with `python3 -I`.

```
build_god.py NATION GOD [--paths "F2 S3"] [--dom 5] [--scales "order=3 prod=1 luck=-1"]
             [--prison awake|dormant|imprisoned] [--bless "Name,Name x2"] [--name "God name"]
             [--mod DIR] [--cost ID=N] [--no-save] [--dry]
build_god.py --save-current [--name "God name"]     # save the design that is open in the game
```

- `--dry` only checks the design with the calculator (budget, minimum sleep, scale limits, bless
  paths and points) and prints the plan. Always run it first.
- `--no-save` stops on the finished Design Pretender screen so the user can look at it, change
  it and save it; `--save-current` then saves it.
- It prints the calculator's and the game's "design points left / bless points left". **The
  game's numbers win**; a difference is printed as DIFFERENT, and the shot shows the design.
- The saved god shows in Game Tools > View Created Pretenders, and in a new game's pretender
  screen with Ctrl+L.
- Screens of each stage: `~/.cache/game-ui/dom6_amd64/god_NN_<stage>.png` (half size). Read them when it stops.
- One build takes 1-1.5 minutes (it hovers every form of the right dominion group).

## Workflow

1. Design with dom6-pretender (`pretender.py design/optimize/build`), agree it with the user.
2. `dom6ui.py find` + `shot`: the game must be on the **main menu or Game Tools**. If it shows
   anything else (a game, a lobby), ask; never back out of a running game.
3. `build_god.py ... --dry`, then the real run (`--no-save` if the user wants to look first).
4. Report the saved file (`~/.dominions6/savedgames/newlords/<era>_<nation>_<n>.2h`), the
   game's points and any difference from the calculator.
5. Leave the game on Game Tools or the main menu, and give focus back to the user's terminal.

## Safety (the user's rules; see dom6-ui)

- Uses the dom6-ui guard: waits until keyboard and mouse have been idle 4 s, sends input only
  while the game window is focused, and stops ("STOPPED: the game lost focus") the moment the
  user switches window. After a stop, look at a fresh shot before doing anything.
- Never touches saved games, network or Steam. It only writes a pretender file in `newlords`.
- Test builds: note `ls newlords` first and delete only the files the test made (check the
  time stamp). The game numbers files per nation (`mid_marignon_0`, `_1`...).
- When a run stops halfway, the game is left as it is: **do not press Escape in the form
  chooser** (it keeps the hovered form). Use the design screen's Cancel (tools mode) to drop an
  unsaved design; it goes back to Game Tools.

## How it reads the screen

Lists (nations, blesses) and the form tooltip are read with dom6-ui's `vision.py`: Tesseract
(NormCap flatpak) reads every line of the screen in one call and `closest()` snaps each to the
known names; the tooltip "Name - N points" is parsed from the reading. Without NormCap it falls
back to `textmatch.py`. dom6-ui's `scripts/textmatch.py` is not OCR: it renders the candidate strings (nation names, form names,
bless names, numbers) in the game's own fonts (`data/guifont.ttf`, titles and panel headers in
`guifont_fancy.ttf`) at quarter-point sizes 15-32 and compares them with the screen, first
whole, then in 36-pixel slices so a different first word cannot hide behind a shared tail
("Raven / Statue of the Underworld"). Numbers are read between known text ("Design points:",
"Name - ... points", "Bless Effects (... bless points left)"). A good match scores under ~0.3.
Text sizes seen: list names ~19, bless list ~20.75, design digits ~19, tooltip 19, main menu
~27.

## Screen facts (window 1920x1044, full-size pixels, version 6.37)

- **Clicks must land on the text or the sprite.** The game ignores clicks on the blank part of
  a list row or a form cell. The script clicks a little way into each row's text and hovers the
  sprite pixel nearest each cell centre (empty cells are skipped).
- Pointer moves glide in (dom6-ui `click`): a pointer that jumps straight onto a row sometimes
  does not register the hover; the click is held 150 ms.
- Game Tools > Create a Pretender God (840,294) > Select Era (radios x 665, y 202/373/531;
  Ok 959,689) > Select Nation (scrolling list, rows ~28.4 px apart from y 73, nation-id order
  within the era; the hover tooltip is the description) > nation overview (Return = Ok) >
  Design Pretender.
- Design Pretender: the window re-centres vertically whenever its content grows, so every
  position is taken from the four panel header bars (pixel RGB 50,49,49 at x 660/700/1200/1262:
  Magic, Bless, Dominion, Imprisonment). Path icons at magic+32, x F 711, A 765, W 817, E 868,
  S 920, D 973, N 1024, G 1077, B 1130; dominion icons at dominion+41, x candles 710, order 772,
  productivity 823, heat 877, growth 925, luck 980, magic 1033; the number sits at icon+15..+38.
  Left click = +1 (or the positive side), right click = -1 (Turmoil, Sloth, Cold, Death,
  Misfortune, Drain): the icon changes side and the number is the size. Sleep radios x 665 at
  prison+34/+63/+91, Ok prison+177, Cancel prison+209. Hotkeys: p form, a add bless.
- Form chooser: groups under red-brown semi-transparent bars "Dominion 4/3/2/1", 10 cells a row
  at x 403+122j, first row at bar+66, rows 116 apart; hover shows "Name - N points" at the
  bottom centre. The order is not by id, and names repeat (Marignon and Ulm have five 260-point
  Dragons): the script tells them apart by comparing each cell's colours with the inspector
  sprites (`dom6-inspector/data/images/sprites/<id>_1.png`).
- Bless list ("Choose Bless Effect"): only blesses the god's paths allow, in the calculator's
  order; rows 31.6 px apart from y 74, names in x 840-1085.
- Ok with points left asks "You have N design points left..." and then "You have N bless effect
  points left..." (Yes 959,459 each). Then the name prompt (random name filled in; Ok 959,458),
  then "All praise X" Ok (959,474), which writes the file and returns to Game Tools.
- Bless points in game = Σ(path level - 1) + the nation's bonus, as the calculator says.

## Limits

- Mod nations and mod forms need the mod enabled in the game (the user decides that; dom6-ui's
  `mods.py enable NAME` does it) and
  `--mod DIR` so the calculator knows them.
- Same-name forms are told apart by colour only: check the shot of the design screen.
- Not done: disciple pretenders, passwords, loading a saved design (Ctrl+L).

## Changing an open design (to do)

When a design is already open on the design screen and only one part changes (blesses, a path,
a scale), change just that part in the game instead of cancelling and rebuilding (user,
2026-10-27). build_god.py has no edit mode yet: `add_blesses()` only adds. **A taken bless is
removed by clicking it in the bless panel on the design screen** (user, 2026-10-27). Next: add an
`--edit` option that skips the nation and form steps and removes/adds only what changed.

## Standards (audit 2026-11-03)
- **Screen:** coordinates here were measured on the 1920x1044 desktop. On Claude's 1912x1000 virtual screen (dom6bg.py / bgplay) find positions by OCR or re-measure - never reuse a stale coordinate (memory: apply tools universally).
- **Where it runs:** prefer Claude's virtual screen (dom6-ui bgplay, dom6bg.py); lock while working, hand back after (hand-back).

## Related skills
dom6-pretender, dom6-ui, dom6-tooltips.
Also (2026-11-03): dom6-pretender, dom6-ui.
