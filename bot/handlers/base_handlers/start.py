from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.config import settings
from bot.database.users.dao import UserDAO
from bot.keyboards.reply.main_keyboards import main_keyboard
from bot.templates.messages_templates import welcome_message

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message):
   
    tg_id = message.from_user.id

    admin = await UserDAO.find_one_or_none(tg_id=tg_id)

    if not admin:
        added_admin = await UserDAO.add(tg_id=message.from_user.id)
        admin = await UserDAO.find_one_or_none(id=added_admin.id)

    if tg_id in set(map(int, settings.ADMIN_IDS.split(","))):
        admin = await UserDAO.update(model_id = admin.id, is_admin=True)

    if admin.is_admin:
        return await message.answer(welcome_message, reply_markup=main_keyboard)
    else:
        return await message.answer('У вас нет доступа.')
    

