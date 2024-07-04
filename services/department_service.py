from datetime import datetime
from typing import Optional, List

from passlib.context import CryptContext

from dto.department_dto import CreateDepartmentDTO
from dto.user_dto import RegisterUserDTO
from infrastructure.models import User, Department
from repositories.department_repository import DepartmentRepository
from repositories.user_repository import UserRepository


class DepartmentService:
    def __init__(self, department_repository: DepartmentRepository):
        self.department_repository = department_repository

    # DepartmentService methods
    async def create(self, dto: CreateDepartmentDTO) -> Department:
        department = await self.get_by_name(dto.department_name)
        if department is not None:
            raise ValueError('Department already exists')

        department = Department(
            department_name=dto.department_name
        )

        return await self.department_repository.create(department)

    async def delete(self, department_name: str) -> None:
        department = await self.get_by_name(department_name)
        if department is None:
            raise ValueError('Department does not exist')

        await self.department_repository.delete(department)

    async def get_by_name(self, department_name: str) -> Optional[Department]:
        return await self.department_repository.get_by_name(department_name)

    async def get_all(self) -> List[Department]:
        return await self.department_repository.get_all()
