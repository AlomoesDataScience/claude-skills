---
name: doc-standards
description: "Documentation standards for this workspace: progressive disclosure, Diataxis kinds, one fact in one place, dates and sources, lifecycle labels, decision records, size budgets, with the docs.py checker. Use when writing or tidying any document."
keywords: "documentation, docs, standards, document management, writing docs, budget, size, lifecycle, status label, superseded, archive, decision record, adr, single source of truth, diataxis, tutorial, how-to, reference, explanation, naming, memory index, check docs"
---

# Doc standards - how documents are kept here

The user's proposal (2026-11-09): "documentation for documentation standards I should get or develop and adopt".
Source: `Proposals/Context cost review.md` section 4. The point: an AI re-reads documents constantly, so
small, layered, single-source documents cost less context and go stale less.

## The rules
1. **Progressive disclosure** - three layers: an always-loaded *index* (MEMORY.md, the skill listing,
   `.claude/skills/INDEX.md`: one short line each) -> a *file* opened when the task needs it -> a *section*
   read with offset/grep. Nothing big lives in an always-loaded layer.
2. **One kind per document (Diataxis)**: tutorial (learning by doing), how-to (steps for one task), reference
   (facts to look up), explanation (why). A SKILL.md is a short how-to; reference goes in `reference/` files.
3. **One fact in one place**; everywhere else links to it. Before writing, search (`checkskills.py`, grep).
4. **Every fact carries its date and source**: "the user, 2026-11-03", "manual p.45", "game screen".
5. **Lifecycle label** under the title: `Status: draft | active | open | waiting | done | superseded | archived`.
   Superseded files move to `Archive/` with a pointer line left behind; never silently deleted.
6. **Decision records**: one short file per real decision - `docs.py adr "TITLE"` -> `Decisions/NNNN-*.md`
   (context, decision, consequences, sources). Keeps "why did we do that" out of memory and chat.
7. **Hand-off per task** (unload skill) - the bridge across clears.
8. **Naming**: dated names for logs and one-off docs (`2026-11-09-topic.md`), stable names for living docs;
   placement follows library-intake.
9. **Docs as code**: skills live in git (skills-manager export), small reviewable changes.

## Budgets (checked by `docs.py check`)
| What | Budget | Over budget -> |
|---|---|---|
| SKILL.md | 150 lines | `skills.py split NAME` |
| Skill description | 40 words (+ `keywords:`) | trim; trigger words to keywords |
| MEMORY.md | 40 lines, 150 chars each | merge memory files, shorten lines |
| Plan, proposal, checklist | 400 lines | split, archive done parts |

## Tools (`scripts/docs.py`, from the workspace root)
```
docs.py check [PATH...] [--all]    budgets, labels, dates, memory links; exit 1 on errors
docs.py label FILE STATUS          set the Status line
docs.py adr "TITLE"                new decision record
```
Run `check` after any documentation sweep and at the end of a task that wrote documents.

## Related skills
skills-manager (split, index), write-skill, unload, archive-curator, cleanup, library-intake, planning.
