# Tracking, lead routing và connector contracts

## Measurement principles

- Định nghĩa internal event theo user intent trước, vendor mapping sau.
- Một conversion không được đếm hai lần giữa browser/server; dùng `event_id` và dedupe.
- Không đưa tên, email, phone hoặc PII khác vào URL, UTM, GA4, data layer hay debug log.
- Chỉ hash PII trong server-side adapter khi policy/nền tảng cho phép và consent phù hợp.
- Không báo “đã track” chỉ vì code có `dataLayer.push`; phải verify runtime và destination.

## Core event taxonomy

| Internal event | Trigger |
|---|---|
| `course_view` | Page course/funnel đủ điều kiện view |
| `cta_click` | CTA có intent rõ được click |
| `video_start` | Video thực sự bắt đầu |
| `video_progress` | Milestone đã định, tránh spam |
| `form_start` | User tương tác lần đầu với form |
| `lead_submitted` | Lead đã lưu thành công ở durable store |
| `webinar_registered` | Registration business rule hoàn tất |
| `webinar_watch_started` | Playback bắt đầu trên watch page |
| `webinar_progress_25` | Đạt 25% |
| `webinar_progress_50` | Đạt 50% |
| `webinar_progress_75` | Đạt 75% |
| `webinar_completed` | Đạt completion rule |
| `webinar_cta_viewed` | CTA tư vấn đủ điều kiện nhìn thấy |
| `webinar_cta_clicked` | CTA tư vấn được click |
| `consultation_booked` | Booking provider/server xác nhận |
| `lead_qualified` | Human/system rule đã duyệt xác nhận |
| `enrollment_paid` | Payment source-of-truth xác nhận |

Event properties an toàn: `event_id`, `occurred_at`, `funnel_id`, `course_track`, `page_id`, `landing_variant`, `source`, `post_id`, `content_angle`, `content_format`, `device_class`, `consent_state`. Không tự đưa `user_id` có thể nhận dạng nếu chưa có policy.

Map GA4/Meta/TikTok ở `tracking-plan.md`. Mapping phải ghi source-of-truth, trigger, dedupe và consent. Kiểm tra official docs hiện hành trước khi implement vì API/event policy thay đổi theo thời gian.

## Lead capture reference architecture

```text
Browser form
  -> Server endpoint
  -> Schema validation + normalization
  -> Consent validation
  -> Rate limit / abuse control
  -> Idempotency check
  -> Durable lead store
  -> Return success with lead_id
  -> Async delivery queue/webhook
  -> N8N
  -> Approved downstream systems
```

Quy tắc:

- Store lead trước khi gọi webhook bên thứ ba.
- `lead_id` là idempotency key xuyên suốt; không dựa vào email/phone trong URL.
- Retry có backoff, dead-letter hoặc failed-delivery state và audit log.
- Duplicate submission trả trạng thái dễ hiểu, không tạo lead rác.
- Downstream lỗi không được làm mất lead đã lưu.
- Client không giữ secret; production database dùng RLS/server boundary phù hợp.

## Connector capability model

Trạng thái:

- `UNVERIFIED`: mặc định; chưa được phép tuyên bố capability.
- `AVAILABLE_READ_ONLY`: đã verify và chỉ đọc.
- `AVAILABLE_WRITE_PENDING_APPROVAL`: có thể ghi nhưng chưa được duyệt action hiện tại.
- `APPROVED_FOR_ACTION`: approval cụ thể, có scope và thời điểm.
- `UNAVAILABLE`: tạo contract/fallback local.

Approval có scope theo action; approval đọc analytics không đồng nghĩa approval gửi SMS hoặc deploy.

## Connector contracts

| Connector | Read-only use | Write use cần approval | Fallback |
|---|---|---|---|
| AI Mentor | Course/class context khi tool xác minh | Import/handoff lead hoặc student mutation | Local source + integration spec |
| Drive/Notion/Lark | Đọc tài liệu được cấp quyền | Tạo/sửa/share doc, task, chat | Local files |
| GA4/Search Console | Read baseline/query | Publish config/audience | Tracking spec |
| Meta/TikTok | Read reporting | Pixel/CAPI config, ads/publish | Adapter + event map |
| Supabase | Read schema theo quyền | Migration/write production | Local schema/adapter |
| N8N/Make | Inspect workflow | Create/activate workflow | Workflow contract |
| Email/SMS/Zalo | Inspect template/provider capability | Send/subscribe/group action | Message sequence draft |
| Zoom/webinar | Inspect configuration | Create session/registrant | On-demand local route spec |
| Vercel/hosting | Inspect project | Deploy/domain/env change | Local build/preview |
| Canva/assets | Read/reuse approved assets | Create/publish/export shared design | Asset brief/local placeholder |

## Consent và governance

Mỗi form nêu rõ data fields, purpose, retention owner, marketing opt-in nếu có và privacy link. Transactional access/reminder không được nhập nhằng với marketing consent. Thiết kế unsubscribe/stop rule cho nurture channels.

AI Mentor không phải CRM mặc định. Chỉ tạo student khi có approved business rule, schema mapping, dedupe và owner. Lead lifecycle nên có source-of-truth riêng: `new -> registered -> watched -> booked -> qualified -> enrolled/lost`.

## Verification checklist

- Test happy path và duplicate submit.
- Test timeout/downstream failure.
- Verify lead tồn tại trước webhook.
- Verify event payload không có PII.
- Verify browser/server dedupe.
- Verify consent behavior.
- Verify destination nhận đúng event bằng debug/test tool chính thức.
- Ghi `VERIFIED`, ngày, môi trường và người kiểm tra; không áp kết luận staging cho production.
