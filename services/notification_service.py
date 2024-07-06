from datetime import datetime
from typing import List, Optional

from dto.notification_dto import CreateNotificationDTO
from infrastructure.models import Notification
from repositories.notification_repository import NotificationRepository


class NotificationService:
    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository

    async def create(self, tgchat_id: int, dto: CreateNotificationDTO):
        if dto.is_repeating:
            if dto.time is None:
                raise ValueError("Time is required")

            if dto.day_of_week is None:
                raise ValueError("Day of week is required")

            if dto.day_of_week < 0 or dto.day_of_week > 6:
                raise ValueError("Day of week must be between 1 and 7")

            if dto.week_parity is None:
                raise ValueError("Week parity is required")

            if dto.week_parity != "odd" and dto.week_parity != "even":
                raise ValueError("Week parity must be 'odd' or 'even'")

            time = datetime.strptime(dto.time, '%H:%M').time()

            notification = Notification(
                tgchat_id=tgchat_id,
                is_repeating=dto.is_repeating,
                day_of_week=dto.day_of_week,
                time=time,
                week_parity=dto.week_parity,
                message=dto.message,
                created_at=datetime.now(),
            )

            await self.notification_repository.create(notification)

        else:
            if dto.date is None:
                raise ValueError("Date is required")

            notification = Notification(
                tgchat_id=tgchat_id,
                is_repeating=dto.is_repeating,
                message=dto.message,
                date=dto.date.replace(tzinfo=None),
                created_at=datetime.now(),
            )

            await self.notification_repository.create(notification)

    async def delete(self, notification_id: int) -> None:
        notification = await self.get_by_id(notification_id)
        if notification is None:
            raise ValueError("Notification not found")

        await self.notification_repository.delete(notification)

    async def get_by_id(self, notification_id: int) -> Optional[Notification]:
        return await self.notification_repository.get_by_id(notification_id)

    async def get_all_by_tgchat_id(self, tgchat_id: int) -> List[Notification]:
        return await self.notification_repository.get_by_tgchat_id(tgchat_id)

    async def get_by_repeat(self) -> List[Notification]:
        return await self.notification_repository.get_by_repeat()
