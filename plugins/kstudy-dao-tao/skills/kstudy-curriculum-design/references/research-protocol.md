# Research protocol for curriculum design

## Research question template

Mỗi research run phải trả lời rõ:

1. Nghề này đang tạo ra những role/task nào?
2. Task nào lặp lại, khó, có giá trị và nên trở thành competency?
3. Doanh nghiệp yêu cầu tool, output, quality standard và seniority nào?
4. Chương trình tham chiếu đang dạy scope, sequence, modality và assessment ra sao?
5. Kstudy có khoảng trống hoặc advantage nào hợp lý?
6. Evidence nào đủ mạnh để thay đổi PLO, course map hoặc workload?

## Source hierarchy

Ưu tiên theo thứ tự:

1. Internal Kstudy baseline, learner evidence, mentor/teacher feedback và
   workbook hiện tại.
2. Official standards, official documentation, primary research và cơ quan nghề.
3. Employer JD public, job board và employer career pages.
4. Official competitor pages, public syllabus, course catalog và instructor page.
5. Coursera/Udemy/YouTube public metadata, outline, preview và review signals.
6. Secondary articles, social posts và discussion groups; chỉ dùng làm signal.

Mỗi source cần có: `source_id`, `source_type`, `title`, `author_or_org`,
`published_or_updated`, `url`, `accessed_at`, `access_status`, `evidence_level`,
`supports` và `limitations`.

## JD window

Ghi rõ:

- `as_of_date`.
- `window_months`: 3 hoặc 6.
- `window_start` và `window_end`.
- Platform và query.

Chỉ đưa JD vào tập chính nếu ngày đăng hoặc ngày cập nhật nằm trong cửa sổ. JD
không có ngày đáng tin cậy đưa vào `undated_signals`, không trộn vào frequency
count. Loại duplicate/repost theo URL, title, employer, location và nội dung
trùng; ghi phương pháp dedup.

## JD coding model

Chuẩn hóa mỗi JD thành:

```text
role → responsibility → task → tool/knowledge → work output → quality signal
```

Ghi cả negative evidence: tool không truy cập được, salary không công khai,
JD quá generic, yêu cầu mâu thuẫn hoặc mẫu thiếu seniority. Không suy ra mức
lương, nhu cầu toàn thị trường hoặc causal claim từ vài tin tuyển dụng.

## Competitor coding model

Tách:

- `program`: chương trình dài hạn/career path.
- `combo`: nhiều course hoặc module được bán theo path.
- `short_course`: course ngắn có thể đối chiếu một course Kstudy.

Mỗi record gồm: provider, audience, promise, public outline, outcomes nếu có,
duration, live/online, assessment, practice, capstone, support, tools,
access_status, source_id và confidence. Ghi `PUBLIC_DESCRIPTION_ONLY` nếu chỉ
thấy landing page.

Không dùng nội dung marketing như bằng chứng rằng provider thực sự dạy toàn bộ
outline. Không mua course, bypass login/paywall, scrape hàng loạt hoặc sao chép
tài liệu có bản quyền.

## Evidence status

- `CONFIRMED`: source trực tiếp, ngày/URL rõ và claim được hỗ trợ.
- `INFERRED`: pattern hoặc suy luận từ nhiều source; phải nêu logic.
- `PROPOSED`: quyết định thiết kế của Kstudy; cần approval nếu ảnh hưởng scope.
- `UNKNOWN`: chưa đủ evidence.
- `RESEARCH_GAP`: đã tìm nhưng không tiếp cận được hoặc evidence không đủ.

Khi web/browser/login capability không khả dụng, ghi URL, trạng thái và gap; không
điền phần nội dung bên trong bằng trí nhớ.
