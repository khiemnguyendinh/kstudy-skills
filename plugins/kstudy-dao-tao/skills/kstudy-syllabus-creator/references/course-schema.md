# course.json — cấu trúc & map sang 6 sheet import

Model soạn **1 file `course.json`** rồi chạy `scripts/build_kstudy_outputs.py course.json <outdir>`. Script sinh 3 file và map các trường như bảng dưới. Giữ đúng tên khóa (`key`) — script không tự sửa.

## Khung course.json

```json
{
  "schema_version": 2,
  "version": 0,
  "approved": false,
  "approved_date": null,
  "changelog": [
    {"version": 1, "date": "YYYY-MM-DD", "summary": "Duyệt bản đầu. (Các dòng sau: ghi rõ bài/buổi nào đổi để lesson-plan-creator biết cascade.)"}
  ],
  "code": "AIVD01",
  "title": "AI Video Shorts cho YouTube",
  "intro_video_url": "[CHỜ LINK]",
  "color": "#F2545B",
  "logo": "/đường/dẫn/kstudy-logo-full.png  (tùy chọn — bỏ trống thì dùng logo mặc định đóng gói sẵn trong skill)",
  "description": "Mô tả ngắn 30–50 từ, hiển thị học viên.",
  "author": "Tên người chủ trì biên soạn (hiện ở khối ký tên cuối docx; thiếu → [Tên tác giả])",
  "prerequisites": {
    "description": "Điều kiện tiên quyết để học môn này, văn xuôi hiển thị học viên. VD (điều kiện kỹ năng/thiết bị): 'Sử dụng máy tính, smartphone, truy cập internet và mạng xã hội thành thạo; soạn thảo được văn bản Tiếng Việt; tốt nghiệp THCS.' VD (điều kiện hoàn thành môn trước): 'Đã hoàn thành môn Enter AI.'",
    "required_courses": ["Mảng mã các môn PHẢI hoàn thành trước (course.code của môn đó), rỗng [] nếu không có điều kiện dạng này — chỉ ghi mã, không ghi tên đầy đủ"]
  },
  "ai_context": "L2 scope-card 150–250 từ, keyword-first (đối tượng, outcome, phạm vi, mạch level, thuật ngữ lõi).",
  "curriculum_overview": "Tổng quan khóa 50–120 từ: hành trình học viên từ đầu đến cuối khóa (KHÔNG lặp mô tả từng bài — script tự nối phần 'Lộ trình' liệt kê từng bài từ lessons[]). Ghép thành courses.curriculum_md, xem §curriculum_md bên dưới.",
  "design_depth": "LITE | STANDARD | FULL (kế thừa từ Curriculum Design/Course Planner)",
  "alignment_status": "PROPOSED",
  "traceability": {
    "job_task_ids": ["JT-03"],
    "competency_ids": ["COMP-03"],
    "plo_ids": ["PLO-02"],
    "clo_ids": ["CLO-AIVD01-01"],
    "lesson_outcome_ids": [],
    "activity_ids": [],
    "evidence_ids": ["EVID-AIVD01-B01.01"],
    "rubric_ids": ["RUBRIC-AIVD01-B01.01"],
    "resource_ids": [],
    "approval_status": "PROPOSED"
  },
  "assessment_blueprint": [
    {
      "evidence_id": "EVID-AIVD01-B01.01",
      "clo_ids": ["CLO-AIVD01-01"],
      "lesson_outcome_ids": ["LO-AIVD01-B01.01"],
      "rubric_id": "RUBRIC-AIVD01-B01.01",
      "method": "Authentic artifact + rubric",
      "gate": "Điều kiện đạt",
      "approval_status": "PROPOSED"
    }
  ],
  "lessons": [
    {
      "sort_order": 1,
      "session_idx": 1,
      "title": "Tên bài",
      "description": "Mô tả ngắn cho học viên 30–50 từ (đoạn văn).",
      "why_important": "1–2 câu: vì sao học phần này quan trọng với học viên (không sáo rỗng/marketing — nêu hệ quả cụ thể nếu bỏ qua bài này).",
      "topic": "Chủ đề chính của bài",
      "concepts": ["khái niệm 1", "khái niệm 2", "khái niệm 3"],
      "objectives": "Mục tiêu đo được: 1) ...; 2) ...",
      "clo_ids": ["CLO-AIVD01-01"],
      "lesson_outcome_ids": ["LO-AIVD01-B01.01"],
      "evidence_ids": ["EVID-AIVD01-B01.01"],
      "rubric_ids": ["RUBRIC-AIVD01-B01.01"],
      "resource_ids": [],
      "traceability": {
        "job_task_ids": ["JT-03"],
        "competency_ids": ["COMP-03"],
        "plo_ids": ["PLO-02"],
        "clo_ids": ["CLO-AIVD01-01"],
        "lesson_outcome_ids": ["LO-AIVD01-B01.01"],
        "activity_ids": [],
        "evidence_ids": ["EVID-AIVD01-B01.01"],
        "rubric_ids": ["RUBRIC-AIVD01-B01.01"],
        "resource_ids": [],
        "approval_status": "PROPOSED"
      },
      "how_to": ["Bước làm thực tế 1", "Bước 2", "Bước 3 (2–5 bước, đủ để học viên tự làm theo)"],
      "example": {"context": "Bối cảnh cụ thể (ai, tình huống nào)", "approach": "Cách làm áp dụng khái niệm của bài vào bối cảnh đó", "expected_result": "Kết quả kỳ vọng, đo được"},
      "mistakes": ["lỗi hay gặp 1 (tùy chọn — gộp vào cuối Nội dung chính ở docx)", "lỗi hay gặp 2"],
      "ai_application": ["cách dùng AI 1 (tùy chọn — không bắt buộc nếu cả môn đã là AI)", "cách dùng AI 2"],
      "main_content": "Đoạn văn bổ sung TÙY CHỌN cho syllabus docx (không tính vào ngân sách content) — chỉ dùng khi why_important/how_to/example chưa đủ diễn giải; đa số bài không cần field này.",
      "lien_he": "liên hệ thực tế / chú thích (KHÔNG hiện ở syllabus docx, KHÔNG vào lessons.content xlsx — dữ liệu giữ cho Lesson Plan bước sau)",
      "gate": "điều kiện đạt để qua level",
      "capstone_artifact": "sản phẩm bài nộp",
      "rubric": {"dat": "tiêu chí tối thiểu", "kha": "đạt + làm đủ hơn", "tot": "khá + chiều sâu/sáng tạo/ngữ cảnh thật"},
      "skill_tags": ["tag_a", "tag_b", "tag_c"],
      "fast_track": "50–100 từ: Bỏ nhập đề. Điểm chốt ... Làm ngay ... Gate giữ nguyên.",
      "resources": [
        {"title": "Tên tài liệu", "type": "video_youtube | pdf | website | ...", "topic": "chủ đề cụ thể của link (có thể khác topic của cả bài)", "description": "≤15 từ: loại + nội dung + khi nào dùng", "url": "https://..."}
      ]
    }
  ],
  "sessions": [
    {"idx": 1, "summary": "Nội dung buổi", "duration_minutes": 120, "default_mode": "hybrid", "format_type": "LT/TH"}
  ],
  "assignments": [
    {"idx": 1, "code": "B1", "title": "Tên bài tập", "brief": "Mô tả", "is_final": false},
    {"idx": 2, "code": "B2", "title": "Capstone", "brief": "Bài cuối khóa", "is_final": true}
  ],
  "radar": [
    {"key": "algorithm_hook", "label": "Thuật toán & Hook", "tags": ["retention_analysis", "hook_writing"]}
  ],
  "kash": {
    "knowledge": [
      {"item": "Khái niệm/nguyên lý nền cần biết, đúc kết từ objectives+concepts toàn khóa", "bloom": "Nhớ | Hiểu"}
    ],
    "skill": [
      {"item": "Kỹ năng làm được, đúc kết từ objectives+gate+capstone_artifact toàn khóa", "bloom": "Áp dụng | Phân tích | Đánh giá | Sáng tạo"}
    ],
    "attitude": ["Thái độ/tư duy cần có sau khóa (không gắn Bloom — thuộc miền cảm xúc/thái độ, không phải nhận thức)"],
    "habit": ["Thói quen làm việc cần hình thành sau khóa (không gắn Bloom)"]
  }
}
```

