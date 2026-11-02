---
name: learn-a-game
description: How Claude learns to play a video game it does not know yet, the way it learned Dominions 6 with the user: read the manual and the in-game help first, map the screen and the controls, explore menus safely without committing anything, test one thing at a time and check the screen after every action, take the teacher's corrections as rules, write down every lesson (knowledge base, game skill, memory), then play for real in small reviewed steps. Covers turn-based strategy games (4X, Dominions, Civilization-likes) and real-time games such as platformers and metroidvanias (Metroid): controls and movement tests, map and backtracking, ability gates, cheap deaths as experiments. Uses dom6-ui-style guarded input and screen reading. Use when the user asks Claude to learn, try, practise or get started with a game, to learn a new screen, mechanic or genre, or asks how Claude should approach a game it has not played.
---

# Learn a game

A method, not a tool: how to go from "never played it" to "plays it sensibly" by reading, clicking,
testing and writing things down. It is how Dominions 6 was learned with the user (2026-10-26/27).
Generic tools: **game-ui** (guarded input, screenshots, OCR in any language), **game-sources**
(manual PDFs as searchable text, wiki fetching). Each game's own notes live in its folder
(`<Genre>/<Game>/.claude/skills/<prefix>-...`); Dominions' are dom6-ui, dom6-knowledge, dom6-game.
Start a new game with its starter skill (`<prefix>-guide`): what the manual covers, where to look.

## The loop

**Read → look → try one thing → check the screen → write it down → repeat.**
Each step is small, so a wrong guess costs one click, not a turn or a life.

## Workflow

### 1. Set the ground rules first
- Ask or recall what must never be done without a go-ahead. Examples: ending a turn, saving over
  a file, spending a rare resource, touching the user's other games, settings or network.
- Find out what makes an action **final** in this game. Dominions: nothing counts until the turn
  ends with `e` or End Turn. A platformer: save points and one-way doors.
- Work only in the game window, through a guard that waits while the user is busy (dom6-ui
  `session.run`, or `gameui.py seq` with `UI_WMCLASS` set to the game). The user may be at the
  desk and may press keys by accident.
- When finished, hand control back visibly. Here that means raising the terminal.

### 2. Read before clicking
- **The manual.** Turn it into searchable text (game-sources `manual.py text`; scanned ones with
  game-ui `ocr.py pdf`), take the outline (`manual.py outline`/`toc`), grep it for each new screen or
  mechanic, and cite the page. Dominions: Formations p. 59, Mercenaries p. 29.
- **The in-game help.** The hotkey list (`?` in Dominions), tooltips, tutorial text and loading
  tips. Save the hotkeys at once into the game skill.
- **Wikis and community tools** for numbers. Dominions: the Mod Inspector, the pretender
  calculator. Prefer the game's own screens when they disagree.

### 3. Map the screen
- Take a screenshot and name every region: top bar, side panels, lists, the play area. Record the
  coordinates of icons and buttons.
- Hover everything and record the tooltips. Right-click and left-click to see which does what:
  in Dominions, right-click views and left-click selects.
- Open every menu, read it, and close it with its own Exit. Never use a button whose effect is
  unknown and might be final.

### 4. Learn the controls by testing
- One input, one screenshot, one conclusion. Never chain blind clicks.
- **Click the word**, not the space beside it: the middle of the label text. Labels change size
  after a choice (an order label shrinks to its word), so read positions fresh, never from an
  old screenshot.
- After every action, check that the expected window opened or the value changed *before* the
  next click. Misclicks in live lists move things (a unit dragged into the wrong squad).
- Lists scroll and popups shift them. Find a row by its text again right before clicking it.
- Learn the modifiers the teacher shows (alt+click for all units of a type, Enter to deselect).

