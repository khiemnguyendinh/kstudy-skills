#!/usr/bin/env python3
"""Regression tests for validate_funnel.py using temporary artifacts only."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate_funnel.py")
SPEC = importlib.util.spec_from_file_location("validate_funnel", MODULE_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


def args(**overrides):
    values = {
        "strict": False,
        "allow_placeholders": False,
        "allow_proposed": False,
        "check_local_sources": False,
        "previous": None,
        "claims": None,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


class TemporaryArtifact(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def write(self, name: str, content: str) -> Path:
        path = self.root / name
        path.write_text(content, encoding="utf-8")
        return path


class StateValidationTests(TemporaryArtifact):
    def valid_state(self) -> dict:
        state = {
            "schema_version": "1.0",
            "workflow_id": "enter-ai-ops",
            "project_name": "Enter AI for Operations",
            "mode": "STRATEGY",
            "status": "PRODUCT_REVIEW",
            "current_gate": "PRODUCT_TRUTH",
            "course_source": {"path": "/tmp/course.json", "version": "1", "fingerprint": "abc", "approval_status": "APPROVED"},
            "audience_contract": {"segment": "SME managers", "role": "manager", "department_or_use_case": "operations", "job_to_be_done": "deploy AI", "desired_outcome": "approved outcome", "ai_maturity": "beginner", "anti_persona": "students", "approval_status": "APPROVED"},
            "product_truth_approval": {"status": "PENDING", "course_fingerprint": None, "audience_fingerprint": None, "decision_id": None, "approved_at": None},
            "acquisition": {"channel": "organic", "source": "fanpage_kstudy", "content_angle": "workflow", "content_format": "post", "landing_variant": "ops"},
            "conversion": {"funnel_entry": "on-demand webinar", "primary": "book consultation", "secondary": "watch webinar"},
            "gates": {
                "INPUT": "PASS",
                "PRODUCT_TRUTH": "PENDING",
                "RESEARCH": "PENDING",
                "STRATEGY": "PENDING",
                "CLAIMS": "PENDING",
                "BRIEF": "PENDING",
                "BUILD": "PENDING",
                "QA": "PENDING",
                "PUBLISH": "PENDING",
            },
            "selected_journey": None,
            "visual_direction": {"visual_style": "editorial", "required_sections": []},
            "connectors": [{"name": "supabase", "status": "UNVERIFIED", "approved_actions": []}],
            "artifacts": {},
            "pending_external_actions": [],
            "decisions": [],
            "completion_scope": None,
            "revision_reason": None,
        }
        state["audience_contract"]["fingerprint"] = VALIDATOR.audience_fingerprint(state["audience_contract"])
        return state

    def approve_product_truth(self, state: dict) -> None:
        state["gates"]["PRODUCT_TRUTH"] = "APPROVED"
        state["audience_contract"]["approval_status"] = "APPROVED"
        state["product_truth_approval"] = {
            "status": "APPROVED",
            "course_fingerprint": state["course_source"]["fingerprint"],
            "audience_fingerprint": state["audience_contract"]["fingerprint"],
            "decision_id": "decision-product-truth-001",
            "approved_at": "2026-07-13T09:00:00+07:00",
        }

    def test_valid_in_progress_state(self) -> None:
        path = self.write("state.json", json.dumps(self.valid_state()))
        self.assertTrue(VALIDATOR.validate_state(path, args()).valid)

    def test_product_gap_blocks_downstream_build(self) -> None:
        state = self.valid_state()
        state["status"] = "PRODUCT_GAP"
        state["gates"]["PRODUCT_TRUTH"] = "BLOCKED"
        state["gates"]["BUILD"] = "PASS"
        state["artifacts"] = {"product_gap_report": "product-gap-report.md", "app": "site/"}
        path = self.write("blocked.json", json.dumps(state))
        codes = {issue.code for issue in VALIDATOR.validate_state(path, args()).errors}
        self.assertIn("STATE_PRODUCT_GAP_DOWNSTREAM", codes)
        self.assertIn("STATE_PRODUCT_GAP_ARTIFACT", codes)

    def test_build_mode_cannot_use_complete(self) -> None:
        state = self.valid_state()
        state["mode"] = "BUILD"
        state["status"] = "COMPLETE"
        state["completion_scope"] = "local funnel"
        path = self.write("build-complete.json", json.dumps(state))
        codes = {issue.code for issue in VALIDATOR.validate_state(path, args()).errors}
        self.assertIn("STATE_BUILD_COMPLETE", codes)

    def test_strategy_complete_requires_approved_gates_and_artifacts(self) -> None:
        state = self.valid_state()
        state["status"] = "COMPLETE"
        state["completion_scope"] = "Strategy pack"
        path = self.write("strategy-incomplete.json", json.dumps(state))
        codes = {issue.code for issue in VALIDATOR.validate_state(path, args()).errors}
        self.assertIn("STATE_COMPLETION_ARTIFACTS", codes)
        self.assertIn("STATE_STRATEGY_COMPLETE", codes)

    def test_build_lifecycle_status_requires_build_mode(self) -> None:
        state = self.valid_state()
        state["status"] = "BUILDING"
        path = self.write("strategy-building.json", json.dumps(state))
        codes = {issue.code for issue in VALIDATOR.validate_state(path, args()).errors}
        self.assertIn("STATE_BUILD_LIFECYCLE_MODE", codes)

    def test_approved_connector_requires_scoped_action(self) -> None:
        state = self.valid_state()
        state["connectors"] = [{"name": "supabase", "status": "APPROVED_FOR_ACTION", "approved_actions": []}]
        path = self.write("connector.json", json.dumps(state))
        codes = {issue.code for issue in VALIDATOR.validate_state(path, args()).errors}
        self.assertIn("STATE_CONNECTOR_APPROVAL", codes)

    def product_gap_state(self) -> dict:
        state = self.valid_state()
        state["status"] = "PRODUCT_GAP"
        state["current_gate"] = "PRODUCT_TRUTH"
        state["gates"]["PRODUCT_TRUTH"] = "BLOCKED"
        state["artifacts"] = {"product_gap_report": "product-gap-report.md"}
        return state

    def test_course_change_uses_reset_then_reevaluate_snapshots(self) -> None:
        previous = self.product_gap_state()
        previous_path = self.write("previous-gap.json", json.dumps(previous))

        reset = copy.deepcopy(previous)
        reset["course_source"]["fingerprint"] = "new-course-fingerprint"
        reset["status"] = "PRODUCT_REVIEW"
        reset["current_gate"] = "PRODUCT_TRUTH"
        reset["gates"]["PRODUCT_TRUTH"] = "PENDING"
        reset["artifacts"] = {}
        reset["revision_reason"] = "Approved Operations course source received"
        reset_path = self.write("reset.json", json.dumps(reset))
        self.assertTrue(VALIDATOR.validate_state(reset_path, args(previous=str(previous_path))).valid)

        passed = copy.deepcopy(reset)
        passed["gates"]["PRODUCT_TRUTH"] = "PASS"
        passed_path = self.write("passed.json", json.dumps(passed))
        self.assertTrue(VALIDATOR.validate_state(passed_path, args(previous=str(reset_path))).valid)

        approved = copy.deepcopy(passed)
        approved["status"] = "RESEARCH"
        approved["current_gate"] = "RESEARCH"
        self.approve_product_truth(approved)
        approved_path = self.write("approved.json", json.dumps(approved))
        self.assertTrue(VALIDATOR.validate_state(approved_path, args(previous=str(passed_path))).valid)

    def test_blocked_product_truth_cannot_jump_directly_to_pass(self) -> None:
        previous = self.product_gap_state()
        previous_path = self.write("blocked-before.json", json.dumps(previous))
        jumped = copy.deepcopy(previous)
        jumped["status"] = "RESEARCH"
        jumped["current_gate"] = "RESEARCH"
        jumped["gates"]["PRODUCT_TRUTH"] = "PASS"
        jumped["artifacts"] = {}
        jumped["revision_reason"] = "New supporting evidence received"
        jumped_path = self.write("blocked-jump.json", json.dumps(jumped))
        codes = {issue.code for issue in VALIDATOR.validate_state(jumped_path, args(previous=str(previous_path))).errors}
        self.assertIn("STATE_BLOCKED_RESET", codes)

        reset = copy.deepcopy(previous)
        reset["status"] = "PRODUCT_REVIEW"
        reset["current_gate"] = "PRODUCT_TRUTH"
        reset["gates"]["PRODUCT_TRUTH"] = "PENDING"
        reset["artifacts"] = {}
        reset["revision_reason"] = "New supporting evidence received"
        reset_path = self.write("blocked-reset.json", json.dumps(reset))
        self.assertTrue(VALIDATOR.validate_state(reset_path, args(previous=str(previous_path))).valid)

    def test_audience_change_requires_product_truth_reset(self) -> None:
        previous = self.valid_state()
        previous["status"] = "RESEARCH"
        previous["current_gate"] = "RESEARCH"
        self.approve_product_truth(previous)
        previous_path = self.write("audience-before.json", json.dumps(previous))

        changed = copy.deepcopy(previous)
        changed["audience_contract"]["desired_outcome"] = "a different approved outcome"
        changed["audience_contract"]["fingerprint"] = VALIDATOR.audience_fingerprint(changed["audience_contract"])
        changed_path = self.write("audience-no-reset.json", json.dumps(changed))
        codes = {issue.code for issue in VALIDATOR.validate_state(changed_path, args(previous=str(previous_path))).errors}
        self.assertIn("STATE_FINGERPRINT_RESET", codes)
        self.assertIn("STATE_REVISION_SNAPSHOT", codes)

        reset = copy.deepcopy(changed)
        reset["status"] = "PRODUCT_REVIEW"
        reset["current_gate"] = "PRODUCT_TRUTH"
        reset["revision_reason"] = "Audience desired outcome changed"
        for gate in VALIDATOR.GATE_ORDER[VALIDATOR.GATE_ORDER.index("PRODUCT_TRUTH") :]:
            reset["gates"][gate] = "PENDING"
        reset["audience_contract"]["approval_status"] = "PROPOSED"
        reset["product_truth_approval"] = {"status": "PENDING", "course_fingerprint": None, "audience_fingerprint": None, "decision_id": None, "approved_at": None}
        reset_path = self.write("audience-reset.json", json.dumps(reset))
        self.assertTrue(VALIDATOR.validate_state(reset_path, args(previous=str(previous_path))).valid)

    def test_pending_gate_cannot_jump_directly_to_approved(self) -> None:
        previous = self.valid_state()
        previous_path = self.write("pending.json", json.dumps(previous))
        approved = copy.deepcopy(previous)
        self.approve_product_truth(approved)
        approved_path = self.write("direct-approved.json", json.dumps(approved))
        codes = {issue.code for issue in VALIDATOR.validate_state(approved_path, args(previous=str(previous_path))).errors}
        self.assertIn("STATE_APPROVAL_REQUIRES_PASS", codes)

    def test_product_truth_pass_cannot_start_research_before_approval(self) -> None:
        state = self.valid_state()
        state["gates"]["PRODUCT_TRUTH"] = "PASS"
        state["status"] = "RESEARCH"
        state["current_gate"] = "RESEARCH"
        path = self.write("pass-without-approval.json", json.dumps(state))
        codes = {issue.code for issue in VALIDATOR.validate_state(path, args()).errors}
        self.assertIn("STATE_PRODUCT_PASS_APPROVAL", codes)

    def test_product_truth_approval_is_bound_to_fingerprints(self) -> None:
        state = self.valid_state()
        self.approve_product_truth(state)
        state["product_truth_approval"]["course_fingerprint"] = "stale-course"
        path = self.write("stale-approval.json", json.dumps(state))
        codes = {issue.code for issue in VALIDATOR.validate_state(path, args()).errors}
        self.assertIn("STATE_PRODUCT_APPROVAL_COURSE", codes)

    def test_product_gap_allows_only_gap_report_artifact(self) -> None:
        state = self.product_gap_state()
        state["artifacts"]["landing_page_brief"] = "landing-page-brief.md"
        path = self.write("gap-artifacts.json", json.dumps(state))
        codes = {issue.code for issue in VALIDATOR.validate_state(path, args()).errors}
        self.assertIn("STATE_PRODUCT_GAP_ARTIFACT", codes)


class ClaimsValidationTests(TemporaryArtifact):
    def test_verified_claim_requires_source(self) -> None:
        text = """# Claims

