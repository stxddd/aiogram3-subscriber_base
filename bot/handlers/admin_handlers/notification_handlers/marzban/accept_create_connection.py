from aiogram import Router
from aiogram.types import Message

from bot.config import settings
from bot.database.connections.dao import ConnectionDAO
from bot.database.clients.dao import ClientDAO

from bot.database.servers.dao import ServerDAO
from bot.handlers.user_handlers.instruction_handlers.get_instructions import get_instruction
from bot.templates.user_templates.message_templates import (
    you_are_successfully_connected_message
)
from bot.templates.user_templates.errors_templates import server_does_not_exists_error
from bot.utils.marzban.marzban_manager import create_user, get_user
from bot.templates.admin_templates.errors_templates import (
    marzban_user_add_error, marzban_link_get_error
)
from bot.keyboards.user_keyboards.reply.main_keyboards import main_keyboard as user_main_keyboard
from bot.keyboards.admin_keyboards.reply.main_keyboards import main_keyboard as admin_main_keyboard
from bot.templates.admin_templates.errors_templates import (
    connection_does_not_exist_error, 
)

router = Router()


async def handle_accept_marzban_client(message: Message, connection_id):
    
    connection = await ConnectionDAO.find_one_or_none(id=connection_id)
    if not connection:
        return await message.answer(connection_does_not_exist_error)
    
    client = await ClientDAO.find_one_or_none(id = connection.client_id)
    
    server = await ServerDAO.find_by_id(connection.server_id)
    
    count_of_clients = server.count_of_clients + 1
    updated_server = await ServerDAO.update(server.id, count_of_clients = count_of_clients)
    
    if not server:
        return await message.answer(server_does_not_exists_error)
    
    connection_name = connection.name
    port = server.port
    

    new_marzban_user = await create_user(
        port = port,
        username=connection_name,
        date_to=connection.date_to
    )

    if not new_marzban_user:
        return await message.answer(marzban_user_add_error) 

    marzban_user = await get_user(
        port = port,
        username=connection_name
    )

    if not marzban_user:
        return await message.answer(marzban_link_get_error)

    link = marzban_user.links[0]

    updated_connection = await ConnectionDAO.update(
        model_id=connection.id,
        marzban_link=link,
    )

    if not updated_connection:
        return await message.answer(marzban_link_get_error)

    await message.bot.send_message(
        client.tg_id, 
        get_instruction(user_os=connection.os_name)
    )
    
    await message.bot.send_message(
        client.tg_id,
        f'`{link}`',
        reply_markup=user_main_keyboard if client.tg_id != settings.ADMIN_TG_ID else admin_main_keyboard, 
        parse_mode="MARKDOWN"
    )

    return await message.bot.send_message(
        client.tg_id,
        you_are_successfully_connected_message(date_to=connection.date_to)
    )
