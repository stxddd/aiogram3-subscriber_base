from sqlalchemy import Date, ForeignKey, String, Column, Integer

from bot.database.database import Base


class Connection(Base):
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True)
    client_id = Column(ForeignKey("clients.id", ondelete="CASCADE"))
    name = Column(String(64), nullable=False)
    os_name = Column(String(16), nullable=False)
    marzban_link = Column(String, nullable=True)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, default=0)

