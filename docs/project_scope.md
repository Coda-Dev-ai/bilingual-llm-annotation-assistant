# Project Scope

## Problem Statement

Companies that receive customer feedback or support requests in both English and French often need consistent annotation before they can triage, analyze, or escalate incoming messages. 
Manual review is slow and expensive, while naive automation can misclassify culturally nuanced, ambiguous, or mixed-language content. 
This project solves that gap by building a bilingual annotation workflow that combines LLM-based labeling with strict output validation and human-review routing. The system is intended to improve consistency, preserve auditability, and reduce the amount of low-risk manual labeling work. 
The local MVP is focused on correctness, schema reliability, and review workflow design rather than production-scale deployment.

## User Flow

1. A user uploads a CSV or JSON file containing support tickets, feedback messages, or reviews.
2. The system validates the input schema and rejects malformed rows before annotation starts.
3. Each record is cleaned, normalized, and assigned a language tag if one is missing.
4. The LLM receives the text, language, allowed labels, and output schema instructions.
5. The model returns structured labels for issue type, sentiment, urgency, summary, and review status.
6. A validation layer checks JSON structure, allowed values, and fallback/retry rules.
7. High-confidence valid records are stored as auto-accepted annotations.
8. Low-confidence, mixed-language, invalid, or culturally ambiguous records are routed to the human review queue.
9. Review outcomes and final annotations are stored for audit and evaluation.
10. Metrics are computed to measure quality by label type and by language.

## Accepted Labels

### issue_type
- billing
- shipping
- product_quality
- account_access
- refund
- technical_issue
- general_inquiry

### sentiment
- positive
- neutral
- negative

### urgency
- low
- medium
- high

### needs_human_review
- true
- false

### review_reason
- ambiguity
- mixed_language
- policy_sensitive
- low_confidence
- cultural_nuance_risk
- invalid_json
- unsupported_label

## Out of Scope

The following items are out of scope for the local MVP:
- production cloud deployment
- user authentication and role-based access control
- real-time streaming ingestion
- background workers and distributed job queues
- support for languages beyond English and French
- advanced reviewer assignment workflows
- full prompt experimentation UI
- model fine-tuning
- enterprise-grade monitoring, alerting, and SSO
- integrations with external helpdesk platforms