### 5. Take the teacher's corrections as rules
- When the user corrects something ("it's too far to the right", "click the word", "red dots
  mean blocked"), it becomes a rule. Save it with its reason in the game skill or knowledge base
  straight away.
- Ask about intent, not about things you can test. Test what can be tested.
- The user decides the pace. Do the step asked, report it, and wait for review before the
  irreversible step.

### 6. Write everything down, in the right place
- **Game skill** (dom6-game; for a new game, its `<prefix>-guide` in the game folder): screens,
  hotkeys, click points, how to do each action, safety rules.
- **Knowledge base** (dom6-knowledge, `kb.py add` with a source and date): mechanics, strategy
  lessons, facts about this game's world (the pretender-to-nation map, thrones, scout reports).
- **Memory:** where the current game stands, the next to-dos, and the user's preferences.
- Write while it is fresh, not at the end. A context reset loses whatever was not written.

### 7. Play for real, in reviewed steps
- Use a checklist for every turn or level, built from what was learned. Dominions turn:
  1. Read the messages.
  2. Scout the neighbours.
  3. Set research.
  4. Give orders and set battle orders.
  5. Recruit and bid on mercenaries.
  6. Check everything.
  7. Hand over for review.
- Before handing over, re-check every order on its own screen. Report what was set and why,
  what went wrong on the way, and what is still unknown.
- Explain choices with the numbers you saw: "30 militia vs our 53", "income 75".

### 8. Make tools out of repeated work
- If the same clicks are done twice, write a small script. Examples: a tooltip reader, a
  province scanner, a list reader that re-finds rows after popups.
- If a script works across sessions, put it in a skill (skills-manager `new`).

## Real-time strategy with pause (Paradox: Stellaris, CK, EU, HOI, Victoria)

The user's note (2026-11-01): Paradox games run in real time, not turns, so a single screenshot is
not enough. And his PC is weak, so they run slowly (late game worst).
- **Play pause-driven:** pause (Space), read the screen, give every order, unpause at speed 1 or 2
  for a short stretch, pause again. Pause on events too (the games can auto-pause on chosen alerts:
  set that up first). This turns them into short turns that screenshot reading can handle.
- **Watch while it runs:** a loop that captures the window every few seconds and OCRs only the
  bits that matter (date, resources, alert icons, popups), pausing when something changes. Build
  this on game-ui's ocr.py as a `watch` mode when we first play one. Keep it light, since the game
  already struggles on this machine.
- Low settings, small galaxies or maps, fewer AI empires: faster ticks and fewer popups.

## Real-time games: platformers and metroidvanias (Metroid and similar)

The loop is the same, but time does not wait, so the order changes:
- **Pause or slow down where possible.** Read the screen while paused. Tests in real time are
  short bursts followed by a screenshot.
- **Movement physics first, in a safe room:** walk speed, jump height and length (tap vs hold),
  run-jump distance, wall and ledge behaviour, crouch and morph, how long a dash or shot lasts.
  Measure in tiles or pixels and write the numbers down. "A full jump clears 3 tiles up, 5
  across" is a fact you can plan with.
- **Enemies one at a time:** their pattern, their reach, how many hits they take, what drops.
  Note what hurts the player and how much (health bar pixels).
- **Deaths and retries are experiments**, as long as they are cheap. Know where the last save or
  checkpoint is before trying something risky. Never save over a slot without a go-ahead.
- **Keep a map with notes.** Rooms, doors by colour or type, blocked paths and *why* they are
  blocked (a high ledge, a missile door, a morph tunnel), save rooms, items. The metroidvania
  loop is: find a gate, note it, find the ability, come back. This is the platformer version of
  "red dots = blocked, needs flying".
- **Abilities change the map.** After each new power, check the gate list for paths it opens.
- **Timing and reaction** may be beyond screenshot-speed play. Say so honestly, and focus on
  routing, planning and mechanics, where careful study wins.

## Strategy games in general (4X, wargames)

- Find the win condition and its numbers early. Dominions: 100 ascension points, and the 60
  thrones are worth exactly 100.
- Learn the economy screens before spending: income, upkeep, what limits buying. On Dominions
  turn 2 that was resources, not gold.
- Scout before attacking, and read every report. Compare the enemy's count and type with your
  own army.
- Settings screens (battle orders, formations, scripts) matter as much as big decisions. Learn
  them on a safe turn.
- Opponents' public announcements (proclamations, the epithet list) are free intelligence.

## Gotchas seen while learning Dominions

Mistakes are part of building a skill, for anyone (the user). Make them where they are cheap,
notice them on the screenshot, fix them, and write the lesson down so it happens once.


- OCR misses words on coloured bars and map labels. Check by screenshot, and click by position
  only after the label has been read once.
- A background watcher can be fooled by another window on top. Check the game window itself.
- Popups can be drawn *instead of* a screen, not over it. Close them with their own Exit.
- Checks that are too strict stop good work: a window may have no title, or a lone commander no
  formations. Loosen the check, then look at the screenshot.
- Don't guess what a symbol, title or term means. Say it is unknown and ask, or test it.
