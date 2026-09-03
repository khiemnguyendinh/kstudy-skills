---
name: kstudy-tot-nghiep
description: Create, edit, structure, and quality-check Vietnamese Kstudy graduation thesis documents, capstone reports, final project proposals, outlines, rubrics, and DOCX/Markdown deliverables. Use when the user asks to draft or polish a Kstudy "de tai tot nghiep", "bao cao tot nghiep", final project, capstone, project defense document, academic-style report, cover page, thesis outline, chapter draft, rubric, supervisor feedback, or brand-aligned Kstudy document package.
---

# Kstudy Tot Nghiep

## Overview

Use this skill to produce Vietnamese-first graduation thesis and capstone documents for Kstudy Academy. Keep the output practical, evidence-based, brand-aligned, and suitable for learners in Digital Marketing, AI, automation, and business operations.

## Core Workflow

1. Clarify the minimum brief if missing: program, learner level, topic, business context, required format, deadline, expected length, and whether the output is outline, draft, DOCX, rubric, or feedback.
2. Read the relevant reference before writing:
   - `references/thesis-structure.md` for document structure, chapter requirements, and defense-ready logic.
   - `references/kstudy-brand-writing.md` for Kstudy brand voice, formatting, and presentation rules.
   - `references/quality-checklist.md` before final delivery or review.
3. Build from source evidence. Use learner/project facts, datasets, interviews, campaign screenshots, analytics exports, or approved course context when available. Mark unknown items as `[CAN_BO_SUNG]`; do not invent statistics, customers, results, quotes, credentials, or system status.
4. Write in Vietnamese. Keep English terms only where they are standard in the field: AI, automation, funnel, workflow, KPI, CPA, ROAS, CRM, landing page, content pillar, dashboard, prompt, agent.
5. Produce the requested artifact directly:
   - For an outline: deliver a numbered table of contents plus chapter objectives and expected evidence.
   - For a full draft: write section by section with academic tone, practical examples, citations/placeholders, and action-oriented recommendations.
   - For DOCX skeletons: use `scripts/create_kstudy_thesis_docx.py`.
   - For review: lead with issues, severity, exact fix, then a concise rewrite or patch suggestion.
6. Run the quality checklist before final response and state any assumptions or missing inputs.

## Kstudy Thesis Principles

- Start with WHY: the business problem, learner objective, and measurable outcome must be visible before methods and tools.
- Keep the thesis practical: every chapter should connect to a real business, campaign, workflow, automation, learner portfolio, or operational case.
- Use CDIO logic when suitable: Conceive the problem, Design the solution, Implement the plan/prototype, Operate or evaluate the result.
- Use KASH when defining outcomes: Knowledge, Attitude, Skill, Habit.
- Use Bloom verbs for learning outcomes and rubrics: identify, analyze, design, implement, evaluate, optimize, present.
- Keep recommendations realistic for a small team: owner, tool, effort, risk, KPI, and next action.

## Default Deliverable Shape

When the user does not specify another structure, use this order:

1. Bia / trang thong tin de tai
2. Loi cam on
3. Cam ket tinh trung thuc
4. Tom tat de tai
5. Muc luc
6. Chuong 1: Boi canh va van de
7. Chuong 2: Co so ly thuyet va khung phan tich
8. Chuong 3: Phuong phap va ke hoach thuc hien
9. Chuong 4: Giai phap / san pham / chien dich / workflow
10. Chuong 5: Danh gia ket qua va khuyen nghi
11. Ket luan
12. Tai lieu tham khao
13. Phu luc / minh chung

Use Vietnamese headings with diacritics in final output. ASCII headings above are for compatibility only.

## DOCX Skeleton Script

Use the script when the user asks for a Word file, `.docx`, template, skeleton, or installable starter document.

```bash
python3 scripts/create_kstudy_thesis_docx.py \
  --title "Ứng dụng AI Automation trong tối ưu phễu tuyển sinh cho Kstudy" \
  --student "Nguyễn Văn A" \
  --program "Digital Marketing định hướng AI Automation" \
  --mentor "Nguyễn Đình Khiêm" \
  --output "/path/to/Kstudy-De-tai-tot-nghiep.docx"
```

The script creates a DOCX starter with Kstudy-colored headings, cover information, chapter sections, evidence placeholders, and a review checklist. After generating it, continue editing the DOCX or convert sections from Markdown as needed.

## Writing Rules

- Write like a Kstudy training consultant, not like a generic academic assistant.
- Prefer clear claims with evidence over long theory summaries.
- Use tables for scope, KPI, timeline, stakeholder, risk, rubric, and implementation plan.
- In methodology sections, state data source, period, sample, tool, limitation, and validation approach.
- In analysis sections, separate observation, interpretation, implication, and recommended action.
- Use placeholders for missing evidence: `[CAN_BO_SUNG: so lieu Ads Manager thang 05/2026]`.
- Do not promise outcomes, exaggerate results, or make legal/compliance claims without source evidence.
- Do not publish, submit, email, or upload a thesis unless the user explicitly approves.

## Review Mode

When reviewing an existing thesis, return findings first:

1. Critical gaps that can fail grading or defense.
2. Evidence gaps and unsupported claims.
3. Structure and logic issues.
4. Kstudy brand/style issues.
5. Suggested rewrite for the highest-impact section.

Keep the review direct and actionable. Use file/page/section references when available.

## Output Contract

End each substantial deliverable with:

- `Gia dinh`: assumptions used.
- `Can bo sung`: missing evidence or decisions.
- `Kiem tra chat luong`: short checklist result.
