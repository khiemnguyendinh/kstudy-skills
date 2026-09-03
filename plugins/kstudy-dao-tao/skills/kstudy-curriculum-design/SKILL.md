---
name: kstudy-curriculum-design
description: >-
  Thiết kế, research, audit và cập nhật khung chương trình đào tạo cấp program
  cho Kstudy từ một ý tưởng lĩnh vực hoặc ngành nghề. Dùng khi cần phân tích
  nghề và job market bằng DACUM, JD 3–6 tháng gần nhất; benchmark chương trình
  đối thủ và khóa học tham chiếu; xác lập KASH/CBET/OBE/CDIO; thiết kế PLO,
  course map, capstone, hybrid workload; xây traceability từ nghề → PLO →
  course/CLO → assessment/activity; hoặc tạo đầu vào đủ chuẩn cho
  kstudy-course-planner. Xuất curriculum-design.json và workbook Excel có cấu
  trúc tương tự khung chương trình Digital Marketing hiện tại. Không dùng để
  viết Syllabus, Lesson Plan, Slide, Video hoặc import/publish vào hệ thống đào tạo.
---

# Kstudy Curriculum Design

## Mục tiêu và ranh giới

Thiết kế một khung chương trình có thể triển khai, kiểm chứng và bàn giao cho
`kstudy-course-planner`, không dừng ở danh sách môn học hoặc outline marketing.
Xuất phát từ nhiệm vụ nghề nghiệp thực tế, quy đổi thành năng lực và thiết kế
kiến trúc chương trình với workload có thể tính toán.

Phân biệt rõ:

- `Kstudy-Curriculum-Design`: cấp program — occupation, job roles, job tasks,
  competencies, PLO, course architecture, workload, capstone, evidence và
  governance.
- `kstudy-course-planner`: cấp course — research sâu cho một course, CLO, lesson
  outline, resources và `curriculum-rd.json` để chuyển sang Syllabus Creator.
- `kstudy-syllabus-creator`: viết Syllabus đã được duyệt.
- `kstudy-lesson-plan-creator`: triển khai từng buổi học từ Syllabus đã duyệt.

Không bịa số liệu, JD, outline đối thủ, source, citation, ngày đăng, learner
feedback hoặc trạng thái truy cập. Tách mọi thông tin thành `CONFIRMED`,
`INFERRED`, `PROPOSED`, `UNKNOWN` và ghi source/evidence tương ứng.

## Chế độ và input

Chọn ngay đầu phiên:

- `NEW_PROGRAM`: tạo chương trình mới từ ý tưởng lĩnh vực/ngành nghề.
- `UPDATE_PROGRAM`: cập nhật chương trình hiện có; giữ baseline và tạo audit.
- `AUDIT_ONLY`: chỉ đánh giá gap, trùng lặp, lỗi thời, workload và traceability.

Chọn research level:

- `LIGHT`: dùng context nội bộ và rà nhanh nguồn chính thức.
- `STANDARD`: thêm learner needs, benchmark chương trình và learning sources.
- `DEEP`: thêm JD/job signals gần đây, benchmark nhiều tầng, tool/resource
  accessibility và kiểm định chéo. Dùng `DEEP` khi ngành mới, ngành biến động
  nhanh hoặc user yêu cầu phân tích thị trường tuyển dụng.

Chọn `design_depth` để kiểm soát mức thiết kế và QA truyền xuống pipeline:

- `LITE`: micro-program hoặc thử nghiệm; giữ occupation signal, PLO và course map
  tối thiểu, chỉ tạo capstone direction.
- `STANDARD`: mặc định cho chương trình B2C; đầy đủ task → competency → PLO →
  course, workload và evidence direction.
- `FULL`: chương trình nghề dài hạn, B2B hoặc liên kết đào tạo; thêm competency
  matrix sâu, job signal gần đây, workload audit, pilot và impact review.

File curriculum cũ chưa có `design_depth` được hiểu là `STANDARD` trong lúc
migration; bản cập nhật kế tiếp phải bổ sung field này.

Input tối thiểu là ý tưởng về lĩnh vực/ngành nghề. Nếu thiếu dữ liệu quan trọng,
tiếp tục bằng giả định có nhãn và hỏi từng câu một; chỉ dừng khi thiếu thông tin
đó làm thay đổi đáng kể scope, learner hoặc thời lượng.

