from sqlalchemy import select
from bot.database.dao.base import BaseDAO
from bot.database.servers.models import Server



class ServerDAO(BaseDAO):
    model = Server
