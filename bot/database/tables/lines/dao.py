from bot.database.dao.base import BaseDAO
from bot.database.tables.lines.models import Line


class LineDAO(BaseDAO):
    model = Line