## Map course.json → sheet import (.xlsx)

| course.json | Sheet | Cột |
|---|---|---|
| code, title, intro_video_url, color, description, ai_context, prerequisites, curriculum_overview | **Info** | Trường / Giá trị (key-value) — `curriculum_overview` ghi vào dòng `curriculum_md` (script tự nối thêm "Lộ trình" từ lessons[], map DB `courses.curriculum_md`) |
| lessons[] (why_important/topic/concepts/objectives/how_to/example/gate/...) | **Lessons** | sort_order, title, description, content (script TỰ COMPOSE 300–600 từ theo schema `COURSE_CONTENT_GUIDELINE.md` §3 từ field cấu trúc — xem §Marker cấm bên dưới) |
| lessons[].resources[] | **Resources** | lesson_sort_order (= sort_order bài), title, type, topic, description, url |
| sessions[] | **Sessions** | idx, summary, duration_minutes, default_mode, format_type |
| assignments[] | **Assignments** | idx, code, title, brief |
| radar[] | **Radar** | key, label, tags (script nối bằng dấu phẩy) |
| kash | *(không có sheet riêng — chỉ dùng cho docx)* | — |

## Ràng buộc từng trường

- **schema_version / version / approved / approved_date / changelog (contract bàn giao):** `schema_version: 2` cố định cho schema hiện tại — đổi cấu trúc schema thì tăng số và cập nhật đồng thời file này + `lesson-json-schema.md` của kstudy-lesson-plan-creator. `approved: false` ở mọi bản nháp; chỉ đặt `true` + điền `approved_date` khi user tuyên bố duyệt bản cuối (lesson-plan-creator từ chối chạy nếu `approved != true`). `version: 0` khi nháp, `1` khi duyệt lần đầu; mỗi lần sửa sau duyệt tăng version + thêm 1 dòng `changelog` `{version, date, summary}` ghi rõ bài/buổi bị ảnh hưởng. Các field này KHÔNG import vào xlsx (chỉ phục vụ pipeline).
- **code, title, author, color:** KHÔNG tự đặt/suy đoán — đây là thông tin định danh, phải hỏi user và chờ xác nhận trước khi ghi vào course.json (xem SKILL.md §Không tự ý bịa thông tin định danh). `code` đúng 6 ký tự A–Z/0–9 ALL CAPS; mã input ≠ 6 → chuẩn hóa rồi báo user, dùng nhất quán cả 3 file. `color` hex `#RRGGBB` — màu thẻ khóa trong import xlsx (heading html/docx dùng màu brand cố định, không theo color).
- **logo:** đường dẫn ảnh logo Kstudy (png/jpg) — **tùy chọn**, có thể bỏ trống. Script tự dùng logo mặc định đã đóng gói sẵn trong skill (`assets/logo/kstudy-logo-full.png`) qua `resolve_logo()`; chỉ set field này khi dự án có logo riêng khác bản mặc định. Nhúng header docx (trái) + banner html. Không tìm thấy file nào (kể cả mặc định) → docx dùng wordmark chữ "KSTUDY".
- **author:** tên người chủ trì biên soạn (đã được user xác nhận) → khối ký tên cuối syllabus docx ("Chủ trì biên soạn" + tên). Thiếu → placeholder `[Tên tác giả]`, không tự bịa tên.
- **prerequisites:** LUÔN hỏi user trước khi soạn course.json — không tự suy đoán kể cả khi có vẻ môn "không cần điều kiện gì" (vẫn cần user xác nhận rõ điều đó). Có 2 dạng, có thể kết hợp: (a) điều kiện kỹ năng/thiết bị/trình độ chung (vd thiết bị, kỹ năng công nghệ, trình độ học vấn) — chỉ cần `description`, `required_courses: []`; (b) điều kiện đã hoàn thành 1 hoặc nhiều môn khác trong hệ thống Kstudy — `description` viết văn xuôi ("Đã hoàn thành môn Enter AI.") VÀ `required_courses` liệt kê đúng `code` (6 ký tự) của (các) môn đó để hệ thống đối chiếu được. Nếu môn tiên quyết chưa có `code` chính thức (chưa build) → hỏi user mã dự kiến hoặc để `required_courses: []` tạm thời và ghi chú trong `description`.
- **design_depth:** kế thừa từ Curriculum Design/Course Planner (`LITE`/`STANDARD`/`FULL`); chỉ dùng để điều chỉnh độ sâu research, review và readiness, không tạo thêm output file. Course cũ thiếu field được hiểu là `STANDARD` trong migration.
- **alignment_status:** `PROPOSED` khi đang soạn; chỉ chuyển `APPROVED` sau khi Constructive Alignment QA đạt.
- **traceability (cấp course):** kế thừa `job_task_ids`, `competency_ids`, `plo_ids` từ Course Planner; khóa `clo_ids`, `lesson_outcome_ids`, `evidence_ids`, `rubric_ids`, `resource_ids` theo contract chung `~/.claude/skills/kstudy-curriculum-design/references/traceability-contract.md`. Không để object này rỗng khi handoff sang Lesson Plan.
- **assessment_blueprint:** mỗi evidence quan trọng phải có method, CLO/LO liên quan, rubric direction và approval status.
- **curriculum_overview:** tổng quan hành trình học viên (50–120 từ) — KHÔNG lặp lại mô tả từng bài (script tự nối phần "Lộ trình" liệt kê `Bài X.Y: <title> — <topic>` từ `lessons[]`, theo đúng thứ tự `sort_order`). Ghép 2 phần thành giá trị dòng `curriculum_md` trong Info sheet, map DB `courses.curriculum_md` — **KHÔNG được để trống** (QA FAIL nếu trống, xem checklist publish).
- **lessons[].session_idx:** buổi (theo `sessions[].idx`) mà bài thuộc về. Script tự tính số hiển thị **"Bài X.Y"** cho docx/html (X = session_idx, Y = thứ tự bài trong buổi đó theo sort_order tăng dần) — KHÔNG gõ tay số này vào `title`. `sort_order` vẫn là số tuyến tính 1..N dùng cho Level/hệ thống, độc lập với "Bài X.Y" hiển thị.
- **lessons[].resources[].type / topic:** `type` là loại tài nguyên (`video_youtube`, `pdf`, `website`, …) dùng để phân loại/lọc; `topic` là chủ đề cụ thể của riêng link đó (có thể hẹp hơn topic của cả bài). Cả hai là field mô tả, không đổi cấu trúc `title`/`description`/`url` đã có.
- **sessions[].format_type:** `"LT"` | `"TH"` | `"LT/TH"` — Lý thuyết/Thực hành, hiển thị ở cột "Hình thức" bảng lịch trình syllabus docx/html. **Khác** `default_mode` (`online`/`offline`/`hybrid`, dùng cho hệ thống/import) — hai field độc lập, không suy ra field này từ field kia.

