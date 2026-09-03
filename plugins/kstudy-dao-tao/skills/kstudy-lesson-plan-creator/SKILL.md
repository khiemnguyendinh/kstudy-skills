---
name: kstudy-lesson-plan-creator
description: >-
  Tạo bộ học liệu giảng dạy cho một buổi Kstudy từ syllabus ĐÃ DUYỆT (`course.json`
  approved=true, từ kstudy-syllabus-creator) + tài liệu tham khảo. Xuất Lesson Plan .docx
  (KASH + Bloom, gate, timeline, demo, bài tập), Slide-outline .md (ôn tập buổi trước/tiên
  quyết, mục tiêu, tổng kết, nội dung buổi sau, gợi ý minh họa/KSD), Video-outline .md
  micro-learning Cốt lõi + Mở rộng, TaiNguyen-ThamKhao .docx. Đọc handoff/resources,
  sinh lesson_seed.json theo buổi, dùng conventions.md, QA validate_lesson.py, reviewer,
  cascade khi syllabus đổi. Dùng khi user nói: soạn lesson plan/kế hoạch bài dạy/giáo án,
  tạo slide bài giảng, demo lớp, video elearning/micro learning, bài tập thực hành, tài
  nguyên tự học, cập nhật học liệu theo syllabus. Không dùng để tạo/import khóa học mới.
---

# Tạo Lesson Plan & học liệu buổi học cho Kstudy

Đây là bước tiếp theo sau khi **syllabus đã duyệt**. Từ `course.json` + handoff + tài liệu tham khảo, biến từng buổi trực tiếp thành **seed + bộ 4 file**:

1. **`lesson_seed.json`** — snapshot đầu vào của buổi, sinh tự động từ `course.json` + `resources.index.json`.
2. **`<CODE>-B<N>-LessonPlan.docx`** — kế hoạch bài dạy chính thức (giảng viên cầm lên lớp).
3. **`<CODE>-B<N>-Slide-outline.md`** — đề cương slide bài giảng, mỗi slide kèm gợi ý minh họa.
4. **`<CODE>-B<N>-Video-outline.md`** — đề cương video e-learning micro-learning (Cốt lõi + Mở rộng).
5. **`<CODE>-B<N>-TaiNguyen-ThamKhao.docx`** — danh mục tài nguyên & tham khảo.

Hai file .docx sinh bằng `scripts/build_lesson_outputs.py` từ một file `lesson.json`; hai file .md do model soạn tay theo template. Không tự gõ tay docx — luôn qua script để nhất quán với syllabus.

## Gate đầu vào — kiểm tra TRƯỚC khi làm bất cứ việc gì (bắt buộc)

1. **`course.json` phải tồn tại ở gốc thư mục môn** và có `approved: true`. Nếu `approved` là `false`/thiếu → DỪNG, báo user: syllabus chưa được đóng dấu duyệt; nếu syllabus thực tế đã duyệt thì quay lại `kstudy-syllabus-creator` cập nhật `approved: true` + `approved_date` (1 phút), nếu chưa duyệt thì duyệt syllabus trước — KHÔNG sản xuất học liệu từ syllabus nháp. Ngoại lệ duy nhất: `course.json` được tạo bởi bản skill cũ chưa có field `approved` VÀ user xác nhận rõ bằng lời là syllabus đã duyệt → tiến hành, đồng thời bổ sung `approved: true` + `approved_date` vào course.json.
2. **`schema_version` = 2.** Thiếu/khác → đọc kỹ dữ liệu thực tế, map thủ công, báo user course.json thuộc schema cũ.
3. **Nguồn sự thật duy nhất:** KASH, objectives, gate, concepts, resources của buổi phải LẤY TỪ course.json rồi chi tiết hóa — KHÔNG soạn lại từ đầu, KHÔNG thêm nội dung ngoài syllabus mà không flag cho user. Phát hiện syllabus thiếu/sai khi soạn học liệu → báo user sửa course.json (qua kstudy-syllabus-creator) rồi mới tiếp, đừng "vá" âm thầm ở lesson plan.
4. **Handoff:** nếu có `handoff_summary.md` và `ThamKhao/resources.index.json`, đọc trước khi hỏi user để tránh hỏi lại thông tin đã chốt; nếu thiếu, vẫn chạy từ `course.json` nhưng báo user handoff chưa đủ.

