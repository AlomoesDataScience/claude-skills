---
name: context-hygiene
description: "Working rules that keep context small: OCR over screenshots, crops, batched calls, capped outputs, sections not whole files, few skills loaded. Use in every task, especially screens, shell work and long sessions."
keywords: "without, losing, quality, text, full, shots, tool, scripts, pasted, file, contents, load, step, needs, unload, ends, doing, check-skills, hook, points, message, commands"
---

# Context hygiene

The user (2026-11-09): "the full size screens are not necessary, OCR is better, we do need to set up proper rules"
... "I'm afraid this will impact performance if we do it wrong." Measured basis: `Proposals/Context cost
review.md` (screenshots 17%, Bash output 27%, inline scripts and file contents 21%, average context 240k).
Everything that enters the context is re-sent on every later request until a clear - so each rule saves many
times its size. **Quality first**: when a rule would make me guess, take the bigger look and say why.

## Screens (games, apps)
1. **Text first**: `bgplay.py text [box] [--find WORD]` gives each text line with its centre (click targets);
   `bgplay.py read REGION` for known panels; `dom6bg.py read ...` in Dominions. Most "what's on screen" and
   "where is the button" questions end here.
2. **Picture only when the picture is the point** (unit positions, map geometry, colours, layouts, a screen
   seen for the first time) - and then **a crop** (`shot --box X0 Y0 X1 Y1`) or the half-size default `shot`.
   `--full` only when small detail across the whole screen is needed (first map of a battle board).
3. **Never re-read** an image already seen; after an action, check the change by text (or a crop of the
   changed area).
4. Waits and checks report in one line (`act`, `isloading`) - don't follow them with a screenshot unless the
   one line says something unexpected.

## Tool calls
- **Batch**: one script per step; independent calls in parallel; no one-line probes (each call re-sends the
  whole context).
- **Cap output**: `| head -n`, `grep -c`, `--n`; scripts print summaries, not dumps. Never `cat` a big file.
- **Read sections**: grep for the heading or line, then `Read` with offset/limit. Skills: read the section
  needed, load a whole skill only when its method is being used.
- **Write big files with a script or a template on disk**, not pasted through Write when avoidable; never
  read a file back just to check a write.

## Shell commands (short commands in ~/.local/bin, scripts in this skill's bin/)
| Command | Instead of |
|---|---|
| `q CMD` | any command with unknown or long output: full output to ~/.cache/q/*.log, prints exit code, line count, first 12 + last 8 lines (`-n/-t/-w` to change); then `grep PAT LOG` / `sed -n A,Bp LOG` |
| `g PATTERN [PATH] [-m 3] [-T 40] [-i]` | `grep -rn`: matches per file, then capped lines |
| `peek FILE` / `peek FILE HEADING words` / `peek FILE 120:160` | `cat` or reading a whole file: outline, one section, or a range |
| `bgp ...` `ho ...` `ctxa` `skl ...` | `python3 -I "/home/.../game-ui/scripts/bgplay.py" ...` etc. (handoff, context-audit, skills-manager) |
- **Commands short**: a reusable analysis goes into a script on disk ONCE (in the skill it belongs to), then
  is called with arguments - no 60-line heredoc Python per question (inline scripts were 2.5 M tokens).
- One `cd` + several steps joined with `;` in one call beats several calls.

## Skills and memory
- Load only the 1-3 skills the current step needs (check-skills light hook); already loaded = don't reload.
- Durable facts go to their home (skill, memory, plan file) at once - then they don't need to stay in context.

## Task ends
- Finished a task or past ~100k context: **unload** (hand-off file, then the user clears).

## Measure
`context-audit` after a change; compare req, avg ctx and the source table with the 2026-11-09 baseline.

## Related skills
unload, context-audit, check-skills, game-ui (`text`, `read`, `shot --box`), loading-screens.
