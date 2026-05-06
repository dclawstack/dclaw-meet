import uuid
from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class CreateMeetingRequest(BaseModel):
    title: str
    transcript: str


class MeetingResponse(BaseModel):
    id: str
    title: str
    transcript: str
    summary: str
    action_items: list[str]
    created_at: str


@router.post("/meetings")
async def create_meeting(req: CreateMeetingRequest):
    return MeetingResponse(
        id=str(uuid.uuid4()),
        title=req.title,
        transcript=req.transcript,
        summary="Mock summary of the meeting...",
        action_items=["Action 1", "Action 2"],
        created_at=datetime.now(timezone.utc).isoformat(),
    )


@router.get("/meetings/{id}/action-items")
async def get_meeting_action_items(id: str):
    return ["Action 1", "Action 2"]
