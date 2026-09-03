---
name: kstudy-course-planner
description: >-
  Thiết kế, research, audit và cập nhật Curriculum cho course Kstudy trước bước
  kstudy-syllabus-creator. Dùng khi user muốn tạo course mới, nghiên cứu nhu cầu
  thị trường, benchmark đối thủ/Udemy/Coursera/YouTube, thiết kế outline hybrid,
  rà soát course đã có, loại bỏ hoặc gộp nội dung lỗi thời, hoặc tạo Course Plan.
  Xuất một file curriculum-rd.json đủ dữ liệu để handoff sang kstudy-syllabus-creator;
  bắt buộc có traceability từ job task/competency/PLO đến CLO/evidence/resource;
  không dùng để build Syllabus, Lesson Plan, Slide hoặc Video.
---

# Kstudy Course Planner

Thiết kế và cập nhật Curriculum R&D cho Kstudy theo hướng evidence-first, thực tiễn, cập nhật và phù hợp hybrid learning. Output chính là một `curriculum-rd.json` dùng làm input cho `kstudy-syllabus-creator`.

## Ranh giới bắt buộc

- Chỉ làm Curriculum R&D, research, academic audit, outline và Course Plan.
- Bảo toàn và mở rộng traceability contract; không làm đứt ID chain từ Curriculum
  Design sang Syllabus Creator.
- Không build `course.json` cuối, `.xlsx`, `.html`, `.docx` Syllabus.
- Không soạn Lesson Plan, Slide hoặc Video; chuyển tiếp cho skill tương ứng sau khi Syllabus được duyệt.
- Không tự import vào AI Mentor, không tự publish, không gửi nội dung ra ngoài.
- Không bịa số liệu, learner feedback, syllabus đối thủ, link, citation hoặc trạng thái truy cập.
- Không tự đặt giá trị chính thức cho `code`, `title`, `author`, `color`, `logo` hoặc `prerequisites`. Có thể đề xuất, nhưng phải ghi `PROPOSED` và chờ user xác nhận.

## Chọn chế độ

Xác định ngay đầu phiên:

- `NEW_COURSE`: course mới hoặc khóa độc lập.
- `UPDATE_COURSE`: course đã có Syllabus/Course Plan/Lesson Plan cần cập nhật.
- `AUDIT_ONLY`: chỉ audit và đề xuất thay đổi, chưa tạo outline mới.

Xác định thêm mức research:

- `LIGHT`: nội bộ + rà nhanh nguồn chính thức.
- `STANDARD`: learner/market needs, competitor benchmark và nguồn học tập chính.
- `DEEP`: thêm job signals, learner evidence, benchmark sâu và kiểm tra tool/resource.

Nếu user không chỉ định, dùng `STANDARD` cho course mới; dùng `LIGHT` cho thay đổi tài nguyên nhỏ và nâng lên `STANDARD` khi thay đổi outcome, scope, đối tượng hoặc cấu trúc course.

Chọn `design_depth` để kiểm soát mức traceability:

- `LITE`: micro-course/khóa thử nghiệm; giữ JT/PLO/CLO/evidence direction tối thiểu.
- `STANDARD`: mặc định cho course B2C; khóa đầy đủ CLO, lesson outcome, evidence,
  rubric direction và resource mapping.
- `FULL`: chương trình nghề dài hạn, B2B hoặc liên kết đào tạo; full chain,
  workload audit, pilot và impact review.

Curriculum cũ chưa có `design_depth` được hiểu là `STANDARD` trong lúc migration;
khi cập nhật lần tiếp theo, bổ sung field này để khóa rõ độ sâu thiết kế.

## Workflow

### 1. Intake và baseline

Đọc toàn bộ tài liệu được cung cấp: khung chương trình, `course.json`, Syllabus, Lesson Plan, Slide, Video, assignment, ebook, PDF, Excel, ảnh và danh sách link. Với Excel/PDF có layout hoặc shape, kiểm tra visual khi extraction dạng bảng không đủ.

Lập trạng thái cho dữ liệu:

- `[CÓ]`: có nguồn rõ ràng.
- `[SUY RA]`: suy luận hợp lý, cần user duyệt.
- `[THIẾU]`: cần hỏi.
- `[MÂU THUẪN]`: các nguồn không thống nhất.

Ở `UPDATE_COURSE`, giữ baseline hiện tại và tạo `update_audit`; nội dung chưa bị ảnh hưởng phải được đánh dấu `KEEP`, không viết lại âm thầm.

