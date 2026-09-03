# Curriculum framework JSON schema

Đây là contract tối thiểu để bàn giao từ `Kstudy-Curriculum-Design` sang
`kstudy-course-planner`. Có thể mở rộng field nhưng không đổi ý nghĩa field lõi.

## Top-level

```json
{
  "schema_version": "1.0",
  "design_mode": "NEW_PROGRAM",
  "research_level": "DEEP",
  "design_depth": "LITE | STANDARD | FULL",
  "status": "PROPOSED",
  "project_brief": {},
  "occupation_analysis": {},
  "competency_architecture": {},
  "program_outcomes": [],
  "capstone": {},
  "curriculum_map": [],
  "workload": {},
  "traceability": {},
  "research": {},
  "quality_review": {},
  "handoff": {}
}
```

## Required semantic content

### `project_brief`

Gồm `working_title`, `field`, `occupation`, `target_learner`, `level`,
`geography`, `delivery_model`, `business_goal`, `duration_assumption`,
`assumptions` và `open_questions`.

### `occupation_analysis`

Gồm `job_families`, `roles`, `tasks`, `tools`, `work_outputs`, `quality_standards`
và `sources`. Mỗi task có `task_id`, `role_id`, `statement`, `frequency`,
`difficulty`, `priority`, `evidence_status`, `source_ids`.

### `competency_architecture`

Gồm `competencies` và `framework_adaptation`. Mỗi competency có `competency_id`,
`statement`, `kash_dimension`, `conditions`, `performance_criteria`, `evidence`,
`task_ids` và `status`.

### `program_outcomes`

Mỗi PLO có `plo_id`, `statement`, `bloom_level`, `kash_dimensions`,
`cdio_adaptation`, `evidence`, `priority` và `source_ids`.

### `curriculum_map`

Mỗi course có `course_id`, `title`, `stage`, `purpose`, `sequence`, `prerequisite_ids`,
`plo_mapping`, `clo_placeholders`, `core_topics`, `artifacts`, `assessment_direction`,
`workload`, `tool_constraints`, `source_ids` và `handoff_status`.

Các field vận hành tùy chọn để xuất workbook tương thích với khung chương trình
Digital Marketing hiện tại gồm: `legacy_title`, `pic`, `tuition`,
`tuition_status`, `live_sessions`, `elearning_units`, `project_guidance`,
`ai_mentor_support`, `strategic_role`, `references` và `workload_notes`.
Không tự suy ra hoặc xác nhận giá trị chính thức cho các field này.

`plo_mapping` dùng `I`, `R` hoặc `M`:

- `I`: Introduce.
- `R`: Reinforce.
- `M`: Master/assess.

### `workload`

Gồm `program_totals`, `course_totals`, `activity_register` và `assumptions`.
Mỗi total phải có sáu thành phần giờ trong [workload-and-hybrid.md](workload-and-hybrid.md).

### `traceability`

Gồm `links`, `coverage_summary`, `orphan_plos`, `orphan_courses`,
`unmapped_activities` và `status`. Mỗi link tối thiểu có `task_id`, `competency_id`,
`plo_id`, `course_id`, `clo_id_or_placeholder`, `activity_id_or_placeholder` và
`assessment_id_or_direction`. Dùng convention và readiness rule trong
[traceability-contract.md](traceability-contract.md). Curriculum Design chỉ khóa
đến course/capstone evidence direction; không tự tạo activity ID chi tiết.

### `research`

Gồm `brief`, `jd_window`, `findings`, `jd_signals`, `competitor_benchmarks`, `sources`, `gaps`
và `recommendations`. Không đưa claim không có `source_ids` hoặc `evidence_status`.

### `handoff`

Gồm `target_skill`, `status`, `course_specs_ready`, `blocking_questions`,
`assumptions_requiring_approval`, `source_gaps` và `next_action`.

## Status rules

`READY_FOR_COURSE_PLANNER` chỉ hợp lệ khi course specs, workload totals,
traceability và quality review không còn blocker. Nếu còn gap ảnh hưởng outcome,
scope, duration hoặc resource bắt buộc, dùng `BLOCKED`.
