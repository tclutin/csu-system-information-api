from datetime import datetime
from typing import Optional, List

from passlib.context import CryptContext

from dto.user_dto import RegisterUserDTO
from infrastructure.models import User
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # UserService methods
    async def create(self, dto: RegisterUserDTO) -> User:
        user = await self.get_by_username(dto.username)
        if user is not None:
            raise ValueError("Username already registered")

        user = await self.get_by_email(dto.email)
        if user is not None:
            raise ValueError("Email already registered")

        user = User(
            username=dto.username,
            email=dto.email,
            hashed_password=self.pwd_context.hash(dto.password),
            role=dto.role,
            fullname=dto.fullname,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        return await self.user_repository.create(user)

    async def delete(self, username: str) -> None:
        user = await self.get_by_username(username)
        if user is None:
            raise ValueError("User not found")

        await self.user_repository.delete(user)

    async def get_by_username(self, username: str) -> Optional[User]:
        return await self.user_repository.get_by_username(username)

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.user_repository.get_by_email(email)

    async def get_all(self) -> List[User]:
        return await self.user_repository.get_all()