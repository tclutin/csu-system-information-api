from datetime import datetime
from typing import Optional, List

from passlib.context import CryptContext

from dto.department_dto import CreateDepartmentDTO
from dto.specialty_dto import CreateSpecialtyDTO
from dto.user_dto import RegisterUserDTO
from infrastructure.models import User, Department, Specialty
from repositories.department_repository import DepartmentRepository
from repositories.specialty_repository import SpecialtyRepository
from repositories.user_repository import UserRepository


class SpecialtyService:
    def __init__(self, specialty_repository: SpecialtyRepository):
        self.specialty_repository = specialty_repository

    # SpecialtyService methods
    async def create(self, dto: CreateSpecialtyDTO) -> Specialty:
        specialty = await self.get_by_name(dto.specialty_name)
        if specialty is not None:
            raise ValueError('Specialty already exists')

        specialty = Specialty(
            specialty_name=dto.specialty_name
        )

        return await self.specialty_repository.create(specialty)

    async def delete(self, specialty_name: str) -> None:
        specialty = await self.get_by_name(specialty_name)
        if specialty is None:
            raise ValueError('Specialty not found')

        await self.specialty_repository.delete(specialty)

    async def get_by_name(self, specialty_name: str) -> Optional[Specialty]:
        return await self.specialty_repository.get_by_name(specialty_name)

    async def get_all(self) -> List[Specialty]:
        return await self.specialty_repository.get_all()
