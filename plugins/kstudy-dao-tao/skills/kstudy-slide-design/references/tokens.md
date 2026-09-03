# Kstudy Design Tokens

Use `assets/templates/colors_and_type.css` as the canonical implementation file.

## Colors

| Token | Hex | Role |
|---|---:|---|
| Navy | `#1D237D` | Primary brand, headings, dark surfaces |
| Bright blue | `#247DF9` | CTA, links, active states, focus |
| Yellow | `#FFD84D` | Accent, highlight, one energetic pop |
| Cyan | `#0198CF` | Gradient mid-tone, icon-derived accent |
| Ink | `#0E1230` | Primary text on light |
| Slate 700 | `#3B4063` | Secondary text |
| Slate 500 | `#6B7099` | Muted text |
| Line | `#E2E4F0` | Dividers and hairlines |
| Surface 2 | `#F4F5FB` | Panels |
| Surface 1 | `#FAFBFE` | Page background |

Yellow is a spice, not a base color. Use it for small highlights, active markers, or one hero accent.

## Background Textures

Use only these canonical Kstudy slide background texture styles unless the user explicitly asks for a new art direction:

| Style name | CSS class | Best use |
|---|---|---|
| Circles · light | `bg-circles-light` | Light content slides, questions, frameworks, diagrams. |
| Circles · bright blue | `bg-circles-bright` | Energetic demo, practice, or transition slides. |
| Circles · brand | `bg-circles-brand` | Covers, section dividers, closing slides, strong concept slides. |
| Grid · bright blue | `bg-grid-blue` | Technical/action slides where a grid supports the message. Do not overuse. |
| Dots · light | `bg-dots-light` | Content-heavy slides, checklists, tables, structured practice. |
| Dots · dark | `bg-dots-dark` | Dark recap, contrast, warning, closing, or high-emphasis slides. |
| White solid | `s-light`, `plain-light`, or `#FFFFFF` | Dense tables, screenshots, or layouts that need maximum neutrality. |

Deck-level rule: for decks with 12+ slides, use at least four of the seven styles above. Do not build a deck that only alternates `Grid · bright blue` and `White solid`.

## Gradients And Key Visual

- `--grad-brand`: navy to bright blue ramp.
- `--grad-circle`: radial navy to blue, used as a large blended gradient-circle key visual.
- `--grad-spark`: blue to cyan with yellow tail, for small energetic accents.

Use navy→blue ramps and blended gradient-circle key visuals as brand structure, not as generic decoration. Use one signature background treatment per composition. Do not stack circles, dots, grids, gradients, and heavy photos all at once.

## Typography

- Display/body/UI: Google Sans Flex.
- Editorial accent: Rokkitt.
- Vietnamese support is required.
- Big headings are heavy and high-contrast. Body copy stays readable and practical.
- Eyebrows are uppercase, short, and widely tracked.

Recommended web scale:

| Role | Size |
|---|---:|
| Display | `56px` |
| H1 | `40px` |
| H2 | `30px` |
| H3 | `22px` |
| Body | `17px` |
| Small | `14px` |
| Eyebrow | `13px` |

Recommended slide scale:

| Role | Size |
|---|---:|
| Hero | `112px` |
| Display | `84px` |
| H1 | `64px` |
| H2 | `48px` |
| H3 | `34px` |
| Lead | `30px` |
| Body | `26px` |
| Small | `22px` |

## Layout

- Spacing uses an 8pt system: `4, 8, 12, 16, 24, 32, 48, 64, 96, 128`.
- Cards: radius `16px` or `24px`, not fully pill-shaped.
- Buttons/chips: pill radius is allowed.
- Shadows: soft, cool, navy-tinted. Avoid harsh black shadows.
- Motion: 200-420ms, calm ease-out, fade + gentle rise, hover lift around `-2px`.

## Icons

- Use Lucide or a similar 2px outline icon style.
- Round caps and joins.
- Avoid emoji as icons.
- The node-K brand mark is for branding moments, not generic feature icons.
