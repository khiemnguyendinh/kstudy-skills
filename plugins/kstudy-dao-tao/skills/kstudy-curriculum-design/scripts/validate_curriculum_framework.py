#!/usr/bin/env python3
"""Validate the structural contract of a Kstudy curriculum-design JSON file."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = (
    "schema_version",
    "design_mode",
    "research_level",
    "status",
    "project_brief",
    "occupation_analysis",
    "competency_architecture",
    "program_outcomes",
    "capstone",
    "curriculum_map",
    "workload",
    "traceability",
    "research",
    "quality_review",
    "handoff",
)

HOUR_FIELDS = (
    "direct_live_hours",
    "elearning_hours",
    "self_study_hours",
    "practice_project_hours",
    "assessment_feedback_hours",
    "mentor_coaching_hours",
)

DESIGN_DEPTHS = {"LITE", "STANDARD", "FULL"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def object_or_empty(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def unique_ids(items: Any, key: str, label: str, errors: list[str]) -> set[str]:
    if not isinstance(items, list):
        fail(errors, f"{label} must be an array")
        return set()
    ids: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict) or not isinstance(item.get(key), str) or not item[key].strip():
            fail(errors, f"{label}[{index}] missing non-empty {key}")
            continue
        if item[key] in ids:
            fail(errors, f"duplicate {key}: {item[key]}")
        ids.add(item[key])
    return ids


def hours_from(value: Any, label: str, errors: list[str]) -> float | None:
    if not isinstance(value, dict):
        fail(errors, f"{label} must be an object")
        return None
    total = 0.0
    for field in HOUR_FIELDS:
        current = value.get(field)
        if not number(current) or current < 0:
            fail(errors, f"{label}.{field} must be a non-negative number")
        else:
            total += float(current)
    reported = value.get("total_hours")
    if not number(reported) or reported < 0:
        fail(errors, f"{label}.total_hours must be a non-negative number")
    elif not math.isclose(float(reported), total, abs_tol=0.01):
        fail(errors, f"{label}.total_hours={reported} does not equal component sum={total:.2f}")
    return total


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_curriculum_framework.py <curriculum-design.json>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"FAIL: file not found: {path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"FAIL: invalid JSON: {exc}", file=sys.stderr)
        return 1

    if not isinstance(data, dict):
        print("FAIL: top-level JSON must be an object", file=sys.stderr)
        return 1

    for field in REQUIRED_TOP_LEVEL:
        if field not in data:
            fail(errors, f"missing top-level field: {field}")

    if data.get("design_depth") is not None and data.get("design_depth") not in DESIGN_DEPTHS:
        fail(errors, "design_depth must be LITE, STANDARD or FULL")

    occupation_analysis = object_or_empty(data.get("occupation_analysis"))
    competency_architecture = object_or_empty(data.get("competency_architecture"))
    workload = object_or_empty(data.get("workload"))
    traceability = object_or_empty(data.get("traceability"))

    plos = unique_ids(data.get("program_outcomes"), "plo_id", "program_outcomes", errors)
    courses = data.get("curriculum_map")
    course_ids = unique_ids(courses, "course_id", "curriculum_map", errors)
    tasks = unique_ids(occupation_analysis.get("tasks"), "task_id", "tasks", errors)
    competencies = unique_ids(
        competency_architecture.get("competencies"),
        "competency_id",
        "competencies",
        errors,
    )

    course_totals = workload.get("course_totals")
    if not isinstance(course_totals, list):
        fail(errors, "workload.course_totals must be an array")
        course_totals = []
    total_hours = 0.0
    total_course_ids: set[str] = set()
    for index, record in enumerate(course_totals):
        if not isinstance(record, dict) or not isinstance(record.get("course_id"), str):
            fail(errors, f"workload.course_totals[{index}] missing course_id")
            continue
        total_course_ids.add(record["course_id"])
        current = hours_from(record, f"workload.course_totals[{index}]", errors)
        if current is not None:
            total_hours += current
    if course_ids and total_course_ids != course_ids:
        fail(errors, "workload.course_totals course_ids do not match curriculum_map course_ids")

    program_totals = workload.get("program_totals")
    if isinstance(program_totals, dict):
        reported = hours_from(program_totals, "workload.program_totals", errors)
        if reported is not None and not math.isclose(reported, total_hours, abs_tol=0.01):
            fail(errors, f"program total={reported:.2f} does not equal course total sum={total_hours:.2f}")
    else:
        fail(errors, "workload.program_totals must be an object")

    links = traceability.get("links")
    if not isinstance(links, list):
        fail(errors, "traceability.links must be an array")
        links = []
    linked_plos: set[str] = set()
    for index, link in enumerate(links):
        if not isinstance(link, dict):
            fail(errors, f"traceability.links[{index}] must be an object")
            continue
        for field in ("task_id", "competency_id", "plo_id", "course_id"):
            if not isinstance(link.get(field), str) or not link[field].strip():
                fail(errors, f"traceability.links[{index}] missing {field}")
        if isinstance(link.get("task_id"), str) and link["task_id"] not in tasks:
            fail(errors, f"traceability link references unknown task_id: {link['task_id']}")
        if isinstance(link.get("competency_id"), str) and link["competency_id"] not in competencies:
            fail(errors, f"traceability link references unknown competency_id: {link['competency_id']}")
        if isinstance(link.get("plo_id"), str):
            linked_plos.add(link["plo_id"])
            if link["plo_id"] not in plos:
                fail(errors, f"traceability link references unknown plo_id: {link['plo_id']}")
        if isinstance(link.get("course_id"), str) and link["course_id"] not in course_ids:
            fail(errors, f"traceability link references unknown course_id: {link['course_id']}")

    orphan_plos = traceability.get("orphan_plos", [])
    if isinstance(orphan_plos, list):
        undeclared = plos - linked_plos - set(str(item) for item in orphan_plos)
        if undeclared:
            fail(errors, f"PLOs neither linked nor declared orphan: {sorted(undeclared)}")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS: {path}")
    print(f"- PLOs: {len(plos)}")
    print(f"- Courses: {len(course_ids)}")
    print(f"- Program hours: {total_hours:.2f}")
    print(f"- Traceability links: {len(links)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
