from datetime import date

from sqlalchemy import BigInteger, Column, Date, Integer

from bot.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, nullable=False, unique=True)
    downloads_today = Column(Integer, default=0)
    last_download_date = Column(Date, default=date.today())

    def reset_if_new_day(self):
        if self.last_download_date != date.today():
            self.downloads_today = 0
            self.last_download_date = date.today()
