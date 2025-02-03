import re

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from bot.database.tables.dao import TableDAO
from bot.templates.messages_templates import select_an_action_for_the_table_message
from bot.keyboards.inline.table_keyboards import get_edit_actions_with_table_keyboard
from bot.templates.errors_templates import table_dose_not_exists_error

router = Router()


class Form(StatesGroup):
    waiting_for_name_data = State()


@router.callback_query(F.data.regexp(r"^edit_table_(\d+)_(.+)$"))
async def handle_edit_table_actions(callback: CallbackQuery):
    await callback.answer()

    match = re.match(r"^edit_table_(\d+)_(.+)$", callback.data)
    
    table_id = int(match.group(1))
    table_name = match.group(2)

    table = await TableDAO.find_all(id=table_id, name = table_name)
    
    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    await callback.message.answer(
        select_an_action_for_the_table_message(table_name),
        reply_markup = await get_edit_actions_with_table_keyboard(
        table_name=table_name, 
        table_id=table_id
    ))