| claim_id | claim | claim_type | status | evidence_type | source | used_on | notes |
|---|---|---|---|---|---|---|---|
| claim_1 | A factual claim | fact | VERIFIED | COURSE_SOURCE |  | hero |  |
"""
        path = self.write("claims.md", text)
        codes = {issue.code for issue in VALIDATOR.validate_claims(path, args()).errors}
        self.assertIn("CLAIM_SOURCE", codes)

    def test_escaped_pipe_parses(self) -> None:
        text = """# Claims

| claim_id | claim | claim_type | status | evidence_type | source | used_on | notes |
|---|---|---|---|---|---|---|---|
| claim_1 | A \\| B | fact | VERIFIED | COURSE_SOURCE | SRC-001 | hero |  |
"""
        path = self.write("escaped.md", text)
        self.assertTrue(VALIDATOR.validate_claims(path, args()).valid)


class BriefValidationTests(TemporaryArtifact):
    def base_manifest(self) -> dict:
        pages = []
        for page_id in ("registration", "thank_you", "watch", "booking", "booking_success"):
            sections = ["main"]
            if page_id == "registration":
                sections = ["hero", "course_value", "course_content", "instructors", "faq", "registration_form"]
            pages.append({
                "id": page_id,
                "path": f"/{page_id}",
                "goal": f"Goal for {page_id}",
                "primary_cta": "continue",
                "sections": sections,
                "claim_ids": [],
                "index_policy": "noindex" if page_id != "registration" else "index",
                "canonical": None if page_id != "registration" else "self",
            })
        return {
            "schema": "kstudy.funnel-brief/v1",
            "mode": "BUILD",
            "funnel_profile": "WEBINAR_BOOKING",
            "pages": pages,
            "routes": [
                {"from": "registration", "action": "submit", "to": "thank_you"},
                {"from": "thank_you", "action": "watch_webinar", "to": "watch"},
                {"from": "watch", "action": "book_consultation", "to": "booking"},
                {"from": "booking", "action": "submit", "to": "booking_success"},
            ],
            "course_explanation": {
                "page_id": "registration",
                "section_ids": {
                    "value": "course_value",
                    "curriculum": "course_content",
                    "instructors": "instructors",
                    "faq": "faq",
                },
                "language_style": {
                    "primary": "vi",
                    "plain_language": True,
                    "jargon_policy": "explain_or_replace",
                    "outcome_frame": "can_do",
                },
                "value_points": [
                    {"category": "capability", "copy": f"Tạo đầu ra công việc {index}", "claim_ids": [f"claim_value_{index}"]}
                    for index in range(1, 5)
                ],
                "modules": [{
                    "module_id": "M01",
                    "customer_title": "Tạo đầu ra đầu tiên",
                    "can_do": ["Tạo một bản tóm tắt dùng cho công việc"],
                    "hands_on_output": "Bản tóm tắt hoàn chỉnh",
                    "source_refs": ["COURSE-M01"],
                    "claim_ids": ["claim_module_1"],
                }],
                "instructors": [{
                    "name": "Giảng viên A",
                    "role_in_course": "Hướng dẫn học phần thực hành",
                    "short_bio": "Giảng viên có hồ sơ đã xác minh và kinh nghiệm phù hợp với nội dung phụ trách.",
                    "image_asset_id": "AST-INSTRUCTOR-01",
                    "source_refs": ["PROFILE-01"],
                    "claim_ids": ["claim_instructor_1"],
                }],
                "faqs": [
                    {
                        "question": f"Câu hỏi thường gặp {index}?",
                        "answer": f"Câu trả lời trực tiếp, có điều kiện và nguồn xác minh {index}.",
                        "source_refs": [f"POLICY-{index}"],
                        "claim_ids": [f"claim_faq_{index}"],
                    }
                    for index in range(1, 5)
                ],
            },
            "events": sorted(VALIDATOR.WEBINAR_EVENTS),
            "lead_routing": {
                "store_first": True,
                "idempotency_key": "lead_id",
                "async_delivery": True,
                "server_validation": True,
                "rate_limit": True,
                "retry_and_failed_delivery": True,
                "audit_log": True,
            },
            "integrity": {
                "fake_live": False,
                "fake_viewers": False,
                "fake_scarcity": False,
                "fake_countdown": False,
                "pii_in_analytics": False,
            },
            "external_actions": [{"action": "deploy", "approval_required": True}],
        }

    def make_brief(self, manifest: dict) -> str:
        headings = "\n\n".join(f"## {number}. Section {number}\n\nComplete." for number in range(1, 19))
        return f"# Brief\n\n```kstudy-funnel-manifest\n{json.dumps(manifest)}\n```\n\n{headings}\n"

    def test_valid_full_funnel_manifest(self) -> None:
        path = self.write("brief.md", self.make_brief(self.base_manifest()))
        self.assertTrue(VALIDATOR.validate_brief(path, args()).valid)

    def test_missing_booking_success_fails(self) -> None:
        manifest = self.base_manifest()
        manifest["pages"] = [page for page in manifest["pages"] if page["id"] != "booking_success"]
        path = self.write("brief-missing.md", self.make_brief(manifest))
        codes = {issue.code for issue in VALIDATOR.validate_brief(path, args()).errors}
        self.assertIn("BRIEF_REQUIRED_PAGES", codes)

    def test_missing_course_explanation_fails(self) -> None:
        manifest = self.base_manifest()
        del manifest["course_explanation"]
        path = self.write("brief-no-course-explanation.md", self.make_brief(manifest))
        codes = {issue.code for issue in VALIDATOR.validate_brief(path, args()).errors}
        self.assertIn("BRIEF_COURSE_EXPLANATION", codes)

    def test_course_explanation_section_must_exist_on_page(self) -> None:
        manifest = self.base_manifest()
        manifest["pages"][0]["sections"].remove("course_content")
        path = self.write("brief-no-course-content-section.md", self.make_brief(manifest))
        codes = {issue.code for issue in VALIDATOR.validate_brief(path, args()).errors}
        self.assertIn("BRIEF_COURSE_SECTION_MISSING", codes)

    def test_course_module_vague_outcome_warns(self) -> None:
        manifest = self.base_manifest()
        manifest["course_explanation"]["modules"][0]["can_do"] = ["Hiểu tổng quan về AI"]
        path = self.write("brief-vague-outcome.md", self.make_brief(manifest))
        report = VALIDATOR.validate_brief(path, args())
        codes = {issue.code for issue in report.warnings}
        self.assertIn("BRIEF_COURSE_MODULE_VAGUE", codes)

    def test_course_faq_requires_at_least_four_items(self) -> None:
        manifest = self.base_manifest()
        manifest["course_explanation"]["faqs"] = manifest["course_explanation"]["faqs"][:3]
        path = self.write("brief-three-faqs.md", self.make_brief(manifest))
        codes = {issue.code for issue in VALIDATOR.validate_brief(path, args()).errors}
        self.assertIn("BRIEF_COURSE_FAQS", codes)

    def test_nested_course_claim_ids_are_cross_checked(self) -> None:
        manifest = self.base_manifest()
        path = self.write("brief-nested-claims.md", self.make_brief(manifest))
        claims = """# Claims

