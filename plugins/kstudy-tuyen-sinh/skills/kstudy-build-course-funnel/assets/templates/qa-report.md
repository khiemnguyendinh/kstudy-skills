# Funnel QA Report

## Summary

- Workflow/funnel ID: `{{funnel_id}}`
- Mode/environment: {{mode_environment}}
- Build status: BUILD_READY/CONNECTED/READY_FOR_PUBLISH/PUBLISHED
- Overall: PASS/FAIL/BLOCKED
- Tested at: {{timestamp}}
- Pending external actions: {{actions_or_none}}

## Gate results

| gate | status | evidence | blocker/owner |
|---|---|---|---|
| Product Truth | PASS/FAIL | {{evidence}} | {{blocker}} |
| Claims | PASS/FAIL | {{validator_output}} | {{blocker}} |
| Brief | PASS/FAIL | {{validator_output}} | {{blocker}} |
| Course explanation | PASS/FAIL | {{value_modules_instructors_faq_evidence}} | {{blocker}} |
| Functional funnel | PASS/FAIL | {{test_evidence}} | {{blocker}} |
| Accessibility | PASS/FAIL | {{evidence}} | {{blocker}} |
| Performance | PASS/FAIL | {{evidence}} | {{blocker}} |
| Tracking/privacy | PASS/FAIL | {{evidence}} | {{blocker}} |
| SEO/GEO/AEO | PASS/FAIL | {{evidence}} | {{blocker}} |

## Route and state QA

| page/state | desktop | mobile | keyboard | tracking | error/fallback | result |
|---|---|---|---|---|---|---|
| registration | {{result}} | {{result}} | {{result}} | {{result}} | {{result}} | PASS/FAIL |
| thank_you | {{result}} | {{result}} | {{result}} | {{result}} | {{result}} | PASS/FAIL |
| watch | {{result}} | {{result}} | {{result}} | {{result}} | {{result}} | PASS/FAIL |
| booking | {{result}} | {{result}} | {{result}} | {{result}} | {{result}} | PASS/FAIL |
| booking_success | {{result}} | {{result}} | {{result}} | {{result}} | {{result}} | PASS/FAIL |

## Tracking verification

{{event_payload_dedupe_consent_destination_evidence}}

## Course explanation QA

| block | source coverage | plain language | mobile presentation | result |
|---|---|---|---|---|
| Sau khóa học làm được gì | {{result}} | {{result}} | {{result}} | PASS/FAIL |
| Nội dung từng học phần | {{result}} | {{result}} | {{result}} | PASS/FAIL |
| Giảng viên và ảnh | {{result}} | {{result}} | {{result}} | PASS/FAIL |
| FAQ | {{result}} | {{result}} | {{result}} | PASS/FAIL |

## Known limitations and decisions

- {{limitation}}

## Release decision

- Decision: {{decision}}
- Required approvals: {{approvals}}
- Rollback/fallback: {{rollback}}
