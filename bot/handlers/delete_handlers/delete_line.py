import re

from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.database.tables.clients.dao import ClientDAO
from bot.database.tables.dao import TableDAO
from bot.keyboards.inline.utils_keyboards import yes_or_not_delte_line_keyboard
from bot.templates.errors_templates import (
    client_dose_not_exists_error,
    table_dose_not_exists_error,
)
from bot.templates.messages_templates import (
    are_you_sure_to_delete_line_message,
    line_are_deleted_message,
    line_are_not_deleted_message,
)

router = Router()

PREPARE_TO_DELETE_CLIENT_PATTERN = r"^prepare_to_delete_line_(\d+)$"
DELETE_CLIENT_PATTERN = r"^delete_line_(\d+)$"


@router.callback_query(F.data.regexp(PREPARE_TO_DELETE_CLIENT_PATTERN))
async def handle_add_line_to_table(callback: CallbackQuery):
    await callback.answer()

    match = re.match(PREPARE_TO_DELETE_CLIENT_PATTERN, callback.data)
    client_id = int(match.group(1))

    current_client = await ClientDAO.find_by_id(client_id)
    if not current_client:
        return await callback.message.answer(client_dose_not_exists_error)

    table = await TableDAO.find_one_or_none(id=current_client.table_id)

    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    table_name = table.name

    return await callback.message.answer(
        are_you_sure_to_delete_line_message(table_name=table_name, line=current_client),
        reply_markup=await yes_or_not_delte_line_keyboard(client_id=client_id),
    )


@router.callback_query(F.data.regexp(DELETE_CLIENT_PATTERN))
async def handle_line_name(callback: CallbackQuery):
    await callback.answer()

    match = re.match(DELETE_CLIENT_PATTERN, callback.data)
    client_id = int(match.group(1))

    current_client = await ClientDAO.find_by_id(client_id)
    if not current_client:
        return await callback.message.answer(client_dose_not_exists_error)

    table = await TableDAO.find_one_or_none(id=current_client.table_id)

    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    table_name = table.name

    delte_line = await ClientDAO.delete(id=client_id)

    if not delte_line:
        return await callback.message.answer(
            line_are_not_deleted_message(table_name=table_name, line=current_client)
        )

    return await callback.message.answer(
        line_are_deleted_message(line=current_client, table_name=table_name)
    )
