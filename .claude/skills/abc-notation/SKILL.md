---
name: abc-notation
description: "ABC music notation: read and write tunes as plain text (header fields, notes, lengths, chords, voices, MIDI programs) and check bar lengths with abccheck.py. Use when writing, reading or fixing ABC tunes or planning the 4X music engine."
keywords: "abc, abc notation, music, tune, score, melody, chord, voice, midi, abc2midi, abcm2ps, EasyABC, %%MIDI program, metre, bar length, L:, M:, K:, Q:, music engine, procedural music, Arrival, Covenant of Ash, Algorithmic Imperium, soundtrack"
---

# ABC notation - music as plain text

Status: active (2026-11-24). Not built: no playback and no renderer. abccheck.py is a read-only checker.

**Origin.** the user 2026-11-24: "Go look into the ABC notation stuff, create a skill for that." His `Overview` file
says: "I suspect that you, the AI, will quite readily be able to produce music/sounds/whatever from knowing ABC
notation and music/sound theory." Also: "I do want to create a scripted generator, because I'm of the mind that
using context can be a big issue." And: "I don't want to get bogged down on a side project like this right now."
The 4X plan (`Build Proposal/07 Sound and Music.md` §2) has the rule **"the user teaches the music theory"**. This skill
covers the notation only. Harmony, voicing and style rules come from the user and get written down as his.

## Where things are
- **The user's tunes:** `Projects/ABC Notation/`. The tune files have no extension. `C:RKH` marks the user's own tunes
  (`ABC Notation`, `Arrival`). `C:AI` or `Arr. Gemini` marks other AIs' output (`Algorithmic Imperium`,
  `Covenent of Ash`, `Arrival Arrangement`), which is a lead only. The .wav files are renders of these tunes and
  others.
- **The standard:** `Code Sources/EasyABC/EasyABC-1.3.8.6-source/reference.txt` (the ABC 2.1 appendix: A.2 field
  table, A.5 `%%` commands). EasyABC is **GPL-2.0, so read it and never copy from it** (license-check;
  THIRD-PARTY-NOTICES row says STOP).
- **Tools on this machine:** none for ABC (no abc2midi, abcm2ps or fluidsynth). There is ffmpeg, plus GM
  soundfonts in `/usr/share/sounds/sf2`. Installing anything is the user's call.

## The notation (in our words)
**Header, in this order:** `X:` (tune number, first), `T:` title, `C:` composer, `L:` unit note length (e.g.
1/8), `M:` metre (4/4, 6/8, `C` = 4/4), `Q:` tempo (`1/4=132`), then `K:` key (last header line, e.g. `Gm`,
`F#m`). The body starts after `K:`. With no `L:`, the default is 1/16 if the metre is below 3/4, else 1/8.
- **Notes:** `C D E F G A B` is the octave from middle C up, `c d e f g a b` the next one. Each `'` raises a note
  an octave and each `,` lowers one (`C,` `c'`). The user's tunes also write `D'` (uppercase with `'`, meaning `d`).
  abccheck counts these, since some programs may read them differently.
- **Accidentals** go before the note: `^` sharp, `_` flat, `=` natural (`^^` `__` double). They last until the
  end of the bar. The key signature applies otherwise.
- **Length** is a multiple of `L:`: `A2` (twice as long), `A/2` or `A/` (half), `A3/2` (dotted), `A/4`. `z` is a
  rest with the same suffixes. `Z4` rests four whole bars.
- **Broken rhythm:** `A>B` means A dotted and B halved, and `A<B` the reverse. The pair keeps its total length.
- **Chords:** `[CEG]2`. The chord lasts as long as its first note times the outer multiplier. A tie is `-`.
- **Tuplets:** `(3abc` means three notes in the time of two. `(p:q:r` means p notes in the time of q, over r
  notes.
- **Bars:** `|`, `||`, `|]` (end), repeats `|:` `:|`, endings `[1` `[2`. Inline changes: `[M:3/4]`, `[L:1/16]`,
  `[K:D]`.
- **Voices:** `V:1 clef=treble name="Lead"`, then `V:1` before that voice's lines (or inline `[V:1]`). Each voice
  must have the same number of bars, or they drift apart.
- **Sound:** `%%MIDI program N` (GM 0-127) under a voice picks its instrument. `%%MIDI channel 10` is drums.
- **Other:** `%` starts a comment. `"Am"` is a chord symbol and `"^text"` an annotation. `!f!`, `!p!` and other
  `!...!` marks are decorations. `{g}` is a grace note (no time). `w:` gives lyrics, `P:A` marks parts.

## Writing a tune (method)
1. **Fix the grid first.** Pick `M:` and `L:` and work out units per bar = M / L (4/4 with L:1/8 is 8 units, and
   with L:1/16 it is 16). Every bar in every voice must add up to that number.
2. **Write voice by voice, bar-aligned.** Put the same number of bars on each line in every voice, so the bars
   line up by eye.
3. **Check:** run `python3 -I .claude/skills/abc-notation/scripts/abccheck.py FILE`. It reports bars that are
   too short or too long per voice, voices with different bar counts, each voice's range (MIDI numbers) and notes
   off the 88 keys. A short first bar is taken as a pickup. Use `--bars` to list every bar.
4. **Keep the range playable:** bass about MIDI 28-55, lead about 60-90. These are PROPOSAL numbers, not the user's.
5. **Theory comes from the user.** When he teaches a rule, write it in a `theory` file in this skill's folder (create it
   then) with his words and the date (doc-capture).

## Checked so far (2026-11-24, abccheck)
- `Arrival`, `Arrival Arrangement` (3 voices), `Algorithmic Imperium` (5 voices) and `Covenent of Ash` (4 voices):
  all bars full, and the voices match.
- `ABC Notation` (the user's): bars 28 and 52 are 3/4 in 4/4 (line 12: `[FF,C][GC][GE,]`, line 15 the same).
  This could be a slip or meant on purpose. Ask the user before changing it. Never edit his files.

## Status / open
- **Playback and render: not built, and waiting on the user's go** (memory sound-and-music-plan: the Kursk demo comes
  first). Options when he says go: install abc2midi + fluidsynth, or write our own ABC-to-MIDI in the engine (our
  licence, our code). OPEN.
- **Procedural generator** (the user's "scripted generator"; 07 §2 PROPOSAL): the game state writes ABC text, so
  output can be read and edited. Fails when: adaptive music needs changes mid-bar that a whole-tune text can't
  express.
- **abccheck limits:** it ignores the key signature in ranges, skips `!...!` and `+...+` contents, and does not
  follow repeats (bars are counted as written). It doesn't know about voice overlay `&`.
  Fails when: a tune uses `&` overlays or multi-line `\` continuation inside a chord.

## Related skills
license-check (EasyABC is GPL; check any ABC tool before use), engine4x-design (07 Sound and Music: the music
engine plan), doc-capture (the user's theory lessons).
