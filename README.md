# Kstudy Claude Code Skills

Bộ skill Claude Code cho đội Kstudy. 2 nhóm:

- **kstudy-dao-tao** — course-planner, curriculum-design, syllabus-creator, lesson-plan-creator, slide-design, tot-nghiep
- **kstudy-tuyen-sinh** — build-course-funnel, design-system, edu-product-strategy

Skill đụng hạ tầng/production (Lovable, GitHub, SSH, Supabase...) nằm ở repo riêng private `kstudy-skills-noi-bo`, không nằm ở đây.

## Hướng dẫn cài theo nhóm

- [Nhóm Đào tạo](docs/cai-dat-dao-tao.md)
- [Nhóm Tuyển sinh](docs/cai-dat-tuyen-sinh.md)

## Cài lần đầu

```bash
/plugin marketplace add khiemnguyendinh/kstudy-skills
```

Rồi cài nhóm skill cần dùng:

```bash
/plugin install kstudy-dao-tao@kstudy-skills
/plugin install kstudy-tuyen-sinh@kstudy-skills
```

(Cài 1 hoặc cả 2 tuỳ team.)

## Cập nhật khi có skill mới

Mỗi lần repo có skill mới hoặc sửa skill cũ, chạy trong Claude Code:

```bash
/plugin marketplace update kstudy-skills
```

## Yêu cầu

Claude Code CLI đã cài (`npm install -g @anthropic-ai/claude-code` hoặc xem [code.claude.com](https://code.claude.com)).
