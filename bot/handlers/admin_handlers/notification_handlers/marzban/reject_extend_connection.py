import re

from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.config import settings
from bot.database.clients.dao import ClientDAO
from bot.database.connections.dao import ConnectionDAO
from bot.templates.admin_templates.messages_templates import marzban_user_rejected_message
from bot.templates.user_templates.message_templates import rejected_message
from bot.decorators.admin_required import admin_required
from bot.templates.admin_templates.errors_templates import (
    marzban_user_add_error,
    marzban_link_get_error
)

router = Router()

REJECT_EXTEND_PATTERN = r"^reject_extend_(\d+)$"


@router.callback_query(F.data.regexp(REJECT_EXTEND_PATTERN))
@admin_required
async def handle_reject_extend_connection(callback: CallbackQuery):
    await callback.answer()

    match = re.match(REJECT_EXTEND_PATTERN, callback.data)
    connection_id = int(match.group(1))

    connection = await ConnectionDAO.find_by_id(model_id=connection_id)
    if not connection:
        return await callback.message.answer(marzban_link_get_error)
    
    client = await ClientDAO.find_one_or_none(id=connection.client_id)
    if not client:
        return await callback.message.answer(marzban_user_add_error)

    await callback.message.delete()

    await callback.message.bot.send_message(
        settings.ADMIN_TG_ID, 
        marzban_user_rejected_message(username=client.username)
    )
    
    await callback.message.bot.send_message(client.tg_id, rejected_message)

    await callback.message.bot.send_message(
        settings.ADMIN_TG_ID,
        marzban_user_rejected_message(username=client.username)
    )
