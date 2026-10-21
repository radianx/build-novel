# Series and localization

## Series continuity

Maintain a series-level canon for facts that cross books. Record each volume's time span, inherited consequences, returning characters, unresolved promises, thematic question, and ending state.

Before closing a later volume:

1. read the books in publication order without planning documents;
2. check continuity, escalation, repeated scene engines, assumed knowledge, and whether each volume has its own narrative promise;
3. distinguish intentional echoes from accidental repetition;
4. verify that a revision to an earlier volume does not invalidate later books;
5. run a final series panel when the author wants a whole-saga stress test.

A series panel evaluates cumulative experience, not merely each manuscript's individual quality. Do not expose future canon to a reader assigned only an earlier volume.

## Translation preparation

Freeze the approved source edition before sustained translation. Create:

```text
translations/<locale>/
├── SOURCE_MANIFEST.md
├── TRANSLATION_BIBLE.md
├── glossary.csv
├── decisions.md
├── issues.md
└── books/<volume>/
    ├── manuscript/
    ├── block-reviews/
    └── production/
```

- `SOURCE_MANIFEST.md`: source commit, files, chapter order, attachments, front matter, and edition date.
- `TRANSLATION_BIBLE.md`: voice, register, punctuation, dialogue, names, units, and locale policy.
- `glossary.csv`: recurring terms, official renderings, context, and forbidden alternatives.
- `decisions.md`: accepted departures that affect later chapters or books.
- `issues.md`: unresolved ambiguities and source defects; do not silently repair them in translation.

Translate chapter by chapter, revise the same text, then review in blocks. Check voice and terminology across the full series before production. Use an independent target-language reader panel after the translation is stable; literal fidelity is not proof of equivalent reader experience.

Treat each language edition as a separate publication record. Preserve the relationship to the same narrative series while maintaining locale-specific title, subtitle, description, series description, categories, search phrases, cover copy, identifiers, and production artifacts. Do not reuse an ISBN or platform identifier unless the platform and identifier rules explicitly allow it.

Before release, compare source and translation manifests rather than file timestamps. Record which frozen source edition the translation represents and whether later source corrections were ported, deliberately omitted, or reserved for a new edition.
