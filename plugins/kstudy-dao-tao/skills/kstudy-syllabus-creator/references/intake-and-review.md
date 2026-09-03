# Tiếp nhận nguyên liệu + Hỏi làm rõ + Vòng review

Mục tiêu: không bao giờ bịa khi thiếu dữ liệu, và không giao học liệu chưa đạt. Skill phải rà soát → hỏi → build → review lặp.

## 0. Quy tắc không tự ý bịa thông tin định danh (áp dụng xuyên suốt A–C)

`title` (tên khóa chính thức), `author` (tên người chủ trì biên soạn), và `code` (mã khóa) là **thông tin định danh** — xuất hiện trên mọi tài liệu giao cho học viên/đối tác. Dù file input có vẻ chứa gợi ý (ví dụ 1 sheet Excel ghi tên khóa khác với tên vừa nghe qua lời user, hoặc suy luận được ai là tác giả từ ngữ cảnh), **không tự đặt giá trị này vào course.json dưới bất kỳ hình thức nào** — kể cả khi gắn nhãn rõ "đây là đề xuất, báo nếu cần đổi". Luôn hỏi trực tiếp qua AskUserQuestion và chờ user xác nhận/cung cấp giá trị chính xác TRƯỚC KHI build. Sai các trường này thì phải làm lại toàn bộ 3 file, tốn công hơn nhiều so với các trường nội dung khác (nơi đề xuất-rồi-sửa vẫn ổn).

## A. Rà soát & phân tích nguyên liệu (làm TRƯỚC khi hỏi)

Quét TẤT CẢ file trong thư mục dự án + file đính kèm (Excel khung chương trình, syllabus docx/xlsx, danh sách link, ảnh/logo). Với mỗi trường khóa học, gán trạng thái:

- `[CÓ]` — trích được, ghi rõ nguồn (file/sheet/dòng).
- `[SUY RA]` — không có sẵn nhưng suy luận hợp lý được, ghi rõ giả định.
- `[THIẾU]` — không có / mơ hồ / mâu thuẫn → phải hỏi.

Danh mục soát, xếp theo mức ảnh hưởng chất lượng:

**Nhóm 0 — định danh, KHÔNG đề xuất mặc định, hỏi trực tiếp (xem §0):**
- Tên khóa chính thức (`title`), mã khóa (`code`), tên người chủ trì biên soạn (`author`).

**Nhóm 1 — thiếu là PHẢI hỏi (quyết định chất lượng học liệu):**
- Đối tượng học viên + trình độ (chi phối ai_context, độ khó, ví dụ).
- **Điều kiện tiên quyết để học môn này** (`prerequisites`) — LUÔN hỏi, kể cả khi có vẻ môn không cần điều kiện gì (vẫn cần user xác nhận "không có điều kiện" thay vì tự bỏ qua). Câu hỏi mẫu: "Điều kiện học môn này là gì?" Có thể là điều kiện kỹ năng/thiết bị (vd: dùng máy tính/smartphone, truy cập internet và mạng xã hội thành thạo, soạn thảo văn bản Tiếng Việt, trình độ học vấn tối thiểu) hoặc điều kiện đã hoàn thành 1 môn khác trong hệ thống Kstudy (vd môn AI Media yêu cầu đã hoàn thành Enter AI; môn Social Content yêu cầu đã hoàn thành Enter Digital) — hỏi rõ **mã** môn tiên quyết đó để ghi vào `required_courses`.
- Outcome khóa + capstone (sản phẩm cuối học viên nộp).
- **Tổng quan hành trình khóa** (`curriculum_overview` → map `courses.curriculum_md`) — 1 đoạn ngắn mô tả học viên đi từ đâu đến đâu qua các bài, KHÔNG lặp mô tả từng bài (script tự nối lộ trình). Trường này BẮT BUỘC không trống (QA FAIL nếu thiếu).
- 6 trục radar + skill_tags — đề xuất từ nội dung nhưng PHẢI cho user xác nhận (ảnh hưởng Portfolio + cách Mentor chấm quiz). Chỉ dùng cho xlsx import, không hiện trong docx.
- **Khung năng lực KASH** (`kash`) — đề xuất từ `objectives`/`concepts`/`gate`/`capstone_artifact` toàn khóa, gồm 4 nhóm Kiến thức/Kỹ năng/Thái độ/Thói quen; Kiến thức & Kỹ năng gắn cấp Bloom (`pedagogy.md` §2). PHẢI cho user xác nhận trước khi đưa vào bản chính thức — đây là mục hiện trong docx thay cho Radar Portfolio.
- Mô tả AI-only cho mỗi tài nguyên (link không mở được → hỏi 1 dòng nội dung; KHÔNG bịa).
- Bài nào = capstone (is_final, 50%).

