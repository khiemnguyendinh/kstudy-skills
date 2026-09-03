# Workflow, state và quality gates

## Mục đích

Giữ funnel đúng sản phẩm, đúng audience và có thể resume mà không hỏi lại quyết định đã khóa.

## Input đủ dùng

Input tối thiểu:

- Syllabus hoặc `course.json` có version và trạng thái approval.
- Audience cụ thể theo role, business context, department/use case và maturity.
- Acquisition source cụ thể.
- Primary conversion.

Input làm giàu:

- Lesson Plan, assignment, capstone, instructor profile, proof, pricing, FAQ.
- Existing landing page, analytics, CRM disposition, webinar data, sales call notes.
- Brand assets, media, video, legal/privacy copy.

Không bịa phần thiếu. Ghi `UNKNOWN` và quyết định phần thiếu đó có block hay không.

## Gate model

| Gate | PASS khi | BLOCK khi |
|---|---|---|
| Input | Có nguồn course, audience, source, conversion | Không biết đang bán gì/cho ai/chuyển đổi gì |
| Product Truth | Course outcome/use case/capstone giải quyết promise chính | Audience cần outcome không được dạy hoặc không có evidence |
| Research | Finding trọng yếu có source/status | Kết luận quan trọng dựa vào suy đoán bị trình bày như fact |
| Strategy | User duyệt journey, CTA, funnel | Chưa chọn journey hoặc còn trade-off lớn |
| Claims | Claim dùng trong copy có evidence hợp lệ | Fake proof, con số không nguồn, guarantee vô căn cứ |
| Brief | Đủ page/section/state/tracking/routing | Brief chỉ là copy outline, không đủ để build |
| Build | Code hoạt động đúng brief, không có blocker | Form/routing/error state/tracking hoặc mobile hỏng |
| Publish | User duyệt external action và credential/config hợp lệ | Chưa approval, chưa verify connector hoặc còn QA blocker |

## Product Truth rubric

Chấm mỗi chuỗi theo `MATCH`, `PARTIAL`, `MISMATCH`, `UNKNOWN`:

1. Audience role và operating context.
2. Trigger/problem ưu tiên.
3. Promise/desired outcome.
4. Course learning outcome.
5. Lesson/use case tạo ra outcome.
6. Capstone/assessment hoặc artifact chứng minh.
7. Delivery/support phù hợp mức năng lực.

Block nếu promise chính có `MISMATCH`, hoặc `UNKNOWN` ảnh hưởng trực tiếp quyết định mua. `PARTIAL` chỉ pass khi copy thu hẹp promise đúng phần course thực sự cung cấp.

## Khi phát hiện product gap

`product-gap-report.md` phải chỉ rõ:

- audience và promise đang yêu cầu;
- evidence từ course hiện tại;
- mismatch theo outcome/lesson/capstone;
- rủi ro nếu vẫn chạy funnel;
- ba lựa chọn: đổi audience/promise, cập nhật product, hoặc tách course/track;
- handoff được đề xuất, nhưng không tự kích hoạt.

Ghi state `PRODUCT_GAP`. Khi có course mới hoặc audience/promise/maturity mới, chạy đúng ba snapshot reset/evaluate/approve bên dưới rồi mới resume. Giữ nguyên acquisition/conversion/connector decisions nếu vẫn còn hiệu lực.

## State machine

```text
INITIALIZED
  -> PRODUCT_REVIEW
PRODUCT_REVIEW
  -> PRODUCT_GAP | RESEARCH
PRODUCT_GAP
  -> PRODUCT_REVIEW              # course/audience revision reset
RESEARCH
  -> STRATEGY_REVIEW
  -> BRIEF_REVIEW
  -> READY_FOR_BUILD
  -> BUILDING
  -> READY_FOR_QA
  -> BUILD_READY
  -> CONNECTED                    # optional, per connector
  -> READY_FOR_PUBLISH
  -> PUBLISHED
```

`BLOCKED` dùng khi thiếu input/approval/capability không thể tiếp tục. External action pending không làm hỏng artifact local; ghi riêng `pending_external_actions`.

`COMPLETE` chỉ dùng cho Strategy hoặc Optimize đã hoàn tất đúng `completion_scope`. Build không dùng `COMPLETE`; trạng thái cuối phản ánh chính xác local build, connection hay production publish.

## Gate transition contract

| Gate value | Ý nghĩa | Transition hợp lệ |
|---|---|---|
| `PENDING` | Chưa đánh giá hoặc đã reset vì source/audience/maturity đổi | `PASS`, `BLOCKED`, `FAIL`; không đi thẳng `APPROVED` |
| `PASS` | Agent/validator đã kiểm tra đủ evidence, chưa có user approval bắt buộc | `APPROVED`, `BLOCKED` nếu evidence mới làm thay đổi kết luận |
| `APPROVED` | User đã duyệt quyết định của gate | downstream có thể bắt đầu |
| `BLOCKED`/`FAIL` | Không thể tiếp tục | chỉ về `PENDING` qua revision snapshot có lý do |
| `SKIPPED` | Không thuộc mode/scope | chỉ dùng khi SKILL định nghĩa rõ |

`status` và `current_gate` phải phản ánh gate đang xử lý. Ví dụ Product Truth mismatch: `status=PRODUCT_GAP`, `current_gate=PRODUCT_TRUTH`. Sau reset: `status=PRODUCT_REVIEW`, `current_gate=PRODUCT_TRUTH`, Product Truth/downstream đều `PENDING`.

## Resume contract: ba snapshot bắt buộc

Khi course fingerprint hoặc audience fingerprint thay đổi:

1. Snapshot reset: cập nhật source/contract + fingerprint, ghi `revision_reason`, đặt `status=PRODUCT_REVIEW`, `current_gate=PRODUCT_TRUTH`, reset Product Truth và toàn bộ downstream về `PENDING`, xóa approval record cũ. Validate snapshot này với `--previous`.
2. Snapshot evaluate: giữ nguyên fingerprint, chạy Product Truth trên source/audience mới, đặt `PASS` hoặc `BLOCKED`. Validate với snapshot reset làm `--previous`.
3. Snapshot approve: nếu gate `PASS`, xin user approval cho audience/promise/maturity; sau approval mới đặt `APPROVED` và ghi `product_truth_approval` gồm course fingerprint, audience fingerprint, decision ID và approved time. Validate với snapshot evaluate làm `--previous`.

Không thay fingerprint và đặt Product Truth `PASS/APPROVED` trong cùng snapshot. Nếu chỉ đổi wording không làm audience contract thay đổi, ghi decision note; nếu role/JTBD/desired outcome/anti-persona/AI maturity đổi thì phải cập nhật audience fingerprint và reset.

## Definition of done theo mode

- `STRATEGY`: Product Truth và các approval gate đã `APPROVED`; có sources/claims, audience, 3–5 journeys, selected journey, funnel blueprint, final brief và tracking/asset plan.
- `BUILD`: tất cả Strategy output + working funnel + server capture contract + QA report.
- `OPTIMIZE`: baseline evidence + prioritized issues + approved experiment spec; nếu triển khai thì thêm test instrumentation và rollback.
