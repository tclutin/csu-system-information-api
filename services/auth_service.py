from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException
from jose import jwt, JWTError, ExpiredSignatureError
from jose.constants import ALGORITHMS
from passlib.context import CryptContext

from config.config import settings
from dto.user_dto import RegisterUserDTO, LoginUserDTO
from infrastructure.models import User


from services.user_service import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # AuthService methods
    async def register(self, dto: RegisterUserDTO) -> str:
        user = await self.user_service.create(dto)
        return self.create_access_token(data={"sub": user.username})

    async def login(self, dto: LoginUserDTO) -> str:
        user = await self.user_service.get_by_username(dto.username)
        if user is None:
            raise ValueError("Username not registered")

        if not self.pwd_context.verify(dto.password, user.hashed_password):
            raise ValueError("Invalid password")

        return self.create_access_token(data={"sub": user.username})

    async def me(self, username: str) -> User:
        user = await self.user_service.get_by_username(username)
        if user is None:
            raise ValueError("Username not registered")

        return user

    # JWT
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=ALGORITHMS.HS256)

    def verify_token(self, token: str) -> dict:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[ALGORITHMS.HS256])
        return payload

