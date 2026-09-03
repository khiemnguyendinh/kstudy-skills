#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinh handoff_summary.md và ThamKhao/resources.index.json từ course.json đã duyệt.

Dùng:
  python scripts/build_handoff_outputs.py course.json .
  python scripts/build_handoff_outputs.py course.json . --allow-draft
"""
import argparse
import datetime as _dt
import json
import os
import re
import sys


def display_numbers(lessons):
    by_session = {}
    for lesson in lessons:
        by_session.setdefault(lesson.get("session_idx"), []).append(lesson)
    out = {}
    for session_idx, group in by_session.items():
        for idx, lesson in enumerate(sorted(group, key=lambda x: x.get("sort_order", 0)), 1):
            sort_order = lesson.get("sort_order")
            out[sort_order] = f"{session_idx}.{idx}" if session_idx is not None else str(sort_order)
    return out


def placeholder_count(obj):
    return json.dumps(obj, ensure_ascii=False).count("[CHỜ")


def prereq_text(course):
    pr = course.get("prerequisites") or {}
    desc = (pr.get("description") or "").strip()
    codes = [c for c in pr.get("required_courses", []) if c]
    if codes:
        tag = "Mã môn tiên quyết: " + ", ".join(codes) + "."
        return (desc + " " + tag).strip() if desc else tag
    return desc


def md_list(items):
    return "\n".join(f"- {item}" for item in items) if items else "- Chưa có"


def build_handoff(course):
    lessons = course.get("lessons", [])
    sessions = course.get("sessions", [])
    disp = display_numbers(lessons)
    lessons_by_session = {}
    for lesson in lessons:
        lessons_by_session.setdefault(lesson.get("session_idx"), []).append(lesson)

    lines = [
        f"# Handoff syllabus — {course.get('title', '')} ({course.get('code', '')})",
        "",
        "## 1. Trạng thái",
        f"- Version: {course.get('version', '')}",
        f"- Approved: {course.get('approved')}",
        f"- Approved date: {course.get('approved_date') or 'Chưa có'}",
        f"- Author: {course.get('author') or 'Chưa có'}",
        "",
        "## 2. Thông tin nền",
        f"- Mô tả: {course.get('description') or 'Chưa có'}",
        f"- Điều kiện tiên quyết: {prereq_text(course) or 'Chưa có'}",
        f"- AI context: {course.get('ai_context') or 'Chưa có'}",
        "",
        "## 3. Outcome / Capstone",
    ]

    final_assignments = [a for a in course.get("assignments", []) if a.get("is_final")]
    if final_assignments:
        for assignment in final_assignments:
            lines.append(f"- {assignment.get('title', '')}: {assignment.get('brief', '')}")
    else:
        artifacts = [l.get("capstone_artifact") for l in lessons if l.get("capstone_artifact")]
        lines.extend(f"- {item}" for item in artifacts[:5])
        if not artifacts:
            lines.append("- Chưa có")

    lines += ["", "## 4. KASH đã duyệt"]
    kash = course.get("kash") or {}
    for key, label in (
        ("knowledge", "Kiến thức"),
        ("skill", "Kỹ năng"),
        ("attitude", "Thái độ"),
        ("habit", "Thói quen"),
    ):
        lines.append(f"### {label}")
        items = kash.get(key) or []
        if not items:
            lines.append("- Chưa có")
            continue
        for item in items:
            if isinstance(item, dict):
                bloom = f" ({item.get('bloom')})" if item.get("bloom") else ""
                lines.append(f"- {item.get('item', '')}{bloom}")
            else:
                lines.append(f"- {item}")

    lines += ["", "## 5. Radar / skill_tags"]
    for axis in course.get("radar", []):
        lines.append(f"- {axis.get('label', axis.get('key', ''))}: {', '.join(axis.get('tags', []))}")
    if not course.get("radar"):
        lines.append("- Chưa có")

    lines += ["", "## 6. Map buổi học"]
    for session in sorted(sessions, key=lambda x: x.get("idx", 0)):
        idx = session.get("idx")
        covered = sorted(lessons_by_session.get(idx, []), key=lambda x: x.get("sort_order", 0))
        covered_txt = "; ".join(
            f"Bài {disp.get(l.get('sort_order'), l.get('sort_order'))}: {l.get('title', '')}"
            for l in covered
        ) or "Chưa map bài"
        lines.append(
            f"- Buổi {idx}: {session.get('summary', '')} | {session.get('duration_minutes', '')} phút | "
            f"{session.get('format_type', '')} | {covered_txt}"
        )

    lines += ["", "## 7. Changelog gần nhất"]
    changelog = course.get("changelog") or []
    for row in changelog[-5:]:
        lines.append(f"- v{row.get('version')} · {row.get('date')}: {row.get('summary')}")
    if not changelog:
        lines.append("- Chưa có")

    lines += ["", "## 8. Open items cần chú ý"]
    waits = placeholder_count(course)
    lines.append(f"- Số placeholder `[CHỜ...]`: {waits}")
    missing_links = []
    for lesson in lessons:
        for resource in lesson.get("resources", []):
            url = (resource.get("url") or "").strip()
            if not url or "[CHỜ" in url:
                missing_links.append(f"Bài {lesson.get('sort_order')}: {resource.get('title', 'Tài nguyên chưa tên')}")
    lines.append("- Link còn thiếu: " + (", ".join(missing_links) if missing_links else "Không phát hiện"))
    lines.append("- Ghi chú: Lesson Plan phải đọc file này trước khi hỏi lại thông tin nền.")

    return "\n".join(lines).rstrip() + "\n"


def resource_status(resource):
    url = (resource.get("url") or "").strip()
    desc = (resource.get("description") or "").strip()
    if not url or "[CHỜ" in url:
        return "needs_url"
    if not desc or "[CHỜ" in desc:
        return "needs_description"
    if not re.match(r"https?://", url):
        return "needs_url_check"
    return "listed_in_course"


def build_resources_index(course):
    items = []
    seq = 1
    for lesson in sorted(course.get("lessons", []), key=lambda x: x.get("sort_order", 0)):
        for resource in lesson.get("resources", []):
            items.append({
                "id": f"R{seq:03d}",
                "lesson_sort_order": lesson.get("sort_order"),
                "session_idx": lesson.get("session_idx"),
                "lesson_title": lesson.get("title", ""),
                "title": resource.get("title", ""),
                "type": resource.get("type", ""),
                "topic": resource.get("topic", ""),
                "description": resource.get("description", ""),
                "url": resource.get("url", ""),
                "source": f"course.json.lessons[{lesson.get('sort_order')}].resources",
                "verification_status": resource_status(resource),
                "notes": "",
            })
            seq += 1
    return {
        "schema_version": 1,
        "course_code": course.get("code", ""),
        "course_title": course.get("title", ""),
        "generated_from": "course.json",
        "generated_at": _dt.date.today().isoformat(),
        "resources": items,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("course_json")
    parser.add_argument("project_root", nargs="?", default=".")
    parser.add_argument("--allow-draft", action="store_true")
    args = parser.parse_args()

    with open(args.course_json, encoding="utf-8") as fh:
        course = json.load(fh)

    if course.get("approved") is not True and not args.allow_draft:
        print("course.json chưa approved=true. Chỉ sinh handoff chính thức sau khi syllabus được duyệt.")
        print("Nếu chỉ muốn xem trước, chạy thêm --allow-draft.")
        return 1

    root = os.path.abspath(args.project_root)
    thamkhao = os.path.join(root, "ThamKhao")
    os.makedirs(thamkhao, exist_ok=True)

    handoff_path = os.path.join(root, "handoff_summary.md")
    resources_path = os.path.join(thamkhao, "resources.index.json")

    with open(handoff_path, "w", encoding="utf-8") as fh:
        fh.write(build_handoff(course))
    with open(resources_path, "w", encoding="utf-8") as fh:
        json.dump(build_resources_index(course), fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    print("Đã tạo handoff:")
    print("  -", handoff_path)
    print("  -", resources_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
