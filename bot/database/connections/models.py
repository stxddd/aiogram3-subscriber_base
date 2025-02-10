from sqlalchemy import String, Column, ForeignKey, Integer

from bot.database.database import Base


class Connection(Base):
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True)
    user_tg_id = Column(ForeignKey('users.tg_id', ondelete="CASCADE"))
    os = Column(String(16), nullable=False)
    nickname = Column(String(32), nullable=False)
    link = Column(String, nullable=True)
