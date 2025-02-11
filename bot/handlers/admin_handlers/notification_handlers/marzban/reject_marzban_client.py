import re

from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.config import settings
from bot.database.connections.dao import ConnectionDAO
from bot.templates.admin_templates.messages_templates import marzban_user_rejected_message
from bot.templates.user_templates.message_templates import rejected_message
from bot.decorators.admin_required import admin_required

router = Router()

REJECT_MARZBAN_PATTERN = r"^reject_marzban_(\d+)$"


@router.callback_query(F.data.regexp(REJECT_MARZBAN_PATTERN))
@admin_required
async def handle_reject_marzban_client(callback: CallbackQuery):
    await callback.answer()

    match = re.match(REJECT_MARZBAN_PATTERN, callback.data)
    connection_id = int(match.group(1))

    connection = await ConnectionDAO.find_by_id(model_id=connection_id)

    if connection:
        deleted_connection = await ConnectionDAO.delete(id=connection_id)

    await callback.message.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.message.bot.send_message(
        settings.ADMIN_TG_ID, marzban_user_rejected_message(username=connection.tg_username, tg_id=connection.user_tg_id), 
    )

    return await callback.message.bot.send_message(connection.user_tg_id ,rejected_message)