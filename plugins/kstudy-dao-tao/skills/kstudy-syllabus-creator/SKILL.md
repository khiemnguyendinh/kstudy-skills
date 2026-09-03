---
name: kstudy-syllabus-creator
description: >-
  Tạo SYLLABUS (đề cương khóa học) Kstudy AI Mentor từ khung chương trình Excel/slide nháp/link,
  tên khóa + tác giả do user xác nhận. Bước Syllabus trong pipeline Kstudy (sau Curriculum,
  trước Lesson Plan/Slide/Video/Quiz) — CẤM soạn các bước sau. Xuất 3 file: import .xlsx khớp
  /admin/curriculum (6 sheet, gồm Radar); .html giảng viên có nút Copy; .docx syllabus rút gọn
  (6 mục + Khung năng lực KASH chuẩn Bloom, không PDF/rubric/Radar, đúng brand
  kstudy-design-system); kèm course.json contract (schema_version 2, approved) bàn giao cho
  kstudy-lesson-plan-creator. ai_context lean 150-250 từ; content mỗi bài 300-600 từ có cấu trúc,
  không marker runtime. Dùng
  khi user nói: tạo/soạn syllabus, soạn khóa học, onboard/import khóa học, ngữ cảnh khóa học,
  radar portfolio, skill_tag, khung năng lực KASH, khung chương trình, /admin/curriculum,
  handoff sang lesson plan, resources index — kể cả không nhắc tên skill. Không dùng cho đề cương
  Sở GD&ĐT, hoặc khi đã có Syllabus duyệt cần bước sau (dùng kstudy-lesson-plan-creator).
---

# Tạo Syllabus cho Kstudy AI Mentor

Biến tài liệu môn học thành **3 file giao cho giảng viên / hệ thống** + **contract/handoff**:

1. **`MÃ - kstudy import - TÊN.xlsx`** — khớp template `/admin/curriculum`, import 1 phát đủ mọi tab. File máy đọc.
2. **`MÃ - Kstudy template - TÊN.html`** — giảng viên đọc; mỗi trường có nút Copy để dán tay vào input AI Mentor.
3. **`MÃ - Kstudy Syllabus - TÊN.docx`** — syllabus chính thức, cấu trúc **rút gọn** (xem §Cấu trúc docx bên dưới), branding đúng `kstudy-design-system` (logo, font, màu), phân cấp Heading 1/2/3 thật của Word.
4. **`course.json`** — nguồn sự thật duy nhất của môn, lưu ở **gốc thư mục môn**; là đầu vào bắt buộc của bước Lesson Plan (xem §Ranh giới & bàn giao).
5. **`handoff_summary.md`** — tóm tắt quyết định đã duyệt để bước Lesson Plan không hỏi lại thông tin nền.
6. **`ThamKhao/resources.index.json`** — registry tài nguyên/link đã biết, trạng thái xác minh và map bài/buổi để tránh kiểm tra trùng.

**Không xuất PDF mặc định.** Chỉ tạo PDF nếu user yêu cầu rõ ràng — mặc định chỉ giao `.docx` (rubric chấm điểm + `.pdf` là dư thừa ở giai đoạn syllabus, học viên/giảng viên chỉ cần bản gọn để đọc/trình bày).

Cả 3 sinh từ **1 file `course.json`** bằng script `scripts/build_kstudy_outputs.py`. Việc của model = soạn `course.json` đúng & lean; script lo định dạng, branding, khớp schema. Không bao giờ tự gõ tay xlsx/docx — luôn qua script để nhất quán.

## Ranh giới skill & bàn giao — contract (quy tắc bắt buộc)

**Điểm dừng của skill này = syllabus + course.json.** TUYỆT ĐỐI KHÔNG sinh các sản phẩm thuộc bước sau, dưới mọi hình thức và mọi mức chi tiết: lesson plan / kế hoạch bài dạy, slide outline, kịch bản hoặc outline video e-learning / micro-learning, kịch bản demo trên lớp, quiz. Kể cả khi user yêu cầu "làm luôn" trong cùng phiên → trả lời: syllabus xong, các sản phẩm đó thuộc skill `kstudy-lesson-plan-creator`, và chỉ nên làm SAU khi syllabus được duyệt (để không phải làm lại học liệu khi syllabus đổi). Lý do cấm cứng: mức chi tiết giảng dạy sinh ở bước syllabus sẽ trùng lặp và lệch chuẩn với bộ học liệu chính thức sinh ở bước sau.

