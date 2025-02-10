from bot.database.dao.base import BaseDAO
from bot.database.connections.models import Connection


class ConnectionDAO(BaseDAO):
    model = Connection
