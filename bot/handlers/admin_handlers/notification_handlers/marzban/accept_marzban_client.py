import re
from random import randint

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.config import settings
from bot.database.connections.dao import ConnectionDAO
from bot.database.tables.clients.dao import ClientDAO
from bot.handlers.user_handlers.instruction_handlers.get_instructions import get_instruction
from bot.keyboards.admin_keyboards.inline.table_keyboards import get_my_tables_for_marzban_keyboard
from bot.utils.marzban.marzban_manager import create_user, get_user
from bot.templates.admin_templates.errors_templates import(
    marzban_user_add_error,
    marzban_link_get_error
)
from bot.templates.admin_templates.errors_templates import adding_data_error
from bot.templates.admin_templates.messages_templates import marzban_user_added_message, pick_table_for_client_message
from bot.keyboards.user_keyboards.reply.main_keyboards import main_keyboard as user_main_keyboard
from bot.keyboards.admin_keyboards.reply.main_keyboards import main_keyboard as admin_main_keyboard
from bot.decorators.admin_required import admin_required

router = Router()

ACCEPT_MARZBAN_PATTERN = r"^accept_marzban_(\d+)$"
GET_TABLE_FOR_CLIENT = r"get_(\d+)_for_marzban_client"


@router.callback_query(F.data.regexp(ACCEPT_MARZBAN_PATTERN))
@admin_required
async def handle_get_table_for_marzban_client(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    match = re.match(ACCEPT_MARZBAN_PATTERN, callback.data)
    connection_id = int(match.group(1))
    
    connection = await ConnectionDAO.find_one_or_none(id=connection_id)
    
    await state.update_data(connection_id=connection_id)
    await callback.message.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await callback.message.bot.send_message(
        settings.ADMIN_TG_ID,
        pick_table_for_client_message(username = connection.tg_username),
        reply_markup=await get_my_tables_for_marzban_keyboard(callback.from_user.id),
    )
    
    


@router.callback_query(F.data.regexp(GET_TABLE_FOR_CLIENT))
@admin_required
async def handle_accept_marzban_client(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    connection_id = data.get('connection_id')
    
    
    match = re.match(GET_TABLE_FOR_CLIENT, callback.data)
    table_id = int(match.group(1))

    connection = await ConnectionDAO.find_one_or_none(id=connection_id)

    new_username = f"{connection.os}_{connection.tg_id}_{randint(10000,99999)}" 

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
        model_id = connection.id,
        link = link
    )

    if not updated_connection:
        return await callback.message.answer(marzban_link_get_error) 
    
    
    new_client = await ClientDAO.add(
        name = connection.tg_username,
        table_id = table_id,
        tg_id = connection.tg_id,
    )
    
    if not new_client:
        new_client = await ClientDAO.find_one_or_none(tg_id = connection.tg_id)
        if not new_client:
            return await callback.message.answer(adding_data_error)
    
    await callback.message.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    
    await callback.message.bot.send_message(
        settings.ADMIN_TG_ID,
        marzban_user_added_message(username=connection.tg_username, date_to=connection.date_to), 
    )

    await callback.message.bot.send_message(
        connection.tg_id, 
        get_instruction(user_os=connection.os)
    )
    
    return await callback.message.bot.send_message(
        connection.tg_id,
        link,
        reply_markup = user_main_keyboard if connection.tg_id != settings.ADMIN_TG_ID else admin_main_keyboard
    )

