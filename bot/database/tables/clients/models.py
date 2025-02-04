from sqlalchemy import Column, ForeignKey, Integer, String

from bot.database.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    table_id = Column(ForeignKey("tables.id", ondelete="CASCADE"))
    name = Column(String(32), nullable=False)
    price = Column(Integer, nullable=False)
    date_from = Column(String(20), nullable=False)
    date_to = Column(String(20), nullable=False)
    days_late = Column(Integer, default=0)
