import os
from datetime import datetime
from typing import Optional, LiteralString

import aiofiles.os as aios

from dto.group_dto import CreateGroupDTO
from infrastructure.models import Group
from repositories import student_repository
from repositories.group_repository import GroupRepository


class GroupService:
    def __init__(self, group_repository: GroupRepository):
        self.group_repository = group_repository

    # GroupService methods
    async def create(self, dto: CreateGroupDTO) -> Group:
        group = await self.get_by_shortname(dto.shortname)
        if group is not None:
            raise ValueError('Group already exists')

        group = Group(
            short_name=dto.shortname,
            specialty=dto.specialty,
            department=dto.department,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        return await self.group_repository.create(group)

    async def update_user_count(self, group_id: int) -> Group:
        group = await self.get_by_id(group_id)
        if group is None:
            raise ValueError('Group not found')

        group.user_count += 1
        group.updated_at = datetime.now()

        return await self.group_repository.update(group)

    async def delete(self, group_id: int) -> None:
        group = await self.get_by_id(group_id)
        if group is None:
            raise ValueError('Group not found')

        await self.group_repository.delete(group)

    async def get_by_shortname(self, shortname: str) -> Optional[Group]:
        return await self.group_repository.get_by_shortname(shortname)

    async def get_by_id(self, group_id: int) -> Optional[Group]:
        return await self.group_repository.get_by_id(group_id)

    async def get_all(self) -> list[Group]:
        return await self.group_repository.get_all()
