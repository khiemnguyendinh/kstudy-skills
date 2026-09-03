# Schema lesson_seed.json

`lesson_seed.json` là snapshot đầu vào của một buổi học, sinh từ `course.json` đã duyệt trước khi soạn `lesson.json`.

Tạo bằng:

```bash
python scripts/build_lesson_seed.py course.json <buoi>
```

Mặc định file được ghi vào `02_LessonPlan/Buoi_<N>/lesson_seed.json`.

## Mục đích

- Giảm hỏi lại thông tin đã chốt ở syllabus.
- Chống lệch giữa `course.json` và học liệu buổi.
- Gom sẵn bài được phủ, gate, objectives, concepts, KASH, resources và fingerprint.

## Schema

```json
{
  "schema_version": 1,
  "course_fingerprint": "12 ký tự SHA-256 đầu của course.json",
  "course_version": 1,
  "code": "ABC123",
  "course_title": "Tên môn",
  "author": "Người chủ trì biên soạn",
  "buoi": 1,
  "total_buoi": 6,
  "session": {
    "idx": 1,
    "summary": "Tóm tắt buổi",
    "duration_minutes": 120,
    "default_mode": "hybrid",
    "format_type": "LT/TH"
  },
  "covers": [
    {
      "sort_order": 1,
      "display_no": "1.1",
      "title": "Tên bài",
      "description": "Mô tả",
      "topic": "Chủ đề",
      "concepts": ["khái niệm"],
      "objectives": "Mục tiêu",
      "main_content": "Nội dung chính",
      "lien_he": "Liên hệ thực tế",
      "mistakes": ["lỗi hay gặp"],
      "ai_application": ["ứng dụng AI"],
      "gate": "Điều kiện qua level",
      "capstone_artifact": "Sản phẩm nộp",
      "rubric": {"dat": "...", "kha": "...", "tot": "..."},
      "skill_tags": ["tag"],
      "resources": []
    }
  ],
  "course_kash": {},
  "session_gate": ["Gate gộp từ các bài"],
  "resources_from_index": [],
  "source_notes": {
    "handoff_summary": "available | missing",
    "resources_index": "available | missing"
  },
  "open_questions": []
}
```

## Quy tắc dùng

- `lesson_seed.json` không thay thế `course.json`; đây là snapshot để soạn buổi.
- `lesson.json.course_fingerprint` phải dùng đúng `course_fingerprint` trong seed.
- Nếu seed thiếu bài hoặc thiếu gate, quay lại kiểm `course.json.session_idx`/`gate`, không tự chế âm thầm.
- Nếu thêm tài nguyên ngoài seed, ghi rõ trong `lesson.json.online_resources` và flag cho user nếu tài nguyên đó thay đổi scope syllabus.
