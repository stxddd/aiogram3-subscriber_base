import re


from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.config import settings
from bot.database.connections.dao import ConnectionDAO
from bot.database.clients.dao import ClientDAO
from bot.database.users.dao import UserDAO
from bot.handlers.user_handlers.instruction_handlers.get_instructions import get_instruction
from bot.keyboards.admin_keyboards.inline.notification_keyboards import get_marzban_access_keyboard
from bot.keyboards.admin_keyboards.inline.table_keyboards import get_my_tables_for_marzban_keyboard
from bot.templates.user_templates.message_templates import you_are_successfully_connected_message, wait_for_admin_message
from bot.utils.marzban.marzban_manager import create_user, get_user
from bot.templates.admin_templates.errors_templates import(
    marzban_user_add_error,
    marzban_link_get_error
)
from bot.templates.admin_templates.errors_templates import adding_data_error
from bot.templates.admin_templates.messages_templates import marzban_user_added_message, pick_table_for_client_message, request_to_connect_message
from bot.keyboards.user_keyboards.reply.main_keyboards import main_keyboard as user_main_keyboard
from bot.keyboards.admin_keyboards.reply.main_keyboards import main_keyboard as admin_main_keyboard
from bot.templates.user_templates.errors_templates import auth_error
from bot.decorators.admin_required import admin_required
from bot.templates.admin_templates.errors_templates import (
    connection_dose_not_exists_error,
    client_does_not_exists_error
)

router = Router()

ACCEPT_MARZBAN_PATTERN = r"^accept_marzban_(\d+)$"
GET_TABLE_FOR_CLIENT = r"get_(\d+)_for_marzban_client"

CONNECT_PAYMENT_CHECK_COMPLETED = r"accept_connect_payment_check_completed_(\d+)_(\d+)"

router = Router()

@router.callback_query(F.data.regexp(CONNECT_PAYMENT_CHECK_COMPLETED))
async def handle_payment_check_completed(callback: CallbackQuery):
    await callback.answer()
    
    match = re.match(CONNECT_PAYMENT_CHECK_COMPLETED, callback.data)
    connection_id = int(match.group(1))
    key = int(match.group(2))

    connection = await ConnectionDAO.find_by_id(model_id=connection_id)
    if not connection:
        return await callback.message.answer(connection_dose_not_exists_error)
    
    client = await ClientDAO.find_one_or_none(id = connection.client_id)
    if not client:
         return await callback.message.answer(client_does_not_exists_error)
    
    await callback.message.bot.send_message(
        client.tg_id,
        wait_for_admin_message
    )
    
    return await callback.message.bot.send_message(
        settings.ADMIN_TG_ID,
        request_to_connect_message(username=client.username, connection=connection, key = key),
        reply_markup=await get_marzban_access_keyboard(connection_id=connection_id)
    )
    

@router.callback_query(F.data.regexp(ACCEPT_MARZBAN_PATTERN))
@admin_required
async def handle_get_table_for_marzban_client(callback: CallbackQuery, state: FSMContext):
    "Обрабатывет новый запрос на подклбчевние, спрашивает в какую базу добавить пользователя"
    await callback.answer()
    
    user = await UserDAO.find_one_or_none(tg_id = callback.from_user.id)

    if not user:
        return await callback.message.answer(auth_error)
    
    match = re.match(ACCEPT_MARZBAN_PATTERN, callback.data)
    connection_id = int(match.group(1))
    
    connection = await ConnectionDAO.find_one_or_none(id=connection_id)
    
    client = await ClientDAO.find_one_or_none(id = connection.client_id)
    
    await state.update_data(connection_id=connection_id)
    await callback.message.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.message.bot.send_message(
        settings.ADMIN_TG_ID,
        pick_table_for_client_message(username = client.username),
        reply_markup=await get_my_tables_for_marzban_keyboard(user_id = user.id),
    )
    

@router.callback_query(F.data.regexp(GET_TABLE_FOR_CLIENT))
@admin_required
async def handle_accept_marzban_client(callback: CallbackQuery, state: FSMContext):
    "Добавляет пользователя в базу, отправляет ему ключ на подключение"
    await callback.answer()
    data = await state.get_data()

    match = re.match(GET_TABLE_FOR_CLIENT, callback.data)
    table_id = int(match.group(1))
    
    connection_id = data.get('connection_id')
    connection = await ConnectionDAO.find_one_or_none(id=connection_id)
    
    client = await ClientDAO.find_one_or_none(id = connection.client_id)
    
    if not client:
        return await callback.message.answer(adding_data_error)
    
    if client.table_id != table_id:
        added_client = await ClientDAO.update(
            model_id = client.id,
            table_id = table_id
        )  

    connection_name = connection.name

    new_marzban_user = await create_user(
        username = connection_name,
        date_to=connection.date_to
    )

    if not new_marzban_user:
        return await callback.message.answer(marzban_user_add_error) 

    marzban_user = await get_user(
        username = connection_name
    )

    if not marzban_user:
        return await callback.message.answer(marzban_link_get_error) 

    link = marzban_user.links[0]

    updated_connection = await ConnectionDAO.update(
        model_id = connection.id,
        marzban_link = link,
    )

    if not updated_connection:
        return await callback.message.answer(marzban_link_get_error) 
    
    await callback.message.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    
    await callback.message.bot.send_message(
        settings.ADMIN_TG_ID,
        marzban_user_added_message(username=client.username, date_to=connection.date_to), 
    )

    await callback.message.bot.send_message(
        client.tg_id, 
        get_instruction(user_os=connection.os_name)
    )
    
    await callback.message.bot.send_message(
        client.tg_id,
        f'`{link}`',
        reply_markup = user_main_keyboard if client.tg_id != settings.ADMIN_TG_ID else admin_main_keyboard, parse_mode="MARKDOWN"
    )

    return await callback.bot.send_message(
        client.tg_id,
        you_are_successfully_connected_message(date_to=connection.date_to)
    )
