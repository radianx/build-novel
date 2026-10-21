# Project files

Use these files as persistent project memory. Existing projects may use different names; map functions rather than duplicating documents.

```text
novel/
├── METADATA.yaml
├── PRODUCTION.yaml
├── RELEASE_MANIFEST.md
├── FRONT_MATTER.md
├── AUTHOR_COMPASS.md
├── CANON.md
├── CHARACTERS.md
├── TIMELINE.md
├── WORLD.md
├── STORY_ENGINE.md
├── REVEALS.md
├── OUTLINE.md
├── SCENE_OUTLINE.md
├── STYLE.md
├── WORKFLOW.md
├── DECISIONS.md
├── manuscript/
├── research/
├── feedback/
├── production/
└── archive/
```

## Authority

Use this default order when sources conflict:

1. The author's latest explicit decision.
2. `CANON.md` and dated entries in `DECISIONS.md`.
3. Accepted story architecture and outlines.
4. The current manuscript.
5. Imported lore and exploratory notes.
6. Suggestions that were never accepted.

Do not treat newer file timestamps as narrative authority by themselves.

## Status vocabulary

- **Canon:** binding unless the author changes it.
- **Provisional:** useful working assumption awaiting confirmation.
- **Reserved:** intentionally deferred for a later part or book.
- **Retired:** no longer active; retain only when its history prevents confusion.
- **Unknown:** a real gap, not permission to invent.

## Update discipline

- Record an accepted fact once in its authoritative file; link or summarize elsewhere.
- Add a dated decision entry when a choice replaces prior canon or affects several documents.
- Update dependent files in the same work session.
- Preserve rejected alternatives only when they may otherwise be reintroduced accidentally.
- Before writing a scene, load only the relevant character, timeline, world, reveal, and style sections.
- Keep title, author, language, series position, rights, and identifiers in `METADATA.yaml`. Never invent an ISBN, publisher, or rights holder.
- Keep trim, bleed, paper, ink, cover finish, marketplace, and artifact settings in `PRODUCTION.yaml`; these are edition-specific and must not be inferred from old exports.
- Freeze each distributable edition in `RELEASE_MANIFEST.md` with its source revision, locale, settings, page count, artifact names, and checksums.
- Keep dedication, epigraph, and other front matter in `FRONT_MATTER.md`. Do not make a generated DOCX the only source of final wording.
