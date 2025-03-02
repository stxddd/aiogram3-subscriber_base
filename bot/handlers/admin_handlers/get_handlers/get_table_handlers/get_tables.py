from aiogram import F, Router
from aiogram.types import Message

from bot.database.tables.dao import TableDAO
from bot.database.users.dao import UserDAO
from bot.keyboards.admin_keyboards.inline.table_keyboards import get_my_tables_keyboard
from bot.templates.admin_templates.keyboards_templates import my_tables_text
from bot.templates.user_templates.errors_templates import auth_error
from bot.templates.admin_templates.messages_templates import (
    our_tables_message,
    table_are_missing_message,
)
from bot.decorators.admin_required import admin_required

router = Router()


@router.message(F.text == my_tables_text)
@admin_required
async def handle_get_tables(message: Message):
    user = await UserDAO.find_one_or_none(tg_id=message.from_user.id)
    
    if not user:
        return await message.answer(auth_error)
    
    tables = await TableDAO.find_all(user_id=user.id)

    if tables:
        return await message.answer(
            our_tables_message,
            reply_markup=await get_my_tables_keyboard(user_id=user.id),
        )

    return await message.answer(table_are_missing_message)
