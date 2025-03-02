from datetime import date

from sqlalchemy import BigInteger, Boolean, Column, Date, Integer

from bot.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, nullable=False, unique=True)
    is_admin = Column(Boolean, default=False)
    marzban_requests_today = Column(Integer, default=0)
    last_marzban_request = Column(Date, default=date.today())

    def reset_if_new_day(self):
        if self.last_marzban_request != date.today():
            self.marzban_requests_today = 0
            self.last_marzban_request = date.today()
        