**Contract `course.json`** (đầy đủ field xem `references/course-schema.md`):

- `schema_version: 2` — bắt buộc. Đổi schema → tăng số này và cập nhật đồng thời `course-schema.md` (skill này) + `lesson-json-schema.md` (kstudy-lesson-plan-creator).
- `approved: false` trong mọi vòng nháp. **Chỉ đặt `true` + điền `approved_date` (YYYY-MM-DD) khi user tuyên bố duyệt bản cuối.** `kstudy-lesson-plan-creator` sẽ TỪ CHỐI chạy nếu `approved != true`.
- `version: 1` khi duyệt lần đầu. **Sửa syllabus sau khi đã duyệt** → tăng `version`, thêm 1 dòng vào `changelog[]` (version, date, summary — ghi rõ bài/buổi nào đổi), giữ `approved: true` nếu bản sửa cũng được duyệt. Đồng thời báo user: các Lesson Plan đã soạn cho những buổi bị ảnh hưởng cần rà lại (lesson-plan-creator tự phát hiện lệch qua fingerprint và đọc `changelog` để biết sửa gì).

**Handoff sau duyệt** (chi tiết xem `references/pipeline-handoff.md`):

- Khi user duyệt bản cuối, ngoài cập nhật `approved: true`, phải sinh/cập nhật `handoff_summary.md` và `ThamKhao/resources.index.json` bằng:
```
python scripts/build_handoff_outputs.py course.json .
```
- `handoff_summary.md` ghi quyết định đã chốt: đối tượng, prerequisites, outcome/capstone, KASH, radar, map buổi, giả định và changelog gần nhất.
- `resources.index.json` là registry tài nguyên dùng chung cho lesson-plan-creator; không thay thế `resources[]` trong `course.json`, chỉ giúp tránh xác minh/lập danh mục trùng lặp.
- Nếu sửa syllabus sau duyệt, chạy lại script này sau khi cập nhật `course.json` và `changelog[]`.

## Cấu trúc thư mục môn (chuẩn chung pipeline — tạo/tuân thủ ngay từ skill này)

```
<Thư mục môn>/
├── course.json          ← contract, nguồn sự thật duy nhất (skill này tạo & cập nhật)
├── handoff_summary.md   ← tóm tắt bàn giao sau khi syllabus được duyệt
├── conventions.md       ← quyết định style học liệu (kstudy-lesson-plan-creator tạo sau pilot)
├── 01_Syllabus/         ← 3 file output của skill này (xlsx, html, docx)
├── 02_LessonPlan/
│   └── Buoi_<N>/        ← lesson_seed.json + bộ 4 file mỗi buổi (bước sau)
└── ThamKhao/            ← khung chương trình gốc, ebook, PDF, slide nháp, resources.index.json
```

Ingest đọc từ `ThamKhao/` (hoặc file user đưa); output ghi vào `01_Syllabus/`; `course.json` luôn ở gốc. Thư mục dự án chưa theo cây này → tạo đúng cây, không phát minh tên khác.

## Không tự ý bịa thông tin định danh (quy tắc bắt buộc)

**Tên khóa học, tên người chủ trì biên soạn (author), và mọi trường định danh khác KHÔNG được tự đặt giá trị** — kể cả khi có vẻ suy ra được từ file input (ví dụ 1 sheet Excel ghi tên khóa khác với tên user vừa nói miệng), và kể cả khi bạn định nói rõ "đây là đề xuất, báo tôi nếu cần đổi". Phải **dừng lại, hỏi rõ, và chờ user xác nhận hoặc tự cung cấp** giá trị chính xác TRƯỚC KHI đưa vào `course.json` hay bất kỳ file nào.

Lý do: tên khóa/tên tác giả là thông tin xuất hiện trên mọi tài liệu giao cho học viên/đối tác — sai thì phải build lại toàn bộ 3 file. Một giá trị "đề xuất tạm" vẫn có rủi ro bị dùng nhầm nếu user duyệt vội các phần khác mà không để ý dòng đó.

