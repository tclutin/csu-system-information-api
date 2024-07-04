from sqlalchemy.future import select
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.models import User, Department


class DepartmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, department: Department) -> Department:
        self.session.add(department)
        await self.session.commit()
        return department

    async def delete(self, department: Department) -> None:
        await self.session.delete(department)
        await self.session.commit()

    async def get_by_name(self, department_name: str) -> Optional[Department]:
        statement = select(Department).where(Department.department_name == department_name)
        result = await self.session.execute(statement)
        return result.scalar()

    async def get_all(self) -> List[Department]:
        statement = select(Department)
        result = await self.session.execute(statement)
        departments = result.scalars().all()
        return list(departments)
