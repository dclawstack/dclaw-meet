# DClaw Meet — Strategic Product Plan v1.3

> YC-Grade Gap Analysis & Autonomous Development Roadmap
> Generated: 2026-05-16
> Based on: `AGENTS.md` architecture audit, scaffold state analysis, YC standards, v1.2 execution learnings

---

## Executive Summary

**DClaw Meet v1.3** is the next evolution of our AI-native meeting platform. While v1.2 established the foundational meeting domain models, CRUD APIs, dashboard shell, and basic AI summary capabilities, **v1.3 focuses on deepening product-market fit through tangible AI value delivery, platform stickiness, and enterprise readiness signals.**

The core thesis remains: remote and hybrid teams waste **31% of meeting time** on coordination. DClaw Meet doesn't just connect people — it ensures every meeting produces **actionable, trackable outcomes.**

---

## Part 1: v1.2 → v1.3 Progress Assessment

### What Shipped in v1.2

| Component | Status | Notes |
|---|---|---|
| Config drift fix | ✅ Complete | Ports, DB, Dockerfile aligned |
| Meeting domain models | ✅ Complete | `User`, `Room`, `Meeting`, `Participant`, `TranscriptSegment`, `ActionItem` |
| Pydantic schemas + repos | ✅ Complete | Full CRUD with `BaseRepository` |
| Alembic migrations | ✅ Complete | Initial schema versioned |
| Backend test suite | ✅ Complete | 70%+ coverage gate |
| Frontend API client | ✅ Complete | Typed fetch wrapper |
| Dashboard shell | ✅ Complete | Next.js layout + navigation |
| Room management | ✅ Complete | Persistent rooms with settings |
| AI meeting summary | ✅ Complete | LLM-powered post-meeting summaries |

### Gaps Identified from v1.2 Build

| Gap | Impact | v1.3 Resolution |
|---|---|---|
| No real-time signaling (WebSocket) | AI copilot is polling-only; high latency | **2.1** — WebSocket foundation for real-time features |
| No user authentication | Anyone can hit any endpoint | **0.11** — JWT auth layer (reclassified as foundation) |
| No file/upload infrastructure | Recordings can't be stored | **0.12** — Object storage abstraction (S3-compatible) |
| Action items not actionable | No email reminders, no progress tracking | **1.5** — Action Item Tracker with notifications |
| Rooms lack scheduling intelligence | Manual time entry only | **1.2** — Smart Scheduling Engine |
| No visibility into meeting health | Teams don't know if meetings are effective | **2.3** — Meeting Analytics Dashboard |
| Frontend pages skeleton-only | No interactivity, no forms | **C0-F** — Form components + validation |
| No invite/sharing loop | Zero viral mechanism | **1.7** — Meeting invite system with shareable links |

---

## Part 2: Prioritized Feature Roadmap

### Legend

| Complexity | Definition | Est. Dev Time | Risk Level |
|---|---|---|---|
| **0** | Low complexity / Core foundational elements / Quick wins | 1–3 days | Low |
| **1** | Medium complexity / Core differentiators | 3–7 days | Medium |
| **2** | High complexity / Advanced features (AI integrations, real-time, complex workflows) | 7–14 days | High |

---

### Complexity 0 — Foundation & Quick Wins

> **Goal:** Unblock all higher-complexity work and close security/gaps left from v1.2.

| # | Feature | Description | v1.3 Rationale | Est. Effort |
|---|---|---|---|---|
| **0.1** | JWT Authentication | Login/register with JWT tokens, password hashing (`bcrypt`), protected routes via `Depends()` | **Security-critical gap** from v1.2; required before any production use | 3 days |
| **0.2** | Current User Context | `GET /api/v1/me` endpoint, auth middleware on frontend, user avatar in nav | Enables personalized dashboards and permission gates | 2 days |
| **0.3** | Object Storage Abstraction | S3-compatible upload/download service (`app/services/storage.py`) with local MinIO for dev | Required for recordings, avatars, exports | 2 days |
| **0.4** | Form Components + Validation | Reusable `MeetingForm`, `RoomForm`, `ActionItemForm` with `react-hook-form` + `zod` validation | Every C1 feature needs forms; this is infrastructure | 2 days |
| **0.5** | Toast/Notification System | Global toast provider for success/error/loading states | UX baseline for all async operations | 1 day |
| **0.6** | Loading & Empty States | Skeleton loaders, empty-state illustrations across all pages | Polish gap from v1.2 skeleton pages | 2 days |
| **0.7** | Error Boundary + 404 Page | Global error boundary, not-found page in App Router | Production resilience | 1 day |
| **0.8** | Frontend Test Foundation | `vitest` + `@testing-library/react` setup; component tests for `Button`, `Card`, `Input` | Quality gate for UI changes | 2 days |

