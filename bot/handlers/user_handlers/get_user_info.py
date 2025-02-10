from aiogram import Router
from aiogram.types import CallbackQuery

from bot.config import settings
from bot.database.connections.dao import ConnectionDAO
from bot.keyboards.admin_keyboards.inline.notification_keyboards import get_marzban_accec_keyboard
from bot.templates.user_templates.message_templates import wait_for_admin_message
from bot.templates.user_templates.errors_templates import added_connection_error
from bot.templates.admin_templates.messages_templates import request_to_connect_message

router = Router()

ADD_CONNECTION_PATTERN = '_add_connection'

@router.callback_query(lambda c: c.data.endswith(ADD_CONNECTION_PATTERN))
async def handle_os_selection(callback: CallbackQuery):
    await callback.answer()

    user_tg_id = callback.from_user.id
    user_os = callback.data.split("_")[0]  
    username = callback.from_user.username or '-'

    added_connection = await ConnectionDAO.add(
        user_tg_id = user_tg_id,
        os = user_os,
        nickname = username
    )

    if not added_connection:        
        return await callback.message.answer(added_connection_error)
    
    await callback.message.delete()
    await callback.message.answer(wait_for_admin_message)

    return await callback.message.bot.send_message(
        settings.ADMIN_TG_ID, 
        request_to_connect_message(username=username, tg_id=user_tg_id), 
        reply_markup=await get_marzban_accec_keyboard(connection_id=added_connection.id)
    )




    





