# DClaw Meet — Strategic Product Plan v1.2

> YC-Grade Gap Analysis & Autonomous Development Roadmap  
> Generated: 2026-05-16  
> Based on: `AGENTS.md` architecture audit, scaffold state analysis, YC standards

---

## Part 1: YC Gap Analysis

### The "Hair-on-Fire" Problem
Remote and hybrid teams waste **31% of meeting time** on coordination, note-taking, and follow-up. Existing tools (Zoom, Teams, Google Meet) are "dumb pipes" — they connect people but do nothing to ensure meetings produce outcomes. Post-meeting, action items are lost in Slack threads, decisions are forgotten, and nobody reviews recordings because transcripts are walls of text.

**DClaw Meet** solves this by being an **AI-native meeting platform** where every meeting automatically generates actionable outcomes.

### Current Scaffold Gaps vs. YC Submission Standard

| YC Criteria | Current State | Gap Severity | Fix Priority |
|---|---|---|---|
| Clear problem statement | Feature list only; no problem framing | 🔴 High | P0 |
| Technical moat | WebRTC commodity; no AI differentiation yet | 🔴 High | P0 |
| Viral growth loop | No invite/sharing mechanism | 🔴 High | P1 |
| Revenue model | None defined | 🟡 High | P1 |
| Real working product | Mock endpoints, no DB, no migrations | 🔴 **Critical** | P0 |
| Scalability story | Basic scaffold, no auth/tenancy | 🟡 Medium | P1 |
| Team execution speed | Scaffold incomplete (wrong ports, wrong spec) | 🔴 **Critical** | P0 |

### Critical Finding: `PRODUCT-SPEC.md` Mismatch
The repository currently ships with a **CRM Product Spec** (Customers, Deals, Activities) despite being named `dclaw-meet` and targeting video conferencing. This is a template leakage and must be corrected before any domain development.

### Competitive Differentiation Strategy
Instead of competing with Zoom on video quality, DClaw Meet competes on **meeting outcomes**:

1. **Pre-meeting:** AI-generated agenda based on attendee roles + past meeting context
2. **During meeting:** Real-time transcription with auto-highlighted decisions and action items
3. **Post-meeting:** Instant shareable recap with linked action items, auto-scheduled follow-ups, and searchable transcript archive

This is the "AI-native" angle that makes YC reviewers lean forward.

---

## Part 2: Prioritized Feature Roadmap

### Complexity 0 — Foundation Fixes (Week 1)
These unblock all other work. No feature development until these are complete.

| # | Feature | Description | Rationale |
|---|---|---|---|
| **0.1** | Fix config drift | Ports `8018`/`3018`, DB `dclaw_meet`, Dockerfile `ENV` | `AGENTS.md` spec mismatch |
| **0.2** | Correct `PRODUCT-SPEC.md` | Rewrite from CRM → Meeting domain spec | Critical template leakage |
| **0.3** | Meeting domain models | `Room`, `Meeting`, `Participant`, `TranscriptSegment`, `ActionItem` | Core entities for Meet app |
| **0.4** | Pydantic schemas + repos | Full CRUD with `BaseRepository` pattern | No more mock dicts |
| **0.5** | Real API routers | Wire `/api/v1/meetings`, `/api/v1/rooms` in `main.py` | Working endpoints |
| **0.6** | Alembic initial migration | Schema version control | Required by `AGENTS.md` |
| **0.7** | Backend test suite | 70%+ coverage on all endpoints | CI gate |
| **0.8** | Frontend API client | Typed fetch wrapper for all endpoints | Frontend-backend contract |
| **0.9** | Dashboard shell | Next.js page with navigation shell | User entry point |
| **0.10** | Docker compose verification | `docker compose up -d` healthy for all services | Deployment readiness |

### Complexity 1 — Core Differentiators (Week 2–3)

