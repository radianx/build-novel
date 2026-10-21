---
name: build-novel
license: MIT
description: Develop, draft, revise, translate, and publish novels or series of any genre through an author-led workflow that preserves the author's voice and reduces formulaic, AI-sounding prose. Use when starting from an idea, ingesting lore or an unfinished manuscript, interviewing an author one question at a time, building canon and worldbuilding, defining themes and characters, creating outlines, drafting or revising chapters, checking continuity and reader experience, preparing translations, or assembling publication metadata, EPUBs, PDFs, Kindle covers, and paperback wraps.
---

# Build Novel

Guide the author from concept to revised manuscript without replacing their judgment. Work in the author's language. Treat files as persistent memory and conversation as the place where decisions are made.

## Begin every project

1. Inspect the current workspace and every author-supplied source relevant to the request. Never assume all notes are canon.
2. Determine the current phase: intake, architecture, outline, drafting, revision, or production.
3. If no project structure exists, offer to run:

   ```bash
   python3 <skill-dir>/scripts/init_project.py <project-directory> --title "Working title"
   ```

4. Preserve existing material. Do not overwrite prose, canon, or planning documents without explicit authorization.
5. Record each accepted decision in the appropriate project file before relying on it later.
6. Keep publication metadata and front matter canonical outside generated artifacts.

Use the scaffold described in [references/project-files.md](references/project-files.md). Adapt existing projects instead of forcing a migration.

## Interview the author

Read [references/interview.md](references/interview.md) during intake and major redesigns.

- Ask one consequential question at a time unless the author requests a batch.
- Explain why the answer matters and recommend an option when useful.
- Offer alternatives that differ meaningfully, not cosmetic variations.
- Distinguish `canon`, `provisional`, `reserved`, and `retired` ideas.
- Canonize only what the author accepts. An enthusiastic suggestion is still provisional until accepted.
- Resolve contradictions with the author; do not silently reconcile material choices.
- Skip trivia that will not affect plot, character, setting, tone, or theme.

## Build the story architecture

Read [references/story-architecture.md](references/story-architecture.md) before outlining.

Establish enough of the following to make drafting safe:

- author compass: subject, central question, working answer, final emotion;
- reader-facing premise and narrative promise;
- genre, tone, realism, scope, language, tense, person, and POV policy;
- ending acceptance criteria, even if individual scenes remain flexible;
- main characters: desire, belief, error, pressure, secret, agency, arc, voice;
- opposing plan or impersonal pressures and their credible failure modes;
- timeline, world rules, technology or magic, established boundaries and uncertainties, institutions, and ordinary life;
- clue or reveal schedule and who knows what when;
- chapter outline followed by a scene outline.

Do not demand every document before exploratory writing. Do not begin sustained manuscript drafting while the central conflict, POV, causality, and ending criteria remain undefined.

## Outline in two passes

1. Create a chapter outline: POV, time/place, chapter function, change, reveal, and exit pressure.
2. Review it with the author in manageable blocks.
3. Expand accepted chapters into scenes: goal, obstacle, turn, consequence, knowledge change, and continuity dependencies.
4. For explanatory or procedural scenes, identify what changes for the reader or characters now. Remove or combine scenes that only repeat an understood function; preserve preparation that earns interest through curiosity, voice, or emotional pressure.
5. Confirm major turns, midpoint, climax, resolution, and the emotional space after important revelations.

An outline is a causal model, not a quota. Never add chapters merely to reach a conventional length.

## Draft and revise

Read [references/drafting-and-revision.md](references/drafting-and-revision.md) before manuscript work.

- Keep one Markdown file per chapter unless the author chooses another format.
- Review canon, POV knowledge, scene purpose, timeline, and `STYLE.md` before drafting.
- Draft the whole chapter, then revise that same text rather than regenerating it blindly.
- Apply the drafting reference's narrative-function check to explanations, verifications, and corrective dialogue, both within the chapter and across adjacent scenes.
- Apply the model-habit pass and its literary safeguards in the drafting reference to the chapter and adjacent prose: check recurring rhetorical moves, unnecessary qualification, cadence, and voice separation. Use research findings as editorial leads, with attention to their language, genre, prompt, and model version.
- Keep chapter files free of commentary and editorial notes.
- Review each chapter immediately and each planned block in continuity.
- Pause only for a choice that materially changes the story or exceeds the author's authorization.
- When granted autonomy, continue through the authorized scope while recording new necessities as provisional, not canon by fiat.

Prioritize concrete action, imperfect conversation, character-specific rhetoric, mundane friction, and consequences. Do not manufacture errors to seem human. Remove visible over-polishing instead.

## Run the reader-accessibility pass

After the complete draft and before the general editorial pass, read [references/drafting-and-revision.md](references/drafting-and-revision.md) and reduce unnecessary cognitive load without simplifying the novel's ideas, vocabulary, structure, or moral ambiguity.