**Nhóm 2 — nên xác nhận (suy ra được nhưng dễ sai):**
- Số buổi + map bài↔buổi (`session_idx`) + hình thức LT/TH (`format_type`, khác `default_mode`) + thời lượng.
- Mạch bài → level (`sort_order`, thứ tự tuyến tính — độc lập với số hiển thị "Bài X.Y").
- Mô tả ngắn khóa + video giới thiệu URL.
- Màu khóa (color) + logo (mặc định dùng logo đóng gói sẵn trong skill nếu dự án không có logo riêng).

**Xuất "Intake report" gửi user** — ngắn, dạng bảng/bullet 3 cột: trường | trạng thái | giá trị/giả định/ghi chú. Đặt Nhóm 1 lên trước. Kèm mục **Độ dày bài** (đủ/mỏng/rất mỏng) + danh sách **Đề xuất làm giàu** cho bài mỏng (khái niệm thiếu / ví dụ thực chiến / lỗi sai phổ biến — xem `pedagogy.md` §5).

## B. Hỏi làm rõ (clarification)

Sau Intake report, hỏi để lấp `[THIẾU]` + xác nhận `[SUY RA]`. Nguyên tắc:

- Dùng AskUserQuestion. Gom **2–4 câu/lượt**, ưu tiên Nhóm 1 trước. Không hỏi thứ user đã cung cấp.
- Mỗi câu là multiple-choice, **phương án đề xuất đứng đầu (Recommended)** + luôn chừa chỗ user nhập tự do.
- Mỗi đề xuất kèm **lý do ngắn** (vì sao đề xuất vậy) để user quyết nhanh.
- Câu hỏi rút từ chính nội dung khóa (cụ thể), không hỏi chung chung.

Bộ câu hỏi mẫu (chỉ hỏi cái còn thiếu/cần xác nhận):
1. **Đối tượng & trình độ:** người mới / có nền tảng / nâng cao / khác.
2. **Điều kiện tiên quyết:** "Điều kiện học môn này là gì?" — kỹ năng/thiết bị/trình độ học vấn, và/hoặc đã hoàn thành môn nào khác (hỏi rõ mã môn đó). LUÔN hỏi câu này, không tự cho là "không có điều kiện gì".
3. **Outcome + capstone:** xác nhận sản phẩm cuối (đề xuất từ nội dung) hay đổi.
4. **Radar 6 trục:** trình 6 trục + skill_tags đề xuất → Đồng ý / Đổi tên trục / Gộp-tách tag. (Dữ liệu này chỉ vào xlsx import, không hiện trong docx.)
4b. **Khung năng lực KASH:** trình 4 nhóm Kiến thức/Kỹ năng (kèm cấp Bloom đề xuất) /Thái độ/Thói quen đúc kết từ nội dung khóa → Đồng ý / Sửa mục / Bỏ mục. Đây là mục hiện trong docx thay cho Radar.
5. **Buổi học:** số buổi + map bài + hình thức + thời lượng (đề xuất) → xác nhận/đổi.
6. **Capstone & trọng số:** chốt bài cuối môn (50%).
7. **Tài nguyên thiếu:** link/mô tả còn trống → nhập, hoặc để `[CHỜ LINK]`/`[CHỜ MÔ TẢ]`.
8. **Nhận diện khóa:** mã / màu / logo / video giới thiệu → xác nhận giá trị đề xuất.
9. **Làm giàu bài mỏng:** với mỗi bài mỏng, trình danh sách đề xuất (khái niệm thiếu / ví dụ thực chiến / lỗi sai) → **Nhận tất cả / Chọn từng mục / Bỏ qua**. Chỉ đưa mục được duyệt vào course.json. KHÔNG bịa số liệu/nguồn. Chi tiết `pedagogy.md` §5.

