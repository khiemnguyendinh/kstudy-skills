---
name: kstudy-build-course-funnel
description: >-
  Nghiên cứu, thiết kế, build và tối ưu funnel tuyển sinh cho một khóa học Kstudy
  từ Syllabus/course.json/lesson plan đã duyệt. Dùng khi cần tạo landing page theo
  từng chân dung khách hàng, webinar/VSL, trang cảm ơn/xem nội dung/đặt lịch, content
  journey, brief chuyển đổi, tracking, SEO/GEO/AEO, prompt frontend hoặc code funnel;
  đặc biệt khi cần diễn giải lợi ích, nội dung từng học phần, giảng viên và FAQ theo
  hướng “học xong làm được gì” bằng ngôn ngữ khách hàng dễ hiểu. Điều phối các skill
  marketing, Kstudy Design System và frontend hiện có; bắt buộc kiểm tra Product
  Truth, evidence và approval trước khi build/publish. Không dùng để sửa Curriculum,
  Syllabus, Lesson Plan hoặc tự gửi/publish/deploy ra hệ thống thật.
---

# Kstudy Build Course Funnel

Biến học liệu khóa học đã duyệt thành một funnel tuyển sinh nhất quán từ điểm chạm đầu tiên đến chuyển đổi cuối. Giữ core chạy được chỉ với file local; connector chỉ làm giàu dữ liệu hoặc thực thi tích hợp sau khi đã xác minh và được duyệt.

## Ranh giới bắt buộc

- Không sửa Curriculum, Syllabus, Lesson Plan, Slide hoặc course outcome.
- Không tiếp tục funnel khi sản phẩm không khớp audience/promise/use case đã chọn.
- Không bịa testimonial, số học viên, kết quả, ROI, lịch khai giảng, ưu đãi, credential, trạng thái live hoặc scarcity.
- Không dùng fake countdown, fake viewer count, fake seat count hoặc webinar giả-live.
- Không thu thập PII trong URL, analytics payload hoặc client log.
- Không hardcode token, secret, service-role key hoặc credential.
- Không tự gửi email/SMS/Zalo, tạo Zoom, ghi production DB, publish GTM/pixel, deploy, đăng Fanpage hoặc thay đổi hệ thống thật.
- Mọi external write/send/publish/deploy/migration cần approval riêng ngay trước thao tác.

## Chọn mode

Xác định một mode chính và ghi vào `workflow-state.json`:

- `STRATEGY`: research, Product Truth, audience, message, journey, funnel blueprint, brief và asset/tracking plan; không build code.
- `BUILD`: chạy lại các gate, hoàn thiện brief rồi build toàn bộ funnel trong phạm vi đã duyệt, gồm trạng thái lỗi và tracking hooks.
- `OPTIMIZE`: audit funnel đang có bằng evidence thật; đề xuất hoặc triển khai thí nghiệm có hypothesis, primary metric và guardrail.

Nếu user yêu cầu “làm landing page” nhưng chưa có strategy đã duyệt, bắt đầu ở `STRATEGY`. Nếu user yêu cầu trọn gói, đi từ `STRATEGY` sang `BUILD` nhưng vẫn dừng tại các approval gate.

## Workflow chuẩn

### 0. Khởi tạo state và intake

Copy `assets/templates/workflow-state.json` vào thư mục dự án. Ghi đường dẫn nguồn, version, audience, AI maturity, acquisition source, conversion goal, mode, connector status và mọi quyết định đã duyệt. Tạo fingerprint cho cả course source và audience contract. Product Truth approval phải lưu đúng hai fingerprint cùng decision record; approval cũ không được tái sử dụng sau revision. State là nguồn tiếp tục công việc; không hỏi lại quyết định đã có.

Đọc tối thiểu:

1. Syllabus hoặc `course.json` đã duyệt.
2. Lesson Plan nếu claim/use case cần độ chi tiết sâu.
3. Brand/design context Kstudy.
4. Funnel hoặc dữ liệu hiện tại nếu chạy `OPTIMIZE`.

Chạy kiểm tra cấu trúc input:

```bash
python3 scripts/validate_funnel.py course path/to/course.json
python3 scripts/validate_funnel.py state path/to/workflow-state.json
```

Validator chỉ kiểm cấu trúc; không thay thế đánh giá chất lượng hay xác minh claim.

### 1. Product Truth Gate

Đối chiếu trực tiếp `audience -> job/problem -> desired outcome -> course outcome -> lesson/use case -> capstone/evidence`. Đọc [references/workflow-and-gates.md](references/workflow-and-gates.md) để chấm gate.

Nếu có mismatch trọng yếu:

1. Tạo `product-gap-report.md` từ template.
2. Đặt `status = PRODUCT_GAP`, `gates.PRODUCT_TRUTH = BLOCKED`.
3. Nêu nội dung hiện có, nội dung audience cần, khoảng trống và đề xuất handoff.
4. Dừng. Không tự gọi Course Planner/Syllabus Creator, không sửa học liệu, không viết funnel như thể sản phẩm đã phù hợp.

Chỉ resume khi nhận bản học liệu đã cập nhật hoặc user thay audience/promise/maturity. Giữ lại source, channel, CTA và các quyết định khác trong state. Resume bắt buộc có ba snapshot: (1) cập nhật fingerprint + `revision_reason`, reset `PRODUCT_TRUTH` và downstream về `PENDING`; (2) đánh giá nguồn mới và chuyển Product Truth `PASS`; (3) sau user approval mới đặt `APPROVED` và ghi approval record khớp hai fingerprint. Không đổi source/audience và pass gate trong cùng snapshot; không nhảy từ `PENDING` thẳng sang `APPROVED`.

### 2. Audience, demand và online behavior

Tách primary persona, secondary persona và anti-persona. Nghiên cứu JTBD, trigger, pain, desired gain, objection, language, awareness, buying committee, behavior online và các điểm chạm. Với mỗi finding, ghi `CONFIRMED`, `INFERRED`, `PROPOSED` hoặc `UNKNOWN` và link về source.

Đọc [references/research-and-messaging.md](references/research-and-messaging.md). Không coi toàn bộ organic traffic là warm; giữ continuity từ `source/post_id/content_angle/content_format/landing_variant` đến hero, proof và CTA.

Có thể dùng `$ck:research` hoặc web/connector read-only để thu thập evidence khi cần dữ liệu bên ngoài. Với thông tin biến động, kiểm tra nguồn chính thức hiện hành và ghi ngày truy cập. Core workflow không phụ thuộc việc các capability này có sẵn.

### 3. Chọn content journey và funnel

Đề xuất 3–5 journey khác nhau, không chỉ đổi headline. Mỗi journey phải có:

- awareness assumption và entry promise;
- content formula/phễu dùng và lý do tương thích;
- sequence từ hook đến proof, objection, mechanism, offer và CTA;
- vai trò video/webinar;
- ưu, nhược, rủi ro, evidence cần có và conversion friction;
- post-conversion routing.

Khuyến nghị một journey, nhưng không xem silence là approval. Khóa `selected_journey` trước khi tạo final brief. Đọc [references/journey-and-funnel-system.md](references/journey-and-funnel-system.md).

Có thể dùng `$ck:copywriting` để phát triển copy theo journey đã chọn. Skill này vẫn sở hữu message hierarchy, claims ledger và approval; copywriting skill không được thay đổi Product Truth hoặc tự thêm claim.

Khi chuyển học liệu sang ngôn ngữ bán khóa học, không bê nguyên CLO/LO, tên kỹ thuật hoặc danh sách chủ đề lên landing page. Chuyển mỗi outcome thành hành động hoặc sản phẩm công việc mà khách hàng có thể hình dung, nhưng không mở rộng quá course outcome đã duyệt.

### 4. Thiết kế experience ngoài landing page

Xây funnel theo conversion goal thật: lead magnet, webinar, VSL, booking, tư vấn 1-1, upsell, downsell, telesale, email/SMS/Zalo, group, Zoom hoặc auto webinar chỉ khi phù hợp.