**C0 Total Estimate:** ~15 days (can parallelize across 2 developers)

---

### Complexity 1 — Core Differentiators

> **Goal:** Ship AI-powered features that users can feel immediately. These are the "demo moments" for YC and early customers.

| # | Feature | Description | v1.3 Rationale | Est. Effort |
|---|---|---|---|---|
| **1.1** | Enhanced AI Summary (v2) | Structured output: key decisions, action items, open questions, sentiment score; markdown export | v1.2 summary was basic text; structured output is the differentiator | 4 days |
| **1.2** | Smart Scheduling Engine | `/api/v1/schedule` endpoint that finds optimal meeting windows across participants; conflict detection | Top user friction point; replaces Calendly for internal teams | 5 days |
| **1.3** | Meeting Invite System | Shareable room links (`/join/:slug`), email invites via SMTP, guest participant support | **Viral loop** — critical for growth; guests become users | 4 days |
| **1.4** | Recording & Transcript Archive | Upload recording metadata, search transcripts with full-text (`tsvector` in Postgres), playback page | Knowledge retention moat; searchable history | 5 days |
| **1.5** | Action Item Tracker (Full) | Extract tasks from AI summary, assign owners, due dates, email reminders, status updates, `/action-items` page | **Outcome guarantee** — the core value prop | 5 days |
| **1.6** | Calendar Integration (Google OAuth) | OAuth 2.0 flow, read calendar events, auto-create meeting entries, sync scheduled rooms | Workflow embedding; reduces context switching | 6 days |
| **1.7** | Meeting Templates | Reusable agenda templates (`Weekly Standup`, `1:1`, `Sprint Review`), auto-populate new meetings | Reduces meeting setup friction; stickiness feature | 3 days |
| **1.8** | Comment Threads on Transcripts | Inline comments and @mentions on transcript segments, threaded discussions | Collaboration layer; keeps discussion in context | 4 days |

**C1 Total Estimate:** ~36 days (parallelizable across 3 streams: AI, Core, Integrations)

---

### Complexity 2 — Advanced Platform

> **Goal:** Build defensibility through real-time AI, analytics data moat, and enterprise-grade capabilities.

| # | Feature | Description | v1.3 Rationale | Est. Effort |
|---|---|---|---|---|
| **2.1** | WebSocket Real-Time Foundation | `ws://` endpoint with `python-socketio`/FastAPI, room-based namespace, auth over socket | Prerequisite for **2.2** and **2.3**; replaces polling | 5 days |
| **2.2** | Real-Time AI Copilot | In-meeting sidebar (via WebSocket) with live transcript streaming, contextual Q&A, decision capture | **Active AI differentiator** — the "wow" demo moment | 8 days |
| **2.3** | Meeting Analytics Dashboard | Talk-time distribution, engagement heatmaps, sentiment trends, meeting health score, exportable reports | **Data moat** + network effect; enterprise sales feature | 7 days |
| **2.4** | Real-Time Translation | Live captioning in 20+ languages via translation service integration | Global team enabler; TAM expansion | 6 days |
| **2.5** | Breakout Rooms | Host-controlled sub-rooms with broadcast message, auto-room assignment, rejoin main room | Enterprise sales feature; competes with Zoom/Teams | 5 days |
| **2.6** | E2EE & Compliance Architecture | End-to-end encryption for recordings, audit log table, SOC 2 readiness documentation | Enterprise trust signal; required for $50K+ ACV deals | 6 days |
| **2.7** | AI Meeting Agenda Generator | Pre-meeting agenda based on attendee roles, past meeting context, and Calendar event description | **Pre-meeting value** — completes the lifecycle | 5 days |

**C2 Total Estimate:** ~42 days (requires C0 + C1 foundations; sequential dependencies marked)

