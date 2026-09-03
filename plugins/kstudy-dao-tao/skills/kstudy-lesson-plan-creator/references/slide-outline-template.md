# Mẫu đề cương slide bài giảng (.md)

File slide do model soạn tay (không sinh bằng script). Đặt tên: `<CODE>-B<N>-Slide-outline.md`.

## Nguyên tắc wording
- Đối tượng người học: người Việt, mới tốt nghiệp THPT hoặc chưa có kinh nghiệm marketing/công nghệ/AI. Viết giọng giảng dạy, thuyết trình, dễ hiểu.
- **Hạn chế từ tiếng Anh** khi có từ tiếng Việt thay thế hợp lý (vd "trí tuệ nhân tạo" thay cho "AI", "công cụ/tác nhân" thay cho "tool/agent"). Chỉ giữ thuật ngữ tiếng Anh khi là tên tính năng/sản phẩm không có bản dịch chuẩn (Custom Instructions, Gems, ChatGPT).
- Tránh từ khẩu ngữ như "Chốt" — dùng "Tổng kết", "Kết luận".
- Đặt tên mục là "Phần 1: Mở đầu", "Phần 2: ..." (không dùng "Khối").
- Mỗi slide một ý chính, ít chữ, bám phần minh họa.
- Outline này là input cho `kstudy-slide-design` (KSD), không phải thiết kế slide hoàn chỉnh. Lesson Plan chịu trách nhiệm: thông điệp học tập + nội dung ngắn + brief minh họa. KSD chịu trách nhiệm: layout, typography, asset, crop, safe area, xuất HTML/PDF.

## Giới hạn độ dài để KSD dàn trang tốt
- Tiêu đề slide thường: tối đa 48 ký tự hoặc 9 từ.
- Tiêu đề cover/section: tối đa 60 ký tự hoặc 11 từ.
- Eyebrow/tag: tối đa 22 ký tự.
- Bullet: 1 dòng, tối đa 14 từ; mỗi slide 2–4 bullet.
- Tránh tiêu đề 2 mệnh đề dài nối bằng dấu hai chấm. Nếu cần giải thích, đưa phần sau xuống "Thông điệp chính".

## Cấu trúc slide mở đầu/kết thúc bắt buộc
- Trước khi soạn outline, kiểm nội dung chính của buổi liền trước:
  - Nếu buổi N > 1: ưu tiên đọc `02_LessonPlan/Buoi_<N-1>/lesson.json`; nếu thiếu, đọc LessonPlan/Slide-outline buổi trước; nếu vẫn thiếu, suy từ `course.json.sessions` + `course.json.lessons` và ghi rõ giả định. Tóm tắt 3-5 ý chính cho slide "Ôn tập buổi trước".
  - Nếu buổi 1: kiểm syllabus/course.json có môn điều kiện tiên quyết không. Nếu có, chỉ lấy các ý chính đã quy định trong syllabus cho slide ôn tập nhanh; không tự bịa kiến thức ngoài syllabus.
- Slide 1 luôn là trang tiêu đề.
- Buổi 1 có môn điều kiện tiên quyết: sau trang tiêu đề lần lượt là "Ôn tập nhanh môn điều kiện tiên quyết" → "Mục tiêu môn học này" → "Bài tập cuối môn" → "Mục tiêu buổi hôm nay".
- Buổi 1 không có môn điều kiện tiên quyết: sau trang tiêu đề lần lượt là "Mục tiêu môn học này" → "Mục tiêu buổi hôm nay".
- Buổi N > 1: sau trang tiêu đề lần lượt là "Ôn tập buổi trước" → "Mục tiêu buổi hôm nay".
- Cuối buổi luôn có "Tổng kết nội dung hôm nay" → "Nội dung buổi sau". Nếu là buổi cuối, thay "Nội dung buổi sau" bằng định hướng hoàn thiện bài tập/cuối môn dựa trên syllabus, không tự bịa phần học mới.

## Mỗi slide bắt buộc có dòng "Minh họa"
Ghi rõ visual job + LOẠI + mô tả/câu lệnh để KSD chọn đúng asset/layout:
- Proof: ảnh Kstudy thật hoặc ảnh user cung cấp đã duyệt.
- Thinking: sơ đồ, framework, concept map, ma trận, timeline.
- Doing: ảnh chụp màn hình thật + annotation cho demo phần mềm.
- Evidence: biểu đồ, metric card, bảng số liệu; chỉ dùng số liệu đã có nguồn.
- Context: ảnh/screenshot public có nguồn, không giả làm bằng chứng Kstudy.
- Concept: ảnh tạo bằng trí tuệ nhân tạo/Canva cho minh họa khái niệm, không dùng làm proof.
- Họa tiết/icon: chỉ dùng khi giúp đọc nhanh checklist, bước, trạng thái.

Đầu file thêm ghi chú phong cách ảnh chung để nối vào cuối mỗi câu lệnh tạo ảnh:
"tối giản, hiện đại, tông màu xanh navy và xanh dương thương hiệu Kstudy, nền sạch, ánh sáng dịu, không chữ".

## Khung mẫu
```
# Đề cương slide bài giảng — Buổi N: <Tên buổi>

Môn: <Tên> (<CODE>) · Buổi N/T · <phút> phút · Nội dung phủ <các bài>
Traceability: CLO <ids> · Lesson Outcome <ids> · Evidence <ids> · Resource <ids> · Approval <status>
Nguyên tắc trình bày: mỗi slide một ý chính, bám minh họa, hạn chế chữ. Dự kiến ~<số> slide.
Phong cách hình ảnh chung: <chuỗi phong cách ở trên>.

## Phần 1: Mở đầu (0–X phút)

**Slide 1 — Trang bìa**
- Mục tiêu học: <slide này giúp học viên hiểu/làm gì>
- Thông điệp chính: <1 câu ngắn, có thể dài hơn tiêu đề>
- Nội dung: <2–4 bullet ngắn, nếu cần>
- Visual job: <Proof | Thinking | Doing | Evidence | Context | Concept>
- Minh họa: <loại — mô tả/câu lệnh/nguồn/cấu trúc hình>
- Gợi ý KSD: <layout mong muốn nếu có: full-bleed photo, split 60/40, sơ đồ 4 bước, screenshot có annotation...>

**Slide 2 — <Ôn tập buổi trước | Ôn tập nhanh môn điều kiện tiên quyết | Mục tiêu môn học này>**
- Mục tiêu học: <giúp học viên nối kiến thức cũ với buổi hôm nay>
- Thông điệp chính: <1 câu ngắn>
- Nội dung: <3-5 ý chính, lấy từ lesson plan buổi trước hoặc syllabus/course.json>
- Visual job: <Thinking | Context>
- Minh họa: <sơ đồ/timeline/checklist thể hiện các ý cần nhớ>
- Gợi ý KSD: <layout checklist hoặc timeline ngắn>

...
```

Số slide bám theo timeline của Lesson Plan (mỗi phần tương ứng một khối thời lượng).
