---
name: kstudy-slide-design
description: Primary Kstudy Academy HTML slide deck skill for designing, reviewing, or exporting 1920x1080 branded slides from briefs, lesson slide outlines, or existing decks. Handles Kstudy slide storyline, visual planning, authentic photos, branded Napkin AI diagrams, charts, screenshots, generated illustrations, safe-area QA, HTML presentation controls, and PDF export. Use for Kstudy slides, lesson decks, workshop decks, executive education materials, slide branding, Napkin AI visual generation, choosing slide images, visualizing slide content, or PDF export. Do not invoke kstudy-design-system separately for normal slide production.
---

# Kstudy Slide Design

Use this skill for Kstudy-branded slide decks only. It packages the current Kstudy design system, real logo assets, slide template files, safe-area rules, and the PDF/export checklist used in production decks. This is the primary production skill for Kstudy slides; `kstudy-design-system` is a foundational reference/asset skill, not a separate slide-production skill unless the user explicitly asks to inspect or change the design system itself.

## Workflow

1. Read [references/brand-guidelines.md](references/brand-guidelines.md) for brand voice, logo usage, imagery, and positioning.
2. Read [references/tokens.md](references/tokens.md) for color, typography, spacing, radii, and motion tokens.
3. If the input is a lesson slide outline from `kstudy-lesson-plan-creator`, read [references/lesson-outline-input.md](references/lesson-outline-input.md) before designing. Treat the outline as learning intent and visual brief, not as final copy/layout.
4. Define the deck objective and storyline before designing visuals: who the learner is, what they should understand or do, and the one clear message for each slide.
5. Read [references/visual-sourcing.md](references/visual-sourcing.md) and [assets/photos/manifest.md](assets/photos/manifest.md) before choosing real Kstudy photos, public photos, diagrams, charts, screenshots, generated images, Canva visuals, or internet images.
6. For decks with more than 3 visual slides, create a visual plan that maps every slide message to its visual type, source, asset file, crop/layout, and connector/tool needed if local assets are insufficient.
7. Apply the visual completeness gate before building: every slide must have a resolved visual source, or be deliberately converted to a diagram/chart/workflow/mockup/key visual that can be created inside the HTML deck.
8. When a slide needs a concept map, hierarchy, process, causal chain, or framework that Napkin AI can express clearly, read [references/napkin-ai.md](references/napkin-ai.md). Use self-created HTML instead when exact geometry, data accuracy, editability, or custom interaction matters more.
9. Read [references/slides.md](references/slides.md) for Kstudy slide structure, safe-area rules, and 1920x1080 deck conventions.
10. Read [references/export-and-qa.md](references/export-and-qa.md) when exporting HTML slides to PDF or checking overlap/layout bugs.
11. Copy needed assets from `assets/` into the target project. Do not point production HTML at files inside this skill folder or hotlink Drive/web assets in production decks.
12. Before final export, confirm the deck runtime is wired correctly: the deck must include `deck-stage.js`, and QA must be run against the actual slide states, not a stale hash-cached render.

## What This Skill Standardizes

- Kstudy slide branding: logo variants, navy/blue/yellow/cyan palette, Google Sans Flex, and Rokkitt accent.
- Header/footer chrome: real Kstudy logo, footer text, website line, and page numbering.
- Safe area discipline: header and footer are reserved bands; content must not overlap them.
- Dense-slide rescue discipline: if a slide still collides with the header/footer after one compression pass, rebuild the layout instead of continuing to shrink text and cards.
- Visual planning discipline: learning objective -> storyline -> slide structure -> visual plan -> brand design -> HTML build -> QA/export.
- Lesson outline consumption: shorten long titles, preserve learning intent, choose one visual job per slide, and convert `Minh họa` briefs into concrete Kstudy-proof photos, diagrams, charts, screenshots, or concept visuals.
- Background texture discipline: use the full Kstudy texture system instead of repeating only grid-blue and white-solid slides.
- Visual selection discipline: real Kstudy photos for proof, diagrams for thinking, screenshots for doing, charts for evidence, and generated/Canva/internet visuals only when appropriate and clearly non-evidence.
- Napkin AI discipline: concise diagram briefs, transparent output, Kstudy design-system palette normalization, warning inspection, credit-aware caching, and slide-level visual QA.
- Conditional connector discipline: local-first, but call the right connector/tool when the visual plan cannot be completed from local assets.
- Public image sourcing discipline: use public images only for social/professional context, platform screenshots, industry examples, or non-Kstudy references; keep source URLs and license notes.
- HTML presentation behavior: fullscreen button, controller placement, print-to-PDF support, and motion that stays calm.
- Visual QA: readability, Vietnamese diacritics, logo contrast, text density, and screenshot/image fitting.
- Default delivery: exactly one user-facing presentation PDF named `<CODE>-B<N>-Slides.pdf`. Do not create separate print, vector-safe, or raster variants unless the user explicitly asks for them.

