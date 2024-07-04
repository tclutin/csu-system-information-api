from typing import List, Optional

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from dto.faq_dto import CreateFAQDTO
from infrastructure.models import FAQ


class FAQRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, faqs: List[FAQ]) -> List[FAQ]:
        self.session.add_all(faqs)
        await self.session.commit()
        return faqs

    async def delete(self, faq: FAQ) -> None:
        await self.session.delete(faq)
        await self.session.commit()

    async def get_all(self) -> List[FAQ]:
        statement = select(FAQ)
        result = await self.session.execute(statement)
        faqs = result.scalars().all()
        return list(faqs)

    async def get_by_question(self, question: str) -> Optional[FAQ]:
        statement = select(FAQ).where(FAQ.question == question)
        result = await self.session.execute(statement)
        return result.scalar()

    async def get_by_id(self, faq_id: int) -> Optional[FAQ]:
        statement = select(FAQ).where(FAQ.faq_id == faq_id)
        result = await self.session.execute(statement)
        return result.scalar()