### 2. Learner, nhu cầu và outcome

Xác định primary learner, secondary learner, anti-persona, trình độ, công việc, thiết bị, thời gian và điều kiện học. Phân tích JTBD, pain point, desired outcome và evidence source; tách `CONFIRMED`, `INFERRED`, `PROPOSED`, `UNKNOWN`.

Dựng outcome v0 và capstone trước outline. Map outcome với CDIO, Bloom, KASH và bằng chứng đánh giá. Outcome cuối chỉ được khóa sau benchmark và Academic Review.

### 3. Research

Research phải bắt đầu từ Research Brief: câu hỏi cần trả lời, outcome liên quan, phạm vi, mức freshness và nguồn ưu tiên. Ưu tiên nguồn nội bộ Kstudy, sau đó official documentation/primary sources, giáo trình/ebook/nghiên cứu, trang chính thức của đối thủ, Udemy/Coursera/YouTube và nguồn thứ cấp.

Chạy các nhánh cần thiết:

- Market: job task, kỹ năng tuyển dụng, nhu cầu learner.
- Competitor: promise, audience, outline công khai, delivery, assessment, support, tool và khoảng trống.
- Learning content: framework, khái niệm, giáo trình, ebook, case.
- Tool/trend: version, tính năng, giới hạn truy cập, thay đổi quy trình và fallback.

Không trình bày nội dung marketing công khai của đối thủ như syllabus đầy đủ. Mỗi finding phải liên kết với `source_id` và có evidence level.

### 4. Academic audit và refresh

Với course cũ, đánh giá từng lesson/topic theo các action:

`KEEP` · `UPDATE` · `EXPAND` · `MERGE` · `MOVE` · `REDUCE` · `REMOVE` · `REPLACE`.

Chỉ đề xuất thay đổi khi có lý do cụ thể: lỗi thời, ưu tiên thấp, effort cao nhưng utility thấp, trùng lặp, không phục vụ outcome, không phù hợp learner/hybrid, tool khó truy cập hoặc có nội dung quan trọng hơn cần đưa vào.

Phân biệt kiến thức nền bền vững với thao tác tool đã lỗi thời. Mỗi đề xuất cần nêu nội dung cũ, evidence, lý do, nội dung mới, ảnh hưởng tới outcome/workload/resource và trạng thái approval.

### 5. Outline và Academic Director Review

Đề xuất một phương án khuyến nghị và tối đa hai phương án thay thế. Mỗi phương án gồm session, topic, framework/tool, outcome, artifact, class activity, e-learning, AI Mentor activity, internet extension, workload và trade-off.

Đóng vai Academic Director để phản biện: scope, độ khó, sequence, tính thực tiễn, tính cập nhật, khả năng truy cập tool, accessibility, hybrid fit, dependency, nội dung cần loại bỏ và rủi ro overload. Sau review mới chốt outcome v1, scope và outline.

### 6. Resource map, alignment và handoff

Map mỗi topic/lesson với tài nguyên core, extension, tool chính, tool thay thế, tài liệu lớp, e-learning, AI Mentor và nguồn internet. Bài tự học ở nhà phải tách khỏi thực hành tại lớp; lớp học tập trung review, demo, coaching và xử lý lỗi.

Thiết kế theo UbD trước khi khóa outline: xác định CLO draft, evidence/capstone,
assessment method và rubric direction rồi mới chọn lesson/resource/activity.
Chạy Constructive Alignment QA cho từng CLO: được dạy ở đâu, được kiểm tra bằng
evidence nào, có rubric nào, resource nào phục vụ và gate có đòi nội dung chưa dạy
hay không. Mỗi activity phải truy được về CLO; mỗi evidence phải truy được về
rubric.

Đọc contract chung tại:

`/Users/macintoshhd/.codex/skills/kstudy-curriculum-design/references/traceability-contract.md`

Giữ nguyên `JT-*`, `COMP-*`, `PLO-*` từ Curriculum Design. Tạo thêm `CLO-*`,
`EVID-*`, `RUBRIC-*` và `RES-*`; không đổi ID theo title hoặc thứ tự lesson.

Chỉ đặt `handoff.status = READY_FOR_SYLLABUS` khi đã xác nhận: title, code, author, prerequisites, learner, outcome, capstone, sessions, outline lessons, resource status, assessment blueprint, traceability chain và các câu hỏi blocker. Nếu thiếu, đặt `BLOCKED` và liệt kê câu hỏi cần user trả lời.

