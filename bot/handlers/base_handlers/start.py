from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.config import settings
from bot.database.users.dao import UserDAO
from bot.keyboards.admin_keyboards.reply.main_keyboards import main_keyboard as main_admin_keyboard
from bot.keyboards.user_keyboards.reply.main_keyboards import main_keyboard as main_user_keyboard
from bot.templates.user_templates.errors_templates import auth_error
from bot.templates.admin_templates.messages_templates import admin_welcome_message
from bot.templates.user_templates.message_templates import welcome_message

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message):
    "Создает user'a в бд, определяет его роль, отправляет приветственное сообщение в зависимости от неё" 
    tg_id = message.from_user.id
    
    admin_tg_id = settings.ADMIN_TG_ID
    user = await UserDAO.find_one_or_none(tg_id=tg_id)

    if not user:
        added_user = await UserDAO.add(
                tg_id=message.from_user.id,
                downloads_today = 0,
                marzban_requests_today = 0,
            )
        if not added_user:
            return await message.answer(auth_error)
        
        user = await UserDAO.find_one_or_none(id=added_user.id)
        if not user:
            return await message.answer(auth_error)

    if tg_id == admin_tg_id:
        user = await UserDAO.update(model_id = user.id, is_admin = True)

    if user.is_admin:
        return await message.answer(admin_welcome_message, reply_markup=main_admin_keyboard)
    else:
        return await message.answer(welcome_message, reply_markup=main_user_keyboard)
    