| claim_id | claim | claim_type | status | evidence_type | source | used_on | notes |
|---|---|---|---|---|---|---|---|
| claim_value_1 | One verified value | outcome | VERIFIED | COURSE_SOURCE | SRC-001 | course_value |  |
"""
        claims_path = self.write("claims.md", claims)
        codes = {
            issue.code
            for issue in VALIDATOR.validate_brief(path, args(claims=str(claims_path))).errors
        }
        self.assertIn("BRIEF_CLAIM_MISSING", codes)

    def test_external_send_requires_approval(self) -> None:
        manifest = self.base_manifest()
        manifest["external_actions"] = [{"action": "send_sms", "approval_required": False}]
        path = self.write("brief-approval.md", self.make_brief(manifest))
        codes = {issue.code for issue in VALIDATOR.validate_brief(path, args()).errors}
        self.assertIn("BRIEF_EXTERNAL_APPROVAL", codes)

    def test_lead_capture_profile_does_not_require_webinar_pages(self) -> None:
        manifest = self.base_manifest()
        manifest["funnel_profile"] = "LEAD_CAPTURE"
        manifest["pages"] = [page for page in manifest["pages"] if page["id"] in {"registration", "thank_you"}]
        manifest["routes"] = [{"from": "registration", "action": "submit", "to": "thank_you"}]
        manifest["events"] = ["course_view", "cta_click", "form_start", "lead_submitted"]
        path = self.write("brief-lead.md", self.make_brief(manifest))
        self.assertTrue(VALIDATOR.validate_brief(path, args()).valid)

    def test_custom_profile_requires_explicit_contract(self) -> None:
        manifest = self.base_manifest()
        manifest["funnel_profile"] = "CUSTOM"
        path = self.write("brief-custom.md", self.make_brief(manifest))
        codes = {issue.code for issue in VALIDATOR.validate_brief(path, args()).errors}
        self.assertIn("BRIEF_CUSTOM_PAGES", codes)
        self.assertIn("BRIEF_CUSTOM_EVENTS", codes)


if __name__ == "__main__":
    unittest.main(verbosity=2)
