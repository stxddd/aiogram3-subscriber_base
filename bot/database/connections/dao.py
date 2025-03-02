from sqlalchemy import select

from bot.database.dao.base import BaseDAO
from bot.database.connections.models import Connection
from bot.database.database import async_session_maker


class ConnectionDAO(BaseDAO):
    model = Connection

    @classmethod
    async def find_all_with_marzban_link(cls, client_id):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.marzban_link.isnot(None)).filter_by(client_id=client_id)
            result = await session.execute(query)
            return result.scalars().all()
    
    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()