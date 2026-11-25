---
name: learn-to-play
description: "How Claude learns to play a new video game: manual and in-game help first, map the screen, safe exploration, one test at a time, lessons written down. Use when asked to learn or start a game, screen or genre."
keywords: "know, yet, twin, learn-to-mod, covers, learning, mod, compound, learned, dominions, read, controls, explore, menus, safely, without, committing, anything, thing, check, after, action, take, teacher's, corrections, rules, write, lesson, knowledge, base, skill, memory, real, small, reviewed, steps, turn-based, strategy, games, civilization-likes, real-time, such, platformers, metroidvanias, metroid"
---

**Rule (the user, 2026-11-02): every new game gets learned with this method BEFORE real play - no exceptions.**

# Learn a game to play

**Twin skill: learn-to-mod.** Learning to play and learning to mod are directly related and compound
on each other (the user, 2026-11-02). It's recommended to do both to get good at either:
- Playing shows what matters: which units, rules and screens decide games, how things feel, and
  what's broken or dull. Without play, a mod is guesswork.
- Modding shows the exact rules: the data tables, scripts and real numbers behind what the screen
  shows. That knowledge makes play precise. Order of truth still holds (game > manual > hypothesis),
  and while playing, read the screen and manual first (play fairly; never hook game data during play).
- Each one feeds the other's notes: play lessons go in the game guide, data facts go in the modding
  skill, and each links to the other.

A method, not a tool: how to go from "never played it" to "plays it sensibly" by reading, clicking,
testing and writing things down. It is how Dominions 6 was learned with the user (2026-10-26/27).
Generic tools: **game-ui** (guarded input, screenshots, OCR in any language), **game-sources**
(manual PDFs as searchable text, wiki fetching). Each game's own notes live in its folder
(`<Genre>/<Game>/.claude/skills/<prefix>-...`); Dominions' are dom6-ui, dom6-knowledge, dom6-game.
Start a new game with its starter skill (`<prefix>-guide`): what the manual covers, where to look.

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

## Load the game's guide first (the user, 2026-11-02: "I kinda thought you read the manual")
- At the start of every session with a game and before every battle/turn sequence, load that game's
  guide skill and read its play reference (FoG II: fog2m-guide PLAY.md). Game guides live in the
  game's folder and do not surface on their own - invoke them.
- When learning a game, read the manual **to play it**: unit types and capabilities, combat tables,
  terrain, morale, victory conditions, hot keys - written into a play reference file. A design
  summary (Systems section) is a separate job and is not enough to play.

## The method, as the user walked me through it (FoG II setup, 2026-11-02) - use for every game
0. **Reflex for anything new: manual-first skill (lookup.py).**
   **FIRST: hotkeys and commands** (the user: "this should literally be first thing you look for").
   Every manual has a UI guide - the colour/ebook version has screenshots with labels pointing at
   each element. Read those pages, the hot key list, every order/command, and the in-game key list
   (F1 or similar - the game wins). Write a COMMANDS.md in the game's guide before playing.
1. **Settings first** - every page of them; know what each option does (hover the control itself,
   not its label, for the tooltip); make the game run how we want it before playing.
2. **Every screen: identify each element** - what it is, what it does; read the text the game
   puts on screen (info boxes, blurbs, tooltips) - that's the game telling you what things are.
3. **Go through lists entry by entry** - click each one, read its description; notice patterns
   (e.g. one blurb per nation, filters) instead of assuming. Markers like FoG II's "$" (= DLC you don't own) are specific to each game - find out what they mean there, never carry them over.
4. **THE MAIN THING (the user): look at the units and what they do** - every unit type on both sides: type, quality, armour, abilities, what it beats and what beats it. That is what the plan is built from.
4b. **Preview before committing** - look at my side's options AND the opponent's (army/unit previews,
   unit cards) before any battle or match.
5. **Every term you see -> look it up in the manual** and write what it means for play (unit card
   words, stats, abilities). Read the manual TO PLAY: tables, unit types, terrain, morale, victory.
6. **Turn knowledge into a plan** - what the opponent fields, what beats it, what that means for my
   choices - saved in a plan file (planning skill), then confirmed against the actual map/situation.
7. **One intentional action at a time**, look at the result, report it; repetition only over items
   already seen and chosen. The user leads the walkthrough; don't run ahead (no Create / End Turn on my own).

## After the play guide: a mechanics family (rules-skills)
Once a game is played regularly, make one skill per mechanic a player decides about with rules-skills (pages
cited, numbers computed, a `## Systems` section). Dominions 6 was the first (2026-11-03, ~45 skills).

## Reference files (read the one the step needs)

| File | Holds |
|---|---|
| `reference/the-loop.md` | **The loop** - Read → look → try one thing → check the screen → write it down → repeat |
| `reference/real-time-strategy-with-pause-paradox-st.md` | **Real-time strategy with pause (Paradox: Stellaris, CK, EU, HOI, Victoria)** - the user's note (2026-11-01): Paradox games run in real time, not turns, so a single screenshot is not enough |
| `reference/real-time-games-platformers-and-metroidv.md` | **Real-time games: platformers and metroidvanias (Metroid and similar)** - The loop is the same, but time does not wait, so the order changes: - Pause or slow down where possible |
| `reference/strategy-games-in-general-4x-wargames.md` | **Strategy games in general (4X, wargames)** - Find the win condition and its numbers early |
| `reference/gotchas-seen-while-learning-dominions.md` | **Gotchas seen while learning Dominions** - Mistakes are part of building a skill, for anyone (the user) |
| `reference/order-of-truth-the user-2026-11-02.md` | **Order of truth (the user, 2026-11-02)** - 1 |
| `reference/war-games-speak-doctrine-both-ways-the user.md` | **War games: speak doctrine both ways (the user, 2026-11-02)** - For any game with fighting (wargame, 4X, grand strategy, tactics), as part of learning it: - Write the game's  |
| `reference/map-games-write-a-game-map-skill-the user-20.md` | **Map games: write a `<game>-map` skill (the user, 2026-11-02)** - Every game with a map or board gets its own map skill before real play, next to its guide |

## Related skills
save-scum (DARK ARTS, learning only: save before a test, reload after; never in real games), learn-to-mod (twin - they compound), manual-first (reflex for anything new), game-setup, game-ui, map-usage + map-camera + photo-map (map games), battle-tactics, planning, learn-from-tutorials, generalize-learning, skills-manager, wiki-scout (pull the game's wiki as text)
