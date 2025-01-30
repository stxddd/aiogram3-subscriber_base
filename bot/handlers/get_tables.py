from aiogram import F, Router
from aiogram.types import Message

from bot.database.tables.dao import TableDAO
from bot.keyboards.inline.tables import get_my_tables_keyboard
from bot.templates.keyboards import my_tables_text
from bot.templates.messages import our_tables, table_are_missing_text

router = Router()


@router.message(F.text == my_tables_text)
async def handle_get_tables(message: Message):

    tg_id = message.from_user.id

    tables = await TableDAO.find_all(owner_tg_id=tg_id)

    if tables:
        return await message.answer(our_tables, reply_markup=await get_my_tables_keyboard(owner_tg_id=tg_id))
    return await message.answer(table_are_missing_text)