**Branding cố định trong generator (không cần config mỗi khóa):** header syllabus = logo trái + "Mã - Tên" phải; footer = "Kstudy Academy .,jsc  -  www.kstudy.edu.vn"; heading màu `#1D237D` (navy) + `#247DF9` (blue); font "Google Sans Flex" (fallback "Be Vietnam Pro" cho html — cần cài Google Sans Flex trên máy để docx render đúng).
- **ai_context / fast_track:** bám ngân sách từ (xem SKILL.md).
- **Bài học = field cấu trúc, KHÔNG tự viết `content`.** Script compose `content` (cho import xlsx + html, map DB `lessons.content`) từ `why_important`/`objectives`/`topic`/`concepts`/`how_to`/`example`/`mistakes`/`gate`/`capstone_artifact`/`rubric`/`skill_tags` theo đúng 6 mục schema `COURSE_CONTENT_GUIDELINE.md` §3 → 300–600 từ có cấu trúc (không phải văn xuôi rời rạc). `lien_he`/`ai_application` KHÔNG vào `content` (giữ cho Lesson Plan bước sau). (Lesson có sẵn `content` → script dùng luôn, backward-compat.)
- **skill_tags (lesson):** mọi tag PHẢI có trong `radar[].tags`. Script QA FAIL nếu lệch. Xem `skill-tags-radar.md`.
- **Chuẩn sư phạm (xem `pedagogy.md`):** `objectives` dùng động từ Bloom đo được; mỗi mục tiêu phải được gate/capstone kiểm tra (alignment); độ khó tăng dần qua level (scaffolding).
- **lesson traceability:** mỗi lesson phải có `clo_ids`, `lesson_outcome_ids`, `evidence_ids`, `rubric_ids`, `resource_ids` và `traceability.approval_status`; `activity_ids` có thể rỗng vì activity chi tiết thuộc kstudy-lesson-plan-creator. Các field này KHÔNG import vào xlsx.
- **rubric `{dat, kha, tot}`:** mỗi bài, để Mentor chấm nhất quán + học viên biết kỳ vọng. Generator nối gọn (Đạt/Khá/Tốt) vào mục "Bài thực hành gợi ý" của `content` bằng câu văn thường — **KHÔNG render mục rubric riêng vào docx syllabus** (xem §Cấu trúc bài trong syllabus docx bên dưới). Thiếu rubric → QA WARN.
- **Marker runtime cấm trong MỌI field nội dung (`ai_context`, `curriculum_overview`, `description`, `content`/các field nguồn của nó, resource `description`):** `[BÀI TẬP]` `[ĐIỂM: XX/100]` `[QUIZ_INLINE]` `[QUIZ_RESULT]` `[LEVEL_UP]` `[COMPLETE_LEVEL: N]` `[CHOICES]` — đây là control signal L8/frontend tự sinh đúng thời điểm (chấm điểm, mở level, hỏi quiz), KHÔNG phải nội dung học thuật. Nhúng sẵn marker này vào content DB khiến Mentor có thể lặp lại sai lúc, hoặc tự ý báo hoàn thành/chấm điểm (grading luôn phải deterministic phía backend). Script QA quét và FAIL nếu phát hiện — xem `COURSE_CONTENT_GUIDELINE.md` §1.
- **radar:** đúng **6** trục. `tags` là mảng (script tự nối phẩy khi ghi xlsx). **Chỉ dùng cho sheet Radar (xlsx import), không còn render trong docx** — Portfolio là dữ liệu nội bộ hệ thống Kstudy AI Mentor, không phải nội dung syllabus giao học viên/giảng viên.
- **kash:** course-level, 4 nhóm theo mô hình KASH (Knowledge–Attitude–Skill–Habit), render ở mục "5. Khung năng lực (KASH)" trong docx (thay cho Radar Portfolio cũ). `knowledge`/`skill` là mảng object `{item, bloom}` — `bloom` lấy đúng 1 trong 6 cấp thang Bloom ở `pedagogy.md` §2 (có thể ghi 2 cấp liền nhau nếu mục đó bắc cầu, vd "Áp dụng/Phân tích"). `attitude`/`habit` là mảng string thuần, không gắn Bloom (Bloom là thang nhận thức — không áp cho thái độ/thói quen). Đúc kết từ `objectives`+`concepts`+`gate`+`capstone_artifact` của TOÀN KHÓA (không phải copy nguyên văn từng bài) — đề xuất từ nội dung rồi cho user xác nhận, giống cách làm radar. Thiếu → QA WARN, mục 5 docx không render (không FAIL build).
- **sessions.default_mode:** `hybrid` | `online` | `offline`. `duration_minutes`: số nguyên (vd 90, 120).
- **assignments.is_final:** đúng **1** bài = `true` (capstone). Hệ tự đặt 50% cho bài cuối, còn lại chia đều — KHÔNG cần cột trọng số trong xlsx.
- **fast_track:** không có cột trong template import → script chỉ đưa vào html (nút Copy) + docx. Muốn auto-import: thêm cột `fast_track` vào sheet Lessons rồi báo để cập nhật script.

