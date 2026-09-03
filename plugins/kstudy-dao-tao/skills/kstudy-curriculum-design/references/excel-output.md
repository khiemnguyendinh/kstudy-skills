# Excel output contract

## Mục tiêu

Workbook là bản vận hành và audit dễ đọc của `curriculum-design.json`, đồng
thời giữ cách nhìn quen thuộc của workbook `Khung chương trình Kstudy 2026_Digital
MKT ứng dụng AI & Automation.xlsx`.

Không dùng Excel làm nguồn sự thật thứ hai. Sửa nội dung ở JSON rồi generate lại
workbook; không sửa ngược thủ công mà không cập nhật JSON.

## Sheet bắt buộc

### `Khung chương trình YYYY`

Đây là sheet chính duy nhất cho người đọc và người lập kế hoạch course. Giữ các
trường quen thuộc:

`STT | Course ID | Tên cũ | Học phần | Giai đoạn | Môn điều kiện | Nội dung trọng tâm | PLO đóng góp | Sản phẩm đầu ra | workload | PIC | Trạng thái | Tham khảo`

Workload gồm trực tiếp/Zoom, e-learning, tự học, thực hành/dự án,
feedback, mentor và tổng giờ. Không đưa Học phí vào workbook mặc định vì không
phải input cần thiết cho `kstudy-course-planner`.

Metadata program, capstone và tổng giờ nằm ở phần đầu sheet; không tạo thêm sheet
`Tổng quan`.

### `Traceability & Evidence`

Đây là sheet audit duy nhất, gồm bốn section theo thứ tự: traceability matrix;
evidence/benchmark/JD signals; quality gates; handoff checklist. Chỉ đưa finding
và signal có giá trị quyết định, không dump toàn bộ source registry hoặc outline
đối thủ. Chi tiết đầy đủ vẫn nằm trong JSON.

## Format baseline

- Header fill xám nhạt `#EFEFEF`, chữ Calibri đậm, căn giữa, wrap text.
- Body có border mảnh nhẹ, chữ mô tả căn trái, số căn phải.
- Ẩn gridlines; freeze dòng header và các cột định danh quan trọng.
- Dùng filter/table cho vùng dữ liệu.
- Dùng formula cho tổng course/program; không hardcode derived total.
- Dùng format số `0.0` cho giờ và `#,##0` cho số lượng; không biến số thành text.
- Mở rộng cột trước khi tăng row height; kiểm tra không bị clip khi render.
- Giữ tối đa hai sheet; không sinh thêm sheet research/benchmark/quality riêng.

## Generator

Chạy script bằng Node.js và dependency `@oai/artifact-tool` từ
`load_workspace_dependencies`:

```text
node scripts/create_curriculum_workbook.mjs curriculum-design.json curriculum-design.xlsx
```

Sau khi export, inspect hai sheet, scan `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`,
`#N/A` và render cả hai sheet.
