from datetime import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from bot.config import settings
from bot.database.connections.dao import ConnectionDAO
from bot.database.users.dao import UserDAO
from bot.keyboards.admin_keyboards.inline.notification_keyboards import get_marzban_accec_keyboard
from bot.templates.user_templates.message_templates import wait_for_admin_message, marzban_day_limit_message
from bot.templates.user_templates.errors_templates import added_connection_error
from bot.templates.user_templates.keyboards_templates import get_new_connection_text
from bot.templates.admin_templates.messages_templates import request_to_connect_message
from bot.keyboards.user_keyboards.inline.marzban_user_info_keyboards import enter_os_keyboard
from bot.templates.user_templates.message_templates import enter_os_message

router = Router()

ADD_CONNECTION_PATTERN = '_add_connection'

@router.message(F.text == get_new_connection_text)
async def handle_os_selection(message: Message):

    user = await UserDAO.find_one_or_none(tg_id = message.from_user.id)
    if user.marzban_requests_today > settings.MARZBAN_REQUEST_DAY_LIMIT:
        return await message.answer(marzban_day_limit_message)
    return await message.answer(enter_os_message, reply_markup=enter_os_keyboard)


@router.callback_query(lambda c: c.data.endswith(ADD_CONNECTION_PATTERN))
async def handle_os_selection(callback: CallbackQuery):
    
    await callback.answer()

    user_tg_id = callback.from_user.id

    user = await UserDAO.find_one_or_none(tg_id = user_tg_id)

    if user.marzban_requests_today > settings.MARZBAN_REQUEST_DAY_LIMIT:
        return await callback.message.answer(marzban_day_limit_message)
    
    marzban_requests_today = user.marzban_requests_today + 1 

    updated_user = await UserDAO.update(
        model_id=user.id, 
        marzban_requests_today = marzban_requests_today,
        last_marzban_request_date = datetime.now()
    )

    user_os = callback.data.split("_")[0]  
    username = callback.from_user.username or '-'

    added_connection = await ConnectionDAO.add(
        user_tg_id = user_tg_id,
        os = user_os,
        tg_username = username
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




    





