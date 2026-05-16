from __future__ import annotations
from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.meet import (
    RoomRepository,
    MeetingRepository,
    UserRepository,
    ParticipantRepository,
    ActionItemRepository,
)
from app.schemas.meet import (
    RoomCreate, RoomUpdate, RoomResponse,
    MeetingCreate, MeetingUpdate, MeetingResponse, MeetingDetailResponse,
    UserCreate, UserUpdate, UserResponse,
    DashboardStats,
    ActionItemResponse,
    ParticipantResponse,
)
from app.models.meet import Room, Meeting, User

router = APIRouter()


# ── Pagination response model ─────────────────────────

class PaginatedUsersResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    items: list[UserResponse]
    total: int

class PaginatedRoomsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    items: list[RoomResponse]
    total: int

class PaginatedMeetingsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    items: list[MeetingResponse]
    total: int

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    existing = await repo.get_by_email(data.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user = User(**data.model_dump())
    return await repo.create(user)


@router.get("/users", response_model=PaginatedUsersResponse)
async def list_users(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    repo = UserRepository(db)
    items, total = await repo.list_all(limit=limit, offset=offset)
    return {"items": items, "total": total}


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: UUID, data: UserUpdate, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await repo.delete(user)


# ── Rooms ─────────────────────────────────────────────

@router.post("/rooms", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create_room(data: RoomCreate, db: AsyncSession = Depends(get_db)):
    repo = RoomRepository(db)
    existing = await repo.get_by_slug(data.slug)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Slug already taken")
    room = Room(**data.model_dump())
    return await repo.create(room)


@router.get("/rooms", response_model=PaginatedRoomsResponse)
async def list_rooms(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    repo = RoomRepository(db)
    items, total = await repo.list_all(limit=limit, offset=offset)
    return {"items": items, "total": total}


@router.get("/rooms/{room_id}", response_model=RoomResponse)
async def get_room(room_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = RoomRepository(db)
    room = await repo.get_by_id(room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return room


@router.put("/rooms/{room_id}", response_model=RoomResponse)
async def update_room(room_id: UUID, data: RoomUpdate, db: AsyncSession = Depends(get_db)):
    repo = RoomRepository(db)
    room = await repo.get_by_id(room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(room, field, value)
    await db.commit()
    await db.refresh(room)
    return room


@router.delete("/rooms/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(room_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = RoomRepository(db)
    room = await repo.get_by_id(room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    await repo.delete(room)


# ── Meetings ──────────────────────────────────────────

@router.post("/meetings", response_model=MeetingResponse, status_code=status.HTTP_201_CREATED)
async def create_meeting(data: MeetingCreate, db: AsyncSession = Depends(get_db)):
    repo = MeetingRepository(db)
    meeting = Meeting(**data.model_dump())
    return await repo.create(meeting)


@router.get("/meetings", response_model=PaginatedMeetingsResponse)
async def list_meetings(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status_filter: Optional[str] = Query(None, alias="status"),
    room_id: Optional[UUID] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    repo = MeetingRepository(db)
    if room_id:
        items, total = await repo.list_by_room(room_id, limit=limit, offset=offset)
    elif status_filter:
        items, total = await repo.list_by_status(status_filter, limit=limit, offset=offset)
    else:
        items, total = await repo.list_all(limit=limit, offset=offset)
    return {"items": items, "total": total}


@router.get("/meetings/{meeting_id}", response_model=MeetingDetailResponse)
async def get_meeting(meeting_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = MeetingRepository(db)
    meeting = await repo.get_by_id(meeting_id)
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
    return meeting


@router.put("/meetings/{meeting_id}", response_model=MeetingResponse)
async def update_meeting(meeting_id: UUID, data: MeetingUpdate, db: AsyncSession = Depends(get_db)):
    repo = MeetingRepository(db)
    meeting = await repo.get_by_id(meeting_id)
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(meeting, field, value)
    await db.commit()
    await db.refresh(meeting)
    return meeting


@router.delete("/meetings/{meeting_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meeting(meeting_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = MeetingRepository(db)
    meeting = await repo.get_by_id(meeting_id)
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
    await repo.delete(meeting)


# ── Dashboard ─────────────────────────────────────────

@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    m_repo = MeetingRepository(db)
    r_repo = RoomRepository(db)
    p_repo = ParticipantRepository(db)
    a_repo = ActionItemRepository(db)

    _meetings, total_meetings = await m_repo.list_all(limit=1)
    _rooms, total_rooms = await r_repo.list_all(limit=1)
    _parts, total_participants = await p_repo.list_all(limit=1)
    open_action_items = await a_repo.count_by_status("open")

    return DashboardStats(
        total_meetings=total_meetings,
        total_rooms=total_rooms,
        total_participants=total_participants,
        open_action_items=open_action_items,
    )
