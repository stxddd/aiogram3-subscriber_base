from functools import wraps

from aiogram import types

from bot.database.users.dao import UserDAO
from bot.templates.user_templates.message_templates import rejected_message

def admin_required(func):
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        user_id = message.from_user.id
        user = await UserDAO.find_one_or_none(tg_id=user_id)

        if user and user.is_admin:
            return await func(message, *args, **kwargs)
        else:
            await message.answer(rejected_message)
            return
    return wrapper