Áp dụng cho: `code`, `title`, `author`, `color`, `logo`, `prerequisites` nếu không có trong input rõ ràng — hỏi qua `AskUserQuestion` (nhóm cùng lượt hỏi làm rõ ở bước 2), không điền placeholder rồi build luôn.

## Hệ chạy thế nào (đọc trước khi viết)

AI Mentor ghép prompt mỗi lượt từ nhiều layer (course/program, bài hiện tại, hồ sơ học viên, trí nhớ, quy tắc output). Các trường ta sinh map vào:

| Trường course.json → sheet import | Layer | Ai đọc |
|---|---|---|
| `ai_context` (Info) | Course/Program | AI |
| `curriculum_overview` → `curriculum_md` (Info) | Course/Program (tổng quan + lộ trình) | AI |
| lesson `content` (Lessons) | Bài hiện tại | AI |
| lesson `resources` mô tả | Bài hiện tại (mô tả) | AI (mô tả) + học viên (link) |
| sessions / assignments / radar | đánh giá, lịch | hệ thống + học viên |

**Ngân sách khác nhau theo field, không phải "càng ngắn càng tốt":** `ai_context` (course-level) là layer bị cắt sớm khi context đầy → giữ lean 150–250 từ, keyword-first. `content` (từng bài, field chatbot dùng để DẠY) phải **ĐỦ** để Mentor dạy không chung chung — 300–600 từ, có cấu trúc 6 mục theo `COURSE_CONTENT_GUIDELINE.md` §3 (xem `references/ai-context-style.md`). Đừng áp công thức "nén tối đa" của `ai_context` sang `content` — hai field khác mục đích.

**Marker runtime — CẤM sinh dưới mọi hình thức, ở mọi field:** `[BÀI TẬP]` `[ĐIỂM: XX/100]` `[QUIZ_INLINE]` `[QUIZ_RESULT]` `[LEVEL_UP]` `[COMPLETE_LEVEL: N]` `[CHOICES]` là control signal hệ thống (frontend/backend) tự sinh đúng thời điểm để chấm điểm/mở level/hỏi quiz — grading luôn deterministic phía backend, Mentor/skill KHÔNG được tự chấm hay tự mở level qua marker nhúng sẵn trong content. Không nhúng các chuỗi này (kể cả để "chừa chỗ") vào `ai_context`, `curriculum_overview`, `description`, `content`, hay mô tả resource. Script build/validate tự quét và FAIL nếu phát hiện — xem `references/course-schema.md` §Marker runtime cấm.

**Không leak global:** đừng nhồi persona/tone/quy tắc định dạng vào `ai_context`/`content` — đó thuộc layer output rules riêng của hệ thống. Các field ta soạn chỉ chứa **kiến thức môn học**.

## Quy trình 6 bước

**1. Ingest + rà soát.** Đọc `curriculum-rd.json` trước nếu được bàn giao từ `kstudy-course-planner`, rồi đọc TẤT CẢ file trong thư mục dự án (khung chương trình Excel, syllabus/slide nháp, danh sách link, logo). Dùng skill `xlsx`/`docx`/`pdf` hoặc pandas/python-docx. Lập **Intake report**: mỗi trường gán `[CÓ]` (nguồn) / `[SUY RA]` (giả định) / `[THIẾU]`. Danh mục đầy đủ: `references/intake-and-review.md` §A. Link không mở được → giữ URL, KHÔNG bịa nội dung. Chấm **độ dày mỗi bài** (đủ/mỏng — nguồn thật quá sơ sài để soạn đủ 300–600 từ có cấu trúc ở bước 4) để chuẩn bị đề xuất làm giàu. Nếu nguồn nháp là tài liệu của đơn vị/tác giả khác (brand/mô hình riêng của họ) → chỉ dùng làm tham khảo ý tưởng/cấu trúc, viết lại 100% nội dung + ví dụ theo đúng đối tượng khóa, không copy nguyên văn.

