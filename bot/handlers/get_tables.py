from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.database.tables.dao import TableDAO
from bot.keyboards.tables import get_my_tables_keyboard
from bot.templates.messages import our_tables

router = Router()


@router.callback_query(F.data == "get_tables")
async def get_tables(callback: CallbackQuery):

    tg_id = callback.from_user.id

    tables = await TableDAO.find_all(owner_tg_id=tg_id)

    await callback.answer()

    try:
        return await callback.message.edit_text(
            our_tables, reply_markup=await get_my_tables_keyboard(owner_tg_id=tg_id)
        )
    except:
        return await callback.message.answer(
            our_tables, reply_markup=await get_my_tables_keyboard(owner_tg_id=tg_id)
        )