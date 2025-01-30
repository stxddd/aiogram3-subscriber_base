import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards.inline.utils import yes_or_not_delte_table_keyboard
from bot.templates.messages import (
    are_you_sure_to_delete_table_message,
    table_are_deleted,
    table_are_not_deleted,
)
from bot.utils.excel_generator import ExcelCRUD

from bot.database.tables.dao import TableDAO
from bot.database.tables.lines.dao import LineDAO

router = Router()



@router.callback_query(F.data.regexp(r"^prepare_to_delete_table_(\d+)_(.+)$"))
async def handle_add_line_to_table(callback: CallbackQuery):
    await callback.answer()
    match = re.match(r"^prepare_to_delete_table_(\d+)_(.+)$", callback.data)

    table_id = int(match.group(1))
    table_name = match.group(2)

    return await callback.message.answer(are_you_sure_to_delete_table_message(table_name), reply_markup= await yes_or_not_delte_table_keyboard(table_name=table_name, table_id=table_id))


@router.callback_query(F.data.regexp(r"^delete_table_(\d+)_(.+)$"))
async def handle_line_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    match = re.match(r"^delete_table_(\d+)_(.+)$", callback.data)

    table_id = int(match.group(1))
    table_name = match.group(2)

    table = await TableDAO.find_all(id=table_id)

    lines = await LineDAO.find_all(table_id=table_id)

    lines_to_delte = await LineDAO.delete(table_id=table_id)

    if not table:
        return await callback.message.answer(table_are_not_deleted(table_name))

    delte_table = await TableDAO.delete(id=table_id)

    if not delte_table:
        return await callback.message.answer(table_are_not_deleted(table_name))
    
    delete_excel_table = await ExcelCRUD.delete_excel_file(
        table_id=table_id,
        table_name=table_name,
        tg_id=callback.from_user.id
    )

    return await callback.message.answer(table_are_deleted(table_name))