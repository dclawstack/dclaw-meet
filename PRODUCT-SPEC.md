# PRODUCT-SPEC: DClaw Meet

## Overview

**App Name:** DClaw Meet  
**Domain:** AI-Powered Video Conferencing & Meeting Management  
**Target User:** Remote and hybrid teams, project managers, executives  
**Value Proposition:** Turn every meeting into actionable outcomes with AI-native transcription, summarization, and task tracking.

---

## Core Problem

Remote and hybrid teams waste 31% of meeting time on coordination, note-taking, and follow-up. Existing tools (Zoom, Teams, Google Meet) are "dumb pipes" — they connect people but do nothing to ensure meetings produce outcomes. Post-meeting, action items are lost in Slack threads, decisions are forgotten, and nobody reviews recordings because transcripts are walls of text.

---

## Core Entities

### User
```
User
├── id: UUID (PK)
├── email: str (unique, required)
├── full_name: str (required)
├── avatar_url: str (optional)
├── created_at: datetime
└── updated_at: datetime
```

### Room
```
Room
├── id: UUID (PK)
├── name: str (required)
├── slug: str (unique, required) — e.g. "weekly-standup"
├── host_id: UUID (FK → User)
├── settings: JSON — waiting_room, recording_enabled, max_participants
├── created_at: datetime
└── updated_at: datetime
```

### Meeting
```
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
```

### Participant
```
Participant
├── id: UUID (PK)
├── meeting_id: UUID (FK → Meeting, ondelete=CASCADE)
├── user_id: UUID (FK → User, ondelete=SET NULL, optional)
├── email: str (required)
├── role: enum ["host", "co_host", "participant", "viewer"]
├── joined_at: datetime (optional)
├── left_at: datetime (optional)
├── created_at: datetime
└── updated_at: datetime
```

### TranscriptSegment
```
TranscriptSegment
├── id: UUID (PK)
├── meeting_id: UUID (FK → Meeting, ondelete=CASCADE)
├── participant_id: UUID (FK → Participant, ondelete=SET NULL, optional)
├── start_time: float — seconds from meeting start
├── end_time: float
├── text: str (required)
├── is_highlight: bool (default false) — AI-marked decision moment
└── created_at: datetime
```

### ActionItem
```
ActionItem
├── id: UUID (PK)
├── meeting_id: UUID (FK → Meeting, ondelete=CASCADE)
├── assignee_id: UUID (FK → User, ondelete=SET NULL, optional)
├── description: str (required)
├── due_date: date (optional)
├── status: enum ["open", "in_progress", "done", "cancelled"]
├── created_at: datetime
└── updated_at: datetime
```

---

## User Stories / Screens

### Screen 1: Dashboard
- Summary cards: total meetings, total rooms, total participants, open action items
- Recent meetings feed with status badges
- Room list with quick links
- Navigation to Meetings and Rooms pages

### Screen 2: Meetings
- Table view with pagination, filter by status
- Create meeting dialog with room selector
- Delete meeting with confirmation
- Status badges (scheduled/live/ended/cancelled)

### Screen 3: Rooms
- Table view with name, slug, and host
- Create room dialog with host selector
- Delete room with confirmation

### Screen 4: Meeting Detail (Future)
- Meeting info with edit/delete
- Participant list with join/leave times
- Transcript viewer with highlights
- Action items with assignees and due dates
- AI-generated summary

### Screen 5: Action Items (Future)
- Kanban-style board by status
- Filter by assignee, meeting, due date
- Quick status updates

---

## AI Features

- **Meeting Summaries:** Auto-generated post-meeting recap with key decisions, action items, and context
- **Real-time Copilot:** In-meeting sidebar with live transcript, contextual Q&A, and decision capture
- **Action Item Extraction:** Automatically identify and create tasks from meeting transcripts
- **Sentiment Analysis:** Track meeting engagement and positivity trends over time
- **Win Probability Prediction:** (Future) Predict deal closure probability from meeting patterns

---

## API Endpoints (v1.2)

```
GET    /api/v1/users              → List users
POST   /api/v1/users              → Create user
GET    /api/v1/users/{id}         → Get user
PUT    /api/v1/users/{id}         → Update user
DELETE /api/v1/users/{id}         → Delete user

GET    /api/v1/rooms              → List rooms
POST   /api/v1/rooms              → Create room
GET    /api/v1/rooms/{id}         → Get room
PUT    /api/v1/rooms/{id}         → Update room
DELETE /api/v1/rooms/{id}         → Delete room

GET    /api/v1/meetings           → List meetings (filter by status, room_id)
POST   /api/v1/meetings           → Create meeting
GET    /api/v1/meetings/{id}      → Get meeting (with participants + action items)
PUT    /api/v1/meetings/{id}      → Update meeting
DELETE /api/v1/meetings/{id}      → Delete meeting

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

## Non-Functional Requirements

- Backend tests: 70%+ coverage
- Frontend: Responsive, Tailwind + pre-built UI components
- Docker: All services start with `docker compose up -d`
- No mock data — everything persisted to database
- Real-time WebRTC integration (Phase 2)
