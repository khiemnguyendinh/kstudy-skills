#!/usr/bin/env python3
"""Deterministic structural validators for Kstudy course funnel artifacts.

This script never calls the network and never claims to validate marketing truth.
It checks only parseability, required contracts, gate consistency, and blockers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable


PLACEHOLDER_RE = re.compile(r"\{\{[^{}]+\}\}|\b(?:TODO|TBD)\b|\[CHỜ[^\]]*\]", re.IGNORECASE)
CLAIM_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$", re.IGNORECASE)


@dataclass
class Issue:
    level: str
    code: str
    location: str
    message: str


class Report:
    def __init__(self, strict: bool = False) -> None:
        self.strict = strict
        self.issues: list[Issue] = []
        self.metadata: dict[str, Any] = {}

    def error(self, code: str, location: str, message: str) -> None:
        self.issues.append(Issue("ERROR", code, location, message))

    def warning(self, code: str, location: str, message: str) -> None:
        self.issues.append(Issue("WARNING", code, location, message))

    @property
    def errors(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.level == "ERROR"]

    @property
    def warnings(self) -> list[Issue]:
        return [issue for issue in self.issues if issue.level == "WARNING"]

    @property
    def valid(self) -> bool:
        return not self.errors and not (self.strict and self.warnings)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    return json.loads(read_text(path))


def has_placeholder(value: Any) -> bool:
    if isinstance(value, str):
        return bool(PLACEHOLDER_RE.search(value))
    if isinstance(value, list):
        return any(has_placeholder(item) for item in value)
    if isinstance(value, dict):
        return any(has_placeholder(key) or has_placeholder(item) for key, item in value.items())
    return False


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


AUDIENCE_FINGERPRINT_FIELDS = (
    "segment",
    "role",
    "department_or_use_case",
    "job_to_be_done",
    "desired_outcome",
    "ai_maturity",
    "anti_persona",
)


def audience_fingerprint(contract: dict[str, Any]) -> str:
    payload = {key: contract.get(key) for key in AUDIENCE_FINGERPRINT_FIELDS}
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def first_value(data: dict[str, Any], paths: Iterable[tuple[str, ...]]) -> Any:
    for path in paths:
        current: Any = data
        for key in path:
            if not isinstance(current, dict) or key not in current:
                current = None
                break
            current = current[key]
        if current not in (None, "", [], {}):
            return current
    return None


def placeholder_issue(report: Report, location: str, value: Any, allow: bool) -> None:
    if has_placeholder(value):
        if allow:
            report.warning("PLACEHOLDER", location, "Artifact still contains template placeholders.")
        else:
            report.error("PLACEHOLDER", location, "Resolve template placeholders before approval/build.")


def validate_course(path: Path, args: argparse.Namespace) -> Report:
    report = Report(args.strict)
    data = read_json(path)
    if not isinstance(data, dict):
        report.error("COURSE_ROOT", "$", "Course JSON root must be an object.")
        return report

    title = first_value(data, [("title",), ("course", "title"), ("course_name",)])
    description = first_value(data, [("description",), ("course", "description")])
    learning_structure = first_value(
        data,
        [("lessons",), ("sessions",), ("modules",), ("course", "lessons"), ("course", "sessions")],
    )
    audience = first_value(
        data,
        [("target_audience",), ("audience",), ("course", "target_audience"), ("course", "learner"), ("ai_context",)],
    )
    outcomes = first_value(
        data,
        [
            ("learning_outcomes",),
            ("outcomes",),
            ("course", "learning_outcomes"),
            ("course", "outcomes"),
            ("kash",),
        ],
    )
    capstone = first_value(
        data,
        [("capstone",), ("course", "capstone"), ("assessment_blueprint", "capstone")],
    )
    if capstone is None and isinstance(data.get("assignments"), list):
        capstone = next(
            (
                item
                for item in data["assignments"]
                if isinstance(item, dict)
                and (str(item.get("code", "")).upper() == "CAPSTONE" or item.get("is_final") is True)
            ),
            None,
        )

    if not nonempty_string(title):
        report.error("COURSE_TITLE", "title", "A non-empty course title is required.")
    if not nonempty_string(description):
        report.error("COURSE_DESCRIPTION", "description", "A non-empty course description is required.")
    if not isinstance(learning_structure, list) or not learning_structure:
        report.error("COURSE_STRUCTURE", "lessons/sessions/modules", "At least one lesson, session, or module is required.")
    if audience is None:
        report.warning("COURSE_AUDIENCE", "target_audience", "No explicit audience found; create an audience contract before Product Truth.")
    if outcomes is None:
        report.warning("COURSE_OUTCOMES", "learning_outcomes", "No explicit outcomes found; Product Truth requires manual traceability.")
    if capstone is None:
        report.warning("COURSE_CAPSTONE", "capstone", "No explicit capstone/evidence found; do not infer learner results.")
    if data.get("approved") is not True and first_value(data, [("status",), ("handoff", "status")]) not in {
        "APPROVED",
        "READY_FOR_FUNNEL",
    }:
        report.warning("COURSE_APPROVAL", "approved/status", "Course source is not explicitly approved for funnel work.")

    raw = path.read_bytes()
    report.metadata["sha256"] = hashlib.sha256(raw).hexdigest()
    report.metadata["title"] = title
    report.metadata["structure_items"] = len(learning_structure) if isinstance(learning_structure, list) else 0
    return report


MODE_VALUES = {"STRATEGY", "BUILD", "OPTIMIZE"}
STATUS_VALUES = {
    "INITIALIZED",
    "PRODUCT_REVIEW",
    "PRODUCT_GAP",
    "RESEARCH",
    "STRATEGY_REVIEW",
    "BRIEF_REVIEW",
    "READY_FOR_BUILD",
    "BUILDING",
    "BUILD_READY",
    "CONNECTED",
    "READY_FOR_QA",
    "READY_FOR_PUBLISH",
    "PUBLISHED",
    "COMPLETE",
    "BLOCKED",
}
GATE_ORDER = ["INPUT", "PRODUCT_TRUTH", "RESEARCH", "STRATEGY", "CLAIMS", "BRIEF", "BUILD", "QA", "PUBLISH"]
GATE_VALUES = {"PENDING", "PASS", "APPROVED", "BLOCKED", "FAIL", "SKIPPED"}
CONNECTOR_VALUES = {
    "UNVERIFIED",
    "AVAILABLE_READ_ONLY",
    "AVAILABLE_WRITE_PENDING_APPROVAL",
    "APPROVED_FOR_ACTION",
    "UNAVAILABLE",
}


def validate_state(path: Path, args: argparse.Namespace) -> Report:
    report = Report(args.strict)
    data = read_json(path)
    if not isinstance(data, dict):
        report.error("STATE_ROOT", "$", "Workflow state root must be an object.")
        return report

    for key in ("schema_version", "workflow_id", "mode", "status", "current_gate", "course_source", "audience_contract", "product_truth_approval", "gates"):
        if key not in data:
            report.error("STATE_REQUIRED", key, "Required state field is missing.")

    if data.get("schema_version") != "1.0":
        report.error("STATE_SCHEMA", "schema_version", "Expected schema_version 1.0.")
    if data.get("mode") not in MODE_VALUES:
        report.error("STATE_MODE", "mode", f"Expected one of {sorted(MODE_VALUES)}.")
    if data.get("status") not in STATUS_VALUES:
        report.error("STATE_STATUS", "status", f"Expected one of {sorted(STATUS_VALUES)}.")
    if data.get("current_gate") not in GATE_ORDER:
        report.error("STATE_CURRENT_GATE", "current_gate", f"Expected one of {GATE_ORDER}.")

    gates = data.get("gates")
    if not isinstance(gates, dict):
        report.error("STATE_GATES", "gates", "Gates must be an object.")
        gates = {}
    for gate in GATE_ORDER:
        value = gates.get(gate)
        if value is None:
            report.error("STATE_GATE_MISSING", f"gates.{gate}", "Required gate is missing.")
        elif value not in GATE_VALUES:
            report.error("STATE_GATE_VALUE", f"gates.{gate}", f"Expected one of {sorted(GATE_VALUES)}.")

    course_source = data.get("course_source") if isinstance(data.get("course_source"), dict) else {}
    audience_contract = data.get("audience_contract") if isinstance(data.get("audience_contract"), dict) else {}
    if gates.get("INPUT") in {"PASS", "APPROVED"}:
        for key in ("path", "fingerprint"):
            if not nonempty_string(course_source.get(key)):
                report.error("STATE_COURSE_SOURCE", f"course_source.{key}", "Passed Input gate requires this course source field.")
        for key in ("segment", "role", "job_to_be_done", "desired_outcome", "ai_maturity", "fingerprint"):
            if not nonempty_string(audience_contract.get(key)):
                report.error("STATE_AUDIENCE", f"audience_contract.{key}", "Passed Input gate requires this audience contract field.")
        declared_audience_fingerprint = audience_contract.get("fingerprint")
        if nonempty_string(declared_audience_fingerprint) and not (
            args.allow_placeholders and has_placeholder(declared_audience_fingerprint)
        ):
            expected_audience_fingerprint = audience_fingerprint(audience_contract)
            if declared_audience_fingerprint != expected_audience_fingerprint:
                report.error("STATE_AUDIENCE_FINGERPRINT", "audience_contract.fingerprint", "Fingerprint does not match the normalized audience contract.")

    downstream_seen = False
    for gate in GATE_ORDER:
        value = gates.get(gate)
        if value in {"PENDING", "BLOCKED", "FAIL"}:
            downstream_seen = True
        elif downstream_seen and value in {"PASS", "APPROVED"}:
            report.error("STATE_GATE_ORDER", f"gates.{gate}", "A downstream gate cannot pass before an upstream pending/failed gate.")

    product_truth = gates.get("PRODUCT_TRUTH")
    artifacts = data.get("artifacts") if isinstance(data.get("artifacts"), dict) else {}
    product_truth_approval = data.get("product_truth_approval") if isinstance(data.get("product_truth_approval"), dict) else {}
    if product_truth_approval.get("status") not in {"PENDING", "APPROVED"}:
        report.error("STATE_PRODUCT_APPROVAL_STATUS", "product_truth_approval.status", "Expected PENDING or APPROVED.")
    if product_truth in {"BLOCKED", "FAIL"}:
        if data.get("status") not in {"PRODUCT_GAP", "BLOCKED"}:
            report.error("STATE_PRODUCT_GAP_STATUS", "status", "Blocked Product Truth requires PRODUCT_GAP or BLOCKED status.")
        if not artifacts.get("product_gap_report"):
            report.error("STATE_PRODUCT_GAP_REPORT", "artifacts.product_gap_report", "Blocked Product Truth requires a product gap report.")
        if data.get("current_gate") != "PRODUCT_TRUTH":
            report.error("STATE_PRODUCT_GAP_GATE", "current_gate", "Blocked Product Truth requires current_gate PRODUCT_TRUTH.")
        for gate in GATE_ORDER[GATE_ORDER.index("RESEARCH") :]:
            if gates.get(gate) not in {"PENDING", "SKIPPED"}:
                report.error("STATE_PRODUCT_GAP_DOWNSTREAM", f"gates.{gate}", "Downstream work must stop after Product Truth is blocked.")
        for artifact_name in artifacts:
            if artifact_name != "product_gap_report":
                report.error("STATE_PRODUCT_GAP_ARTIFACT", f"artifacts.{artifact_name}", "Only product_gap_report may exist while Product Truth is blocked.")

    if product_truth == "PASS":
        if data.get("status") != "PRODUCT_REVIEW" or data.get("current_gate") != "PRODUCT_TRUTH":
            report.error("STATE_PRODUCT_PASS_APPROVAL", "status/current_gate", "Product Truth PASS must remain in PRODUCT_REVIEW at PRODUCT_TRUTH until user approval is recorded.")
        for gate in GATE_ORDER[GATE_ORDER.index("RESEARCH") :]:
            if gates.get(gate) not in {"PENDING", "SKIPPED"}:
                report.error("STATE_PRODUCT_PASS_DOWNSTREAM", f"gates.{gate}", "Downstream gates cannot start before Product Truth is APPROVED.")

    if product_truth == "APPROVED":
        if audience_contract.get("approval_status") != "APPROVED":
            report.error("STATE_PRODUCT_APPROVAL", "audience_contract.approval_status", "APPROVED Product Truth requires the audience/promise contract to be explicitly APPROVED.")
        if product_truth_approval.get("status") != "APPROVED":
            report.error("STATE_PRODUCT_APPROVAL_RECORD", "product_truth_approval.status", "APPROVED Product Truth requires an APPROVED fingerprint-bound approval record.")
        if product_truth_approval.get("course_fingerprint") != course_source.get("fingerprint"):
            report.error("STATE_PRODUCT_APPROVAL_COURSE", "product_truth_approval.course_fingerprint", "Approval record must match the current course fingerprint.")
        if product_truth_approval.get("audience_fingerprint") != audience_contract.get("fingerprint"):
            report.error("STATE_PRODUCT_APPROVAL_AUDIENCE", "product_truth_approval.audience_fingerprint", "Approval record must match the current audience fingerprint.")
        for key in ("decision_id", "approved_at"):
            if not nonempty_string(product_truth_approval.get(key)):
                report.error("STATE_PRODUCT_APPROVAL_EVIDENCE", f"product_truth_approval.{key}", "Approval record requires this field.")
    elif product_truth_approval.get("status") == "APPROVED":
        report.error("STATE_STALE_PRODUCT_APPROVAL", "product_truth_approval.status", "Approval record must be PENDING unless Product Truth gate is APPROVED.")

    if gates.get("BUILD") in {"PASS", "APPROVED"}:
        if not data.get("selected_journey"):
            report.error("STATE_BUILD_JOURNEY", "selected_journey", "Build requires an approved selected journey.")
        for gate in ("PRODUCT_TRUTH", "STRATEGY", "CLAIMS", "BRIEF"):
            if gates.get(gate) != "APPROVED":
                report.error("STATE_BUILD_PREREQUISITE", f"gates.{gate}", "Build requires this gate to be explicitly APPROVED first.")
    if data.get("status") == "READY_FOR_BUILD":
        for gate in ("PRODUCT_TRUTH", "STRATEGY", "CLAIMS", "BRIEF"):
            if gates.get(gate) != "APPROVED":
                report.error("STATE_READY_FOR_BUILD", f"gates.{gate}", "READY_FOR_BUILD requires explicit approval of all strategy gates.")

    if data.get("status") == "PUBLISHED" and gates.get("QA") not in {"PASS", "APPROVED"}:
        report.error("STATE_COMPLETE_QA", "gates.QA", "Published Build state requires QA PASS/APPROVED.")
    if data.get("status") == "PUBLISHED" and gates.get("PUBLISH") not in {"PASS", "APPROVED"}:
        report.error("STATE_PUBLISH_GATE", "gates.PUBLISH", "PUBLISHED status requires Publish gate PASS/APPROVED.")
    if data.get("status") in {"BUILD_READY", "CONNECTED", "READY_FOR_PUBLISH", "PUBLISHED"}:
        for gate in ("BUILD", "QA"):
            if gates.get(gate) not in {"PASS", "APPROVED"}:
                report.error("STATE_BUILD_READY_GATE", f"gates.{gate}", "This Build lifecycle status requires BUILD and QA PASS/APPROVED.")
    if data.get("status") == "COMPLETE":
        if data.get("mode") == "BUILD":
            report.error("STATE_BUILD_COMPLETE", "status", "BUILD mode must use BUILD_READY, CONNECTED, READY_FOR_PUBLISH, or PUBLISHED instead of COMPLETE.")
        if not nonempty_string(data.get("completion_scope")):
            report.error("STATE_COMPLETION_SCOPE", "completion_scope", "COMPLETE requires a non-empty completion_scope.")
        if not artifacts:
            report.error("STATE_COMPLETION_ARTIFACTS", "artifacts", "COMPLETE requires at least one completed artifact.")
        if data.get("mode") == "STRATEGY":
            for gate in ("PRODUCT_TRUTH", "STRATEGY", "CLAIMS", "BRIEF"):
                if gates.get(gate) != "APPROVED":
                    report.error("STATE_STRATEGY_COMPLETE", f"gates.{gate}", "Completed Strategy requires explicit approval of this gate.")
            if gates.get("RESEARCH") not in {"PASS", "APPROVED"}:
                report.error("STATE_STRATEGY_RESEARCH", "gates.RESEARCH", "Completed Strategy requires Research PASS/APPROVED.")
    if data.get("status") in {"BUILDING", "READY_FOR_QA", "BUILD_READY", "CONNECTED", "READY_FOR_PUBLISH", "PUBLISHED"} and data.get("mode") != "BUILD":
        report.error("STATE_BUILD_LIFECYCLE_MODE", "mode", "This Build lifecycle status requires mode BUILD.")

    connectors = data.get("connectors", [])
    if not isinstance(connectors, list):
        report.error("STATE_CONNECTORS", "connectors", "Connectors must be a list.")
    else:
        for index, connector in enumerate(connectors):
            if not isinstance(connector, dict):
                report.error("STATE_CONNECTOR", f"connectors[{index}]", "Connector must be an object.")
                continue
            if connector.get("status") not in CONNECTOR_VALUES:
                report.error("STATE_CONNECTOR_STATUS", f"connectors[{index}].status", f"Expected one of {sorted(CONNECTOR_VALUES)}.")
            if connector.get("status") == "APPROVED_FOR_ACTION" and not connector.get("approved_actions"):
                report.error("STATE_CONNECTOR_APPROVAL", f"connectors[{index}].approved_actions", "APPROVED_FOR_ACTION requires at least one scoped approved action.")
        if data.get("status") == "CONNECTED" and not any(
            isinstance(connector, dict)
            and connector.get("status") in {"AVAILABLE_READ_ONLY", "AVAILABLE_WRITE_PENDING_APPROVAL", "APPROVED_FOR_ACTION"}
            for connector in connectors
        ):
            report.error("STATE_CONNECTED", "connectors", "CONNECTED requires at least one verified available connector.")

    placeholder_issue(report, "$", data, args.allow_placeholders)

    if args.previous:
        previous = read_json(Path(args.previous))
        if not isinstance(previous, dict):
            report.error("STATE_PREVIOUS", "--previous", "Previous state root must be an object.")
        else:
            if previous.get("workflow_id") != data.get("workflow_id"):
                report.error("STATE_WORKFLOW_ID", "workflow_id", "workflow_id cannot change across resume.")
            old_course_fingerprint = first_value(previous, [("course_source", "fingerprint")])
            new_course_fingerprint = first_value(data, [("course_source", "fingerprint")])
            old_audience_fingerprint = first_value(previous, [("audience_contract", "fingerprint")])
            new_audience_fingerprint = first_value(data, [("audience_contract", "fingerprint")])
            fingerprint_changed = (
                bool(old_course_fingerprint and new_course_fingerprint and old_course_fingerprint != new_course_fingerprint)
                or bool(old_audience_fingerprint and new_audience_fingerprint and old_audience_fingerprint != new_audience_fingerprint)
            )
            if fingerprint_changed:
                if not nonempty_string(data.get("revision_reason")):
                    report.error("STATE_REVISION_REASON", "revision_reason", "Changed course/audience fingerprint requires a revision reason.")
                if data.get("status") != "PRODUCT_REVIEW" or data.get("current_gate") != "PRODUCT_TRUTH":
                    report.error("STATE_REVISION_SNAPSHOT", "status/current_gate", "Fingerprint change requires a PRODUCT_REVIEW reset snapshot at PRODUCT_TRUTH.")
                for gate in GATE_ORDER[GATE_ORDER.index("PRODUCT_TRUTH") :]:
                    if gates.get(gate) != "PENDING":
                        report.error("STATE_FINGERPRINT_RESET", f"gates.{gate}", "Changed course/audience fingerprint requires Product Truth and all downstream gates to be PENDING in the reset snapshot.")
                if product_truth_approval.get("status") != "PENDING" or any(
                    product_truth_approval.get(key) is not None
                    for key in ("course_fingerprint", "audience_fingerprint", "decision_id", "approved_at")
                ):
                    report.error("STATE_APPROVAL_RESET", "product_truth_approval", "Fingerprint change requires the previous Product Truth approval record to be cleared.")
                if old_audience_fingerprint != new_audience_fingerprint and audience_contract.get("approval_status") == "APPROVED":
                    report.error("STATE_AUDIENCE_APPROVAL_RESET", "audience_contract.approval_status", "Changed audience fingerprint requires fresh audience approval.")
            old_gates = previous.get("gates", {}) if isinstance(previous.get("gates"), dict) else {}
            for gate in GATE_ORDER:
                old_value = old_gates.get(gate)
                new_value = gates.get(gate)
                if old_value == "PENDING" and new_value == "APPROVED":
                    report.error("STATE_APPROVAL_REQUIRES_PASS", f"gates.{gate}", "A gate must move from PENDING to PASS before a separate APPROVED snapshot.")
                if old_value in {"BLOCKED", "FAIL"} and new_value not in {"BLOCKED", "FAIL"}:
                    if new_value != "PENDING":
                        report.error("STATE_BLOCKED_RESET", f"gates.{gate}", "A blocked/failed gate must reset to PENDING in a separate snapshot before it can pass.")
                    if not nonempty_string(data.get("revision_reason")):
                        report.error("STATE_BLOCKED_REVISION", "revision_reason", "Resetting a blocked/failed gate requires a revision reason.")
                    if gate == "PRODUCT_TRUTH" and (
                        data.get("status") != "PRODUCT_REVIEW" or data.get("current_gate") != "PRODUCT_TRUTH"
                    ):
                        report.error("STATE_BLOCKED_PRODUCT_REVIEW", "status/current_gate", "Resetting Product Truth requires PRODUCT_REVIEW at current_gate PRODUCT_TRUTH.")
            if not data.get("revision_reason"):
                for gate in GATE_ORDER:
                    if old_gates.get(gate) in {"PASS", "APPROVED"} and gates.get(gate) not in {"PASS", "APPROVED"}:
                        report.error("STATE_GATE_REGRESSION", f"gates.{gate}", "Regressing an approved gate requires revision_reason.")
    return report


def split_markdown_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in stripped:
        if escaped:
            current.append(char)
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    if escaped:
        current.append("\\")
    cells.append("".join(current).strip())
    return cells


def parse_claims(text: str, report: Report) -> dict[str, dict[str, str]]:
    required = ["claim_id", "claim", "claim_type", "status", "evidence_type", "source", "used_on", "notes"]
    lines = text.splitlines()
    header_index = -1
    headers: list[str] = []
    for index, line in enumerate(lines):
        cells = [cell.lower() for cell in split_markdown_row(line)] if "|" in line else []
        if set(required).issubset(cells):
            header_index = index
            headers = cells
            break
    if header_index < 0:
        report.error("CLAIMS_HEADER", "Claims table", f"Missing claims table with headers: {', '.join(required)}.")
        return {}
    if len(headers) != len(set(headers)):
        report.error("CLAIMS_HEADER_DUPLICATE", "Claims table", "Claims table headers must be unique.")
        return {}

    claims: dict[str, dict[str, str]] = {}
    for line_number, line in enumerate(lines[header_index + 2 :], start=header_index + 3):
        if not line.strip().startswith("|"):
            if claims:
                break
            continue
        cells = split_markdown_row(line)
        if len(cells) != len(headers):
            report.error("CLAIMS_COLUMNS", f"line {line_number}", f"Expected {len(headers)} columns, got {len(cells)}.")
            continue
        row = dict(zip(headers, cells))
        claim_id = row.get("claim_id", "")
        if not claim_id:
            continue
        if claim_id in claims:
            report.error("CLAIMS_DUPLICATE", f"line {line_number}", f"Duplicate claim_id {claim_id}.")
        claims[claim_id] = row
    return claims


def validate_claim_rows(text: str, args: argparse.Namespace) -> tuple[Report, dict[str, dict[str, str]]]:
    report = Report(args.strict)
    claims = parse_claims(text, report)
    type_values = {
        "fact",
        "outcome",
        "instructor",
        "policy",
        "support",
        "testimonial",
        "social_proof",
        "urgency",
        "price",
        "compliance",
    }
    status_values = {"VERIFIED", "INFERRED", "PROPOSED", "UNKNOWN", "REJECTED"}
    for claim_id, row in claims.items():
        location = f"claim:{claim_id}"
        if not CLAIM_ID_RE.match(claim_id):
            report.error("CLAIM_ID", location, "claim_id must match ^[a-z0-9][a-z0-9_-]*$.")
        if not row.get("claim"):
            report.error("CLAIM_TEXT", location, "Claim text is required.")
        placeholder_issue(report, location, row, args.allow_placeholders)
        claim_type = row.get("claim_type", "").lower()
        status = row.get("status", "").upper()
        if claim_type not in type_values:
            report.error("CLAIM_TYPE", location, f"Expected one of {sorted(type_values)}.")
        if status not in status_values:
            report.error("CLAIM_STATUS", location, f"Expected one of {sorted(status_values)}.")
        if status == "VERIFIED" and not row.get("source"):
            report.error("CLAIM_SOURCE", location, "VERIFIED claim requires a source.")
        if row.get("used_on") and status != "VERIFIED":
            if args.allow_proposed:
                report.warning("CLAIM_PUBLIC_DRAFT", location, "Non-verified claim is referenced by draft copy.")
            else:
                report.error("CLAIM_PUBLIC", location, "Only VERIFIED claims may be used in public copy.")
        if status == "REJECTED" and row.get("used_on"):
            report.error("CLAIM_REJECTED_USE", location, "REJECTED claim cannot be used.")
        if args.check_local_sources and status == "VERIFIED":
            source = row.get("source", "")
            if source and not re.match(r"^[a-z]+://", source, re.IGNORECASE) and not source.startswith("SRC-"):
                source_path = Path(source).expanduser()
                if not source_path.exists():
                    report.error("CLAIM_LOCAL_SOURCE", location, f"Local source does not exist: {source}")
    if not claims:
        report.error("CLAIMS_EMPTY", "Claims table", "At least one claim row is required.")
    return report, claims


def validate_claims(path: Path, args: argparse.Namespace) -> Report:
    report, _ = validate_claim_rows(read_text(path), args)
    return report


WEBINAR_PAGE_IDS = {"registration", "thank_you", "watch", "booking", "booking_success"}
WEBINAR_ROUTES = {
    ("registration", "submit", "thank_you"),
    ("thank_you", "watch_webinar", "watch"),
    ("watch", "book_consultation", "booking"),
    ("booking", "submit", "booking_success"),
}
WEBINAR_EVENTS = {
    "course_view",
    "cta_click",
    "video_start",
    "video_progress",
    "form_start",
    "lead_submitted",
    "webinar_registered",
    "webinar_watch_started",
    "webinar_progress_25",
    "webinar_progress_50",
    "webinar_progress_75",
    "webinar_completed",
    "webinar_cta_viewed",
    "webinar_cta_clicked",
    "consultation_booked",
}
BASE_EVENTS = {"course_view", "cta_click"}
FUNNEL_PROFILES = {"WEBINAR_BOOKING", "LEAD_CAPTURE", "CONSULTATION_BOOKING", "DIRECT_SALE", "CUSTOM"}
PROFILE_REQUIREMENTS = {
    "WEBINAR_BOOKING": {
        "pages": WEBINAR_PAGE_IDS,
        "routes": WEBINAR_ROUTES,
        "events": WEBINAR_EVENTS,
    },
    "LEAD_CAPTURE": {
        "pages": {"registration", "thank_you"},
        "routes": {("registration", "submit", "thank_you")},
        "events": BASE_EVENTS | {"form_start", "lead_submitted"},
    },
    "CONSULTATION_BOOKING": {
        "pages": {"landing", "booking", "booking_success"},
        "routes": {("landing", "book_consultation", "booking"), ("booking", "submit", "booking_success")},
        "events": BASE_EVENTS | {"form_start", "consultation_booked"},
    },
    "DIRECT_SALE": {
        "pages": {"landing", "checkout", "purchase_success"},
        "routes": {("landing", "enroll", "checkout"), ("checkout", "submit", "purchase_success")},
        "events": BASE_EVENTS | {"form_start", "enrollment_paid"},
    },
}
MUTATING_ACTION_WORDS = {"write", "send", "publish", "deploy", "migration", "migrate", "create", "activate"}
PII_KEYS = {"email", "phone", "telephone", "full_name", "name", "address", "zalo_id", "user_email", "user_phone"}
COURSE_EXPLANATION_SECTION_KEYS = ("value", "curriculum", "instructors", "faq")
COURSE_VALUE_CATEGORIES = {"capability", "application", "support_or_right"}
CONCRETE_OUTCOME_MARKERS = (
    "tạo",
    "viết",
    "soạn",
    "cài đặt",
    "kết nối",
    "lên lịch",
    "tóm tắt",
    "trích xuất",
    "kiểm tra",
    "phân tích",
    "chỉnh sửa",
    "trình bày",
    "vận hành",
    "xử lý",
    "thiết kế",
    "xây dựng",
    "thực hiện",
    "hoàn thành",
    "đánh giá",
    "quản lý",
    "sử dụng",
)
ABSTRACT_OUTCOME_MARKERS = ("hiểu", "nắm", "biết", "nhận thức", "làm quen", "tổng quan", "tư duy")


def extract_manifest(text: str, report: Report) -> dict[str, Any]:
    blocks = re.findall(r"```kstudy-funnel-manifest\s*\n(.*?)\n```", text, flags=re.DOTALL)
    if len(blocks) != 1:
        report.error("BRIEF_MANIFEST_COUNT", "manifest", f"Expected exactly one kstudy-funnel-manifest block, found {len(blocks)}.")
        return {}
    try:
        manifest = json.loads(blocks[0])
    except json.JSONDecodeError as exc:
        report.error("BRIEF_MANIFEST_JSON", "manifest", f"Invalid JSON: {exc}.")
        return {}
    if not isinstance(manifest, dict):
        report.error("BRIEF_MANIFEST_ROOT", "manifest", "Manifest root must be an object.")
        return {}
    return manifest


def collect_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(str(key).lower())
            keys.update(collect_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(collect_keys(child))
    return keys


def nonempty_string_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(nonempty_string(item) for item in value)


def collect_claim_ids(value: Any) -> set[str]:
    claim_ids: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "claim_ids" and isinstance(child, list):
                claim_ids.update(str(item) for item in child if nonempty_string(item))
            else:
                claim_ids.update(collect_claim_ids(child))
    elif isinstance(value, list):
        for child in value:
            claim_ids.update(collect_claim_ids(child))
    return claim_ids


def validate_course_explanation(
    manifest: dict[str, Any],
    page_by_id: dict[str, dict[str, Any]],
    report: Report,
    args: argparse.Namespace,
) -> dict[str, Any]:
    contract = manifest.get("course_explanation")
    if not isinstance(contract, dict):
        report.error(
            "BRIEF_COURSE_EXPLANATION",
            "manifest.course_explanation",
            "A course landing brief requires a structured course_explanation contract.",
        )
        return {}

    page_id = contract.get("page_id")
    if not nonempty_string(page_id) or page_id not in page_by_id:
        report.error(
            "BRIEF_COURSE_PAGE",
            "manifest.course_explanation.page_id",
            "Course explanation page_id must reference an existing page.",
        )
        page_sections: set[str] = set()
    else:
        sections = page_by_id[page_id].get("sections", [])
        page_sections = {str(item) for item in sections} if isinstance(sections, list) else set()

    section_ids = contract.get("section_ids")
    if not isinstance(section_ids, dict):
        report.error(
            "BRIEF_COURSE_SECTIONS",
            "manifest.course_explanation.section_ids",
            "Section ids for value, curriculum, instructors, and faq are required.",
        )
    else:
        for key in COURSE_EXPLANATION_SECTION_KEYS:
            section_id = section_ids.get(key)
            location = f"manifest.course_explanation.section_ids.{key}"
            if not nonempty_string(section_id):
                report.error("BRIEF_COURSE_SECTION_ID", location, "A non-empty section id is required.")
            elif page_sections and section_id not in page_sections:
                report.error(
                    "BRIEF_COURSE_SECTION_MISSING",
                    location,
                    f"Section id {section_id!r} is not declared on page {page_id!r}.",
                )

    language = contract.get("language_style")
    expected_language = {
        "primary": "vi",
        "plain_language": True,
        "jargon_policy": "explain_or_replace",
        "outcome_frame": "can_do",
    }
    if not isinstance(language, dict):
        report.error(
            "BRIEF_COURSE_LANGUAGE",
            "manifest.course_explanation.language_style",
            "Plain Vietnamese language contract is required.",
        )
    else:
        for key, expected in expected_language.items():
            if language.get(key) != expected:
                report.error(
                    "BRIEF_COURSE_LANGUAGE_RULE",
                    f"manifest.course_explanation.language_style.{key}",
                    f"Expected {expected!r}.",
                )

    value_points = contract.get("value_points")
    if not isinstance(value_points, list) or len(value_points) < 4:
        message = "Include at least four concrete capability, application, or verified support/right points."
        if args.allow_placeholders and isinstance(value_points, list) and value_points and has_placeholder(value_points):
            report.warning("BRIEF_COURSE_VALUE_POINTS", "manifest.course_explanation.value_points", message)
        else:
            report.error("BRIEF_COURSE_VALUE_POINTS", "manifest.course_explanation.value_points", message)
        value_points = []
    for index, point in enumerate(value_points):
        location = f"manifest.course_explanation.value_points[{index}]"
        if not isinstance(point, dict):
            report.error("BRIEF_COURSE_VALUE_POINT", location, "Value point must be an object.")
            continue
        if point.get("category") not in COURSE_VALUE_CATEGORIES:
            report.error(
                "BRIEF_COURSE_VALUE_CATEGORY",
                f"{location}.category",
                f"Expected one of {sorted(COURSE_VALUE_CATEGORIES)}.",
            )
        for field in ("copy",):
            if not nonempty_string(point.get(field)):
                report.error("BRIEF_COURSE_VALUE_COPY", f"{location}.{field}", "Concrete customer-facing copy is required.")
        if not nonempty_string_list(point.get("claim_ids")):
            report.error("BRIEF_COURSE_VALUE_CLAIMS", f"{location}.claim_ids", "At least one claim_id is required.")

    modules = contract.get("modules")
    if not isinstance(modules, list) or not modules:
        report.error(
            "BRIEF_COURSE_MODULES",
            "manifest.course_explanation.modules",
            "Include every in-scope course module with customer-facing outcomes.",
        )
        modules = []
    seen_module_ids: set[str] = set()
    for index, module in enumerate(modules):
        location = f"manifest.course_explanation.modules[{index}]"
        if not isinstance(module, dict):
            report.error("BRIEF_COURSE_MODULE", location, "Module must be an object.")
            continue
        module_id = module.get("module_id")
        if not nonempty_string(module_id):
            report.error("BRIEF_COURSE_MODULE_ID", f"{location}.module_id", "Module id is required for source traceability.")
        elif module_id in seen_module_ids:
            report.error("BRIEF_COURSE_MODULE_DUPLICATE", f"{location}.module_id", f"Duplicate module id {module_id}.")
        else:
            seen_module_ids.add(module_id)
        for field in ("customer_title", "hands_on_output"):
            if not nonempty_string(module.get(field)):
                report.error("BRIEF_COURSE_MODULE_FIELD", f"{location}.{field}", "A customer-facing value is required.")
        outcomes = module.get("can_do")
        if not nonempty_string_list(outcomes):
            report.error(
                "BRIEF_COURSE_MODULE_OUTCOMES",
                f"{location}.can_do",
                "Include at least one plain-language action the learner can perform.",
            )
        else:
            for outcome_index, outcome in enumerate(outcomes):
                lowered = outcome.lower()
                has_concrete_marker = any(marker in lowered for marker in CONCRETE_OUTCOME_MARKERS)
                has_abstract_marker = any(marker in lowered for marker in ABSTRACT_OUTCOME_MARKERS)
                if has_abstract_marker and not has_concrete_marker:
                    report.warning(
                        "BRIEF_COURSE_MODULE_VAGUE",
                        f"{location}.can_do[{outcome_index}]",
                        "Outcome sounds conceptual; rewrite it as a concrete action or work output.",
                    )
        if not nonempty_string_list(module.get("source_refs")):
            report.error("BRIEF_COURSE_MODULE_SOURCES", f"{location}.source_refs", "At least one course/lesson source ref is required.")
        if not nonempty_string_list(module.get("claim_ids")):
            report.error("BRIEF_COURSE_MODULE_CLAIMS", f"{location}.claim_ids", "At least one claim_id is required.")

    instructors = contract.get("instructors")
    if not isinstance(instructors, list) or not instructors:
        report.error(
            "BRIEF_COURSE_INSTRUCTORS",
            "manifest.course_explanation.instructors",
            "Include at least one verified course instructor.",
        )
        instructors = []
    for index, instructor in enumerate(instructors):
        location = f"manifest.course_explanation.instructors[{index}]"
        if not isinstance(instructor, dict):
            report.error("BRIEF_COURSE_INSTRUCTOR", location, "Instructor must be an object.")
            continue
        for field in ("name", "role_in_course", "short_bio", "image_asset_id"):
            if not nonempty_string(instructor.get(field)):
                report.error("BRIEF_COURSE_INSTRUCTOR_FIELD", f"{location}.{field}", "Verified instructor content is required.")
        if not nonempty_string_list(instructor.get("source_refs")):
            report.error("BRIEF_COURSE_INSTRUCTOR_SOURCES", f"{location}.source_refs", "At least one verified profile source is required.")
        if not nonempty_string_list(instructor.get("claim_ids")):
            report.error("BRIEF_COURSE_INSTRUCTOR_CLAIMS", f"{location}.claim_ids", "At least one claim_id is required.")

    faqs = contract.get("faqs")
    if not isinstance(faqs, list) or len(faqs) < 4:
        message = "Include at least four relevant, source-backed FAQs."
        if args.allow_placeholders and isinstance(faqs, list) and faqs and has_placeholder(faqs):
            report.warning("BRIEF_COURSE_FAQS", "manifest.course_explanation.faqs", message)
        else:
            report.error("BRIEF_COURSE_FAQS", "manifest.course_explanation.faqs", message)
        faqs = []
    for index, faq in enumerate(faqs):
        location = f"manifest.course_explanation.faqs[{index}]"
        if not isinstance(faq, dict):
            report.error("BRIEF_COURSE_FAQ", location, "FAQ must be an object.")
            continue
        for field in ("question", "answer"):
            if not nonempty_string(faq.get(field)):
                report.error("BRIEF_COURSE_FAQ_FIELD", f"{location}.{field}", "A direct customer-facing value is required.")
        if not nonempty_string_list(faq.get("source_refs")):
            report.error("BRIEF_COURSE_FAQ_SOURCES", f"{location}.source_refs", "At least one course, policy, or research source ref is required.")
        if not nonempty_string_list(faq.get("claim_ids")):
            report.error("BRIEF_COURSE_FAQ_CLAIMS", f"{location}.claim_ids", "At least one claim_id is required.")
    return contract


def validate_brief(path: Path, args: argparse.Namespace) -> Report:
    report = Report(args.strict)
    text = read_text(path)
    manifest = extract_manifest(text, report)
    if not manifest:
        return report
    if manifest.get("schema") != "kstudy.funnel-brief/v1":
        report.error("BRIEF_SCHEMA", "manifest.schema", "Expected kstudy.funnel-brief/v1.")
    if manifest.get("mode") not in {"STRATEGY", "BUILD", "OPTIMIZE"}:
        report.error("BRIEF_MODE", "manifest.mode", "Expected STRATEGY, BUILD, or OPTIMIZE.")
    profile = manifest.get("funnel_profile")
    if profile not in FUNNEL_PROFILES:
        report.error("BRIEF_PROFILE", "manifest.funnel_profile", f"Expected one of {sorted(FUNNEL_PROFILES)}.")

    pages = manifest.get("pages")
    page_by_id: dict[str, dict[str, Any]] = {}
    paths: set[str] = set()
    if not isinstance(pages, list):
        report.error("BRIEF_PAGES", "manifest.pages", "Pages must be a list.")
        pages = []
    for index, page in enumerate(pages):
        if not isinstance(page, dict):
            report.error("BRIEF_PAGE", f"manifest.pages[{index}]", "Page must be an object.")
            continue
        page_id = page.get("id")
        page_path = page.get("path")
        if not nonempty_string(page_id):
            report.error("BRIEF_PAGE_ID", f"manifest.pages[{index}].id", "Page id is required.")
        elif page_id in page_by_id:
            report.error("BRIEF_PAGE_DUPLICATE", f"manifest.pages[{index}].id", f"Duplicate page id {page_id}.")
        else:
            page_by_id[page_id] = page
        if not nonempty_string(page_path):
            report.error("BRIEF_PAGE_PATH", f"manifest.pages[{index}].path", "Page path is required.")
        elif page_path in paths:
            report.error("BRIEF_PATH_DUPLICATE", f"manifest.pages[{index}].path", f"Duplicate page path {page_path}.")
        else:
            paths.add(page_path)
        for field in ("goal", "primary_cta"):
            if not nonempty_string(page.get(field)):
                report.error("BRIEF_PAGE_REQUIRED", f"manifest.pages[{index}].{field}", "Required page field is missing.")
        if not isinstance(page.get("sections"), list) or not page.get("sections"):
            report.error("BRIEF_PAGE_SECTIONS", f"manifest.pages[{index}].sections", "Page needs at least one section.")
        if page.get("index_policy") not in {"index", "noindex"}:
            report.error("BRIEF_INDEX_POLICY", f"manifest.pages[{index}].index_policy", "Expected index or noindex.")
        if page.get("index_policy") == "index" and not page.get("canonical"):
            report.error("BRIEF_CANONICAL", f"manifest.pages[{index}].canonical", "Indexable page requires canonical/self-canonical.")
    if profile == "CUSTOM":
        custom_required_pages = manifest.get("required_page_ids")
        if not isinstance(custom_required_pages, list) or not custom_required_pages:
            report.error("BRIEF_CUSTOM_PAGES", "manifest.required_page_ids", "CUSTOM profile requires a non-empty required_page_ids list.")
            required_pages: set[str] = set()
        else:
            required_pages = {str(item) for item in custom_required_pages}
    else:
        required_pages = PROFILE_REQUIREMENTS.get(profile, {}).get("pages", set())
    missing_pages = required_pages - set(page_by_id)
    if missing_pages:
        report.error("BRIEF_REQUIRED_PAGES", "manifest.pages", f"Missing required page ids: {sorted(missing_pages)}.")

    routes = manifest.get("routes")
    route_tuples: set[tuple[str, str, str]] = set()
    if not isinstance(routes, list):
        report.error("BRIEF_ROUTES", "manifest.routes", "Routes must be a list.")
        routes = []
    for index, route in enumerate(routes):
        if not isinstance(route, dict):
            report.error("BRIEF_ROUTE", f"manifest.routes[{index}]", "Route must be an object.")
            continue
        item = (str(route.get("from", "")), str(route.get("action", "")), str(route.get("to", "")))
        if item in route_tuples:
            report.error("BRIEF_ROUTE_DUPLICATE", f"manifest.routes[{index}]", f"Duplicate route {item}.")
        route_tuples.add(item)
    if profile == "CUSTOM":
        custom_routes = manifest.get("required_routes", [])
        required_routes = {
            (str(item.get("from", "")), str(item.get("action", "")), str(item.get("to", "")))
            for item in custom_routes
            if isinstance(item, dict)
        }
    else:
        required_routes = PROFILE_REQUIREMENTS.get(profile, {}).get("routes", set())
    missing_routes = required_routes - route_tuples
    if missing_routes:
        report.error("BRIEF_REQUIRED_ROUTES", "manifest.routes", f"Missing required routes: {sorted(missing_routes)}.")

    events = manifest.get("events")
    if not isinstance(events, list):
        report.error("BRIEF_EVENTS", "manifest.events", "Events must be a list.")
        events = []
    if profile == "CUSTOM":
        custom_events = manifest.get("required_events", [])
        if not isinstance(custom_events, list) or not custom_events:
            report.error("BRIEF_CUSTOM_EVENTS", "manifest.required_events", "CUSTOM profile requires a non-empty required_events list.")
            required_events: set[str] = set()
        else:
            required_events = BASE_EVENTS | {str(item) for item in custom_events}
    else:
        required_events = PROFILE_REQUIREMENTS.get(profile, {}).get("events", set())
    missing_events = required_events - set(events)
    if missing_events:
        report.error("BRIEF_REQUIRED_EVENTS", "manifest.events", f"Missing required events: {sorted(missing_events)}.")

    lead_routing = manifest.get("lead_routing")
    if not isinstance(lead_routing, dict):
        report.error("BRIEF_LEAD_ROUTING", "manifest.lead_routing", "Lead routing must be an object.")
        lead_routing = {}
    for key in ("store_first", "async_delivery", "server_validation", "rate_limit", "retry_and_failed_delivery", "audit_log"):
        if lead_routing.get(key) is not True:
            report.error("BRIEF_LEAD_RULE", f"manifest.lead_routing.{key}", "This lead safety rule must be true.")
    if lead_routing.get("idempotency_key") != "lead_id":
        report.error("BRIEF_IDEMPOTENCY", "manifest.lead_routing.idempotency_key", "Expected lead_id.")

    integrity = manifest.get("integrity")
    if not isinstance(integrity, dict):
        report.error("BRIEF_INTEGRITY", "manifest.integrity", "Integrity contract must be an object.")
        integrity = {}
    for key in ("fake_live", "fake_viewers", "fake_scarcity", "fake_countdown", "pii_in_analytics"):
        if integrity.get(key) is not False:
            report.error("BRIEF_INTEGRITY_RULE", f"manifest.integrity.{key}", "This integrity risk must be explicitly false.")

    actions = manifest.get("external_actions", [])
    if not isinstance(actions, list):
        report.error("BRIEF_EXTERNAL_ACTIONS", "manifest.external_actions", "External actions must be a list.")
    else:
        for index, action in enumerate(actions):
            if not isinstance(action, dict):
                report.error("BRIEF_EXTERNAL_ACTION", f"manifest.external_actions[{index}]", "Action must be an object.")
                continue
            action_name = str(action.get("action", "")).lower()
            if any(word in action_name for word in MUTATING_ACTION_WORDS) and action.get("approval_required") is not True:
                report.error("BRIEF_EXTERNAL_APPROVAL", f"manifest.external_actions[{index}]", "Mutating external action requires explicit approval_required=true.")

    tracking_contract = manifest.get("event_properties", manifest.get("tracking_properties", {}))
    pii_keys = collect_keys(tracking_contract) & PII_KEYS
    if pii_keys:
        report.error("BRIEF_PII", "manifest.event_properties", f"PII keys are not allowed in analytics contract: {sorted(pii_keys)}.")

    course_explanation = validate_course_explanation(manifest, page_by_id, report, args)

    required_headings = {f"## {number}." for number in range(1, 19)}
    present_headings = {prefix for prefix in required_headings if prefix in text}
    if present_headings != required_headings:
        missing = sorted(required_headings - present_headings)
        report.error("BRIEF_HEADINGS", "markdown", f"Missing required numbered brief sections: {missing}.")

    placeholder_issue(report, "manifest", manifest, args.allow_placeholders)
    placeholder_issue(report, "markdown", text, args.allow_placeholders)

    if args.claims:
        claim_args = argparse.Namespace(
            strict=False,
            allow_placeholders=args.allow_placeholders,
            allow_proposed=False,
            check_local_sources=False,
        )
        claims_report, claims = validate_claim_rows(read_text(Path(args.claims)), claim_args)
        report.issues.extend(claims_report.issues)
        used_ids = collect_claim_ids(page_by_id)
        used_ids.update(collect_claim_ids(course_explanation))
        for claim_id in used_ids:
            row = claims.get(claim_id)
            if row is None:
                report.error("BRIEF_CLAIM_MISSING", f"claim_ids.{claim_id}", "Claim is not present in ledger.")
            elif row.get("status", "").upper() != "VERIFIED":
                report.error("BRIEF_CLAIM_STATUS", f"claim_ids.{claim_id}", "Claim used by brief must be VERIFIED.")
    return report


def emit(report: Report, as_json: bool) -> int:
    if as_json:
        payload = {
            "valid": report.valid,
            "errors": [asdict(issue) for issue in report.errors],
            "warnings": [asdict(issue) for issue in report.warnings],
            "metadata": report.metadata,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for issue in report.issues:
            print(f"{issue.level} {issue.code} {issue.location}: {issue.message}")
        if report.metadata:
            print("METADATA " + json.dumps(report.metadata, ensure_ascii=False, sort_keys=True))
        state = "PASS" if report.valid else "FAIL"
        print(f"{state}: {len(report.errors)} error(s), {len(report.warnings)} warning(s)")
    return 0 if report.valid else 1


def add_common_flags(parser: argparse.ArgumentParser, *, placeholders: bool = True) -> None:
    parser.add_argument("path", help="Artifact path")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failure")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Emit JSON report")
    if placeholders:
        parser.add_argument("--allow-placeholders", action="store_true", help="Warn instead of fail on template placeholders")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate Kstudy course funnel artifacts")
    subparsers = parser.add_subparsers(dest="command", required=True)

    course = subparsers.add_parser("course", help="Validate course.json structure")
    add_common_flags(course, placeholders=False)

    state = subparsers.add_parser("state", help="Validate workflow-state.json")
    add_common_flags(state)
    state.add_argument("--previous", help="Previous workflow state for transition validation")

    claims = subparsers.add_parser("claims", help="Validate claims Markdown ledger")
    add_common_flags(claims)
    claims.add_argument("--allow-proposed", action="store_true", help="Warn when proposed claims are referenced in draft copy")
    claims.add_argument("--check-local-sources", action="store_true", help="Check local source paths without fetching URLs")

    brief = subparsers.add_parser("brief", help="Validate landing-page-brief.md")
    add_common_flags(brief)
    brief.add_argument("--claims", help="Claims ledger to cross-check page claim_ids")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    path = Path(args.path).expanduser()
    try:
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {path}")
        if args.command == "course":
            report = validate_course(path, args)
        elif args.command == "state":
            report = validate_state(path, args)
        elif args.command == "claims":
            report = validate_claims(path, args)
        elif args.command == "brief":
            report = validate_brief(path, args)
        else:
            parser.error("Unknown command")
            return 2
        return emit(report, args.as_json)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"FATAL READ_OR_PARSE {path}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