**2. Hỏi làm rõ.** Trình Intake report rồi hỏi user lấp `[THIẾU]` + xác nhận `[SUY RA]`: **tên khóa + mã khóa (không tự đặt — xem §Không tự ý bịa thông tin định danh)**, tên người chủ trì biên soạn, đối tượng & trình độ, outcome/capstone, **điều kiện tiên quyết để học môn này** (xem `prerequisites` trong `course-schema.md` — LUÔN hỏi câu "Điều kiện học môn này là gì?" trước khi soạn course.json, không tự suy đoán/bỏ qua kể cả khi có vẻ môn không cần điều kiện gì), 6 trục radar, buổi học (số buổi + hình thức LT/TH mỗi buổi), tài nguyên thiếu mô tả, màu/logo. Dùng AskUserQuestion gom 2–4 câu/lượt, mỗi câu kèm phương án đề xuất + lý do (trừ tên khóa/tác giả — mục đó hỏi trực tiếp, không kèm phương án mặc định). KHÔNG bịa khi thiếu — hỏi. §B. **Mã khóa:** 6 ký tự A–Z/0–9 ALL CAPS; input ≠ 6 → tự chuẩn hóa (`AIVID01`(7)→`AIVD01`), báo user. Bài mỏng → trình **đề xuất làm giàu** (khái niệm/ví dụ/lỗi sai) cho user chọn nhận/bỏ, không bịa (`pedagogy.md` §5).

**3. Dựng traceability, radar 6 trục + skill_tag, và khung năng lực KASH.** Kế thừa `JT/COMP/PLO` từ `kstudy-course-planner`; khóa `CLO`, evidence direction, rubric direction và resource mapping cho từng lesson theo contract chung `~/.claude/skills/kstudy-curriculum-design/references/traceability-contract.md`; upstream thiếu → ghi `NEEDS_INPUT`, không tạo ID giả. Radar (sau khi user chốt; tag nhúng vào từng bài) — xem `references/skill-tags-radar.md`: 12–24 tag canonical (snake_case) → gom đúng 6 trục → mỗi bài 2–4 tag thuộc 1 trục. Radar **chỉ dùng cho xlsx import** (Portfolio hệ thống) — không còn hiện trong docx. Song song, đúc kết **`kash`** (course-level, field `knowledge`/`skill`/`attitude`/`habit`) từ toàn bộ `objectives`/`concepts`/`gate`/`capstone_artifact` của các bài: mỗi mục Kiến thức/Kỹ năng gắn 1 cấp Bloom (`references/pedagogy.md` bảng động từ) theo đúng scaffolding của khóa (level đầu → Nhớ/Hiểu, level giữa → Áp dụng/Phân tích, level cuối/capstone → Đánh giá/Sáng tạo); Thái độ/Thói quen không gắn Bloom. Đây là nội dung hiện ở mục "5. Khung năng lực (KASH)" trong docx, thay cho Radar Portfolio cũ.

