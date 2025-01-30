from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from bot.config import settings



engine = create_async_engine(settings.DATABASE_URL)

async_session_maker = sessionmaker(
    engine, autocommit=False, autoflush=False, class_=AsyncSession, expire_on_commit=False, close_resets_only=False
)


class Base(DeclarativeBase):
    pass