Trả lời xong → chốt `course.json`. Nếu user bảo "tự quyết" → dùng đề xuất, ghi rõ đã giả định gì.

## C. Vòng review chất lượng (sau khi build)

### C1. Tự kiểm trước khi trình — Quality Scorecard
Chạy `build_kstudy_outputs.py` (QA tự động: mã khóa, ngân sách token, `prerequisites` không trống, `curriculum_overview` không trống, `kash` không trống, radar 6 trục, skill_tag consistency, 1 capstone, đếm `[CHỜ]`, thiếu rubric, không marker runtime cấm). Rồi tự chấm **scorecard 6 tiêu chí**, mỗi tiêu chí: **Đạt / Một phần / Chưa** + bằng chứng 1 dòng. Mọi tiêu chí phải **Đạt** mới trình; "Một phần"/"Chưa" → sửa rồi chấm lại.

| # | Tiêu chí | Đo bằng |
|---|---|---|
| 1 | Alignment | mỗi objective được gate/capstone kiểm tra (đối chiếu tay) — `pedagogy.md` §1 |
| 2 | Bloom + scaffolding | objectives dùng động từ đo được; độ khó tăng dần qua level — §2,3 |
| 3 | Lean AI | ai_context/content trong ngân sách, keyword-first (QA script) |
| 4 | Phủ tài nguyên + sạch [CHỜ] | mỗi bài ≥1 tài nguyên có mô tả AI; QA hết [CHỜ] |
| 5 | Radar/skill_tag | đúng 6 trục, tag khớp (QA script) |
| 6 | Đánh giá có rubric | gate rõ + rubric đạt/khá/tốt mỗi bài — §4 |

Trình scorecard này cho user ở C2 (cho thấy chất lượng đã được kiểm).

### C1b. Review phản biện độc lập (trước khi trình)
Sau khi tự chấm scorecard, chạy **1 phản biện độc lập** để soi bằng con mắt khác — xem `references/reviewer-agent.md`. Sửa hết điểm "Chưa"/"Một phần" critic chỉ ra; verdict "CHƯA" thì KHÔNG trình. Đây là chốt chặn chất lượng quan trọng nhất vì người soạn tự review hay bỏ sót.

### C2. Trình cho user review
Present `.docx` (syllabus chính thức) + `.html` (đọc nhanh, có nút Copy). KHÔNG kèm `.pdf` trừ khi user đã yêu cầu (xem §PDF không xuất mặc định trong SKILL.md). Kèm: tóm tắt QA + **điểm cần user để mắt** (vd radar, `kash`, capstone, tài nguyên còn `[CHỜ]`, giả định đã dùng, `prerequisites` nếu còn thiếu).

### C3. Thu feedback có cấu trúc
Hỏi user "đạt chưa?" theo từng khía cạnh, gọn:
- Nội dung bài đúng/đủ? Độ khó hợp đối tượng?
- `ai_context` / `content` đủ cho AI Mentor hiểu?
- Radar / skill_tags hợp lý? Khung năng lực KASH đủ/đúng cấp Bloom?
- Tài nguyên đủ/đúng?
- Trình bày docx.

### C4. Sửa & lặp
Áp feedback vào `course.json` → build lại → trình lại (C2). Mỗi vòng **chỉ sửa phần được góp ý**, giữ phần đã duyệt. Lặp C2–C4 đến khi user duyệt ("đạt"/"ok") hoặc feedback rỗng (mọi mục ổn).
