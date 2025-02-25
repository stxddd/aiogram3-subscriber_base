from sqlalchemy import Column, ForeignKey, Integer, String

from bot.database.database import Base


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String(32), nullable=False)
