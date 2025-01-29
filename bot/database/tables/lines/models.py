from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String

from bot.database.database import Base


class Line(Base):
    __tablename__ = "lines"

    id = Column(Integer, primary_key=True)
    owner_tg_id = Column(BigInteger, nullable=False)
    table_id = Column(ForeignKey("tables.id"))
    subscriber_tg_id = Column(String(32), nullable=False)
    subscriber_price = Column(Integer, nullable=False)
    subscriber_date = Column(String(32), nullable=False)
