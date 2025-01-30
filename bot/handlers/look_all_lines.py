import re
from aiogram import F, Router
from aiogram.types import CallbackQuery
from bot.database.tables.lines.dao import LineDAO
from bot.templates.messages import all_table_lines_message, table_has_no_lines_message

router = Router()


@router.callback_query(F.data.regexp(r"^look_all_table_data_(\d+)_(.+)$"))
async def handle_look_all_lines(callback: CallbackQuery):
    await callback.answer()

    match = re.match(r"^look_all_table_data_(\d+)_(.+)$", callback.data)
    table_id = int(match.group(1))
    table_name = match.group(2)

    lines = await LineDAO.find_all(table_id=table_id)
    
    if not lines:
        return await callback.message.answer(table_has_no_lines_message(table_name))
    
    return await callback.message.answer(all_table_lines_message(lines, table_name), parse_mode="HTML")
