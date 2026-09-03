# Workload and hybrid design

## Hour taxonomy

| Field | Ý nghĩa | Ví dụ hoạt động |
|---|---|---|
| `direct_live_hours` | Thời gian synchronous với giảng viên | classroom, Zoom, workshop, review |
| `elearning_hours` | Học liệu số có cấu trúc | video, reading, quiz, simulation |
| `self_study_hours` | Tự đọc, research, reflection, preparation | reading extension, note, prework |
| `practice_project_hours` | Tạo output và luyện skill | lab, campaign, workflow, portfolio |
| `assessment_feedback_hours` | Review và sửa theo rubric | critique, grading, retake, QA |
| `mentor_coaching_hours` | Hỗ trợ có người/AI Mentor | office hour, group coaching, 1-1 |

Không gộp tất cả thành “giờ học”. Báo cáo riêng `contact_hours`,
`asynchronous_hours`, `applied_hours`, `assessment_hours`, `mentor_hours` và
`total_learner_workload_hours`.

## Calculation rules

Với mỗi course:

```text
total_course_hours
  = direct_live_hours
  + elearning_hours
  + self_study_hours
  + practice_project_hours
  + assessment_feedback_hours
  + mentor_coaching_hours
```

Với program:

```text
total_program_hours = sum(total_course_hours)
```

Mỗi activity phải có `activity_id`, `course_id`, `mode`, `minutes`, `artifact`,
`assessment_link`, `counts_toward` và `source_or_assumption`. Một activity chỉ
được tính một lần. Nếu thời gian nằm trong live session nhưng là independent
practice, tách activity và ghi rõ cách tính.

## Baseline discipline

Có thể tham chiếu workbook Digital Marketing ứng dụng AI & Automation hiện tại
để xem cấu trúc session, e-learning, project guidance và mentor support. Chỉ
dùng số liệu đã xác minh từ workbook hoặc user. Nếu chưa xác nhận thời lượng một
session, ghi `PROPOSED_ASSUMPTION`, không biến thành định mức chính thức.

## Hybrid sequencing

Một learning unit nên mô tả:

1. Prework/e-learning để tạo nền.
2. Live/Zoom để demo, diagnose, coach và xử lý misconception.
3. Practice/project để tạo work artifact.
4. Mentor/peer feedback để sửa.
5. Assessment và reflection để chứng minh transfer.

Không dùng live để đọc lại toàn bộ e-learning. Không đẩy practice quan trọng vào
“tự học” nếu learner cần feedback hoặc tool environment. Với tool có chi phí,
privacy hoặc account friction, quy định tool chính, fallback và access check.

## Capacity checks

Review tối thiểu:

- Tổng giờ/tuần và thời gian cao điểm.
- Tỷ lệ live với asynchronous và applied practice.
- Tải practice/project so với level đầu vào.
- Số lượng tool/account phải học đồng thời.
- Feedback capacity của giảng viên/mentor.
- Có đủ thời gian cho capstone, revision và portfolio polish hay không.

Không đặt target tỷ lệ modality cố định cho mọi program; giải thích trade-off theo
learner, occupation, delivery model và evidence.