| # | Feature | Description | YC Angle |
|---|---|---|---|
| **1.1** | AI Meeting Summary | LLM-powered post-meeting summary with decisions & action items extract | Immediate visible value |
| **1.2** | Smart Scheduling Engine | Find optimal times across participant calendars | Reduces scheduling friction |
| **1.3** | Meeting Room System | Persistent rooms with settings, waiting rooms, host controls | Replaces Zoom links |
| **1.4** | Recording & Transcript Archive | Cloud recording with searchable transcripts | Long-term knowledge retention |
| **1.5** | Action Item Tracker | Extract tasks from meetings, assign owners, due dates | **Outcome guarantee** |
| **1.6** | Calendar Integration (Google/Outlook) | OAuth-based calendar read/write | Workflow embedding |

### Complexity 2 — Advanced Platform (Week 4–6)

| # | Feature | Description | Moat Factor |
|---|---|---|---|
| **2.1** | Real-time AI Copilot | In-meeting sidebar with live transcript, contextual Q&A, decision capture | Active AI differentiator |
| **2.2** | Real-time Translation | Live captioning in 20+ languages | Global team enabler |
| **2.3** | Meeting Analytics Dashboard | Talk-time distribution, engagement heatmaps, sentiment trends | Data moat (network effect) |
| **2.4** | Breakout Rooms | Host-controlled sub-rooms with broadcast | Enterprise sales feature |
| **2.5** | E2EE & Compliance | End-to-end encryption, SOC 2 readiness architecture | Enterprise trust signal |

---

## Part 3: Data Model — Meeting Domain (v1.2)

```
User
├── id: UUID (PK)
├── email: str (unique, required)
├── full_name: str (required)
├── avatar_url: str (optional)
├── created_at: datetime
└── updated_at: datetime

Room
├── id: UUID (PK)
├── name: str (required)
├── slug: str (unique, required) — e.g. "weekly-standup"
├── host_id: UUID (FK → User)
├── settings: JSON — waiting_room, recording_enabled, max_participants
├── created_at: datetime
└── updated_at: datetime

Meeting
├── id: UUID (PK)
├── room_id: UUID (FK → Room)
├── title: str (required)
├── scheduled_start: datetime (optional)
├── scheduled_end: datetime (optional)
├── status: enum ["scheduled", "live", "ended", "cancelled"]
├── recording_url: str (optional)
├── summary: str (optional) — AI-generated
├── created_at: datetime
└── updated_at: datetime

Participant
├── id: UUID (PK)
├── meeting_id: UUID (FK → Meeting, ondelete=CASCADE)
├── user_id: UUID (FK → User, ondelete=SET NULL)
├── email: str (required) — for guests without accounts
├── role: enum ["host", "co_host", "participant", "viewer"]
├── joined_at: datetime (optional)
├── left_at: datetime (optional)
├── created_at: datetime
└── updated_at: datetime

TranscriptSegment
├── id: UUID (PK)
├── meeting_id: UUID (FK → Meeting, ondelete=CASCADE)
├── participant_id: UUID (FK → Participant, ondelete=SET NULL)
├── start_time: float — seconds from meeting start
├── end_time: float
├── text: str (required)
├── is_highlight: bool (default false) — AI-marked decision moment
├── created_at: datetime

ActionItem
├── id: UUID (PK)
├── meeting_id: UUID (FK → Meeting, ondelete=CASCADE)
├── assignee_id: UUID (FK → User, ondelete=SET NULL)
├── description: str (required)
├── due_date: date (optional)
├── status: enum ["open", "in_progress", "done", "cancelled"]
├── created_at: datetime
└── updated_at: datetime
```

---

## Part 4: Implementation Sprints

### Sprint 1 (Days 1–3): Complexity 0 — Foundation
- [ ] Fix all config drift (ports, DB name, env vars)
- [ ] Rewrite `PRODUCT-SPEC.md` to Meeting domain
- [ ] Build core domain models: `User`, `Room`, `Meeting`, `Participant`, `TranscriptSegment`, `ActionItem`
- [ ] Create Pydantic schemas with `ConfigDict(from_attributes=True)`
- [ ] Create repositories extending `BaseRepository`
- [ ] Create CRUD routers in `app/api/v1/`
- [ ] Wire routers in `app/api/main.py`
- [ ] Generate initial alembic migration
- [ ] Write `pytest` suite (70%+ coverage)
- [ ] Commit: `feat(foundation): meeting domain CRUD + config fix`

