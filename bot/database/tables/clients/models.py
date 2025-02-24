from sqlalchemy import Column, ForeignKey, Integer, String, Date

from bot.database.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, nullable=False, unique=True)
    table_id = Column(ForeignKey("tables.id", ondelete="CASCADE"))
    name = Column(String(32), nullable=False)

    