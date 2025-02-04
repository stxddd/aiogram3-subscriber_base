import re
from aiogram import F, Router
from aiogram.types import CallbackQuery
from bot.database.tables.dao import TableDAO
from bot.database.tables.clients.dao import ClientDAO
from bot.keyboards.inline.table_keyboards import get_actions_with_table_keyboard
from bot.templates.messages_templates import all_table_lines_message, table_has_no_lines_message
from bot.templates.errors_templates import table_dose_not_exists_error
router = Router()

LOOK_ALL_CLIENTS_PATTERN = r"^look_all_table_data_(\d+)$"

@router.callback_query(F.data.regexp(LOOK_ALL_CLIENTS_PATTERN))
async def handle_look_all_lines(callback: CallbackQuery):
    await callback.answer()

    match = re.match(LOOK_ALL_CLIENTS_PATTERN, callback.data)
    table_id = int(match.group(1))

    table = await TableDAO.find_one_or_none(id=table_id)

    if not table:
        return await callback.message.answer(table_dose_not_exists_error)
    
    table_name = table.name

    clients = await ClientDAO.find_all(table_id=table_id)
    
    if not clients:
        return await callback.message.answer(table_has_no_lines_message(table_name))
    
    return await callback.message.answer(all_table_lines_message(clients, table_name), parse_mode="HTML", reply_markup = await get_actions_with_table_keyboard(table_id=table_id))