## Research: quy tắc truy cập và đăng nhập

Khi website yêu cầu đăng nhập:

1. Dừng tại domain đó.
2. Yêu cầu user tự đăng nhập trên browser hiện tại.
3. Không yêu cầu hoặc tiếp nhận password, token, cookie hay payment information.
4. Chờ user báo đã đăng nhập rồi mới tiếp tục.
5. Nếu user không đăng nhập, dùng nguồn public và ghi research gap.

Không tự mua khóa học, không scrape toàn bộ khóa trả phí, không transcript hàng loạt video và không sao chép nội dung có bản quyền. Chỉ tóm tắt phần được truy cập hợp lệ, metadata, preview, mục lục, description, timestamp cần thiết hoặc tài liệu user cung cấp.

Nếu browser/login capability không khả dụng, giữ URL, ghi `[CHỜ TRUY CẬP]` và không bịa phần nội dung bên trong.

## Citation và evidence

Mỗi source phải có tối thiểu: `source_id`, `source_type`, `title`, `author_or_org`, `published_or_updated`, `url`, `accessed_at`, `access_status`, `evidence_level`, `supports`, `citation`.

Citation mẫu:

- Sách/ebook: Tác giả. (Năm). *Tên sách* (edition). Nhà xuất bản. Chương/trang nếu có.
- Official web: Tổ chức. (Năm hoặc ngày cập nhật). *Tên trang*. URL. Ngày truy cập.
- YouTube: Kênh. (Ngày đăng). *Tên video* [Video]. YouTube. URL, timestamp nếu dùng.
- Udemy/Coursera: Instructor/organization. (n.d. hoặc ngày truy cập). *Tên khóa học*. Nền tảng. URL.
- Competitor page: Đơn vị. (Ngày truy cập). *Tên khóa/trang*. URL. Ghi rõ nếu chỉ là public description.

Không tự điền tác giả/năm/edition khi không tìm thấy; dùng `unknown` và ghi gap. Tóm tắt/paraphrase, không sao chép dài từ nguồn có bản quyền.

## Output contract

Mặc định chỉ ghi một file:

```text
Course_Planner/<course-folder>/curriculum-rd.json
```

JSON phải là superset có cấu trúc của input Syllabus Creator, gồm tối thiểu:

- `schema_version`, `planner_mode`, `research_level`, `design_depth`, `status`.
- `course`: context, identity status, learner, needs, scope, outcomes, capstone, prerequisites, sessions, lessons, hybrid, resources và assessment blueprint.
- `research`: brief, findings, sources, gaps và recommendations.
- `traceability`: job tasks, competencies, PLOs, CLOs, evidence, rubric, resources,
  mappings, alignment status và approval status.
- `update_audit`: chỉ bắt buộc ở `UPDATE_COURSE`.
- `handoff`: target skill, status, blocking questions và assumptions.

Bản trình bày research/outline để user duyệt nằm trong hội thoại; chỉ tạo Markdown report nếu user yêu cầu.

Đọc [references/course-rd-schema.md](references/course-rd-schema.md) trước khi viết JSON. Đọc [references/research-and-citations.md](references/research-and-citations.md) khi có web/ebook/video/competitor research. Đọc [references/academic-update-audit.md](references/academic-update-audit.md) ở `UPDATE_COURSE`. Đọc [references/hybrid-and-scope.md](references/hybrid-and-scope.md) khi thiết kế session và workload. Đọc traceability contract dùng chung trước khi khóa handoff.

Sau khi viết JSON, chạy:

```text
python scripts/validate_curriculum_rd.py curriculum-rd.json
```

Validator PASS chỉ xác nhận cấu trúc và blocker; không thay thế academic review hoặc xác minh sự thật của nguồn.

## Approval protocol

Không xem silence là approval. Dùng trạng thái `PROPOSED`, `APPROVED`, `REJECTED`, `DEFERRED`, `NEEDS_INPUT`, `SUPERSEDED`. Hỏi từng nhóm quyết định có ảnh hưởng lớn nhất, không dump toàn bộ câu hỏi một lượt.

Không được chuyển sang Syllabus Creator khi `handoff.status` còn `BLOCKED`, còn định danh chính thức chưa xác nhận hoặc còn source gap ảnh hưởng trực tiếp tới outcome/resource bắt buộc.