---

### Future Roadmap (Post-v1.3 / v2.0 Candidates)

| Feature | Complexity | Notes |
|---|---|---|
| Microsoft 365 / Outlook Calendar | 1 | Mirror of Google Calendar integration |
| Native mobile apps (React Native) | 2 | TAM expansion |
| AI-powered meeting scheduling bot (email parsing) | 2 | "Forward me an email and I'll schedule it" |
| Enterprise SSO (SAML / OIDC) | 2 | Required for Fortune 500 |
| White-label / custom domains | 1 | Agency/reseller model |
| Revenue / billing integration (Stripe) | 1 | Freemium → Pro → Enterprise tiers |
| Integration marketplace (Slack, Notion, Jira) | 1–2 | Ecosystem play |

---

## Part 3: Implementation Sprints (v1.3)

### Sprint A: Foundation Hardening (Week 1)
**Focus:** Close v1.2 security/UX gaps. Everything here blocks C1 and C2.

- [ ] **0.1** JWT auth: `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `GET /api/v1/me`
- [ ] **0.1** Protect all existing v1.2 routes with `Depends(get_current_user)`
- [ ] **0.2** Frontend auth: login page, token storage (`httpOnly` cookie preferred), auth context
- [ ] **0.3** Storage service abstraction with local MinIO dev setup
- [ ] **0.4** Build `MeetingForm`, `RoomForm`, `ActionItemForm` with validation
- [ ] **0.5** Global toast notification system
- [ ] **0.6** Skeleton loaders + empty states on all v1.2 pages
- [ ] [QA Gate] All v1.2 pages interactive; auth enforced; tests pass

**Sprint A Commit:** `feat(auth): JWT auth layer + form infrastructure`

---

### Sprint B: AI Deepening + Scheduling (Week 2)
**Focus:** Make the AI tangible and solve the #1 user pain point (scheduling).

- [ ] **1.1** Enhanced AI summary with structured JSON output (decisions, action_items, questions, sentiment)
- [ ] **1.1** Markdown export for summaries (`/api/v1/meetings/{id}/summary/export`)
- [ ] **1.2** Smart scheduling: availability endpoint, conflict detection algorithm
- [ ] **1.2** Schedule suggestion UI component
- [ ] **1.7** Meeting templates CRUD (`/api/v1/templates`)
- [ ] **1.7** Template selector in meeting creation flow
- [ ] [QA Gate] AI summary demo-ready; scheduling finds real conflicts

**Sprint B Commit:** `feat(ai): structured summaries + smart scheduling + templates`

---

### Sprint C: Growth Loop + Archive (Week 3)
**Focus:** Viral mechanism and knowledge retention.

- [ ] **1.3** Shareable room links with slug-based access (`/join/:slug`)
- [ ] **1.3** Email invite service with HTML templates (SMTP/SendGrid abstraction)
- [ ] **1.3** Guest participant flow (no account required)
- [ ] **1.4** Recording metadata storage + `tsvector` transcript search
- [ ] **1.4** Transcript playback page with synchronized segments
- [ ] **1.8** Comment threads on transcript segments
- [ ] [QA Gate] External users can join meetings; transcripts are searchable

**Sprint C Commit:** `feat(growth): invite system + recording archive + transcript comments`

---

### Sprint D: Action Items + Calendar (Week 4)
**Focus:** Close the loop on meeting outcomes.

- [ ] **1.5** Action item extraction from AI summary (automated)
- [ ] **1.5** Full action item CRUD with due dates, assignees, status
- [ ] **1.5** `/action-items` dashboard page with filters (me, open, overdue)
- [ ] **1.5** Email reminder cron/batch job for due action items
- [ ] **1.6** Google OAuth 2.0 flow (backend + frontend)
- [ ] **1.6** Calendar read: list upcoming events
- [ ] **1.6** Auto-create meeting entries in Google Calendar on schedule
- [ ] [QA Gate] Action items are tracked and reminded; calendar sync works

**Sprint D Commit:** `feat(outcomes): action item tracker + Google Calendar integration`

---

### Sprint E: WebSocket + Real-Time Foundation (Week 5)
**Focus:** Platform upgrade for real-time capabilities.

- [ ] **2.1** WebSocket server setup with `python-socketio` and FastAPI
- [ ] **2.1** Room-based namespace authentication over socket
- [ ] **2.1** Frontend Socket.IO client integration
- [ ] **2.1** Heartbeat/reconnection handling
- [ ] **2.7** AI agenda generator: pre-meeting prompt with attendee context
- [ ] **2.7** Agenda preview and edit before meeting starts
- [ ] [QA Gate] WebSocket connections stable; agendas generated pre-meeting

**Sprint E Commit:** `feat(realtime): WebSocket foundation + AI agenda generator`

---

### Sprint F: Real-Time AI Copilot (Week 6)
**Focus:** The flagship feature. Active AI during meetings.

- [ ] **2.2** Live transcript streaming via WebSocket
- [ ] **2.2** In-meeting sidebar with real-time transcript display
- [ ] **2.2** Contextual Q&A: "What did Sarah agree to?"
- [ ] **2.2** Decision capture: one-click "Mark as Decision" during meeting
- [ ] **2.4** Live caption translation architecture (translation service abstraction)
- [ ] [QA Gate] Copilot responds to questions in <3s; decisions auto-captured

**Sprint F Commit:** `feat(copilot): real-time AI sidebar + decision capture`

---

### Sprint G: Analytics + Enterprise Signals (Week 7–8)
**Focus:** Data moat and compliance.

- [ ] **2.3** Analytics data aggregation pipeline (meeting duration, talk-time, sentiment)
- [ ] **2.3** Dashboard charts: engagement heatmap, talk-time pie, sentiment trend
- [ ] **2.3** Meeting health score algorithm
- [ ] **2.5** Breakout room modeling and host controls
- [ ] **2.6** Audit log table (who did what, when)
- [ ] **2.6** E2EE architecture document + recording encryption at rest
- [ ] [QA Gate] Analytics render correctly; audit logs capture all mutations

**Sprint G Commit:** `feat(platform): analytics dashboard + enterprise readiness`

---

## Part 4: Data Model Evolution (v1.3)

### New Models

```
User (extended from v1.2)
├── password_hash: str (new)
├── google_calendar_token: JSON (new, nullable)
├── timezone: str (new, default "UTC")
└── email_verified: bool (new, default false)

