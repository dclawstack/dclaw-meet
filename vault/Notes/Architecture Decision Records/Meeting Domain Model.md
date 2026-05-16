---
date: 2026-05-16
tags: [decision, domain]
---

# ADR-002: Meeting Domain Data Model

## Status
- [x] Accepted

## Context
The repository shipped with a CRM `PRODUCT-SPEC.md` despite being named `dclaw-meet` and targeting video conferencing. This was a scaffold template leakage.

## Decision
Replace all CRM entities with a meeting domain: User → Room → Meeting → Participant → TranscriptSegment → ActionItem. Each entity has a clear purpose in the meeting lifecycle.

## Consequences
- **Easier:** Aligned domain with product name and YC pitch.
- **Harder:** All existing mock endpoints and test files needed replacement.
- **Trade-off:** No CRM features; future CRM app would be a separate repository (`dclaw-crm`).
