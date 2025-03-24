import re

from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.database.connections.dao import ConnectionDAO
from bot.database.clients.dao import ClientDAO
from bot.keyboards.admin_keyboards.inline.clients_keyboards import get_clients_for_edit
from bot.keyboards.admin_keyboards.inline.connections_keyboards import get_connections_to_edit
from bot.templates.admin_templates.errors_templates import (
    client_does_not_exists_error,
)
from bot.templates.admin_templates.messages_templates import (
    one_client_message,
    table_base_info_message,
)
from bot.decorators.admin_required import admin_required

router = Router()

EDIT_PAGE_PATTERN = r"^edit_page_(\d+)$"
EDIT_CLIENT_PATTERN = r"^edit_client"
GET_CLIENT_TO_EDIT_PATTERN = r"^get_client_to_edit_(\d+)$"


@router.callback_query(F.data.regexp(EDIT_PAGE_PATTERN))
@admin_required
async def handle_pagination(callback: CallbackQuery):
    await callback.answer()

    match = re.match(EDIT_PAGE_PATTERN, callback.data)
    page = int(match.group(1))

    clients = await ClientDAO.find_all()

    if not clients:
        return await callback.message.answer(client_does_not_exists_error)

    await callback.message.edit_reply_markup(
        reply_markup=await get_clients_for_edit(clients=clients, page=page)
    )


@router.callback_query(F.data.regexp(EDIT_CLIENT_PATTERN))
@admin_required
async def handle_get_clients(callback: CallbackQuery):
    await callback.answer()

    clients = await ClientDAO.find_all()

    if not clients:
        return await callback.message.answer(client_does_not_exists_error)

    await callback.message.answer(
        table_base_info_message(clients_count=len(clients)),
        reply_markup=await get_clients_for_edit(clients=clients, page=1),
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

    connections = await ConnectionDAO.find_all_with_marzban_link(client_id=current_client.id)

    await callback.message.answer(
        one_client_message(client=current_client, connections=connections),
        reply_markup=await get_connections_to_edit(client_id=client_id),
    )
