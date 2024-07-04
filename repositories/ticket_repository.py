from typing import Optional, List

from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.models import Student, Ticket


class TicketRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, ticket: Ticket) -> Ticket:
        self.session.add(ticket)
        await self.session.commit()
        return ticket

    async def delete(self, ticket: Ticket) -> None:
        await self.session.delete(ticket)
        await self.session.commit()

    async def update(self, ticket: Ticket) -> Ticket:
        statement = (
            update(Ticket)
            .where(Ticket.ticket_id == ticket.ticket_id)
            .values(
                status=ticket.status,
                tgchat_id=ticket.tgchat_id,
                fullname=ticket.fullname,
                wish_group=ticket.wish_group,
                photo=ticket.photo,
                message=ticket.message,
                updated_at=ticket.updated_at,
            )
            .returning(Ticket)
        )

        result = await self.session.execute(statement)
        updated_group = result.scalar()

        await self.session.commit()
        return updated_group

    async def get_by_id(self, ticket_id: int) -> Optional[Ticket]:
        statement = select(Ticket).where(Ticket.ticket_id == ticket_id)
        result = await self.session.execute(statement)
        return result.scalar()

    async def get_active_by_tgchat_id(self, tgchat_id: int) -> Optional[Ticket]:
        statement = select(Ticket).where(and_(Ticket.tgchat_id == tgchat_id, Ticket.status == "open"))
        result = await self.session.execute(statement)
        return result.scalar()

    async def get_all_open(self) -> List[Ticket]:
        statement = select(Ticket).where(Ticket.status == "open")
        result = await self.session.execute(statement)
        tickets = result.scalars().all()
        return list(tickets)