## Cấu trúc bài trong syllabus docx (script tự render từ field — rút gọn 6 mục)

Mỗi bài render đúng 6 phần theo thứ tự sau (bỏ qua phần nào field trống), nhãn là **Heading 3 thật** (không phải đoạn bold giả heading):

1. **`Bài X.Y: <title>`** — Heading 2; X.Y tính từ `session_idx` + thứ tự trong buổi, không lấy từ `title`.
2. **Mô tả** ← `description`, đoạn văn, KHÔNG có nhãn đứng trước.
3. **Mục tiêu:** ← `objectives` (list nếu có đánh số 1)/2)..., đoạn văn nếu không).
4. **Nội dung chính:** ← `why_important` (câu mở, in nghiêng) + `topic` (● in đậm) + `concepts` (– cấp 2) + `how_to` (đánh số) + `example` (Bối cảnh/Cách làm/Kết quả kỳ vọng) + `main_content` nếu có (đoạn văn bổ sung tùy chọn, không tính ngân sách content) + `mistakes` nếu có (gộp 1 câu cuối, không tách nhãn riêng). Cùng nguồn field với `content` sinh cho xlsx, chỉ khác cách trình bày (docx dùng bullet/số thứ tự thay vì heading `##`).
5. **Tài nguyên & công cụ:** ← `resources` (tên công cụ in đậm + mô tả in nghiêng xám + url).
6. **Bài tập:** ← `gate` + `capstone_artifact` + tên bài tương ứng. **KHÔNG in `rubric`** (đạt/khá/tốt) ở syllabus — rubric vẫn có trong course.json/xlsx cho AI Mentor chấm nội bộ.

