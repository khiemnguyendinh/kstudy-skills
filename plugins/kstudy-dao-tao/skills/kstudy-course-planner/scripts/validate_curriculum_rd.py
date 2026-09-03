#!/usr/bin/env python3
"""Validate the minimal structural contract for curriculum-rd.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MODES = {"NEW_COURSE", "UPDATE_COURSE", "AUDIT_ONLY"}
RESEARCH_LEVELS = {"LIGHT", "STANDARD", "DEEP"}
DESIGN_DEPTHS = {"LITE", "STANDARD", "FULL"}
STATUSES = {"DRAFT", "PENDING_APPROVAL", "READY_FOR_SYLLABUS", "BLOCKED"}
APPROVALS = {"PROPOSED", "APPROVED", "REJECTED", "DEFERRED", "NEEDS_INPUT", "SUPERSEDED"}
SOURCE_STATUS = {"PUBLIC", "LOGIN_REQUIRED", "PAYWALL", "USER_PROVIDED", "BROKEN", "UNKNOWN"}


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    required = {"schema_version", "planner_mode", "research_level", "status", "course", "research", "handoff"}
    missing = sorted(required - data.keys())
    if missing:
        errors.append("missing top-level keys: " + ", ".join(missing))
    if data.get("planner_mode") not in MODES:
        errors.append("planner_mode must be NEW_COURSE, UPDATE_COURSE or AUDIT_ONLY")
    if data.get("research_level") not in RESEARCH_LEVELS:
        errors.append("research_level must be LIGHT, STANDARD or DEEP")
    if data.get("design_depth") is not None and data.get("design_depth") not in DESIGN_DEPTHS:
        errors.append("design_depth must be LITE, STANDARD or FULL")
    if data.get("status") not in STATUSES:
        errors.append("status is invalid")
    if not isinstance(data.get("course"), dict):
        errors.append("course must be an object")
    if not isinstance(data.get("research"), dict):
        errors.append("research must be an object")
    if not isinstance(data.get("handoff"), dict):
        errors.append("handoff must be an object")

    traceability = data.get("traceability")
    if traceability is not None and not isinstance(traceability, dict):
        errors.append("traceability must be an object when present")

    research = data.get("research", {})
    sources = research.get("sources", [])
    if not isinstance(sources, list):
        errors.append("research.sources must be an array")
    else:
        seen: set[str] = set()
        for i, source in enumerate(sources):
            if not isinstance(source, dict):
                errors.append(f"research.sources[{i}] must be an object")
                continue
            sid = source.get("source_id")
            if not sid or sid in seen:
                errors.append(f"research.sources[{i}] needs a unique source_id")
            if sid:
                seen.add(sid)
            for key in ("source_type", "title", "access_status", "evidence_level", "citation"):
                if not source.get(key):
                    errors.append(f"research.sources[{i}] missing {key}")
            if source.get("access_status") not in SOURCE_STATUS:
                errors.append(f"research.sources[{i}] has invalid access_status")
            if source.get("access_status") in {"PUBLIC", "LOGIN_REQUIRED", "PAYWALL", "BROKEN"} and not source.get("url"):
                errors.append(f"research.sources[{i}] needs url for web source")

    if data.get("planner_mode") == "UPDATE_COURSE" and not isinstance(data.get("update_audit"), list):
        errors.append("UPDATE_COURSE requires update_audit array")
    if isinstance(data.get("update_audit"), list):
        for i, item in enumerate(data["update_audit"]):
            if not isinstance(item, dict):
                errors.append(f"update_audit[{i}] must be an object")
                continue
            if item.get("approval_status") not in APPROVALS:
                errors.append(f"update_audit[{i}] has invalid approval_status")

    handoff = data.get("handoff", {})
    if handoff.get("status") == "READY_FOR_SYLLABUS":
        course = data.get("course", {})
        identity = course.get("identity", {}) if isinstance(course, dict) else {}
        for key in ("code", "title", "author"):
            value = identity.get(key, {}) if isinstance(identity, dict) else {}
            if not isinstance(value, dict) or value.get("status") != "CONFIRMED" or not value.get("value"):
                errors.append(f"handoff ready requires confirmed course.identity.{key}")
        if not handoff.get("blocking_questions") == []:
            errors.append("handoff ready requires blocking_questions to be an empty array")
        for key in ("learner", "outcomes", "capstone", "prerequisites", "sessions", "lessons"):
            if not course.get(key):
                errors.append(f"handoff ready requires course.{key}")
        if not isinstance(traceability, dict):
            errors.append("handoff ready requires top-level traceability object")
        else:
            for key in ("job_task_ids", "competency_ids", "plo_ids", "clo_ids", "evidence_ids", "rubric_ids", "resource_ids", "mappings"):
                if not traceability.get(key):
                    errors.append(f"handoff ready requires traceability.{key}")
            if traceability.get("alignment_status") in {None, "NEEDS_INPUT"}:
                errors.append("handoff ready requires traceability.alignment_status")
            if traceability.get("approval_status") in {None, "NEEDS_INPUT"}:
                errors.append("handoff ready requires traceability.approval_status")
        if not course.get("assessment_blueprint"):
            errors.append("handoff ready requires course.assessment_blueprint")

    secret_pattern = re.compile(r"password|token|api[_-]?key|cookie|secret", re.I)
    def scan(value: object, path: str = "") -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if secret_pattern.search(str(key)):
                    errors.append(f"possible credential field: {path}.{key}")
                scan(child, f"{path}.{key}")
        elif isinstance(value, list):
            for i, child in enumerate(value):
                scan(child, f"{path}[{i}]")
    scan(data)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("json_path", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.json_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: cannot read JSON: {exc}")
        return 1
    if not isinstance(data, dict):
        print("FAIL: root must be an object")
        return 1
    errors = validate(data)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: curriculum-rd.json structure and handoff rules")
    return 0


if __name__ == "__main__":
    sys.exit(main())
