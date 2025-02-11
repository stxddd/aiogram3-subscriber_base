import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.database.tables.dao import TableDAO
from bot.keyboards.admin_keyboards.inline.utils_keyboards import yes_or_not_delte_table_keyboard
from bot.templates.admin_templates.errors_templates import table_dose_not_exists_error
from bot.templates.admin_templates.messages_templates import (
    are_you_sure_to_delete_table_message,
    table_are_deleted_message,
    table_are_not_deleted_message,
)
from bot.decorators.admin_required import admin_required

router = Router()

PREPARE_TO_DELTE_TABLE_PATTERN = r"^prepare_to_delete_table_(\d+)$"
DELTE_TABLE_PATTERN = r"^delete_table_(\d+)$"


@router.callback_query(F.data.regexp(PREPARE_TO_DELTE_TABLE_PATTERN))
async def handle_prepate_to_delete_table(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    match = re.match(PREPARE_TO_DELTE_TABLE_PATTERN, callback.data)
    table_id = int(match.group(1))

    table = await TableDAO.find_one_or_none(id=table_id)

    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    table_name = table.name

    await callback.message.answer(
        are_you_sure_to_delete_table_message(table_name),
        reply_markup=await yes_or_not_delte_table_keyboard(table_id=table_id),
    )


@router.callback_query(F.data.regexp(DELTE_TABLE_PATTERN))
async def handle_delete_table(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    match = re.match(DELTE_TABLE_PATTERN, callback.data)
    table_id = int(match.group(1))

    table = await TableDAO.find_one_or_none(id=table_id)

    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    table_name = table.name

    delte_table = await TableDAO.delete(id=table_id)

    if not delte_table:
        return await callback.message.answer(table_are_not_deleted_message(table_name))

    return await callback.message.answer(table_are_deleted_message(table_name))
