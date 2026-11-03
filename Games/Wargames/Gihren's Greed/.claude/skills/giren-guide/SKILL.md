---
name: giren-guide
description: Starter guide to Gihren's Greed (Kidou Senshi Gundam - Giren no Yabou, Bandai's Gundam grand-strategy wargame series; the community wiki covers Axis no Kyoui V for PSP/PS2), a Japanese-language game - what it is (strategic map phase plus hex battles, factions and campaigns, tech levels, production, pilots and their stats, scanning and Minovsky particles), how Claude reads its Japanese screens (game-ui ocr.py --lang jpn plus Claude's own translation, a glossary kept here), and the local copy of the girensgreed.fandom.com wiki (sources/wiki/*.wiki, fetched through the MediaWiki API). Uses game-ui, game-sources, learn-to-play. Use when the user wants to play, learn or talk about Gihren's Greed / Giren no Yabou, needs its Japanese screens read or translated, or asks about its factions, units, pilots, events or mechanics.
---

# Gihren's Greed (Giren no Yabou) - starter guide

Status 2026-10-29: no manual exists for the user ("I can't find the manual. Game is in
Japanese, I need a translator/screen reader for Japanese"). The fan wiki was fetched; the GameFAQs
FAQ the user linked (gamefaqs.gamespot.com ... /faqs/74572) is behind Cloudflare and not in the
archive yet - ask the user to save it from a browser if needed. Not played yet.
**Check first:** which edition and platform the user has (the wiki is about *Axis no Kyoui V*,
PSP/PS2; later entries exist, e.g. the 2021 PS4/Switch *Gihren's Greed*). Likely run in an
emulator (PPSSPP / PCSX2): find its window class with `wmctrl -lx`.

## Sources here

- `sources/titles.txt`: all 368 wiki page titles. `sources/wiki/<title>.wiki`: the pages' wikitext
  (MediaWiki markup; `grep -l` across them; `[[target|text]]` are links). Fetched with game-sources
  `wikifetch.py allpages/api https://girensgreed.fandom.com/api.php ...` (the HTML site gives 403,
  the API answers).
- Start with: `Menus` (screen-by-screen menu meanings), `Rank Translations`, `Factions`,
  `Helpful Tips and Hints`, `Calculations and figures`, `Unit Stats and Hit Calculation`,
  `Mechanic Database`, `Abilities Database`, `Unit recommendation and battle tactics`, and the
  campaign strategy pages (Zeon, EFSF/Revil, AEUG, Titans, Axis Zeon). The rest are units, ships
  and characters (one page each).

## What it is (Claude's summary)

A turn-based grand-strategy wargame across the Gundam Universal Century: you lead a faction
(Zeon, the Earth Federation/EFSF, AEUG, Titans, Axis and unlockable ones), alternating a
**strategic phase** on a world map of areas in space and on Earth (move forces, develop technology,
run projects, spy, manage money and resources, end turn) with **battles** on a tactical map.
Technology is tracked as general, mobile suit and mobile armour levels; production unlocks new
units; story **events** branch by choices (event trees per faction) and by alignment (law/chaos).
**Pilots** matter: rank sets their zone of control, command and charisma help their stack and ZOC,
shooting/fighting/reflex drive combat, kills promote. In battle, **scan** unknown enemies before
attacking (unscanned targets are much harder to hit) and use **Minovsky particles** (they cripple
long-range fire and sensors, especially in space; you can scatter them and attack in the same turn).

World map menu (from the wiki's Menus page): information/espionage, military/movement,
development/technology, plan/projects, system, end turn - plus the turn, money and resources
readouts. **End turn only with the user's go.**

## Reading the Japanese screen

1. `gameui.py shot --full` (UI_WMCLASS = the emulator), crop the menu or message box.
2. `ocr.py image SHOT --box ... --lang jpn --scale 3 --dark` (light-on-dark text; `--psm 7` for
   one line). Vertical text: `--lang jpn_vert`.
3. Translate it yourself; check names against the wiki (pilot, unit and place names are in
   English there) and add every menu word here, so later screens read at a glance.

Glossary (game-generic words; extend as screens are read): 生産 production, 開発 development,
作戦 operations, 外交 diplomacy, 情報 information, 諜報 espionage, 計画 plan/projects, 移動 move,
攻撃 attack, 索敵 search/scan, 待機 standby, ターン終了 end turn, 資金 funds, 資源 resources,
技術 technology, 部隊 unit/force, 戦艦 battleship, 機体 machine (mobile suit), パイロット pilot,
階級 rank, 指揮 command, 魅力 charisma, 射撃 shooting, 格闘 melee, 耐久 endurance, 反応 reaction.

## To learn next

1. Confirm edition and platform with the user; look at the title screen with game-ui.
2. Read the Menus and Mechanic Database pages in full; map the world-map menu with click points.
3. Start the Zeon or EFSF main campaign (best documented) with the user's go.
