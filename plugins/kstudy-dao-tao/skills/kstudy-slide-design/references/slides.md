# Kstudy Slide Deck Rules

Use for presentation decks, lesson materials, VSL decks, workshop slides, and executive education materials.

## Template

Copy these files into the output/project folder:

- `assets/templates/slides/index.html`
- `assets/templates/slides/slides.css`
- `assets/templates/slides/deck-stage.js`
- `assets/templates/slides/image-slot.js`
- Needed logos from `assets/brand/`
- Needed photos from `assets/photos/`

The source template is tuned for `1920x1080` decks.

## Structure

- Header: Kstudy logo.
- Footer: page number, `Hoc vien Kstudy`, and `www.kstudy.edu.vn` when suitable.
- Safe area is mandatory: reserve a dedicated header band and footer band on every slide.
- No title, body copy, cards, tables, screenshots, notes, or decorative visuals may overlap the header/logo area or footer area.
- For `1920x1080` decks, reserve at least:
  - top safe area: `160px`
  - bottom safe area: `110px`
  - left/right safe area: `96px`
- For dense lesson slides, start from a stricter content frame unless there is a reason not to:
  - top content start: `184-200px`
  - bottom content end: at least `24px` above the footer band
- Place all main slide content inside an inner content frame that starts below the header and ends above the footer.
- Use alternating light/dark sections for longer decks.
- Keep one clear message per slide.
- Avoid dense text. Prefer short heading, 2-4 support points, and one strong visual.
- For decks with 12+ slides, vary background texture deliberately. Use at least four of the canonical styles from `references/tokens.md`: Circles · light, Circles · bright blue, Circles · brand, Grid · bright blue, Dots · light, Dots · dark, White solid.
- Do not create a Kstudy deck that only uses `Grid · bright blue` and `White solid`; it reads repetitive and underuses the design system.
- Ordinary slide titles should stay around 48 characters or 9 words. Cover/section titles may reach 60 characters or 11 words. Shorten title copy before reducing font size.
- If an upstream lesson outline has a long title, preserve the learning intent but rewrite the visible title for slide fit; move the nuance into body copy or speaker notes.
- Start from learning objective and storyline before designing slide visuals. The deck flow should be: objective -> storyline -> slide structure -> visual plan -> brand design -> HTML build -> QA/export.

## Dense Slide Rules

- Treat these as high-risk layouts: long titles, phone/mockup frames, 2-column case-study proofs, checklist boards, 4-card matrices, workflow strips near the footer, and closing slides with both photo and gate card.
- On these slides, preserve the footer band first. Do not let page number or website line share space with any card, note, or decorative shape.
- If a slide still feels crowded after one reasonable pass of copy tightening and spacing reduction, rebuild the visual structure instead of continuing to shrink type.
- Prefer lower, wider boards over tall device mockups when the slide also needs a large title and 2-3 explanatory cards.
- For proof/case-study slides, shorten the visible title before shrinking the entire column.
- For checklist/table slides, reduce row height and panel padding before reducing font size below the normal reading range.

## Slide Types To Reuse

- Cover: big promise/title, Kstudy logo, gradient circle or real photo.
- Section divider: dark navy, large section number/title.
- Problem/insight: one sharp statement plus evidence or implications.
- Framework: 3-5 step system, cards, or timeline.
- Case study: context, action, result, learning.
- Workflow/SOP: trigger, action, output, error handling.
- Comparison: two-column table with clear recommendation.
- Quote/stat: Rokkitt accent for stat or pull quote.
- Closing/CTA: next action, QR/link/contact when provided.

## Visual Rules

- Use navy or near-white as the main base.
- Use bright blue for primary action and visual direction.
- Use yellow once per slide for attention, not as a large background.
- Do not use visuals only for decoration. Every photo, diagram, chart, screenshot, icon, or illustration must clarify the slide's message.
- Every slide must have a clear visual job. Use a real photo, diagram, chart, table, comparison, timeline, workflow, icon system, screenshot placeholder, or deliberate key visual. Text-only slides are allowed only for intentional section dividers or very short quote/stat moments.
- In lesson decks, prefer diagrams for concepts, workflows for procedures, tables/matrices for comparison, screenshots for software demos, and real Kstudy photos for classroom/practice proof.
- Use real people images when explaining learners, classes, instructors, or outcomes.
- Read `assets/photos/manifest.md` and `references/visual-sourcing.md` before choosing visuals for a deck.
- Use real Kstudy photos for proof about Kstudy classes, learners, mentors, workshops, testimonials, events, or outcomes.
- Use public photos only for social/professional context, public references, platform examples, industry examples, or non-Kstudy context. Keep source URLs and rights notes in the visual plan or project notes.
- Use diagrams, charts, matrices, timelines, or screenshots when they explain workflows, data, decisions, or software better than a photo.
- Use Napkin AI for compact concept structures when it accelerates the visual plan. Follow `references/napkin-ai.md`, normalize to Kstudy design-system colors, and place transparent output directly on the slide surface.
- Use screenshots with annotations for tool lessons and software walkthroughs. Keep UI current and avoid fake real-world states.
- Use generated/Canva/internet visuals only for conceptual or non-evidence imagery; never fake Kstudy classrooms, testimonials, or events.
- Use grid/dot textures lightly. They should support hierarchy, not compete with content.
- Use icons sparingly and consistently, preferably Lucide outline icons.

## Background Texture Rotation

Use this practical rotation for 20-slide lesson decks unless the content suggests a better rhythm:

- Cover/major section/closing: `bg-circles-brand` or `bg-dots-dark`.
- Questions, frameworks, mental models: `bg-circles-light`.
- Demo/practice transition: `bg-circles-bright` or `bg-grid-blue`.
- Checklists, tables, practice gates: `bg-dots-light`.
- Dense comparison tables or real screenshots: `White solid`.

Before final QA, scan the deck as a contact sheet. If two adjacent slides have the same texture without a learning reason, change one. If more than half the deck uses one texture family, rebalance.

## Visual Planning Pattern

For decks with more than 3 visual slides, create a visual plan before implementing slides:

| Slide | Message | Visual type | Source | Asset/file | Crop/layout | Rights/notes |
|---|---|---|---|---|---|---|

Use the plan to prevent repeated imagery, weak decoration, unsourced public photos, fake proof, and mismatched visuals.

A practical rule for Kstudy decks:

- Proof: real Kstudy photo or approved user-supplied photo.
- Thinking: diagram, framework, matrix, timeline, or concept map.
- Doing: screenshot, annotated UI, workflow, or step-by-step SOP.
- Evidence: sourced chart, metric card, benchmark, or timeline.
- Context: public photo, official screenshot, public source, or restrained generated concept visual.

## Copy Rules

- Vietnamese-first, direct, practical.
- Every slide should answer: why this matters, what to do, or what the learner gets.
- Do not make up proof numbers. Mark placeholders clearly if data is missing.
- Avoid decorative slogans without learning value.

## Verification

- Check readability at full slide and thumbnail size.
- Confirm Vietnamese diacritics render correctly.
- Confirm logo contrast: white logo on dark, color logo on light.
- Confirm the content frame stays inside the safe area on every slide type.
- Confirm no text overlaps visual assets at 1920x1080.
