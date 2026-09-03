# Pipeline handoff sau khi syllabus được duyệt

Mục tiêu: khóa quyết định ở bước syllabus, giảm hỏi lại ở bước Lesson Plan, tránh xác minh tài nguyên trùng lặp.

## Khi nào tạo

Chỉ tạo/cập nhật sau khi `course.json` đã được user duyệt:

```bash
python scripts/build_handoff_outputs.py course.json .
```

Nếu cần xem trước ở bản nháp, dùng `--allow-draft` và ghi rõ đây chưa phải handoff chính thức.

## Output

1. `handoff_summary.md` ở gốc thư mục môn.
2. `ThamKhao/resources.index.json`.

## `handoff_summary.md`

File này là tóm tắt vận hành cho người/agent soạn học liệu buổi. Nội dung bắt buộc:

- Course identity: code, title, author, version, approved date.
- Điều kiện tiên quyết.
- Mô tả khóa, AI context, outcome/capstone.
- KASH đã duyệt.
- Radar 6 trục + tag.
- Sessions: buổi, thời lượng, hình thức, bài được phủ.
- Changelog gần nhất và điểm cần rà nếu syllabus đổi.
- Open items: `[CHỜ]`, link thiếu, tài nguyên cần xác minh.

Không đưa timeline, demo, slide/video outline, bài tập chi tiết từng buổi vào file này.

## `resources.index.json`

Registry tài nguyên dùng chung, không thay thế `lessons[].resources[]` trong `course.json`.

Schema:

```json
{
  "schema_version": 1,
  "course_code": "ABC123",
  "course_title": "Tên môn",
  "generated_from": "course.json",
  "generated_at": "YYYY-MM-DD",
  "resources": [
    {
      "id": "R001",
      "lesson_sort_order": 1,
      "session_idx": 1,
      "lesson_title": "Tên bài",
      "title": "Tên tài nguyên",
      "type": "website",
      "topic": "Chủ đề link",
      "description": "Mô tả ngắn",
      "url": "https://...",
      "source": "course.json.lessons[1].resources",
      "verification_status": "listed_in_course | needs_url | needs_description",
      "notes": ""
    }
  ]
}
```

## Quy tắc dùng ở bước Lesson Plan

- Đọc `handoff_summary.md` trước khi hỏi user thêm thông tin nền.
- Đọc `resources.index.json` trước khi lập tài nguyên buổi.
- Nếu tài nguyên có `verification_status` không ổn, xử lý ở Lesson Plan bằng cách xác minh hoặc hỏi user; không tự bịa nội dung.
- Nếu phát hiện tài nguyên mới khi soạn buổi, thêm vào tài nguyên buổi; chỉ cập nhật `resources.index.json` khi đó là tài nguyên dùng lại nhiều buổi hoặc user xác nhận đưa vào registry chung.
