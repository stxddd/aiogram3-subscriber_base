from sqlalchemy import BigInteger, Column, Integer

from bot.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, nullable=False)
