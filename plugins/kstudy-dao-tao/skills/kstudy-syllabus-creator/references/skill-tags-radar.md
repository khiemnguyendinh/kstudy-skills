# skill_tag taxonomy + Radar Portfolio (6 trục)

## Vòng lặp cần khớp

1. Mentor gán `skill_tag` cho mỗi câu quiz nó ra.
2. Radar gom skill_tag theo 6 trục → vẽ năng lực học viên ở trang Portfolio.

Rủi ro: nếu mỗi bài không **khai báo sẵn** tag chuẩn, Mentor tự chế tag tự do (`brand`, `branding`, `thuong_hieu`...) → không khớp trục nào → radar trống/loạn. Vì vậy skill này định nghĩa tag **một lần**, gắn vào trục, và nhúng vào từng bài để Mentor copy đúng tag.

## Xây taxonomy (làm TRƯỚC khi viết bài)

**Bước 1 — Rút 12–24 tag canonical** từ chủ đề khóa. Mỗi tag là 1 **năng lực/kỹ năng cụ thể**, không phải chủ đề mơ hồ.
- snake_case, tiếng Việt-không-dấu hoặc English term chuẩn.
- Cụ thể & đo được: `positioning_statement` (tốt) > `positioning` (rộng) > `marketing` (vô dụng).
- Bám động từ năng lực: viết được / phân tích được / dựng được cái gì.

**Bước 2 — Gom vào ĐÚNG 6 trục.** Mỗi trục = 1 nhóm năng lực trọng yếu của môn. Cân bằng: mỗi trục 2–5 tag, không để 1 trục 1 tag và 1 trục 10 tag. Mỗi trục có:
- `key`: snake_case ngắn (`positioning`, `do_luong`).
- Tên hiển thị: tiếng Việt, học viên đọc trên radar (`Định vị thương hiệu`).
- Skill tags: các tag thuộc trục.

**Bước 3 — Nhúng vào bài.** Mỗi bài chọn 2–4 tag liên quan vào field `skill_tags` (script tự nối thành dòng `skill_tags:` cuối `content`). Mọi tag dùng trong bài PHẢI tồn tại trong 6 trục (script QA chặn lỗi này).

## Nguyên tắc chọn 6 trục

- Phủ trọn outcome khóa: nhìn 6 tên trục là hình dung được "học xong giỏi 6 mảng gì".
- Trực giao: tránh 2 trục chồng nghĩa.
- Ổn định: trục là năng lực, không phải tên bài (bài có thể đổi, năng lực thì không).
- Mỗi level/bài nên chạm ≥1 trục; toàn khóa phủ cả 6.

## Ví dụ — khóa Brand-led Marketing Strategy (BRND01)

| Key | Tên hiển thị | Skill tags |
|---|---|---|
| `research_insight` | Nghiên cứu & Insight | `consumer_insight`, `market_research`, `segmentation` |
| `positioning` | Định vị thương hiệu | `positioning_statement`, `competitive_framing`, `value_proposition` |
| `brand_architecture` | Kiến trúc thương hiệu | `brand_pyramid`, `brand_hierarchy`, `naming` |
| `comms_planning` | Kế hoạch truyền thông | `comms_objective`, `channel_mix`, `big_idea` |
| `measurement` | Đo lường & Tối ưu | `brand_kpi`, `share_of_voice`, `brand_tracking` |
| `creative_strategy` | Chiến lược sáng tạo | `creative_brief`, `rtb`, `tone_of_voice` |

Bài 2 (Positioning) nhúng: `positioning_statement, competitive_framing, value_proposition` → tất cả thuộc trục `positioning` + `creative_strategy`. Khớp.

## Lỗi thường gặp

- Tag rộng (`marketing`, `brand`) → đổi thành năng lực cụ thể.
- >6 hoặc <6 trục → hệ yêu cầu đúng 6.
- Tag trong bài không có trong trục nào → thêm vào trục phù hợp hoặc đổi tag.
- Trục đặt theo tên bài thay vì năng lực → đổi sang năng lực bền vững.
