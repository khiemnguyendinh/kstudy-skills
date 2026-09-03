# Build, SEO/GEO/AEO và QA

## Build contract

Code phải bám `landing-page-brief.md`, không tự thêm claim, offer, urgency hoặc page. Nếu brief thiếu quyết định ảnh hưởng logic, cập nhật brief và xin approval trước khi code tiếp.

Mặc định dùng stack của project. Với project mới Kstudy, ưu tiên Next.js + TypeScript, server endpoint, Supabase/Postgres và Vercel; không thêm dependency nếu existing stack đủ.

Phân biệt trạng thái:

- `BUILD_READY`: code/local preview/adapter/spec đã hoàn tất và QA local PASS.
- `CONNECTED`: connector cụ thể đã cấu hình và verify ở môi trường ghi rõ.
- `READY_FOR_PUBLISH`: không còn blocker, nhưng chưa production deploy.
- `PUBLISHED`: chỉ sau approval và verify production URL/runtime.

Nếu chưa có production lead store/booking provider, dùng repository/adapter boundary và một local test adapter xác định được success, duplicate, timeout và downstream failure. Ưu tiên local database/emulator đã có trong project; nếu không có, deterministic fake adapter chỉ dùng cho automated test. Không gọi fake adapter là durable production store hoặc `CONNECTED`.

Video thật thiếu không chặn kiểm thử layout, player, progress, CTA và error recovery bằng test media có nhãn. Nó chặn `READY_FOR_PUBLISH` cho đến khi asset manifest chuyển sang `APPROVED` và nội dung/claim/caption được QA.

## Page implementation requirements

- Semantic HTML, correct heading order, keyboard navigation, visible focus.
- Form có label, validation gần field, server validation, loading/success/error/duplicate states.
- Responsive mobile-first; CTA không che content/consent.
- Media có dimensions/aspect-ratio để tránh layout shift; video có caption/transcript path khi khả thi.
- Respect reduced motion; animation phục vụ hierarchy, không cản conversion.
- Không dùng UI kit content làm dữ liệu thật.
- Không tự tạo dashboard/card grid chỉ vì dễ build; layout phục vụ narrative.
- Render đủ `course_explanation` tại page đã khai báo: value, curriculum theo outcome, instructor và FAQ.
- Không thay outcome bằng danh sách chủ đề. Không rút gọn nhiều module thành các card giống nhau nếu làm mất “sau học phần này làm được gì”.
- Bio giảng viên đi cùng ảnh thật đã duyệt; mobile giữ ảnh, tên, vai trò và bio trong cùng context.
- Accordion FAQ phải dùng button semantic, điều khiển được bằng keyboard và không ẩn câu trả lời khỏi HTML crawlable.

## Kstudy visual sequence

1. Dùng UI/UX skill để xác định conversion hierarchy và interaction pattern.
2. Dùng Kstudy Design System cho token, logo, typography và approved assets.
3. Dùng frontend skill để implement.
4. Dùng taste/visual review để loại generic template, kiểm density, rhythm, composition.

Khi hỏi direction, tuân thủ interview mode từng câu một. Lưu `visual_style` và `required_sections` trong state/brief.

## SEO

- Unique evergreen page có thể index nếu phục vụ search intent và có canonical/self-canonical phù hợp.
- Paid/duplicate/test variants dùng canonical hoặc `noindex` theo strategy; không mặc định `noindex` cho mọi landing page.
- Unique title, meta description, one clear H1, crawlable copy, meaningful internal link khi page indexable.
- Sitemap/robots/canonical phải nhất quán với environment.
- Structured data chỉ dùng type/field đủ điều kiện và đúng nội dung visible; không giả review/rating/course data.
- FAQ section có thể hữu ích cho người dùng, nhưng không hứa rich result.

## GEO/AEO

Không tạo “AI SEO trick”. Tập trung:

- entity rõ: Kstudy, course/track, instructor, audience, outcome, format;
- câu trả lời trực tiếp cho query thật;
- heading/FAQ/summary có cấu trúc;
- claim có evidence và ngày cập nhật;
- transcript, curriculum, author/about và policy pages có thể crawl khi phù hợp;
- internal linking và canonical nhất quán.

Khi thực thi, kiểm tra tài liệu chính thức hiện hành của search engine/platform. Không bắt buộc `llms.txt` nếu không có mục tiêu/consumer xác định.

## QA matrix

### Product/message

- Audience/promise đúng course đã duyệt.
- Hero giữ continuity với source/content angle.
- Mọi public claim tồn tại trong claims ledger và `VERIFIED`.
- Course value mô tả năng lực/ứng dụng/quyền lợi cụ thể, không chỉ dùng tính từ quảng cáo.
- Mỗi học phần trong scope có tên dễ hiểu, `can_do`, hands-on output và source ref.
- Thuật ngữ cần thiết được giải thích hoặc thay bằng từ phổ thông; không bê nguyên CLO/LO lên page.
- Tên, vai trò, bio, ảnh và credential của từng giảng viên đều đã xác minh.
- FAQ xuất phát từ objection thật và policy/course source; câu trả lời thẳng, đủ điều kiện và giới hạn.
- Không fake live/urgency/viewer/scarcity.
- CTA phù hợp awareness và next step.

### Funnel/function

- Route registration -> thank-you -> watch -> booking -> success.
- Direct URL, back/refresh, duplicate submit và expired/invalid access có behavior rõ.
- Lead lưu trước async downstream.
- Booking success dựa vào provider/source-of-truth, không chỉ click.

### UI/accessibility

- Mobile/desktop, keyboard, focus, contrast, labels, errors, reduced motion.
- No horizontal overflow, clipped CTA, unreadable overlay hoặc fake UI.
- Asset authentic, optimized và có alt text phù hợp.

### Performance/security/privacy

- Core Web Vitals/performance được đo trong môi trường ghi rõ.
- Không client secret, service role hoặc credential trong bundle/log.
- Server validation, rate limit, abuse protection, safe redirect.
- Consent và privacy copy đúng data flow.

### Tracking

- Event trigger không double-fire.
- `event_id` dedupe browser/server.
- Payload không PII.
- Source/post/content/variant được bảo toàn.
- Destination verification có evidence; nếu chưa thì ghi pending.

### SEO/AEO/GEO

- index policy/canonical/metadata/heading/schema đúng từng page.
- Page test/duplicate không cạnh tranh index.
- Content accessible/crawlable, không giấu toàn bộ value trong video.

## Optimize mode

Ưu tiên diagnostic theo funnel stage và source/audience. Phân biệt:

- instrumentation gap;
- traffic/message mismatch;
- page friction;
- webinar engagement issue;
- booking/qualification issue;
- sales/offer issue.

Không A/B test nhiều biến mà không biết giả thuyết. Mỗi experiment ghi: hypothesis, segment, variant delta, primary metric, guardrail, event source, duration/sample caveat, decision rule và rollback. Không bịa baseline/uplift.
