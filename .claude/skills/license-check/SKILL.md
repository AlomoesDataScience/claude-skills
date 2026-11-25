---
name: license-check
description: "Check the licence of any code, library, asset or tool before we use or ship it, keep a THIRD-PARTY-NOTICES register, ship notices in builds, with licensecheck.py. Use before pulling outside code or assets and before any release."
keywords: "license, licence, licensing, MIT, GPL, LGPL, BSD, Apache, zlib, MPL, creative commons, CC-BY, open source, attribution, notices, third party, THIRD-PARTY-NOTICES, copyleft, nuget licences, github licence, release, itch.io, engine-sim, ABC music, respect the license, licensecheck.py"
---

# License check - respect every licence, before use and in every build

**Origin (rule):** the user, 2026-11-16: "Make sure we are not breaking the liscense by using it here. We need to
respect the liscense." ... "Also write a liscense check skill". The first use was engine-sim for our sound
(4X Build Proposal 07). That check also found that our own GalaxyViewer releases v0.2.0-v0.2.3 shipped MIT and
Zlib libraries with no notices.

## When
- Before any outside code, library, data set, font, image, sound or music enters a project. This covers ports,
  copies and "just reading it to learn" (see 4).
- Before every release build. A release ships its notices or it doesn't ship.
- When the user drops source he didn't write (Needs Review inbox, ABC music maker and so on).

## The method
1. **Find the real source.** A download page or an org page is often not the code. engine-sim's
   community-edition repo holds only a binary, and the MIT code is the author's older repo. Read the README for
   "open source", "license" and links.
2. **Read the licence**, without guessing from memory. Use the licence file, its exact text, and every bundled
   or submodule piece.
   - Remote, on GitHub: `scripts/licensecheck.py github OWNER/REPO`. That is one call for the licence, one for
     .gitmodules, and one per submodule. site-rules says the GitHub API is allowed, at 60 requests an hour.
   - Local: `scripts/licensecheck.py scan DIR` lists every licence file and SPDX tag, names them, and flags
     folders with code but no licence of their own.
   - .NET: `scripts/licensecheck.py nuget PROJECT_DIR` reads the packages' licences from the local cache. Then
     scan the build output, because transitive natives come too.
3. **Judge with the table below.** Unclear, STOP, or a mix of licences: ask the user. He rules, and the ruling
   goes in the register.
4. **No licence = all rights reserved.** We may read it but not copy, port or ship it. For our own folk's code
   (the user, friends), the owner states the terms in writing first.
5. **Register it** in the project's `THIRD-PARTY-NOTICES.md`: component, version or commit, licence,
   copyright holder, the text file in `licenses/`, and the notes. Use "Planned" rows for what isn't used yet.
6. **Ship it.** Each build archive carries `THIRD-PARTY-NOTICES.md` and `licenses/`. Ported or copied source
   files get a header naming the origin file, the commit and the licence.
7. **Respect the author's wishes beyond the law** when they state them (credit, no passing their work off as
   ours, no use of their name as our product's). Do it as a courtesy, and write it in the register's notes.

## What each licence asks of a binary release (itch.io, GitHub)

| Licence | Use? | We must |
|---|---|---|
| MIT, ISC, BSD-2, MS-PL | yes | ship the copyright + licence text |
| BSD-3 | yes | the same, and not use their names to endorse ours |
| Zlib, BSL-1.0 | yes | mark changed source; a notice in binaries isn't required but we ship it anyway |
| Apache-2.0 | yes | ship LICENSE + their NOTICE file, and mark changed files |
| CC0, Unlicense | yes | nothing (credit anyway) |
| CC-BY | yes, for assets | credit author, title, licence and link visibly |
| MPL-2.0 | with care | MPL files we change stay MPL and their source is offered; the rest of the game is unaffected |
| LGPL | with care | link dynamically only, the user can swap the library, and its source is offered. Ask the user |
| GPL, AGPL | STOP | the whole game would have to be GPL. The user decides |
| CC-BY-SA | ask the user | derived assets share alike |
| CC-BY-NC, ND, "non-commercial", "personal use" | STOP | itch.io sales are commercial; ND forbids changes |
| none / custom | STOP | all rights reserved until the owner says otherwise |

This is a working guide, not legal advice. Anything with money or doubt goes to the user.

## Per project
- **4X engine:** register at `Projects/Our Games/4x Game Engine/THIRD-PARTY-NOTICES.md` and texts in `licenses/`.
  The build ships both (engine4x-dev release step). Planned: engine-sim (MIT) and the ABC music maker (not checked yet).

## Fails when
- A transitive dependency (a native library inside a single-file build) is missed. Scan the output, not only
  the project file.
- A file's own header says something different from the repo's root LICENSE. The API only reads the root;
  scan the cloned tree.
- A licence changes between versions (engine-sim went closed after v0.1.11a). Pin the version or commit we use.

## Related skills
site-rules (rules for each host before any call), wiki-scout (text sources, cite and use our own words),
engine4x-dev (the release step ships the notices), review-inbox memory (identify drops; check their licence),
library-intake (filing), abc-notation (EasyABC is GPL: read only)
