# Landing Page and Funnel Build Brief

```kstudy-funnel-manifest
{
  "schema": "kstudy.funnel-brief/v1",
  "mode": "BUILD",
  "funnel_profile": "WEBINAR_BOOKING",
  "funnel_id": "{{funnel_id}}",
  "course_track": "{{course_track}}",
  "audience": "{{audience}}",
  "source": "{{source}}",
  "selected_journey": "{{journey_id}}",
  "pages": [
    {
      "id": "registration",
      "path": "/{{registration_path}}",
      "goal": "{{goal}}",
      "primary_cta": "register_webinar",
      "sections": ["hero", "course_value", "course_content", "mechanism", "proof", "instructors", "faq", "agenda", "registration_form"],
      "claim_ids": [],
      "index_policy": "index",
      "canonical": "self"
    },
    {
      "id": "thank_you",
      "path": "/{{thank_you_path}}",
      "goal": "{{goal}}",
      "primary_cta": "watch_webinar",
      "sections": ["confirmation", "access", "expectation", "support"],
      "claim_ids": [],
      "index_policy": "noindex",
      "canonical": null
    },
    {
      "id": "watch",
      "path": "/{{watch_path}}",
      "goal": "{{goal}}",
      "primary_cta": "book_consultation",
      "sections": ["video", "agenda", "contextual_proof", "consultation_cta", "support"],
      "claim_ids": [],
      "index_policy": "noindex",
      "canonical": null
    },
    {
      "id": "booking",
      "path": "/{{booking_path}}",
      "goal": "{{goal}}",
      "primary_cta": "confirm_booking",
      "sections": ["value", "qualification", "scheduler", "privacy", "support"],
      "claim_ids": [],
      "index_policy": "noindex",
      "canonical": null
    },
    {
      "id": "booking_success",
      "path": "/{{booking_success_path}}",
      "goal": "{{goal}}",
      "primary_cta": "review_next_steps",
      "sections": ["confirmation", "next_steps", "reschedule", "support"],
      "claim_ids": [],
      "index_policy": "noindex",
      "canonical": null
    }
  ],
  "routes": [
    {"from": "registration", "action": "submit", "to": "thank_you"},
    {"from": "thank_you", "action": "watch_webinar", "to": "watch"},
    {"from": "watch", "action": "book_consultation", "to": "booking"},
    {"from": "booking", "action": "submit", "to": "booking_success"}
  ],
  "course_explanation": {
    "page_id": "registration",
    "section_ids": {
      "value": "course_value",
      "curriculum": "course_content",
      "instructors": "instructors",
      "faq": "faq"
    },
    "language_style": {
      "primary": "vi",
      "plain_language": true,
      "jargon_policy": "explain_or_replace",
      "outcome_frame": "can_do"
    },
    "value_points": [
      {
        "category": "capability",
        "copy": "{{value_point_written_as_a_concrete_action}}",
        "claim_ids": ["{{claim_id}}"]
      }
    ],
    "modules": [
      {
        "module_id": "{{module_id}}",
        "customer_title": "{{plain_language_module_title}}",
        "can_do": ["{{after_this_module_you_can_do}}"],
        "hands_on_output": "{{artifact_or_completed_work_task}}",
        "source_refs": ["{{course_or_lesson_source_ref}}"],
        "claim_ids": ["{{claim_id}}"]
      }
    ],
    "instructors": [
      {
        "name": "{{verified_instructor_name}}",
        "role_in_course": "{{teaching_role}}",
        "short_bio": "{{short_relevant_verified_bio}}",
        "image_asset_id": "{{approved_instructor_image_asset_id}}",
        "source_refs": ["{{verified_profile_source_ref}}"],
        "claim_ids": ["{{claim_id}}"]
      }
    ],
    "faqs": [
      {
        "question": "{{real_customer_question}}",
        "answer": "{{plain_direct_verified_answer}}",
        "source_refs": ["{{course_policy_or_research_source_ref}}"],
        "claim_ids": ["{{claim_id}}"]
      }
    ]
  },
  "events": [
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
    "consultation_booked"
  ],
  "lead_routing": {
    "store_first": true,
    "idempotency_key": "lead_id",
    "async_delivery": true,
    "server_validation": true,
    "rate_limit": true,
    "retry_and_failed_delivery": true,
    "audit_log": true
  },
  "integrity": {
    "fake_live": false,
    "fake_viewers": false,
    "fake_scarcity": false,
    "fake_countdown": false,
    "pii_in_analytics": false
  },
  "external_actions": [
    {"action": "deploy", "status": "PENDING", "approval_required": true},
    {"action": "send_or_publish", "status": "PENDING", "approval_required": true}
  ]
}
```

## 1. Goal and scope

- Business goal: {{business_goal}}
- Audience/source: {{audience_and_source}}
- Primary/secondary conversion: {{conversion}}
- In scope: {{scope}}
- Out of scope: {{out_of_scope}}

