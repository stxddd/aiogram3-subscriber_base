from sqlalchemy import select
from sqlalchemy import cast, String

from bot.database.dao.base import BaseDAO
from bot.database.database import async_session_maker
from bot.database.clients.models import Client


class ClientDAO(BaseDAO):
    model = Client

    @classmethod
    async def search_all(cls, query: str):
        async with async_session_maker() as session:
            stmt = select(cls.model).where(
                cls.model.username.ilike(f"%{query}%") | 
                cast(cls.model.tg_id, String).ilike(f"%{query}%")
            )
            
            result = await session.execute(stmt)
            return result.scalars().all()
