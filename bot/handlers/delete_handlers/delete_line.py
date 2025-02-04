import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards.inline.utils_keyboards import yes_or_not_delte_line_keyboard
from bot.templates.messages_templates import (
    are_you_sure_to_delete_line_message,
    line_are_deleted_message,
    line_are_not_deleted_message,
)
from bot.database.tables.clients.dao import ClientDAO
from bot.templates.errors_templates import client_dose_not_exists_error
router = Router()


@router.callback_query(F.data.regexp(r"^prepare_to_delete_line_(\d+)_(.+)$"))
async def handle_add_line_to_table(callback: CallbackQuery):
    await callback.answer()
    match = re.match(r"^prepare_to_delete_line_(\d+)_(.+)$", callback.data)

    line_id = int(match.group(1))
    line = await ClientDAO.find_one_or_none(id=line_id)
    
    if not line:
        return await callback.message.answer(client_dose_not_exists_error)

    table_name = match.group(2) 

    return await callback.message.answer(
        are_you_sure_to_delete_line_message(table_name=table_name, line=line),
          reply_markup= await yes_or_not_delte_line_keyboard(table_name=table_name, line_id=line_id)
    )


@router.callback_query(F.data.regexp(r"^delete_line_(\d+)_(.+)$"))
async def handle_line_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    match = re.match(r"^delete_line_(\d+)_(.+)$", callback.data)

    line_id = int(match.group(1))
    table_name = match.group(2)

    line = await ClientDAO.find_one_or_none(id=line_id)
    
    if not line:
        return await callback.message.answer(client_dose_not_exists_error)
    
    delte_line = await ClientDAO.delete(id=line_id)

    if not delte_line:
        return await callback.message.answer(line_are_not_deleted_message(table_name=table_name, line=line))

    return await callback.message.answer(line_are_deleted_message(table_name=table_name, line=line))