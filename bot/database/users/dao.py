from bot.database.dao.base import BaseDAO
from bot.database.users.models import User


class UsersDAO(BaseDAO):
    model = User