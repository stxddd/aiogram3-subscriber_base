from bot.database.dao.base import BaseDAO
from bot.database.tables.models import Table


class TableDAO(BaseDAO):
    model = Table