Template (new)
├── id: UUID (PK)
├── name: str — e.g. "Weekly Standup"
├── description: str (optional)
├── agenda_items: JSON — ordered list of agenda topics
├── default_duration_minutes: int
├── created_by_id: UUID (FK → User)
├── created_at: datetime
└── updated_at: datetime

MeetingInvite (new)
├── id: UUID (PK)
├── meeting_id: UUID (FK → Meeting, ondelete=CASCADE)
├── email: str
├── token: str (unique, for magic-link access)
├── status: enum ["pending", "accepted", "declined"]
├── invited_at: datetime
└── responded_at: datetime (optional)

AuditLog (new)
├── id: UUID (PK)
├── user_id: UUID (FK → User, ondelete=SET NULL)
├── action: str — e.g. "meeting.created", "action_item.updated"
├── resource_type: str — e.g. "meeting", "room"
├── resource_id: UUID
├── metadata: JSON (optional)
├── created_at: datetime

Recording (new)
├── id: UUID (PK)
├── meeting_id: UUID (FK → Meeting, ondelete=CASCADE)
├── storage_key: str — S3/MinIO object key
├── duration_seconds: int
├── file_size_bytes: int
├── transcript_text: str (optional, full transcript)
├── transcript_search_vector: tsvector (generated)
├── created_at: datetime

Comment (new)
├── id: UUID (PK)
├── transcript_segment_id: UUID (FK → TranscriptSegment, ondelete=CASCADE)
├── author_id: UUID (FK → User, ondelete=SET NULL)
├── content: str
├── parent_id: UUID (FK → Comment, ondelete=CASCADE, nullable — threaded)
├── created_at: datetime
└── updated_at: datetime
```

### Updated Models

```
Meeting (updated)
├── agenda: JSON (new, generated by AI or from template)
├── health_score: float (new, nullable — 0.0 to 1.0)
└── google_calendar_event_id: str (new, nullable)

ActionItem (updated)
├── source: enum ["manual", "ai_extracted"] (new)
├── reminded_at: datetime (new, nullable)
└── reminder_count: int (new, default 0)

