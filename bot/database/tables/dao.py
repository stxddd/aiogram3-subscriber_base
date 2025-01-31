from bot.database.dao.base import BaseDAO
from bot.database.tables.models import Table
from sqlalchemy import select
from bot.database.database import async_session_maker

class TableDAO(BaseDAO):
    model = Table

    @classmethod
    async def update(cls, model_id: int, **data):
        async with async_session_maker() as session:
            query = await session.execute(select(cls.model).filter_by(id=model_id))
            result = query.scalars().first()
            if result:
                existing_query = await session.execute(
                    select(cls.model)
                    .filter_by(name=data["name"], owner_tg_id=result.owner_tg_id)
                    .filter(cls.model.id != model_id)  
                )
                existing_object = existing_query.scalars().first()
                if existing_object:
                    return None
                for key, value in data.items():
                    setattr(result, key, value)
                await session.commit()
                return result
            return None