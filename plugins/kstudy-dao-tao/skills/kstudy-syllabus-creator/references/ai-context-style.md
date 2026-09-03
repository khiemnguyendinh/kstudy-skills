# Cách viết ai_context (course, L2) và content (lesson, DB thật)

Hai field khác mục đích, khác ngân sách — đừng áp cùng 1 kiểu viết cho cả hai.

## `courses.ai_context` (course-level, L2 scope-card) — LEAN, 150–250 từ

Layer này bị cắt sớm khi context window đầy — viết dạng scope-card, keyword-dense, không văn xuôi kể lể.

### Kỹ thuật cắt từ (áp cho `ai_context`)

- Bỏ mở đầu: "Trong khóa này", "Học viên sẽ được học", "Mục đích của khóa là".
- Bỏ nối: "bên cạnh đó", "ngoài ra", "đầu tiên thì".
- Bỏ tính từ marketing: "cực kỳ quan trọng", "nền tảng vững chắc".
- Giữ: danh từ khái niệm, động từ outcome, tên artifact, thuật ngữ lõi.
- Dùng nhãn rõ (Đối tượng / Outcome / Phạm vi / Mạch level / Thuật ngữ lõi) thay vì câu trôi.

**XẤU (văn xuôi, ~40 từ chỉ tải ~2 ý):**
> Trong khóa học này, chúng ta sẽ cùng nhau khám phá thế giới thú vị của marketing. Học viên sẽ hiểu được các khái niệm quan trọng.

**TỐT (nhãn, tải nhiều ý hơn trong cùng độ dài):**
> Đối tượng: marketer mới, chưa có nền tảng positioning. Outcome: viết được 1 bản định vị thương hiệu hoàn chỉnh. Phạm vi: 2 bài — positioning, RTB; không bao gồm truyền thông đa kênh. Mạch level: bài 1 khái niệm, bài 2 ứng dụng case thật. Thuật ngữ lõi: POD, POP, RTB, frame of reference.

## `lessons.content` (bài học, DB thật `lessons.content`) — ĐỦ, 300–600 từ, có cấu trúc

Đây là field chatbot AI Mentor dùng để DẠY nội dung bài — quá ngắn/toàn keyword rời rạc thì Mentor dạy chung chung, không đủ ví dụ/quy trình cụ thể. Theo đúng schema `COURSE_CONTENT_GUIDELINE.md` §3 — **KHÔNG viết văn xuôi tự do, cũng KHÔNG nén thành list từ khóa trần trụi**: giữa 2 thái cực đó là **có cấu trúc rõ theo 6 mục**, mỗi mục vài câu ngắn, đủ ý để dạy được, không lặp/không sáo rỗng.

6 mục bắt buộc theo thứ tự (script tự ghép từ field course.json, xem `course-schema.md`):

```md
## Vì sao học phần này quan trọng
<1-2 câu, hệ quả cụ thể nếu bỏ qua>

## Khái niệm cốt lõi
- khái niệm 1
- khái niệm 2

## Cách làm thực tế
1. bước 1
2. bước 2

## Ví dụ áp dụng
Bối cảnh: ...
Cách làm: ...
Kết quả kỳ vọng: ...

## Lỗi thường gặp
- lỗi 1

## Bài thực hành gợi ý
Học viên cần tạo: ...
Tiêu chí đạt: ...
```

**XẤU (quá ngắn, chỉ liệt kê từ khóa, ~15 từ — Mentor không đủ để dạy):**
> Chủ đề: brand positioning. Khái niệm: POD, POP, RTB. Gate: nộp statement.

**XẤU (văn xuôi kể lể, không cấu trúc, sáo rỗng):**
> Trong bài học này, chúng ta sẽ cùng nhau khám phá thế giới thú vị của định vị thương hiệu, một khái niệm cực kỳ quan trọng mà bất kỳ marketer nào cũng cần nắm vững...

**TỐT (có cấu trúc, đủ ý, ~120 từ cho 1 đoạn trích — bài thật cần đủ 300–600 từ toàn bài):**
> ## Khái niệm cốt lõi
> - Target: nhóm khách hàng mục tiêu cụ thể
> - Frame of reference: nhóm sản phẩm cạnh tranh trực tiếp
> - POD (Point of Difference): điểm khác biệt học viên claim
> - RTB (Reason to Believe): bằng chứng cho POD
>
> ## Ví dụ áp dụng
> Bối cảnh: thương hiệu cà phê nội địa mới ra mắt.
> Cách làm: xác định target (dân văn phòng 25–35 tuổi), frame of reference (cà phê rang xay công sở), 2 POD (nguồn gốc Việt + giá hợp lý) kèm RTB cho từng POD.
> Kết quả kỳ vọng: 1 đoạn positioning statement đủ 4 thành phần, có RTB cụ thể không chung chung.

