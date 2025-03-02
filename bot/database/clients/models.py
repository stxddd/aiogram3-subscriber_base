from sqlalchemy import BigInteger, Column, Integer, String, ForeignKey

from bot.database.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, nullable=False, unique=True)
    table_id = Column(ForeignKey("tables.id", ondelete="CASCADE"), nullable=True)
    username = Column(String(32), nullable=False)