## Cấu trúc thư mục môn (chuẩn chung pipeline)

```
<Thư mục môn>/
├── course.json          ← contract từ kstudy-syllabus-creator (chỉ đọc; sửa qua skill đó)
├── handoff_summary.md   ← tóm tắt đã duyệt từ kstudy-syllabus-creator (đọc nếu có)
├── conventions.md       ← quyết định style học liệu (skill này tạo sau pilot — xem §Conventions)
├── 01_Syllabus/         ← output bước syllabus (không đụng)
├── 02_LessonPlan/
│   └── Buoi_<N>/        ← lesson_seed.json + bộ 4 file <CODE>-B<N>-* của buổi N
└── ThamKhao/            ← ebook, PDF, tài liệu nguồn, resources.index.json
```

## Nguyên tắc thiết kế (đọc trước)

Lớp trực tiếp và video e-learning có vai trò khác nhau, tránh trùng lặp:
- **Trên lớp** = "làm được cùng mentor": demo trực tiếp + thực hành có người kèm + xử lý lỗi. Không dùng giờ lớp đọc-chép lý thuyết.
- **Video e-learning** = "hiểu sâu + tự làm lại": theo mô hình **Cốt lõi + Mở rộng**. Cốt lõi tái hiện nội dung lớp (xem trước/xem lại); Mở rộng đào sâu ngoài giờ. Video Cốt lõi và Lesson Plan dùng chung một nguồn (concepts + demo steps) để không lệch.
- **Slide outline** = input cho `kstudy-slide-design` (KSD), không phải bản thiết kế slide hoàn chỉnh. Skill này tạo thông điệp học tập, nội dung ngắn, visual job và brief minh họa; KSD quyết định layout, typography, ảnh thật/screenshot/biểu đồ/sơ đồ, safe area và xuất deck.

Chiến lược triển khai: **pilot buổi đầu trước** — làm trọn bộ 4 file buổi 1, để user duyệt và chốt template, rồi nhân rộng các buổi còn lại đồng nhất qua `conventions.md`.

## Conventions — chống lệch chuẩn giữa các buổi (bắt buộc)

Buổi 2..N thường được soạn ở phiên chat khác — model không nhớ gì về pilot. Cơ chế:

- **Sau khi user duyệt bộ 4 file pilot (Buổi 1):** ghi mọi quyết định style đã chốt vào `conventions.md` ở gốc thư mục môn, theo template `references/conventions-template.md` (giọng văn & wording, số slide/buổi & kiểu mở đầu-kết, số video/bài & độ dài & định dạng ưa dùng, phong cách demo, format bài tập, các góp ý của user đã tiếp thu). Trình user xác nhận nội dung conventions trước khi lưu.
- **Đầu MỌI lần soạn buổi bất kỳ (kể cả cùng phiên):** đọc `conventions.md` trước khi soạn; tuân thủ tuyệt đối. Muốn làm khác một quyết định đã ghi → hỏi user, được đồng ý thì cập nhật `conventions.md` (kèm dòng changelog cuối file) rồi mới áp dụng — để các buổi sau theo chuẩn mới, không tạo 2 chuẩn song song.
- `conventions.md` chưa tồn tại mà user yêu cầu soạn buổi ≠ 1 → hỏi: đã có buổi pilot được duyệt chưa? Có → đề nghị bổ sung conventions từ bộ file đó trước; chưa → đề xuất làm pilot đúng quy trình.

## Cascade — khi syllabus thay đổi sau khi đã có học liệu

