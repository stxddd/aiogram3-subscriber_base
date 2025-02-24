import re

from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.database.connections.dao import ConnectionDAO
from bot.database.tables.clients.dao import ClientDAO
from bot.database.tables.dao import TableDAO
from bot.keyboards.admin_keyboards.inline.clients_keyboards import (
    get_clients_data_unit_to_edit,
    get_clients_for_edit,
)
from bot.templates.admin_templates.errors_templates import (
    client_does_not_exists_error,
    table_dose_not_exists_error,
)
from bot.templates.admin_templates.messages_templates import (
    one_client_message,
    table_base_info_message,
    table_has_no_clients_message,
)
from bot.decorators.admin_required import admin_required

router = Router()

EDIT_PAGE_PATTERN = r"^edit_page_(\d+)_(\d+)$"
EDIT_CLIENT_PATTERN = r"^edit_client_(\d+)$"
GET_CLIENT_TO_EDIT_PATTERN = r"^get_client_to_edit_(\d+)$"

@router.callback_query(F.data.regexp(EDIT_PAGE_PATTERN))
@admin_required
async def handle_pagination(callback: CallbackQuery):
    await callback.answer()

    match = re.match(EDIT_PAGE_PATTERN, callback.data)
    table_id = int(match.group(1))
    page = int(match.group(2))

    await callback.message.edit_reply_markup(
        reply_markup=await get_clients_for_edit(table_id=table_id, page=page)
    )


@router.callback_query(F.data.regexp(EDIT_CLIENT_PATTERN))
@admin_required
async def handle_get_clients(callback: CallbackQuery):
    await callback.answer()

    match = re.match(EDIT_CLIENT_PATTERN, callback.data)
    table_id = int(match.group(1))

    table = await TableDAO.find_one_or_none(id=table_id)
    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    table_name = table.name
    clients = await ClientDAO.find_all(table_id=table_id)

    if not clients:
        return await callback.message.answer(
            table_has_no_clients_message(table_name=table_name)
        )

    clients_count = len(clients)

    await callback.message.answer(
        table_base_info_message(table_name=table_name, clients_count=clients_count, all_prices=0),
        reply_markup=await get_clients_for_edit(table_id=table_id, page=1),
    )


@router.callback_query(F.data.regexp(GET_CLIENT_TO_EDIT_PATTERN))
@admin_required
async def handle_get_client(callback: CallbackQuery):
    await callback.answer()

    match = re.match(GET_CLIENT_TO_EDIT_PATTERN, callback.data)
    client_id = int(match.group(1))

    current_client = await ClientDAO.find_by_id(model_id=client_id)

    if not current_client:
        return await callback.message.answer(client_does_not_exists_error)

    table = await TableDAO.find_one_or_none(id=current_client.table_id)

    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    table_name = table.name
    
    connections = await ConnectionDAO.find_all(tg_id=current_client.tg_id)

    await callback.message.answer(
        one_client_message(client=current_client, table_name=table_name, connections = connections),
        reply_markup=await get_clients_data_unit_to_edit(client_id=client_id),
    )
