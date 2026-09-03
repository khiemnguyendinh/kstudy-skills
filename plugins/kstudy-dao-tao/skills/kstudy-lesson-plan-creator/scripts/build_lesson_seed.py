#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinh lesson_seed.json cho một buổi từ course.json đã duyệt.

Dùng:
  python scripts/build_lesson_seed.py course.json 1
  python scripts/build_lesson_seed.py course.json 1 02_LessonPlan/Buoi_1
"""
import argparse
import hashlib
import json
import os
import sys


def fingerprint(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:12]


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


def read_json_if_exists(path):
    if path and os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    return None


def lesson_snapshot(lesson, display_no):
    return {
        "sort_order": lesson.get("sort_order"),
        "display_no": display_no,
        "session_idx": lesson.get("session_idx"),
        "title": lesson.get("title", ""),
        "description": lesson.get("description", ""),
        "topic": lesson.get("topic", ""),
        "concepts": lesson.get("concepts", []),
        "objectives": lesson.get("objectives", ""),
        "main_content": lesson.get("main_content", ""),
        "lien_he": lesson.get("lien_he", ""),
        "mistakes": lesson.get("mistakes", []),
        "ai_application": lesson.get("ai_application", []),
        "gate": lesson.get("gate", ""),
        "capstone_artifact": lesson.get("capstone_artifact", ""),
        "rubric": lesson.get("rubric", {}),
        "skill_tags": lesson.get("skill_tags", []),
        "resources": lesson.get("resources", []),
    }


def resources_for_session(resources_index, session_idx, sort_orders):
    if not resources_index:
        return []
    selected = []
    for resource in resources_index.get("resources", []):
        if resource.get("session_idx") == session_idx or resource.get("lesson_sort_order") in sort_orders:
            selected.append(resource)
    return selected


def open_questions(course, selected_lessons, resources_from_index):
    questions = []
    if not selected_lessons:
        questions.append("Không có lesson nào có session_idx khớp buổi này.")
    if not any(l.get("gate") for l in selected_lessons):
        questions.append("Các bài trong buổi chưa có gate; cần sửa course.json qua syllabus skill.")
    weak_resources = [
        r.get("title") or r.get("id")
        for r in resources_from_index
        if str(r.get("verification_status", "")).startswith("needs_")
    ]
    if weak_resources:
        questions.append("Tài nguyên cần xác minh: " + ", ".join(weak_resources))
    if json.dumps(course, ensure_ascii=False).count("[CHỜ"):
        questions.append("course.json còn placeholder [CHỜ...]; không bịa phần thiếu khi soạn lesson.")
    return questions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("course_json")
    parser.add_argument("buoi", type=int)
    parser.add_argument("outdir", nargs="?")
    parser.add_argument("--resources-index")
    parser.add_argument("--allow-draft", action="store_true")
    args = parser.parse_args()

    course_path = os.path.abspath(args.course_json)
    with open(course_path, encoding="utf-8") as fh:
        course = json.load(fh)

    if course.get("approved") is not True and not args.allow_draft:
        print("course.json chưa approved=true — không sinh lesson_seed chính thức.")
        print("Nếu chỉ muốn xem thử, chạy thêm --allow-draft.")
        return 1

    root = os.path.dirname(course_path)
    outdir = args.outdir or os.path.join(root, "02_LessonPlan", f"Buoi_{args.buoi}")
    os.makedirs(outdir, exist_ok=True)

    resources_index_path = args.resources_index or os.path.join(root, "ThamKhao", "resources.index.json")
    resources_index = read_json_if_exists(resources_index_path)
    handoff_path = os.path.join(root, "handoff_summary.md")

    lessons = course.get("lessons", [])
    disp = display_numbers(lessons)
    selected = sorted(
        [lesson for lesson in lessons if lesson.get("session_idx") == args.buoi],
        key=lambda x: x.get("sort_order", 0),
    )
    sort_orders = {lesson.get("sort_order") for lesson in selected}
    session = next((s for s in course.get("sessions", []) if s.get("idx") == args.buoi), {})
    resources_selected = resources_for_session(resources_index, args.buoi, sort_orders)

    total_buoi = len(course.get("sessions", [])) or max([s.get("idx", 0) for s in course.get("sessions", [])] or [args.buoi])
    seed = {
        "schema_version": 1,
        "course_fingerprint": fingerprint(course_path),
        "course_version": course.get("version"),
        "code": course.get("code", ""),
        "course_title": course.get("title", ""),
        "author": course.get("author", ""),
        "buoi": args.buoi,
        "total_buoi": total_buoi,
        "session": {
            "idx": session.get("idx", args.buoi),
            "summary": session.get("summary", ""),
            "duration_minutes": session.get("duration_minutes", 90),
            "default_mode": session.get("default_mode", "hybrid"),
            "format_type": session.get("format_type", ""),
        },
        "covers": [lesson_snapshot(lesson, disp.get(lesson.get("sort_order"), str(lesson.get("sort_order")))) for lesson in selected],
        "course_kash": course.get("kash", {}),
        "session_gate": [lesson.get("gate", "") for lesson in selected if lesson.get("gate")],
        "resources_from_index": resources_selected,
        "source_notes": {
            "handoff_summary": "available" if os.path.exists(handoff_path) else "missing",
            "resources_index": "available" if resources_index else "missing",
        },
    }
    seed["open_questions"] = open_questions(course, selected, resources_selected)

    outpath = os.path.join(outdir, "lesson_seed.json")
    with open(outpath, "w", encoding="utf-8") as fh:
        json.dump(seed, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    print("Đã tạo lesson seed:")
    print("  -", outpath)
    if seed["open_questions"]:
        print("Open questions:")
        for item in seed["open_questions"]:
            print("  -", item)
    return 0


if __name__ == "__main__":
    sys.exit(main())