Mỗi node phải có `trigger -> owner -> tool -> action -> output -> SLA -> error handling -> approval`. Không thêm kênh chỉ vì tool có sẵn. Với evergreen webinar, công khai là on-demand/recorded; không giả lập live.

### 5. Viết blueprint, brief và asset plan

Tạo các artifact cần thiết từ `assets/templates/`:

- `source-and-claims-ledger.md`
- `audience-and-journey.md`
- `funnel-blueprint.md`
- `landing-page-brief.md`
- `asset-manifest.md`
- `tracking-plan.md`
- `frontend-agent-prompt.md`

Brief phải mô tả từng **section**: mục tiêu tâm lý, heading/paragraph/microcopy/link, hierarchy, proof, visual/video/form/CTA, layout, responsive behavior, interaction, state lỗi, tracking và chuyển hướng. Không nhầm `section` với course session.

Mọi landing page giới thiệu khóa học phải chỉ rõ một `course_explanation.page_id` và có đủ bốn cụm:

1. **Giá trị khóa học**: “Sau khóa học bạn làm được gì”, ứng dụng vào công việc nào và quyền lợi/hỗ trợ nào đã được xác minh.
2. **Nội dung học dễ hiểu**: mỗi học phần có tên hướng khách hàng, ít nhất một câu “sau học phần này bạn có thể tự tay làm gì”, đầu ra thực hành và source ref.
3. **Giảng viên**: một hoặc nhiều giảng viên, vai trò trong khóa học, bio ngắn liên quan trực tiếp, ảnh và credential có nguồn xác minh.
4. **FAQ**: trả lời objection thật về mức đầu vào, mức phù hợp, thời gian, công cụ, hỗ trợ, học bù/quyền truy cập hoặc chính sách đã xác minh.

Đọc [references/course-offer-copy.md](references/course-offer-copy.md) trước khi viết bốn cụm này. Nếu thiếu outcome, quyền lợi, profile giảng viên, ảnh hoặc policy cần cho public copy, đặt `NEEDS_INPUT` và chặn `BRIEF` approval; không điền bằng suy đoán.

Mọi claim xuất hiện trong copy phải có `claim_id` và evidence. Chạy:

```bash
python3 scripts/validate_funnel.py claims path/to/source-and-claims-ledger.md
python3 scripts/validate_funnel.py brief path/to/landing-page-brief.md \
  --claims path/to/source-and-claims-ledger.md --strict
```

### 6. Build frontend

Chỉ chạy khi `PRODUCT_TRUTH`, `STRATEGY`, `CLAIMS` và `BRIEF` đều `APPROVED`, không chỉ `PASS`. Dùng skill theo thứ tự:

1. `$ck:ui-ux-pro-max` để chọn UX pattern, conversion hierarchy và accessibility direction.
2. `$kstudy-design-system` để áp token, logo, typography, asset và component contract của Kstudy.
3. `$ck:frontend-design` để xây giao diện production-grade.
4. `$design-taste-frontend` để loại generic AI slop và review visual craft.

Thứ tự ưu tiên khi có xung đột:

`product truth/evidence/ethics > audience/conversion strategy > Kstudy brand > accessibility/performance > decorative taste`.

Không copy số liệu, testimonial, avatar, pricing hoặc content mẫu từ UI kit. Đọc [references/build-seo-and-qa.md](references/build-seo-and-qa.md) trước khi code.

Trong `BUILD`, nếu scope là full webinar funnel, tạo và nối đủ:

- registration landing page;
- thank-you/confirmation page;
- on-demand watch page;
- consultation booking flow;
- loading, empty, validation, duplicate submission, expired/invalid link và integration failure states;
- server-side lead capture, idempotency, tracking hooks và consent behavior.

Frontend phải render đúng bốn cụm course explanation tại `course_explanation.page_id`, giữ nguyên thứ tự/hierarchy đã duyệt. Không thay nội dung cụ thể bằng card chung chung, icon trang trí hoặc danh sách tên bài học lấy nguyên từ syllabus.

### 7. Connector và tracking