- Khi soạn xong `lesson.json`, ghi vào đó `course_fingerprint` = 12 ký tự đầu SHA-256 của file course.json (script validate tự tính và báo nếu thiếu — xem lệnh in fingerprint ở `validate_lesson.py --fingerprint`).
- `validate_lesson.py` phát hiện fingerprint lệch (course.json đã đổi sau khi buổi được soạn) → đọc `changelog[]` trong course.json, xác định buổi nào bị ảnh hưởng, liệt kê cho user: buổi X cần rà mục nào. Chỉ rebuild các buổi bị ảnh hưởng, các buổi khác cập nhật fingerprint mới sau khi đã xác nhận không liên quan.
- KHÔNG bao giờ sửa course.json từ skill này để "khớp" với học liệu — chiều đúng là syllabus → học liệu.

## Quy trình 7 bước

**1. Gate + Ingest.** Chạy §Gate đầu vào. Đọc `conventions.md` (nếu có), `handoff_summary.md` (nếu có), `course.json` của môn (lessons, sessions, assignments, radar, skill_tags, changelog) và `ThamKhao/resources.index.json` (nếu có). Trước khi soạn lesson plan/slide outline, xác định bối cảnh chuyển tiếp:
- Nếu buổi N > 1: kiểm nội dung chính của buổi liền trước từ `02_LessonPlan/Buoi_<N-1>/lesson.json`; nếu thiếu, đọc LessonPlan/Slide-outline buổi trước; nếu vẫn thiếu, suy từ `course.json.sessions` + `course.json.lessons` của buổi N-1 và ghi rõ đây là suy từ syllabus. Tóm tắt 3-5 ý chính để dùng cho slide "Ôn tập buổi trước".
- Nếu buổi 1: kiểm syllabus/course.json có môn điều kiện tiên quyết không. Nếu có, lấy các ý chính đã được quy định trong syllabus để dùng cho slide "Ôn tập nhanh môn điều kiện tiên quyết"; không tự bịa nội dung ôn tập ngoài syllabus. Nếu không có môn điều kiện, bỏ phần ôn tập tiên quyết.

Sinh `lesson_seed.json` cho buổi bằng:
```
python scripts/build_lesson_seed.py course.json <N>
```
Seed nằm tại `02_LessonPlan/Buoi_<N>/lesson_seed.json`; dùng seed này làm checklist đầu vào khi soạn, không dùng trí nhớ phiên chat. Xác định buổi này phủ những bài (lesson) nào qua `session_idx`. Đọc `main_content`, `concepts`, `objectives`, `gate`, `mistakes`, `lien_he`, `ai_application`, `resources` của các bài liên quan.

**2. Nghiên cứu bổ sung.** Cột "tham khảo" trong khung chương trình + PDF/ebook trong `ThamKhao/` (có thể nạp NotebookLM) + web search để cập nhật tool/tính năng mới nhất (tên tính năng, giao diện). Link không mở được → giữ URL, không bịa. Xác minh URL chính thức trước khi đưa vào file tài nguyên.

**3. Thiết kế phân bổ.** Chốt: thời lượng buổi (lấy `duration_minutes` của session trong course.json; mặc định 90 phút nếu thiếu), tiến trình theo phút (mở đầu → lý thuyết trọng tâm → demo → thực hành có hướng dẫn → tổng kết), learning zone của từng hoạt động (`classroom`, `e_learning`, `ai_mentor`, `internet`), số video mỗi bài (3–6, phân Cốt lõi/Mở rộng), formative check (đặt TRƯỚC gate để phát hiện lỗi sớm), gate của buổi (gộp từ gate các bài — không tự chế). Với mỗi activity xác định lesson outcome, hướng evidence/rubric, mức Miller (`KNOWS`/`KNOWS_HOW`/`SHOWS_HOW`/`DOES`) và phương án UDL nếu thực sự cần. Nếu thiếu dữ liệu (đối tượng, tác giả đứng lớp, sản phẩm capstone) → hỏi user gọn từng mục, không bịa.

