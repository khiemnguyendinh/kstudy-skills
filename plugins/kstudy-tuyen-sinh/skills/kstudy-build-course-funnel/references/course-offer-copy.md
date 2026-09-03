# Diễn giải khóa học theo ngôn ngữ khách hàng

## Mục tiêu

Biến học liệu đã duyệt thành nội dung landing page giúp khách hàng trả lời nhanh:

1. Khóa học giúp tôi xử lý việc gì?
2. Sau mỗi học phần tôi tự làm được gì?
3. Ai hướng dẫn và vì sao người đó phù hợp?
4. Những băn khoăn trước khi đăng ký được giải đáp thế nào?

Không biến landing page thành bản syllabus rút gọn. Không hạ chuẩn Product Truth để copy nghe hấp dẫn hơn.

## Nguồn và trạng thái

| Nội dung public | Nguồn ưu tiên | Khi thiếu dữ liệu |
|---|---|---|
| Việc học viên có thể làm | Course outcome, lesson outcome, activity, assignment, capstone | `NEEDS_INPUT` nếu không truy được về học liệu |
| Ứng dụng trong công việc | Use case đã duyệt, demo, first-party evidence | Ghi `PROPOSED`; không phát hành như fact |
| Quyền lợi, lịch, quyền truy cập, cộng đồng | Policy/offer hiện hành đã duyệt | Không suy đoán |
| Giảng viên, học vị, nơi làm việc, kinh nghiệm | Profile chính thức hoặc hồ sơ Kstudy đã xác minh | Không dùng credential chưa có nguồn |
| FAQ | Audience research + policy/course source | Trả lời `Chưa xác định` trong brief hoặc xin input |

Mỗi câu có tính fact/promise phải có `claim_id`. Mỗi module, instructor và FAQ phải có `source_refs`.

## 1. Cụm giá trị khóa học

Mở bằng một câu mô tả khóa học theo cấu trúc:

`Học cách [thực hiện nhóm việc] để [tạo kết quả công việc], phù hợp với [đối tượng/mức đầu vào].`

Sau đó dùng 4–7 bullet, ưu tiên theo thứ tự:

1. Năng lực có thể thực hiện sau khóa học.
2. Công việc hoặc tình huống thực tế có thể áp dụng.
3. Sản phẩm/đầu ra học viên tự tạo.
4. Hình thức hỗ trợ hoặc quyền lợi đã được xác minh.

Viết bullet theo công thức:

`[Động từ hành động] + [việc/sản phẩm cụ thể] + [bối cảnh hoặc tiêu chí cần thiết].`

Tốt:

- “Tóm tắt một bộ tài liệu dài thành bản ý chính để chuẩn bị họp.”
- “Thiết lập lịch chạy tự động cho một tác vụ lặp lại và biết cách dừng khi có lỗi.”

Tránh:

- “Nắm vững AI.”
- “Nâng cao tư duy.”
- “Làm chủ công nghệ đột phá.”

Một lợi ích trừu tượng chỉ được giữ khi đi kèm ví dụ hành động cụ thể ngay sau đó.

## 2. Nội dung từng học phần

Bao phủ toàn bộ học phần thuộc scope đã duyệt. Mỗi học phần dùng cấu trúc:

| Trường | Quy tắc |
|---|---|
| `module_id` | Giữ ID để trace về source; không nhất thiết hiển thị public |
| `customer_title` | Tên dễ hiểu, nói rõ nhóm việc hoặc kết quả chính |
| `can_do` | 1–4 câu bắt đầu bằng hành động học viên tự thực hiện được |
| `hands_on_output` | File, workflow, kế hoạch, báo cáo, nội dung hoặc thao tác hoàn chỉnh; nếu không có artifact, mô tả tác vụ hoàn thành |
| `source_refs` | Course/lesson/activity/assignment chứng minh nội dung |
| `claim_ids` | Claim dùng trong public copy |

Ưu tiên động từ quen thuộc: tạo, viết, soạn, cài đặt, kết nối, lên lịch, tóm tắt, trích xuất, kiểm tra, phân tích, chỉnh sửa, trình bày, vận hành, xử lý.

Chỉ giữ thuật ngữ chuyên ngành khi khách hàng cần biết để ra quyết định. Lần đầu xuất hiện phải giải thích bằng một cụm ngắn. Không dùng tên framework, taxonomy hoặc công nghệ nội bộ để thay cho việc học viên làm được.

Phân biệt:

- **Chủ đề được dạy**: “Prompt engineering cơ bản”.
- **Việc học viên làm được**: “Viết yêu cầu rõ để AI trả về email, bảng tóm tắt hoặc kế hoạch đúng cấu trúc mong muốn”.

Không hứa “làm được sau học phần” nếu lesson plan chỉ giới thiệu khái niệm mà không có hoạt động/evidence tương ứng.

## 3. Giảng viên

Tạo một block cho mỗi giảng viên:

- tên;
- vai trò trong khóa học hoặc học phần phụ trách;
- chức danh/credential liên quan trực tiếp;
- bio 60–120 từ, ưu tiên kinh nghiệm giúp dạy đúng nội dung;
- ảnh thật có owner/quyền sử dụng/alt text trong asset manifest;
- `source_refs` và `claim_ids`.

Đặt nội dung cạnh ảnh trên desktop, xếp ảnh trước bio trên mobile. Với nhiều giảng viên, làm rõ ai phụ trách nội dung nào; không ghép credential của nhiều người thành một claim chung.

Không viết tiểu sử dài, không liệt kê thành tích không liên quan và không sao chép profile từ nguồn ngoài nếu chưa được phép.

## 4. FAQ

Chọn tối thiểu 4 câu hỏi từ objection và câu hỏi sales/support có evidence. Ưu tiên:

- Tôi chưa có nền tảng có học được không?
- Khóa học phù hợp hoặc không phù hợp với ai?
- Mỗi tuần cần dành bao nhiêu thời gian?
- Cần tài khoản, thiết bị, phần mềm hoặc ngoại ngữ ở mức nào?
- Bỏ lỡ buổi học thì xử lý ra sao?
- Có bài tập, phản hồi, AI Mentor hoặc cộng đồng hỗ trợ thế nào?
- Sau khi đăng ký/thanh toán nhận quyền truy cập khi nào?

Chỉ dùng câu hỏi liên quan đến khóa học cụ thể. Mỗi câu trả lời:

1. trả lời thẳng trong câu đầu;
2. giải thích điều kiện/giới hạn;
3. nêu bước tiếp theo nếu người đọc cần xác nhận;
4. gắn `source_refs` và `claim_ids` cho fact/policy.

FAQ không phải nơi che giấu prerequisite, chi phí phát sinh, giới hạn công cụ hoặc điều kiện nhận quyền lợi.

## Kiểm tra ngôn ngữ dễ hiểu

Đọc lại bằng góc nhìn người chưa học chuyên ngành:

- Có hình dung được việc hoặc đầu ra cụ thể không?
- Có biết học phần nào tạo ra đầu ra đó không?
- Có thuật ngữ nào có thể thay bằng từ phổ thông?
- Câu có ngắn, một ý chính và chủ ngữ rõ không?
- Có claim nào vượt quá source?
- Có nhầm “được học” với “sẽ chắc chắn đạt kết quả” không?

Nếu một câu chỉ trả lời “học gì” mà chưa trả lời “làm được gì”, viết lại trước khi xin duyệt Brief.
