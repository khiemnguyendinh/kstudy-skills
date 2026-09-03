# Research, audience và message evidence

## Nguyên tắc

Landing page theo audience không chỉ thay danh xưng. Phải thay problem hierarchy, language, proof, mechanism, objection, use case, CTA friction và post-conversion path.

## Research brief

Trước khi research, ghi:

- quyết định cần hỗ trợ;
- câu hỏi cụ thể;
- audience/source/market;
- freshness cần thiết;
- nguồn ưu tiên;
- điều gì có thể làm thay đổi funnel;
- điểm dừng research.

## Source hierarchy

Ưu tiên theo mức gần quyết định mua:

1. Approved course materials và Kstudy first-party evidence.
2. Sales calls, webinar questions, support logs, learner feedback đã xác minh.
3. Analytics/Search Console/ads data có segment rõ.
4. Organic comments/search/query/community behavior có thể truy nguồn.
5. Official research, platform docs và primary sources.
6. Competitor public pages và secondary sources để tạo hypothesis, không dùng làm proof cho Kstudy.

Ghi ngày truy cập và giới hạn của source. Không biến benchmark thành số liệu Kstudy.

## Audience model

Tối thiểu mô tả:

- role, authority, buying committee và người trực tiếp triển khai;
- company stage/size chỉ khi có evidence hoặc ghi giả định;
- department, workflow, job-to-be-done và trigger;
- current workaround, cost/risk, desired progress;
- AI maturity, tool access, security/compliance concern;
- objection: time, complexity, trust, implementation, budget, internal adoption;
- online behavior: query, page/group/channel, format, engagement pattern;
- moments of receptivity và điểm chạm;
- anti-persona và qualification signal.

## Organic continuity

Mỗi entry asset cần mapping:

| Field | Ví dụ cấu trúc |
|---|---|
| `source` | fanpage_kstudy |
| `post_id` | first-party content ID |
| `content_angle` | workflow bottleneck / manager story / demo |
| `content_format` | post / short video / carousel / live recap |
| `awareness` | problem-aware / solution-aware |
| `landing_variant` | matching hero and proof path |

Không dùng PII. Giữ UTM hoặc first-party attribution an toàn. Hero phải trả lời đúng lời hứa của content dẫn vào.

## Message architecture

Tách 6 lớp:

1. Problem truth: điều audience đang gặp, diễn đạt bằng ngôn ngữ có source.
2. Desired progress: trạng thái công việc tốt hơn, không phóng đại outcome.
3. Mechanism: cách khóa học tạo chuyển đổi năng lực.
4. Proof: curriculum, artifact, demo, mentor, process hoặc verified outcome.
5. Objection handling: ai phù hợp/không phù hợp, prerequisite, time, tool, support.
6. CTA: bước tiếp theo có friction tương xứng awareness.

## Claims ledger

Status hợp lệ:

- `VERIFIED`: có source/evidence đủ dùng trong public copy.
- `INFERRED`: suy luận từ evidence gián tiếp; không được phát hành như fact.
- `PROPOSED`: định hướng copy, chưa được phát hành như fact.
- `UNKNOWN`: thiếu dữ liệu.
- `REJECTED`: không dùng.

Evidence type có thể là `COURSE_SOURCE`, `FIRST_PARTY_DATA`, `APPROVED_POLICY`, `DEMO`, `INSTRUCTOR_PROFILE`, `EXTERNAL_CONTEXT`. Claim kết quả học viên phải là first-party verified; curriculum chỉ chứng minh nội dung được dạy, không chứng minh kết quả của mọi học viên.

## Research ethics

- Không scrape nội dung private/paid hoặc thu thập PII không cần thiết.
- Không sao chép voice/copy của đối thủ.
- Không suy ra persona từ stereotype.
- Không gọi correlation là causation.
- Không dùng comment đơn lẻ làm market fact; dùng làm hypothesis và ghi limitation.
