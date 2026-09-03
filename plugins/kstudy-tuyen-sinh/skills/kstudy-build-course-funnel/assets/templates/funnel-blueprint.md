# Funnel Blueprint

## Funnel contract

- Workflow/funnel ID: `{{funnel_id}}`
- Course track: `{{course_track}}`
- Audience: {{audience}}
- Source: {{source}}
- Selected journey: `{{journey_id}}`
- Primary conversion: {{primary_conversion}}
- Build boundary: local/integration-ready unless external action is separately approved.

## Experience map

```text
{{organic_content}}
  -> {{registration_page}}
  -> {{lead_store}}
  -> {{thank_you_page}}
  -> {{watch_page}}
  -> {{booking_page}}
  -> {{booking_success}}
  -> {{human_consultation_or_next_step}}
```

## Node definitions

| node_id | route/channel | audience state | entry promise | primary CTA | data/consent | success route | failure/fallback | owner/tool | event | approval |
|---|---|---|---|---|---|---|---|---|---|---|
| registration | `/{{registration_path}}` | {{state}} | {{promise}} | {{cta}} | {{fields_and_consent}} | thank_you | {{fallback}} | {{owner_tool}} | webinar_registered | {{approval}} |
| thank_you | `/{{thank_you_path}}` | registered | {{promise}} | {{cta}} | none | watch | {{fallback}} | web | cta_click | none |
| watch | `/{{watch_path}}` | watching | {{promise}} | book consultation | {{access_data}} | booking | {{fallback}} | {{video_tool}} | webinar_progress_* | {{approval}} |
| booking | `/{{booking_path}}` | high intent | {{promise}} | confirm booking | {{fields_and_consent}} | booking_success | {{fallback}} | {{booking_tool}} | consultation_booked | {{approval}} |
| booking_success | `/{{success_path}}` | booked | {{expectation}} | {{secondary_cta}} | none | {{next}} | {{fallback}} | web | course_view | none |

## Lead routing

- Source of truth: {{durable_lead_store}}
- Lead ID/idempotency: `lead_id`
- Store-first: yes
- Async delivery: yes
- Downstream orchestrator: {{n8n_or_other}}
- Retry/backoff: {{policy}}
- Failed delivery/dead letter: {{policy}}
- Audit log owner: {{owner}}
- Qualification owner/SLA: {{owner_and_sla}}
- AI Mentor handoff rule: {{explicit_rule_or_not_used}}

## Post-conversion branches

| Trigger | Branch | Purpose | Owner | Tool | Consent | Stop rule | Error handling | Approval |
|---|---|---|---|---|---|---|---|---|
| {{trigger}} | {{email_sms_zalo_telesale_group_zoom}} | {{purpose}} | {{owner}} | {{tool}} | {{consent}} | {{stop_rule}} | {{error}} | REQUIRED/NOT_REQUIRED |

## Error and edge states

- Form validation: {{behavior}}
- Duplicate submission: {{behavior}}
- Lead stored, downstream failed: {{behavior}}
- Invalid/expired access: {{behavior}}
- Video unavailable: {{behavior}}
- Booking provider unavailable: {{behavior}}
- No slots/timezone mismatch: {{behavior}}
- Tracking/consent unavailable: {{behavior}}

## Pending decisions

- {{decision}}
