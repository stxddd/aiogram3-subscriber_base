import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.database.tables.dao import TableDAO
from bot.keyboards.inline.table_keyboards import get_actions_with_table_keyboard
from bot.templates.messages_templates import table_name_message
from bot.templates.errors_templates import table_dose_not_exists_error

router = Router()


@router.callback_query(F.data.regexp(r"^get_(\d+)_(.+?)_table$"))
async def actions_with_table(callback: CallbackQuery, state: FSMContext):
    match = re.match(r"^get_(\d+)_(.+?)_table$", callback.data)
    await callback.answer()

    table_id = int(match.group(1))
    table_name = match.group(2)

    table = await TableDAO.find_all(id=table_id, name = table_name)
    
    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    message_sent = await callback.message.answer(table_name_message(table_name), reply_markup = await get_actions_with_table_keyboard(table_id, table_name))

    await state.update_data(table_id=table_id, table_name=table_name, message_sent_id = callback.message.message_id)