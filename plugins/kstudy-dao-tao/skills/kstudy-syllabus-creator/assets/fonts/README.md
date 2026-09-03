# Font nhúng cho PDF

PDF được sinh bằng LibreOffice (convert từ docx). Máy convert phải có font thì PDF mới đúng;
thiếu font → LibreOffice thay nhầm (vd ra serif) → "sai format".

## Mặc định (không cần làm gì)
Generator alias `Google Sans Flex` → các font sans có sẵn, phủ tiếng Việt: **Carlito → Liberation Sans → DejaVu Sans**.
PDF ra đúng (sans, đủ dấu), font được nhúng trong PDF nên hiển thị đúng trên mọi máy.

## Muốn PDF dùng ĐÚNG "Google Sans Flex"
Thả file font vào **một trong** các nơi sau (generator tự cài trước khi convert):
- thư mục này: `assets/fonts/` của skill, hoặc
- thư mục `fonts/` đặt cạnh `course.json`, hoặc
- đường dẫn khai trong `course.json`: `"fonts_dir": "/đường/dẫn/tới/fonts"`.

Chấp nhận `.ttf` / `.otf` / `.ttc`. Nên đủ 4 kiểu: Regular, Bold, Italic, BoldItalic
(để in đậm/nghiêng trong PDF đúng nét). Khi file có family đúng tên "Google Sans Flex",
fontconfig khớp tên và PDF dùng đúng font đó (bỏ qua fallback).

Lưu ý: nếu chia sẻ skill ra ngoài, chỉ nhúng font bạn có quyền phân phối. Roboto/Be Vietnam Pro
là phương án mã nguồn mở (OFL/Apache) thay thế gần giống Google Sans nếu cần.