**4. Soạn `lesson.json`** cho buổi theo `references/lesson-json-schema.md` và contract chung `~/.claude/skills/kstudy-curriculum-design/references/traceability-contract.md`, từ `lesson_seed.json` (kèm `course_fingerprint`). Chuẩn sư phạm: chuẩn đầu ra KASH dùng **động từ Bloom đo được** (rút từ `kash` + `objectives` course.json, chi tiết hóa cho buổi); tiến trình phải cộng đúng `duration_min`; mỗi bài tập nêu sản phẩm nộp + tiêu chí đạt; gate gộp từ gate các bài. Không có activity nào đứng ngoài chuỗi outcome/evidence. Upstream thiếu mapping `CLO/LO/evidence/rubric/resource` → ghi `NEEDS_INPUT`, không tạo ID giả. Nếu muốn thêm nội dung ngoài seed/syllabus, flag rõ cho user duyệt trước.

**5. Build 2 file docx + soạn 2 file .md.** Chạy:
```
python scripts/build_lesson_outputs.py lesson.json <outdir>
```
→ LessonPlan.docx + TaiNguyen-ThamKhao.docx theo đúng chuẩn trình bày Kstudy (`references/presentation-standard.md`). Kiểm tra bằng cách render: `soffice --headless --convert-to pdf` rồi `pdftoppm` xem ảnh. Slide theo `references/slide-outline-template.md`: tiêu đề slide ngắn (thường ≤48 ký tự), mỗi slide có "Mục tiêu học", "Thông điệp chính", "Visual job", "Minh họa", "Gợi ý KSD"; mô tả rõ nên dùng ảnh Kstudy thật, screenshot, sơ đồ, biểu đồ, timeline, ma trận hay ảnh tạo bằng trí tuệ nhân tạo. Cấu trúc slide mở đầu/kết thúc bắt buộc:
- Slide 1 là trang tiêu đề.
- Buổi 1 có môn điều kiện tiên quyết: sau trang tiêu đề lần lượt là "Ôn tập nhanh môn điều kiện tiên quyết" → "Mục tiêu môn học này" → "Bài tập cuối môn" → "Mục tiêu buổi hôm nay".
- Buổi 1 không có môn điều kiện tiên quyết: sau trang tiêu đề lần lượt là "Mục tiêu môn học này" → "Mục tiêu buổi hôm nay".
- Buổi N > 1: sau trang tiêu đề lần lượt là "Ôn tập buổi trước" → "Mục tiêu buổi hôm nay".
- Cuối buổi luôn có "Tổng kết nội dung hôm nay" → "Nội dung buổi sau"; nếu là buổi cuối, thay "Nội dung buổi sau" bằng định hướng hoàn thiện bài tập/cuối môn dựa trên syllabus, không tự bịa phần học mới.
Video theo `references/video-outline-template.md` (đặt tên "Video X.Y", mỗi video kèm "Mục tiêu" + "Định dạng đề xuất" + outline dạng list). Cả hai outline phải giữ các ID `lesson_outcome_ids`, `evidence_ids`, `resource_ids` ở dòng `Traceability:` đầu tài liệu; không tự tạo ID mới.

**6. QA tự động.** Chạy:
```
python scripts/validate_lesson.py lesson.json course.json --slide <Slide-outline.md> --video <Video-outline.md>
```
Nếu `lesson.json` chưa khai báo `lesson_seed_file`, truyền thêm `--seed lesson_seed.json`. Kiểm: gate approved, fingerprint/cascade, seed fingerprint, tổng phút = duration_min, gate buổi không rỗng & đủ so với các bài, độ phủ objectives trong tiến trình/demo/bài tập, KASH đủ 4 nhóm + động từ đo được, wording linter (từ khẩu ngữ, từ tiếng Anh có bản Việt thay thế), mỗi slide có "Minh họa", mỗi video có "Mục tiêu" + "Định dạng đề xuất", số video/bài 3–6, có phân Cốt lõi/Mở rộng, cấu trúc traceability (`traceability` + `approval_status`, `activity_map` có zone/outcome hợp lệ, `formative_checks` có `feedback_action`, `miller_level`, `udl_options`, `resource_map`/`online_resources` URL hợp lệ hoặc placeholder `[CHỜ...]`). Khi chốt buổi để bàn giao pilot, chạy thêm `--ready` để nâng các cảnh báo traceability/activity/formative thành FAIL. **Sửa mọi FAIL trước khi đi tiếp; mỗi WARN phải được xử lý hoặc giải trình với user, không lờ đi.**