Đọc các tài liệu theo nhu cầu:

1. Đọc [framework-stack.md](references/framework-stack.md) ở mọi phiên.
2. Đọc [research-protocol.md](references/research-protocol.md) khi có market,
   competitor, JD, tool hoặc thông tin cần cập nhật.
3. Đọc [workload-and-hybrid.md](references/workload-and-hybrid.md) khi thiết kế
   thời lượng, modality, session, practice hoặc capstone.
4. Đọc [curriculum-framework-schema.md](references/curriculum-framework-schema.md)
   trước khi tạo JSON.
5. Đọc [traceability-contract.md](references/traceability-contract.md) để tạo
   ID chain và mapping downstream.
6. Đọc [excel-output.md](references/excel-output.md) khi cần xuất hoặc kiểm tra
   workbook Excel.
7. Đọc [quality-gates.md](references/quality-gates.md) trước khi kết luận hoặc
   đặt `handoff.status = READY_FOR_COURSE_PLANNER`.

Nếu tồn tại, ưu tiên framework pack của Kstudy tại:

`/Users/macintoshhd/AI Agent/Quản lý đào tạo Kstudy/Phát triển chương trình/Curriculum Framework/`

Đọc framework card `.md` trước; mở PDF canonical khi cần kiểm tra định nghĩa,
bảng, sơ đồ hoặc source. Không đọc toàn bộ pack nếu chỉ cần một nhánh.

## Workflow chuẩn

### 1. Intake, baseline và Research Brief

Tạo `project_brief` gồm: ý tưởng nghề, business intent, target learner,
delivery model, geography, ngôn ngữ, thời lượng dự kiến, level đầu ra, tool
constraints và output mong muốn.

Với `UPDATE_PROGRAM`, đọc tất cả file được cung cấp, giữ bản hiện tại làm
baseline và đánh dấu mỗi thay đổi `KEEP`, `UPDATE`, `EXPAND`, `MERGE`, `MOVE`,
`REDUCE`, `REMOVE`, `REPLACE`.

Tạo Research Brief trước khi research:

- Câu hỏi cần trả lời.
- PLO hoặc quyết định curriculum mà evidence sẽ hỗ trợ.
- Phạm vi địa lý, thời gian và nhóm learner.
- Freshness requirement.
- Source priority và research gaps dự kiến.

### 2. Phân tích nghề và thị trường lao động

Phân tích theo chuỗi:

`Job family → role → responsibility → task → tool/input → work output → quality standard`

Dùng DACUM/job-task analysis để xác định công việc, không bắt đầu bằng tên môn
học. Với mỗi task quan trọng, ghi: tần suất, độ khó, dependency, mức tự chủ,
điều kiện thực hiện, lỗi thường gặp và evidence có thể quan sát.

Khi phân tích tuyển dụng, tạo bảng evidence với tối thiểu: `source_id`, platform,
job title, organization, posted date, captured date, location, seniority, task,
skill/tool, output, evidence level và limitation. Nếu lọc 3 tháng, dùng cửa sổ
từ `current_date - 3 months` đến `current_date`; nếu 6 tháng thì dùng đúng cửa sổ
đó và ghi ngày bắt đầu/kết thúc trong báo cáo.

Không gọi một mẫu JD nhỏ là “nhu cầu toàn thị trường”. Tách `observed signal`,
`recurring pattern`, `inference` và `research gap`. Với LinkedIn hoặc Facebook
group yêu cầu login, dừng tại trang đó và yêu cầu user tự đăng nhập; không nhận
password, token, cookie hoặc payment information. Nếu không truy cập được, giữ
URL và ghi `[CHỜ TRUY CẬP]`.

### 3. Benchmark chương trình và khóa học tham chiếu

Benchmark public description, curriculum outline, learning outcomes, delivery,
assessment, support, tools, capstone và workload của các nguồn phù hợp. Có thể
tham chiếu Run by Linh, Vinalink, Tomorrow Marketer, VTC Academy, FPT
Polytechnic, FPT International, Coursera, Udemy và đơn vị khác do user chỉ định.

