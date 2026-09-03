# Acceptance case: Enter AI for Operations

Tài liệu này là test case cho workflow, không phải approved product brief.

## Intake đã khóa

- Audience: quản lý trực tiếp triển khai AI tại các phòng ban vận hành của SME/khởi nghiệp/công ty gia đình.
- Department focus: hành chính, nhân sự, tài chính, quản lý và điều hành.
- Desired progress: chuyển workflow văn phòng thủ công sang ứng dụng AI Agent để nâng chất lượng và hiệu quả vận hành.
- Acquisition: organic từ Fanpage Kstudy.
- Funnel entry: đăng ký evergreen/on-demand webinar.
- Primary post-webinar conversion: đặt lịch tư vấn.
- Attribution: track riêng theo source/post/content angle/landing variant.
- Build scope sau khi product được duyệt: registration, thank-you, watch, booking, error states và tracking.

## Expected Product Truth behavior với Enter AI hiện tại

Nếu source course hiện tại tập trung chủ yếu vào AI tools, content/media, landing page, website, Marketing plan, Facebook MCP hoặc auto-posting, trong khi chưa chứng minh outcome/use case/capstone cho workflow vận hành, gate phải kết luận `MISMATCH` hoặc `PARTIAL` trọng yếu.

Expected action:

1. Tạo product gap report có citation đến lesson/session/capstone hiện tại.
2. Đề xuất tách track `Enter AI for Operations` hoặc thu hẹp audience/promise.
3. Đặt `waiting for product update`/`PRODUCT_GAP`.
4. Dừng trước audience research sâu, journey và landing brief public.
5. Không tự sửa course hiện tại và không tự gọi skill học liệu.

Đây là PASS của guardrail, không phải failure của skill.

## Resume acceptance

Khi có Syllabus/course source mới đã duyệt cho Operations:

- tạo snapshot reset: cập nhật source path/version/fingerprint, ghi revision reason, reset Product Truth/downstream về `PENDING`;
- giữ lại audience, organic Fanpage, evergreen webinar, booking CTA và track riêng;
- tạo snapshot evaluate: chạy lại Product Truth và đặt `PASS` hoặc `BLOCKED`;
- nếu `PASS`, tạo snapshot approve riêng sau user approval, lưu approval record khớp course/audience fingerprint;
- sau approval, tiếp tục research và đề xuất 3–5 journey;
- không hỏi lại các quyết định đã khóa trừ khi source mới làm chúng mâu thuẫn.

## Build acceptance sau approval

Funnel local/integration-ready phải có đủ 5 page state: registration, thank-you, watch, booking, booking success; store-first lead routing; no fake-live mechanics; internal event taxonomy và approval boundaries cho mọi external write/publish/deploy.
