from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.database.users.dao import UserDAO
from bot.keyboards.reply.main_keyboards  import main_keyboard
from bot.templates.messages_templates import welcome_message

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message):
    tg_id = message.from_user.id 

    user = await UserDAO.find_one_or_none(tg_id=tg_id)

    if not user:
        user = await UserDAO.add(tg_id=message.from_user.id)
    return await message.answer(welcome_message, reply_markup=main_keyboard)