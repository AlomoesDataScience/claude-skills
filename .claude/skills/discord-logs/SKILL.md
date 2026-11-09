---
name: discord-logs
description: "Read the user's Discord history from Discord's data export zip into per-channel logs and a searchable database (discordlogs.py). Use when the user wants to find or keep something he wrote on Discord."
keywords: "request, settings, privacy, messages, servers, dms, group, emailed, few, days, reads, directly, nothing, extracted, run, builds, readable, markdown, file, channel, under, server, day, sqlite, full-text, search, words, phrases, date, plus, lists, stats, tokens, bots, scraping, itself, pull, game, talk, turn, deadlines, deals, notes, log, scraper"
---

# Discord logs from the data export (discord-logs)

The user (2026-11-03): "can you make a discord log scraper?" - he picked his own messages and DMs, as readable
logs and a searchable database.

## Why the export, not a scraper
- Scraping with his account token is a self-bot: against Discord's terms and can get the account banned.
  Never build that, never ask for his token (house rule: no cookies, logins or bot-check evasion).
- A bot token works only for servers whose admin adds the bot - an option later for a server he runs.
- The export is Discord's own, complete for his messages - but it has **only his messages**, not replies.

## Steps
1. The user: Discord > Settings > Data & Privacy > Request all of my Data (Messages ticked). The zip arrives by
   email (days, not minutes). He puts it anywhere (e.g. Downloads).
2. `python3 -I scripts/discordlogs.py import ~/Downloads/package.zip` -> `~/Documents/discord-logs/`
   (`--out DIR` to change). Personal data: keep it out of the workspace and the skills git.
3. Read: `logs/<server>/<channel>.md`, `logs/DMs/<name>.md`.
4. Search: `discordlogs.py search "turn deadline" --server Dominions --from 2026-01-01` (FTS5: "phrase",
   word*, OR, NOT); `channels`, `stats`, `sql "SELECT ..."` (tables channels, messages).
5. A newer package: import again (it replaces the database).

## Notes
- Handles both package layouts: Messages/c<id>/messages.json (new) and Messages/<id>/messages.csv (old);
  index.json gives channel and DM names; attachments stay as links.
- Tested 2026-11-03 on a made-up package in both layouts (not yet on a real one - check the first real import's
  counts against what the user expects).
- Game talk worth keeping (deadlines, deals) goes into that game's folder as notes, with dates.

## Related skills
user-todo (things he must do himself, like requesting the export), library-intake (filing drops),
skills-manager.
