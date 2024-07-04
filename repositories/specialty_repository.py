from sqlalchemy.future import select
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.models import User, Department, Specialty


class SpecialtyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, specialty: Specialty) -> Specialty:
        self.session.add(specialty)
        await self.session.commit()
        return specialty

    async def delete(self, specialty: Specialty) -> None:
        await self.session.delete(specialty)
        await self.session.commit()

    async def get_by_name(self, specialty_name: str) -> Optional[Specialty]:
        statement = select(Specialty).where(Specialty.specialty_name == specialty_name)
        result = await self.session.execute(statement)
        return result.scalar()

    async def get_all(self) -> List[Specialty]:
        statement = select(Specialty)
        result = await self.session.execute(statement)
        specialties = result.scalars().all()
        return list(specialties)
