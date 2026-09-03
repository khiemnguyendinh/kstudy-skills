# Chuẩn sư phạm & làm giàu nội dung

Mục tiêu: nâng từ "đúng form" lên "giáo trình dạy được". Áp khi soạn `course.json` (bước 4) và khi tự review (bước 6).

## 1. Constructive alignment (nguyên tắc lõi)

Mỗi bài phải khớp 3 chân: **Mục tiêu ↔ Nội dung dạy ↔ Đánh giá (gate/capstone)**.

- Mỗi mục tiêu phải được DẠY (xuất hiện ở concepts/main_content) và được KIỂM TRA (gate hoặc capstone đo đúng mục tiêu đó).
- Không để mục tiêu "mồ côi" (nêu nhưng không dạy/không chấm). Không để gate đòi thứ chưa dạy.
- Tự kiểm: liệt kê mục tiêu của bài → đối chiếu từng cái với gate/capstone. Lệch là sửa.

## 2. Mục tiêu đo được (động từ Bloom)

Mở đầu mục tiêu bằng động từ quan sát/đo được, đúng cấp nhận thức. Tránh "hiểu / biết / nắm được" (không đo được).

| Cấp | Động từ (chọn dùng) |
|---|---|
| Nhớ | liệt kê, gọi tên, nhận diện, nhắc lại |
| Hiểu | giải thích, phân biệt, tóm tắt, ví dụ hóa |
| Áp dụng | áp dụng, dựng, triển khai, tính, sử dụng |
| Phân tích | phân tích, mổ xẻ, so sánh, đối chiếu, chẩn đoán |
| Đánh giá | đánh giá, phản biện, lựa chọn có lý do, kiểm định |
| Sáng tạo | thiết kế, xây dựng, đề xuất, sản xuất, tổng hợp |

Mỗi mục tiêu gắn 1 artifact/bằng chứng đo được.

**Liên hệ khung KASH (course-level, xem `course-schema.md` §`kash`):** khi đúc kết mục "Khung năng lực (KASH)" cho docx, chỉ nhóm **Kiến thức** (Knowledge) và **Kỹ năng** (Skill) gắn cấp Bloom — vì Bloom là thang nhận thức/kỹ năng. Nhóm **Thái độ** (Attitude) và **Thói quen** (Habit) thuộc miền cảm xúc/hành vi, không gắn Bloom. Cấp Bloom gán cho từng mục KASH nên khớp với vị trí mục đó trong mạch scaffolding của khóa (mục Kiến thức nền → Nhớ/Hiểu; mục Kỹ năng nâng cao/capstone → Đánh giá/Sáng tạo) — xem §3 bên dưới.

## 3. Scaffolding (độ khó tăng dần qua level)

Khóa đi từ cấp thấp → cao (đúng ZPD của AI Mentor):
- Level đầu: Nhớ/Hiểu — khái niệm nền.
- Level giữa: Áp dụng/Phân tích — làm trên ca thật.
- Level cuối/capstone: Đánh giá/Sáng tạo — tổng hợp, ra sản phẩm.

Mỗi bài kế thừa bài trước (ghi rõ "dùng kết quả bài N" ở `lien_he`/gate). Tránh nhảy bậc đột ngột hoặc các bài cùng một bậc nhận thức suốt khóa (đi ngang = không tiến bộ).

## 4. Rubric chấm — `rubric: {dat, kha, tot}`

Mỗi gate kèm rubric 3 mức để Mentor chấm `[ĐIỂM]` nhất quán và học viên biết kỳ vọng:
- **đạt** (qua level): tiêu chí tối thiểu.
- **khá**: đạt + làm đúng/đủ hơn.
- **tốt**: khá + chiều sâu / sáng tạo / áp dụng đúng ngữ cảnh thật.

Mỗi mức 1 dòng ngắn, bám đúng mục tiêu + artifact của bài. Generator nối gọn rubric vào mục "Bài thực hành gợi ý" của `content` (Đạt/Khá/Tốt) để Mentor chấm — **KHÔNG hiện rubric riêng trong docx syllabus** (ẩn khỏi bản đọc cho giảng viên/học viên, xem `course-schema.md` §Cấu trúc bài trong syllabus docx); rubric đầy đủ vẫn có trong `course.json`/sheet Lessons.

Ví dụ (bài positioning): đạt = statement đủ 4 thành phần; khá = + 2 POD có RTB; tốt = + phản biện với 1 đối thủ thật.

## 5. Làm giàu nội dung (khi syllabus mỏng)

Dấu hiệu mỏng: bài chỉ có tên + 1 dòng; thiếu khái niệm/ví dụ/bài tập; nội dung thật < ~80 từ. Giáo trình mỏng vào → mỏng ra, không dạy được.

Khi mỏng, **ĐỀ XUẤT bổ sung cho user duyệt** (đưa vào Intake report, mục "Đề xuất làm giàu"):
- Khái niệm lõi còn thiếu (theo chuẩn lĩnh vực).
- 1–2 ví dụ thực chiến gắn ngữ cảnh học viên.
- Lỗi sai / hiểu lầm phổ biến.
- 1 bài tập luyện đúng mục tiêu.
- Ứng dụng AI cho bài (nếu hợp).

Kỷ luật chống bịa: bám kiến thức chuẩn của lĩnh vực; **KHÔNG bịa số liệu/nguồn/URL/tên riêng**; đánh dấu rõ "đề xuất bổ sung"; chỉ đưa vào `course.json` **sau khi user OK**. Việc của skill là biên soạn có đề xuất, không phải chép lại cái khung.

### Quy trình đề xuất làm giàu (gắn vào bước intake + review)
1. Khi rà soát, chấm độ dày mỗi bài: đủ / mỏng / rất mỏng.
2. Với bài mỏng, soạn **danh sách đề xuất** theo 3 nhóm tối thiểu: khái niệm thiếu · ví dụ thực chiến · lỗi sai phổ biến (thêm bài tập/ứng dụng AI nếu hợp).
3. Trình user dạng chọn được: **[Nhận tất cả] / [Chọn từng mục] / [Bỏ qua]**. Ghi rõ cái nào là đề xuất.
4. Chỉ mục được user duyệt mới đưa vào `course.json` (concepts / main_content / mistakes / resources / ai_application). Cái bị từ chối thì bỏ.