### Sprint 2 (Days 4–6): Complexity 0 — Frontend Shell
- [ ] Build typed API client in `src/lib/api.ts`
- [ ] Create dashboard layout with sidebar navigation
- [ ] Create meetings list page (`/meetings`)
- [ ] Create meeting detail page (`/meetings/[id]`)
- [ ] Create room management page (`/rooms`)
- [ ] Commit: `feat(frontend): dashboard shell + meeting pages`

### Sprint 3 (Days 7–10): Complexity 1 — AI Summary + Rooms
- [ ] Integrate LLM service for meeting summaries (`app/services/ai_summary.py`)
- [ ] Build persistent room system with settings
- [ ] Create room scheduling flow
- [ ] Commit: `feat(ai): meeting summaries + room system`

### Sprint 4 (Days 11–14): Complexity 1 — Recording + Action Items
- [ ] Recording metadata storage + transcript indexing
- [ ] Action item extraction & tracker UI
- [ ] Commit: `feat(recording): cloud recording + action items`

### Sprint 5 (Days 15–21): Complexity 2 — Advanced AI + Analytics
- [ ] Real-time copilot sidebar architecture
- [ ] Analytics dashboard foundation
- [ ] Translation layer architecture
- [ ] Commit: `feat(platform): ai copilot + analytics`

---

## Part 5: API Contract (v1.2)

```
GET    /api/v1/rooms              → List rooms
POST   /api/v1/rooms              → Create room
GET    /api/v1/rooms/{id}         → Get room
PUT    /api/v1/rooms/{id}         → Update room
DELETE /api/v1/rooms/{id}         → Delete room

GET    /api/v1/meetings           → List meetings
POST   /api/v1/meetings           → Create meeting
GET    /api/v1/meetings/{id}      → Get meeting
PUT    /api/v1/meetings/{id}      → Update meeting
DELETE /api/v1/meetings/{id}      → Delete meeting
POST   /api/v1/meetings/{id}/summary  → Generate AI summary
GET    /api/v1/meetings/{id}/action-items → List action items

GET    /api/v1/participants       → List participants
POST   /api/v1/participants       → Add participant
GET    /api/v1/participants/{id}  → Get participant
DELETE /api/v1/participants/{id}  → Remove participant

GET    /api/v1/action-items       → List action items
POST   /api/v1/action-items       → Create action item
PUT    /api/v1/action-items/{id}  → Update action item
DELETE /api/v1/action-items/{id}  → Delete action item

GET    /api/v1/dashboard          → Dashboard stats
```

---

## Part 6: Success Metrics

| Metric | Target | Measurement |
|---|---|---|
| Backend test coverage | ≥ 70% | `pytest --cov` |
| Build pass rate | 100% | `npm run build`, `pytest` |
| Docker healthchecks | All green | `docker compose ps` |
| API response time (p95) | < 200ms | Load testing |
| AI summary accuracy | > 85% | Human eval on sample meetings |

---

## Part 7: Anti-Patterns Reinforcement

During autonomous development, these rules are non-negotiable:
- **NEVER** use `declarative_base()` — always import `Base` from `app.models.base`
- **NEVER** use `default_factory=` in `mapped_column()` — use `default=` instead
- **NEVER** use in-memory mock dicts — all data through PostgreSQL
- **NEVER** skip alembic migrations for schema changes
- **NEVER** hardcode `localhost:PORT` in frontend — use `NEXT_PUBLIC_API_URL`
- **NEVER** install shadcn CLI — use pre-built components in `src/components/ui/`
- **NEVER** use `MappedAsDataclass` in `Base` — plain `DeclarativeBase` only
- **NEVER** use timezone-aware `datetime` in models — use `utc_now()` from `app.core.utils`
