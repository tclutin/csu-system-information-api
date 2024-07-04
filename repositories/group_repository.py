from typing import List, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from infrastructure.models import Group


class GroupRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, group: Group) -> Group:
        self.session.add(group)
        await self.session.commit()
        return group

    async def delete(self, group: Group) -> None:
        await self.session.delete(group)
        await self.session.commit()

    async def update(self, group: Group) -> Group:
        statement = (
            update(Group)
            .where(Group.group_id == group.group_id)
            .values(
                short_name=group.short_name,
                specialty=group.specialty,
                department=group.department,
                user_count=group.user_count,
                updated_at=group.updated_at
            )
            .returning(Group)
        )

        result = await self.session.execute(statement)
        updated_group = result.scalar()

        await self.session.commit()
        return updated_group

    async def get_all(self) -> List[Group]:
        statement = select(Group)
        result = await self.session.execute(statement)
        groups = result.scalars().all()
        return list(groups)

    async def get_by_id(self, group_id: int) -> Optional[Group]:
        statement = select(Group).where(Group.group_id == group_id)
        result = await self.session.execute(statement)
        return result.scalar()

    async def get_by_shortname(self, shortname: str) -> Optional[Group]:
        statement = select(Group).where(Group.short_name == shortname)
        result = await self.session.execute(statement)
        return result.scalar()