`ai_application` và `lien_he` KHÔNG hiện ở syllabus docx (mức chi tiết đó thuộc Lesson Plan, bước sau trong pipeline) — vẫn giữ trong course.json để dùng khi soạn Lesson Plan. `main_content` chỉ vào docx, không tính vào ngân sách `content`.

Ngoài cấu trúc theo bài (mục 3), docx còn 2 mục course-level cố định ở cuối: **"4. Bài tập & đánh giá"** (từ `assignments[]`) và **"5. Khung năng lực (KASH)"** (từ `kash`, 4 khối Kiến thức/Kỹ năng/Thái độ/Thói quen — xem §Ràng buộc từng trường bên trên). Mục 5 **thay thế** "Radar Portfolio" của các bản trước — radar 6 trục vẫn bắt buộc dựng đúng nhưng chỉ để phục vụ sheet Radar trong xlsx import, không còn là nội dung đọc được trong syllabus.

## 3 file output

| File | Cho ai | Nội dung |
|---|---|---|
| `<code> - kstudy import - <title>.xlsx` | Hệ thống | 6 sheet khớp template, import 1 phát |
| `<code> - Kstudy template - <title>.html` | Giảng viên | Mọi trường + nút Copy; bảng buổi/bài tập/radar |
| `<code> - Kstudy Syllabus - <title>.docx` | Hồ sơ/giảng viên | Syllabus chính thức, cấu trúc 6 mục rút gọn; header logo + mã-tên, footer Kstudy, phân cấp Heading 1/2/3 |

