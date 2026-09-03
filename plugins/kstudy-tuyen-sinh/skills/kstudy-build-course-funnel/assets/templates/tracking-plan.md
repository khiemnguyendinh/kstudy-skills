# Tracking and Attribution Plan

## Measurement contract

- Funnel ID/course track: `{{funnel_id}}` / `{{course_track}}`
- Primary conversion: {{primary_conversion}}
- Source of truth: {{source_of_truth}}
- Consent model: {{consent_model}}
- Environments: {{environments}}

## Attribution dimensions

| dimension | source | allowed values/normalization | persistence | PII risk |
|---|---|---|---|---|
| source | URL/content link | {{values}} | first-party/session policy | none |
| post_id | Fanpage content record | {{values}} | {{policy}} | none |
| content_angle | content taxonomy | {{values}} | {{policy}} | none |
| content_format | content taxonomy | {{values}} | {{policy}} | none |
| landing_variant | app config | {{values}} | {{policy}} | none |

## Event dictionary and vendor mapping

| internal_event | trigger/source-of-truth | required properties | GA4 mapping | Meta/TikTok mapping | browser/server | event_id/dedupe | consent | QA status |
|---|---|---|---|---|---|---|---|---|
| lead_submitted | durable lead store success | funnel_id, course_track, source, variant | generate_lead | {{mapping_or_not_used}} | server | lead event_id | {{rule}} | PENDING |
| webinar_registered | registration business rule success | funnel_id, source, variant | {{mapping}} | {{mapping}} | server | registration event_id | {{rule}} | PENDING |
| webinar_watch_started | actual playback | funnel_id, page_id | {{mapping}} | {{mapping}} | browser | playback event_id | {{rule}} | PENDING |
| webinar_progress_25/50/75 | unique milestone reached | funnel_id, milestone | {{mapping}} | {{mapping}} | browser | session+milestone | {{rule}} | PENDING |
| webinar_completed | completion rule reached | funnel_id | {{mapping}} | {{mapping}} | browser/server | completion event_id | {{rule}} | PENDING |
| consultation_booked | booking provider/server confirms | funnel_id, booking_source | {{mapping}} | {{mapping}} | server | booking event_id | {{rule}} | PENDING |
| lead_qualified | approved qualification source | funnel_id, rule_version | qualify_lead or custom | {{mapping}} | server | lead_id+state | {{rule}} | RESERVED/IMPLEMENTED/PENDING |
| enrollment_paid | payment source confirms | funnel_id, currency/value if permitted | purchase | {{mapping}} | server | transaction ID | {{rule}} | RESERVED/IMPLEMENTED/PENDING |

Also define: `course_view`, `cta_click`, `video_start`, `video_progress`, `form_start`, `webinar_cta_viewed`, `webinar_cta_clicked`.

## Data quality and privacy

- No PII in URL/UTM/GA4/data layer/client log.
- Event naming/versioning: {{policy}}
- Retry/late event handling: {{policy}}
- Bot/internal traffic: {{policy}}
- Timezone/currency: {{policy}}
- Retention/access owner: {{owner}}

## Verification evidence

| environment | event | method/tool | expected | observed | status | verified_at | owner |
|---|---|---|---|---|---|---|---|
| {{environment}} | {{event}} | {{method}} | {{expected}} | {{observed}} | PENDING/PASS/FAIL | {{date}} | {{owner}} |

Do not mark production verified from code inspection or staging evidence alone.