Mọi connector bắt đầu `UNVERIFIED`. Chỉ dùng read-only sau khi xác minh capability; action ghi dữ liệu cần approval riêng. Đọc [references/tracking-and-connectors.md](references/tracking-and-connectors.md).

Không mặc định AI Mentor là CRM. Lead chỉ thành student sau rule/handoff được duyệt. Kiến trúc mặc định:

`browser -> server endpoint -> validate/rate-limit/idempotency -> durable lead store -> async webhook -> N8N -> downstream`.

Track event nội bộ theo intent, rồi map sang GA4/Meta/TikTok. Dùng `event_id` để dedupe browser/server. Không báo pixel “đã gắn” nếu chưa verify trong runtime và nền tảng đích.

### 8. QA, handoff và optimize

Chạy QA theo [references/build-seo-and-qa.md](references/build-seo-and-qa.md) và tạo `qa-report.md`. Verify tối thiểu: message continuity, claims, course value, outcome từng học phần, plain-language, profile giảng viên, FAQ, form/routing, mobile, accessibility, performance, SEO/AEO/GEO, analytics payload, error states và no-fake-urgency.

`OPTIMIZE` chỉ dùng dữ liệu quan sát được. Mỗi test phải có hypothesis, page/audience/source, one primary metric, guardrails, sample-size caveat, start/end rule và rollback. Không tuyên bố uplift trước khi đủ evidence.

Ở `BUILD`, phân biệt `BUILD_READY` (local/integration-ready), `CONNECTED` (connector đã verify), `READY_FOR_PUBLISH` và `PUBLISHED`. Không gộp các trạng thái này thành “đã xong”.

`BUILD_READY` cho phép production connector và media cuối còn pending, nhưng local route/test adapter phải chạy và gap phải ghi rõ. Video/webinar thật còn thiếu sẽ block `READY_FOR_PUBLISH`; dùng test media/placeholder có nhãn chỉ để verify watch experience, không phát hành như content thật.

## Connector policy

- Core local bắt buộc hoạt động dù không có connector.
- Read-only có thể tự dùng sau khi đã verify: AI Mentor/Drive, web research, analytics/Search Console, ads reporting, asset library.
- Write-capable nhưng luôn approval: Supabase, N8N, Lark, email, SMS, Zalo, Zoom/webinar, ads/pixel publish, Vercel/deploy, Fanpage/Canva publish.
- Nếu connector không có, tạo integration contract và checklist; không giả lập trạng thái đã kết nối.

## Output contract

Tùy phase, artifact set có thể gồm:

```text
funnel-project/
  workflow-state.json
  product-gap-report.md        # chỉ khi gate BLOCKED
  source-and-claims-ledger.md
  audience-and-journey.md
  funnel-blueprint.md
  landing-page-brief.md
  asset-manifest.md
  tracking-plan.md
  frontend-agent-prompt.md
  qa-report.md
  app-or-site/                 # chỉ ở BUILD
```

Chỉ dùng `status = COMPLETE` cho `STRATEGY` hoặc `OPTIMIZE` khi deliverable đúng mode đã hoàn tất và ghi rõ `completion_scope`. Với `BUILD`, dùng `BUILD_READY`, `CONNECTED`, `READY_FOR_PUBLISH` hoặc `PUBLISHED`; không dùng `COMPLETE` để che external action còn pending.

Chỉ tạo artifact thuộc phase hiện tại. Ví dụ Product Truth BLOCKED chỉ cần state và product gap report; không sinh hàng loạt brief rỗng để tạo cảm giác tiến độ.

## Approval protocol

Dùng `PROPOSED`, `APPROVED`, `REJECTED`, `DEFERRED`, `NEEDS_INPUT`, `BLOCKED`. Hỏi từng quyết định có ảnh hưởng lớn nhất. Approval bắt buộc tại:

1. audience/promise sau Product Truth;
2. selected journey và funnel architecture;
3. final brief/claims trước Build;
4. external write/send/publish/deploy;
5. experiment launch trong Optimize.

Không suy diễn approval từ việc user không phản hồi.
