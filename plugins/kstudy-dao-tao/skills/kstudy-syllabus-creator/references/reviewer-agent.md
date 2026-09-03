# Review phản biện độc lập (critic)

Người soạn (cùng 1 model) dễ "yêu con mình" → bỏ sót lỗi. Trước khi trình user bản cuối, chạy **1 phản biện độc lập** để soi bằng con mắt mới.

## Khi nào
- Bắt buộc trước lần trình cuối cho khóa quan trọng / capstone nặng / chương trình đào tạo.
- Nên chạy ít nhất 1 lần mỗi khóa; có thể mỗi vòng review nếu sửa nhiều.

## Cách chạy
- **Có subagent** (Task tool): spawn 1 general-purpose agent với prompt critic dưới; đưa nó đường dẫn `course.json` + file `.html`/`.docx` đã build + `pedagogy.md`. Người soạn KHÔNG gợi ý đáp án — để critic tự soi.
- **Không có subagent:** tự đọc lại bản nháp đúng theo prompt dưới, "đội mũ phản biện" (kém khách quan hơn nhưng vẫn bắt được nhiều lỗi).

## Prompt critic (copy nguyên, dán cho agent)
```
Bạn là PHẢN BIỆN giáo trình độc lập của Kstudy — KHÔNG phải người soạn. Nhiệm vụ: tìm lỗi, không khen.
Đọc: course.json + syllabus (.html/.docx) + pedagogy.md. Chấm theo scorecard 6 tiêu chí
(1 Alignment, 2 Bloom/scaffolding, 3 Lean AI, 4 Phủ tài nguyên + sạch [CHỜ], 5 Radar/skill_tag, 6 Rubric).
MỖI tiêu chí: Đạt / Một phần / Chưa + bằng chứng cụ thể (trích đúng bài/field) + 1 fix đề xuất.
Soi sâu các lỗi hay gặp:
- Mục tiêu "mồ côi" (nêu nhưng không dạy hoặc không chấm); gate đòi thứ chưa dạy.
- Động từ không đo được ("hiểu/biết/nắm"); độ khó KHÔNG tăng dần qua level (đi ngang).
- Bài mỏng (thiếu khái niệm/ví dụ/lỗi sai); tài nguyên thiếu hoặc mô tả rỗng.
- Rubric 3 mức không phân biệt rõ (đạt/khá/tốt na ná nhau); capstone không tổng hợp được các bài.
- ai_context/content rò rỉ persona/marker, hoặc vượt ngân sách token.
- skill_tag trong bài lệch 6 trục; radar không phủ hết outcome khóa.
- `prerequisites` thiếu hoặc quá chung chung (không nói rõ điều kiện kỹ năng/thiết bị/trình độ, hoặc thiếu mã môn tiên quyết khi có điều kiện dạng "đã hoàn thành môn khác").
- `kash` thiếu hoặc hời hợt: mục Kiến thức/Kỹ năng gắn sai/thiếu cấp Bloom, cấp Bloom không khớp scaffolding của khóa (vd mục capstone mà gắn "Nhớ"); Thái độ/Thói quen bị gắn nhầm cấp Bloom (không nên có); nội dung KASH không đúc kết được từ objectives/concepts/gate thật của các bài (nghe chung chung, có thể áp cho bất kỳ khóa nào).
Kết: TOP 3 vấn đề lớn nhất phải sửa + verdict: "ĐẠT để trình" hoặc "CHƯA, cần sửa".
Chỉ nêu vấn đề CÓ THẬT kèm dẫn chứng; không bịa, không chấm khống.
```

## Sau phản biện
- Sửa mọi điểm **Chưa / Một phần** + TOP 3 → build lại.
- Nếu verdict "CHƯA" → KHÔNG trình bản đó cho user; sửa rồi phản biện lại.
- Khi trình user, tóm tắt 1 đoạn: critic đã bắt gì, đã sửa gì (cho thấy chất lượng được kiểm độc lập).
