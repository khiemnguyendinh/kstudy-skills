---
name: kstudy-design-system
description: Foundational Kstudy Academy brand/design-system reference for tokens, logos, authentic photo assets, visual sourcing rules, website UI kit, and maintaining/updating the Kstudy design system itself. Use for Kstudy landing pages, website sections, branded UI/assets, token/logo/photo questions, or explicit requests to inspect/change the design system. Do NOT use as the primary slide-production skill; for Kstudy slide decks, lesson decks, presentation design, slide images, safe-area QA, or PDF export, use kstudy-slide-design.
---

# Kstudy Design System

This is a foundational brand/design-system skill. For normal Kstudy slide production, use
`kstudy-slide-design`; it already bundles the slide-specific design system and production
workflow. Use this skill for website/UI work, branded assets, token/logo/photo questions,
or when the user explicitly asks to inspect/change the design system.

Read **`README.md`** first — it holds the full brand context, content voice, visual
foundations, and iconography rules. When the output needs photos, diagrams, charts, or
generated visuals, also read **`references/visual-sourcing.md`** and
**`assets/photos/manifest.md`** before choosing visuals. Then explore the other files:

- `colors_and_type.css` — all design tokens (colors, type scales for slides and web,
  spacing, radii, shadows, gradients, textures). Background texture styles are Circles ·
  light, Circles · bright blue, Circles · brand, Grid · bright blue, Dots · light, Dots ·
  dark, and White solid. Gradients use navy→blue ramps plus the blended gradient-circle key
  visual. Fonts: **Google Sans Flex** (display +
  body/UI, ALL-CAPS headings at weight 800) and **Rokkitt** (serif accent) — load from CDN,
  both support Vietnamese.
- `slides/` — reference slide-template library built on `deck-stage.js` (1920×1080). Use it
  when maintaining this design system or when `kstudy-slide-design` needs a canonical
  template reference. Do not use this skill directly to produce ordinary slide decks.
- `ui_kits/website/` — **primary deliverable.** Marketing-site / landing-page components
  (React/JSX: `components.jsx`, `app.jsx`, `website.css`) for kstudy.edu.vn. Start here for
  any landing page, section, or web UI request.
- `preview/` — small spec cards (colors, type, components) for quick visual reference.
- `assets/` — logos (color + white), the node-"K" icon (color, white, transparent), and
  `photos/` (real brand photography for slide/landing-page imagery, with
  `photos/manifest.md` for selecting the right image).
- `references/visual-sourcing.md` — rules for matching slide/page content to real Kstudy
  photos, Google Drive asset sources, diagrams, charts, AI-generated imagery, Canva, or
  internet-sourced visuals.

## Visual sourcing rule
Use authentic Kstudy photos first for classroom, instructor, learner, testimonial, team,
event, and proof-led layouts. If the local photo set is insufficient, consult the Kstudy
asset index in `references/visual-sourcing.md`. Use diagrams/charts when the content is a
workflow, data story, framework, comparison, or decision. Use generated imagery, Canva, or
internet search only when it serves the message better than available real photos, and do
not present generated or external people/events as real Kstudy evidence.

## Background texture rule
For slide/template maintenance, keep all seven canonical background styles available and
use at least four styles in decks with 12+ slides. Do not let production templates regress
to only `Grid · bright blue` plus `White solid`.

## Logo rule
Use the **white** logo on dark/navy backgrounds; the **color** logo on light backgrounds.

## Brief before building (new landing page only)
Before generating a **new** landing page from scratch, ask a short multiple-choice
brief in chat or with Codex's available user-input tool instead of guessing style direction. Skip this entirely when:
editing/extending something already built in this conversation, or the person already stated
mood + sections in their request (don't re-ask what they already told you).

**Landing page** — ask exactly these 2 questions in one call:
1. `single_select` — "Phong cách chủ đạo cho landing page?" — options: "Tối — hero gradient
   thương hiệu, nổi bật" / "Sáng — nền trắng/xám, grid/dots kỹ thuật, chuyên nghiệp" / "Mix —
   hero tối, phần nội dung sáng (khuyến nghị)" / "Để Codex tự chọn"
2. `multi_select` — "Landing page cần section nào?" — options: "Hero + Nav" / "Tính năng / Lộ
   trình học" / "Minh chứng (số liệu, testimonial, giảng viên)" / "Bảng giá · CTA · Footer"

Only add a 3rd question (e.g. exact slide count) if genuinely undetermined after these two.
Once answered, build directly — don't loop back for further confirmation unless something
is actually ambiguous.

## Safe area — mandatory, prevents content/logo/footer overlap
The single most common defect in generated slides: content drifting into the header (logo)
or footer (page-no / org text) band. These bands are fixed and non-negotiable on the
1920×1080 canvas:

- **Header band**: y = 0–172px (logo glyph itself sits at 56–144px)
- **Footer band**: y = 964–1080px (footer text sits at 54–84px from the bottom edge)
- `.head` / `.foot` bar spans x = 130–1790px at `z-index:5` — always paints above any
  content that doesn't set its own z-index.

Rules, in order of how often they get violated:

1. Any container holding real text, cards, or a CTA **must** be wrapped in `.fill.pad` (or
   the equivalent 172/130/116 padding). Never use bare `.fill` for that content — `.fill`
   alone is reserved for full-bleed background layers (photo, gradient, texture).
2. Full-bleed photo/video layers **must** carry a scrim across the *entire width* of both
   bands, not just under the headline. Use `.scrim-head` + `.scrim-foot` (in `slides.css`) —
   a scrim that only darkens one side (e.g. a left-to-right gradient sized to a left-anchored
   headline) is not sufficient on its own; it can leave the opposite corner unprotected.
3. Split/multi-panel layouts (a color panel or image running full-height beside a text
   column): check what's actually behind *each half* of the header/footer bar and color the
   `pageno` / `org` spans individually to match. A single `.on-dark` toggle only works when
   the whole bar sits over one consistent background — it will silently fail on the half that
   isn't dark.
4. Before finalizing, confirm the stacked content height inside `.pad` fits the 792px budget
   (1080 − 172 − 116). Per-line reference: hero ≈130px, display/title ≈97px, h1 ≈74px, h2
   ≈55px, h3 ≈39px, lead/body ≈39–45px. If copy runs long, shorten it — don't let
   `.slide{overflow:hidden}` silently clip it right at the footer.
5. Freely-placed decorative elements (`.adot`, `.orb`, badges) may bleed into the header/
   footer bands only if they carry no text/information and use `z-index:4` or lower.
6. Self-check before delivering: temporarily add `.safe-outline` to a slide's root element to
   render a dashed guide at the exact safe boundary, eyeball every slide against it, then
   remove the class from the final file.

`slides/index.html` slide 09 (full-bleed) and slide 11 (feature-split) apply all of the above.
Use them as reference when maintaining templates or when KSD needs canonical structure.

## When invoked
If creating landing pages, mocks, throwaway prototypes, or branded web/UI assets, **copy
assets out** and produce static HTML (or React) files for the user to view — start from
`ui_kits/website/` for landing pages / web sections.
If working on production code, copy assets and apply the rules here to design on-brand.

If invoked without guidance, ask the user what they want to build (**slide deck** or
**landing page**). If the answer is slide deck, hand off to `kstudy-slide-design`. If the
answer is landing page or design-system work, proceed here and check the relevant safe-area
or layout rules before delivery.
