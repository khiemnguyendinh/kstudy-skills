# Cài skill Kstudy — Nhóm Đào tạo

Hướng dẫn cài skill Claude Code cho đội đào tạo: curriculum, syllabus, lesson plan, slide, tốt nghiệp.

## 1. Điều kiện

- Đã cài Claude Code CLI. Chưa có thì cài:

  ```bash
  npm install -g @anthropic-ai/claude-code
  ```

  hoặc xem hướng dẫn tại [code.claude.com](https://code.claude.com).
- Đã đăng nhập Claude Code (gõ `claude` rồi làm theo hướng dẫn đăng nhập lần đầu).

## 2. Cài skill

Mở Claude Code, gõ lần lượt 2 lệnh:

```
/plugin marketplace add khiemnguyendinh/kstudy-skills
```

```
/plugin install kstudy-dao-tao@kstudy-skills
```

Xong là có 6 skill sau. Không cần gõ tên skill — cứ mô tả đúng việc cần làm, Claude tự chọn skill phù hợp:

| Skill | Dùng khi nào |
|---|---|
| `kstudy-curriculum-design` | Thiết kế khung chương trình đào tạo cấp ngành/program mới, benchmark đối thủ, xác lập chuẩn đầu ra (PLO) |
| `kstudy-course-planner` | Lên kế hoạch/khung nội dung 1 course cụ thể, trước khi viết syllabus |
| `kstudy-syllabus-creator` | Tạo đề cương khóa học (syllabus) từ khung chương trình đã duyệt |
| `kstudy-lesson-plan-creator` | Soạn giáo án, slide-outline, video-outline cho từng buổi học từ syllabus đã duyệt |
| `kstudy-slide-design` | Thiết kế slide bài giảng HTML chuẩn brand Kstudy, xuất PDF |
| `kstudy-tot-nghiep` | Soạn đề tài/báo cáo tốt nghiệp, đề cương, rubric cho học viên |

## 3. Cập nhật khi có skill mới

```
/plugin marketplace update kstudy-skills
```

Chạy lệnh này định kỳ để lấy skill mới hoặc bản sửa lỗi — không cần add lại marketplace.

## 4. Gỡ cài (nếu cần)

```
/plugin uninstall kstudy-dao-tao@kstudy-skills
```

## Hỗ trợ

Lỗi khi cài hoặc skill chạy sai → báo anh Khiêm.
