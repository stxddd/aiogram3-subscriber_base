from bot.database.dao.base import BaseDAO
from bot.database.users.models import User

class UserDAO(BaseDAO):
    model = User
