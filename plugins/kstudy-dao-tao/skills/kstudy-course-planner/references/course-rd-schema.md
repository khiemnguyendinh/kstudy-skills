# Curriculum R&D JSON contract

`curriculum-rd.json` is a planning superset, not the final `course.json`. Keep research provenance and approval state here; the next skill enriches the course-level and lesson-level fields before build.

## Top-level shape

```json
{
  "schema_version": "1.0",
  "planner_mode": "NEW_COURSE | UPDATE_COURSE | AUDIT_ONLY",
  "research_level": "LIGHT | STANDARD | DEEP",
  "design_depth": "LITE | STANDARD | FULL",
  "status": "DRAFT | PENDING_APPROVAL | READY_FOR_SYLLABUS | BLOCKED",
  "course": {},
  "research": {},
  "update_audit": [],
  "traceability": {},
  "handoff": {}
}
```

## Required course sections

`course` should contain:

- `identity`: `code`, `title`, `author`, `color`, `logo`, each with `value` and `status` (`CONFIRMED`, `PROPOSED`, `MISSING`). Do not invent official values.
- `program_context`: framework membership, role in product system, prerequisites and follow-on courses.
- `learner`: primary, secondary, anti-persona, entry level, jobs, constraints and evidence.
- `needs`: prioritized jobs, pains, desired outcomes and evidence references.
- `scope`: included topics, excluded topics, core/extension boundary and assumptions.
- `outcomes`: course outcomes, CDIO phase, Bloom, KASH, evidence and capstone.
- `sessions`: `idx`, summary, duration, mode, format type and hybrid allocation.
- `lessons`: architecture-level lessons with `sort_order`, `session_idx`, title, topic, concepts, objectives, gate, artifact, resource ids and lesson-level traceability.
- `hybrid`: classroom, e-learning, AI Mentor and internet roles; expected learner workload.
- `resources`: planned resources linked to `research.sources` by `source_ids`.
- `assessment_blueprint`: evidence direction, assessment method, rubric direction,
  gate and approval status for important CLO/capstone evidence.

Do not force detailed Syllabus fields such as lean `ai_context`, final rubric or final radar into the planner. The planner may propose them, but `kstudy-syllabus-creator` owns finalization.

## Research sections

`research` contains:

- `brief`: questions, outcomes supported, scope and freshness requirement.
- `findings`: claim, evidence status, source ids, implication and confidence.
- `sources`: complete source records; see `research-and-citations.md`.
- `gaps`: inaccessible, conflicting or insufficient evidence.
- `recommendations`: curriculum actions supported by findings.

## Traceability

Đọc contract chung tại:

`/Users/macintoshhd/.codex/skills/kstudy-curriculum-design/references/traceability-contract.md`

Top-level `traceability` phải có:

- `job_task_ids`, `competency_ids`, `plo_ids` kế thừa từ Curriculum Design.
- `clo_ids`, `evidence_ids`, `rubric_ids`, `resource_ids` ở cấp course.
- `mappings`: từng mapping từ nguồn nghề đến course outcome/evidence.
- `alignment_status`, `approval_status` và `gaps` nếu chain chưa hoàn chỉnh.

Mỗi lesson architecture nên có object `traceability` cùng field contract; không
để lesson chỉ có title/topic mà không có hướng evidence.

## Update audit

For `UPDATE_COURSE`, each item contains:

```json
{
  "location": "Bài 3 / Topic",
  "existing_content": "...",
  "action": "KEEP | UPDATE | EXPAND | MERGE | MOVE | REDUCE | REMOVE | REPLACE",
  "reason": "...",
  "source_ids": ["SRC-001"],
  "impact": ["outcome", "resource", "workload"],
  "approval_status": "PROPOSED"
}
```

## Handoff gate

`handoff.status` may be `BLOCKED` until all official identity values, learner, prerequisites, outcome, capstone, sessions and resource blockers are resolved. `READY_FOR_SYLLABUS` means the next skill may ingest the file and ask only normal Syllabus-level confirmations.

Use `blocking_questions` for questions that must be answered before handoff. Use `assumptions` for non-blocking assumptions that remain visible to the next skill.
