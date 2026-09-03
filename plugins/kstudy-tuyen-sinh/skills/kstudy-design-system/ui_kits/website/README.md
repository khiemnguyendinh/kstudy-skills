# Kstudy — Marketing Website UI Kit

High-fidelity recreation of the Kstudy Academy marketing site (kstudy.edu.vn) built on
the shared design system (`../../colors_and_type.css`). A single-page, responsive,
interactive landing page for the **AI & Automation Marketing** program.

> No production codebase or Figma was provided — this kit is an **original brand-true
> recreation** built from the brand system, not a copy of an existing kstudy.edu.vn build.

## Files
- `index.html` — mounts the React app (React 18 + Babel standalone + Lucide via CDN)
- `components.jsx` — section components: `NavBar`, `Hero`, `Features`, `Curriculum`,
  `StatsBand`, `Testimonials`, `CTASection`, `Footer`, `EnrollModal`, plus an `Icon` helper.
  All exported to `window` for cross-file use.
- `app.jsx` — page shell + interactivity (enroll modal state, Lucide re-draw)
- `website.css` — component classes (web scale, responsive at 880px)

## Interactions
- **Sticky frosted nav** with smooth-scroll anchors; collapses to a hamburger menu < 880px.
- **Enroll modal** — opens from any "Đăng ký tư vấn" button (nav, hero, CTA); fake form with
  focus-ring inputs and a success state.
- **Hover states** — cards lift + deepen shadow; buttons rise; links shift to brand blue.

## Sections (component coverage)
Nav · Hero (gradient-orb visual) · Features (3 outcome cards) · Curriculum (4-week timeline
cards) · Stats band (dark) · Testimonials (3) · CTA panel · Footer (links + contact icons).

## Notes & caveats
- Social/brand icons were swapped to generic **contact** icons (globe / mail / phone / send) —
  current Lucide ships no brand logos. Swap for real social links + a brand-icon set if needed.
- Testimonial avatars use initials placeholders — drop in real "người thật" photos.
- Copy is representative Vietnamese marketing copy following the brand voice (see root README
  → Content Fundamentals).
