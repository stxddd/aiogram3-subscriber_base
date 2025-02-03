from sqlalchemy import select
from bot.database.dao.base import BaseDAO
from bot.database.tables.lines.models import Client
from bot.database.database import async_session_maker

class ClientDAO(BaseDAO):
    model = Client
        
    @classmethod
    async def check_expired(cls, today):
        async with async_session_maker() as session:
            result = await session.execute(select(cls.model).where(cls.model.date_to == today))
            expired_models = result.scalars().all()
