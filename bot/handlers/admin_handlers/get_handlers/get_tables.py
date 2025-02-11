from aiogram import F, Router
from aiogram.types import Message

from bot.database.tables.dao import TableDAO
from bot.keyboards.admin_keyboards.inline.table_keyboards import get_my_tables_keyboard
from bot.templates.admin_templates.keyboards_templates import my_tables_text
from bot.templates.admin_templates.messages_templates import (
    our_tables_message,
    table_are_missing_message,
)
from bot.decorators.admin_required import admin_required

router = Router()


@router.message(F.text == my_tables_text)
@admin_required
async def handle_get_tables(message: Message):
    tg_id = message.from_user.id

    tables = await TableDAO.find_all(user_tg_id=tg_id)

    if tables:
        return await message.answer(
            our_tables_message,
            reply_markup=await get_my_tables_keyboard(user_tg_id=tg_id),
        )

    return await message.answer(table_are_missing_message)
