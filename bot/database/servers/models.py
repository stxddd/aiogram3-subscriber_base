from sqlalchemy import Column, Integer, String

from bot.database.database import Base

class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    port = Column(Integer, nullable=False, default=8000)
    count_of_clients = Column(Integer, default=0)