**4. Soạn `course.json`.** Theo `references/course-schema.md` (field cấu trúc bài). Điền `schema_version: 2`, `approved: false`, `version: 0` (nháp). Kế thừa `design_depth`: `LITE` cho micro-course, `STANDARD` mặc định cho B2C, `FULL` cho chương trình nghề dài hạn/B2B — độ sâu chỉ đổi mức research/review, không tạo thêm file output. Mỗi lesson phải có `clo_ids`, `lesson_outcome_ids`, `evidence_ids`, `rubric_ids`, `resource_ids` và `traceability.approval_status`; `activity_ids` để rỗng vì activity chi tiết thuộc `kstudy-lesson-plan-creator`. `alignment_status` giữ `PROPOSED` cho tới khi Constructive Alignment QA đạt. Viết `curriculum_overview` (tổng quan hành trình học viên — script tự nối thêm lộ trình từng bài thành `curriculum_md`, KHÔNG được để trống). Mỗi **Bài = 1 Level** (`sort_order`, số tuyến tính 1..N — dùng cho hệ thống/Level). Mỗi bài gắn thêm `session_idx` = buổi nó thuộc về, để script tự tính số hiển thị **"Bài X.Y"** (X = buổi, Y = thứ tự bài trong buổi đó) cho docx/html — không tự gõ tay "Bài 1.1" vào `title`. Viết `why_important`/`how_to`/`example` + các field khác theo `references/ai-context-style.md` (content phải ĐỦ 300–600 từ có cấu trúc, không phải lean tối đa); theo chuẩn sư phạm `references/pedagogy.md`: mục tiêu Bloom đo được + alignment mục tiêu↔gate + scaffolding độ khó tăng dần + **rubric đạt/khá/tốt mỗi gate** (rubric vẫn bắt buộc trong `course.json` để Mentor chấm — chỉ không hiện trong docx, xem §Cấu trúc docx). `mistakes`/`ai_application` là **field tùy chọn, không bắt buộc mỗi bài**: môn thuần AI thì thường không cần khai `ai_application` riêng (cả môn đã là ứng dụng AI); môn không phải AI thì ưu tiên có gợi ý `ai_application` nếu hợp, không ép. `mistakes` khi có thì script tự gộp vào mục "Lỗi thường gặp" của `content` và cuối "Nội dung chính" của docx. Mỗi `resources[]` cần thêm `type` (`video_youtube`/`pdf`/`website`/…) và `topic` (chủ đề cụ thể của link đó, có thể khác `topic` của cả bài) bên cạnh `title`/`description`/`url` sẵn có. Mỗi `sessions[]` cần thêm `format_type` (`"LT"`/`"TH"`/`"LT/TH"`) — hình thức Lý thuyết/Thực hành hiển thị ở docx, **khác** với `default_mode` (online/offline/hybrid, dùng cho hệ thống). Bám ngân sách dưới. **Không nhúng marker runtime** (xem §Hệ chạy thế nào) vào bất kỳ field nào.

**5. Build + QA.** Chạy:
```
python scripts/build_kstudy_outputs.py course.json <outdir>
```
→ 3 file (xlsx import, html, docx — KHÔNG có pdf trừ khi chạy `--pdf`) + QA tự động (mã khóa, ngân sách token, `prerequisites` không trống, `curriculum_overview` không trống, `kash` không trống, radar 6 trục, skill_tag consistency, 1 capstone, đếm chỗ `[CHỜ]`, không marker runtime cấm, `design_depth` hợp lệ, traceability + `assessment_blueprint` theo contract). Sửa mọi FAIL; WARN `prerequisites`/`kash` trống → quay lại hỏi/đúc kết, đừng bỏ qua (thiếu `kash` = mục 5 docx trống). Nếu cần bản in/PDF, chạy thêm `soffice --headless --convert-to pdf "<file>.docx"` sau khi user đã duyệt bản docx cuối — đừng tạo PDF ở mọi vòng nháp.

**6. Vòng review — lặp tới khi user duyệt.** Tự kiểm bằng **Quality Scorecard 7 tiêu chí** (alignment, Bloom/scaffolding, lean, phủ tài nguyên, radar, rubric, traceability) — mọi tiêu chí phải Đạt → **chạy phản biện độc lập** (`references/reviewer-agent.md`: spawn 1 agent critic chấm draft, sửa hết điểm Chưa/Một phần) → trình `.docx` + `.html` + scorecard + tóm tắt critic cho user → thu feedback theo khía cạnh → sửa `course.json` → build lại → lặp. Mỗi vòng chỉ sửa phần được góp ý, và **chỉ sửa field đã confirm KHÔNG phải do tự bịa** — nếu feedback đụng tới tên khóa/tác giả/mã khóa, áp giá trị user cho chính xác, không tự suy diễn thêm. **Khi user tuyên bố duyệt bản cuối:** đặt `approved: true`, `approved_date` = ngày duyệt, `version: 1` (hoặc tăng version nếu là bản sửa sau duyệt + thêm dòng `changelog`), lưu `course.json` về gốc thư mục môn, chạy `python scripts/build_handoff_outputs.py course.json .`, rồi thông báo bước tiếp theo là `kstudy-lesson-plan-creator`. Chi tiết vòng review: `references/intake-and-review.md` §C.

## Cấu trúc docx (khác template kỹ thuật của xlsx/html)

Bảng **"1. Thông tin chung"** (đầu docx) có dòng **"Điều kiện tiên quyết"** ← `prerequisites.description` (+ nếu `required_courses` không rỗng, script tự nối thêm mã các môn phải hoàn thành trước). Thiếu field này → QA WARN, không chặn build nhưng phải hỏi lại user trước khi giao bản chính thức.