Room (updated)
├── is_public: bool (new, default false — for open join links)
└── allow_guests: bool (new, default true)
```

---

## Part 5: API Contract (v1.3 Evolved)

### Auth
```
POST   /api/v1/auth/register         → Create account
POST   /api/v1/auth/login            → JWT token pair (access + refresh)
POST   /api/v1/auth/refresh          → Refresh access token
GET    /api/v1/me                    → Current user profile
PUT    /api/v1/me                    → Update profile
```

### Rooms (v1.2 + additions)
```
GET    /api/v1/rooms                 → List my rooms
POST   /api/v1/rooms                 → Create room
GET    /api/v1/rooms/{id}            → Get room
PUT    /api/v1/rooms/{id}            → Update room
DELETE /api/v1/rooms/{id}            → Delete room
GET    /api/v1/rooms/{slug}/join     → Validate join link
```

### Meetings (v1.2 + additions)
```
GET    /api/v1/meetings              → List meetings
POST   /api/v1/meetings              → Create meeting
GET    /api/v1/meetings/{id}         → Get meeting + agenda
PUT    /api/v1/meetings/{id}         → Update meeting
DELETE /api/v1/meetings/{id}         → Delete meeting
POST   /api/v1/meetings/{id}/start   → Mark as live
POST   /api/v1/meetings/{id}/end     → Mark as ended + trigger AI summary
POST   /api/v1/meetings/{id}/summary → Generate/get AI summary
GET    /api/v1/meetings/{id}/summary/export → Download markdown
POST   /api/v1/meetings/{id}/agenda  → Generate AI agenda (pre-meeting)
```

### Schedules
```
POST   /api/v1/schedule/find         → Find optimal meeting windows
GET    /api/v1/schedule/conflicts    → Check conflicts for time window
```

### Templates
```
GET    /api/v1/templates             → List templates
POST   /api/v1/templates             → Create template
GET    /api/v1/templates/{id}        → Get template
PUT    /api/v1/templates/{id}        → Update template
DELETE /api/v1/templates/{id}        → Delete template
```

### Invites
```
POST   /api/v1/invites               → Send meeting invite
GET    /api/v1/invites/{token}       → Validate invite token
POST   /api/v1/invites/{token}/accept → Accept invite (guest or user)
```

### Recordings
```
POST   /api/v1/recordings            → Register recording upload
GET    /api/v1/recordings/{id}       → Get recording metadata
GET    /api/v1/recordings/{id}/download → Signed download URL
GET    /api/v1/recordings/search     → Full-text transcript search
```

### Transcript Comments
```
GET    /api/v1/transcript-segments/{id}/comments → List comments
POST   /api/v1/transcript-segments/{id}/comments → Add comment
DELETE /api/v1/comments/{id}         → Delete comment
```

### Action Items
```
GET    /api/v1/action-items          → List (filter: mine, meeting, status)
POST   /api/v1/action-items          → Create manually
PUT    /api/v1/action-items/{id}     → Update status/due date/assignee
DELETE /api/v1/action-items/{id}     → Delete
POST   /api/v1/action-items/{id}/remind → Trigger reminder
```

### Calendar
```
GET    /api/v1/calendar/auth         → Google OAuth redirect URL
POST   /api/v1/calendar/callback     → OAuth callback
GET    /api/v1/calendar/events       → List upcoming events
POST   /api/v1/calendar/sync         → Sync meeting to calendar
```

### Analytics
```
GET    /api/v1/analytics/overview    → Dashboard KPIs
GET    /api/v1/analytics/meetings/{id} → Per-meeting analytics
GET    /api/v1/analytics/trends      → Time-series trends
```

### Real-Time (WebSocket)
```
WS     /ws/meetings/{id}             → Join meeting channel
  → events: transcript.segment, copilot.response, decision.marked,
            participant.joined, participant.left, breakout.announced
