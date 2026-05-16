---
obsidianUIMode: preview
description: DClaw Meet — Project Homepage Vault
---

# DClaw Meet — Obsidian Vault

> **Last updated:** 2026-05-16  
> **Version:** v1.2  
> **Status:** Active Development

---

## Quick Links

| Area | Path | Purpose |
|---|---|---|
| [[Notes/Development Log]] | `Notes/` | Daily dev notes, decisions, blockers |
| [[Notes/Architecture Decision Records]] | `Notes/` | Key architectural decisions |
| [[Notes/YC Submission Draft]] | `Notes/` | Y Combinator application materials |
| [[Projects/v1.2 Roadmap]] | `Projects/` | Feature roadmap & sprint tracking |
| [[Projects/Data Model]] | `Projects/` | Entity diagrams & schema notes |
| [[Daily/]] | `Daily/` | Standup notes, retro entries |
| [[Templates/]] | `Templates/` | Reusable note templates |
| [[Archive/]] | `Archive/` | Completed sprints, retired decisions |

---

## Project Identity

| Field | Value |
|---|---|
| **App Name** | DClaw Meet |
| **Category** | AI-Powered Video Conferencing |
| **Backend Port** | 8018 (FastAPI + SQLAlchemy 2.0) |
| **Frontend Port** | 3018 (Next.js 14 + Tailwind) |
| **Database** | dclaw_meet (PostgreSQL) |
| **Base API** | /api/v1 |

---

## Active Sprint

**Sprint 1 — Foundation (Complexity 0)**
- [x] Fix config drift (ports, DB name)
- [x] Meeting domain models (User, Room, Meeting, Participant, TranscriptSegment, ActionItem)
- [x] Pydantic schemas + repositories
- [x] CRUD routers wired in main.py
- [x] 20 backend tests passing
- [x] Frontend dashboard + meetings + rooms pages
- [x] npm run build passes

---

## Key Documents

- `PLAN-v1.2.md` — Strategic roadmap with YC gap analysis
- `AGENTS.md` — Architecture lock & anti-patterns
- `PRODUCT-SPEC.md` — Meeting domain specification
- `SCALING-PLAYBOOK.md` — Parallel agent workflow

---

## Graph Index

```dataview
TABLE file.mtime as "Modified", file.folder as "Folder"
FROM ""
SORT file.mtime DESC
LIMIT 50
```

---

## Tag Index

- #todo — Open tasks
- #decision — Architectural decisions
- #blocker — Active blockers
- #sprint — Sprint artifacts
- #feature — Feature notes
- #meeting — Meeting notes
- #ai — AI-related notes