## Marker runtime — CẤM nhúng vào bất kỳ field content nào

`[BÀI TẬP]` `[ĐIỂM: XX/100]` `[QUIZ_INLINE]` `[QUIZ_RESULT]` `[LEVEL_UP]` `[COMPLETE_LEVEL: N]` `[CHOICES]` là control signal hệ thống (L8/frontend) tự sinh đúng lúc để chấm điểm/mở level/hỏi quiz — KHÔNG được viết sẵn các chuỗi này (kể cả biến thể không dấu) vào `ai_context`, `curriculum_overview`, `description`, `content`/các field nguồn của nó, hay mô tả resource. Lý do: nếu marker nằm sẵn trong dữ liệu bài học, Mentor có thể copy lại đúng nguyên văn sai thời điểm, hoặc tự nhận hoàn thành/tự chấm điểm — trong khi chấm điểm phải luôn deterministic phía backend. Script `build_kstudy_outputs.py`/`validate_course.py` quét và FAIL nếu phát hiện.

## Mô tả tài nguyên (AI-only)

Mục tiêu: để Mentor biết **bên trong link có gì** → match đúng nhu cầu học viên (rule: chỉ trích URL có trong context, không bịa). Công thức: `<loại> + <nội dung cụ thể> + <khi nào dùng>`, ≤15 từ.

- TỐT: `Slide 12 trang: 4P + ví dụ Vinamilk; dùng khi học viên hỏi marketing mix`
- TỐT: `Template Google Sheet: bảng tính share of voice; dùng cho bài tập đo lường`
- XẤU: `Slide bài 1` / `Tài liệu hay về marketing` (không cho AI biết nội dung)

Phân loại để Mentor chọn đúng theo nhu cầu: hỏi khái niệm → video/slide; cần làm bài có mẫu → pdf/template; hỏi tình huống → case.

## fast_track_md

Dành cho học viên trình độ cao (placement/self-declared). Chỉ bỏ **nhập đề + warm-up**; GIỮ gate quiz + capstone artifact (nếu không sẽ phá chuẩn đầu ra). Công thức 50–100 từ: `Bỏ nhập đề. Điểm chốt: <2–3 ý cô đọng>. Làm ngay: <bài tập/artifact>. Gate giữ nguyên.`

## Việt-trước khi trình bày

Khái niệm/nội dung viết **tiếng Việt trước**; chỉ giữ thuật ngữ tiếng Anh KHÓ dịch, đặt trong ngoặc sau cụm Việt. Tránh dồn một chuỗi keyword tiếng Anh khó hiểu cho người đọc syllabus.

- TỐT: "Tỷ lệ xem hết (watch-through rate)", "Câu mở (hook)", "Đường cong giữ chân (retention curve)".
- XẤU: "watch-through rate", "swipe-away", "hook", "loop", "retention curve" (toàn tiếng Anh).

Áp cho `concepts`, `how_to`, `example`, `mistakes`, `why_important`, `objectives`. Thuật ngữ đã quá phổ biến (SEO, AI, CTR) để nguyên, không dịch gượng. (Generator tự viết hoa đầu câu/đầu mục khi render docx — không cần lo hoa/thường khi soạn.)

## Checklist tự kiểm mỗi field

- [ ] `ai_context` (course) trong 150–250 từ; `content` (mỗi bài) trong 300–600 từ, đủ 6 mục; resource desc ≤15 từ; `fast_track` 50–100 từ; `curriculum_overview` 50–120 từ, không rỗng.
- [ ] `content` có cấu trúc rõ 6 mục (không văn xuôi tự do, không list từ khóa trần trụi).
- [ ] Không có câu mở đầu thừa / tính từ marketing trong field cho-AI.
- [ ] Mọi skill_tag trong bài đều có trong 6 trục radar.
- [ ] Objectives mở đầu bằng động từ đo được + gắn artifact.
- [ ] Không leak persona/tone (thuộc L1/L8).
- [ ] Không có marker runtime cấm (`[BÀI TẬP]`/`[ĐIỂM:]`/`[QUIZ_INLINE]`/`[QUIZ_RESULT]`/`[LEVEL_UP]`/`[COMPLETE_LEVEL]`/`[CHOICES]`) trong bất kỳ field nào.
