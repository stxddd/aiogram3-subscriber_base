from sqlalchemy import select
from sqlalchemy.sql import func
from sqlalchemy import desc, cast, Date

from bot.database.dao.base import BaseDAO
from bot.database.database import async_session_maker
from bot.database.tables.clients.models import Client


class ClientDAO(BaseDAO):
    model = Client

    from sqlalchemy.future import select

    @classmethod
    async def count_all_prices(cls, table_id):
        async with async_session_maker() as session:
            query = select(func.sum(cls.model.price)).where(
                cls.model.table_id == table_id
            )
            result = await session.execute(query)
            total_sum = result.scalar() or 0
            return total_sum

    @classmethod
    async def find_all_order_by(cls, table_id):
        async with async_session_maker() as session:
            query = select(cls.model).where(
                cls.model.table_id == table_id
            ).order_by(
                cls.model.date_to.asc()     
            )
            result = await session.execute(query)
            return result.scalars().all() 
