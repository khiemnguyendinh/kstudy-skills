# Frontend Agent Prompt

Use `$ck:ui-ux-pro-max`, then `$kstudy-design-system`, then `$ck:frontend-design`, then `$design-taste-frontend` to build the approved Kstudy funnel below.

## Sources of truth

- Workflow state: `{{workflow_state_path}}`
- Approved landing/funnel brief: `{{landing_brief_path}}`
- Claims ledger: `{{claims_ledger_path}}`
- Funnel blueprint: `{{funnel_blueprint_path}}`
- Asset manifest: `{{asset_manifest_path}}`
- Tracking plan: `{{tracking_plan_path}}`
- Existing project/stack: `{{project_path_and_stack}}`

Read all sources before editing. If they conflict, use this priority:

`product truth/evidence/ethics > audience/conversion strategy > Kstudy brand > accessibility/performance > decorative taste`.

## Build scope

Implement the exact approved routes, sections, content hierarchy, video/form/CTA placement, redirects, loading/error/duplicate states, responsive behavior, server-side store-first lead capture, idempotency, async integration boundary and tracking hooks.

Render the approved `course_explanation` contract without rewriting it: value/outcome bullets, every in-scope module with “can do” and hands-on output, one card/block per verified instructor beside the approved image, and at least four FAQs. Preserve plain Vietnamese; explain or replace specialist terms.

Do not:

- invent or modify public claims, price, urgency, testimonials, stats or offer;
- copy example content/data from Kstudy UI kit;
- use fake live, viewer count, scarcity or countdown;
- put PII in URL/analytics/data layer;
- expose secrets client-side;
- send/publish/deploy/migrate or change external systems without a separate approval.

## Definition of done

- All approved routes and edge states work locally.
- Brief/claims validators PASS.
- Type/lint/test/build checks appropriate to the project PASS.
- Mobile, keyboard, focus, contrast, form error, reduced-motion and media accessibility are verified.
- Tracking fires once with correct non-PII payload and dedupe contract.
- SEO/index/canonical/metadata follow the brief.
- Course value, module outcomes, instructor profiles and FAQs match the approved brief and remain easy to understand on mobile.
- Create/update `qa-report.md` with evidence, blockers and pending external actions.
