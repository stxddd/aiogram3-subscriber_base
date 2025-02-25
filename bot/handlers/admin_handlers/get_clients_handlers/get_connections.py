import re

from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.database.connections.dao import ConnectionDAO
from bot.database.clients.dao import ClientDAO

from bot.keyboards.admin_keyboards.inline.connections_keyboards import get_connection_info_keyboard, get_connections_to_edit
from bot.templates.admin_templates.errors_templates import (
    client_does_not_exists_error,
    table_dose_not_exists_error,
)
from bot.templates.admin_templates.messages_templates import (
    admin_link_message,
    client_dose_not_have_connections_message,
    client_info_message,
    connection_info_message,
)
from bot.decorators.admin_required import admin_required

router = Router()

EDIT_CONNECTION_PAGE_PATTERN = r"^edit_connections_page_(\d+)_(\d+)$"
EDIT_CONNECTION_PATTERN = r"^get_connection_(\d+)$"
GET_CONNECTION_TO_EDIT_PATTERN = r"^get_connection_to_edit_(\d+)$"

GET_CONNECTION_LINK_PATTERN = r"^get_marzban_link_(\d+)$"

@router.callback_query(F.data.regexp(EDIT_CONNECTION_PAGE_PATTERN))
@admin_required
async def handle_pagination(callback: CallbackQuery):
    await callback.answer()

    match = re.match(EDIT_CONNECTION_PAGE_PATTERN, callback.data)
    client_id = int(match.group(1))
    page = int(match.group(2))

    await callback.message.edit_reply_markup(
        reply_markup=await get_connections_to_edit(client_id=client_id, page=page)
    )


@router.callback_query(F.data.regexp(EDIT_CONNECTION_PATTERN))
@admin_required
async def handle_get_clients(callback: CallbackQuery):
    await callback.answer()

    match = re.match(EDIT_CONNECTION_PATTERN, callback.data)
    client_id = int(match.group(1))

    client = await ClientDAO.find_one_or_none(id=client_id)
    if not client:
        return await callback.message.answer(table_dose_not_exists_error)

    client_username = client.username
    
    connections = await ConnectionDAO.find_all(client_id=client_id)

    if not connections:
        return await callback.message.answer(
           client_dose_not_have_connections_message(client_username)
        )

    connections_count = len(connections)

    await callback.message.answer(
        client_info_message(client_username, connections_count),
        reply_markup=await get_connections_to_edit(client_id=client_id, page=1),
    )


@router.callback_query(F.data.regexp(GET_CONNECTION_TO_EDIT_PATTERN))
@admin_required
async def handle_get_client(callback: CallbackQuery):
    await callback.answer()

    match = re.match(GET_CONNECTION_TO_EDIT_PATTERN, callback.data)
    connection_id = int(match.group(1))
    
    current_connection = await ConnectionDAO.find_by_id(model_id=connection_id)
    if not current_connection:
        return await callback.message.answer(client_dose_not_have_connections_message)

    client = await ClientDAO.find_one_or_none(id=current_connection.client_id)
    if not client:
        return await callback.message.answer(client_does_not_exists_error)
    
    client_username = client.username
    connections = await ConnectionDAO.find_all(client_id=client.id)
    
    await callback.message.answer(
       connection_info_message(current_connection, client_username),
        reply_markup=await get_connection_info_keyboard(connection_id=current_connection.id),
    )


@router.callback_query(F.data.regexp(GET_CONNECTION_LINK_PATTERN))
@admin_required
async def handle_get_link(callback: CallbackQuery):
    await callback.answer()
    
    match = re.match(GET_CONNECTION_LINK_PATTERN, callback.data)
    connection_id = int(match.group(1))
    
    current_connection = await ConnectionDAO.find_by_id(model_id=connection_id)
    if not current_connection:
        return await callback.message.answer(client_dose_not_have_connections_message)
    
    client = await ClientDAO.find_one_or_none(id=current_connection.client_id)
    if not client:
        return await callback.message.answer(client_does_not_exists_error)
    
    link = current_connection.marzban_link
    
    return await callback.message.answer(text = admin_link_message(current_connection, client.username))