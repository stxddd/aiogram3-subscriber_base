from datetime import date

from aiogram import Router
from aiogram.types import Message

from bot.database.connections.dao import ConnectionDAO
from bot.database.clients.dao import ClientDAO
from bot.templates.admin_templates.messages_templates import (
    successful_extension_message,
)
from bot.utils.marzban.marzban_manager import extend_user
from bot.templates.admin_templates.errors_templates import (
    connection_does_not_exist_error,
)

router = Router()
    
    
async def handle_reject_marzban_client(message: Message, connection_id: int, price: int, date_to: date):
    connection = await ConnectionDAO.find_one_or_none(id=connection_id)
    
    if not connection:
        return await message.answer(connection_does_not_exist_error)
    
    client = await ClientDAO.find_one_or_none(id=connection.client_id)

    old_date_to = connection.date_to
    old_price = connection.price
    
    new_date_to = date_to
    new_price = price
    
    updated_connection = await ConnectionDAO.update(
        model_id=connection.id,
        price=new_price,
        date_to=new_date_to
    )

    updated_marzban_user = await extend_user(username=connection.name, date_to=new_date_to)
    
    await message.answer(
        successful_extension_message(
            username=client.username,
            connection=connection,
            new_date_to=new_date_to,
            old_date_to=old_date_to,
            old_price=old_price,
            new_price=new_price,
        )
    )
    
    await message.delete_message()
    