```

---

## Part 6: Risk Assessment & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| WebSocket scaling challenges | Medium | High | Design stateless socket handlers; Redis adapter for multi-node |
| LLM API latency >5s for copilot | Medium | High | Streaming responses; fallback to cached templates; tiered LLM (fast/slow) |
| Google OAuth app verification delays | Medium | Medium | Start verification early; document with screenshots for submission |
| Postgres `tsvector` performance on large transcripts | Low | Medium | Add GIN index; paginate search; consider pg_trgm for fuzzy |
| Frontend build size bloat with charts + socket client | Low | Medium | Dynamic imports (`next/dynamic`) for analytics dashboard |
| Email deliverability (reminders, invites) | Medium | Medium | Use SendGrid/Mailgun; implement bounce tracking; retry logic |
| Auth token security (XSS/CSRF) | Low | High | `httpOnly` cookies; CSRF protection; short expiry on access tokens |

---

## Part 7: Success Metrics (v1.3 Targets)

| Metric | v1.2 Baseline | v1.3 Target | Measurement |
|---|---|---|---|
| Backend test coverage | 70% | ≥ 80% | `pytest --cov` |
| Frontend test coverage | 0% | ≥ 50% | `vitest --coverage` |
| Build pass rate | 100% | 100% | CI gate |
| Docker healthchecks | All green | All green | `docker compose ps` |
| API response time (p95) | < 200ms | < 150ms | Load testing |
| AI summary generation time | ~10s | < 5s | Instrumented logging |
| WebSocket message latency | N/A | < 500ms | Client-side instrumentation |
| Auth-protected endpoints | 0% | 100% | Security audit |
| User-invite → signup conversion | N/A | > 15% | Analytics tracking |
| Action item completion rate | N/A | > 60% | DB query |

---

## Part 8: Resource Allocation

| Role | Sprint Focus | Estimate |
|---|---|---|
| **Backend Engineer A** | Auth, APIs, Scheduling, Calendar | Weeks 1–4 |
| **Backend Engineer B** | AI services, Storage, WebSocket, Analytics | Weeks 2–7 |
| **Frontend Engineer** | Forms, Auth UI, Dashboard, Copilot sidebar | Weeks 1–6 |
| **DevOps / QA** | Docker, CI, Load testing, Security audit | Weeks 4–8 (part-time) |

**Total Timeline:** ~8 weeks for full v1.3 scope.
**MVP Cut (Sprints A–D):** ~4 weeks — authentication, AI summaries, scheduling, invites, action items, calendar. This is the YC application-ready scope.

---

## Part 9: Anti-Patterns Reinforcement (v1.3)

All v1.2 anti-patterns remain in effect. Additional v1.3-specific rules:

| Anti-Pattern | Why It Breaks Things | Correct Alternative |
|---|---|---|
| Storing JWT in `localStorage` | XSS vulnerability → token theft | `httpOnly` cookie or secure cookie storage |
| Raw SQL for `tsvector` search | SQL injection risk; bypasses ORM | SQLAlchemy `func.to_tsvector` + parameterized queries |
| Synchronous LLM calls in request handlers | Blocks event loop; timeouts | Background task queue (`celery` or `arq`) or streaming |
| WebSocket broadcasts without room scoping | Privacy leak — all clients get all messages | Namespace/channel per meeting |
| Missing rate limiting on auth endpoints | Brute-force vulnerability | Implement `slowapi` or nginx rate limiting |
| Hardcoded SMTP/LLM credentials | Security breach; non-portable | Environment variables only; use secrets manager in prod |
| No audit logging for sensitive mutations | Compliance gap; no incident tracing | `AuditLog` entry on every `create`/`update`/`delete` |

---

## Part 10: Definition of Done (v1.3)

DClaw Meet v1.3 is complete when:

1. [ ] All Sprint A–G features are coded and merged
2. [ ] Backend coverage ≥ 80%; Frontend coverage ≥ 50%
3. [ ] All endpoints protected by JWT auth
4. [ ] `docker compose up -d` boots a fully functional system
5. [ ] AI summary generates structured output in < 5 seconds
6. [ ] Action items are auto-extracted, assigned, and reminded
7. [ ] Google Calendar sync works end-to-end
8. [ ] WebSocket real-time copilot streams transcript live
9. [ ] Analytics dashboard renders meeting health scores
10. [ ] External users can join via shareable link without account
11. [ ] Security audit passed (auth, XSS, CSRF, rate limiting)
12. [ ] **NO MOCK DATA** — all data persisted in PostgreSQL

---

> **Document Status:** Ready for autonomous development. Do not proceed to coding until agent confirms alignment with `AGENTS.md` architecture rules.