Mỗi bài trong "3. Nội dung bài học" render đúng thứ tự, mỗi nhãn là **Heading 3 thật** (không phải đoạn bold giả heading — giữ đúng outline Word H1 > H2 > H3):

1. **`Bài X.Y: <title>`** — Heading 2, số X.Y tính từ `session_idx` + thứ tự trong buổi, KHÔNG lấy từ `title` (title chỉ chứa tên bài, sạch, không tự gắn số).
2. **Mô tả** — text trực tiếp ngay dưới heading, KHÔNG có nhãn "Mô tả:" đứng trước.
3. **Mục tiêu:** (H3) — bullet, từ field `objectives`.
4. **Nội dung chính:** (H3) — gộp `why_important` (câu mở, in nghiêng) + `topic` + `concepts` (bullet 2 cấp) + `how_to` (đánh số) + `example` (Bối cảnh/Cách làm/Kết quả kỳ vọng) + `main_content` nếu có (đoạn văn bổ sung tùy chọn, không giới hạn ngân sách vì chỉ vào docx) + `mistakes` nếu có (gộp thành 1 câu cuối, không tách nhãn). Cùng nguồn field với `content` sinh cho xlsx (xem `course-schema.md`). KHÔNG hiện `ai_application`, KHÔNG hiện `lien_he` riêng ở syllabus — mức chi tiết đó dành cho Lesson Plan (bước sau).
5. **Tài nguyên & công cụ:** (H3) — liệt kê `resources[]`: tên công cụ + mô tả + url.
6. **Bài tập:** (H3) — `gate` + `capstone_artifact` + tên bài tương ứng nếu có. **KHÔNG in `rubric` (đạt/khá/tốt)** ở syllabus — rubric vẫn nằm trong `course.json`/xlsx để Mentor chấm, chỉ ẩn khỏi bản đọc cho giảng viên/học viên.

Bảng "2. Lịch trình buổi học" cột **Hình thức** hiện `format_type` (LT/TH), không phải `default_mode`.

Mục **"5. Khung năng lực (KASH)"** (cuối docx, trước khối ký tên) ← field `kash`: 4 khối `Kiến thức (Knowledge)` / `Kỹ năng (Skill)` / `Thái độ (Attitude)` / `Thói quen (Habit)`, mỗi khối là bullet list. Kiến thức/Kỹ năng mỗi mục kèm cấp Bloom trong ngoặc (vd "(Áp dụng)"); Thái độ/Thói quen không gắn Bloom. Đây là mục **thay thế "Radar Portfolio"** cũ — Radar (6 trục + skill_tag) vẫn tồn tại và bắt buộc đúng 6 trục, nhưng chỉ phục vụ sheet **Radar** trong xlsx import (Portfolio hệ thống Kstudy AI Mentor), KHÔNG còn hiện cho giảng viên/học viên đọc trong docx. Thiếu `kash` → mục 5 không render (QA WARN, không FAIL).

Branding: logo mặc định đã đóng gói sẵn trong chính skill này (`assets/logo/kstudy-logo-full.png` — bản màu, nền sáng, lấy nguồn từ `kstudy-design-system`; script tự dùng qua `resolve_logo()`, không cần trỏ đường dẫn ngoài). Chỉ đặt `course.json.logo` khi dự án có logo riêng khác bản mặc định. Font "Google Sans Flex", navy `#1D237D` / blue `#247DF9` (đã hard-code sẵn trong script, khớp design system — không tự đổi màu khi chưa hỏi).

## Ngân sách token

