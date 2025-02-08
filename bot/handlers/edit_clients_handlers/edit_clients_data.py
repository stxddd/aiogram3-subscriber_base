import re

from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.database.tables.clients.dao import ClientDAO
from bot.database.tables.dao import TableDAO
from bot.keyboards.inline.clients_keyboards import (
    get_clients_data_unit_to_edit,
    get_clients_for_edit,
)
from bot.templates.errors_templates import (
    client_does_not_exists_error,
    table_dose_not_exists_error,
)
from bot.templates.messages_templates import (
    one_client_message,
    table_base_info_message,
    table_has_no_clients_message,
)

router = Router()

EDIT_PAGE_PATTERN = r"^edit_page_(\d+)_(\d+)$"
EDIT_CLIENT_PATTERN = r"^edit_client_(\d+)$"
GET_CLIENT_TO_EDIT_PATTERN = r"^get_client_to_edit_(\d+)$"

@router.callback_query(F.data.regexp(EDIT_PAGE_PATTERN))
async def handle_pagination(callback: CallbackQuery):
    await callback.answer()

    match = re.match(EDIT_PAGE_PATTERN, callback.data)
    table_id = int(match.group(1))
    page = int(match.group(2))

    await callback.message.edit_reply_markup(
        reply_markup=await get_clients_for_edit(table_id=table_id, page=page)
    )


@router.callback_query(F.data.regexp(EDIT_CLIENT_PATTERN))
async def handle_get_client_to_edit(callback: CallbackQuery):
    await callback.answer()

    match = re.match(EDIT_CLIENT_PATTERN, callback.data)
    table_id = int(match.group(1))

    table = await TableDAO.find_one_or_none(id=table_id)
    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    table_name = table.name
    clients = await ClientDAO.find_all_order_by(table_id=table_id)

    if not clients:
        return await callback.message.answer(
            table_has_no_clients_message(table_name=table_name)
        )

    clients_count = len(clients)

    all_prices = await ClientDAO.count_all_prices(table_id=table_id)

    if not all_prices:
        return await callback.message.answer(client_does_not_exists_error)

    await callback.message.answer(
        table_base_info_message(table_name=table_name, clients_count=clients_count, all_prices=all_prices),
        reply_markup=await get_clients_for_edit(table_id=table_id, page=1),
    )


@router.callback_query(F.data.regexp(GET_CLIENT_TO_EDIT_PATTERN))
async def handle_edit_client(callback: CallbackQuery):
    await callback.answer()

    match = re.match(GET_CLIENT_TO_EDIT_PATTERN, callback.data)
    client_id = int(match.group(1))

    current_client = await ClientDAO.find_by_id(client_id)

    if not current_client:
        return await callback.message.answer(client_does_not_exists_error)

    table = await TableDAO.find_one_or_none(id=current_client.table_id)

    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    table_name = table.name

    await callback.message.answer(
        one_client_message(client=current_client, table_name=table_name),
        reply_markup=await get_clients_data_unit_to_edit(client_id=client_id),
    )
