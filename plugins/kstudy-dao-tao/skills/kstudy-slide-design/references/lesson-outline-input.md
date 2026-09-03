# Lesson slide outline input contract

Use this when the source is `<CODE>-B<N>-Slide-outline.md` from `kstudy-lesson-plan-creator`.

## Role split

- Lesson-plan-creator owns: learning objective, short message, required content, visual job, and illustration brief.
- KSD owns: slide layout, typography, brand styling, asset selection, image crop, diagram/chart design, safe-area QA, HTML/PDF export.
- Do not treat the outline as final slide copy. Preserve intent, then shorten and design.

## Expected slide block

```markdown
**Slide N — <short title>**
- Mục tiêu học: <what learner understands/does>
- Thông điệp chính: <one sentence>
- Nội dung: <2-4 short bullets>
- Visual job: <Proof | Thinking | Doing | Evidence | Context | Concept>
- Minh họa: <visual type — source/structure/prompt>
- Gợi ý KSD: <optional layout hint>
```

## Title handling

- Ordinary slide title target: <=48 characters or <=9 words.
- Cover/section title target: <=60 characters or <=11 words.
- If title is too long, shorten it without changing the learning intent.
- Move nuance into `Thông điệp chính`, body copy, or speaker notes.
- Avoid colon-heavy titles. Prefer one crisp claim.

## Visual job mapping

| Visual job | KSD should use |
|---|---|
| Proof | Real Kstudy photo or approved user-supplied proof asset |
| Thinking | Diagram, framework, concept map, matrix, timeline |
| Doing | Real screenshot/mockup with annotations |
| Evidence | Chart, metric card, sourced table, timeline |
| Context | Public photo/screenshot with source, not Kstudy proof |
| Concept | Generated/Canva concept visual, clearly not proof |

## Minh họa parsing rules

- If `Minh họa` says screenshot/demo/tool: use a screenshot or UI mock with annotations; do not use AI concept art.
- If it says workflow/SOP/process: prefer flowchart, timeline, swimlane, or step cards.
- If it says compare/decision: use comparison table, matrix, or quadrant.
- If it says data/KPI/benchmark: use only supplied or sourced numbers; otherwise show placeholder state and flag missing data.
- If it says Kstudy class/student/mentor/proof: use authentic Kstudy photo assets or ask for approved image.
- If it says AI-generated concept: keep it conceptual; never present generated people/classes/events as real Kstudy evidence.

## Output expectations

KSD may revise slide count lightly if needed for readability, but keep the same learning sequence unless user approves restructuring.
