# DClaw Meet — v1.2 Feature Roadmap

> Based on: Y Combinator vertical SaaS principles, trending GitHub repos (jitsi-meet, livekit), AI product research (Zoom, Google Meet, Whereby, Around)

## Pre-Flight Checklist

- [ ] `frontend/package-lock.json` committed after any `npm install` / dependency change
- [ ] `frontend/next-env.d.ts` exists and is committed
- [ ] `docker-compose.yml` healthchecks correct
- [ ] `frontend/Dockerfile` declares `ARG NEXT_PUBLIC_API_URL` before `RUN npm run build`

## v1.0 Feature Inventory (Current)

- [ ] Video conferencing rooms
- [ ] Screen sharing
- [ ] Scheduling
- [ ] Basic recording
- [ ] Real backend CRUD (no mocks)
- [ ] Docker + Helm deployment
- [ ] Alembic migrations
- [ ] Backend tests

---

## v1.2 Roadmap

### P0 — Must Have (Ship in v1.0, demo-ready)

#### 1. AI Meet Copilot (Meeting Assistant)
**Description:** AI assistant that joins meetings, transcribes, takes notes, and extracts action items. "What were the action items from the standup?"
- **AI Angle:** Real-time transcription + summarization + action item extraction.
- **Backend:** `/api/v1/ai/meet` bot. Transcription pipeline.
- **Frontend:** Meeting sidebar with live transcript and highlights.
- **Files:** `backend/app/services/meet_ai.py`, `frontend/src/components/meet-copilot.tsx`

#### 2. Video Conferencing with WebRTC
**Description:** High-quality video/audio with adaptive bitrate, noise suppression, and virtual backgrounds.
- **Backend:** WebRTC SFU/MCU. Signal server.
- **Frontend:** Video grid with speaker highlighting. Background blur/replacement.
- **Files:** `backend/app/services/webrtc.py`

#### 3. Screen Sharing & Collaboration
**Description:** Share screen, window, or tab. Co-annotate on shared content.
- **Backend:** Screen sharing stream relay.
- **Frontend:** Share picker. Annotation toolbar.
- **Files:** `frontend/src/components/screen-share.tsx`

#### 4. Smart Scheduling & Calendar Integration
**Description:** Find optimal meeting times across calendars. Send invites. Handle time zones.
- **Backend:** Calendar API integration. Availability calculation.
- **Frontend:** Scheduling assistant with time slot picker.
- **Files:** `backend/app/services/scheduling.py`

### P1 — Should Have (v1.1–1.2)

#### 5. AI Meeting Summaries & Follow-Ups
**Description:** Auto-generated meeting summary with key decisions, action items, and follow-up email draft.
- **AI Angle:** Post-meeting LLM synthesis.
- **Backend:** Summary generation pipeline.
- **Frontend:** Meeting recap page with shareable link.

#### 6. Breakout Rooms
**Description:** Host creates breakout rooms. Auto-assign or self-select. Broadcast messages.
- **Backend:** Room management. Participant routing.
- **Frontend:** Breakout control panel.

#### 7. Polling & Q&A
**Description:** Live polls, quizzes, and moderated Q&A during meetings.
- **Backend:** Real-time poll engine. Q&A moderation queue.
- **Frontend:** Poll creator. Q&A upvote board.

#### 8. Recording & Cloud Playback
**Description:** Cloud recording with searchable transcript. Chapter markers.
- **Backend:** Recording storage. Transcript indexing.
- **Frontend:** Playback with transcript sync. Search within recording.

### P2 — Could Have (v1.3+)

#### 9. AI Real-Time Translation
**Description:** Live captioning and voice translation for multilingual meetings.

#### 10. Meeting Analytics
**Description:** Talk time distribution, engagement scores, sentiment analysis.

#### 11. Virtual Whiteboard
**Description:** Collaborative infinite canvas with shapes, sticky notes, and templates.

#### 12. Spatial Audio & 3D Rooms
**Description:** Proximity-based audio and 3D virtual meeting spaces.

---

## Implementation Priority

1. **Week 1–2:** AI Meet Copilot (P0.1) + WebRTC Conferencing (P0.2)
2. **Week 3–4:** Screen Sharing (P0.3) + Smart Scheduling (P0.4)
3. **Week 5–6:** Meeting Summaries (P1.5) + Breakout Rooms (P1.6)
4. **Week 7–8:** Polling/Q&A (P1.7) + Recording (P1.8)
