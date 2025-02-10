import re
from random import randint

from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.config import settings
from bot.database.connections.dao import ConnectionDAO
from bot.utils.marzban.marzban_manager import create_user, get_user
from bot.templates.admin_templates.errors_templates import(
    marzban_user_add_error,
    marzban_link_get_error
)
from bot.templates.admin_templates.messages_templates import marzban_user_added_message

router = Router()

ACCEPT_MARZBAN_PATTERN = r"^accept_marzban_(\d+)$"


@router.callback_query(F.data.regexp(ACCEPT_MARZBAN_PATTERN))
async def handle_accept_marzban_client(callback: CallbackQuery):
    await callback.answer()

    match = re.match(ACCEPT_MARZBAN_PATTERN, callback.data)
    connection_id = int(match.group(1))

    connection = await ConnectionDAO.find_one_or_none(id=connection_id)

    new_username = f"{connection.os}_{connection.user_tg_id}_{randint(10000,99999)}" 

    new_marzban_user = await create_user(
        username = new_username
    )

    if not new_marzban_user:
        return await callback.message.answer(marzban_user_add_error) 

    marzban_user = await get_user(
        username = new_username
    )

    if not marzban_user:
        return await callback.message.answer(marzban_link_get_error) 

    link = marzban_user.links[0]

    updated_connection = await ConnectionDAO.update(
        model_id=connection.id,
        link = link
    )

    if not updated_connection:
        return await callback.message.answer(marzban_link_get_error) 
    
    await callback.message.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.message.bot.send_message(
        settings.ADMIN_TG_ID,
        marzban_user_added_message(username=connection.nickname, tg_id=connection.user_tg_id), 
    )

    await callback.message.bot.send_message(connection.user_tg_id ,f"...")
    return await callback.message.bot.send_message(connection.user_tg_id ,f"{link}")
