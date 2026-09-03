# Schema lesson.json (đầu vào cho build_lesson_outputs.py)

Mỗi buổi trực tiếp = 1 file `lesson.json`. Script sinh 2 file docx: LessonPlan và TaiNguyen-ThamKhao.

## Trường chung
- `schema_version` (int): 2 — khớp `schema_version` của course.json; đổi schema thì cập nhật đồng thời file này + `course-schema.md` của kstudy-syllabus-creator.
- `course_fingerprint` (str): 12 ký tự đầu SHA-256 của file course.json tại thời điểm soạn buổi (lấy bằng `python scripts/validate_lesson.py --fingerprint course.json`). Dùng phát hiện cascade khi syllabus đổi.
- `lesson_seed_file` (str, khuyến nghị): đường dẫn `lesson_seed.json` đã dùng để soạn buổi, thường là `02_LessonPlan/Buoi_<N>/lesson_seed.json`.
- `code` (str): mã môn ALL CAPS, vd "ENTRAI".
- `course_title` (str): tên đầy đủ của môn.
- `buoi` (int), `total_buoi` (int): số thứ tự buổi và tổng số buổi.
- `duration_min` (int): thời lượng buổi, vd 90.
- `format` (str): hình thức, vd "Hybrid (Lý thuyết kết hợp Thực hành)".
- `covers` (str): các bài (lesson) mà buổi này phủ.
- `author` (str): người biên soạn (mặc định lấy từ course.json của môn).
- `title` (str): tên buổi (ngắn, dùng làm tiêu đề).
- `logo` (str, tùy chọn): đường dẫn logo; bỏ trống dùng logo bundle trong assets.

## Lesson Plan
- `kash` (list[[nhóm, mô tả]]): 4 dòng KASH, mô tả dùng động từ Bloom đo được.
- `gate` (list[str]): điều kiện hoàn thành buổi (gộp gate của các bài).
- `timeline` (list[[phút, hoạt động, nội dung, hình thức]]): tổng thời lượng phải khớp `duration_min`.
- `demos` (list[{title, steps[], mistake}]): kịch bản minh họa trên lớp; mỗi bước 1 câu; "mistake" là điểm dễ sai.
- `exercises` (list[[nhãn, nội dung]]): bài tập tại lớp; mỗi mục nêu sản phẩm nộp + tiêu chí đạt.
- `homework` (list[str]): bài tập về nhà, gắn với đồ án cuối khóa.
- `resources_files` (list[str]): tên các file đi kèm (slide .md, video .md, tài nguyên .docx).

## Traceability và thiết kế hoạt động

- `traceability` (object): kế thừa `job_task_ids`, `competency_ids`, `plo_ids`,
  `clo_ids`, `lesson_outcome_ids`, `evidence_ids`, `rubric_ids`, `resource_ids`
  và `approval_status` theo contract chung. `activity_ids` được tạo ở tầng này.
- `miller_level` (str): `KNOWS` | `KNOWS_HOW` | `SHOWS_HOW` | `DOES`.
- `activity_map` (list[object]): mỗi activity có `activity_id`, `zone`
  (`classroom` | `e_learning` | `ai_mentor` | `internet`), `phase`,
  `duration_min` (nếu có), `lesson_outcome_ids`, `evidence_ids` và `formative`.
- `formative_checks` (list[object]): mỗi check có `check_id`, `type`, `minute`
  hoặc `phase`, `target_outcome_ids`, `prompt`, `feedback_action` và có thể có
  `evidence_ids`.
- `udl_options` (object, tùy chọn): `representation`, `action_expression`,
  `engagement`; chỉ thêm phương án thực sự giúp learner tiếp cận/thể hiện năng lực.
- `resource_map` (list[object], tùy chọn): `resource_id`, `title`, `url`, `purpose`
  để liên kết resource với outcome/activity; không thay thế `online_resources`
  và `attached_resources` dùng để build tài liệu.

## Tài nguyên & Tham khảo
- `online_resources` (list[[tên, nội dung sử dụng, url]]): URL đầy đủ; không bịa link.
- `attached_resources` ({folder, note, items[[tên, nội dung, vị trí]]}): tài liệu offline; ghi rõ tên file + vị trí thư mục trong thư mục chung.
- `study_hints` (list[str]): gợi ý học thêm; nếu là YouTube chưa có link cố định thì ghi dạng từ khóa tìm kiếm, bổ sung link khi đã chọn video.

## Quan hệ với lesson_seed.json

- Trước khi soạn `lesson.json`, sinh `lesson_seed.json` bằng `scripts/build_lesson_seed.py`.
- `lesson.json.course_fingerprint` phải trùng `lesson_seed.json.course_fingerprint`.
- `covers`, `gate`, `online_resources`, `kash`, `duration_min` trong `lesson.json` phải trace được về seed/course; nếu thêm ngoài seed, ghi rõ trong phần trình user duyệt.
- Nếu seed báo `open_questions`, xử lý hoặc trình user trước khi build học liệu chính thức.