PDF **không xuất mặc định**. Chỉ tạo khi user yêu cầu rõ, sau khi bản docx đã được duyệt: `soffice --headless --convert-to pdf "<file>.docx"` (hoặc `build_kstudy_outputs.py ... --pdf`).

## Handoff output sau duyệt

Sau khi `approved=true`, chạy `python scripts/build_handoff_outputs.py course.json .` để tạo:

| File | Cho ai | Nội dung |
|---|---|---|
| `handoff_summary.md` | Agent/người soạn Lesson Plan | Tóm tắt quyết định đã duyệt: identity, prerequisites, KASH, radar, map buổi, changelog, open items |
| `ThamKhao/resources.index.json` | Agent/người soạn Lesson Plan | Registry tài nguyên/link đã biết, trạng thái xác minh, map bài/buổi |

Hai file này là handoff metadata, KHÔNG phải nguồn sự thật mới và KHÔNG thay thế `course.json`.

## Kiểm nhanh trước khi giao

- Chạy build script → đọc khối QA, 0 FAIL.
- `curriculum_md` (Info sheet) không rỗng; mỗi bài `content` 300–600 từ; không FAIL marker runtime cấm.
- Sau khi duyệt, chạy handoff script → kiểm có `handoff_summary.md` và `ThamKhao/resources.index.json`.
- Mở .html xem trình bày + thử 1 nút Copy.
- Mở .xlsx đối chiếu template (6 sheet, header khớp).
- Số bài = số dòng Lessons; mỗi resource có `lesson_sort_order` đúng bài.
- (Tùy chọn) QA lại file xlsx đã sửa tay: `python scripts/validate_course.py "<import.xlsx>"`.