## 2. Product truth and evidence

- Approved course source/version: {{source}}
- Audience–outcome alignment: {{alignment}}
- Claims ledger: `{{claims_ledger_path}}`
- Prohibited/unverified claims: {{claims_not_to_use}}

## 3. Audience and message continuity

- Awareness/JTBD: {{awareness_jtbd}}
- Source/post/content angle/variant: {{continuity}}
- Message hierarchy: {{problem_desired_progress_mechanism_proof_offer}}
- Primary objections: {{objections}}

## 4. Experience map and page roles

{{registration_to_booking_experience}}

## 5. Registration page section specifications

For every section specify: objective, heading, paragraph/microcopy/link hierarchy, `claim_id`, proof, visual/video/form/CTA, layout, responsive behavior, interaction, tracking and next route.

### Section REG-01 — Hero

- Psychological objective: {{objective}}
- H1/eyebrow/body: {{copy_hierarchy}}
- CTA/microcopy: {{cta}}
- Claim IDs: {{claim_ids}}
- Visual/layout: {{visual}}
- Responsive/interaction: {{behavior}}
- Event/route: {{event_route}}

### Section REG-02 — Sau khóa học bạn làm được gì

- One-sentence course description: {{what_the_course_helps_the_customer_do}}
- 4–7 capability/application/support bullets: {{value_points}}
- Claim IDs and proof: {{claim_ids_and_sources}}
- CTA and verified learning rights: {{cta_and_rights}}
- Visual/layout/responsive/tracking: {{section_contract}}

### Section REG-03 — Nội dung khóa học: sau mỗi học phần bạn tự làm được gì

For every approved module include: `module_id`, customer-facing title, 1–4 `can_do` outcomes, hands-on output, source refs and claim IDs.

{{all_modules_in_plain_customer_language}}

### Section REG-04 — Giảng viên

For every instructor include: verified name, course role, relevant short bio, approved image asset, source refs and claim IDs. Specify desktop image-and-copy layout and mobile order.

{{all_verified_instructors}}

### Section REG-05 — Câu hỏi thường gặp

Include at least four real objections with direct, plain-language answers. Cover prerequisites, fit, time/tools/support/access or policy only when relevant and verified.

{{verified_faqs}}

### Section REG-06+ — {{section_name}}

{{repeat_contract_for_every_section}}

## 6. Thank-you page section specifications

{{confirmation_access_expectation_support_sections}}

## 7. Watch page and webinar specifications

- Webinar disclosure: clearly on-demand/recorded.
- Video objective, hook, teaching beats, proof, objections and CTA: {{video_contract}}
- Caption/transcript/thumbnail: {{media_accessibility}}
- CTA reveal/persistence rule: {{rule}}
- Video loading/error/recovery: {{states}}
- Progress events: {{events}}

## 8. Booking and success specifications

{{booking_value_qualification_scheduler_privacy_reschedule_success_error}}

## 9. Forms, data, consent and lead routing

{{fields_validation_consent_store_first_idempotency_async_delivery_retry_audit}}

## 10. External interactions and routing

{{email_sms_zalo_telesale_group_zoom_upsell_downsell_if_approved}}

## 11. Tracking and attribution

- Tracking plan: `{{tracking_plan_path}}`
- Internal events/vendor mappings/dedupe: {{tracking_summary}}
- Attribution fields: `source`, `post_id`, `content_angle`, `content_format`, `landing_variant`.
- PII exclusion/consent: {{privacy}}

## 12. SEO, GEO and AEO

{{index_policy_canonical_metadata_heading_schema_entity_faq_transcript_internal_links}}

## 13. Visual and design direction

- UX direction: {{ux_direction}}
- Kstudy tokens/assets: {{brand_contract}}
- Visual style: {{visual_style}}
- Required sections: {{required_sections}}
- Anti-patterns: fake data, generic dashboard cards, decorative gradients without purpose, unverified stock-as-proof.

## 14. Accessibility and performance

{{semantic_html_keyboard_focus_contrast_labels_errors_reduced_motion_media_performance}}

## 15. Error and edge states

{{loading_empty_validation_duplicate_expired_video_failure_booking_failure_downstream_failure}}

## 16. Asset manifest

Reference `{{asset_manifest_path}}`. Every asset needs owner, status, source/license, placement, format/dimensions, alt/caption and fallback.

## 17. Acceptance criteria

- Product Truth, Strategy, Claims and Brief gates are APPROVED.
- All manifest routes and states work locally.
- Claims validator and brief validator PASS.
- Course value, every in-scope module, instructor block and at least four verified FAQs are complete.
- Module copy says what the learner can do; it is not only a list of topics or specialist terms.
- Mobile, accessibility, functional, tracking, privacy and SEO QA have no blocker.
- External writes remain pending until separately approved.

## 18. Unresolved decisions

- {{decision_or_none}}
