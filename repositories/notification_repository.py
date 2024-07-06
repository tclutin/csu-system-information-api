from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.models import Notification


class NotificationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, notification: Notification) -> Notification:
        self.session.add(notification)
        await self.session.commit()
        return notification

    async def delete(self, notification: Notification) -> None:
        await self.session.delete(notification)
        await self.session.commit()


    async def get_by_id(self, notification_id: int) -> Optional[Notification]:
        statement = select(Notification).where(Notification.notification_id == notification_id)
        result = await self.session.execute(statement)
        return result.scalar()

    async def get_by_tgchat_id(self, tgchat_id: int) -> List[Notification]:
        statement = select(Notification).where(Notification.tgchat_id == tgchat_id)
        result = await self.session.execute(statement)
        notifications = result.scalars().all()
        return list(notifications)

    async def get_by_repeat(self) -> List[Notification]:
        statement = select(Notification).where(Notification.is_repeating == True)
        result = await self.session.execute(statement)
        notifications = result.scalars().all()
        return list(notifications)