| Trường | Ai đọc | Ngân sách | Ghi chú |
|---|---|---|---|
| `description` (course/lesson) | Học viên | 30–50 từ | Văn xuôi mượt |
| `curriculum_overview` | AI | 50–120 từ | Tổng quan hành trình học viên, KHÔNG lặp mô tả từng bài — script tự nối "Lộ trình" từ `lessons[]` thành `curriculum_md` |
| `ai_context` (course) | AI | 150–250 từ | Scope-card: đối tượng, outcome, phạm vi, mạch level, thuật ngữ. Layer bị cắt sớm khi context đầy → giữ lean |
| lesson `content` | AI | 300–600 từ | ĐỦ để dạy, có cấu trúc 6 mục (`references/ai-context-style.md`): vì sao quan trọng, mục tiêu, khái niệm cốt lõi, cách làm thực tế, ví dụ áp dụng, lỗi thường gặp, bài thực hành gợi ý (gồm rubric). `main_content` là field bổ sung TÙY CHỌN, không tính vào ngân sách này |
| resource `description` | AI | ≤15 từ | Keyword + loại + khi nào dùng |
| `fast_track` | AI | 50–100 từ | Skip intro cho học viên giỏi. KHÔNG vào import xlsx (template chưa có cột) → nằm ở html/docx; muốn auto-import thì thêm cột rồi báo |
| `rubric` (dat/kha/tot) | AI + người | ~10–20 từ/mức | Generator nối gọn vào mục "Bài thực hành gợi ý" của `content` — KHÔNG render riêng vào docx |

~1.5 token/từ tiếng Việt. `content` mỗi bài tự đủ (Mentor chỉ inject bài hiện tại, không giả định nhớ bài trước). Script không tự cắt bớt field khi vượt ngân sách — nếu QA báo WARN/FAIL vượt 600 từ, tự rút gọn `concepts`/`how_to`/`example` trước (giữ nguyên `rubric`/`gate`/`capstone_artifact` vì đó là phần hệ thống chấm dựa vào).

## Nguyên tắc vàng

- **Keyword > câu.** "Mục tiêu: phân biệt POD vs POP; viết 1 positioning statement" thắng "Trong bài này học viên sẽ học...".
- **Mỗi bài tự đủ cho AI.** Mentor chỉ thấy L2 + bài hiện tại; đừng giả định nó nhớ bài trước (L5 chập chờn).
- **Resource mô tả = nội dung BÊN TRONG link**, không nhắc lại tên. "Slide 12 trang: 4P, ví dụ Vinamilk" > "Slide bài 1". Tên công cụ thật (đã xác minh URL) — không bịa link, không đoán tên sản phẩm mới; nếu không chắc, `WebSearch` xác minh trước khi đưa vào `resources`.
- **Gate + capstone + rubric nằm trong `content`** (form không có input riêng) để Mentor biết chính xác điều kiện qua bài — nhưng **KHÔNG nhúng marker `[COMPLETE_LEVEL: N]`/`[ĐIỂM: XX/100]` vào đó**: hệ thống (frontend/backend) tự phát marker đúng lúc dựa trên việc chấm deterministic, skill chỉ cung cấp tiêu chí bằng câu văn thường. Dù docx không hiện rubric, `content` vẫn phải có.
- **fast_track ≠ bỏ gate.** Chỉ bỏ nhập đề/warm-up; gate quiz + capstone artifact luôn giữ.
- **Không tự đặt tên khóa/tác giả/mã khóa/điều kiện tiên quyết.** Xem mục riêng ở đầu file.
- **Không lấn sang bước Lesson Plan.** Xem §Ranh giới skill & bàn giao — vi phạm ranh giới = trùng lặp học liệu.
- **Handoff không phải lesson plan.** `handoff_summary.md` và `resources.index.json` chỉ là dữ liệu bàn giao; KHÔNG chứa timeline, demo, slide/video outline hay bài tập chi tiết từng buổi.

## Output

3 file trong `01_Syllabus/` + `course.json` ở gốc thư mục môn + sau duyệt có `handoff_summary.md` và `ThamKhao/resources.index.json` (PDF chỉ khi được yêu cầu). Branding docx/html cố định trong generator, logo mặc định đã đóng gói sẵn trong skill — chỉ cần đặt `course.json.logo` trỏ tới logo trong thư mục dự án nếu khác bản mặc định. Thiếu dữ liệu (link, mô tả bài, đối tượng, màu khóa, **tên khóa, tên tác giả, điều kiện tiên quyết**) → hỏi user gọn từng mục, không bịa. Nếu user chỉ cần dán tay → hướng họ tới file `.html` (nút Copy); cần import nhanh → file `.xlsx`.
