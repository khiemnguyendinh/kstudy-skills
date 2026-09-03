# Kstudy Academy — Design System

> **Học viện Kstudy / Kstudy Academy**
> Tagline: **Đào tạo AI & Automation Marketing**
> Web: [www.kstudy.edu.vn](https://www.kstudy.edu.vn)
> Logo sub-line: *"Study by case studies"*

This design system is the **source-of-truth brand foundation** for Kstudy. It stores
tokens, logos, authentic photos, visual sourcing rules, slide-template references,
marketing-website UI kit, and reusable assets.

For actual Kstudy slide deck production, use `kstudy-slide-design`. That skill packages the
slide-specific workflow, safe-area QA, visual planning, HTML deck build, and PDF export.
Use this design-system skill directly when building Kstudy landing pages/web UI, branded
assets, or when the user explicitly asks to inspect or change the design system itself.

---

## 1. What is Kstudy?

Kstudy Academy is a Vietnamese training institute (*học viện*) teaching **AI and
Automation Marketing**. Its students learn practical, case-study-driven skills across the
digital-marketing and growth stack: social media, content, AI tools, marketing automation,
analytics, and career outcomes (CV / portfolio / job placement). The brand voice is
modern, technical, optimistic, and results-oriented.

**Brand keyword field** (drives imagery, copy, iconography):
> digital · social media · AI · automation · technical · trending · growth · business ·
> management · internet · marketing · media · tool · staff · việc làm · CV · portfolio ·
> link · education

### Sources given for this system
- Square brand **icon** (network-node "K", cyan + slate-navy dots) — supplied logo file
- Full **horizontal logo** (icon + "Kstudy" wordmark + tagline) — supplied logo file
- A supplied "white" logo file that was a solid-white block and unusable; the white
  logo/icon in `assets/` were **regenerated** from the color logo — see Caveats
- Brand brief: colors, keywords, background textures, style directions, key-visual notes

No codebase or Figma was provided — the system is built from the logos + brand brief. The
original raw source files (corporate PDFs, screenshots, page scans) are **not bundled** in
this skill package to keep it lightweight — only the derived, ready-to-use assets in
`assets/` are included.

---

## 2. Content Fundamentals (voice & copy)

**Language:** Vietnamese-first (vi-VN), with English for technical terms that students
already use untranslated (AI, automation, marketing, tool, growth, CV, portfolio, workflow).
Mixing is natural and expected — e.g. *"Làm chủ AI tools trong 8 tuần."*

**Tone:** Confident, encouraging, practical. Speaks to ambitious learners and working
professionals. Outcome-driven ("results you can show on a CV"), never academic or stuffy.

**Person:** Addresses the learner directly as **"bạn"** (you). The academy refers to itself
as **"Kstudy"** or **"chúng tôi"** (we). Warm but professional.

**Casing:**
- Headlines: sentence case in Vietnamese (diacritics always correct), Title Case acceptable
  for short English taglines.
- Eyebrows / kickers / tags: `UPPERCASE` in mono with wide tracking (e.g. `KHÓA HỌC AI`,
  `CASE STUDY`, `AUTOMATION`).
- Never SHOUT full sentences.

**Numbers & proof:** Concrete and specific — *"8 tuần"*, *"+200% reach"*, *"1.200+ học viên"*.
Used sparingly as proof points, not decoration. Avoid invented vanity stats.

**Emoji:** Not part of the brand voice. Avoid in headings and formal copy. Use brand icons
(line icons / the node motif) instead of emoji.

**Example copy:**
- Hero: *"Đào tạo AI & Automation Marketing — học bằng case study thực chiến."*
- CTA: *"Đăng ký tư vấn"*, *"Xem lộ trình"*, *"Bắt đầu ngay"*
- Eyebrow: `LỘ TRÌNH 2026` · `AI MARKETING` · `THỰC CHIẾN`
- Section: *"Bạn sẽ học được gì?"*, *"Lộ trình 8 tuần"*, *"Học viên nói gì"*

---

## 3. Visual Foundations

### Colors
The official palette is three brand colors plus the icon cyan:

| Token | Hex | Role |
|---|---|---|
| Navy `--navy` | `#1D237D` | Primary brand, dark surfaces, headings on light |
| Bright blue `--blue` | `#247DF9` | Action, links, primary buttons, focus |
| Yellow `--yellow` | `#FFD84D` | Accent, highlight, energy, single hero pop |
| Cyan `--cyan` | `#0198CF` | Gradient mid-tone (from the icon) |

Neutrals are **cool / navy-tinted** (not pure gray) so they harmonize with the brand. Full
scales, tints, and semantic mappings live in [`colors_and_type.css`](colors_and_type.css).
Yellow is a *spice* — one accent per composition, never a large fill area.

### Typography
Two Vietnamese-capable families, loaded from CDN (see
[`colors_and_type.css`](colors_and_type.css)):
- **Google Sans Flex** (`--font-display`, `--font-sans`, `--font-body`) — the variable
  workhorse for **everything**: display headings, body, subheads, eyebrows, UI. Full
  Vietnamese subset. Hierarchy comes from weight (800 display → 600 labels → 400 body),
  size, and casing. Display headings are **ALL CAPS** at weight 800; body is sentence case.
- **Rokkitt** (`--font-serif`) — slab serif for **editorial accents**: pull quotes and the
  large stat figures, adding warmth/contrast against the sans.
- **Eyebrows/kickers** are Google Sans Flex `UPPERCASE` with wide tracking (no monospace —
  the brand ships no mono face; `--font-mono` is an alias to the sans for legacy refs).
- Slide scale starts at **26px body / 84px display**; web scale at 17px / 56px. See the
  `--t-*` (slide) and `--w-*` (web) tokens. *(Oswald was trialled as the display face and
  removed — the system now uses Google Sans Flex for headings.)*

### Backgrounds & textures
Canonical Kstudy slide background texture styles:

| Style | CSS class | Use |
|---|---|---|
| **Circles · light** | `.bg-circles-light` | Light content, questions, frameworks, concept diagrams |
| **Circles · bright blue** | `.bg-circles-bright` | Demo, practice, energetic transition slides |
| **Circles · brand** | `.bg-circles-brand` | Covers, section dividers, closing, strong brand moments |
| **Grid · bright blue** | `.bg-grid-blue` | Technical/action slides; use sparingly |
| **Dots · light** | `.bg-dots-light` | Content-heavy slides, checklists, tables, practice gates |
| **Dots · dark** | `.bg-dots-dark` | Recap, contrast, warning, closing, high-emphasis slides |
| **White solid** | `.s-light`, `.plain-light`, or `#FFFFFF` | Dense tables, screenshots, maximum-neutrality layouts |

For decks with 12+ slides, use at least four of these seven styles. Avoid decks that only
alternate **Grid · bright blue** and **White solid**.

### Gradients & key visual
Kstudy's gradient system uses **navy→blue ramps** and the blended **gradient-circle key
visual**. The signature circle is a soft radial navy→blue→cyan orb that blends into the
background with low-contrast edges, often large and partially off-canvas for size contrast
and symmetry. See `--grad-circle`, `--grad-brand`, and `--grad-spark`.

### Key visual / motif
**Gradient circles** (orbs) blended with the background, played against sharp geometric
grid lines — *gradient + flat + geometric*. Compositions favor **symmetry** and **size
contrast** (one very large element vs. small supporting ones). The node/connection motif
from the logo icon can echo as connector lines/dots.

### Imagery
**Real people** (*người thật*) — authentic Kstudy photos of learners, instructors,
workspaces, classes, events, and team moments are the default proof layer. Read
[`assets/photos/manifest.md`](assets/photos/manifest.md) and
[`references/visual-sourcing.md`](references/visual-sourcing.md) before selecting visuals.
Photos may be slightly cool-graded to sit with the navy/blue palette, or masked into
circles/orbs to match the key visual. Use generated imagery, Canva, or internet-sourced
images only for conceptual illustration, public references, or missing non-proof visuals;
never present generated/external people, classrooms, testimonials, or events as real
Kstudy evidence.

### Spacing, radii, elevation
- **8pt spacing** system (`--s-1`…`--s-10`).
- **Radii:** generous and rounded — cards `--r-md` (16) to `--r-lg` (24), pills for tags &
  buttons (`--r-pill`). Echoes the rounded, blobby logo icon.
- **Shadows:** soft, cool, navy-tinted (`--shadow-sm…xl`); colored glow shadows for primary
  buttons (`--shadow-blue`) and highlights (`--shadow-yellow`).

### Motion
- Calm, confident easing: `cubic-bezier(.22,1,.36,1)` (ease-out-expo-ish), 200–420ms.
- **Fades + gentle rise** (translateY 8–16px) for entrances. Slide content rises in on
  activation. No bounces, no spinners-as-decoration.
- Hover: subtle lift (translateY -2px) + shadow deepen; links brighten toward `--blue`.
- Press: scale 0.98 + shadow reduce. Focus: 3px `--blue` ring at 35% alpha.

### Cards & surfaces
White (or `--surface-2`) fill, `--r-md/lg` radius, 1px `--line` border *or* `--shadow-md`
(not both heavily), generous interior padding (`--s-5/6`). Dark cards use `--navy-700` with a
hairline of `rgba(255,255,255,.08)`.

### Transparency & blur
Used sparingly — frosted nav bars (`backdrop-filter: blur(12px)` over translucent white),
and translucent chips over gradient orbs. Gradient circles themselves use low-opacity edges
to "blend," not hard-edged.

---

## 4. Iconography

- **No bespoke icon font shipped with the brand.** The system standardizes on **Lucide**
  (https://lucide.dev) — a clean, geometric, **2px-stroke** line set that matches Kstudy's
  technical-but-friendly feel. Loaded from CDN in templates. *(This is a documented
  substitution — see Caveats. Swap for an official set if one exists.)*
- **Stroke style:** outline / line icons only, 2px stroke, round caps & joins. Avoid filled
  or duotone icon styles for UI; reserve fills for the brand node-motif.
- **Brand node motif:** the logo's connected-blob "K" can be reused as a decorative motif
  (connector dots/lines) but is **not** a UI icon — keep it for brand moments.
- **Emoji:** not used. **Unicode glyphs as icons:** avoid; use Lucide.
- Key brand art lives in [`assets/`](assets/): logo (color + white), icon (color + white +
  transparent).

---

## 5. Index / Manifest

**Root**
- `README.md` — this file
- `colors_and_type.css` — all color + type + spacing + shadow + texture tokens
- `SKILL.md` — Agent-Skill manifest for downloading into Claude Code

**Folders**
- `assets/` — logos (color + white), the node-"K" icon (color, white, transparent PNGs), and
  real Kstudy photos with a selection manifest
- `references/visual-sourcing.md` — source priority and visual decision rules for photos,
  diagrams, charts, generated images, Canva, and internet imagery
- `preview/` — Design-System tab cards (colors, type, spacing, components, brand)
- `slides/` — **★ primary deliverable** — 12-type slide-template deck. One `index.html`
  (static, directly-editable slides) on `deck-stage.js`, styled by `slides.css`. Uses
  `image-slot.js` for "người thật" photo drops and Lucide for icons.
- `ui_kits/website/` — marketing-website UI kit: `index.html` + `components.jsx` + `app.jsx`
  + `website.css` (React/JSX, see its own README)

> Fonts load from CDN (Oswald + Rokkitt via Google Fonts; Google Sans Flex via Fontsource) —
> there is no local `fonts/` folder. See the `@import`/`@font-face` block in
> `colors_and_type.css`.

---

## 6. Caveats
- The supplied white logo (`Logo kstudy trang.png`) was a solid-white block; the white
  logo/icon in `assets/` were **regenerated** from the color logo. Please confirm or supply
  the official white/mono lockups.
- **Lucide** icons are a substitution (no official Kstudy icon set was provided).
- Fonts are **user-specified**: Google Sans Flex (display + body) + Rokkitt (serif accent).
  Google Sans Flex is loaded as a variable font from the Fontsource CDN (Google Fonts also
  hosts it); Rokkitt comes from Google Fonts. Both include Vietnamese subsets. The wordmark
  in the logo uses a different rounded display face — supply it if exact wordmark matching is
  needed.
- Local imagery includes a starter set of real Kstudy photos. For broader campaigns, use
  the Google Sheet/Drive asset index referenced in `references/visual-sourcing.md` when
  authenticated access is available.