Tách ba lớp:

- Program dài hạn hoặc career path.
- Combo/path gồm nhiều course.
- Course ngắn hạn tương đương với từng course nhỏ trong Kstudy.

Chỉ kết luận từ phần public hoặc tài liệu user cung cấp. Không coi landing page
là syllabus đầy đủ, không mua course, không scrape khóa trả phí, không transcript
hàng loạt video và không sao chép nội dung có bản quyền. Dùng benchmark để tìm
pattern, gap, positioning và mức workload; không copy outline.

### 4. Xây competency architecture

Quy đổi job tasks thành competency units theo KASH:

- `Knowledge`: biết và giải thích nguyên lý, thuật ngữ, decision rule.
- `Attitude`: tiêu chuẩn nghề nghiệp, ownership, ethics, customer/user focus.
- `Skill`: thực hiện được thao tác và tạo work output.
- `Habit`: lặp lại quy trình, tự kiểm tra, ghi chép, cải tiến và vận hành ổn định.

Viết mỗi competency bằng động từ quan sát được, điều kiện thực hiện và tiêu chuẩn
đầu ra. Không dùng “hiểu”, “nắm”, “biết” nếu không kèm evidence kiểm tra được.

Thiết kế PLO theo OBE và adapted CDIO. CDIO là gốc từ engineering; với Digital
Marketing, AI và automation phải ghi rõ `adapted`, không tuyên bố tuân thủ đầy
đủ nếu chỉ mượn nguyên lý. PLO cần bao gồm kiến thức nền, năng lực chuyên môn,
triển khai hệ thống/workflow, communication, ethics, self-learning và capstone.

### 5. Thiết kế program architecture

Thiết kế từ PLO và capstone ngược về course map:

`PLO → competency → course → CLO placeholder → assessment evidence → learning activity`

Mỗi course spec cần có tối thiểu:

- `course_id`, tên đề xuất, purpose và role trong sequence.
- PLO được đóng góp: `I` Introduce, `R` Reinforce, `M` Master/assess.
- Prerequisites và dependency.
- CLO placeholder theo Bloom/KASH.
- Core topics, work artifacts và assessment evidence.
- Modality, workload breakdown và tool/resource constraints.
- Quan hệ với course trước/sau và phần giao cho `kstudy-course-planner`.

Gom course theo stage hoặc track có logic tăng dần: foundation → core execution
→ integration/automation → capstone/portfolio. Gộp hoặc loại nội dung trùng khi
không tạo thêm PLO, artifact hoặc decision capability.

### 6. Thiết kế hybrid workload

Tính riêng và cộng kiểm chứng các thành phần:

- `direct_live_hours`: lớp trực tiếp hoặc Zoom có giảng viên.
- `elearning_hours`: video/readings/quiz có cấu trúc.
- `self_study_hours`: đọc, research, reflection và chuẩn bị.
- `practice_project_hours`: thực hành, production, lab và project.
- `assessment_feedback_hours`: review, rubric, correction và retake.
- `mentor_coaching_hours`: AI Mentor, group coaching hoặc 1-1.

Không gán một hoạt động vào hai nhóm thời lượng. Mỗi activity phải có `mode`,
`minutes`, `artifact`, `assessment_link` và `counts_toward`. Tổng program phải
bằng tổng course; tổng course phải bằng tổng activity đã kiểm kê. Nếu workbook
Digital Marketing ứng dụng AI & Automation hiện tại được dùng làm baseline, chỉ
dùng các số đã xác minh; không biến giả định như số phút/session thành số chính
thức.

### 7. Assessment, capstone và traceability

Thiết kế evidence trước khi khóa topic. Dùng Miller để chọn mức thể hiện phù hợp:
`Knows → Knows how → Shows how → Does`. Dùng Bloom để mô tả độ phức tạp nhận
thức; dùng PBL/WBL khi work artifact là cách tốt nhất để chứng minh năng lực.

Bắt buộc tạo traceability matrix:

`Job task → competency → PLO → course → CLO → activity → artifact/assessment → rubric`

