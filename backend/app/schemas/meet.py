from datetime import datetime, date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


# ── User ──────────────────────────────────────────────

class UserBase(BaseModel):
    email: str
    full_name: str
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime
    updated_at: datetime


# ── Room ──────────────────────────────────────────────

class RoomBase(BaseModel):
    name: str
    slug: str
    settings: Optional[dict] = None


class RoomCreate(RoomBase):
    host_id: UUID


class RoomUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    settings: Optional[dict] = None


class RoomResponse(RoomBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    host_id: UUID
    created_at: datetime
    updated_at: datetime


# ── Meeting ───────────────────────────────────────────

class MeetingBase(BaseModel):
    title: str
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    status: Optional[str] = "scheduled"
    recording_url: Optional[str] = None
    summary: Optional[str] = None


class MeetingCreate(MeetingBase):
    room_id: UUID


class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    status: Optional[str] = None
    recording_url: Optional[str] = None
    summary: Optional[str] = None


class MeetingResponse(MeetingBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    room_id: UUID
    created_at: datetime
    updated_at: datetime


class MeetingDetailResponse(MeetingResponse):
    participants: list["ParticipantResponse"] = []
    action_items: list["ActionItemResponse"] = []


# ── Participant ───────────────────────────────────────

class ParticipantBase(BaseModel):
    email: str
    role: Optional[str] = "participant"
    joined_at: Optional[datetime] = None
    left_at: Optional[datetime] = None


class ParticipantCreate(ParticipantBase):
    meeting_id: UUID
    user_id: Optional[UUID] = None


class ParticipantUpdate(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
    joined_at: Optional[datetime] = None
    left_at: Optional[datetime] = None


class ParticipantResponse(ParticipantBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    meeting_id: UUID
    user_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime


# ── Transcript Segment ────────────────────────────────

class TranscriptSegmentBase(BaseModel):
    start_time: float
    end_time: float
    text: str
    is_highlight: bool = False


class TranscriptSegmentCreate(TranscriptSegmentBase):
    meeting_id: UUID
    participant_id: Optional[UUID] = None


class TranscriptSegmentResponse(TranscriptSegmentBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    meeting_id: UUID
    participant_id: Optional[UUID] = None
    created_at: datetime


# ── Action Item ───────────────────────────────────────

class ActionItemBase(BaseModel):
    description: str
    due_date: Optional[date] = None
    status: Optional[str] = "open"


class ActionItemCreate(ActionItemBase):
    meeting_id: UUID
    assignee_id: Optional[UUID] = None


class ActionItemUpdate(BaseModel):
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = None
    assignee_id: Optional[UUID] = None


class ActionItemResponse(ActionItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    meeting_id: UUID
    assignee_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime


# Dashboard
class DashboardStats(BaseModel):
    total_meetings: int
    total_rooms: int
    total_participants: int
    open_action_items: int
