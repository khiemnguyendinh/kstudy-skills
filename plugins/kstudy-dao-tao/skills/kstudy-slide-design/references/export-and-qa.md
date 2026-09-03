# Export And QA

## When To Read

Read this file when:

- exporting a Kstudy HTML deck to PDF
- fixing title/logo/footer overlap
- checking fullscreen presentation controls
- validating screenshots, cards, or tables inside the slide safe area

## HTML Deck Implementation Rules

- Build slides for `1920x1080`.
- Confirm the HTML includes the deck runtime script before debugging layout or exporting:
  - `deck-stage.js` must be copied into the deck folder
  - the HTML must include `<script src="deck-stage.js"></script>` before `</body>`
- Keep a reserved safe area on every slide:
  - top: `160px`
  - bottom: `110px`
  - left/right: `96px`
- Implement the content frame with CSS variables when possible:
  - `--safe-top`
  - `--safe-right`
  - `--safe-bottom`
  - `--safe-left`
- Apply those variables to:
  - slide padding
  - logo/header position
  - footer position
  - speaker notes position
- On mobile preview, reduce the safe area proportionally, but keep header/footer protected.

## Overlap Prevention Checklist

- Title does not enter the logo band.
- First content block starts below the header.
- Footer line and page number stay clear of notes and body content.
- Tables do not grow into footer space.
- Screenshot frames fit inside the content frame.
- Decorative background graphics remain behind content and never force layout collisions.
- Napkin diagrams use a local approved asset, remain transparent unless a background is intentional, and do not sit on an accidental white plate/card.
- Napkin labels remain readable at thumbnail size; line colors follow the Kstudy palette and do not disappear into grid/dot textures.
- For dense slides, check the distance between the lowest content block and the footer band explicitly. If that distance is visually weak, rebuild the layout.

## Screenshot QA Rules

- Do not trust repeated screenshots that only change `#slide-number` inside the same page session. `deck-stage` restores the hash on load and can hold a stale slide when the page stays alive.
- For screenshot QA, use one of these patterns:
  1. navigate with a unique query string per slide, then include the hash, or
  2. create a fresh page/session per slide.
- Save targeted screenshots for every dense or previously broken slide, not just a contact sheet.
- If a slide breaks repeatedly after spacing tweaks, stop compressing and redesign the slide structure.

## Fullscreen And Controller Rules

- Put presentation controls at the bottom while presenting.
- Keep controller chrome outside the slide content area.
- Use calm transitions only: fade or gentle directional movement.

## PDF Export Workflow

Default presentation export:

1. Export from Chrome headless or `window.print()` with print CSS tuned for `16:9`.
2. Hide toolbar in print media.
3. Make each slide print as one page.
4. Use `-webkit-print-color-adjust: exact`, `print-color-adjust: exact`, and an sRGB browser color profile.
5. Keep text, tables, diagrams, and CSS backgrounds as vector output whenever possible.
6. After export, verify page count and remove blank pages if the browser adds them.
7. Reject the PDF if font metrics, opacity, background pattern scale, or shadows differ materially from the HTML render.
8. Save exactly one user-facing PDF by default: `<CODE>-B<N>-Slides.pdf`.

Raster fallback:

- Do not use raster PDF by default. Use it only when the user explicitly accepts the trade-off.
- State the trade-off before using raster: heavier file, less editable/reusable text, and possible image softness on zoom.
- Do not create separate `print`, `vector-safe`, or `raster` PDF variants unless explicitly requested.

Texture/color safety for vector PDF:

- Avoid masked transparent texture layers in print media because some PDF viewers can reinterpret blue textures as pink/magenta.
- In `@media print`, replace masked dot/grid/circle textures with explicit CSS gradients or flat vector-safe fills.
- Keep `print-color-adjust: exact` and check the exported PDF against the HTML render before handoff.

## Canva Import Policy

- Do not treat Canva as the canonical format for Kstudy HTML decks.
- Canva HTML import may preserve the first-page visual but often imports the deck as one page and may not load local assets.
- Canva PDF import may break fonts, layout, opacity, and drop shadows.
- If Canva cannot preserve quality and structure, skip Canva import and state that HTML is the canonical source.
- If the user still needs Canva, import raster slide images or a raster PDF only as a flat presentation. Warn that it is for viewing/presenting, not high-fidelity editable reconstruction.

## Verification

- Confirm Vietnamese diacritics render correctly.
- Confirm `32`-page decks remain `32` pages after filtering blank pages.
- Confirm white logo is used on dark slides and color logo on light slides.
- Confirm no text overlaps header/footer at full slide size.
- Confirm dense slides individually, not only through the contact sheet.
- Confirm background textures match the HTML render: no enlarged grid/dot/circle pattern after export.
- Confirm opacity, gradients, and drop shadows survive export visually; if not, use raster screenshot PDF.
- Confirm Napkin SVG/PNG transparency, palette, Vietnamese labels, and attribution/watermark state match the approved HTML slide.
