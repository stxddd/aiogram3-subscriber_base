from sqlalchemy import Date, String, Column, Integer

from bot.database.database import Base


class Connection(Base):
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True)
    tg_id =  Column(Integer, nullable=False)
    tg_username = Column(String(32), nullable=False)
    os = Column(String(16), nullable=False)
    link = Column(String, nullable=True)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, default=0)

