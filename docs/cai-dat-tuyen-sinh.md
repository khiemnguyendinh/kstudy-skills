# Cài skill Kstudy — Nhóm Tuyển sinh

Hướng dẫn cài skill Claude Code cho đội tuyển sinh: funnel khóa học, content, marketing, landing page, design system, chiến lược sản phẩm.

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
/plugin install kstudy-tuyen-sinh@kstudy-skills
```

Xong là có 3 skill sau. Không cần gõ tên skill — cứ mô tả đúng việc cần làm, Claude tự chọn skill phù hợp:

| Skill | Dùng khi nào |
|---|---|
| `kstudy-build-course-funnel` | Research, thiết kế, build và tối ưu funnel tuyển sinh cho 1 khóa học: landing page, webinar/VSL, content journey, tracking |
| `kstudy-design-system` | Tra token màu/chữ/logo, ảnh thật, UI kit thương hiệu Kstudy khi làm landing page, ấn phẩm marketing |
| `kstudy-edu-product-strategy` | Xây chiến lược sản phẩm giáo dục, phân loại portfolio khóa học, mô hình doanh thu/lợi nhuận |

## 3. Cập nhật khi có skill mới

```
/plugin marketplace update kstudy-skills
```

Chạy lệnh này định kỳ để lấy skill mới hoặc bản sửa lỗi — không cần add lại marketplace.

## 4. Gỡ cài (nếu cần)

```
/plugin uninstall kstudy-tuyen-sinh@kstudy-skills
```

## Hỗ trợ

Lỗi khi cài hoặc skill chạy sai → báo anh Khiêm.
