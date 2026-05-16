from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.meet import User, Room, Meeting, Participant, TranscriptSegment, ActionItem
from app.repositories.base_repo import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()


class RoomRepository(BaseRepository[Room]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Room)

    async def get_by_slug(self, slug: str) -> Room | None:
        result = await self.db.execute(select(Room).where(Room.slug == slug))
        return result.scalar_one_or_none()


class MeetingRepository(BaseRepository[Meeting]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Meeting)

    async def list_by_room(self, room_id: UUID, limit: int = 20, offset: int = 0) -> tuple[list[Meeting], int]:
        result = await self.db.execute(
            select(Meeting)
            .where(Meeting.room_id == room_id)
            .limit(limit)
            .offset(offset)
        )
        items = list(result.scalars().all())
        count_result = await self.db.execute(
            select(func.count()).select_from(Meeting).where(Meeting.room_id == room_id)
        )
        total = count_result.scalar() or 0
        return items, total

    async def list_by_status(self, status: str, limit: int = 20, offset: int = 0) -> tuple[list[Meeting], int]:
        result = await self.db.execute(
            select(Meeting)
            .where(Meeting.status == status)
            .limit(limit)
            .offset(offset)
        )
        items = list(result.scalars().all())
        count_result = await self.db.execute(
            select(func.count()).select_from(Meeting).where(Meeting.status == status)
        )
        total = count_result.scalar() or 0
        return items, total


class ParticipantRepository(BaseRepository[Participant]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Participant)

    async def list_by_meeting(self, meeting_id: UUID, limit: int = 50, offset: int = 0) -> list[Participant]:
        result = await self.db.execute(
            select(Participant)
            .where(Participant.meeting_id == meeting_id)
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())


class TranscriptSegmentRepository(BaseRepository[TranscriptSegment]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, TranscriptSegment)

    async def list_by_meeting(self, meeting_id: UUID, limit: int = 100, offset: int = 0) -> list[TranscriptSegment]:
        result = await self.db.execute(
            select(TranscriptSegment)
            .where(TranscriptSegment.meeting_id == meeting_id)
            .order_by(TranscriptSegment.start_time)
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())


class ActionItemRepository(BaseRepository[ActionItem]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, ActionItem)

    async def list_by_meeting(self, meeting_id: UUID, limit: int = 50, offset: int = 0) -> list[ActionItem]:
        result = await self.db.execute(
            select(ActionItem)
            .where(ActionItem.meeting_id == meeting_id)
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def list_by_assignee(self, assignee_id: UUID, limit: int = 50, offset: int = 0) -> list[ActionItem]:
        result = await self.db.execute(
            select(ActionItem)
            .where(ActionItem.assignee_id == assignee_id)
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def count_by_status(self, status: str) -> int:
        result = await self.db.execute(
            select(func.count()).select_from(ActionItem).where(ActionItem.status == status)
        )
        return result.scalar() or 0
