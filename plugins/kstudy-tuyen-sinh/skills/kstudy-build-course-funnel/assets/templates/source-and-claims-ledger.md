# Source and Claims Ledger

## Sources

| source_id | type | title | owner_or_org | date | location | accessed_at | status | supports | limitation |
|---|---|---|---|---|---|---|---|---|---|
| SRC-001 | COURSE_SOURCE | {{title}} | Kstudy | {{date_or_unknown}} | {{path_or_url}} | {{date}} | VERIFIED | {{supports}} | {{limitation}} |

## Claims

| claim_id | claim | claim_type | status | evidence_type | source | used_on | notes |
|---|---|---|---|---|---|---|---|
| claim_001 | {{claim_text}} | fact | PROPOSED | COURSE_SOURCE | SRC-001 |  | {{notes}} |

Use separate claim rows for course value, each module outcome, instructor credential, learning support/right and policy answer used in FAQ.

Allowed `claim_type`: `fact`, `outcome`, `instructor`, `policy`, `support`, `testimonial`, `social_proof`, `urgency`, `price`, `compliance`.

Allowed `status`: `VERIFIED`, `INFERRED`, `PROPOSED`, `UNKNOWN`, `REJECTED`.

Only `VERIFIED` claims may be used in approved public copy.
