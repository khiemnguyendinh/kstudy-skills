# Strategy Document Standards

Use these standards for formal strategy artifacts, especially Vietnamese Markdown, DOCX, PDF, slides, and diagrams.

## 1. Audience, names, and titles

Create a title map before drafting:

| Person/entity | Formal artifact name | Conversational name | Notes |
|---|---|---|---|
| | | | |

Rules:

- Use the formal artifact name consistently in headings, tables, RACI, diagrams, and captions.
- Do not copy the chat salutation into an institutional strategy.
- For Phoenix strategy documents, use **Thầy Khiêm** for Nguyễn Đình Khiêm; do not use **Anh Khiêm**.
- Run a final search for forbidden or superseded names.

## 2. Vietnamese-first language

Use clear Vietnamese equivalents when they are natural:

| Avoid overuse | Prefer |
|---|---|
| business model | mô hình kinh doanh |
| operating model | mô hình vận hành |
| roadmap | lộ trình |
| stage gate | cổng quyết định/cổng nghiệm thu |
| deliverable | sản phẩm bàn giao/kết quả bắt buộc |
| owner | người chủ trì/người chịu trách nhiệm cuối |
| cash engine | động cơ dòng tiền/trụ tự nuôi |
| profit engine | động cơ lợi nhuận |
| unit economics | kinh tế đơn vị |
| due diligence | thẩm định |

Keep AI, KPI, RACI, LMS, CRM, B2B, B2C, automation, and other familiar terms only when they are shorter or more precise. Define them at first use if the audience may not know them.

## 3. Concision

- Lead with the decision and target.
- Use keywords and short sentences; remove presentation filler.
- Keep one paragraph to one main idea.
- Prefer a table when comparing repeated fields.
- Avoid repeating the same target in several sections unless one is a summary and the definitions remain identical.
- Separate **Đã xác nhận**, **Giả định cần kiểm chứng**, **Ước tính kế hoạch**, and **Khuyến nghị**.

## 4. Roadmap granularity

Executive strategy should show phase-level outcomes, not a daily task calendar.

| Horizon | Minimum content |
|---|---|
| 15 days | Foundation objectives, major workstreams, mandatory outputs, owners, gate |
| Days 16–30 | AI-native rollout objectives, adoption, data, dashboards, governance, gate |
| Days 31–90 | Capacity, financial, quality, partner, and pilot evidence |
| One year | SMART financial, portfolio, capability, and outcome targets |
| Two years | Validated scale and focused portfolio |
| After two years | Vision and options unless evidence supports detail |

Use daily tasks only for cutover, crisis response, regulatory deadline, or an explicitly requested checklist.

## 5. SMART targets

Every material target should specify:

- metric and definition;
- baseline when known;
- target value or range;
- deadline or measurement window;
- owner;
- source of truth;
- condition to stop, hold, or revise.

Do not call a target SMART if the denominator, period, or data source is missing.

## 6. Visuals

Use a real diagram when showing:

- an ecosystem with multiple components;
- a learner journey or operating flow;
- a timeline with several horizons;
- two or more financial engines combining into a total;
- ownership or data relationships.

Rules:

- Keep labels short; move explanations to surrounding text or tables.
- Do not use long prose boxes joined by arrow characters.
- Preserve the actual center and direction of value flow.
- Use consistent colors, typography, units, and naming.
- Inspect the diagram at the final document size.
- If Napkin or another visual API fails due to access, credits, or service errors, state that clearly and use Mermaid, SVG, or another labeled fallback. Do not claim the fallback was API-generated.

## 7. Financial presentation

- Distinguish tuition/billings, retained revenue/cash, contribution, operating result, and cash balance.
- Show short- and long-cycle engines separately before aggregation.
- Show cost ceilings and break-even conditions, not only revenue targets.
- Label interpolated monthly values as planning assumptions.
- State whether annual totals exclude unmodeled periods or products.

## 8. Artifact QA

Before delivery:

1. Search for old titles, wrong names, placeholders, duplicated headings, and outdated dates.
2. Recalculate totals, ranges, margins, and break-even volumes.
3. Verify ecosystem roles and revenue ownership remain consistent.
4. Verify the strategy does not contain accidental daily micromanagement.
5. For DOCX/PDF, test file integrity, render pages, inspect tables and diagrams, and confirm page size.
6. Link the final artifact using its actual path and state which parts remain assumptions.
