# Cài skill Kstudy — Nhóm Đào tạo

Hướng dẫn cài skill cho đội đào tạo: curriculum, syllabus, lesson plan, slide, tốt nghiệp. Dùng được trên **Claude Code, ChatGPT Work (Codex) và Antigravity** — cả 3 công cụ đọc chung định dạng `SKILL.md`, nên 1 bộ skill dùng chung được cho cả 3, chỉ khác thư mục cài.

## Cách 1 — Copy-paste prompt (khuyên dùng, chạy được cả 3 công cụ)

Mở Claude Code / Codex CLI / Antigravity, dán nguyên văn prompt dưới đây rồi Enter. Agent tự nhận diện đang chạy trên công cụ nào và cài đúng chỗ:

```
Bạn đang chạy trong Claude Code, Codex CLI (ChatGPT Work), hoặc Antigravity — tự xác định bạn là công cụ nào rồi làm các bước sau bằng shell:

1. Nếu chưa có thư mục ~/.kstudy/kstudy-skills, chạy:
   git clone https://github.com/khiemnguyendinh/kstudy-skills.git ~/.kstudy/kstudy-skills
   Nếu đã có rồi, chạy:
   git -C ~/.kstudy/kstudy-skills pull

2. Copy toàn bộ thư mục con trong ~/.kstudy/kstudy-skills/plugins/kstudy-dao-tao/skills/ vào đúng thư mục skill cá nhân của bạn (tạo thư mục nếu chưa có, ghi đè nếu đã tồn tại):
   - Claude Code: ~/.claude/skills/
   - Codex CLI: ~/.agents/skills/
   - Antigravity: ~/.gemini/config/skills/

3. Liệt kê tên các skill vừa copy để xác nhận xong.
```

Cài xong, mở phiên làm việc mới (đóng mở lại Claude Code / Codex / Antigravity) để skill hiện ra.

**Cập nhật khi có skill mới:** dán lại đúng prompt trên — bước 1 tự `pull` bản mới, bước 2 tự ghi đè.

## Cách 2 — Native qua Claude Code plugin (chỉ Claude Code)

```
/plugin marketplace add khiemnguyendinh/kstudy-skills
```

```
/plugin install kstudy-dao-tao@kstudy-skills
```

Cập nhật: `/plugin marketplace update kstudy-skills`
Gỡ cài: `/plugin uninstall kstudy-dao-tao@kstudy-skills`

## Danh sách skill trong nhóm

Không cần gõ tên skill — cứ mô tả đúng việc cần làm, agent tự chọn skill phù hợp:

| Skill | Dùng khi nào |
|---|---|
| `kstudy-curriculum-design` | Thiết kế khung chương trình đào tạo cấp ngành/program mới, benchmark đối thủ, xác lập chuẩn đầu ra (PLO) |
| `kstudy-course-planner` | Lên kế hoạch/khung nội dung 1 course cụ thể, trước khi viết syllabus |
| `kstudy-syllabus-creator` | Tạo đề cương khóa học (syllabus) từ khung chương trình đã duyệt |
| `kstudy-lesson-plan-creator` | Soạn giáo án, slide-outline, video-outline cho từng buổi học từ syllabus đã duyệt |
| `kstudy-slide-design` | Thiết kế slide bài giảng HTML chuẩn brand Kstudy, xuất PDF |
| `kstudy-tot-nghiep` | Soạn đề tài/báo cáo tốt nghiệp, đề cương, rubric cho học viên |

## Gỡ cài thủ công (Codex / Antigravity)

Xóa đúng thư mục skill trong thư mục cá nhân tương ứng, ví dụ Codex:

```bash
rm -rf ~/.agents/skills/kstudy-syllabus-creator
```

## Hỗ trợ

Lỗi khi cài hoặc skill chạy sai → báo anh Khiêm.
