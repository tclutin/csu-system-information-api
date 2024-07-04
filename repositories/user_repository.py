from sqlalchemy.future import select
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        return user

    async def delete(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()

    async def get_all(self) -> List[User]:
        statement = select(User)
        result = await self.session.execute(statement)
        users = result.scalars().all()
        return list(users)

    async def get_by_username(self, username: str) -> Optional[User]:
        statement = select(User).where(User.username == username)
        result = await self.session.execute(statement)
        return result.scalar()

    async def get_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalar()
