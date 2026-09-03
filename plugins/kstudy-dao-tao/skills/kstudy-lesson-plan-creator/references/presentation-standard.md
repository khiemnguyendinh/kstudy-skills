# Chuẩn trình bày văn bản Kstudy (docx)

Nguồn chân lý là `scripts/kstudy_docx_style.py` — mọi file .docx PHẢI sinh qua script để nhất quán với syllabus. Không tự gõ tay docx.

## Branding cố định
- Font: **Google Sans Flex** (đặt cho ascii/hAnsi/cs/eastAsia). Máy convert thiếu font sẽ tự fallback sang sans có sẵn khi xuất PDF — không lỗi.
- Màu: navy **#1D237D** (tiêu đề lớn, chữ tô đậm, nền header bảng), blue **#247DF9** (Heading 1), grey **#6B7280** (chú thích, header/footer phụ).
- Header: bảng 2 cột không viền — logo màu (`assets/kstudy-logo-full.png`) bên trái, dòng "MÃ · Buổi N — <nhãn>" bên phải (grey 9pt).
- Footer: căn giữa, "Kstudy Academy .,jsc  -  www.kstudy.edu.vn" (grey 9pt).
- Lề: trên/dưới 0.8 inch, trái/phải 0.9 inch.

## Phân cấp
- Normal 10.5pt. Heading 1 = 13.5pt blue (mục lớn "1.", "2."...). Heading 2 = 12.5pt navy (tiêu đề minh họa/demo). Heading 3 = 10.5pt navy (nhãn phụ).
- Khối tiêu đề đầu trang: dòng "kicker" navy 13pt + tên buổi navy 19pt + phụ đề grey italic 11pt, tất cả căn giữa.
- Cuối tài liệu Lesson Plan: khối ký "Chủ trì biên soạn" + tên tác giả, căn phải.

## Bảng
- Style "Table Grid", cell margin nhẹ, độ rộng cột cố định (fixed layout).
- Hàng tiêu đề: nền navy, chữ trắng in đậm 10.5pt.

## Bullet & đánh số
- Bullet cấp 1: ký hiệu ● màu navy; cấp 2: – màu grey; thụt lề treo.
- Danh sách các bước trong minh họa: đánh số "1." navy đậm, mỗi minh họa đánh số lại từ 1.
