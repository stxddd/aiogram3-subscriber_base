from sqlalchemy import BigInteger, Column, Integer, String

from bot.database.database import Base


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True)
    owner_tg_id = Column(BigInteger, nullable=False)
    name = Column(String(32), nullable=False)