import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from bot.keyboards.inline.line_keyboards import get_lines_for_edit, get_lines_data_unit_to_edit
from bot.templates.messages_templates import (
    one_line_message, 
    pick_line_for_edit_message,
    table_has_no_lines_message,
    impossible_to_edit_line_message
)
from bot.database.tables.lines.dao import LineDAO

router = Router()


@router.callback_query(F.data.regexp(r"^edit_data_(\d+)_(.+)$"))
async def handle_get_line_to_edit(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    match = re.match(r"^edit_data_(\d+)_(.+)$", callback.data)

    table_id = int(match.group(1))
    table_name = match.group(2)

    lines = await LineDAO.find_all(table_id=table_id)

    if not lines:
        return await callback.message.answer(table_has_no_lines_message(table_name=table_name))

    await callback.message.answer(pick_line_for_edit_message, reply_markup= await get_lines_for_edit(table_id=table_id, table_name=table_name))


@router.callback_query(F.data.regexp(r"^get_line_to_edit_(\d+)_(.+)$"))
async def handle_edit_line(callback: CallbackQuery):
    await callback.answer()
    match = re.match(r"^get_line_to_edit_(\d+)_(.+)$", callback.data)

    line_id = int(match.group(1))
    table_name = match.group(2)

    line = await LineDAO.find_one_or_none(id = line_id)
    if not line:
        return await callback.message.answer(impossible_to_edit_line_message)

    await callback.message.answer(one_line_message(line=line, table_name=table_name), reply_markup = await get_lines_data_unit_to_edit(line_id=line_id, table_name=table_name))