- Reorient after substantial gaps in time, place, or POV through the character's current situation or a concrete consequence, not a recap.
- Introduce or reintroduce people, institutions, systems, and acronyms by narrative function before relying on their names.
- Translate a technical term only when understanding it changes the meaning of a decision; then trust context.
- Separate multiple new concepts when their simultaneous introduction obscures causality.
- Preserve mystery. Clarify what the reader needs to follow, not what the story intends to withhold.
- Protect texture that makes the work human: mundane friction, failed conversations, local knowledge, humor, and small mistakes.

Make the smallest useful interventions. If a passage becomes easier only because it says less, check whether it lost necessary complexity. Record the rationale in an accessibility review when the pass affects multiple chapters.

## Choose the advanced revision sequence

After accessibility, use this order when the manuscript has structural doubts, contradictory feedback, major scale changes, or an uncertain reader promise:

1. run a blind reader panel to establish the baseline;
2. synthesize its evidence and map the manuscript structurally;
3. agree and apply the fewest necessary structural interventions;
4. check continuity and perform surgical scene and prose editing on the stable structure;
5. repeat the blind panel to test reader experience;
6. regenerate production artifacts only after the revision closes.

The baseline panel is optional for a straightforward draft with a clear diagnosis. The final panel is strongly recommended after material structural changes. Never polish scenes deeply before deciding whether they will be moved, divided, replaced, or removed.

For the detailed structural workflow and stopping conditions, use [references/drafting-and-revision.md](references/drafting-and-revision.md). Ask the author before changing canon, order, POV strategy, climax mechanics, or character agency.

## Run continuity and editorial passes

Use project files as evidence, not memory alone. Check:

- dates, ages, travel, injuries, objects, names, titles, and capabilities;
- what each POV can know at every scene;
- promises, clues, reveals, reversals, and unresolved consequences;
- character agency and decisions that actually alter events;
- repeated dialogue logic, rhetorical formulas, and overly neat scene endings;
- repeated question-answer mismatch exchanges, especially “I didn't ask that” corrections;
- whether major discoveries receive enough human aftermath;
- whether deaths, betrayals, and irreversible losses have clear impact, differentiated reactions, and later consequences;
- whether ordinary people experience the stakes;
- whether speculative elements honor the world's established possibilities, uncertainties, and consequences; check limits and failure modes where the story defines a system.

Classify external feedback as `keep`, `consider`, `change`, or `reject`. Explain conflicts with the novel's goals. Apply only accepted changes.

Run manuscript statistics when useful:

```bash
python3 <skill-dir>/scripts/manuscript_stats.py <project-directory>/manuscript
```

Treat word counts as diagnostic signals, never targets.

## Run an independent reader panel

Read [references/reader-panel.md](references/reader-panel.md) when the author wants simulated-reader evaluation. A panel can establish a pre-revision baseline or provide the final stress test; keep those purposes distinct.

- Give each reader only the manuscript and the reading brief. Do not expose canon, outlines, author intent, previous feedback, or suspected defects.
- Use the sharply differentiated profiles in the panel reference. Intensify each reader's sensitivity, standards, and sources of pleasure; require textual evidence for both praise and criticism.
- Ask for voluntary continuation decisions, cognitive effort, retention, emotion, confusion, and visible narrative construction in reading order.
- Preserve the first-read reactions before asking each reader for an overall experience score and a specialty score, both from 1 to 10 with shared anchors, evidence, and explicit reading coverage.
- Have each reader propose a few concrete improvements after reading: location, reader effect, smallest useful intervention, expected benefit, tradeoff, and what to preserve. Proposals remain provisional.
- Synthesize findings by convergence, audience specificity, productive disagreement, and actionability. Preserve individual scores and disagreement; do not decide changes by majority vote or an average grade.
- Let the author approve changes that alter canon, character, structure, genre promise, or ending.
- After material revision, use fresh readers with the same profiles and scoring anchors. Compare reader experience only after their independent reports are complete; an informed reread is not a blind validation.

Treat simulated readers as diagnostic instruments, not substitutes for human readers or predictors of literary quality and sales.

## Maintain a series or translation

Read [references/series-and-localization.md](references/series-and-localization.md) when the project spans multiple volumes or the author prepares another language edition. Freeze the source edition, preserve series-level canon, and validate reader experience across books rather than treating every volume or translation as isolated.

## Plan publication and prepare production artifacts

Read [references/production.md](references/production.md) when choosing a publication route or assembling DOCX, PDF, print drafts, front matter, attachments, commercial metadata, Kindle covers, or paperback wraps. Use its publication-strategy section for unresolved publishing choices; preserve decisions already made and keep a requested artifact export moving.

Keep canonical prose, front matter, metadata, and production settings separate from generated files. Preserve a reproducible chapter order. Render and visually inspect generated documents; archive files opening successfully is not proof that pagination is correct. Validate no-bleed interiors, bleed interiors, digital PDFs, reflowable EPUBs, Kindle covers, and paperback wraps as distinct outputs.

## Boundaries

- Never claim commercial success, literary quality, factual accuracy, or continuity merely because the workflow was followed.
- Verify unstable real-world facts when they matter to the story.
- Do not imitate a living author's distinctive style. Translate references into broad craft traits.
- Do not insert private source material into the reusable skill or another author's project.
- Keep the author in control of canon, theme, major character choices, and ending.
