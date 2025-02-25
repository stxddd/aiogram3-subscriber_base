from sqlalchemy import select
from sqlalchemy.sql import func
from sqlalchemy import desc, cast, Date

from bot.database.dao.base import BaseDAO
from bot.database.database import async_session_maker
from bot.database.clients.models import Client


class ClientDAO(BaseDAO):
    model = Client

    from sqlalchemy.future import select

    # @classmethod
    # async def count_all_prices(cls, table_id):
    #     async with async_session_maker() as session:
    #         query = select(func.sum(cls.model.price)).where(
    #             cls.model.table_id == table_id
    #         )
    #         result = await session.execute(query)
    #         total_sum = result.scalar() or 0
    #         return total_sum


