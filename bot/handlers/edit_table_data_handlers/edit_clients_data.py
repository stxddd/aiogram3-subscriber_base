import re

from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.database.tables.clients.dao import ClientDAO
from bot.database.tables.dao import TableDAO
from bot.keyboards.inline.line_keyboards import (
    get_lines_data_unit_to_edit,
    get_lines_for_edit,
)
from bot.templates.errors_templates import (
    client_does_not_exists_error,
    table_dose_not_exists_error,
)
from bot.templates.messages_templates import (
    one_line_message,
    pick_line_for_edit_message,
    table_has_no_lines_message,
)

router = Router()

EDIT_PAGE_PATTERN = r"^edit_page_(\d+)_(\d+)$"
EDIT_DATA_PATTERN = r"^edit_data_(\d+)$"
GET_LINE_TO_EDIT_PATTERN = r"^get_line_to_edit_(\d+)$"

@router.callback_query(F.data.regexp(EDIT_PAGE_PATTERN))
async def handle_pagination(callback: CallbackQuery):
    await callback.answer()

    match = re.match(EDIT_PAGE_PATTERN, callback.data)
    table_id = int(match.group(1))
    page = int(match.group(2))

    await callback.message.edit_reply_markup(
        reply_markup=await get_lines_for_edit(table_id=table_id, page=page)
    )


@router.callback_query(F.data.regexp(EDIT_DATA_PATTERN))
async def handle_get_line_to_edit(callback: CallbackQuery):
    await callback.answer()

    match = re.match(EDIT_DATA_PATTERN, callback.data)
    table_id = int(match.group(1))

    table = await TableDAO.find_one_or_none(id=table_id)
    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    table_name = table.name
    clients = await ClientDAO.find_all_order_by(table_id=table_id)

    if not clients:
        return await callback.message.answer(
            table_has_no_lines_message(table_name=table_name)
        )

    await callback.message.answer(
        pick_line_for_edit_message,
        reply_markup=await get_lines_for_edit(table_id=table_id, page=1),
    )


@router.callback_query(F.data.regexp(GET_LINE_TO_EDIT_PATTERN))
async def handle_edit_line(callback: CallbackQuery):
    await callback.answer()

    match = re.match(GET_LINE_TO_EDIT_PATTERN, callback.data)
    client_id = int(match.group(1))

    current_client = await ClientDAO.find_by_id(client_id)

    if not current_client:
        return await callback.message.answer(client_does_not_exists_error)

    table = await TableDAO.find_one_or_none(id=current_client.table_id)

    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    table_name = table.name

    await callback.message.answer(
        one_line_message(client=current_client, table_name=table_name),
        reply_markup=await get_lines_data_unit_to_edit(client_id=client_id),
    )