**7. Phản biện độc lập + trình duyệt.** Chạy critic theo `references/reviewer-agent.md` (spawn 1 agent phản biện chấm scorecard 7 tiêu chí; sửa hết điểm Chưa/Một phần; verdict "CHƯA" → không trình). Sau đó trình cả bộ 4 file + tóm tắt QA/critic cho user duyệt; sửa theo góp ý. **Buổi pilot được duyệt → tạo/cập nhật `conventions.md` (§Conventions) rồi mới nhân rộng các buổi còn lại.**

## Chuẩn wording (rất quan trọng)

Người học là người Việt mới tốt nghiệp THPT hoặc chưa có kinh nghiệm ngành. Viết dễ hiểu, giọng giảng dạy; **hạn chế từ tiếng Anh** khi có từ tiếng Việt thay thế hợp lý (dùng "trí tuệ nhân tạo", "công cụ/tác nhân"...); chỉ giữ thuật ngữ tiếng Anh cho tên tính năng/sản phẩm (Custom Instructions, Gems, ChatGPT). Tránh từ khẩu ngữ như "Chốt". Wording linter trong `validate_lesson.py` quét tự động — nhưng linter chỉ bắt được danh sách từ đã khai báo, model vẫn chịu trách nhiệm chính.

## Môi trường

Dùng `python-docx` (npm registry có thể bị chặn nên KHÔNG dùng docx-js). Cài: `pip install python-docx --break-system-packages`. Script tự dùng logo bundle trong `assets/kstudy-logo-full.png`.

## Chuẩn đầu vào/đầu ra
- Đầu vào: `course.json` **đã duyệt** (từ kstudy-syllabus-creator, `approved: true`) + `handoff_summary.md`/`resources.index.json` (nếu có) + `conventions.md` (nếu có) + thư mục `ThamKhao/` của môn.
- Đầu ra: mỗi buổi 1 thư mục (`02_LessonPlan/Buoi_<N>/`) chứa `lesson_seed.json` + 4 file đặt tên `<CODE>-B<N>-*`; sau pilot có thêm `conventions.md` ở gốc thư mục môn.

## Reference files
- `references/presentation-standard.md` — chuẩn trình bày docx (màu, font, header/footer, heading, bảng, bullet).
- `references/lesson-json-schema.md` — schema đầy đủ của lesson.json (khớp course.json schema_version 2).
- `references/lesson-seed-schema.md` — schema `lesson_seed.json` sinh từ course.json trước khi soạn buổi.
- `references/slide-outline-template.md` — mẫu + quy ước slide (Minh họa, wording).
- `references/video-outline-template.md` — mẫu + quy ước video (Cốt lõi/Mở rộng, Định dạng đề xuất).
- `references/conventions-template.md` — template conventions.md chống lệch chuẩn giữa các buổi.
- `references/reviewer-agent.md` — quy trình + prompt phản biện độc lập cho bộ học liệu buổi.
- `scripts/validate_lesson.py` — QA tự động lesson.json + 2 file .md đối chiếu course.json; kiểm luôn traceability, Miller, activity_map, formative check, UDL, resource URL (cờ `--ready` cho gate READY_FOR_PILOT).
- Contract traceability dùng chung: `~/.claude/skills/kstudy-curriculum-design/references/traceability-contract.md`.
