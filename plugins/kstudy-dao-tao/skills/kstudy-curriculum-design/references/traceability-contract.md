# Kstudy Learning Traceability Contract

Contract dữ liệu chung cho pipeline:

`Kstudy-Curriculum-Design → kstudy-course-planner → kstudy-syllabus-creator → kstudy-lesson-plan-creator`

## Chuỗi chuẩn

```text
Job Task → Competency → PLO → CLO → Lesson Outcome → Activity → Evidence → Rubric → Resource → AI Mentor Gate
```

## Object contract

Mỗi artifact có thể chứa một object `traceability`:

```json
{
  "job_task_ids": [],
  "competency_ids": [],
  "plo_ids": [],
  "clo_ids": [],
  "lesson_outcome_ids": [],
  "activity_ids": [],
  "evidence_ids": [],
  "rubric_ids": [],
  "resource_ids": [],
  "approval_status": "PROPOSED"
}
```

Không yêu cầu mọi field phải đầy đủ ở mọi tầng. Chỉ các field thuộc tầng hiện
tại mới là bắt buộc; field downstream được để rỗng kèm status/gap rõ ràng.

## ID convention

ID phải ổn định, không lấy trực tiếp từ title:

- `JT-<n>`: job task.
- `COMP-<n>`: competency.
- `PLO-<n>`: program outcome.
- `CLO-<COURSE>-<n>`: course outcome.
- `LO-<COURSE>-B<buổi>.<n>`: lesson outcome.
- `ACT-<COURSE>-B<buổi>.<lesson>.<n>`: activity.
- `EVID-<COURSE>-B<buổi>.<lesson>`: evidence/artifact.
- `RUBRIC-<COURSE>-B<buổi>.<lesson>`: rubric.
- `RES-<COURSE>-B<buổi>.<lesson>.<n>`: resource.
- `FC-<COURSE>-B<buổi>.<lesson>.<n>`: formative check.

Nếu hệ thống đã có ID cũ, giữ ID cũ và thêm alias/migration note; không âm thầm
đổi ID khiến downstream mất liên kết.

## Phạm vi theo skill

| Skill | Tạo hoặc khóa |
|---|---|
| Curriculum Design | `JT`, `COMP`, `PLO`, course map và capstone evidence direction |
| Course Planner | Kế thừa `JT/COMP/PLO`; tạo `CLO` draft, evidence blueprint, rubric direction, resource map |
| Syllabus Creator | Khóa `CLO`; tạo `LO`, `EVID`, `RUBRIC`, resource mapping trong `course.json` |
| Lesson Plan Creator | Tạo `ACT`, `FC`, zone, formative feedback, Miller/UDL và kiểm tra timeline |

## Invariants

1. Không có activity nếu không phục vụ CLO hoặc lesson outcome.
2. Không có lesson outcome nếu không có evidence direction.
3. Không có evidence nếu không có rubric hoặc assessment method được duyệt.
4. Mọi PLO phải truy được về job task hoặc mục tiêu chiến lược đã xác nhận.
5. Resource bắt buộc phải gắn với outcome/activity mà nó phục vụ.
6. Không tham chiếu ID không tồn tại ở cùng artifact hoặc upstream artifact.
7. `approval_status = APPROVED` chỉ dùng sau review; im lặng không phải approval.

## Approval và readiness

- `PROPOSED`: đề xuất, chưa khóa.
- `APPROVED`: đã được duyệt cho downstream sử dụng.
- `REJECTED`: đã review và không dùng trong version hiện tại.
- `NEEDS_INPUT`: thiếu dữ liệu/quyết định của user.
- `DEFERRED`: tạm hoãn trong version hiện tại.
- `SUPERSEDED`: bị thay thế bởi version/ID mới.

`READY_FOR_SYLLABUS` yêu cầu đầy đủ chain đến CLO/evidence direction.

`READY_FOR_LESSON_PLAN` yêu cầu đầy đủ chain đến lesson outcome/evidence/rubric/resource.

`READY_FOR_PILOT` yêu cầu thêm activity, formative checks, timeline và resource URL.

## Alignment rule

Với mỗi CLO/lesson outcome, phải trả lời được:

- Được dạy ở đâu?
- Được kiểm tra bằng evidence nào?
- Rubric/quality standard nào đánh giá evidence?
- Resource và activity nào dẫn đến evidence?

Gate không được yêu cầu nội dung chưa được dạy hoặc chưa có resource/activity
tương ứng.
