# Production

## Source and output separation

Keep Markdown or the author's chosen editable format canonical. Put generated DOCX, PDF, EPUB, cover proofs, and printer packages under `production/`. Do not copy-edit only the generated file and leave the source stale.

Read `METADATA.yaml`, `PRODUCTION.yaml`, and `FRONT_MATTER.md` before assembly. Propagate the same title, author, language, series name and position, rights, description, and supplied identifiers to every format. Never invent missing publication metadata or infer current production settings from an older PDF.

## Assembly order

Record an explicit sequence containing:

- title page;
- copyright or edition notice;
- optional dedication and epigraph;
- parts, chapters, interludes, and attachments;
- acknowledgements or other back matter.

Never infer attachment placement from filenames alone when the story specifies positions.

## Output profiles

Treat these as different products:

- **Print interior DOCX/PDF:** normally excludes the cover wrap. Respect trim, margins, recto/verso openings, and intentional blank pages.
- **Digital PDF:** may include the front cover and a courtesy page. Preserve interior parity when a right- or left-hand reveal matters. Export headings as bookmarks and use a tagged PDF when supported.
- **Reflowable EPUB:** include the cover in metadata and reading order, a navigable table of contents, semantic headings, language, series metadata, and alternative text. Do not simulate print parity with blank XHTML pages; start a visual reveal in its own document instead.
- **Paperback cover wrap:** one page containing back cover, spine, and front cover plus the printer's required bleed. Build it only after the final interior page count and paper stock are known.
- **Kindle marketing cover:** a separate portrait image in sRGB. Do not reuse a CMYK print export; dark or black thumbnails can result even when the source appears correct locally.

Keep diagrams as accessible text when their design is not essential. When the image itself matters, provide alternative text that conveys its narrative information. Alternative text is metadata and should not appear on the printed page.

## Validation

After generating an artifact:

1. Confirm the archive or file format opens.
2. Render it with the target layout engine when available.
3. Verify page size, page count, chapter count, and ordering.
4. Inspect title, front matter, part openings, attachments, chapter transitions, final pages, headers, footers, and page numbers.
5. Check blank pages, clipped objects, doubled margins, orphaned headings, font substitution, and image resolution.
6. Verify title, author, language, series, rights, identifiers, and keywords against `METADATA.yaml`.
7. Search extracted text for draft labels, placeholders, unresolved notes, and accidentally repeated front matter.
8. Confirm bookmarks or EPUB navigation, internal resources, alternative text, and the intended final page or section.

An internally valid DOCX can still paginate incorrectly. Visual rendering is required before calling a print draft complete.

For EPUB, verify that `mimetype` is the first uncompressed ZIP entry, the package and XHTML parse, referenced resources exist, and the spine and navigation match the assembly order. Run EPUBCheck when available.

Use the bundled validator for deterministic checks:

```bash
python3 <skill-dir>/scripts/validate_publication.py production/book.epub
python3 <skill-dir>/scripts/validate_publication.py production/book_digital.pdf --profile digital
python3 <skill-dir>/scripts/validate_publication.py production/book_print.pdf --profile print-bleed --trim 6x9 --require-final-recto
python3 <skill-dir>/scripts/validate_publication.py production/cover.pdf --profile cover-wrap --trim 6x9 --pages 262 --paper groundwood
python3 <skill-dir>/scripts/validate_publication.py production/kindle.jpg --profile kindle-cover
```

The validator complements visual inspection; it cannot judge page design, cropping, meaningful image descriptions, or whether an intentional blank page falls on the correct side.

## Covers

Judge a front cover at full size and thumbnail size. Check title hierarchy, author name, series identity, genre signal, canon implications, and visual continuity across a series. Before printing, obtain the printer's trim, bleed, spine, color, and resolution specifications; a front-cover concept is not a press-ready wrap.

For a KDP-style paperback wrap, verify current printer documentation before use. The commonly published calculation is:

```text
spine = even page count × paper multiplier
wrap width = back trim width + spine + front trim width + 0.25 inches
wrap height = trim height + 0.25 inches
```

Common black-ink multipliers are white `0.002252`, cream `0.0025`, and groundwood `0.00235` inches per page. Round an odd interior count up to an even count before calculating the cover. The bundled helper composes predesigned front and back panels and optional spine text:

```bash
python3 <skill-dir>/scripts/build_kdp_cover.py \
  --front front.png --back back.png --pages 261 --paper groundwood \
  --spine-text "TITLE • SERIES • AUTHOR" --output production/cover.pdf
```

Keep text at least 0.0625 inches from either spine fold and reserve the printer's barcode area on the back. Matte versus glossy changes the physical finish, not wrap dimensions.

## Bleed interiors

When any interior element reaches a trimmed edge, use the printer's bleed profile for every page, not only the illustrated page. For a 6 × 9 inch KDP interior, pages are normally 6.125 × 9.25 inches: 0.125 inches at the outside edge and at both top and bottom edges, with no added bleed at the binding edge. Preserve the ordinary text box inside the 6 × 9 trim area. If a final image must occupy a full recto, verify both full-page coverage and odd page parity after rendering.

Do not confuse interior bleed selection with cover bleed: a print cover wrap always includes its own exterior bleed.

## Commercial metadata

Before publishing, confirm title, subtitle, description, series description, categories, search phrases, language, marketplace, and edition identity against the actual platform form. Treat category names and eligibility as unstable marketplace data rather than permanent skill knowledge. Keep search phrases useful and distinct; do not fill slots with repeated title words merely because a form allows them.

Each language edition needs its own localized metadata and publication record even when it belongs to the same narrative series.

## Release freeze

After visual approval, update `RELEASE_MANIFEST.md` with the source revision, locale, trim, bleed, paper, finish, page count, artifact filenames, and SHA-256 checksums. Record which files were actually uploaded. Do not call an edition frozen while the release manifest points to superseded or unverified artifacts.

## Distribution hygiene

Exclude temporary lock files, private research, reader contact information, obsolete exports, and version ZIPs unless explicitly requested. Keep a reversible archive before destructive production edits.

Close the layout application before external DOCX edits. A valid lock file or an unsaved GUI session can overwrite metadata changes or make a headless render use stale content. Reopen and re-render after external modification.

Keep print interiors, bleed variants, cover wraps, Kindle covers, and shareable digital PDFs under distinct names. Before release, inspect repository status so obsolete covers, intermediate images, temporary ZIPs, and superseded exports are not distributed accidentally.
