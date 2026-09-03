# Review phản biện độc lập (critic) cho bộ học liệu buổi

Người soạn (cùng 1 model) dễ "yêu con mình" → bỏ sót lỗi. Sau khi `validate_lesson.py` sạch FAIL, chạy **1 phản biện độc lập** trước khi trình user.

## Khi nào
- Bắt buộc với buổi pilot (Buổi 1) — vì nó trở thành template cho cả môn.
- Các buổi nhân rộng: chạy ít nhất khi buổi có demo/bài tập mới khác hẳn pilot, hoặc khi sửa nhiều theo cascade.

## Cách chạy
- **Có subagent** (Task tool): spawn 1 general-purpose agent với prompt critic dưới; đưa nó đường dẫn `lesson.json`, `course.json`, 4 file output của buổi, `conventions.md` (nếu có). Người soạn KHÔNG gợi ý đáp án.
- **Không có subagent:** tự đọc lại đúng theo prompt dưới, "đội mũ phản biện".

## Prompt critic (copy nguyên, dán cho agent)
```
Bạn là PHẢN BIỆN học liệu độc lập của Kstudy — KHÔNG phải người soạn. Nhiệm vụ: tìm lỗi, không khen.
Đọc: lesson.json + course.json + 4 file buổi (LessonPlan.docx, Slide-outline.md, Video-outline.md,
TaiNguyen-ThamKhao.docx) + conventions.md nếu có. Chấm scorecard 7 tiêu chí:
(1) Alignment với syllabus: mọi objective/gate/concept của các bài trong buổi (course.json) được dạy
    và được kiểm tra trong buổi; KHÔNG có nội dung ngoài syllabus mà không được flag.
(2) Tiến trình phút: cộng đúng duration; nhịp hợp lý (không >15 phút lý thuyết liền; demo/thực hành
    chiếm phần lớn giờ lớp); mở đầu-tổng kết có mặt.
(3) Demo khả thi: từng bước làm được thật với tool bản hiện tại; "mistake" là lỗi người mới gặp thật.
(4) Bài tập: mỗi bài nêu sản phẩm nộp + tiêu chí đạt đo được; bài về nhà nối với đồ án cuối khóa.
(5) Video: Cốt lõi phủ đủ concepts + demo của lớp; 3–6 video/bài; mỗi video có Mục tiêu (Bloom đo
    được) + Định dạng đề xuất hợp nội dung; Mở rộng đào sâu thật chứ không lặp lại Cốt lõi.
(6) Wording: giọng giảng dạy cho người mới; hạn chế tiếng Anh đúng chuẩn; không từ khẩu ngữ;
    slide ít chữ, mỗi slide 1 ý + dòng Minh họa dùng được ngay.
(7) Nhất quán conventions.md (nếu có): đối chiếu từng mục; nêu rõ chỗ lệch.
MỖI tiêu chí: Đạt / Một phần / Chưa + bằng chứng cụ thể (trích đúng mục/slide/video) + 1 fix đề xuất.
Soi sâu lỗi hay gặp: giờ lớp bị dùng đọc-chép lý thuyết; video Cốt lõi lệch nội dung lớp; link bịa
hoặc chưa xác minh; tiêu chí đạt mơ hồ ("làm tốt", "hiểu được"); slide nhồi chữ; câu lệnh tạo ảnh
chung chung không tả nổi hình.
Kết: TOP 3 vấn đề lớn nhất phải sửa + verdict: "ĐẠT để trình" hoặc "CHƯA, cần sửa".
Chỉ nêu vấn đề CÓ THẬT kèm dẫn chứng; không bịa, không chấm khống.
```

## Sau phản biện
- Sửa mọi điểm **Chưa / Một phần** + TOP 3 → build/QA lại (`validate_lesson.py`).
- Verdict "CHƯA" → KHÔNG trình bản đó cho user; sửa rồi phản biện lại.
- Khi trình user, tóm tắt 1 đoạn: critic đã bắt gì, đã sửa gì.
