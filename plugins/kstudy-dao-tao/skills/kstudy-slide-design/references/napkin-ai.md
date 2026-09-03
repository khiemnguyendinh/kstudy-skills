# Napkin AI For Kstudy Slides

Read this reference only when the visual plan assigns a slide to Napkin AI.

## Decision Rule

Use Napkin AI for concept maps, hierarchies, 3-6 branch frameworks, causal chains, process flows, and compact comparisons. Use self-created HTML/CSS/SVG when exact geometry, data fidelity, editable labels, animation, or repeated deck-wide components matter more.

Do not use Napkin AI as evidence or proof. It must not invent Kstudy classes, learners, outcomes, software states, metrics, testimonials, or market data.

## Kstudy Visual Direction

Use the palette and hierarchy from `kstudy-design-system`:

- Style: flat, minimal, professional education, clear hierarchy, restrained line work.
- Primary dark: `#1D237D`.
- Primary: `#247DF9`.
- Secondary: `#0198CF`.
- Accent: `#FFD84D`, used selectively.
- Light fill: `#E8F4FF`.
- Text on light: `#0E1230` or navy.
- Avoid purple-led palettes, rainbow nodes, playful hand-drawn styles, heavy shadows, glossy 3D, and decorative icons.

## Production Workflow

1. Reduce the slide idea to one visual sentence and 3-6 short nodes. Keep labels parallel and remove explanatory paragraphs before generation.
2. Put the source text in a UTF-8 file and save generated assets under the deck project, normally `assets/images/napkin/`.
3. Read `NAPKIN_API_TOKEN` from the environment or a project-local `.napkin.local`. Add `.napkin.local` to `.gitignore`. Never paste, print, log, or commit the token.
4. Prefer SVG for scalable slide use. Request `transparent_background=true`, `color_mode=light`, `language=vi-VN`, horizontal orientation, and about 1800px width. Use PNG only when the SVG renders incorrectly.
5. If a Kstudy custom style exists, store its brand ID in `NAPKIN_KSTUDY_STYLE_ID`. Treat built-in or custom `style_id` values as hints until the completed response confirms them.
6. Generate once with `scripts/napkin_generate.py`. The script skips an existing output unless `--force` is explicit, polls asynchronously, and downloads immediately because status/file URLs expire.
7. Inspect `warnings`. If `invalid_style_id` appears, do not assume Kstudy styling was applied. Use a verified custom brand ID or run `scripts/normalize_napkin_brand.py --brand kstudy` on the SVG/PNG.
8. Place the visual directly on the slide surface. Keep its own background transparent; do not add a default white panel, card, border, or shadow beneath it.
9. Render the slide at 1920x1080 and check it at full size and thumbnail size. Verify Vietnamese text, hierarchy, line contrast, safe area, and visual balance with the title/footer.
10. Keep the approved source text, generated asset, and final normalized asset together. Reuse the approved file instead of spending credits on unchanged requests.

## Recommended Commands

Generate a transparent SVG:

```bash
python3 scripts/napkin_generate.py \
  --content-file assets/images/napkin/framework.txt \
  --output assets/images/napkin/framework-raw.svg \
  --context "Kstudy education slide. Flat, minimal, professional, clear hierarchy, restrained navy-blue-cyan palette." \
  --visual-query mindmap \
  --style-env NAPKIN_KSTUDY_STYLE_ID
```

Normalize to the Kstudy design-system palette:

```bash
python3 scripts/normalize_napkin_brand.py \
  --brand kstudy \
  --input assets/images/napkin/framework-raw.svg \
  --output assets/images/napkin/framework-kstudy.svg
```

For PNG fallback, use the same normalization command. Add `--clear-edge-white` only when an opaque near-white canvas remains connected to the image edges.

## API And Failure Handling

- API flow: `POST /v1/visual` -> poll `GET /v1/visual/{request-id}/status` -> authenticated download from the returned file URL.
- The API is a developer preview. Do not make a production deck pipeline depend on it without a cached fallback asset.
- On `429`, respect `Retry-After` and retry with backoff.
- On `no_credits`, stop and report the credit issue. Do not loop.
- On `no_visuals`, simplify the content or split it into smaller structures.
- On `not_enough_visuals` or orientation warnings, use the valid output only after visual QA.
- On `invalid_style_id`, keep the generated file only if palette normalization and QA make it acceptable.

## Watermark And Rights

Free-plan outputs may include a Napkin watermark. Do not erase, crop, cover, or programmatically remove it. Use a paid watermark-free output or keep the attribution visible. Record Napkin AI as the visual source in project notes when appropriate.

## HTML Integration

Use a neutral transparent image layer:

```css
.napkin-visual {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: transparent;
  border: 0;
  box-shadow: none;
}
```

Decorative grid/dot/circle textures may continue behind the transparent visual, but reduce their opacity if they compete with diagram lines or labels.
