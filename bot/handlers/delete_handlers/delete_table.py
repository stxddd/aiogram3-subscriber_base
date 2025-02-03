import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.handlers.post_handlers.add_data_to_table import delete_message_safely
from bot.keyboards.inline.utils_keyboards import yes_or_not_delte_table_keyboard
from bot.templates.messages_templates import (
    are_you_sure_to_delete_table_message,
    table_are_deleted_message,
    table_are_not_deleted_message,
)
from bot.database.tables.dao import TableDAO
from bot.templates.errors_templates import table_dose_not_exists_error

router = Router()


@router.callback_query(F.data.regexp(r"^prepare_to_delete_table_(\d+)_(.+)$"))
async def handle_prepate_to_delete_table(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    match = re.match(r"^prepare_to_delete_table_(\d+)_(.+)$", callback.data)

    table_id = int(match.group(1))
    table_name = match.group(2)

    table = await TableDAO.find_all(id=table_id)
    
    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    message_sent = await callback.message.answer(
        are_you_sure_to_delete_table_message(table_name), 
        reply_markup= await yes_or_not_delte_table_keyboard(table_name=table_name, table_id=table_id)
    )
    await state.update_data(message_sent=message_sent.message_id)


@router.callback_query(F.data.regexp(r"^delete_table_(\d+)_(.+)$"))
async def handle_delete_table(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    match = re.match(r"^delete_table_(\d+)_(.+)$", callback.data)

    table_id = int(match.group(1))
    table_name = match.group(2)

    table = await TableDAO.find_all(id=table_id)

    if not table:
        return await callback.message.answer(table_are_not_deleted_message(table_name))
    
    delte_table = await TableDAO.delete(id=table_id)

    if not delte_table:
        return await callback.message.answer(table_are_not_deleted_message(table_name))
    
    data = await state.get_data()
    await delete_message_safely(callback.bot, callback.message.chat.id, data.get("message_sent")) 

    return await callback.message.answer(table_are_deleted_message(table_name))