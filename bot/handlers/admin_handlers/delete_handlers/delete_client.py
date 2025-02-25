import re

from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.database.connections.dao import ConnectionDAO
from bot.database.clients.dao import ClientDAO
from bot.database.tables.dao import TableDAO
from bot.keyboards.admin_keyboards.inline.utils_keyboards import yes_or_not_delte_client_keyboard
from bot.templates.admin_templates.errors_templates import (
    client_does_not_exists_error,
    table_dose_not_exists_error,
)
from bot.templates.admin_templates.messages_templates import (
    are_you_sure_to_delete_client_message,
    client_are_deleted_message,
    client_are_not_deleted_message,
)
from bot.decorators.admin_required import admin_required

router = Router()

PREPARE_TO_DELETE_CLIENT_PATTERN = r"^prepare_to_delete_client_(\d+)$"
DELETE_CLIENT_PATTERN = r"^delete_client_(\d+)$"


@router.callback_query(F.data.regexp(PREPARE_TO_DELETE_CLIENT_PATTERN))
@admin_required
async def handle_prepare_to_delete_client(callback: CallbackQuery):
    await callback.answer()

    match = re.match(PREPARE_TO_DELETE_CLIENT_PATTERN, callback.data)
    client_id = int(match.group(1))

    current_client = await ClientDAO.find_by_id(client_id)
    if not current_client:
        return await callback.message.answer(client_does_not_exists_error)

    table = await TableDAO.find_one_or_none(id=current_client.table_id)

    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    table_name = table.name

    connections = await ConnectionDAO.find_all(client_id=current_client.id)
    
    return await callback.message.answer(
        are_you_sure_to_delete_client_message(table_name=table_name, client=current_client, connections=connections),
        reply_markup=await yes_or_not_delte_client_keyboard(client_id=client_id),
    )


@router.callback_query(F.data.regexp(DELETE_CLIENT_PATTERN))
@admin_required
async def handle_delete_clietn(callback: CallbackQuery):
    await callback.answer()

    match = re.match(DELETE_CLIENT_PATTERN, callback.data)
    
    client_id = int(match.group(1))
    current_client = await ClientDAO.find_by_id(client_id)
    
    if not current_client:
        return await callback.message.answer(client_does_not_exists_error)
    
    connections = await ConnectionDAO.find_all(client_id=current_client.id)
    for connection in connections:
        await ConnectionDAO.delete(id=connection.id)

    table = await TableDAO.find_one_or_none(id=current_client.table_id)

    if not table:
        return await callback.message.answer(table_dose_not_exists_error)

    table_name = table.name
    connections = await ConnectionDAO.find_all(client_id=current_client.id)
    delte_client = await ClientDAO.delete(id=client_id)

    if not delte_client:
        return await callback.message.answer(
            client_are_not_deleted_message(table_name=table_name, client=current_client)
        )

    return await callback.message.answer(
        client_are_deleted_message(client=current_client, table_name=table_name, connections=connections)
    )
