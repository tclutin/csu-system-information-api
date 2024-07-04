from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.models import Student


class StudentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, student: Student) -> Student:
        self.session.add(student)
        await self.session.commit()
        return student

    async def delete(self, student: Student) -> None:
        await self.session.delete(student)
        await self.session.commit()

    async def get_all(self) -> List[Student]:
        statement = select(Student)
        result = await self.session.execute(statement)
        students = result.scalars().all()
        return list(students)

    async def get_students_by_group_id(self, group_id: str) -> List[Student]:
        statement = select(Student).where(Student.group_id == group_id)
        result = await self.session.execute(statement)
        students = result.scalars().all()
        return list(students)

    async def get_student_by_id(self, student_id: int) -> Student:
        statement = select(Student).where(Student.student_id == student_id)
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def get_by_tgchat_id(self, tgchat_id: int) -> Optional[Student]:
        statement = select(Student).where(Student.tgchat_id == tgchat_id)
        result = await self.session.execute(statement)
        return result.scalar()
