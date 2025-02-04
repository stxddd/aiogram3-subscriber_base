import re
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards.inline.line_keyboards import get_lines_for_edit, get_lines_data_unit_to_edit
from bot.templates.messages_templates import (
    one_line_message,
    pick_line_for_edit_message,
    table_has_no_lines_message,
    impossible_to_edit_line_message
)
from bot.templates.errors_templates import table_dose_not_exists_error
from bot.database.tables.clients.dao import ClientDAO
from bot.database.tables.dao import TableDAO

router = Router()

EDIT_DATA_PATTERN = r"^edit_data_(\d+)_(.+)$"
GET_LINE_TO_EDIT_PATTERN = r"^get_line_to_edit_(\d+)_(.+)$"


@router.callback_query(F.data.regexp(EDIT_DATA_PATTERN))
async def handle_get_line_to_edit(callback: CallbackQuery):
    await callback.answer()

    match = re.match(EDIT_DATA_PATTERN, callback.data)
    table_id = int(match.group(1))
    table_name = match.group(2)

    table = await TableDAO.find_one_or_none(id=table_id)
    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    lines = await ClientDAO.find_all(table_id=table_id)
    if not lines:
        return await callback.message.answer(table_has_no_lines_message(table_name=table_name))

    await callback.message.answer(pick_line_for_edit_message, reply_markup=await get_lines_for_edit(table_id=table_id, table_name=table_name))


@router.callback_query(F.data.regexp(GET_LINE_TO_EDIT_PATTERN))
async def handle_edit_line(callback: CallbackQuery):
    await callback.answer()

    match = re.match(GET_LINE_TO_EDIT_PATTERN, callback.data)
    line_id = int(match.group(1))
    table_name = match.group(2)

    line = await ClientDAO.find_one_or_none(id=line_id)
    if not line:
        return await callback.message.answer(impossible_to_edit_line_message)

    await callback.message.answer(
        one_line_message(line=line, table_name=table_name),
        reply_markup=await get_lines_data_unit_to_edit(line_id=line_id, table_name=table_name)
    )