Kiểm tra ba lỗi: orphan PLO, course không đóng góp PLO, activity không phục vụ
CLO/assessment. UDL dùng để thiết kế nhiều cách tiếp cận và thể hiện nhưng không
hạ tiêu chuẩn đầu ra. 4C/ID dùng khi skill phức hợp cần whole task, supportive
information, just-in-time procedural information và part-task practice.

### 8. Review và approval

Thực hiện academic review như Academic Director: scope, sequence, dependency,
job relevance, tool accessibility, learner load, assessment validity,
accessibility, capstone feasibility, overlap và operational cost.

Đánh giá theo CIPP ở cấp chương trình và Kirkpatrick khi cần theo dõi transfer,
behavior hoặc result. Dùng ADDIE như process shell lặp lại, không coi ADDIE là
quality proof. Không xem im lặng là approval; dùng `PROPOSED`, `APPROVED`,
`REJECTED`, `DEFERRED`, `NEEDS_INPUT`, `SUPERSEDED`.

### 9. Handoff cho Course Planner

Chỉ đặt `handoff.status = READY_FOR_COURSE_PLANNER` khi mỗi course đã có identity
đề xuất, purpose, PLO mapping, CLO placeholder, scope, prerequisite, artifact,
assessment direction, modality, workload và source/gap status.

Nếu còn thiếu thông tin không ảnh hưởng blocker, ghi `PROPOSED` hoặc `UNKNOWN` và
tiếp tục. Nếu thiếu thông tin làm thay đổi program scope, learner, duration,
PLO hoặc course architecture, đặt `BLOCKED` và liệt kê câu hỏi cần user quyết
định. Không tự chuyển sang Syllabus Creator.

## Output contract

Mặc định tạo trong project hiện tại:

```text
Curriculum Design/<program-slug>/curriculum-design.json
Curriculum Design/<program-slug>/curriculum-design.xlsx
```

Không tạo `curriculum-design.md` mặc định. Chỉ tạo Markdown report khi anh Khiêm
yêu cầu riêng bản đọc để review hoặc trình bày.

JSON và workbook phải tuân theo [curriculum-framework-schema.md](references/curriculum-framework-schema.md)
và [excel-output.md](references/excel-output.md).

JSON phải có tối thiểu: `schema_version`, `design_mode`, `research_level`, `design_depth`, `status`,
`project_brief`, `occupation_analysis`, `competency_architecture`, `program_outcomes`,
`capstone`, `curriculum_map`, `workload`, `traceability`, `research`, `quality_review`
và `handoff`.

Không ghi đè file hiện có nếu chưa xác định baseline/version. Với update, tạo
version hoặc file mới và giữ audit trail.

Sau khi tạo JSON, chạy:

```text
python3 /Users/macintoshhd/.codex/skills/kstudy-curriculum-design/scripts/validate_curriculum_framework.py <path>/curriculum-design.json
```

Validator chỉ kiểm tra cấu trúc, ID, tổng thời lượng và traceability; không thay
thế research, academic review, source verification hoặc approval của anh Khiêm.

Sau khi JSON PASS, tạo Excel bằng bundled Node.js và `@oai/artifact-tool`:

```text
node /Users/macintoshhd/.codex/skills/kstudy-curriculum-design/scripts/create_curriculum_workbook.mjs \
  <path>/curriculum-design.json \
  <path>/curriculum-design.xlsx
```

Kiểm tra workbook bằng `inspect` và render tất cả sheet trước khi bàn giao. Excel
chỉ là presentation/audit layer của JSON; không tạo một sự thật thứ hai. Các ô
tổng thời lượng phải là formula; evidence/source summary nằm trong sheet
`Traceability & Evidence`; source registry đầy đủ vẫn nằm trong JSON.

## Nguyên tắc quyết định

- Ưu tiên job task và work artifact hơn tên framework hoặc danh sách topic.
- Ưu tiên một architecture nhỏ, có thể vận hành với team lean, hơn một chương
  trình bao phủ quá rộng.
- Ưu tiên năng lực có thể quan sát, đánh giá và chuyển giao vào công việc.
- Tách kiến thức bền vững khỏi thao tác tool dễ lỗi thời; version hóa tool.
- Ghi rõ mọi giả định, gap, trade-off và người cần duyệt.
- Không viết phần nội dung thuộc Syllabus, Lesson Plan, Slide hoặc Video.
