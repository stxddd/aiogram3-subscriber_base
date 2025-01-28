from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from bot.database.users.dao import UsersDAO
from bot.keyboards.home import home_keyboard
from bot.templates.messages import main_menu, welcome_message

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    tg_id = message.from_user.id 

    user = await UsersDAO.find_one_or_none(tg_id=tg_id)

    if not user:
        user = await UsersDAO.add(tg_id=message.from_user.id)
    return await message.answer(welcome_message, reply_markup=home_keyboard)


@router.callback_query(F.data == "main_menu")
async def menu(callback: CallbackQuery):
    await callback.answer()

    return await callback.message.edit_text(main_menu, reply_markup=home_keyboard)