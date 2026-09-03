#!/usr/bin/env python3
"""Create the single-file Course Planner draft after the user has approved the target folder."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path, help="Course Planner folder")
    parser.add_argument("--mode", choices=["NEW_COURSE", "UPDATE_COURSE", "AUDIT_ONLY"], default="NEW_COURSE")
    parser.add_argument("--research-level", choices=["LIGHT", "STANDARD", "DEEP"], default="STANDARD")
    parser.add_argument("--design-depth", choices=["LITE", "STANDARD", "FULL"], default="STANDARD")
    args = parser.parse_args()

    args.target.mkdir(parents=True, exist_ok=True)
    output = args.target / "curriculum-rd.json"
    if output.exists():
        raise SystemExit(f"Refusing to overwrite existing file: {output}")
    data = {
        "schema_version": "1.0",
        "planner_mode": args.mode,
        "research_level": args.research_level,
        "design_depth": args.design_depth,
        "status": "DRAFT",
        "course": {
            "identity": {
                "code": {"value": None, "status": "MISSING"},
                "title": {"value": None, "status": "MISSING"},
                "author": {"value": None, "status": "MISSING"},
                "color": {"value": None, "status": "MISSING"},
                "logo": {"value": None, "status": "MISSING"}
            },
            "learner": None,
            "outcomes": [],
            "capstone": None,
            "prerequisites": None,
            "sessions": [],
            "lessons": [],
            "assessment_blueprint": []
        },
        "research": {"brief": [], "findings": [], "sources": [], "gaps": [], "recommendations": []},
        "traceability": {
            "job_task_ids": [],
            "competency_ids": [],
            "plo_ids": [],
            "clo_ids": [],
            "evidence_ids": [],
            "rubric_ids": [],
            "resource_ids": [],
            "mappings": [],
            "alignment_status": "NEEDS_INPUT",
            "approval_status": "NEEDS_INPUT",
            "gaps": ["Import job_task_ids, competency_ids and plo_ids from Curriculum Design."]
        },
        "update_audit": [] if args.mode == "UPDATE_COURSE" else None,
        "handoff": {
            "target_skill": "kstudy-syllabus-creator",
            "status": "BLOCKED",
            "blocking_questions": ["Confirm course identity, learner, prerequisites, outcomes and capstone."],
            "assumptions": []
        }
    }
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