## Assets

- `assets/brand/`: official Kstudy logos and icons for light/dark slides.
- `assets/photos/`: authentic Kstudy classroom/team/event imagery plus `manifest.md` for matching images to slide context.
- `assets/templates/colors_and_type.css`: canonical brand token CSS.
- `assets/templates/slides/`: HTML deck template, runtime, and image helpers.
- `scripts/napkin_generate.py`: credit-aware Napkin API generation and immediate download.
- `scripts/normalize_napkin_brand.py`: Kstudy/Phoenix SVG or PNG palette normalization.

## Non-Negotiables

- Use the current Kstudy system: navy `#1D237D`, blue `#247DF9`, yellow `#FFD84D`, cyan `#0198CF`.
- Use `kstudy-logo-full.png` on light backgrounds and `kstudy-logo-white.png` on dark backgrounds.
- Reserve safe area for header/footer on every slide. No title, table, screenshot, note, or card may overlap logo or footer.
- Do not trust a “probably fine” dense slide. Slides with long titles, 2-column proofs, checklist boards, mock phone/UI frames, or closing gates must be rendered and checked individually before export.
- Prefer one clear message per slide. Reduce text before shrinking type.
- For decks with 12+ slides, use at least four canonical background textures: Circles · light, Circles · bright blue, Circles · brand, Grid · bright blue, Dots · light, Dots · dark, White solid.
- Every slide needs a visual job: real photo, diagram, chart/table, comparison, workflow, timeline, screenshot/mockup, icon system, or intentional key visual. Avoid text-only content slides.
- Treat Napkin AI output as concept illustration, not evidence. Never use it to fabricate Kstudy proof, data, software state, testimonials, or outcomes.
- For Napkin diagrams, request a transparent background and prefer SVG. Integrate the visual directly over the slide background without a default white plate, border, card, or shadow.
- Do not assume `style_id` was applied. Inspect API warnings; on `invalid_style_id`, use an approved custom Kstudy brand ID or normalize the generated SVG/PNG to navy `#1D237D`, bright blue `#247DF9`, cyan `#0198CF`, and yellow `#FFD84D` before use.
- Cache approved Napkin assets in the deck project and reuse them. Do not spend credits regenerating an unchanged visual.
- Do not finalize a deck while the visual plan has unresolved visual sources. Resolve gaps through Google Drive for Kstudy proof, Kstudy AI Mentor/Supabase for real class/session examples, web search for public/current context, Canva for Canva assets/compositions, image generation for concept visuals, or by converting the slide into a self-created diagram/chart/workflow.
- Keep ordinary slide titles to roughly 48 characters / 9 words; cover or section titles may reach 60 characters / 11 words. Move explanations into body copy or speaker notes.
- Keep Vietnamese-first copy, with natural English terms such as AI, automation, workflow, tool, KPI, ROI when needed.
- Do not present generated, stock, or internet people/classes/events as real Kstudy proof.
- When AI-generated visuals include people, prefer Asian/Vietnamese-looking characters to match Kstudy's Vietnamese learner audience, while keeping the image clearly conceptual rather than proof.
- Do not use an image only to decorate a slide. Every photo, diagram, chart, screenshot, icon, or illustration must clarify the slide's message.
- Proof about Kstudy classes, learners, mentors, workshops, testimonials, or events must come from authentic Kstudy assets or user-supplied approved photos.
- HTML is the canonical output for Kstudy slide decks. If PDF or Canva import changes font, layout, background texture scale, opacity, or shadows, skip Canva or export a raster screenshot PDF as a flat preview only.
- For Kstudy lesson decks, export the presentation PDF as vector browser print-to-PDF by default, with print-safe texture CSS and `print-color-adjust: exact`. Use raster only after explicit user approval because it makes files heavier and text/images less reusable.
